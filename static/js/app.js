// static/js/app.js

// Utility functions
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

const hideError = (id) => {
    hideElement(id);
};

const toFourDecimals = (value) => Number(Number(value).toFixed(4));

// File input preview
const setupFilePreview = () => {
    const diseaseInput = document.getElementById('disease-image');
    if (diseaseInput) {
        diseaseInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const preview = document.getElementById('image-preview');
                    preview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Crop upload boxes
    const cropInputs = document.querySelectorAll('.crop-input');
    cropInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    const preview = input.parentElement.querySelector('.crop-preview');
                    preview.innerHTML = `<img src="${event.target.result}" alt="Preview">`;
                };
                reader.readAsDataURL(file);
            }
        });
    });
};

// Convert file to base64
const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = () => {
            const base64 = reader.result.split(',')[1];
            resolve(base64);
        };
        reader.onerror = (error) => reject(error);
    });
};

// Disease Detection Form Handler
const setupDiseaseDetection = () => {
    const form = document.getElementById('disease-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError('disease-error');
        hideElement('disease-result');
        showElement('disease-loading');

        try {
            const cropSelect = document.getElementById('crop-select');
            const imageInput = document.getElementById('disease-image');
            const crop = cropSelect.value;
            const file = imageInput.files[0];

            if (!crop || !file) {
                throw new Error('Please select a crop and upload an image');
            }
            if (crop === 'other') {
                throw new Error('Other crops are not supported by the trained disease models yet.');
            }

            const imageBase64 = await fileToBase64(file);

            const response = await fetch('/api/detect_disease', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    crop: crop,
                    image: imageBase64
                })
            });

            hideElement('disease-loading');

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Disease detection failed');
            }

            const result = await response.json();
            displayDiseaseResult(result);

        } catch (error) {
            hideElement('disease-loading');
            showError('disease-error', error.message);
        }
    });
};

// Display disease detection results
const displayDiseaseResult = (result) => {
    document.getElementById('result-crop').textContent = result.crop.toUpperCase();
    document.getElementById('result-class').textContent = result.predicted_label || `Class ${result.predicted_class}`;
    document.getElementById('result-confidence').textContent = 
        `${(result.confidence * 100).toFixed(2)}%`;

    // Display probability bars
    const probDiv = document.getElementById('result-probabilities');
    probDiv.replaceChildren();

    result.all_probabilities.forEach((prob, idx) => {
        const probPercent = (prob * 100).toFixed(2);
        const label = result.class_labels?.[idx] || `Class ${idx}`;
        if (label === 'Invalid') return;
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

// Yield Prediction Form Handler
const setupYieldPrediction = () => {
    const form = document.getElementById('yield-form');
    if (!form) return;

    let weatherSequence = null;
    const weatherInputs = form.querySelectorAll('.weather-grid input');
    const weatherSource = document.getElementById('weather-source');

    weatherInputs.forEach(input => input.addEventListener('input', () => {
        weatherSequence = null;
        weatherSource.textContent = 'Using manually entered weather conditions.';
    }));

    document.getElementById('fetch-weather').addEventListener('click', async () => {
        const place = document.getElementById('weather-location').value;
        if (place === '') {
            showError('yield-error', 'Choose an agricultural region before getting live weather.');
            return;
        }

        try {
            hideError('yield-error');
            const response = await fetch(`/api/weather?place=${encodeURIComponent(place)}`);
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || 'Live weather lookup failed');

            weatherSequence = result.sequence;
            const current = weatherSequence[0];
            document.getElementById('weather-temperature').value = toFourDecimals(current.temperature).toFixed(4);
            document.getElementById('weather-rainfall').value = toFourDecimals(current.rainfall).toFixed(4);
            document.getElementById('weather-humidity').value = toFourDecimals(current.humidity).toFixed(4);
            document.getElementById('weather-soil-moisture').value = toFourDecimals(current.soil_moisture).toFixed(4);
            weatherSource.textContent = `Live 12-step forecast loaded for ${result.location} from Open-Meteo.`;
        } catch (error) {
            showError('yield-error', error.message);
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
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
            if (Object.values(rawWeather).some(value => value === '')) {
                throw new Error('Enter all weather values or load a live agricultural-region forecast.');
            }

            const weather = {
                temperature: Number(rawWeather.temperature),
                rainfall: Number(rawWeather.rainfall),
                humidity: Number(rawWeather.humidity),
                soil_moisture: Number(rawWeather.soil_moisture),
            };

            const payload = weatherSequence
                ? { weather_sequence: weatherSequence }
                : { weather };
            const response = await fetch('/api/predict_yield', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(payload)
            });

            hideElement('yield-loading');

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Yield prediction failed');
            }

            const result = await response.json();
            displayYieldResult(result);

        } catch (error) {
            hideElement('yield-loading');
            showError('yield-error', error.message);
        }
    });
};

// Display yield prediction results
const displayYieldResult = (result) => {
    const yieldValue = result.yield_prediction;
    const trendText = yieldValue >= 6.0
        ? 'Excellent'
        : yieldValue >= 5.0
            ? 'Healthy'
            : yieldValue >= 4.0
                ? 'Moderate'
                : 'Low';

    document.getElementById('result-yield').textContent = yieldValue.toFixed(2);
    document.getElementById('yield-trend').textContent = trendText;
    document.getElementById('yield-coverage').textContent = result.sequence_length === 12 ? '12 weather steps' : 'Manual input';

    let qualityText = '';
    if (yieldValue >= 6.0) {
        qualityText = '✅ Excellent Yield - Optimal growing conditions';
    } else if (yieldValue >= 5.0) {
        qualityText = '👍 Good Yield - Healthy crop development';
    } else if (yieldValue >= 4.0) {
        qualityText = '⚠️ Moderate Yield - Monitor for improvements';
    } else {
        qualityText = '❌ Low Yield - Requires attention';
    }

    document.getElementById('yield-quality').textContent = qualityText;

    const explanation = yieldValue >= 6.0
        ? `The model estimates about ${yieldValue.toFixed(2)} tons of harvest per hectare under these conditions. This is a favorable forecast, so continue monitoring water, pests, and crop health.`
        : yieldValue >= 5.0
            ? `The model estimates about ${yieldValue.toFixed(2)} tons of harvest per hectare. Conditions look usable, but better irrigation, nutrition, and disease monitoring may improve the harvest.`
            : yieldValue >= 4.0
                ? `The model estimates about ${yieldValue.toFixed(2)} tons of harvest per hectare. Review rainfall, soil moisture, temperature stress, and crop disease risks before making decisions.`
                : `The model estimates about ${yieldValue.toFixed(2)} tons of harvest per hectare. Treat this as a warning to inspect the field and address water, soil, temperature, or disease problems.`;
    document.getElementById('yield-explanation').textContent = `${explanation} The estimate is a decision-support forecast, not a guaranteed harvest. It uses ${result.sequence_length === 12 ? '12 weather steps' : 'the entered weather values'} and should be compared with local field records.`;

    const maxYield = 7.0;
    const percentage = Math.min((yieldValue / maxYield) * 100, 100);
    const yieldBarFill = document.getElementById('yield-bar-fill');
    yieldBarFill.style.width = percentage + '%';

    showElement('yield-result');
};

// Health Check
const checkHealth = async () => {
    try {
        const response = await fetch('/api/health');
        const health = await response.json();
        
        const indicator = document.getElementById('health-status');
        if (indicator) {
            if (health.status === 'healthy') {
                indicator.textContent = '●';
                indicator.style.color = '#2ecc71';
            } else {
                indicator.textContent = '●';
                indicator.style.color = '#e74c3c';
            }
        }
    } catch (error) {
        console.error('Health check failed:', error);
    }
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    setupFilePreview();
    setupDiseaseDetection();
    setupYieldPrediction();
    checkHealth();

    // Periodic health check
    setInterval(checkHealth, 30000);
});
