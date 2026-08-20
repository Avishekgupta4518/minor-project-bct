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
    document.getElementById('result-class').textContent = `Class ${result.predicted_class}`;
    document.getElementById('result-confidence').textContent = 
        `${(result.confidence * 100).toFixed(2)}%`;

    // Display probability bars
    const probDiv = document.getElementById('result-probabilities');
    probDiv.innerHTML = '';
    
    result.all_probabilities.forEach((prob, idx) => {
        const probPercent = (prob * 100).toFixed(2);
        const barHTML = `
            <div class="prob-bar">
                <span class="prob-label">Class ${idx}</span>
                <div class="prob-container">
                    <div class="prob-bar-fill" style="width: ${probPercent}%"></div>
                </div>
                <span class="prob-value">${probPercent}%</span>
            </div>
        `;
        probDiv.innerHTML += barHTML;
    });

    showElement('disease-result');
};

// Yield Prediction Form Handler
const setupYieldPrediction = () => {
    const form = document.getElementById('yield-form');
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        hideError('yield-error');
        hideElement('yield-result');
        showElement('yield-loading');

        try {
            const imageData = {};
            const cropInputs = document.querySelectorAll('.crop-input');

            for (const input of cropInputs) {
                const crop = input.name;
                const file = input.files[0];
                if (file) {
                    const imageBase64 = await fileToBase64(file);
                    imageData[crop] = imageBase64;
                }
            }

            if (Object.keys(imageData).length === 0) {
                throw new Error('Please upload at least one crop image');
            }

            const response = await fetch('/api/predict_yield', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(imageData)
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
    document.getElementById('yield-coverage').textContent = `${Math.min(100, Math.round((yieldValue / 7.0) * 100))}%`;

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
