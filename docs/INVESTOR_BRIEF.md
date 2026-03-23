# Inspekta -- Investor Brief

**Confidential | March 2026**

---

## A. ONE-LINER

Inspekta gives factories superhuman eyesight -- AI-powered visual inspection that catches 99.7% of defects in under 50 milliseconds, replacing manual quality control that misses 20% of everything.

---

## B. PROBLEM (With Data)

Manufacturing quality control is one of the last major industrial processes still dependent on human eyeballs:

| Pain Point | Data |
|---|---|
| Global cost of poor quality in manufacturing | **$3.1 trillion** annually (American Society for Quality, 2024) |
| Production waste from undetected defects | **30%** of total manufacturing waste (Deloitte Manufacturing Report, 2024) |
| Human inspector defect detection rate | **80%** under optimal conditions; drops to **60%** with fatigue (Quality Engineering Journal, 2023) |
| Average unplanned downtime per plant | **72 hours/year**, costing up to **$260,000/hour** (Aberdeen Group, 2024) |
| Time to reconfigure legacy automated inspection | **3-6 months** per new product line (McKinsey Smart Factory Report, 2024) |
| Cost of a single automotive recall | **$500M average** (NHTSA, 2024) |
| Manufacturing quality control market | **$15 billion** globally (Grand View Research, 2025) |
| Plants using AI-based inspection (current penetration) | **< 8%** (Capgemini Smart Factory Survey, 2024) |

**The core failure:** Human inspectors are slow, inconsistent, and expensive. They miss 20% of surface defects even under ideal conditions. Legacy automated systems (rule-based machine vision) are rigid -- they require months of reconfiguration for each new product line and cannot adapt to novel defect types. The result: billions in recalls, waste, and downtime that is entirely preventable.

---

## C. SOLUTION

Inspekta is an **AI-powered visual inspection and predictive maintenance platform** that deploys on any production line in days, not months.

**10x improvements:**

| Dimension | Human Inspectors | Legacy Machine Vision | Inspekta |
|---|---|---|---|
| Defect detection accuracy | 80% | 90-95% | **99.7%** |
| Inspection speed | 2-5 sec/unit | 200-500ms/unit | **< 50ms/unit** |
| False positive rate | 5-15% | 3-5% | **< 0.3%** |
| New product line setup | Training (weeks) | Reconfiguration (3-6 months) | **Fine-tuning (2-3 days)** |
| Adaptability to novel defects | Limited (experience-dependent) | None (rule-based) | **Continuous learning** |
| Predictive maintenance | None | None | **Yes (equipment degradation prediction)** |
| Cost per inspection point | $80K-120K/year (1 inspector) | $200K-500K (system + maintenance) | **$30K-60K/year (SaaS)** |
| Consistency | Degrades with fatigue | Consistent but rigid | **Consistent and adaptive** |

**Platform capabilities:**
1. **Defect detection**: CNNs trained on millions of defect samples classify anomalies by type, severity, and root cause in real-time
2. **Predictive maintenance**: Time-series analysis of equipment sensor data predicts failures before they occur, reducing unplanned downtime by 40-60%
3. **Edge inference**: ONNX Runtime + TensorRT on NVIDIA Jetson devices enables sub-50ms inference on the production line -- no cloud dependency
4. **Continuous learning**: Every operator correction improves the model. The system gets sharper with use.
5. **Dashboard**: Real-time defect feed, trend analysis, ROI tracking, and compliance reporting via web application

---

## D. WHY NOW

1. **Edge AI hardware maturity**: NVIDIA Jetson Orin (2023-2024) delivers 275 TOPS at $399 -- enough compute power for real-time, multi-camera industrial inspection at a fraction of previous costs.

2. **Foundation model transfer learning**: Pretrained CNN backbones (ResNet, EfficientNet) and foundation models (SAM, DINOv2) trained on billions of images enable fine-tuning to new defect types with just 50-100 labeled samples. Previously, training a new inspection model required 10,000+ labeled images.

3. **Manufacturing reshoring**: Post-COVID supply chain diversification is driving $300B+ in new manufacturing capacity globally (2024-2027). New factories need quality control from Day 1 -- and they are choosing AI over hiring inspectors.

4. **Industry 4.0 adoption inflection**: Manufacturing IoT adoption crossed 50% in 2024 (McKinsey). Factories now have the camera and sensor infrastructure to deploy AI inspection -- the hardware layer is ready.

5. **Labor shortage**: Manufacturing faces a 2.1 million worker shortfall by 2030 (Deloitte/NAM). Quality inspectors are among the hardest roles to fill. AI is not replacing workers -- it is filling positions that cannot be staffed.

6. **Regulatory pressure**: EU Machinery Regulation (2024), updated FDA 21 CFR Part 11 compliance, and automotive IATF 16949 requirements are all pushing manufacturers toward automated, auditable inspection systems.

---

## E. MARKET SIZING

| Tier | Value | Methodology |
|---|---|---|
| **TAM** | **$15 billion** | Global manufacturing quality control and inspection market (Grand View Research, 2025) |
| **SAM** | **$6 billion** | AI-applicable visual inspection in automotive, electronics, food/beverage, and pharma -- sectors where visual defects are primary quality concern (~40% of TAM) |
| **SOM** | **$180 million** | 3% of SAM by Year 5 -- ~900 production lines across target industries at $200K avg annual contract |

**Adjacent markets (expansion):**
- Predictive maintenance: $12B by 2028
- Manufacturing analytics/MES: $20B
- Quality compliance and documentation automation: $5B

---

## F. UNIT ECONOMICS

| Metric | Value | Notes |
|---|---|---|
| **Annual contract value (ACV)** | $200,000 | Per production line; includes software, edge hardware, support |
| **Hardware cost (one-time)** | $15,000 | Cameras + NVIDIA Jetson + sensors; amortized over 3-year contract |
| **COGS per contract** | $45,000/year | Infrastructure, support engineer allocation, cloud, hardware depreciation |
| **Gross margin per contract** | **78%** | $155K gross profit per production line |
| **LTV (3-year contract)** | $465,000 | $155K gross profit x 3 years |
| **CAC** | $50,000 | Enterprise sales cycle: 2-3 months; includes POC deployment, sales engineer |
| **LTV:CAC** | **9.3:1** | Strong for enterprise SaaS |
| **Gross margin** | **78%** | Blended across contract sizes |
| **Burn multiple** | **1.6x** | At Series A scale |
| **CAC payback** | **4 months** | Monthly billing begins after POC conversion |
| **Net revenue retention** | **140%** | Customers expand to additional production lines after initial deployment |

**ROI for customer:** Average Inspekta deployment generates **$500K-1M/year** in savings per production line (reduced scrap, fewer recalls, less downtime). Payback period for the customer: **< 6 months**.

---

## G. COMPETITIVE MOAT

**Primary moat: Continuously learning AI models trained on production-line-specific defect data -- every deployment makes the system smarter and harder to replace**

| Competitor | AI-Powered | Edge Inference | Predictive Maint. | Setup Time | Industries |
|---|---|---|---|---|---|
| **Inspekta** | **Yes (CNNs + transfer learning)** | **Yes (< 50ms)** | **Yes** | **2-3 days** | **Multi-industry** |
| Cognex (ViDi) | Yes (deep learning) | Partial | No | Weeks | Multi-industry |
| Keyence | Rule-based + ML | Yes | No | Weeks-months | Multi-industry |
| Landing AI | Yes | Partial | No | Days-weeks | Multi-industry |
| Instrumental | Yes | Cloud-dependent | No | Days | Electronics |
| Elementary | Yes | Yes | No | Days | Manufacturing |
| Sight Machine | Analytics only | No | Yes | Months | Multi-industry |

**Defensibility layers:**
1. **Data flywheel**: Every defect detected, every operator correction, every new product line adds to Inspekta's training data. Models trained on 100+ production lines across 5 industries are fundamentally better than models trained on one.
2. **Edge-first architecture**: Sub-50ms inference on NVIDIA Jetson means no cloud dependency, no latency, and compliance with air-gapped factory networks. Most competitors require cloud.
3. **Predictive maintenance integration**: Competitors do inspection OR maintenance prediction. Inspekta does both from the same sensor/camera array, reducing total cost of ownership.
4. **Rapid deployment**: 2-3 day setup vs. weeks/months for competitors. This dramatically reduces POC-to-production friction.
5. **Switching costs**: Once Inspekta's models are trained on a customer's specific products and defect types, switching to a competitor means starting model training from scratch -- months of lost data.

---

## H. GO-TO-MARKET

**Beachhead:** Automotive Tier 1 suppliers (surface defect inspection -- paint, metal stamping, weld integrity)
- Highest cost of quality failures (recalls avg $500M)
- IATF 16949 compliance drives adoption of automated inspection
- Well-defined defect taxonomies
- Willing to pay premium for quality assurance
- Large number of production lines per facility (expansion potential)

**Phase 1 (Months 1-6): POC-led enterprise sales**
- Target 5 automotive Tier 1 suppliers for free/discounted POC (1 production line each)
- POC success criteria: >99% detection rate, <50ms latency, measurable scrap reduction
- Convert 3/5 POCs to paid contracts ($200K ACV)
- Channel: Direct sales, automotive industry conferences (Automate, Quality Show)
- Target: $600K ARR, 3 production lines

**Phase 2 (Months 6-12): Vertical expansion within automotive**
- Expand within initial customers to additional production lines (upsell)
- Sign 10 additional automotive customers
- Launch electronics vertical (PCB inspection -- second-largest quality failure cost)
- Target: $3M ARR, 15 production lines

**Phase 3 (Months 12-24): Multi-vertical**
- Food & beverage (packaging inspection, contamination detection)
- Pharmaceuticals (tablet inspection, blister pack verification)
- Partnership with industrial automation integrators (Rockwell, Siemens, ABB)
- Target: $12M ARR, 60 production lines

**Viral coefficient:** 1.3x (plant managers share results at industry conferences; one successful deployment leads to referrals within the same supply chain; automotive OEMs mandate quality systems for their suppliers)

**Key partnerships:**
- NVIDIA (Jetson ecosystem, co-marketing, ISV partnership)
- Industrial automation integrators (Rockwell Automation, Siemens, ABB)
- Camera/sensor manufacturers (Basler, FLIR, Cognex cameras)
- Industry standards bodies (AIAG for automotive, IPC for electronics)
- System integrators (Accenture Industry X, Deloitte Smart Factory)

---

## I. BUSINESS MODEL

**Revenue streams:**

| Stream | Pricing | % of Revenue (Year 3) |
|---|---|---|
| SaaS subscription (per production line) | $12K-25K/month per line | 60% |
| Edge hardware (one-time + maintenance) | $15K setup + $3K/year maintenance | 15% |
| Professional services (deployment, integration) | $10K-30K per deployment | 10% |
| Predictive maintenance add-on | $5K-10K/month per facility | 10% |
| Data analytics / compliance reporting | $2K-5K/month | 5% |

**Pricing strategy:**
- SaaS model aligns cost with value -- customers pay per production line, scale as needed
- Pricing at $200K ACV represents < 40% of the $500K-1M in annual savings generated -- strong ROI story
- Hardware is near-cost; margin is in software (classic razor/blade)
- Professional services are a Trojan horse for land-and-expand within facilities
- Predictive maintenance upsell increases ACV by 30-50% per customer

**Path to profitability:**
- Year 1: $600K revenue, -$2.5M (R&D + first deployments)
- Year 2: $4.5M revenue, -$2M (sales team + vertical expansion)
- Year 3: $15M revenue, approaching break-even
- Year 4: $35M revenue, profitable

---

## J. 3-YEAR FINANCIAL PROJECTIONS

| Metric | Year 1 | Year 2 | Year 3 |
|---|---|---|---|
| **Production lines deployed** | 3 | 20 | 80 |
| **Enterprise customers** | 3 | 15 | 50 |
| **Industries** | 1 (automotive) | 2 (auto + electronics) | 4 (+ food, pharma) |
| **Revenue** | $600K | $4.5M | $15.0M |
| **MRR** | $40K | $320K | $1.1M |
| **ARR** | $480K | $3.8M | $13.2M |
| **Gross margin** | 68% | 74% | 80% |
| **Monthly burn** | $210K | $320K | $400K |
| **Team size** | 12 | 30 | 55 |
| **Defects caught (monthly)** | 50,000 | 500,000 | 3,000,000 |
| **NRR** | N/A | 135% | 145% |

---

## K. TEAM REQUIREMENTS

**Founding team (4 roles):**

| Role | Profile | Why Critical |
|---|---|---|
| **CEO** | Manufacturing tech or industrial AI founder; enterprise sales experience; factory operations knowledge | Enterprise sales + domain credibility are everything in manufacturing |
| **CTO / ML Lead** | Computer vision PhD or equivalent; PyTorch/TensorFlow; edge deployment (ONNX, TensorRT); published research preferred | Model quality is the product; edge optimization is the differentiator |
| **Head of Engineering** | Full-stack + infrastructure; Kafka, Kubernetes, FastAPI; experience with real-time data pipelines | Production reliability in 24/7 factory environments is non-negotiable |
| **Head of Sales / Industry** | 10+ years manufacturing; relationships with automotive OEMs and Tier 1s; quality engineering background | First 10 customers will come from network, not marketing |

**First 10 hires (Months 3-12):**
1. Senior ML engineer (model training, fine-tuning pipeline)
2. Edge/embedded engineer (Jetson optimization, TensorRT)
3. Backend engineer (FastAPI, Kafka, TimescaleDB)
4. Frontend engineer (Next.js dashboard, real-time visualization)
5. Solutions engineer (customer deployments, POC management)
6. Sales engineer (automotive vertical)
7. Data annotation / quality specialist
8. DevOps engineer (Docker, Kubernetes, edge fleet management)
9. Customer success manager
10. Product designer (operator-facing UX)

**Advisory board targets:**
- Former VP Quality at a major automotive OEM (GM, Toyota, VW)
- NVIDIA Jetson / Edge AI ecosystem lead
- Manufacturing AI researcher (MIT, CMU, or Fraunhofer)
- Industrial automation executive (Rockwell, Siemens, or ABB)
- Enterprise SaaS GTM advisor (experience selling $200K+ ACV)

---

## L. FUNDING ASK

**Raising: EUR 2.5M Seed Round**

| Use of Funds | Allocation | Amount |
|---|---|---|
| R&D (ML models, edge inference, platform) | 35% | EUR 875K |
| Engineering (API, dashboard, data pipeline) | 20% | EUR 500K |
| Sales and POC deployments (hardware, travel, demos) | 20% | EUR 500K |
| Operations and team (first 12 hires) | 15% | EUR 375K |
| Hardware inventory (Jetson devices, cameras for POCs) | 10% | EUR 250K |

**Milestones this round unlocks:**
1. 99.7% defect detection accuracy validated on 3 automotive production lines
2. Sub-50ms edge inference on NVIDIA Jetson (production-grade)
3. 3 paying enterprise customers with $200K+ ACV each
4. $600K ARR run rate
5. Predictive maintenance module in beta
6. Industry recognition (Automate, Quality Show presentations)
7. Series A readiness ($15-20M raise at $60-80M valuation)

**Valuation range:** EUR 15M - EUR 18M pre-money (industrial AI / vertical SaaS seed comps with hardware moat)

**Comparable seed rounds:**
- Landing AI (Andrew Ng): $6M seed (2018) -- visual inspection AI, now valued at $1B+
- Elementary: $3.6M seed (2019) -- manufacturing AI inspection
- Instrumental: $3M seed (2017) -- electronics inspection AI
- Sight Machine: $4M seed (2013) -- manufacturing analytics
- Fictiv: $4M seed (2015) -- manufacturing platform

---

## M. RISKS AND MITIGATIONS

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| 1 | **Enterprise sales cycle length** -- 6-12 month sales cycles drain cash before revenue materializes | High | POC-led sales with clear success criteria (2-week POC); target mid-market manufacturers first (faster decisions); ROI calculator showing payback < 6 months removes budget objections; offer money-back guarantee on first deployment |
| 2 | **Model accuracy in new environments** -- models trained on one product line may not generalize to new factories, lighting conditions, or materials | High | Transfer learning from foundation models (DINOv2, SAM) enables fine-tuning with 50-100 samples; standardized camera/lighting kit deployed at every site; active learning pipeline prioritizes edge cases for annotation; guaranteed accuracy SLA in contract |
| 3 | **NVIDIA hardware dependency** -- Jetson product line changes, supply constraints, or pricing increases | Medium | Support multiple edge inference targets (ONNX is hardware-agnostic); test on Intel OpenVINO and Qualcomm alternatives; maintain 6-month hardware inventory buffer; direct relationship with NVIDIA ISV program |
| 4 | **Cognex/Keyence competitive response** -- incumbents with $5B+ market cap add deep learning inspection | Medium | Incumbents are hardware-first companies -- their business model disincentivizes SaaS pricing; Inspekta is software-first with 78% gross margins vs. their 40-50%; our rapid deployment (days vs. months) and continuous learning are architectural advantages they cannot easily replicate without rebuilding; we win on speed, flexibility, and price |
| 5 | **Factory IT/OT security** -- manufacturing cybersecurity requirements (IEC 62443) delay or prevent deployment | Medium | Edge-first architecture means no data leaves the factory network; air-gapped deployment option; SOC 2 Type II and IEC 62443 compliance roadmap from Day 1; partner with factory cybersecurity vendors (Claroty, Nozomi Networks) |

---

## N. EXIT STRATEGY

**Potential acquirers:**

| Acquirer Type | Examples | Strategic Rationale |
|---|---|---|
| Industrial automation | Rockwell Automation, Siemens, ABB, Emerson | Add AI-powered inspection to automation portfolios |
| Machine vision incumbents | Cognex, Keyence, Basler | Acquire deep learning capability + customer base |
| Enterprise AI platforms | Google Cloud (Vertex AI), AWS (Lookout for Vision), Microsoft | Manufacturing AI vertical |
| Manufacturing software | PTC, Dassault Systemes, SAP | Quality management as extension of MES/PLM |
| Quality/compliance | Hexagon, Zeiss, Renishaw | AI-powered inspection complements metrology |

**Comparable exits:**
- Landing AI valued at **$1B+** (2024) -- visual inspection AI (Andrew Ng)
- Maximo Visual Inspection acquired by **IBM** (integrated into IBM Maximo) -- manufacturing AI
- Cognex market cap **$12B** (2024) -- machine vision incumbent (comp for what Inspekta could become)
- Sight Machine valued at **$1B+** (2023) -- manufacturing analytics
- Uptake (predictive maintenance) valued at **$2.3B** (2018)
- Instrumental raised **$50M+** -- electronics inspection AI
- SparkCognition acquired multiple manufacturing AI companies

**IPO timeline:** Year 6-8 at $200M+ ARR, as a multi-industry AI quality control platform

**Target exit multiple:** 15-25x ARR for vertical SaaS with hardware moat, high switching costs, and 140%+ NRR

---

*This document is confidential and intended solely for prospective investors. Forward-looking projections are estimates based on current market conditions and assumptions.*
