# INSPEKTA -- Technical & Strategic Audit Report

**Audit Date:** 2026-03-23
**Auditor:** Independent Technical Review
**Classification:** Confidential

---

## Executive Summary

Inspekta is an ambitious industrial AI quality control project targeting the MunichTech EXPO AI Innovation Hackathon 2026. The submission demonstrates strong engineering fundamentals, a well-architected ML pipeline, and exceptionally polished pitch materials. However, the project operates entirely on random weights (no trained model), has no real test suite, and several claims in the pitch materials cannot be substantiated by the current codebase. The gap between what is *built* and what is *claimed* is the central risk.

---

## 1. CODE QUALITY -- 7.5/10

**Strengths:**
- Clean, well-structured Python with proper type hints (`from __future__ import annotations`, `Optional`, `List`, `Sequence`)
- Excellent use of dataclasses and enums for domain modeling (`DefectType`, `BoundingBox`, `Detection`, `InspectionResult`)
- Consistent logging throughout both `detector.py` and `server.py`
- Proper module docstrings and inline section separators improve readability
- Weight initialization follows best practices (Kaiming normal, focal-loss-style classification bias)
- `to_dict()` serialization methods on all domain types -- clean API boundary

**Weaknesses:**
- Zero unit tests anywhere in the repository
- No linting configuration (no `pyproject.toml`, `setup.cfg`, `.flake8`, `ruff.toml`)
- No CI/CD pipeline
- The `import json` inside the WebSocket handler (line 506 of `server.py`) is a lazy import buried in a loop -- should be at module level
- No `__init__.py` files visible, making the package structure ambiguous
- README says `uvicorn main:app` but the actual file is `server.py` -- the getting-started instructions are broken
- No `.gitignore`, `Dockerfile`, or `Makefile`
- Frontend is a single monolithic HTML file (~1000+ lines) with all CSS/JS inline -- no component structure, no build system

---

## 2. LANDING PAGE -- 8.5/10

**Strengths:**
- Visually polished. Professional-grade design that would hold up next to funded startup landing pages
- Responsive design with proper `clamp()` font sizing, media queries, and mobile hamburger menu
- Effective animated scanner visual in the hero section creates immediate product understanding
- Interactive ROI calculator is a standout feature -- directly addresses buyer objections
- Clean typography system using Inter, proper font-weight hierarchy, good vertical rhythm
- Smooth scroll, sticky nav with backdrop blur, and CSS-only animations (no JS framework dependency)
- Good section flow: Hero > Problem > Solution > How It Works > Industries > ROI > CTA

**Weaknesses:**
- Single monolithic HTML file. All CSS is embedded (~1000 lines of styles). All JS is inline. This is unmaintainable at scale but acceptable for a hackathon
- No `<noscript>` fallback
- Emoji usage for icons (`problem-icon`, `solution-icon`, `industry-icon`) -- should use SVG for consistency and professionalism at this level of polish
- CTA buttons link to `#` -- no real form, no email capture, no Calendly integration
- No favicon
- No OpenGraph / Twitter Card meta tags beyond the basic `<meta name="description">`
- No performance optimization (no image lazy loading, no critical CSS extraction)
- The ROI calculator JS connects to the backend API (`/api/v1/roi`) -- will fail if backend is not running. Should have a client-side fallback

---

## 3. ML PIPELINE -- 7.0/10

**Strengths:**
- Legitimate custom architecture: ResNet-style backbone (4 stages) + Feature Pyramid Network (FPN) + shared classification/regression heads. This is not a toy -- it is a proper single-shot detector
- Residual connections with proper shortcut projections when dimensions change
- FPN implementation is correct: lateral connections + top-down pathway + smoothing convolutions
- Anchor generation with multiple scales (32, 64, 128, 256) and ratios (0.5, 1.0, 2.0) -- standard practice
- Box decoding with `exp` clamping (`max=4.0`) to prevent numerical instability
- NMS post-processing using `torchvision.ops.nms`
- ImageNet normalization values in preprocessing (0.485, 0.456, 0.406)
- Multi-device support: CUDA, MPS (Apple Silicon), CPU auto-detection
- Warm-up routine to stabilize GPU/JIT caches before inference
- Batch inference support

**Weaknesses:**
- **The model runs on random weights.** There is no trained model, no training script, no dataset, no training loop, no loss function. The `load_model()` call in `server.py` explicitly uses demo mode. This means every claim about "99.7% accuracy" is entirely hypothetical
- No training pipeline whatsoever -- no `train.py`, no data loading, no augmentation, no validation loop
- No ONNX export, no TensorRT optimization, no quantization -- despite the pitch claiming edge deployment on NVIDIA Jetson with sub-50ms inference
- The pitch claims "ViT-based" backbone, but the actual implementation is a pure CNN (ResNet-style convolutions). This is a direct contradiction
- No model versioning, no experiment tracking (no MLflow, no W&B)
- The `_generate_anchors` function uses Python loops over grid cells -- should be vectorized with `torch.meshgrid` for performance
- Feature map size computation (`INPUT_SIZE // s for s in [4, 8, 16, 32]`) is hardcoded and assumes specific stride behavior that should be derived from the architecture
- Severity classification is based purely on confidence score, not on defect type or area -- a 0.91 confidence scratch and a 0.91 confidence crack get the same "critical" severity, which is nonsensical in a real industrial context

---

## 4. BACKEND -- 8.0/10

**Strengths:**
- Well-structured FastAPI application with proper async lifecycle management (`@asynccontextmanager`)
- Comprehensive REST API surface: inspection, batch inspection, analytics, alerts, factory lines CRUD, predictive maintenance, ROI calculator, dashboard aggregation
- WebSocket endpoint for real-time video stream analysis with proper binary/text message handling
- Pydantic models for input validation with sensible defaults and constraints (`Field(default=0.05, ge=0.0, le=1.0)`)
- CORS middleware configured (appropriate for hackathon; wildcard `*` origins would need tightening for production)
- Proper HTTP error codes: 503 for model not ready, 404 for missing resources, 400 for bad input
- Analytics computation with defect rate, severity distribution, and per-type breakdowns
- Predictive maintenance heuristic (first-half vs second-half defect rate comparison) is a reasonable MVP approach

**Weaknesses:**
- **All data is in-memory.** No database. Restart = total data loss. The in-memory stores (`_inspection_history`, `_alerts`, `_factory_lines`) will grow unbounded and eventually exhaust memory
- **Thread safety issue:** The WebSocket handler mutates `detector.confidence_threshold` (lines 543-549) on the shared detector instance. With concurrent WebSocket connections, this creates a race condition where one stream's threshold affects another stream's inference
- No authentication or authorization on any endpoint. Anyone can delete factory lines, acknowledge alerts, etc.
- No rate limiting
- No request size limits on file uploads -- a 10GB image upload would be accepted
- `datetime.utcnow()` is deprecated in Python 3.12+ -- should use `datetime.now(timezone.utc)`
- No API versioning enforcement (v1 is in the path but there is no mechanism to evolve)
- No pagination cursor -- offset-based pagination will degrade with large datasets
- `requirements.txt` includes `aiofiles` but it is never imported or used
- WebSocket binary frame processing is synchronous (`detector.detect_frame` is a blocking call in an async handler) -- this will block the event loop under load

---

## 5. PITCH MATERIALS -- 9.0/10

**Strengths:**
- **PITCH_DECK.md:** Exceptionally well-written. The narrative arc (Problem > Why Now > Solution > Demo > Tech > Market > Business Model > Traction > Competition > Ask > Close) follows the classic VC pitch structure perfectly. The opening hook ("Every 0.8 seconds...") is strong
- **pitch_deck.html:** Production-quality interactive slide deck with animations, animated counters, scanner visualization, TAM/SAM/SOM concentric circles, pricing cards, competitive comparison table, financial projection cards, and fund allocation bars. Speaker notes built in. Keyboard navigation. This is the best artifact in the entire submission
- **DEMO_SCRIPT.md:** Professional-grade demo script with exact timing, contingency plans, and specific metrics to hit at each phase. The contingency section ("If the live feed fails...") shows maturity
- **VIDEO_STORYBOARD.md:** Cinema-quality storyboard with shot-by-shot breakdown, pacing rules, creative direction, and production notes for a minimum viable version. Includes multi-format deliverables (16:9, 9:16, 1:1)
- Consistent messaging across all materials. The tagline ("See What Humans Miss. Fix What Machines Can't.") is memorable and appears everywhere

**Weaknesses:**
- The pitch deck has 12 slides. The README says "max 10 slides" for the hackathon. This needs trimming
- The numbers in the pitch deck (EUR 2.5M seed) and the investor brief ($4.0M seed) are inconsistent -- which is the real ask?
- Traction claims ("3 pilot LOIs signed", "2 provisional patents filed") cannot be verified from the repository contents. If these are fabricated for the hackathon, this is a serious credibility risk
- The demo script references features not yet built: "new product setup wizard", "root cause panel", "trend graph", "Slack/email integration"

---

## 6. INVESTOR READINESS -- 8.0/10

**Strengths:**
- **INVESTOR_BRIEF.md:** This is a thorough, 320-line document covering one-liner, problem (with cited sources), solution (with 10x improvement table), why now (6 converging forces), market sizing (TAM/SAM/SOM with methodology), unit economics (LTV:CAC 9.3:1), competitive moat (6 defensibility layers), GTM phases, business model, 3-year financial projections, team requirements, funding ask with comparable seed rounds, risk/mitigation matrix, and exit strategy
- Unit economics are well-constructed and internally consistent
- Risk/mitigation section is honest and addresses real concerns (enterprise sales cycles, model generalization, hardware dependency)
- Exit strategy names specific acquirer types with strategic rationale
- Comparable companies (Landing AI, Elementary, Instrumental) are relevant and well-chosen

**Weaknesses:**
- The brief asks for $4.0M at $16-20M pre-money valuation, but the pitch deck asks for EUR 2.5M. These are different numbers and signal either a moving target or sloppy version control
- Financial projections are aggressive: $600K Year 1 to $15M Year 3 (25x growth in 2 years). This requires signing 47 new enterprise customers in Year 3 alone while simultaneously entering 2 new verticals
- The SOM in the investor brief ($300M) differs from the pitch deck ($180M)
- "< 8%" AI inspection penetration stat is cited to "Capgemini Smart Factory Survey, 2024" -- this should be verified; misattributed statistics in an investor document are a major red flag
- No actual team bios. The document lists "team requirements" as if hiring, rather than showcasing existing founders. For a seed-stage company, this is concerning
- Claims of "sub-50ms inference" in the investor brief but the actual code measures inference time and the pitch deck says "sub-200ms" -- yet another inconsistency

---

## 7. HACKATHON FIT -- 7.5/10

**Strengths:**
- Clear problem statement with large market opportunity
- Working end-to-end system: frontend (landing page) + backend (API) + ML pipeline (detector)
- Interactive demo potential: upload an image, get bounding boxes back
- ROI calculator adds a business-relevance dimension that judges will appreciate
- Strong pitch materials that will perform well in presentation rounds
- WebSocket support for real-time video analysis is a differentiator

**Weaknesses:**
- The README checklist has everything unchecked (`- [ ]`), suggesting the submission is not complete
- No deployed landing page URL. README says "Landing page deployed" but there is no deployment
- No actual working demo with trained weights -- the detector produces random noise on random weights
- README says "Next.js (React)" for frontend, but the actual frontend is a plain HTML file. The tech stack description is aspirational, not actual
- README getting-started instructions reference `npm install` and `npm run dev` for frontend -- there is no `package.json` or Node.js project. These instructions are fiction
- The architecture diagram in the README shows Kafka, PostgreSQL + TimescaleDB, Kubernetes, Grafana, Prometheus -- none of which exist in the codebase
- No model performance benchmarks (a checklist item)
- No edge deployment proof-of-concept (a checklist item)

---

## 8. CRITICAL ISSUES

| # | Issue | Severity | Impact |
|---|-------|----------|--------|
| 1 | **No trained model.** The entire ML pipeline runs on random weights. All accuracy claims (99.7%) are unsubstantiated. | CRITICAL | The core product claim is demonstrably false in the current codebase |
| 2 | **Tech stack fiction.** README and pitch materials claim Next.js, Kafka, PostgreSQL, TimescaleDB, Kubernetes, Grafana, ONNX, TensorRT. None exist. The frontend is a single HTML file. The backend uses in-memory Python dicts. | HIGH | Misrepresentation of technical capabilities |
| 3 | **Inconsistent funding ask.** Pitch deck: EUR 2.5M. Investor brief: $4.0M. These are different amounts in different currencies. | HIGH | Signals lack of rigor or version control |
| 4 | **Architecture claim mismatch.** Pitch says "ViT-based" backbone. Code implements a CNN (ResNet-style). | HIGH | Technical credibility gap |
| 5 | **WebSocket race condition.** Shared detector threshold mutation across concurrent connections. | MEDIUM | Will cause incorrect inference results under concurrent load |
| 6 | **Broken getting-started instructions.** README says `uvicorn main:app` but file is `server.py`. Frontend instructions reference non-existent `npm` project. | MEDIUM | First-time users cannot run the project |
| 7 | **Unbounded in-memory storage.** No eviction policy on inspection history, alerts, etc. | MEDIUM | Memory exhaustion under sustained use |
| 8 | **Inference blocks the event loop.** `detector.detect_frame()` is a synchronous PyTorch call inside an async WebSocket handler. | MEDIUM | Backend becomes unresponsive during inference |

---

## 9. RECOMMENDATIONS

### P0 -- Must Fix Before Submission

1. **Train the model or be transparent.** Either provide a training script + trained weights on a public defect dataset (MVTec AD is ideal and free), or clearly label the entire project as a "prototype with simulated inference." Do not claim 99.7% accuracy with random weights.

2. **Fix the README.** Correct `uvicorn main:app` to `uvicorn server:app`. Remove fake `npm install / npm run dev` frontend instructions. Replace them with "open `src/frontend/index.html` in a browser." Align the tech stack section to reflect what actually exists.

3. **Reconcile the numbers.** Pick one funding ask (EUR 2.5M or $4.0M). Pick one SOM ($180M or $300M). Pick one inference target (sub-50ms or sub-200ms). Search-and-replace across all documents.

4. **Fix the architecture claim.** Either change the pitch to say "ResNet-style CNN backbone" (which is what the code is), or implement a ViT backbone (which would be a significant rewrite).

### P1 -- Should Fix for Credibility

5. **Add basic tests.** Even 10 pytest tests covering `Detection.to_dict()`, `BoundingBox.area`, `_decode_boxes`, the ROI endpoint, and the health check would demonstrate engineering discipline.

6. **Fix the WebSocket race condition.** Create a per-connection detector config or pass the threshold as a parameter to `detect_frame()` rather than mutating shared state.

7. **Run inference in a thread pool.** Wrap `detector.detect_frame()` in `asyncio.to_thread()` or `loop.run_in_executor()` to avoid blocking the event loop.

8. **Add a Dockerfile.** A single `Dockerfile` that builds and runs the backend would dramatically improve "just works" credibility.

9. **Check the README checklist boxes.** Unchecked checkboxes signal incompleteness to judges.

### P2 -- Nice to Have

10. **Add OpenAPI docs customization.** FastAPI auto-generates Swagger UI at `/docs` -- add example request/response bodies to the endpoint docstrings.

11. **Vectorize anchor generation.** Replace the Python loop in `_generate_anchors` with `torch.meshgrid` for a 10-50x speedup.

12. **Add a `Makefile` or `justfile`.** `make run`, `make test`, `make lint` -- standard ergonomics.

13. **Separate CSS/JS from the landing page HTML.** Extract into `style.css` and `main.js` files.

14. **Add a favicon and OpenGraph meta tags** to the landing page for social sharing.

---

## 10. OVERALL SCORE

| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Code Quality | 7.5/10 | 15% | 1.125 |
| Landing Page | 8.5/10 | 10% | 0.850 |
| ML Pipeline | 7.0/10 | 20% | 1.400 |
| Backend | 8.0/10 | 15% | 1.200 |
| Pitch Materials | 9.0/10 | 15% | 1.350 |
| Investor Readiness | 8.0/10 | 10% | 0.800 |
| Hackathon Fit | 7.5/10 | 15% | 1.125 |
| **OVERALL** | | | **7.85/10** |

### Verdict

**Strong hackathon submission with a serious credibility gap.**

The pitch materials are exceptional -- genuinely top-tier. The backend API is well-designed and feature-rich. The landing page is polished. The ML architecture is legitimate and demonstrates real computer vision knowledge.

But the project has a fundamental integrity problem: the gap between what is claimed and what is built. The pitch says 99.7% accuracy, ViT backbone, sub-50ms edge inference, Kafka pipelines, and Kubernetes deployments. The code has random weights, a CNN backbone, no edge optimization, Python dicts for storage, and a monolithic HTML file for a frontend.

For a hackathon, this is forgivable -- prototypes are expected to be aspirational. But judges who dig into the code will notice. The fix is straightforward: either train the model on MVTec AD (a free, standard benchmark) and report real numbers, or be upfront that the inference engine is a demo with simulated results. Honesty about the current state, combined with a clear roadmap, is more compelling than unverifiable claims.

**If the P0 issues are addressed, this moves from 7.85 to a 8.5+ submission.** The bones are strong. The story is compelling. The engineering is competent. It just needs its claims to match its code.

---

*End of audit. All scores reflect the state of the codebase as of 2026-03-23.*
