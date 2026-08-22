# Security Audit

Checked on 2026-08-21. Updated to correct CSRF status against actual `app.py`/`utils/security.py`
implementation (previous version of this document incorrectly listed CSRF as unenforced).

## Resolved

- **CSRF protection is enforced on every non-GET request** via `csrf_protect()` in
  `app.py`'s `before_request` hook, backed by `generate_csrf_token()` /
  `validate_csrf()` in `utils/security.py`. Tokens are embedded in every HTML form
  (`auth.html`, `admin.html`, `manage_dataset.html`, `manage_models.html`) and sent as an
  `X-CSRF-Token` header for JSON/API requests (`static/js/app.js`'s `apiFetch`). Requests
  without a valid token receive `403`.
- Uploaded JSON requests are limited to 8 MB with Flask `MAX_CONTENT_LENGTH`.
- Base64 image decoding uses strict validation.
- Pillow has a 20-million-pixel decompression limit.
- Uploaded admin filenames use `secure_filename` and are stored in staging folders.
- Uploaded model files are not activated automatically.
- Active PyTorch checkpoints use `weights_only=True` loading.
- Passwords use Werkzeug password hashing; plaintext passwords are never stored.
- Session cookies are HttpOnly and SameSite=Lax; HTTPS deployments can enable `COOKIE_SECURE=1`.
- Login `next` redirects are restricted to local paths to prevent open redirects.
- Responses include `nosniff`, `SAMEORIGIN`, Referrer-Policy, and a Content-Security-Policy header.
- Disease probability labels are inserted with DOM `textContent`, not HTML interpolation.
- Disease and yield input ranges are validated server-side.
- Sensitive endpoints (`/register`, `/login`, `/api/detect_disease`, `/api/predict_yield`,
  `/api/weather`) are rate-limited via `utils/security.py`'s `rate_limit()` decorator.

## Remaining Limitations

- The development fallback `SECRET_KEY` is intentionally available for local startup. Set a
  long random `SECRET_KEY` in production; the app raises at startup if `FLASK_ENV=production`
  and no `SECRET_KEY` is set, but this doesn't cover every non-local deployment mode.
- The Open-Meteo request is an outbound dependency with no caching, retry/backoff, or
  monitoring — a spike in weather lookups can hit Open-Meteo's own rate limits.
- The bundled yield dataset (`data/yield_data.csv`) is synthetic; model accuracy claims
  require real historical weather/yield validation before any production use.
- Admin-uploaded datasets and model weights are staged in `data/managed/` and
  `models/managed/` but not automatically schema/shape-validated against the expected
  architecture before activation — a malformed or mismatched upload could break inference if
  manually swapped in.
- Guest (unauthenticated) predictions are currently stored with a null user ID. Review
  data-retention and privacy requirements before public deployment.
- Flask's built-in server is for development only; use a production WSGI server (e.g.
  `gunicorn app:app`) and HTTPS in any real deployment.
- No automated test coverage yet for `utils/database.py`, `utils/security.py`, or the
  Flask route layer in `app.py` — current tests (`tests/test_lazy_feature_extractor.py`,
  `tests/test_spatial_features.py`, `test_app.py`) don't exercise auth, CSRF, or rate-limit
  behavior directly.
