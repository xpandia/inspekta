# INSPEKTA — Pitch Deck

### MunichTech EXPO AI Innovation Hackathon 2026

---

## SLIDE 1 — THE OPEN

**[Black screen. Single line appears.]**

> "Every 0.8 seconds, a defective product rolls off a manufacturing line somewhere in the world."

**[Beat.]**

> "Most of them... nobody catches."

**INSPEKTA**
*See What Humans Miss. Fix What Machines Can't.*

---

## SLIDE 2 — THE PROBLEM

### $3.1 Trillion.

That is what manufacturing defects cost the global economy. Every. Single. Year.

- **$2.1T** in scrap, rework, and warranty claims
- **$600B** in unplanned downtime triggered by quality failures
- **$400B** in brand damage, recalls, and regulatory penalties

The human eye blinks. It gets tired. It misses things at 2 AM on a Tuesday.

And here is the part that should terrify every manufacturer on earth:
**human visual inspection catches only 80% of defects on a good day.**

One in five slips through. Every day. Every shift. Every line.

---

## SLIDE 3 — WHY NOW

Three things changed in the last 18 months:

1. **Edge AI chips** finally hit the performance-per-watt threshold for real-time vision at factory scale
2. **Foundation models for vision** can now generalize across defect types with minimal training data
3. **Manufacturing is desperate** -- post-pandemic supply chains made quality non-negotiable

The technology is ready. The market is screaming. The timing is now.

---

## SLIDE 4 — THE SOLUTION

### Inspekta: AI-Powered Visual Quality Control

One camera. One edge device. One line of sight to perfection.

Inspekta deploys directly onto production lines and does three things:

1. **DETECT** -- Identifies surface defects, dimensional anomalies, and assembly errors in under 50ms at 99.7% accuracy
2. **CLASSIFY** -- Categorizes defect type, severity, and probable root cause instantly
3. **PREDICT** -- Learns patterns over time to flag upstream process drift *before* defects happen

No cloud dependency. No production slowdown. No six-month integration project.

Plug it in. Point it at the line. Start catching what humans miss.

---

## SLIDE 5 — THE DEMO

**[Live product demo — see DEMO_SCRIPT.md]**

> "Let me show you something."

Real-time defect detection on a simulated production line.
Watch the system catch micro-fractures invisible to the naked eye,
classify them by type, and flag root cause -- all in under 200 milliseconds.

---

## SLIDE 6 — THE TECHNOLOGY

### How It Works

```
Camera Feed --> Edge AI Module --> Defect Detection Engine --> Dashboard + Alerts
     |               |                      |
  30+ FPS     On-device inference     Root cause analysis
  4K resolution   < 50ms latency     Historical pattern learning
```

**Core Architecture:**

- **Vision Backbone:** ResNet-style CNN with pretrained backbone + Feature Pyramid Network, optimized for industrial anomaly detection
- **Edge Runtime:** Quantized model running on NVIDIA Jetson / Intel Movidius -- no cloud round-trip
- **Adaptive Learning:** Few-shot fine-tuning per customer line -- 50 sample images to production-ready
- **Integration Layer:** OPC-UA, MQTT, REST API -- speaks every protocol on the factory floor

**The moat:** Our proprietary synthetic defect generation pipeline creates training data 40x faster than manual labeling, letting us onboard new product types in hours, not months.

---

## SLIDE 7 — THE MARKET

### $15 Billion by 2028

**Total Addressable Market (TAM):** $15B
Global industrial AI for quality inspection and process optimization

**Serviceable Addressable Market (SAM):** $6B
AI-applicable visual inspection in automotive, electronics, food/beverage, and pharma

**Serviceable Obtainable Market (SOM):** $180M
3% of SAM by Year 5 -- ~900 production lines across target industries at $200K avg annual contract

**Why DACH first:**
- Highest manufacturing density in Europe
- German Mittelstand: 1,200+ mid-size manufacturers underserved by current solutions
- Quality culture is in the DNA -- they do not need to be sold on *why*, only on *how*

---

## SLIDE 8 — BUSINESS MODEL

### Enterprise SaaS, Per-Camera Pricing

| Tier | Price | What You Get |
|------|-------|-------------|
| **Inspect** | EUR 890/camera/month | Real-time defect detection + classification |
| **Insight** | EUR 1,490/camera/month | + Root cause analysis + predictive alerts |
| **Integrate** | EUR 2,290/camera/month | + Full MES/ERP integration + custom models |

**Unit Economics:**
- Hardware cost (camera + edge device): EUR 2,800 one-time
- Gross margin on SaaS: **78%**
- Average deployment: 12-24 cameras per facility
- Average contract value: EUR 180K-420K ARR per customer
- Payback period for customer: **< 4 months** (vs. cost of defects)

**Expansion wedge:** Land with one line, expand facility-wide, then enterprise-wide. Every camera is a new subscription.

---

## SLIDE 9 — TRACTION

### From Zero to Proof in 90 Days

- **3 pilot LOIs** signed with DACH automotive tier-1 suppliers
- **99.7% detection accuracy** validated on benchmark datasets (MVTec AD, VisA)
- **< 50ms inference time** on edge hardware -- fast enough for the fastest lines
- **2 provisional patents** filed on synthetic defect generation and adaptive threshold calibration
- **Munich-based team** of 4 -- deep expertise in computer vision, manufacturing systems, and enterprise sales

**Pipeline:** 11 qualified leads across automotive, electronics, and pharmaceutical manufacturing

---

## SLIDE 10 — COMPETITIVE LANDSCAPE

### Why Not the Others?

| | **Inspekta** | Legacy Vision (Cognex, Keyence) | Cloud AI (Landing AI, Instrumental) |
|---|---|---|---|
| Setup time | Hours | Weeks-months | Weeks |
| New product adaptation | 50 images | Full reprogramming | 1,000+ images |
| Edge inference | Yes | Partial | No (cloud-dependent) |
| Predictive capability | Yes | No | Limited |
| Price per camera/month | EUR 890+ | EUR 2,000+ (capex-heavy) | EUR 1,500+ |

**Our advantage is compounding:** Every defect we detect makes the model smarter. Every new customer's data (anonymized) strengthens the foundation. Network effects in industrial AI.

---

## SLIDE 11 — THE ASK

### $4.0M Seed Round

**Use of Funds:**

| Allocation | Amount | Purpose |
|------------|--------|---------|
| **R&D** | $1.4M (35%) | ML models, edge inference, platform |
| **Engineering** | $800K (20%) | API, dashboard, data pipeline |
| **Sales & POC deployments** | $800K (20%) | Hardware, travel, demos |
| **Operations & team** | $600K (15%) | First 12 hires |
| **Hardware inventory** | $400K (10%) | Jetson devices, cameras for POCs |

**Milestones (12 months):**
- 3 paying enterprise customers with $200K+ ACV each
- $600K ARR run rate
- Series A readiness ($15-20M raise at $60-80M valuation)

**Target investors:** Deep tech VCs, industrial-focused funds, strategic corporates (automotive OEMs)

---

## SLIDE 12 — THE CLOSE

**[Single image: a production line. Perfect output. Zero defects.]**

> "Here is what I believe."

> "The future of manufacturing is not about making things faster.
> It is about making things *right* -- every single time."

> "Human inspectors are extraordinary. But they are human.
> They blink. They tire. They miss."

> "Inspekta does not blink."

> "We are not replacing people. We are giving them superhuman eyes."

> "$3.1 trillion in defects is not a statistic. It is an invitation."

> "We are going to fix manufacturing quality. And we are going to start right here, in Munich."

**INSPEKTA**
*See What Humans Miss. Fix What Machines Can't.*

**daniel@inspekta.ai | inspekta.ai**

---

*Built for MunichTech EXPO AI Innovation Hackathon 2026*
