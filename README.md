# Inspekta

**Every defect caught is a failure prevented.**

---

## Vision

We believe factories should have perfect eyesight. Inspekta gives them exactly that — AI vision that never blinks, never tires, and never lets a defect through.

---

## The Problem

Manufacturing is bleeding. Every year:

- **$3.1 trillion** lost globally to poor quality control (ASQ)
- **30%** of production waste stems from undetected defects
- **72 hours** average unplanned downtime per plant annually — each hour costing up to $260,000
- Human inspectors catch only **80%** of surface defects under optimal conditions

The status quo is broken: manual inspection is slow, inconsistent, and expensive. Legacy automated systems are rigid, require months to reconfigure, and cannot adapt to new product lines.

---

## The Solution

Inspekta is an **AI-powered visual inspection and predictive maintenance platform** purpose-built for industrial manufacturing.

It combines real-time computer vision with predictive analytics to:

1. **Detect defects** at superhuman accuracy (99.7%+) across any production line
2. **Predict failures** before they happen by analyzing equipment degradation patterns
3. **Reduce waste** by catching issues at the earliest possible stage

One platform. Every defect. Zero excuses.

---

## How It Works

### 1. Capture
High-resolution cameras and edge sensors are deployed on the production line. Images stream in real time — every unit, every angle, every time.

### 2. Analyze
Our AI models process each frame in under 50ms. Convolutional neural networks trained on millions of defect samples classify anomalies by type, severity, and root cause. Predictive models monitor equipment health and flag degradation trends.

### 3. Act
Operators receive instant alerts with annotated images, severity scores, and recommended actions. Dashboards surface trends. The system learns continuously — every correction makes it sharper.

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Computer Vision** | Python, PyTorch, OpenCV |
| **ML Backbone** | ResNet18 (pretrained, ImageNet) + FPN + detection heads |
| **Backend API** | FastAPI (Python), WebSocket for real-time video |
| **Frontend** | Single-page HTML/CSS/JS (responsive landing page + ROI calculator) |
| **Data Store** | In-memory (prototype — swap for a database in production) |

---

## Architecture

```
[Camera / Sensor Array]
        |
   [Image Upload or WebSocket Stream]
        |
   [FastAPI Backend]  ──  PyTorch CNN inference, alerting, analytics
        |
   [In-Memory Store]  ──  Inspection history, alerts, factory lines
        |
   [HTML Dashboard / Landing Page]  ──  Defect feed, ROI calculator
```

---

## Industries

- **Automotive** — Surface defects, weld integrity, paint quality, assembly verification
- **Electronics** — PCB soldering inspection, component placement, micro-crack detection
- **Food & Beverage** — Packaging integrity, contamination detection, label verification
- **Pharmaceuticals** — Tablet inspection, blister pack verification, serialization
- **Metals & Materials** — Surface finish, dimensional accuracy, corrosion detection

---

## Key Metrics (Target)

| Metric | Value |
|---|---|
| Defect detection accuracy | 99.7%+ |
| Inference latency | < 50ms per frame |
| False positive rate | < 0.3% |
| Reduction in scrap/waste | 40-60% |
| ROI payback period | < 6 months |

---

## Team Structure

| Role | Responsibility |
|---|---|
| **ML Engineer** | Model training, dataset curation, edge optimization |
| **Backend Engineer** | API design, streaming pipeline, database architecture |
| **Frontend Engineer** | Dashboard, real-time visualization, UX |
| **Domain Expert** | Manufacturing process knowledge, validation criteria |

---

## Hackathon Submission Checklist

- [ ] Project registered on DoraHacks (MunichTech EXPO AI Innovation Hackathon 2026)
- [ ] README with vision, architecture, and tech stack
- [ ] Working demo — live defect detection on sample images/video
- [ ] Landing page deployed
- [ ] Pitch deck (max 10 slides)
- [ ] 3-minute video walkthrough
- [ ] GitHub repository with clean commit history
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Model performance benchmarks
- [ ] Edge deployment proof-of-concept

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/your-org/inspekta.git
cd inspekta

# Backend
cd src/backend
pip install -r requirements.txt
uvicorn server:app --reload
# API docs available at http://localhost:8000/docs
# An API key is printed to the console on first start.
# Set INSPEKTA_API_KEY env var to use your own key.

# Frontend (no build step required)
# Open src/frontend/index.html in your browser.
```

---

## License

MIT License. Built for MunichTech EXPO AI Innovation Hackathon 2026.

---

<p align="center"><strong>Inspekta</strong> — Because quality is not an act, it is a habit.</p>
