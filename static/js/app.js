const I18N = window.APP_I18N || {};
const APP_LANG = window.APP_LANG || 'en';
const t = (key, vars = {}) => {
    let str = I18N[key] || key;
    Object.entries(vars).forEach(([k, v]) => {
        str = str.replace(`{${k}}`, v);
    });
    return str;
};

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
let lastYieldResult = null;

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
    const MAX_DIMENSION = 1024;
    const reader = new FileReader();
    reader.onerror = reject;
    reader.onload = () => {
        const img = new Image();
        img.onerror = reject;
        img.onload = () => {
            let { width, height } = img;
            if (width > MAX_DIMENSION || height > MAX_DIMENSION) {
                const scale = MAX_DIMENSION / Math.max(width, height);
                width = Math.round(width * scale);
                height = Math.round(height * scale);
            }
            const canvas = document.createElement('canvas');
            canvas.width = width;
            canvas.height = height;
            canvas.getContext('2d').drawImage(img, 0, 0, width, height);
            resolve(canvas.toDataURL('image/jpeg', 0.85).split(',')[1]);
        };
        img.src = reader.result;
    };
    reader.readAsDataURL(file);
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
            if (!crop || !file) throw new Error(t('choose_crop_and_image'));

            const imageBase64 = await fileToBase64(file);
            const response = await apiFetch('/api/detect_disease', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crop, image: imageBase64, lang: APP_LANG }),
            });
            const result = await response.json();
            hideElement('disease-loading');
            if (!response.ok) throw new Error(result.error || t('disease_detection_failed'));
            lastDiseaseResult = result;
            displayDiseaseResult(result);
        } catch (error) {
            hideElement('disease-loading');
            showError('disease-error', error.message);
        }
    });
};

const displayDiseaseResult = (result) => {
    document.getElementById('result-crop').textContent = result.crop;
    const routing = document.getElementById('result-gatekeeper');
    if (routing) {
        if (result.gatekeeper) {
            const conf = `${(result.gatekeeper.confidence * 100).toFixed(2)}%`;
            let text = t('gatekeeper_routed', { crop: result.crop, conf });
            if (result.gatekeeper.fallback && result.gatekeeper.raw_top_crop) {
                text += ' ' + t('gatekeeper_fallback', {
                    crop: result.gatekeeper.raw_top_crop,
                    alt: result.crop
                });
            }
            routing.textContent = text;
            routing.classList.remove('hidden');
        } else {
            routing.textContent = '';
            routing.classList.add('hidden');
        }
    }
    document.getElementById('result-class').textContent = result.predicted_label_display || result.predicted_label || `Class ${result.predicted_class}`;
    document.getElementById('result-confidence').textContent = `${(result.confidence * 100).toFixed(2)}%`;
    document.getElementById('result-recommendation').textContent = result.recommendation || '';

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

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        hideError('yield-error');
        hideElement('yield-result');
        showElement('yield-loading');

        try {
            const place = document.getElementById('yield-location').value;
            if (!place) throw new Error(t('choose_region_first'));

            const response = await apiFetch('/api/predict_yield', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ place }),
            });
            const result = await response.json();
            hideElement('yield-loading');
            if (!response.ok) throw new Error(result.error || t('yield_prediction_failed'));
            displayYieldResult(result);
        } catch (error) {
            hideElement('yield-loading');
            showError('yield-error', error.message);
        }
    });
};

const displayYieldResult = (result) => {
    lastYieldResult = result;
    document.getElementById('result-yield').textContent = Number(result.yield_prediction).toFixed(2);
    document.getElementById('yield-explanation').textContent = t('yield_explanation', {
        place: result.place,
        years: result.based_on_years,
        year: result.last_record_year,
    });
    showElement('yield-result');
};

const downloadReport = () => {
    if (!lastDiseaseResult && !lastYieldResult) return;
    const rows = [['Field', 'Value']];
    if (lastDiseaseResult) {
        rows.push(['Crop', lastDiseaseResult.crop]);
        rows.push(['Disease finding', lastDiseaseResult.predicted_label]);
        rows.push(['Confidence', `${(lastDiseaseResult.confidence * 100).toFixed(2)}%`]);
        rows.push(['Recommendation', lastDiseaseResult.recommendation || '']);
    }
    if (lastYieldResult) {
        rows.push(['Rice yield prediction (t/ha)', lastYieldResult.yield_prediction]);
        rows.push(['Region', lastYieldResult.place]);
    }
    rows.push(['Generated', new Date().toISOString()]);
    const csv = rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `field-companion-report-${Date.now()}.csv`;
    link.click();
    URL.revokeObjectURL(url);
};

const setupReportDownload = () => {
    document.getElementById('download-report')?.addEventListener('click', downloadReport);
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
    setupReportDownload();
    checkHealth();
    setInterval(checkHealth, 30000);
});
