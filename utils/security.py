import secrets
import time
from collections import defaultdict, deque
from functools import wraps

from flask import abort, g, jsonify, request, session

ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP"}
RATE_LIMIT_WINDOW_SECONDS = 60
RATE_LIMIT_MAX_REQUESTS = 40
_RATE_BUCKET_LIMIT = 4096
_rate_buckets = defaultdict(deque)
_last_bucket_prune = 0.0


def generate_csrf_token():
    token = session.get("_csrf_token")
    if not token:
        token = secrets.token_urlsafe(32)
        session["_csrf_token"] = token
    return token


def validate_csrf():
    if request.method in {"GET", "HEAD", "OPTIONS"}:
        return True
    sent = request.headers.get("X-CSRF-Token") or request.form.get("csrf_token")
    expected = session.get("_csrf_token")
    if not expected or not sent or not secrets.compare_digest(str(sent), str(expected)):
        return False
    return True


def csrf_protect(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if request.method not in {"GET", "HEAD", "OPTIONS"} and not validate_csrf():
            if request.path.startswith("/api/") or request.is_json:
                return jsonify({"error": "Invalid or missing security token. Refresh the page and try again."}), 403
            abort(403)
        return view(*args, **kwargs)
    return wrapped


def client_key():
    forwarded = request.headers.get("X-Forwarded-For", "")
    if forwarded:
        return forwarded.split(",")[0].strip()[:128]
    return request.remote_addr or "unknown"


def prune_rate_buckets(now):
    """Drop stale buckets so the in-memory store cannot grow without bound."""
    global _last_bucket_prune
    if now - _last_bucket_prune < RATE_LIMIT_WINDOW_SECONDS:
        return
    _last_bucket_prune = now
    if len(_rate_buckets) <= _RATE_BUCKET_LIMIT:
        return
    for key in [key for key, bucket in _rate_buckets.items() if not bucket]:
        del _rate_buckets[key]


def rate_limit(max_requests=RATE_LIMIT_MAX_REQUESTS, window_seconds=RATE_LIMIT_WINDOW_SECONDS):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            now = time.time()
            prune_rate_buckets(now)
            bucket = _rate_buckets[f"{view.__name__}:{client_key()}"]
            while bucket and now - bucket[0] > window_seconds:
                bucket.popleft()
            if len(bucket) >= max_requests:
                if request.path.startswith("/api/") or request.is_json:
                    return jsonify({"error": "Too many requests. Please wait a moment and try again."}), 429
                abort(429)
            bucket.append(now)
            g.rate_remaining = max_requests - len(bucket)
            return view(*args, **kwargs)
        return wrapped
    return decorator


def validate_image(image):
    image_format = (image.format or "").upper()
    if image_format not in ALLOWED_IMAGE_FORMATS:
        raise ValueError("Only JPEG, PNG, or WEBP images are allowed.")
    width, height = image.size
    if width < 16 or height < 16:
        raise ValueError("Image is too small to analyze.")
    if width * height > 20_000_000:
        raise ValueError("Image is too large.")
    return image
