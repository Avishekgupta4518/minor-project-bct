# Security Audit

Checked on 2026-08-21.

## Resolved

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

## Remaining Limitations

- Authenticated HTML POST forms do not yet have CSRF tokens. Deploy behind same-site protections and add Flask-WTF or a small token middleware before exposing the app publicly.
- The development fallback `SECRET_KEY` is intentionally available for local startup. Set a long random `SECRET_KEY` in production.
- The Open-Meteo request is an outbound dependency and should have caching, retry/backoff, and monitoring for production.
- The bundled yield dataset is synthetic; model accuracy claims require real historical weather/yield validation.
- Admin-uploaded datasets and model weights are staged but not automatically validated. Validate file schema, tensor keys, and model architecture before activation.
- Guest predictions are currently stored with a null user ID. Review data-retention and privacy requirements before public deployment.
- Flask's built-in server is for development only; use a production WSGI server and HTTPS in deployment.
