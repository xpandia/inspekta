"""
Inspekta -- FastAPI Backend
============================
REST + WebSocket API for industrial defect detection, analytics,
predictive maintenance, and factory-line management.
"""

from __future__ import annotations

import asyncio
import io
import json
import logging
import os
import secrets
import time
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import cv2
import numpy as np
from fastapi import (
    Depends,
    FastAPI,
    File,
    Header,
    HTTPException,
    Query,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel, Field

from detector import DefectDetector, DefectType, InspectionResult

# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

# API key is read from the INSPEKTA_API_KEY env var.  If not set a random key
# is generated at startup and printed to the console so the operator can use it.
_API_KEY: str = os.environ.get("INSPEKTA_API_KEY", "")
if not _API_KEY:
    _API_KEY = secrets.token_urlsafe(32)

MAX_UPLOAD_BYTES = 20 * 1024 * 1024  # 20 MB per file


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> str:
    """Dependency that validates the X-API-Key header on every request."""
    if not secrets.compare_digest(x_api_key, _API_KEY):
        raise HTTPException(status_code=401, detail="Invalid or missing API key")
    return x_api_key

logger = logging.getLogger("inspekta.server")
logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(name)s  %(levelname)s  %(message)s")

# ---------------------------------------------------------------------------
# In-memory stores (swap for a real DB in production)
# ---------------------------------------------------------------------------

_inspection_history: List[Dict[str, Any]] = []
_alerts: List[Dict[str, Any]] = []
_factory_lines: Dict[str, Dict[str, Any]] = {}
_maintenance_schedule: List[Dict[str, Any]] = []

# Default factory line for demo
_factory_lines["line-1"] = {
    "id": "line-1",
    "name": "Assembly Line Alpha",
    "camera_url": None,
    "active": True,
    "created_at": datetime.now(timezone.utc).isoformat(),
    "total_inspections": 0,
    "total_defects": 0,
}

# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------

class FactoryLineCreate(BaseModel):
    name: str
    camera_url: Optional[str] = None

class FactoryLineUpdate(BaseModel):
    name: Optional[str] = None
    camera_url: Optional[str] = None
    active: Optional[bool] = None

class AlertAck(BaseModel):
    alert_id: str

class MaintenanceCreate(BaseModel):
    line_id: str
    scheduled_date: str
    description: str
    priority: str = Field(default="medium", pattern="^(low|medium|high|critical)$")

class ROIRequest(BaseModel):
    inspections_per_day: int = 1000
    defect_rate_before: float = Field(default=0.05, ge=0.0, le=1.0)
    defect_rate_after: float = Field(default=0.005, ge=0.0, le=1.0)
    cost_per_defect_usd: float = 150.0
    system_cost_usd: float = 250_000.0

class AnalyticsQuery(BaseModel):
    line_id: Optional[str] = None
    last_n: int = Field(default=100, ge=1, le=10_000)

# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

detector: Optional[DefectDetector] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global detector
    logger.info("Starting Inspekta backend ...")
    if not os.environ.get("INSPEKTA_API_KEY"):
        logger.info("Generated API key (set INSPEKTA_API_KEY env var to override): %s", _API_KEY)
    detector = DefectDetector()
    detector.load_model()  # demo mode — pretrained ResNet18 backbone, no task-specific weights
    detector.warm_up()
    logger.info("Detector ready.")
    yield
    logger.info("Shutting down Inspekta backend.")


app = FastAPI(
    title="Inspekta API",
    version="1.0.0",
    description="Industrial AI Quality Control & Predictive Maintenance",
    lifespan=lifespan,
    dependencies=[Depends(verify_api_key)],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _record_inspection(result: InspectionResult, line_id: str = "line-1") -> Dict[str, Any]:
    """Persist inspection result and trigger alerts if needed."""
    record = result.to_dict()
    record["timestamp"] = datetime.now(timezone.utc).isoformat()
    record["line_id"] = line_id
    _inspection_history.append(record)

    # update line stats
    line = _factory_lines.get(line_id)
    if line:
        line["total_inspections"] = line.get("total_inspections", 0) + 1
        line["total_defects"] = line.get("total_defects", 0) + len(result.detections)

    # generate alerts for critical / high severity defects
    for det in result.detections:
        if det.severity in ("critical", "high"):
            alert = {
                "id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "line_id": line_id,
                "image_id": result.image_id,
                "defect_type": det.defect_type.value,
                "severity": det.severity,
                "confidence": round(det.confidence, 4),
                "acknowledged": False,
            }
            _alerts.append(alert)
            logger.warning("ALERT: %s defect (%s) on %s", det.severity, det.defect_type.value, line_id)

    return record


def _compute_analytics(line_id: Optional[str], last_n: int) -> Dict[str, Any]:
    """Aggregate stats from inspection history."""
    records = _inspection_history
    if line_id:
        records = [r for r in records if r.get("line_id") == line_id]
    records = records[-last_n:]

    total = len(records)
    if total == 0:
        return {"total_inspections": 0, "defect_rate": 0.0, "defects_by_type": {}, "avg_inference_ms": 0.0}

    defect_count = sum(1 for r in records if r["pass_fail"] == "FAIL")
    defects_by_type: Dict[str, int] = defaultdict(int)
    severity_counts: Dict[str, int] = defaultdict(int)
    total_inference = 0.0

    for r in records:
        total_inference += r.get("inference_time_ms", 0.0)
        for d in r.get("detections", []):
            defects_by_type[d["defect_type"]] += 1
            severity_counts[d["severity"]] += 1

    return {
        "total_inspections": total,
        "pass_count": total - defect_count,
        "fail_count": defect_count,
        "defect_rate": round(defect_count / total, 4) if total else 0.0,
        "defects_by_type": dict(defects_by_type),
        "severity_distribution": dict(severity_counts),
        "avg_inference_ms": round(total_inference / total, 2),
    }


def _predictive_maintenance_score(line_id: str, window: int = 200) -> Dict[str, Any]:
    """
    Heuristic predictive-maintenance scoring based on recent defect trends.
    In production this would be a trained time-series model.
    """
    records = [r for r in _inspection_history if r.get("line_id") == line_id][-window:]
    if len(records) < 10:
        return {"line_id": line_id, "health_score": 1.0, "recommendation": "Insufficient data"}

    total = len(records)
    defect_count = sum(1 for r in records if r["pass_fail"] == "FAIL")
    defect_rate = defect_count / total

    # check trend (compare first half vs second half)
    mid = total // 2
    first_half_rate = sum(1 for r in records[:mid] if r["pass_fail"] == "FAIL") / mid
    second_half_rate = sum(1 for r in records[mid:] if r["pass_fail"] == "FAIL") / (total - mid)

    health_score = max(0.0, 1.0 - defect_rate * 5)  # rough mapping
    trend = "stable"
    if second_half_rate > first_half_rate * 1.5:
        trend = "degrading"
        health_score *= 0.7
    elif second_half_rate < first_half_rate * 0.5:
        trend = "improving"

    if health_score < 0.3:
        recommendation = "Immediate maintenance required"
        priority = "critical"
    elif health_score < 0.55:
        recommendation = "Schedule maintenance within 48 hours"
        priority = "high"
    elif health_score < 0.8:
        recommendation = "Plan maintenance in next cycle"
        priority = "medium"
    else:
        recommendation = "No action needed"
        priority = "low"

    return {
        "line_id": line_id,
        "health_score": round(health_score, 3),
        "defect_rate": round(defect_rate, 4),
        "trend": trend,
        "recommendation": recommendation,
        "priority": priority,
        "sample_size": total,
    }


# ---------------------------------------------------------------------------
# REST endpoints
# ---------------------------------------------------------------------------

@app.get("/health", dependencies=[])
async def health_check():
    return {"status": "ok", "model_loaded": detector is not None and detector.model is not None}


# ---- Image analysis -------------------------------------------------------

@app.post("/api/v1/inspect", response_model=None)
async def inspect_image(
    file: UploadFile = File(...),
    line_id: str = Query("line-1"),
):
    """Upload a single image for defect inspection."""
    if detector is None or detector.model is None:
        raise HTTPException(503, "Model not ready")

    if line_id not in _factory_lines:
        raise HTTPException(404, f"Factory line '{line_id}' not found")

    try:
        contents = await file.read()
        if len(contents) > MAX_UPLOAD_BYTES:
            raise HTTPException(413, f"File too large ({len(contents)} bytes). Maximum is {MAX_UPLOAD_BYTES} bytes.")
        image = Image.open(io.BytesIO(contents))
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(400, f"Invalid image file: {exc}")

    image_id = f"{line_id}_{uuid.uuid4().hex[:8]}"
    result = detector.detect(image, image_id=image_id)
    record = _record_inspection(result, line_id=line_id)
    return record


@app.post("/api/v1/inspect/batch", response_model=None)
async def inspect_batch(
    files: List[UploadFile] = File(...),
    line_id: str = Query("line-1"),
):
    """Upload multiple images for batch inspection."""
    if detector is None or detector.model is None:
        raise HTTPException(503, "Model not ready")

    if line_id not in _factory_lines:
        raise HTTPException(404, f"Factory line '{line_id}' not found")

    images, ids = [], []
    for f in files:
        try:
            contents = await f.read()
            if len(contents) > MAX_UPLOAD_BYTES:
                raise HTTPException(413, f"File '{f.filename}' too large. Maximum is {MAX_UPLOAD_BYTES} bytes.")
            images.append(Image.open(io.BytesIO(contents)))
            ids.append(f"{line_id}_{uuid.uuid4().hex[:8]}")
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(400, f"Invalid image file ({f.filename}): {exc}")

    results = detector.detect_batch(images, image_ids=ids)
    records = [_record_inspection(r, line_id=line_id) for r in results]
    return {"count": len(records), "results": records}


# ---- History & Analytics --------------------------------------------------

@app.get("/api/v1/inspections")
async def list_inspections(
    line_id: Optional[str] = None,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    records = _inspection_history
    if line_id:
        records = [r for r in records if r.get("line_id") == line_id]
    total = len(records)
    page = records[offset: offset + limit]
    return {"total": total, "limit": limit, "offset": offset, "results": page}


@app.get("/api/v1/analytics")
async def get_analytics(
    line_id: Optional[str] = None,
    last_n: int = Query(100, ge=1, le=10_000),
):
    return _compute_analytics(line_id, last_n)


@app.get("/api/v1/dashboard")
async def dashboard():
    """Aggregated dashboard data across all factory lines."""
    lines_summary = []
    for lid, line in _factory_lines.items():
        pm = _predictive_maintenance_score(lid)
        lines_summary.append({
            "line": line,
            "analytics": _compute_analytics(lid, 200),
            "maintenance": pm,
        })

    unack_alerts = [a for a in _alerts if not a["acknowledged"]]
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "lines": lines_summary,
        "pending_alerts": len(unack_alerts),
        "recent_alerts": unack_alerts[-10:],
        "upcoming_maintenance": _maintenance_schedule[:5],
    }


# ---- Alerts ---------------------------------------------------------------

@app.get("/api/v1/alerts")
async def list_alerts(acknowledged: Optional[bool] = None, limit: int = Query(50, ge=1, le=500)):
    alerts = _alerts
    if acknowledged is not None:
        alerts = [a for a in alerts if a["acknowledged"] == acknowledged]
    return {"total": len(alerts), "alerts": alerts[-limit:]}


@app.post("/api/v1/alerts/acknowledge")
async def acknowledge_alert(body: AlertAck):
    for a in _alerts:
        if a["id"] == body.alert_id:
            a["acknowledged"] = True
            return {"status": "ok", "alert": a}
    raise HTTPException(404, "Alert not found")


# ---- Factory lines --------------------------------------------------------

@app.get("/api/v1/lines")
async def list_lines():
    return {"lines": list(_factory_lines.values())}


@app.post("/api/v1/lines")
async def create_line(body: FactoryLineCreate):
    lid = f"line-{uuid.uuid4().hex[:6]}"
    _factory_lines[lid] = {
        "id": lid,
        "name": body.name,
        "camera_url": body.camera_url,
        "active": True,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "total_inspections": 0,
        "total_defects": 0,
    }
    return _factory_lines[lid]


@app.patch("/api/v1/lines/{line_id}")
async def update_line(line_id: str, body: FactoryLineUpdate):
    if line_id not in _factory_lines:
        raise HTTPException(404, "Line not found")
    line = _factory_lines[line_id]
    if body.name is not None:
        line["name"] = body.name
    if body.camera_url is not None:
        line["camera_url"] = body.camera_url
    if body.active is not None:
        line["active"] = body.active
    return line


@app.delete("/api/v1/lines/{line_id}")
async def delete_line(line_id: str):
    if line_id not in _factory_lines:
        raise HTTPException(404, "Line not found")
    del _factory_lines[line_id]
    return {"status": "deleted", "line_id": line_id}


# ---- Predictive maintenance -----------------------------------------------

@app.get("/api/v1/maintenance/predict/{line_id}")
async def predict_maintenance(line_id: str):
    if line_id not in _factory_lines:
        raise HTTPException(404, "Line not found")
    return _predictive_maintenance_score(line_id)


@app.get("/api/v1/maintenance/schedule")
async def get_maintenance_schedule():
    return {"schedule": _maintenance_schedule}


@app.post("/api/v1/maintenance/schedule")
async def create_maintenance_task(body: MaintenanceCreate):
    if body.line_id not in _factory_lines:
        raise HTTPException(404, "Line not found")
    task = {
        "id": str(uuid.uuid4()),
        "line_id": body.line_id,
        "scheduled_date": body.scheduled_date,
        "description": body.description,
        "priority": body.priority,
        "status": "scheduled",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _maintenance_schedule.append(task)
    _maintenance_schedule.sort(key=lambda t: t["scheduled_date"])
    return task


# ---- ROI ------------------------------------------------------------------

@app.post("/api/v1/roi")
async def calculate_roi(body: ROIRequest):
    """Estimate return on investment for deploying Inspekta."""
    daily_units = body.inspections_per_day
    yearly_units = daily_units * 365

    defects_before = yearly_units * body.defect_rate_before
    defects_after = yearly_units * body.defect_rate_after
    defects_caught = defects_before - defects_after

    annual_savings = defects_caught * body.cost_per_defect_usd
    payback_days = (body.system_cost_usd / (annual_savings / 365)) if annual_savings > 0 else float("inf")
    three_year_roi = ((annual_savings * 3 - body.system_cost_usd) / body.system_cost_usd) * 100

    return {
        "annual_defects_prevented": int(defects_caught),
        "annual_savings_usd": round(annual_savings, 2),
        "payback_period_days": round(payback_days, 1),
        "three_year_roi_percent": round(three_year_roi, 1),
        "system_cost_usd": body.system_cost_usd,
    }


# ---------------------------------------------------------------------------
# WebSocket -- real-time video stream analysis
# ---------------------------------------------------------------------------

@app.websocket("/ws/stream/{line_id}")
async def video_stream(ws: WebSocket, line_id: str):
    """
    Real-time video frame analysis over WebSocket.

    Protocol (binary):
      Client sends raw JPEG/PNG frames as binary messages.
      Server replies with JSON inspection results.

    Protocol (text / JSON):
      Client sends {"action": "configure", "confidence_threshold": 0.4, ...}
      to adjust detector parameters mid-stream.
    """
    if line_id not in _factory_lines:
        await ws.close(code=4004, reason="Line not found")
        return

    await ws.accept()
    logger.info("WebSocket connected for line %s", line_id)

    frame_count = 0
    local_conf_threshold = 0.35

    try:
        while True:
            message = await ws.receive()

            # --- text message: configuration update -------------------------
            if "text" in message and message["text"]:
                try:
                    payload = json.loads(message["text"])
                except json.JSONDecodeError:
                    await ws.send_json({"error": "Invalid JSON"})
                    continue

                if payload.get("action") == "configure":
                    if "confidence_threshold" in payload:
                        local_conf_threshold = float(payload["confidence_threshold"])
                    await ws.send_json({"status": "configured", "confidence_threshold": local_conf_threshold})
                    continue

                if payload.get("action") == "ping":
                    await ws.send_json({"action": "pong", "timestamp": datetime.now(timezone.utc).isoformat()})
                    continue

            # --- binary message: image frame --------------------------------
            if "bytes" in message and message["bytes"]:
                frame_data = message["bytes"]
                frame_count += 1

                try:
                    np_arr = np.frombuffer(frame_data, dtype=np.uint8)
                    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
                    if frame is None:
                        await ws.send_json({"error": "Could not decode frame"})
                        continue
                except Exception as exc:
                    await ws.send_json({"error": f"Frame decode error: {exc}"})
                    continue

                if detector is None or detector.model is None:
                    await ws.send_json({"error": "Model not ready"})
                    continue

                image_id = f"{line_id}_frame_{frame_count}"
                # Pass threshold as parameter to avoid race conditions
                # across concurrent WebSocket connections.  Also run in
                # a thread so blocking PyTorch inference does not stall
                # the async event loop.
                result = await asyncio.to_thread(
                    detector.detect_frame, frame, image_id,
                    confidence_threshold=local_conf_threshold,
                )

                _record_inspection(result, line_id=line_id)
                await ws.send_json(result.to_dict())

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected for line %s (frames processed: %d)", line_id, frame_count)
    except Exception as exc:
        logger.error("WebSocket error on line %s: %s", line_id, exc, exc_info=True)
        try:
            await ws.close(code=1011, reason=str(exc)[:120])
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
