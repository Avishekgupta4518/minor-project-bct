const showElement = (id) => {
    const el = document.getElementById(id);
    if (el) el.classList.remove('hidden');
};

const hideElement = (id) => {
    const el = document.getElementById(id);
    if (el) el.classList.add('hidden');
};

const showError = (id, message) => {
    const el = document.getElementById(id);
    if (el) {
        el.textContent = message;
        showElement(id);
    }
};

const hideError = (id) => hideElement(id);

const toFourDecimals = (value) => Number(Number(value).toFixed(4));

const csrfToken = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
};

const apiFetch = (url, options = {}) => {
    const headers = Object.assign({
        'X-CSRF-Token': csrfToken(),
    }, options.headers || {});
    return fetch(url, Object.assign({}, options, { headers, credentials: 'same-origin' }));
};

let lastDiseaseResult = null;

const setupNavigation = () => {
    const toggle = document.getElementById('nav-toggle');
    const menu = document.getElementById('navbar-menu');
    if (!toggle || !menu) return;
    toggle.addEventListener('click', () => menu.classList.toggle('open'));
};

const setupFilePreview = () => {
    const diseaseInput = document.getElementById('disease-image');
    if (!diseaseInput) return;
    diseaseInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        const preview = document.getElementById('image-preview');
        preview.replaceChildren();
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (loadEvent) => {
            const image = document.createElement('img');
            image.alt = 'Leaf preview';
            image.src = loadEvent.target.result;
            preview.appendChild(image);
        };
        reader.readAsDataURL(file);
    });
};

const fileToBase64 = (file) => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result.split(',')[1]);
    reader.onerror = reject;
});

const setupDiseaseDetection = () => {
    const form = document.getElementById('disease-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideError('disease-error');
        hideElement('disease-result');
        showElement('disease-loading');

        try {
            const crop = document.getElementById('crop-select').value;
            const file = document.getElementById('disease-image').files[0];
            if (!crop || !file) throw new Error('Choose a crop and upload a leaf image.');

            const imageBase64 = await fileToBase64(file);
            const response = await apiFetch('/api/detect_disease', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crop, image: imageBase64 }),
            });
            const result = await response.json();
            hideElement('disease-loading');
            if (!response.ok) throw new Error(result.error || 'Disease detection failed');
            lastDiseaseResult = result;
            const yieldCrop = document.getElementById('yield-crop');
            if (yieldCrop && !yieldCrop.value) yieldCrop.value = crop;
            displayDiseaseResult(result);
        } catch (error) {
            hideElement('disease-loading');
            showError('disease-error', error.message);
        }
    });
};

const displayDiseaseResult = (result) => {
    document.getElementById('result-crop').textContent = result.crop;
    document.getElementById('result-class').textContent = result.predicted_label || `Class ${result.predicted_class}`;
    document.getElementById('result-confidence').textContent = `${(result.confidence * 100).toFixed(2)}%`;
    const note = document.getElementById('buddy-note');
    const healthy = String(result.predicted_label || '').toLowerCase().includes('healthy');
    note.textContent = healthy
        ? 'This scan looks healthy. The yield buddy will support the weather forecast.'
        : 'This scan found a problem. The yield buddy will lower the weather-only harvest number.';

    const probDiv = document.getElementById('result-probabilities');
    probDiv.replaceChildren();
    result.all_probabilities.forEach((prob, idx) => {
        const label = result.class_labels?.[idx] || `Class ${idx}`;
        if (label === 'Invalid') return;
        const probPercent = (prob * 100).toFixed(2);
        const bar = document.createElement('div');
        bar.className = 'prob-bar';
        const labelElement = document.createElement('span');
        labelElement.className = 'prob-label';
        labelElement.textContent = label;
        const container = document.createElement('div');
        container.className = 'prob-container';
        const fill = document.createElement('div');
        fill.className = 'prob-bar-fill';
        fill.style.width = `${probPercent}%`;
        const value = document.createElement('span');
        value.className = 'prob-value';
        value.textContent = `${probPercent}%`;
        container.appendChild(fill);
        bar.append(labelElement, container, value);
        probDiv.appendChild(bar);
    });
    showElement('disease-result');
};

const setupYieldPrediction = () => {
    const form = document.getElementById('yield-form');
    if (!form) return;

    let weatherSequence = null;
    const weatherInputs = form.querySelectorAll('.weather-grid input');
    const weatherSource = document.getElementById('weather-source');

    weatherInputs.forEach((input) => input.addEventListener('input', () => {
        weatherSequence = null;
        weatherSource.textContent = 'Using the values you typed. Load a region forecast for a true future sequence.';
    }));

    document.getElementById('fetch-weather').addEventListener('click', async () => {
        const place = document.getElementById('weather-location').value;
        if (!place) {
            showError('yield-error', 'Choose a field region before loading weather.');
            return;
        }
        try {
            hideError('yield-error');
            const response = await apiFetch(`/api/weather?place=${encodeURIComponent(place)}`);
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Live weather lookup failed');
            weatherSequence = result.sequence;
            const current = weatherSequence[0];
            document.getElementById('weather-temperature').value = toFourDecimals(current.temperature).toFixed(4);
            document.getElementById('weather-rainfall').value = toFourDecimals(current.rainfall).toFixed(4);
            document.getElementById('weather-humidity').value = toFourDecimals(current.humidity).toFixed(4);
            document.getElementById('weather-soil-moisture').value = toFourDecimals(current.soil_moisture).toFixed(4);
            weatherSource.textContent = `Loaded a 12-step future forecast for ${result.location}.`;
        } catch (error) {
            showError('yield-error', error.message);
        }
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideError('yield-error');
        hideElement('yield-result');
        showElement('yield-loading');

        try {
            const rawWeather = {
                temperature: document.getElementById('weather-temperature').value,
                rainfall: document.getElementById('weather-rainfall').value,
                humidity: document.getElementById('weather-humidity').value,
                soil_moisture: document.getElementById('weather-soil-moisture').value,
            };
            if (Object.values(rawWeather).some((value) => value === '')) {
                throw new Error('Enter all weather values or load a region forecast.');
            }
            const weather = {
                temperature: Number(rawWeather.temperature),
                rainfall: Number(rawWeather.rainfall),
                humidity: Number(rawWeather.humidity),
                soil_moisture: Number(rawWeather.soil_moisture),
            };
            const crop = document.getElementById('yield-crop').value || lastDiseaseResult?.crop || null;
            const payload = weatherSequence
                ? { weather_sequence: weatherSequence }
                : { weather };
            payload.crop = crop;
            payload.place = document.getElementById('weather-location').value || null;
            if (lastDiseaseResult) {
                payload.disease = {
                    crop: lastDiseaseResult.crop,
                    predicted_class: lastDiseaseResult.predicted_class,
                    predicted_label: lastDiseaseResult.predicted_label,
                    confidence: lastDiseaseResult.confidence,
                    num_classes: lastDiseaseResult.num_classes,
                };
            }

            const response = await apiFetch('/api/predict_yield', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            const result = await response.json();
            hideElement('yield-loading');
            if (!response.ok) throw new Error(result.error || 'Yield prediction failed');
            displayYieldResult(result);
        } catch (error) {
            hideElement('yield-loading');
            showError('yield-error', error.message);
        }
    });
};

const relationshipLabel = (code) => ({
    aligned: 'Aligned',
    weather_only: 'Weather only',
    plant_supports_weather: 'Plant supports weather',
    disease_reduces_yield: 'Disease reduces yield',
    weak_shift: 'Small shift',
    mixed_signals: 'Mixed signals',
}[code] || code);

const displayYieldResult = (result) => {
    const fused = result.fused_yield ?? result.yield_prediction;
    const lstm = result.lstm_yield ?? fused;
    const adjustment = result.adjustment ?? 0;
    document.getElementById('result-yield').textContent = Number(fused).toFixed(2);
    document.getElementById('lstm-yield').textContent = `${Number(lstm).toFixed(2)} t/ha`;
    document.getElementById('yield-adjustment').textContent = `${adjustment > 0 ? '+' : ''}${Number(adjustment).toFixed(2)}`;
    document.getElementById('yield-trend').textContent = relationshipLabel(result.relationship);
    document.getElementById('yield-coverage').textContent = result.sequence_length === 12 ? '12 future steps' : 'Manual input';

    const plantUsed = result.plant && result.plant.available;
    let qualityText = plantUsed
        ? 'The buddy used both the leaf scan and the weather LSTM.'
        : 'No leaf scan was attached, so this is mostly a weather forecast.';
    if (fused >= 6.0) qualityText = `Strong outlook. ${qualityText}`;
    else if (fused >= 5.0) qualityText = `Usable outlook. ${qualityText}`;
    else if (fused >= 4.0) qualityText = `Moderate outlook. ${qualityText}`;
    else qualityText = `Low outlook. ${qualityText}`;
    document.getElementById('yield-quality').textContent = qualityText;

    const explanation = plantUsed
        ? `Weather LSTM estimated ${Number(lstm).toFixed(2)} t/ha. After plant health was included, the joined forecast is ${Number(fused).toFixed(2)} t/ha (${adjustment > 0 ? 'up' : 'down'} ${Math.abs(adjustment).toFixed(2)}). Compare this with your field notes before acting.`
        : `Scan a leaf first so the buddy can move this ${Number(fused).toFixed(2)} t/ha weather forecast with actual plant health.`;
    document.getElementById('yield-explanation').textContent = explanation;
    document.getElementById('yield-bar-fill').style.width = `${Math.min((fused / 7.0) * 100, 100)}%`;
    showElement('yield-result');
};

const checkHealth = async () => {
    try {
        const response = await apiFetch('/api/health');
        const health = await response.json();
        const indicator = document.getElementById('health-status');
        if (indicator) indicator.style.color = health.status === 'healthy' ? '#2f6b45' : '#b42318';
    } catch (error) {
        const indicator = document.getElementById('health-status');
        if (indicator) indicator.style.color = '#b42318';
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setupNavigation();
    setupFilePreview();
    setupDiseaseDetection();
    setupYieldPrediction();
    checkHealth();
    setInterval(checkHealth, 30000);
});
