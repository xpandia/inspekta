"""
Inspekta -- Industrial AI Defect Detection Engine
==================================================
Computer-vision pipeline for real-time manufacturing defect detection.
Supports crack, scratch, deformation, and discoloration classification
with bounding-box localisation and confidence scoring.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional, Sequence

import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from PIL import Image, ImageDraw
from torchvision import models, transforms
from torchvision.ops import nms

logger = logging.getLogger("inspekta.detector")

# ---------------------------------------------------------------------------
# Domain types
# ---------------------------------------------------------------------------

class DefectType(str, Enum):
    CRACK = "crack"
    SCRATCH = "scratch"
    DEFORMATION = "deformation"
    DISCOLORATION = "discoloration"

NUM_CLASSES = len(DefectType) + 1  # +1 for background


@dataclass
class BoundingBox:
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def width(self) -> float:
        return self.x_max - self.x_min

    @property
    def height(self) -> float:
        return self.y_max - self.y_min

    @property
    def area(self) -> float:
        return self.width * self.height

    def to_dict(self) -> dict:
        return {
            "x_min": round(self.x_min, 2),
            "y_min": round(self.y_min, 2),
            "x_max": round(self.x_max, 2),
            "y_max": round(self.y_max, 2),
        }


@dataclass
class Detection:
    defect_type: DefectType
    confidence: float
    bbox: BoundingBox
    severity: str = ""  # low / medium / high / critical

    def __post_init__(self) -> None:
        if not self.severity:
            self.severity = self._classify_severity()

    def _classify_severity(self) -> str:
        if self.confidence >= 0.90:
            return "critical"
        if self.confidence >= 0.75:
            return "high"
        if self.confidence >= 0.55:
            return "medium"
        return "low"

    def to_dict(self) -> dict:
        return {
            "defect_type": self.defect_type.value,
            "confidence": round(self.confidence, 4),
            "severity": self.severity,
            "bbox": self.bbox.to_dict(),
        }


@dataclass
class InspectionResult:
    image_id: str
    detections: List[Detection] = field(default_factory=list)
    inference_time_ms: float = 0.0
    image_width: int = 0
    image_height: int = 0
    pass_fail: str = "PASS"

    def __post_init__(self) -> None:
        self.pass_fail = "FAIL" if self.detections else "PASS"

    def to_dict(self) -> dict:
        return {
            "image_id": self.image_id,
            "pass_fail": self.pass_fail,
            "num_defects": len(self.detections),
            "detections": [d.to_dict() for d in self.detections],
            "inference_time_ms": round(self.inference_time_ms, 2),
            "image_width": self.image_width,
            "image_height": self.image_height,
        }


# ---------------------------------------------------------------------------
# Model architecture
# ---------------------------------------------------------------------------

class _ConvBlock(nn.Module):
    """Conv -> BatchNorm -> ReLU with optional residual shortcut."""

    def __init__(self, in_ch: int, out_ch: int, stride: int = 1, residual: bool = False):
        super().__init__()
        self.residual = residual
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, stride=stride, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_ch)
        self.shortcut: Optional[nn.Module] = None
        if residual and (stride != 1 or in_ch != out_ch):
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_ch, out_ch, 1, stride=stride, bias=False),
                nn.BatchNorm2d(out_ch),
            )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        identity = x
        out = F.relu(self.bn1(self.conv1(x)), inplace=True)
        out = self.bn2(self.conv2(out))
        if self.residual:
            if self.shortcut is not None:
                identity = self.shortcut(identity)
            out = out + identity
        return F.relu(out, inplace=True)


class _FPN(nn.Module):
    """Lightweight Feature Pyramid Network for multi-scale detection."""

    def __init__(self, in_channels_list: List[int], out_channels: int = 128):
        super().__init__()
        self.lateral = nn.ModuleList([
            nn.Conv2d(c, out_channels, 1) for c in in_channels_list
        ])
        self.smooth = nn.ModuleList([
            nn.Conv2d(out_channels, out_channels, 3, padding=1) for _ in in_channels_list
        ])

    def forward(self, features: List[torch.Tensor]) -> List[torch.Tensor]:
        laterals = [l(f) for l, f in zip(self.lateral, features)]
        # top-down pathway
        for i in range(len(laterals) - 1, 0, -1):
            laterals[i - 1] = laterals[i - 1] + F.interpolate(
                laterals[i], size=laterals[i - 1].shape[2:], mode="nearest"
            )
        return [s(l) for s, l in zip(self.smooth, laterals)]


class DefectDetectionNet(nn.Module):
    """
    Compact single-shot detector tailored for industrial defect detection.

    Architecture:
      - ResNet-style backbone with 4 stages
      - FPN neck for multi-scale feature fusion
      - Parallel classification + regression heads

    Input : (B, 3, 512, 512)
    Output: class logits  (B, N_anchors, NUM_CLASSES)
            bbox offsets  (B, N_anchors, 4)
    """

    ANCHOR_SIZES = [32, 64, 128, 256]
    ANCHOR_RATIOS = [0.5, 1.0, 2.0]
    INPUT_SIZE = 512

    def __init__(self, use_pretrained_backbone: bool = True) -> None:
        super().__init__()
        if use_pretrained_backbone:
            # Use a pretrained ResNet18 as backbone for transfer learning
            resnet = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
            self.stem = nn.Sequential(
                resnet.conv1,
                resnet.bn1,
                resnet.relu,
                resnet.maxpool,
            )
            self.stage1 = resnet.layer1  # 64 channels
            self.stage2 = resnet.layer2  # 128 channels
            self.stage3 = resnet.layer3  # 256 channels
            self.stage4 = resnet.layer4  # 512 channels
            logger.info("Backbone initialised from pretrained ResNet18 (ImageNet1K_V1)")
        else:
            # backbone from scratch
            self.stem = nn.Sequential(
                nn.Conv2d(3, 64, 7, stride=2, padding=3, bias=False),
                nn.BatchNorm2d(64),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(3, stride=2, padding=1),
            )
            self.stage1 = self._make_stage(64, 64, blocks=2, stride=1)
            self.stage2 = self._make_stage(64, 128, blocks=2, stride=2)
            self.stage3 = self._make_stage(128, 256, blocks=2, stride=2)
            self.stage4 = self._make_stage(256, 512, blocks=2, stride=2)

        # FPN
        self.fpn = _FPN([64, 128, 256, 512], out_channels=128)

        # detection heads (shared across FPN levels)
        num_anchors = len(self.ANCHOR_RATIOS)
        self.cls_head = nn.Sequential(
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(inplace=True),
            nn.Conv2d(128, num_anchors * NUM_CLASSES, 3, padding=1),
        )
        self.reg_head = nn.Sequential(
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, 3, padding=1), nn.ReLU(inplace=True),
            nn.Conv2d(128, num_anchors * 4, 3, padding=1),
        )

        self._init_weights()

    # ---- helpers -----------------------------------------------------------

    @staticmethod
    def _make_stage(in_ch: int, out_ch: int, blocks: int, stride: int) -> nn.Sequential:
        layers = [_ConvBlock(in_ch, out_ch, stride=stride, residual=True)]
        for _ in range(1, blocks):
            layers.append(_ConvBlock(out_ch, out_ch, residual=True))
        return nn.Sequential(*layers)

    def _init_weights(self) -> None:
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode="fan_out", nonlinearity="relu")
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.ones_(m.weight)
                nn.init.zeros_(m.bias)
        # bias init for classification head (reduce false-positive rate at start)
        prior_prob = 0.01
        bias_value = -np.log((1 - prior_prob) / prior_prob)
        nn.init.constant_(self.cls_head[-1].bias, bias_value)

    # ---- forward -----------------------------------------------------------

    def forward(self, x: torch.Tensor):
        c1 = self.stage1(self.stem(x))
        c2 = self.stage2(c1)
        c3 = self.stage3(c2)
        c4 = self.stage4(c3)

        fpn_feats = self.fpn([c1, c2, c3, c4])

        cls_preds, reg_preds = [], []
        num_anchors = len(self.ANCHOR_RATIOS)
        for feat in fpn_feats:
            B, _, H, W = feat.shape
            cls = self.cls_head(feat)  # (B, A*C, H, W)
            reg = self.reg_head(feat)  # (B, A*4, H, W)
            cls = cls.view(B, num_anchors, NUM_CLASSES, H, W).permute(0, 1, 3, 4, 2)
            reg = reg.view(B, num_anchors, 4, H, W).permute(0, 1, 3, 4, 2)
            cls_preds.append(cls.reshape(B, -1, NUM_CLASSES))
            reg_preds.append(reg.reshape(B, -1, 4))

        return torch.cat(cls_preds, dim=1), torch.cat(reg_preds, dim=1)


# ---------------------------------------------------------------------------
# Anchor generation
# ---------------------------------------------------------------------------

def _generate_anchors(
    image_size: int,
    feature_sizes: List[int],
    anchor_sizes: List[int],
    anchor_ratios: List[float],
    device: torch.device,
) -> torch.Tensor:
    """Return (N, 4) tensor of anchors in (cx, cy, w, h) format."""
    all_anchors = []
    for feat_size, anchor_size in zip(feature_sizes, anchor_sizes):
        stride = image_size / feat_size
        for gy in range(feat_size):
            for gx in range(feat_size):
                cx = (gx + 0.5) * stride
                cy = (gy + 0.5) * stride
                for ratio in anchor_ratios:
                    w = anchor_size * np.sqrt(ratio)
                    h = anchor_size / np.sqrt(ratio)
                    all_anchors.append([cx, cy, w, h])
    return torch.tensor(all_anchors, dtype=torch.float32, device=device)


def _decode_boxes(anchors: torch.Tensor, offsets: torch.Tensor) -> torch.Tensor:
    """Decode predicted offsets relative to anchors -> (x1, y1, x2, y2)."""
    cx = anchors[:, 0] + offsets[:, 0] * anchors[:, 2]
    cy = anchors[:, 1] + offsets[:, 1] * anchors[:, 3]
    w = anchors[:, 2] * torch.exp(offsets[:, 2].clamp(max=4.0))
    h = anchors[:, 3] * torch.exp(offsets[:, 3].clamp(max=4.0))
    x1 = cx - w / 2
    y1 = cy - h / 2
    x2 = cx + w / 2
    y2 = cy + h / 2
    return torch.stack([x1, y1, x2, y2], dim=1)


# ---------------------------------------------------------------------------
# Image preprocessing
# ---------------------------------------------------------------------------

class ImagePreprocessor:
    """Deterministic preprocessing pipeline for inference."""

    def __init__(self, target_size: int = 512):
        self.target_size = target_size
        self.transform = transforms.Compose([
            transforms.Resize((target_size, target_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ])

    def __call__(self, image: Image.Image) -> torch.Tensor:
        return self.transform(image.convert("RGB"))

    def preprocess_cv2(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess an OpenCV BGR frame."""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)
        return self(pil_img)

    def preprocess_batch(self, images: Sequence[Image.Image]) -> torch.Tensor:
        return torch.stack([self(img) for img in images])


# ---------------------------------------------------------------------------
# Synthetic data generation (demo / testing)
# ---------------------------------------------------------------------------

def generate_synthetic_defect_image(
    width: int = 512,
    height: int = 512,
    num_defects: int = 3,
    seed: Optional[int] = None,
) -> tuple[Image.Image, list[dict]]:
    """
    Generate a synthetic industrial surface image with artificial defects
    for demo and testing purposes.

    Returns:
        (PIL image, list of ground-truth annotations)
        Each annotation: {"defect_type": str, "bbox": [x_min, y_min, x_max, y_max]}
    """
    rng = np.random.RandomState(seed)

    # Create a base surface texture (brushed metal look)
    base = rng.randint(160, 200, (height, width), dtype=np.uint8)
    # Add horizontal streaks for realism
    for _ in range(30):
        y = rng.randint(0, height)
        intensity = rng.randint(-20, 20)
        thickness = rng.randint(1, 3)
        base[max(0, y - thickness):y + thickness, :] += intensity
    base = np.clip(base, 0, 255).astype(np.uint8)
    img_array = np.stack([base, base, base], axis=-1)  # grayscale -> RGB

    annotations: list[dict] = []
    defect_types = list(DefectType)

    for _ in range(num_defects):
        defect_type = defect_types[rng.randint(0, len(defect_types))]
        # Random bbox
        cx = rng.randint(60, width - 60)
        cy = rng.randint(60, height - 60)
        w = rng.randint(30, 80)
        h = rng.randint(30, 80)
        x_min = max(0, cx - w // 2)
        y_min = max(0, cy - h // 2)
        x_max = min(width, cx + w // 2)
        y_max = min(height, cy + h // 2)

        if defect_type == DefectType.CRACK:
            # Draw a jagged dark line
            pts = []
            x, y = x_min, rng.randint(y_min, y_max)
            for step in range(10):
                pts.append((x, y))
                x += (x_max - x_min) // 10
                y += rng.randint(-5, 6)
                y = np.clip(y, y_min, y_max)
            for i in range(len(pts) - 1):
                cv2.line(img_array, pts[i], pts[i + 1], (40, 40, 40), rng.randint(1, 3))

        elif defect_type == DefectType.SCRATCH:
            # Draw a thin diagonal line
            cv2.line(img_array, (x_min, y_min), (x_max, y_max),
                     (80, 80, 80), rng.randint(1, 2))

        elif defect_type == DefectType.DEFORMATION:
            # Draw a warped ellipse
            cv2.ellipse(img_array, (cx, cy), (w // 2, h // 2), rng.randint(0, 180),
                        0, 360, (100, 100, 120), -1)

        elif defect_type == DefectType.DISCOLORATION:
            # Draw a colour patch
            color = (rng.randint(100, 180), rng.randint(80, 140), rng.randint(60, 120))
            cv2.rectangle(img_array, (x_min, y_min), (x_max, y_max), color, -1)
            # Blend with original
            alpha = 0.5
            roi = img_array[y_min:y_max, x_min:x_max]
            patch = np.full_like(roi, color)
            img_array[y_min:y_max, x_min:x_max] = (
                alpha * patch + (1 - alpha) * roi
            ).astype(np.uint8)

        annotations.append({
            "defect_type": defect_type.value,
            "bbox": [int(x_min), int(y_min), int(x_max), int(y_max)],
        })

    # Add slight Gaussian noise
    noise = rng.normal(0, 5, img_array.shape).astype(np.int16)
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    pil_image = Image.fromarray(img_array)
    return pil_image, annotations


# ---------------------------------------------------------------------------
# Inference engine
# ---------------------------------------------------------------------------

class DefectDetector:
    """
    High-level inference engine wrapping model, preprocessing, and
    post-processing into a single ``detect`` call.

    Usage::

        detector = DefectDetector()
        detector.load_model("weights/best.pt")   # or use random weights for demo
        detector.warm_up()
        result = detector.detect(pil_image, image_id="part-0042")
    """

    DEFECT_LABELS = {i + 1: dt for i, dt in enumerate(DefectType)}

    def __init__(
        self,
        confidence_threshold: float = 0.35,
        nms_iou_threshold: float = 0.45,
        device: Optional[str] = None,
    ):
        if device is None:
            if torch.cuda.is_available():
                self.device = torch.device("cuda")
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = torch.device("mps")
            else:
                self.device = torch.device("cpu")
        else:
            self.device = torch.device(device)

        self.confidence_threshold = confidence_threshold
        self.nms_iou_threshold = nms_iou_threshold
        self.preprocessor = ImagePreprocessor(target_size=DefectDetectionNet.INPUT_SIZE)
        self.model: Optional[DefectDetectionNet] = None
        self._anchors: Optional[torch.Tensor] = None
        self._warmed_up = False

        logger.info("DefectDetector initialised (device=%s)", self.device)

    # ---- model lifecycle ---------------------------------------------------

    def load_model(self, weights_path: Optional[str] = None, use_pretrained_backbone: bool = True) -> None:
        """Load model weights from disk, or initialise with a pretrained backbone (demo).

        When no weights_path is provided the model uses a pretrained ResNet18
        backbone (ImageNet) so that the feature extractor produces meaningful
        representations even without task-specific training.
        """
        self.model = DefectDetectionNet(use_pretrained_backbone=use_pretrained_backbone).to(self.device)
        if weights_path and Path(weights_path).is_file():
            state = torch.load(weights_path, map_location=self.device, weights_only=True)
            self.model.load_state_dict(state)
            logger.info("Loaded weights from %s", weights_path)
        else:
            logger.warning("No weights loaded -- running with random initialisation (demo mode)")
        self.model.eval()

        # pre-compute anchors
        feat_sizes = [
            DefectDetectionNet.INPUT_SIZE // s
            for s in [4, 8, 16, 32]
        ]
        self._anchors = _generate_anchors(
            DefectDetectionNet.INPUT_SIZE,
            feat_sizes,
            DefectDetectionNet.ANCHOR_SIZES,
            DefectDetectionNet.ANCHOR_RATIOS,
            self.device,
        )

    def warm_up(self, iterations: int = 3) -> None:
        """Run dummy inference to warm up GPU / JIT caches."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        dummy = torch.randn(1, 3, DefectDetectionNet.INPUT_SIZE, DefectDetectionNet.INPUT_SIZE, device=self.device)
        with torch.no_grad():
            for _ in range(iterations):
                self.model(dummy)
        self._warmed_up = True
        logger.info("Model warm-up complete (%d iterations)", iterations)

    # ---- inference ---------------------------------------------------------

    @torch.no_grad()
    def detect(self, image: Image.Image, image_id: str = "unknown") -> InspectionResult:
        """Run defect detection on a single PIL image."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        orig_w, orig_h = image.size
        tensor = self.preprocessor(image).unsqueeze(0).to(self.device)

        t0 = time.perf_counter()
        cls_logits, reg_offsets = self.model(tensor)
        inference_ms = (time.perf_counter() - t0) * 1000

        detections = self._post_process(
            cls_logits[0], reg_offsets[0], orig_w, orig_h
        )

        result = InspectionResult(
            image_id=image_id,
            detections=detections,
            inference_time_ms=inference_ms,
            image_width=orig_w,
            image_height=orig_h,
        )
        result.pass_fail = "FAIL" if detections else "PASS"
        return result

    @torch.no_grad()
    def detect_batch(
        self, images: Sequence[Image.Image], image_ids: Optional[Sequence[str]] = None,
    ) -> List[InspectionResult]:
        """Run detection on a batch of images."""
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        if image_ids is None:
            image_ids = [f"batch-{i}" for i in range(len(images))]

        sizes = [(img.size[0], img.size[1]) for img in images]
        batch_tensor = self.preprocessor.preprocess_batch(images).to(self.device)

        t0 = time.perf_counter()
        cls_logits, reg_offsets = self.model(batch_tensor)
        total_ms = (time.perf_counter() - t0) * 1000
        per_image_ms = total_ms / len(images)

        results = []
        for i in range(len(images)):
            orig_w, orig_h = sizes[i]
            detections = self._post_process(cls_logits[i], reg_offsets[i], orig_w, orig_h)
            res = InspectionResult(
                image_id=image_ids[i],
                detections=detections,
                inference_time_ms=per_image_ms,
                image_width=orig_w,
                image_height=orig_h,
            )
            res.pass_fail = "FAIL" if detections else "PASS"
            results.append(res)
        return results

    @torch.no_grad()
    def detect_frame(
        self,
        frame: np.ndarray,
        image_id: str = "frame",
        confidence_threshold: Optional[float] = None,
    ) -> InspectionResult:
        """Run detection on a raw OpenCV BGR frame (for video streams).

        Args:
            confidence_threshold: If provided, overrides the detector's default
                threshold for this call only (thread-safe).
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")

        orig_h, orig_w = frame.shape[:2]
        tensor = self.preprocessor.preprocess_cv2(frame).unsqueeze(0).to(self.device)

        t0 = time.perf_counter()
        cls_logits, reg_offsets = self.model(tensor)
        inference_ms = (time.perf_counter() - t0) * 1000

        conf_thresh = confidence_threshold if confidence_threshold is not None else self.confidence_threshold
        detections = self._post_process(cls_logits[0], reg_offsets[0], orig_w, orig_h, confidence_threshold=conf_thresh)
        result = InspectionResult(
            image_id=image_id,
            detections=detections,
            inference_time_ms=inference_ms,
            image_width=orig_w,
            image_height=orig_h,
        )
        result.pass_fail = "FAIL" if detections else "PASS"
        return result

    # ---- post-processing ---------------------------------------------------

    def _post_process(
        self,
        cls_logits: torch.Tensor,
        reg_offsets: torch.Tensor,
        orig_w: int,
        orig_h: int,
        confidence_threshold: Optional[float] = None,
    ) -> List[Detection]:
        """NMS + thresholding + coordinate rescaling."""
        assert self._anchors is not None
        conf_thresh = confidence_threshold if confidence_threshold is not None else self.confidence_threshold

        probs = F.softmax(cls_logits, dim=-1)  # (N_anchors, NUM_CLASSES)
        # ignore background class (index 0)
        fg_probs = probs[:, 1:]  # (N_anchors, NUM_CLASSES-1)
        max_probs, max_classes = fg_probs.max(dim=1)  # both (N_anchors,)

        # threshold
        keep_mask = max_probs > conf_thresh
        if not keep_mask.any():
            return []

        scores = max_probs[keep_mask]
        class_ids = max_classes[keep_mask] + 1  # shift back (0 was bg)
        boxes = _decode_boxes(self._anchors[keep_mask], reg_offsets[keep_mask])

        # clamp to image bounds (model space)
        boxes[:, 0::2].clamp_(0, DefectDetectionNet.INPUT_SIZE)
        boxes[:, 1::2].clamp_(0, DefectDetectionNet.INPUT_SIZE)

        # NMS per class
        keep_indices = nms(boxes, scores, self.nms_iou_threshold)
        boxes = boxes[keep_indices]
        scores = scores[keep_indices]
        class_ids = class_ids[keep_indices]

        # rescale to original image coordinates
        scale_x = orig_w / DefectDetectionNet.INPUT_SIZE
        scale_y = orig_h / DefectDetectionNet.INPUT_SIZE
        boxes[:, 0] *= scale_x
        boxes[:, 2] *= scale_x
        boxes[:, 1] *= scale_y
        boxes[:, 3] *= scale_y

        detections: List[Detection] = []
        for i in range(len(scores)):
            cid = int(class_ids[i].item())
            defect_type = self.DEFECT_LABELS.get(cid)
            if defect_type is None:
                continue
            detections.append(Detection(
                defect_type=defect_type,
                confidence=float(scores[i].item()),
                bbox=BoundingBox(
                    x_min=float(boxes[i, 0].item()),
                    y_min=float(boxes[i, 1].item()),
                    x_max=float(boxes[i, 2].item()),
                    y_max=float(boxes[i, 3].item()),
                ),
            ))

        # sort by confidence descending
        detections.sort(key=lambda d: d.confidence, reverse=True)
        return detections
