# app.py
import io
import json
import os
from functools import wraps
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from PIL import Image
from werkzeug.utils import secure_filename

from config import AGRICULTURAL_LOCATIONS, CROP_NAMES, DEVICE, WEATHER_SEQUENCE_LENGTH
from utils.database import (
    add_prediction,
    authenticate_user,
    connection,
    count_records,
    create_user,
    find_user,
    find_user_by_email,
    init_database,
    list_predictions,
    list_users,
    prediction_summary,
)
from utils.feature_extractor import FeatureExtractor
from utils.security import csrf_protect, generate_csrf_token, rate_limit, validate_image
from utils.yield_pipeline import YieldPipeline, parse_weather_payload

Image.MAX_IMAGE_PIXELS = 20_000_000

app = Flask(__name__, template_folder="templates", static_folder="static")
secret_key = os.getenv("SECRET_KEY")
if not secret_key:
    if os.getenv("FLASK_ENV") == "production":
        raise RuntimeError("SECRET_KEY must be set in production.")
    secret_key = "development-only-change-this-secret"
app.config["SECRET_KEY"] = secret_key
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("COOKIE_SECURE", "0") == "1"
init_database()

feature_extractor = FeatureExtractor()
yield_pipeline = YieldPipeline()
yield_model_ready = yield_pipeline.spatial_ready


@app.context_processor
def inject_globals():
    return {
        "csrf_token": generate_csrf_token(),
        "user": current_user(),
    }


@app.before_request
def enforce_csrf():
    if request.endpoint in {"static"}:
        return None
    return csrf_protect(lambda: None)()


@app.after_request
def add_security_headers(response):
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Content-Security-Policy",
        "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; base-uri 'self'; form-action 'self'",
    )
    response.headers.setdefault("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
    if getattr(g, "rate_remaining", None) is not None:
        response.headers["X-RateLimit-Remaining"] = str(g.rate_remaining)
    return response


def current_user():
    user_id = session.get("user_id")
    return find_user(user_id) if user_id else None


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                if request.path.startswith("/api/"):
                    return jsonify({"error": "Authentication required."}), 401
                return redirect(url_for("login", next=request.path))
            if user["role"] not in roles:
                if request.path.startswith("/api/"):
                    return jsonify({"error": "You do not have permission for this resource."}), 403
                return render_template("error.html", code=403, message="You do not have permission for this page."), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator


@app.route("/")
def index():
    return render_template(
        "index.html",
        crops=CROP_NAMES,
        yield_model_ready=yield_model_ready,
        buddy_ready=yield_pipeline.buddy_ready,
        agricultural_locations=AGRICULTURAL_LOCATIONS,
    )


@app.route("/register", methods=["GET", "POST"])
@rate_limit(20, 60)
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        if not name or not email or "@" not in email or "." not in email.split("@")[-1]:
            flash("Enter a valid name and email address.", "error")
            return render_template("auth.html", mode="register")
        if len(password) < 8:
            flash("Name, email, and a password of at least 8 characters are required.", "error")
            return render_template("auth.html", mode="register")
        if find_user_by_email(email):
            flash("An account with that email already exists.", "error")
            return render_template("auth.html", mode="register")
        create_user(name, email, password)
        flash("Account created. Please sign in.", "success")
        return redirect(url_for("login"))
    return render_template("auth.html", mode="register")


@app.route("/login", methods=["GET", "POST"])
@rate_limit(12, 60)
def login():
    if request.method == "POST":
        user = authenticate_user(request.form.get("email", ""), request.form.get("password", ""))
        if not user:
            flash("Invalid email or password.", "error")
            return render_template("auth.html", mode="login")
        session.clear()
        session["user_id"] = user["id"]
        generate_csrf_token()
        next_url = request.args.get("next", "")
        if not next_url.startswith("/") or next_url.startswith("//"):
            next_url = url_for("index")
        return redirect(next_url)
    return render_template("auth.html", mode="login")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/history")
@role_required("farmer", "analyst", "admin")
def history():
    user = current_user()
    records = list_predictions(None if user["role"] in ("analyst", "admin") else user["id"])
    return render_template("history.html", records=records)


@app.route("/admin")
@role_required("admin")
def admin_dashboard():
    return render_template(
        "admin.html",
        users=list_users(),
        users_count=count_records("users"),
        predictions_count=count_records("prediction_history"),
        summaries=prediction_summary(),
        yield_model_ready=yield_model_ready,
        buddy_ready=yield_pipeline.buddy_ready,
    )


@app.route("/admin/dataset", methods=["GET", "POST"])
@role_required("admin")
def manage_dataset():
    dataset_dir = Path(app.root_path) / "data" / "managed"
    dataset_dir.mkdir(parents=True, exist_ok=True)
    if request.method == "POST":
        uploaded = request.files.get("dataset")
        if not uploaded or not uploaded.filename.lower().endswith(".csv"):
            flash("Upload a CSV dataset.", "error")
        else:
            filename = secure_filename(uploaded.filename)
            if not filename:
                flash("Invalid filename.", "error")
            else:
                uploaded.save(dataset_dir / filename)
                flash(f"Dataset {filename} uploaded for review.", "success")
        return redirect(url_for("manage_dataset"))
    files = sorted(path.name for path in dataset_dir.glob("*.csv"))
    return render_template("manage_dataset.html", files=files)


@app.route("/admin/models", methods=["GET", "POST"])
@role_required("admin")
def manage_models():
    model_dir = Path(app.root_path) / "models" / "managed"
    model_dir.mkdir(parents=True, exist_ok=True)
    if request.method == "POST":
        uploaded = request.files.get("model")
        if not uploaded or not uploaded.filename.lower().endswith((".pth", ".pt")):
            flash("Upload a PyTorch .pth or .pt model file.", "error")
        else:
            filename = secure_filename(uploaded.filename)
            if not filename:
                flash("Invalid filename.", "error")
            else:
                uploaded.save(model_dir / filename)
                flash(f"Model {filename} uploaded for review. Restart after validating weights.", "success")
        return redirect(url_for("manage_models"))
    files = sorted(path.name for path in model_dir.iterdir() if path.is_file())
    return render_template("manage_models.html", files=files)


@app.route("/api/analytics")
@role_required("analyst", "admin")
def analytics():
    return jsonify({
        "users": count_records("users"),
        "predictions": count_records("prediction_history"),
        "summary": [dict(item) for item in prediction_summary()],
    })


@app.route("/admin/users/<int:user_id>/role", methods=["POST"])
@role_required("admin")
def update_user_role(user_id):
    role = request.form.get("role", "")
    if role not in {"farmer", "analyst", "admin"}:
        flash("Invalid role.", "error")
        return redirect(url_for("admin_dashboard"))
    if user_id == session.get("user_id") and role != "admin":
        flash("You cannot remove your own admin role.", "error")
        return redirect(url_for("admin_dashboard"))
    with connection() as database:
        database.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
    flash("User role updated.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/analyst")
@role_required("analyst", "admin")
def analyst_dashboard():
    return render_template("history.html", records=list_predictions(), analyst_view=True)


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "yield_model_ready": yield_model_ready,
        "buddy_ready": yield_pipeline.buddy_ready,
        "device": DEVICE,
        "crops": CROP_NAMES,
    })


@app.route("/api/weather", methods=["GET"])
@rate_limit(20, 60)
def weather():
    place_key = request.args.get("place", "").lower()
    location = AGRICULTURAL_LOCATIONS.get(place_key)
    if not location:
        return jsonify({"error": "Choose a supported agricultural region."}), 400

    query = urlencode({
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "hourly": "temperature_2m,precipitation,relative_humidity_2m",
        "forecast_days": 2,
        "timezone": "auto",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{query}"

    try:
        http_request = Request(url, headers={"User-Agent": "SmartMultiCrop/1.0"})
        with urlopen(http_request, timeout=15) as response:
            payload = json.load(response)
    except TimeoutError:
        app.logger.error("Weather API timeout for %s", place_key)
        return jsonify({"error": "Weather service timed out. Please try again later."}), 503
    except OSError:
        app.logger.error("Weather API connection error for %s", place_key)
        return jsonify({"error": "Could not connect to weather service. Check your network."}), 503
    except Exception:
        app.logger.exception("Unexpected weather lookup failure for %s", place_key)
        return jsonify({"error": "Weather service is unavailable right now."}), 503

    hourly = payload.get("hourly", {})
    temp = hourly.get("temperature_2m", [])
    precip = hourly.get("precipitation", [])
    humidity = hourly.get("relative_humidity_2m", [])

    if len(temp) < WEATHER_SEQUENCE_LENGTH or len(precip) < WEATHER_SEQUENCE_LENGTH or len(humidity) < WEATHER_SEQUENCE_LENGTH:
        return jsonify({"error": "Incomplete forecast data from weather service."}), 503

    sequence = []
    for index in range(WEATHER_SEQUENCE_LENGTH):
        sequence.append({
            "temperature": round(float(temp[index]), 2),
            "rainfall": round(max(0.0, float(precip[index])), 2),
            "humidity": round(float(humidity[index]), 2),
            "soil_moisture": round(min(100.0, float(humidity[index]) * 0.55 + float(precip[index]) * 4.0), 2),
        })

    return jsonify({
        "sequence": sequence,
        "source": "Open-Meteo",
        "location": location["name"],
        "length": WEATHER_SEQUENCE_LENGTH,
        "place": place_key,
    })


def decode_image(image_data):
    import base64

    try:
        img_bytes = base64.b64decode(image_data, validate=True)
    except Exception as exc:
        raise ValueError("Invalid image encoding.") from exc
    if len(img_bytes) > 8 * 1024 * 1024:
        raise ValueError("Image is too large.")
    image = Image.open(io.BytesIO(img_bytes))
    validate_image(image)
    image = image.convert("RGB")
    image.thumbnail((4096, 4096))
    return image


def store_prediction(prediction_type, input_data, **fields):
    user = current_user()
    add_prediction(user["id"] if user else None, prediction_type, input_data, **fields)


@app.route("/api/detect_disease", methods=["POST"])
@rate_limit(20, 60)
def detect_disease():
    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        crop_name = data.get("crop")
        image_data = data.get("image")
        if not crop_name or not image_data:
            return jsonify({"error": "Missing crop or image data"}), 400
        if crop_name == "other":
            return jsonify({"error": "Other crops are not supported by the trained disease models. Select a listed crop."}), 422
        if crop_name not in CROP_NAMES:
            return jsonify({"error": "That crop is not supported."}), 400
        if not isinstance(image_data, str) or len(image_data) > 12_000_000:
            return jsonify({"error": "Image payload is invalid or too large."}), 400

        image = decode_image(image_data)
        result = feature_extractor.detect_disease(crop_name, image)
        if "error" in result:
            return jsonify(result), 400

        store_prediction(
            "disease",
            {"crop": crop_name},
            crop=crop_name,
            disease_class=result["predicted_class"],
            disease_label=result["predicted_label"],
            confidence=result["confidence"],
        )
        return jsonify(result), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Disease detection failed")
        return jsonify({"error": "Disease detection failed. Try another clear leaf photo."}), 500


@app.route("/api/predict_yield", methods=["POST"])
@rate_limit(20, 60)
def predict_yield():
    if not yield_model_ready:
        return jsonify({"error": "Yield model checkpoint not found."}), 503

    try:
        data = request.get_json(silent=True)
        if not data:
            return jsonify({"error": "No JSON data"}), 400

        weather_steps = parse_weather_payload(data)
        crop_name = data.get("crop")
        if crop_name and crop_name not in CROP_NAMES:
            return jsonify({"error": "That crop is not supported."}), 400
        place_key = (data.get("place") or "").lower() or None
        if place_key and place_key not in AGRICULTURAL_LOCATIONS:
            return jsonify({"error": "Choose a supported agricultural region."}), 400

        disease_result = data.get("disease")
        if disease_result is not None and not isinstance(disease_result, dict):
            return jsonify({"error": "Disease context must be an object from the plant scan."}), 400
        if isinstance(disease_result, dict):
            allowed = {
                "crop",
                "predicted_class",
                "predicted_label",
                "confidence",
                "num_classes",
            }
            disease_result = {key: disease_result[key] for key in allowed if key in disease_result}

        result = yield_pipeline.predict(
            weather_steps,
            crop_name=crop_name,
            disease_result=disease_result,
            place_key=place_key,
        )
        store_prediction(
            "yield",
            {
                "weather": weather_steps,
                "crop": crop_name,
                "place": place_key,
                "relationship": result["relationship"],
            },
            crop=crop_name,
            yield_prediction=result["fused_yield"],
            disease_label=result["relationship"],
            confidence=result["plant"]["health"] if result["plant"]["available"] else None,
        )
        result["weather_features"] = ["temperature", "rainfall", "humidity", "soil_moisture"]
        return jsonify(result), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Yield prediction failed")
        return jsonify({"error": "Yield prediction failed. Check the weather values and try again."}), 500


if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")   # <-- changed here
    port = int(os.getenv("FLASK_PORT", "5000"))
    app.run(debug=False, use_reloader=False, host=host, port=port)
