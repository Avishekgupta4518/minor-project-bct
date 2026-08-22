# TASK.md — Smart Multi-Crop Disease Detection & Yield Prediction
### Consolidated Improvement Plan (Farmer Usability + Academic Rigor)

> Work top to bottom. Each phase is checked in and demo-able on its own — don't jump ahead.

---

## Phase 0 — Documentation Cleanup (do this first, ~1 hour)

Nothing else matters if your docs contradict your code — this is the first thing a teacher checks.

- [ ] Delete `PROJECT_SUMMARY.md`, `DEPLOYMENT_READY.txt`, `IMPLEMENTATION_STATUS.md`
- [ ] Rewrite `README.md` as the single source of truth:
  - Real architecture (Gatekeeper CNN → species CNN, Spatial LSTM → Buddy Fusion), not the old single-CNN SRS diagram
  - One accurate "Status" section (no more contradicting checklists)
  - Setup instructions for Linux/Mac AND Windows
- [ ] Keep `PROJECT_CONTEXT.md` only as a dated historical/internal spec, clearly marked **superseded by README**
- [ ] Fix `SECURITY_AUDIT.md` — move CSRF, security headers, cookie flags from "Remaining Limitations" to "Resolved" (they're already implemented)
- [ ] Add `.gitignore`: `*.pth`, `data/*.db`, `.venv/`, `__pycache__/`, `data/managed/`, `models/managed/`
- [ ] Fix `requirements.txt` — add missing `timm` (GatekeeperCNN needs it; fresh installs currently break)

---

## Phase 1 — Farmer-Facing Quick Wins (~1–2 days)

These directly answer "what should I do?" for the actual end user — highest value-per-effort.

- [ ] **Action recommendations after disease detection** — static dict in `config.py` mapping each disease label → 1-2 line advice + "consult local extension officer" fallback. No ML required, pure lookup.
- [ ] **Input tooltips/placeholders** — explain each weather field in plain language ("Temperature in °C for your field right now").
- [ ] **History trend chart** — add Chart.js to `templates/history.html`: yield-over-time line chart + disease-occurrence bar chart per crop. Turns raw SQLite rows into insight.
- [ ] **Client-side image compression** before upload (canvas resize to ~1024px before base64 encode) — reduces payload on slow mobile connections, cuts server load.
- [ ] **Download report button** — generate a simple PDF/CSV per prediction (disease + yield + weather) so farmers can save/share with an advisor. Use `reportlab` or the existing `pdf` skill.

## Phase 1.5 — Nice-to-Have Farmer Features (only if time remains)
- [ ] Nepali/English language toggle (highest-impact "nice-to-have" given target region — Chitwan, Jhapa, Kailali etc. are Nepali-speaking)
- [ ] SMS/email alert for critical predictions (skip unless you already have Twilio/SMTP creds — don't chase this if it eats your timeline)
- [ ] Offline PWA capture-now-predict-later — genuinely useful but complex; only attempt after everything else is done

---

## Phase 2 — Engineering Credibility for Teachers (~3–5 days)

- [ ] **Tests** — add `pytest` coverage for `utils/database.py`, `utils/security.py`, `utils/yield_pipeline.py`, and key `app.py` routes (auth, role checks, disease/yield endpoints). This is the single highest-leverage grading item — currently only 2 test files exist and none cover the DB, security, or route layer.
- [ ] **CI** — `.github/workflows/ci.yml` running `pytest` (and `pytest --cov` for a coverage report/badge) on every push.
- [ ] **Swagger/OpenAPI docs** — `flask-swagger-ui` or `flasgger` so `/api/health`, `/api/detect_disease`, `/api/predict_yield`, `/api/weather` are interactively testable and documented as a real contract.
- [ ] **Dockerfile + docker-compose.yml** — one-command launch (app + model weights). Proves deployability without your teacher fighting your Windows PowerShell steps.
- [ ] **Production WSGI entrypoint** — `gunicorn app:app` in the Docker image instead of Flask's dev server; confirm `SECRET_KEY`/`DATABASE_PATH`/`COOKIE_SECURE` are read from env vars (mostly already true).
- [ ] **Architecture diagram** — one accurate Mermaid diagram in the README replacing the stale SRS diagram.

---

## Phase 3 — Hardening & Ops (do after Phase 2, if time allows)

- [ ] **Structured logging** (JSON logs) + a lightweight `/api/metrics` endpoint (request counts, latency, error counts) — you already have `/api/health`, this extends it.
- [ ] **Validate uploaded models/datasets before activation** — check tensor keys/shapes against expected architecture before an admin-uploaded `.pth` can be swapped in; currently files are staged but unchecked.
- [ ] **Cache Open-Meteo responses** (in-memory TTL cache is enough — Redis is optional) to avoid hammering the weather API and speed up repeated region lookups.
- [ ] **Guided "how to use" page** with screenshots (skip Shepherd.js unless you have spare time — a static page is 90% of the value for 10% of the effort).

---

## Phase 4 — Only If Genuinely Ahead of Schedule

- [ ] PostgreSQL support alongside SQLite (shows scalability awareness — not required for a demo-scale minor project)
- [ ] Background retraining pipeline (Celery + Redis) triggered on admin dataset upload
- [ ] Simple model registry with version tags + rollback in the admin panel
- [ ] A/B comparison between two CNN checkpoints

---

## ❌ Explicitly Out of Scope (say no to these)

| Idea | Why not |
|---|---|
| IoT sensor integration | Needs hardware, not a software-project deliverable |
| Real-time satellite imagery | Overkill, depends on paid external APIs |
| Native mobile app | Responsive web/PWA already covers this |
| Blockchain / "AI fairness" reports | Irrelevant to the agricultural mission; "BCT" here is your TU IOE program code, not a blockchain requirement |
| Full multi-tenancy / enterprise org support | Current user/role system already covers farmer/analyst/admin needs |
| Model versioning + A/B testing as a *first* priority | Correct instinct, wrong order — only attempt in Phase 4 if everything above is done |

---

## Suggested Order of Attack

1. Phase 0 (docs) — same day
2. Phase 1 (farmer quick wins) — days 1–2
3. Phase 2 (teacher credibility: tests, CI, Docker, Swagger) — days 3–5
4. Phase 3 (hardening) — if time remains
5. Phase 1.5 / Phase 4 — only as stretch goals

**Rule of thumb:** every item you add should have a clear, statable benefit to either the farmer or the grader. If you can't say who it's for in one sentence, cut it.
