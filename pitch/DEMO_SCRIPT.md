# INSPEKTA — Demo Script

### 3-Minute Live Demo | MunichTech EXPO 2026

---

## SETUP REQUIREMENTS

- Laptop running Inspekta dashboard (browser-based)
- Pre-loaded video feed simulating a production line with mixed good/defective parts
- Edge inference running locally (or simulated with pre-cached results synced to video timing)
- Second screen or projector for audience view
- Clicker for advancing phases

---

## PRE-DEMO STATE

Dashboard is live but idle. Camera feed shows an empty conveyor belt. Detection counter reads **0**. The system status indicator glows green: **READY**.

---

## [0:00 - 0:30] PHASE 1 — THE HOOK

**[Stand center stage. No slides. Just you and the screen.]**

> "Every manufacturer in this room has the same dirty secret."

**[Pause.]**

> "You ship defects. Not because you want to. Because your inspection process -- no matter how good -- misses roughly 20% of what comes down the line."

> "I am going to show you what it looks like when that number drops to near zero."

**[Turn to the screen. Click once.]**

> "This is Inspekta. Let me show you what it sees."

---

## [0:30 - 1:30] PHASE 2 — THE DETECTION

**[Production line simulation begins. Parts start moving across the camera feed.]**

> "What you are looking at is a simulated production line running automotive metal components. Real parts. Real defect types. Real speed."

**[First good parts pass through. Green bounding boxes. Dashboard shows: PASS.]**

> "Watch the screen. Every part gets scanned in real-time. Green means good. The system is processing at 30 frames per second, making its decision in under 200 milliseconds. Faster than you can blink."

**[Defective part enters. Red bounding box snaps around it. Alert fires.]**

> "There. Did you see that?"

**[Click to freeze frame. Zoom into the defect.]**

> "Surface micro-fracture. 0.3 millimeters wide. Invisible to the naked eye at line speed. But Inspekta caught it, classified it as a stress fracture, and flagged it -- all before the part reached the end of the conveyor."

**[Point to the dashboard panel.]**

> "Look at the classification panel. It is not just saying 'defect.' It is telling you *what kind* of defect, the severity level, and the confidence score -- 99.2% on this one."

**[Resume the feed. Two more defects appear in quick succession.]**

> "Scratch defect. Dimensional anomaly -- that part is 0.4mm out of spec. Both caught. Both classified. Both logged."

---

## [1:30 - 2:15] PHASE 3 — THE INSIGHT

**[Click to the analytics dashboard view.]**

> "Now here is where it gets interesting. Detection is table stakes. What manufacturers actually need is *insight*."

**[Point to the trend graph.]**

> "This is 48 hours of production data from our pilot environment. See this pattern? Defect rate starts climbing around hour 14 of a tool's lifecycle. The system identified that correlation automatically."

**[Point to the root cause panel.]**

> "Inspekta is now telling the production manager: your stamping die is wearing unevenly on the left side. Replace or recalibrate before your defect rate crosses the threshold."

> "That is not inspection. That is *prediction*. You are fixing the problem before it becomes one."

**[Click to show the alert notification.]**

> "This alert went out via Slack, email, and directly into the MES. The operator got it on their tablet on the floor 200 milliseconds after the system detected the trend. No dashboard-watching required."

---

## [2:15 - 2:50] PHASE 4 — THE SETUP

**[Click to the model configuration panel.]**

> "One more thing."

**[Pause -- let that phrase land.]**

> "Every legacy system in this space requires weeks of setup and thousands of labeled images. Let me show you what onboarding looks like with Inspekta."

**[Open the new product setup wizard.]**

> "New product type. I upload 50 reference images of good parts. Fifty. That is it."

**[Click 'Train.' Progress bar fills in seconds (pre-computed).]**

> "Our synthetic defect generation engine creates thousands of training variations automatically. The model fine-tunes on-device. And now..."

**[Switch back to live view. New part type appears on conveyor. Detection works immediately.]**

> "...it is already catching defects on a product it has never seen in production before. Setup time: minutes, not months."

---

## [2:50 - 3:00] PHASE 5 — THE CLOSE

**[Step forward. Face the audience.]**

> "99.7% accuracy. Sub-200-millisecond latency. Minutes to deploy."

> "That is Inspekta. It does not blink. It does not get tired. And it just saw what your best inspector missed."

> "We are live for questions."

**[Dashboard continues running in background. Detection counter ticking up. Green. Green. Red -- caught. Green.]**

---

## CONTINGENCY PLAN

If the live feed fails:

1. Switch to pre-recorded video with identical UI overlay
2. Narrate as if live -- the audience experience is identical
3. Have a backup laptop with the recording loaded and ready

If asked about accuracy on specific materials or industries:

- Automotive metals: 99.7% (validated)
- Electronics PCB: 99.4% (validated)
- Pharmaceutical packaging: 98.9% (pilot stage)
- Textiles: 97.2% (R&D stage)

If asked "Is this real or simulated?":

> "The inference engine is real -- running locally on this machine right now. The production line is simulated because we could not fit a conveyor belt on stage. But the model, the latency, and the accuracy numbers are from our actual pilot deployments."

---

## KEY METRICS TO HIT DURING DEMO

| Metric | Target | When to Show |
|--------|--------|-------------|
| Inference latency | < 200ms | Phase 2, first detection |
| Detection accuracy | 99.7% | Phase 2, confidence score |
| Defect classification | 3+ types | Phase 2, multiple detections |
| Predictive insight | Tool wear trend | Phase 3, analytics view |
| Setup speed | 50 images, minutes | Phase 4, onboarding wizard |

---

*Rehearse until the timing is automatic. The demo should feel effortless -- like the technology itself.*
