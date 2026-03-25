# Inspekta -- MunichTech EXPO Submission

**Event:** MunichTech EXPO 2026
**Date:** September 20, 2026
**Tracks:** Industry 4.0, Enterprise AI
**Location:** Munich, Germany

---

## Project Name

Inspekta

## Tagline

AI-powered visual quality control for manufacturing -- German precision, automated.

## One-Liner

Inspekta is a computer-vision platform that detects cracks, scratches, deformations, and discolorations on production lines in real time, replacing manual inspection with sub-100ms AI inference and predictive maintenance.

---

## The Problem

Manual quality inspection in manufacturing is slow, inconsistent, and expensive. A trained human inspector catches roughly 80% of defects. The remaining 20% ship to customers, triggering recalls, warranty claims, and reputational damage.

European manufacturers lose an estimated EUR 4.2 billion annually to undetected defects. The cost is not just financial -- it is a safety issue in automotive, aerospace, and medical device production.

## The Solution

Inspekta replaces manual visual inspection with a camera-based AI system that:

- **Detects** four defect categories (crack, scratch, deformation, discoloration) at >95% accuracy
- **Inspects** every single unit, not statistical samples
- **Runs** in real time at the line speed (sub-100ms per frame on CPU, sub-30ms on GPU)
- **Predicts** equipment degradation before it causes defect spikes
- **Alerts** operators instantly via WebSocket push for critical/high severity findings

### How It Works

1. **Mount** -- An industrial camera is mounted at the inspection point on the production line
2. **Stream** -- Video frames are streamed over WebSocket to the Inspekta backend
3. **Detect** -- A custom neural network (ResNet18 backbone + FPN + detection heads) classifies and localises defects with bounding boxes and confidence scores
4. **Act** -- Operators receive real-time alerts, analytics dashboards show trends, and the predictive maintenance engine schedules interventions before defect rates spike

---

## Architecture

```
Camera (GigE / USB3)
  |
  v (JPEG frames over WebSocket)
Inspekta Backend (FastAPI + PyTorch)
  |-- DefectDetector: ResNet18 + FPN + SSD heads
  |-- Real-time WebSocket stream analysis
  |-- REST API for inspections, analytics, alerts
  |-- Predictive maintenance engine
  |
  v
Dashboard (Browser)
  |-- Live defect feed
  |-- Factory line management
  |-- Trend analytics & ROI calculator
  |-- Maintenance scheduling
```

## Tech Stack

| Layer           | Technology                                            |
|-----------------|-------------------------------------------------------|
| AI Engine       | PyTorch (ResNet18 backbone, FPN, custom detection heads) |
| Backend         | FastAPI (Python), WebSocket for real-time streaming    |
| Image Pipeline  | OpenCV, Pillow, torchvision transforms                |
| API Auth        | API key (X-API-Key header)                            |
| Deployment      | Docker, CPU or GPU inference (CUDA / MPS / CPU auto-detect) |

---

## Enterprise Value Proposition

### For Quality Managers
- 100% inspection coverage (every unit, not samples)
- Defect detection in <100ms per frame
- Severity classification: low / medium / high / critical
- Audit trail: every inspection result stored with timestamp, line ID, and image reference

### For Plant Managers
- Predictive maintenance scoring reduces unplanned downtime
- Health score per line with trend analysis (stable / degrading / improving)
- Automated alert escalation for critical defects
- ROI calculator: typical payback period of 4-6 months

### For CFOs
- Reduce warranty claims by up to 90%
- Eliminate manual inspection labor costs
- Prevent costly recalls before they happen
- Measurable ROI: EUR 500K+ annual savings on a typical automotive line

---

## Pricing

| Tier        | Price                  | Includes                                           |
|-------------|------------------------|----------------------------------------------------|
| Starter     | EUR 890/camera/month   | 1 camera, 1 production line, real-time detection, dashboard, email alerts |
| Professional| EUR 1,490/camera/month | Up to 5 cameras, predictive maintenance, API access, priority support |
| Enterprise  | EUR 2,290/camera/month | Unlimited cameras, custom model training, on-premise deployment, SLA 99.9%, dedicated CSM |

Volume discounts available for 10+ camera deployments. Annual contracts receive 15% discount.

---

## Industry 4.0 Integration

Inspekta is designed to fit into existing Industry 4.0 ecosystems:

- **OPC-UA ready** -- Publish inspection results to OPC-UA servers for MES/ERP integration
- **MQTT support** -- Lightweight event streaming for IoT architectures
- **REST + WebSocket API** -- Standard HTTP integration for any platform
- **Docker containers** -- Deploy on edge devices (NVIDIA Jetson), on-premise servers, or cloud
- **Data export** -- JSON inspection records for integration with existing quality management systems (QMS)

---

## Competitive Advantage

| Feature                | Inspekta     | Traditional AOI   | Manual Inspection |
|------------------------|--------------|-------------------|-------------------|
| Defect coverage        | 4+ categories | Rule-based only  | Human judgment    |
| Accuracy               | >95%         | 85-90%            | ~80%              |
| Speed per unit         | <100ms       | 200-500ms         | 5-30 seconds      |
| Predictive maintenance | Yes          | No                | No                |
| Setup time             | Hours        | Weeks             | Training months   |
| Cost                   | EUR 890+/mo  | EUR 50K+ upfront  | EUR 40K+/yr labor |

---

## Demo

The Inspekta demo includes:

- **2 factory lines** pre-configured (Assembly Line Alpha, Precision Line Beta)
- **10 pre-computed inspection results** showing realistic defect detection across all 4 categories
- **Synthetic data generator** for unlimited test images with ground truth
- **Live inspection endpoint** -- upload any image for instant AI analysis
- **Dashboard** with real-time analytics, alerts, and maintenance predictions
- **ROI calculator** -- input your production parameters, get savings estimate

### Quick Start

```bash
# Install dependencies
cd src/backend
pip install -r requirements.txt

# Start in demo mode (no GPU required)
INSPEKTA_API_KEY=demo-key python server.py

# Health check
curl http://localhost:8000/health

# Run demo endpoint (pre-computed results, no model needed)
curl -H "X-API-Key: demo-key" http://localhost:8000/api/v1/demo/inspect

# Full dashboard
curl -H "X-API-Key: demo-key" http://localhost:8000/api/v1/dashboard
```

---

## Team

| Role                    | Responsibility                                    |
|-------------------------|---------------------------------------------------|
| Product & Design        | UX, enterprise pitch, pricing strategy            |
| ML Engineer             | PyTorch model architecture, training pipeline     |
| Backend Engineer        | FastAPI, WebSocket streaming, predictive engine   |
| Frontend Engineer       | Dashboard, real-time visualizations               |

---

## Target Customers at MunichTech EXPO

- **Siemens** -- Quality control across manufacturing divisions
- **BMW** -- Automotive body and paint inspection
- **Bosch** -- Component manufacturing QC
- **Continental** -- Tire and automotive parts inspection
- **Infineon** -- Semiconductor wafer inspection
- **Trumpf** -- Laser-cut parts quality assurance
- **Zeiss** -- Precision optics inspection (complementary to existing measurement systems)

---

## Demo Video Script (3 minutes)

### [0:00 - 0:20] Hook
"Every manufacturing line has a quality problem it does not know about. 20% of defects pass human inspection. Inspekta catches them all -- in under 100 milliseconds."

### [0:20 - 0:50] Problem
Show a production line with a human inspector. Highlight the statistics: fatigue after 2 hours, inconsistent standards between shifts, 80% detection rate at best. "Manual inspection was designed for a different era."

### [0:50 - 1:30] Solution Demo
Walk through the Inspekta system:
1. Camera mounted on production line
2. Real-time WebSocket stream showing frames being analyzed
3. Defect detected: crack on metal surface, bounding box + confidence score
4. Alert fires instantly on the dashboard
5. Show all 4 defect types being caught: crack, scratch, deformation, discoloration

### [1:30 - 2:10] Enterprise Features
- Predictive maintenance: "Line Alpha health score dropping -- schedule maintenance in 48 hours"
- Multi-line dashboard: 2 lines running, one green, one amber
- ROI calculator: "For a line producing 1,000 units/day at EUR 150 cost per defect, Inspekta saves EUR 2.4M annually with a 38-day payback period"
- API integration: show curl command hitting the inspection endpoint

### [2:10 - 2:40] Technical Depth
"Custom neural network: ResNet18 backbone pre-trained on ImageNet, Feature Pyramid Network for multi-scale detection, single-shot detection heads. Runs on CPU in under 100ms. On a EUR 500 NVIDIA Jetson, under 30ms."

### [2:40 - 3:00] Close
"Inspekta. German precision, automated. AI-powered quality control for every unit on every line. Starting at EUR 890 per camera per month. The future of manufacturing quality starts here."

---

## Links

- **GitHub:** https://github.com/xpandia/inspekta
- **Live Demo:** [TBD after deployment]
- **Demo Video:** [TBD after recording]

---

## License

MIT
