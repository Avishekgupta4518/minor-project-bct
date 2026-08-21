# app.py
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import torch
from pathlib import Path
from models.lstm_model import YieldLSTM
from utils.feature_extractor import FeatureExtractor
from config import (
    CROP_NAMES,
    DEVICE,
    WEATHER_FEATURES,
    WEATHER_LSTM_MODEL_PATH,
    WEATHER_RANGES,
    WEATHER_SEQUENCE_LENGTH,
    AGRICULTURAL_LOCATIONS,
)
import base64
from PIL import Image
import io
import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen
from functools import wraps
from werkzeug.utils import secure_filename
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

Image.MAX_IMAGE_PIXELS = 20_000_000

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'development-only-change-this-secret'
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = os.getenv('COOKIE_SECURE', '0') == '1'
init_database()

# Load weather LSTM model
lstm_model = YieldLSTM(input_size=len(WEATHER_FEATURES), hidden_size=64, num_layers=2).to(DEVICE)
yield_model_ready = Path(WEATHER_LSTM_MODEL_PATH).exists()
if yield_model_ready:
    lstm_model.load_state_dict(torch.load(WEATHER_LSTM_MODEL_PATH, map_location=DEVICE, weights_only=True))
    lstm_model.eval()
else:
    app.logger.warning("Weather yield model checkpoint not found at %s. Train train_lstm.py first.", WEATHER_LSTM_MODEL_PATH)

# Feature extractor
feature_extractor = FeatureExtractor()


@app.after_request
def add_security_headers(response):
    response.headers.setdefault('X-Content-Type-Options', 'nosniff')
    response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
    response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
    response.headers.setdefault('Content-Security-Policy', "default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'")
    return response


def current_user():
    user_id = session.get('user_id')
    return find_user(user_id) if user_id else None


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = current_user()
            if not user:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'Authentication required.'}), 401
                return redirect(url_for('login', next=request.path))
            if user['role'] not in roles:
                if request.path.startswith('/api/'):
                    return jsonify({'error': 'You do not have permission for this resource.'}), 403
                return render_template('error.html', code=403, message='You do not have permission for this page.'), 403
            return view(*args, **kwargs)
        return wrapped
    return decorator

@app.route('/')
def index():
    """Home page - dashboard"""
    return render_template(
        'index.html',
        crops=CROP_NAMES,
        yield_model_ready=yield_model_ready,
        agricultural_locations=AGRICULTURAL_LOCATIONS,
        user=current_user(),
    )


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or not email or len(password) < 8:
            flash('Name, email, and a password of at least 8 characters are required.', 'error')
            return render_template('auth.html', mode='register')
        if find_user_by_email(email):
            flash('An account with that email already exists.', 'error')
            return render_template('auth.html', mode='register')
        create_user(name, email, password)
        flash('Account created. Please sign in.', 'success')
        return redirect(url_for('login'))
    return render_template('auth.html', mode='register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = authenticate_user(request.form.get('email', ''), request.form.get('password', ''))
        if not user:
            flash('Invalid email or password.', 'error')
            return render_template('auth.html', mode='login')
        session.clear()
        session['user_id'] = user['id']
        next_url = request.args.get('next', '')
        if not next_url.startswith('/') or next_url.startswith('//'):
            next_url = url_for('index')
        return redirect(next_url)
    return render_template('auth.html', mode='login')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/history')
@role_required('farmer', 'analyst', 'admin')
def history():
    user = current_user()
    records = list_predictions(None if user['role'] in ('analyst', 'admin') else user['id'])
    return render_template('history.html', records=records, user=user)


@app.route('/admin')
@role_required('admin')
def admin_dashboard():
    return render_template(
        'admin.html',
        users=list_users(),
        users_count=count_records('users'),
        predictions_count=count_records('prediction_history'),
        summaries=prediction_summary(),
        user=current_user(),
    )


@app.route('/admin/dataset', methods=['GET', 'POST'])
@role_required('admin')
def manage_dataset():
    dataset_dir = Path(app.root_path) / 'data' / 'managed'
    dataset_dir.mkdir(parents=True, exist_ok=True)
    if request.method == 'POST':
        uploaded = request.files.get('dataset')
        if not uploaded or not uploaded.filename.lower().endswith('.csv'):
            flash('Upload a CSV dataset.', 'error')
        else:
            filename = secure_filename(uploaded.filename)
            uploaded.save(dataset_dir / filename)
            flash(f'Dataset {filename} uploaded for review.', 'success')
        return redirect(url_for('manage_dataset'))
    files = sorted(path.name for path in dataset_dir.glob('*.csv'))
    return render_template('manage_dataset.html', files=files, user=current_user())


@app.route('/admin/models', methods=['GET', 'POST'])
@role_required('admin')
def manage_models():
    model_dir = Path(app.root_path) / 'models' / 'managed'
    model_dir.mkdir(parents=True, exist_ok=True)
    if request.method == 'POST':
        uploaded = request.files.get('model')
        if not uploaded or not uploaded.filename.lower().endswith(('.pth', '.pt')):
            flash('Upload a PyTorch .pth or .pt model file.', 'error')
        else:
            filename = secure_filename(uploaded.filename)
            uploaded.save(model_dir / filename)
            flash(f'Model {filename} uploaded for review. Restart after validating weights.', 'success')
        return redirect(url_for('manage_models'))
    files = sorted(path.name for path in model_dir.iterdir() if path.is_file())
    return render_template('manage_models.html', files=files, user=current_user())


@app.route('/api/analytics')
@role_required('analyst', 'admin')
def analytics():
    return jsonify({
        'users': count_records('users'),
        'predictions': count_records('prediction_history'),
        'summary': [dict(item) for item in prediction_summary()],
    })


@app.route('/admin/users/<int:user_id>/role', methods=['POST'])
@role_required('admin')
def update_user_role(user_id):
    role = request.form.get('role', '')
    if role not in {'farmer', 'analyst', 'admin'}:
        flash('Invalid role.', 'error')
        return redirect(url_for('admin_dashboard'))
    with connection() as database:
        database.execute('UPDATE users SET role = ? WHERE id = ?', (role, user_id))
    flash('User role updated.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/analyst')
@role_required('analyst', 'admin')
def analyst_dashboard():
    return render_template('history.html', records=list_predictions(), user=current_user(), analyst_view=True)

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'yield_model_ready': yield_model_ready,
        'device': DEVICE,
        'crops': CROP_NAMES
    })

@app.route('/api/weather', methods=['GET'])
def weather():
    """Fetch a 12-step weather sequence for a supported agricultural region."""
    place_key = request.args.get('place', '').lower()
    location = AGRICULTURAL_LOCATIONS.get(place_key)
    if not location:
        return jsonify({'error': f'Location "{place_key}" not supported. Choose from: {list(AGRICULTURAL_LOCATIONS.keys())}'}), 400

    latitude = location['latitude']
    longitude = location['longitude']

    query = urlencode({
        'latitude': latitude,
        'longitude': longitude,
        'hourly': 'temperature_2m,precipitation,relative_humidity_2m',
        'forecast_days': 2,
        'timezone': 'auto',
    })
    url = f'https://api.open-meteo.com/v1/forecast?{query}'

    try:
        with urlopen(url, timeout=15) as response:
            payload = json.load(response)
    except TimeoutError as te:
        app.logger.error(f"Weather API timeout for {place_key}: {te}")
        return jsonify({'error': 'Weather service timed out. Please try again later.'}), 503
    except ConnectionError as ce:
        app.logger.error(f"Weather API connection error for {place_key}: {ce}")
        return jsonify({'error': 'Could not connect to weather service. Check your network.'}), 503
    except Exception as e:
        app.logger.error(f"Unexpected error fetching weather for {place_key}: {e}")
        return jsonify({'error': f'Weather service unavailable: {str(e)}'}), 503

    hourly = payload.get('hourly', {})
    temp = hourly.get('temperature_2m', [])
    precip = hourly.get('precipitation', [])
    humidity = hourly.get('relative_humidity_2m', [])

    # Ensure we have at least WEATHER_SEQUENCE_LENGTH readings
    if len(temp) < WEATHER_SEQUENCE_LENGTH or len(precip) < WEATHER_SEQUENCE_LENGTH or len(humidity) < WEATHER_SEQUENCE_LENGTH:
        app.logger.warning(f"Incomplete weather data for {place_key}: temp={len(temp)}, precip={len(precip)}, humidity={len(humidity)}")
        return jsonify({'error': 'Incomplete forecast data from weather service.'}), 503

    # Build the sequence
    sequence = []
    for i in range(WEATHER_SEQUENCE_LENGTH):
        step = {
            'temperature': round(temp[i], 2),
            'rainfall': round(precip[i], 2),
            'humidity': round(humidity[i], 2),
            'soil_moisture': round(min(100.0, humidity[i] * 0.55 + precip[i] * 4.0), 2),
        }
        sequence.append(step)

    return jsonify({
        'sequence': sequence,
        'source': 'Open-Meteo',
        'location': location['name'],
        'length': WEATHER_SEQUENCE_LENGTH,
    }), 200

@app.route('/api/detect_disease', methods=['POST'])
def detect_disease():
    """
    Detect disease for a specific crop from an uploaded image.
    
    Expected JSON:
    {
        "crop": "apple",
        "image": "<base64_encoded_image>"
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        crop_name = data.get('crop')
        image_data = data.get('image')
        
        if not crop_name or not image_data:
            return jsonify({'error': 'Missing crop or image data'}), 400
        
        if crop_name == 'other':
            return jsonify({'error': 'Other crops are not supported by the trained disease models. Select a listed crop.'}), 422
        if crop_name not in CROP_NAMES:
            return jsonify({'error': f'Crop {crop_name} not supported. Supported crops: {CROP_NAMES}'}), 400
        
        # Decode base64 image
        try:
            img_bytes = base64.b64decode(image_data, validate=True)
            image = Image.open(io.BytesIO(img_bytes)).convert('RGB')
            image.thumbnail((4096, 4096))
        except Exception as e:
            return jsonify({'error': f'Invalid image data: {str(e)}'}), 400
        
        # Detect disease
        result = feature_extractor.detect_disease(crop_name, image)
        
        if 'error' in result:
            return jsonify(result), 400

        user = current_user()
        add_prediction(
            user['id'] if user else None,
            'disease',
            {'crop': crop_name},
            crop=crop_name,
            disease_class=result['predicted_class'],
            disease_label=result['predicted_label'],
            confidence=result['confidence'],
        )
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/predict_yield', methods=['POST'])
def predict_yield():
    """
    Predict crop yield from current weather conditions.
    
    Expected JSON:
    {"weather": {"temperature": 26, "rainfall": 180, "humidity": 70, "soil_moisture": 62}}
    """
    if not yield_model_ready:
        return jsonify({'error': 'Yield model checkpoint not found. Train the LSTM model first.'}), 503

    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data'}), 400

        weather_sequence = data.get('weather_sequence')
        if weather_sequence is not None:
            if not isinstance(weather_sequence, list) or len(weather_sequence) != WEATHER_SEQUENCE_LENGTH:
                return jsonify({'error': f'weather_sequence must contain {WEATHER_SEQUENCE_LENGTH} steps.'}), 400
            weather = weather_sequence
        else:
            weather = data.get('weather')
        if not isinstance(weather, dict):
            if not isinstance(weather, list):
                return jsonify({'error': 'Weather data or a 12-step weather_sequence is required.'}), 400

        weather_steps = weather if isinstance(weather, list) else [weather] * WEATHER_SEQUENCE_LENGTH

        normalized = []
        for weather_step in weather_steps:
            missing_features = [feature for feature in WEATHER_FEATURES if feature not in weather_step]
            if missing_features:
                return jsonify({'error': f'Missing weather fields: {", ".join(missing_features)}'}), 400
            normalized_step = []
            for feature in WEATHER_FEATURES:
                try:
                    value = float(weather_step[feature])
                except (TypeError, ValueError):
                    return jsonify({'error': f'{feature} must be numeric.'}), 400
                minimum, maximum = WEATHER_RANGES[feature]
                if not minimum <= value <= maximum:
                    return jsonify({'error': f'{feature} must be between {minimum:g} and {maximum:g}.'}), 400
                normalized_step.append((value - minimum) / (maximum - minimum))
            normalized.append(normalized_step)

        features = torch.tensor([normalized], dtype=torch.float32).to(DEVICE)

        # Predict yield
        with torch.no_grad():
            yield_pred = lstm_model(features).item()

        user = current_user()
        add_prediction(
            user['id'] if user else None,
            'yield',
            {'weather': weather_steps},
            yield_prediction=round(yield_pred, 2),
        )

        return jsonify({
            'yield_prediction': round(yield_pred, 2),
            'weather_features': WEATHER_FEATURES,
            'sequence_length': WEATHER_SEQUENCE_LENGTH,
        }), 200
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)