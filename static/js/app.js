const I18N = window.APP_I18N || {};
const APP_LANG = window.APP_LANG || 'en';
const t = (key, vars = {}) => {
    let str = I18N[key] || key;
    Object.entries(vars).forEach(([k, v]) => {
        str = str.replaceAll(`{${k}}`, v);
    });
    return str;
};

const REDUCED_MOTION = window.matchMedia?.('(prefers-reduced-motion: reduce)').matches;

let lastDiseaseResult = null;
let lastYieldResult = null;

/* ---------- DOM helpers ---------- */

const $id = (id) => document.getElementById(id);
const showEl = (el) => el && el.classList.remove('hidden');
const hideEl = (el) => el && el.classList.add('hidden');

const csrfToken = () => {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute('content') : '';
};

const apiFetch = (url, options = {}) => {
    const headers = Object.assign({ 'X-CSRF-Token': csrfToken() }, options.headers || {});
    return fetch(url, Object.assign({}, options, { headers, credentials: 'same-origin' }));
};

const setLoadingButton = (btnId, loading) => {
    const btn = $id(btnId);
    if (!btn) return;
    btn.disabled = loading;
    btn.classList.toggle('is-loading', loading);
};

/* ---------- Form validation ---------- */

const markFieldError = (fieldId, show) => {
    const field = $id(fieldId)?.closest('.field');
    if (!field) return;
    field.classList.toggle('has-error', show);
};

const clearFieldErrors = (form) => {
    if (!form) return;
    form.querySelectorAll('.field.has-error').forEach((f) => f.classList.remove('has-error'));
};

/* ---------- Skeleton loading ---------- */

const renderSkeleton = (container, count = 3) => {
    if (!container) return;
    container.replaceChildren();
    for (let i = 0; i < count; i++) {
        const row = document.createElement('div');
        row.style.cssText = 'display:flex;align-items:center;gap:var(--sp-3);margin:8px 0';
        const circle = document.createElement('div');
        circle.className = 'skeleton skeleton-circle';
        circle.style.cssText = 'width:36px;height:36px;flex-shrink:0';
        const lines = document.createElement('div');
        lines.style.cssText = 'flex:1;display:flex;flex-direction:column;gap:6px';
        const line1 = document.createElement('div');
        line1.className = 'skeleton skeleton-text';
        const line2 = document.createElement('div');
        line2.className = 'skeleton skeleton-text short';
        lines.append(line1, line2);
        row.append(circle, lines);
        container.appendChild(row);
    }
};

/* ---------- Toasts ---------- */

const ICONS = { success: '#i-check-circle', error: '#i-alert', info: '#i-info' };

const showToast = (message, type = 'info', duration = 4200) => {
    const stack = $id('toast-stack');
    if (!stack) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.setAttribute('role', type === 'error' ? 'alert' : 'status');
    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    icon.setAttribute('class', 'icon');
    icon.style.width = '18px';
    icon.style.height = '18px';
    const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    use.setAttribute('href', ICONS[type] || ICONS.info);
    icon.appendChild(use);
    const span = document.createElement('span');
    span.textContent = message;
    toast.append(icon, span);
    stack.appendChild(toast);
    setTimeout(() => {
        toast.classList.add('leaving');
        setTimeout(() => toast.remove(), 220);
    }, duration);
};

/* ---------- Animation helpers ---------- */

const animateValue = (element, target, { decimals = 2, suffix = '', duration = 800 } = {}) => {
    if (!element) return;
    if (REDUCED_MOTION) {
        element.textContent = `${Number(target).toFixed(decimals)}${suffix}`;
        return;
    }
    const start = performance.now();
    const step = (now) => {
        const progress = Math.min((now - start) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        element.textContent = `${(target * eased).toFixed(decimals)}${suffix}`;
        if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
};

const animateBarsIn = (container) => {
    requestAnimationFrame(() => {
        container?.querySelectorAll('[data-width]').forEach((el) => {
            el.style.width = el.dataset.width;
        });
    });
};

/* ---------- Session stats (KPI cards) ---------- */

const STATS_KEY = 'agrivision_stats';

const loadStats = () => {
    try {
        return JSON.parse(localStorage.getItem(STATS_KEY)) || { scans: 0, healthy: 0, diseased: 0, yields: [] };
    } catch {
        return { scans: 0, healthy: 0, diseased: 0, yields: [] };
    }
};

const saveStats = (stats) => {
    try { localStorage.setItem(STATS_KEY, JSON.stringify(stats)); } catch { /* private mode */ }
};

let sessionStats = loadStats();

const renderKPIs = () => {
    animateValue($id('kpi-scans'), sessionStats.scans, { decimals: 0 });
    const healthyPct = sessionStats.scans ? (sessionStats.healthy / sessionStats.scans) * 100 : null;
    const healthyEl = $id('kpi-healthy');
    if (healthyPct === null) {
        healthyEl.textContent = '–';
    } else {
        animateValue(healthyEl, healthyPct, { decimals: 1, suffix: '%' });
    }
    animateValue($id('kpi-diseased'), sessionStats.diseased, { decimals: 0 });
    const yields = sessionStats.yields;
    const avgEl = $id('kpi-yield');
    if (!yields.length) {
        avgEl.textContent = '–';
    } else {
        animateValue(avgEl, yields.reduce((a, b) => a + b, 0) / yields.length, { decimals: 2 });
    }
};

const recordDiseaseScan = (result) => {
    sessionStats.scans += 1;
    if (String(result.predicted_label || '').toLowerCase().includes('healthy')) {
        sessionStats.healthy += 1;
    } else {
        sessionStats.diseased += 1;
    }
    saveStats(sessionStats);
    renderKPIs();
};

const recordYieldPrediction = (value) => {
    sessionStats.yields.push(Number(value));
    if (sessionStats.yields.length > 50) sessionStats.yields.shift();
    saveStats(sessionStats);
    renderKPIs();
};

/* ---------- Greeting & date ---------- */

const setupGreeting = () => {
    const hour = new Date().getHours();
    const key = hour < 12 ? 'greet_morning' : hour < 17 ? 'greet_afternoon' : 'greet_evening';
    const name = document.body.dataset.user || t('farmer');
    const greetEl = $id('greet-line');
    if (greetEl) greetEl.textContent = `${t(key)}, ${name}`;
    const dateEl = $id('today-date');
    if (dateEl) {
        const locale = APP_LANG === 'ne' ? 'ne-NP' : undefined;
        dateEl.textContent = new Date().toLocaleDateString(locale, {
            weekday: 'long', year: 'numeric', month: 'long', day: 'numeric',
        });
    }
}

/* ---------- Sidebar navigation ---------- */

const setupSidebar = () => {
    const shell = $id('shell');
    const hamburger = $id('nav-toggle');
    const backdrop = $id('sidebar-backdrop');
    const collapseBtn = $id('collapse-btn');

    const setMobile = (open) => {
        shell.classList.toggle('sidebar-open', open);
        hamburger?.setAttribute('aria-expanded', String(open));
        document.body.style.overflow = open ? 'hidden' : '';
    };

    hamburger?.addEventListener('click', () =>
        setMobile(!shell.classList.contains('sidebar-open')));

    backdrop?.addEventListener('click', () => setMobile(false));

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && shell.classList.contains('sidebar-open')) {
            setMobile(false);
        }
    });

    shell.querySelectorAll('.sidebar-nav a').forEach((link) =>
        link.addEventListener('click', () => setMobile(false)));

    const KEY = 'agrivision_sidebar_collapsed';
    if (window.innerWidth > 1024 && localStorage.getItem(KEY) === '1') {
        shell.classList.add('collapsed');
    }
    collapseBtn?.addEventListener('click', () => {
        const collapsed = shell.classList.toggle('collapsed');
        localStorage.setItem(KEY, collapsed ? '1' : '0');
    });
};

/* ---------- File upload: drag & drop, paste, preview ---------- */

const previewFile = (file) => {
    const wrap = $id('image-preview');
    const dropText = $id('drop-text');
    const zone = $id('file-drop');
    if (wrap) wrap.replaceChildren();
    if (!file || !file.type.startsWith('image/')) {
        if (dropText) dropText.textContent = t('drop_hint');
        zone?.classList.remove('has-file');
        return;
    }
    if (dropText) dropText.textContent = file.name;
    zone?.classList.add('has-file');
    const reader = new FileReader();
    reader.onload = (loadEvent) => {
        if (!wrap) return;
        const holder = document.createElement('div');
        holder.className = 'preview-wrap';
        const image = document.createElement('img');
        image.alt = 'Crop preview';
        image.src = loadEvent.target.result;
        holder.appendChild(image);
        wrap.appendChild(holder);
    };
    reader.readAsDataURL(file);
};

const acceptDroppedFile = (file, input) => {
    if (!file || !input) return;
    try {
        const transfer = new DataTransfer();
        transfer.items.add(file);
        input.files = transfer.files;
    } catch { /* DataTransfer unsupported */ }
    previewFile(file);
};

const setupDropzone = () => {
    const input = $id('disease-image');
    const zone = $id('file-drop');
    if (!input || !zone) return;

    input.addEventListener('change', () => previewFile(input.files[0]));

    ['dragenter', 'dragover'].forEach((type) =>
        zone.addEventListener(type, (event) => {
            event.preventDefault();
            zone.classList.add('dragging');
        }));

    ['dragleave', 'drop'].forEach((type) =>
        zone.addEventListener(type, (event) => {
            event.preventDefault();
            zone.classList.remove('dragging');
            if (type === 'drop') acceptDroppedFile(event.dataTransfer?.files?.[0], input);
        }));

    document.addEventListener('paste', (event) => {
        const item = Array.from(event.clipboardData?.items || []).find((i) => i.type.startsWith('image/'));
        if (item) acceptDroppedFile(item.getAsFile(), input);
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

const showPreviewError = (message) => {
    const box = $id('disease-error');
    if (!box) return;
    const textEl = $id('disease-error-text');
    if (textEl) textEl.textContent = message;
    showEl(box);
};

/* ---------- Confidence ring ---------- */

const RING_CIRCUMFERENCE = 2 * Math.PI * 52;

const renderConfidenceRing = (pct, warn) => {
    const fg = $id('ring-fg');
    const label = $id('ring-pct');
    if (!fg || !label) return;
    fg.style.strokeDasharray = String(RING_CIRCUMFERENCE);
    fg.classList.toggle('warn', warn);
    fg.style.strokeDashoffset = String(RING_CIRCUMFERENCE);
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            fg.style.strokeDashoffset = String(RING_CIRCUMFERENCE * (1 - pct));
        });
    });
    animateValue(label, pct, { decimals: 1, suffix: '%', duration: 900 });
};

/* ---------- Disease detection ---------- */

const displayDiseaseResult = (result) => {
    const container = $id('disease-result');
    const label = result.predicted_label_display || result.predicted_label || `Class ${result.predicted_class}`;
    const healthy = String(result.predicted_label || '').toLowerCase().includes('healthy');
    const pct = Number(result.confidence) * 100;

    $id('result-crop').textContent = result.crop;
    $id('kv-crop').textContent = result.crop;
    $id('verdict-main').textContent = label;

    const statusBadge = $id('result-status');
    statusBadge.textContent = healthy ? t('status_healthy_badge') : t('status_diseased_badge');
    statusBadge.className = healthy ? 'badge success' : 'badge warning';

    $id('result-confidence').textContent = `${pct.toFixed(2)}%`;
    $id('result-recommendation').textContent = result.recommendation || '';

    renderConfidenceRing(pct, !healthy);

    const routing = $id('result-gatekeeper');
    if (routing) {
        if (result.gatekeeper) {
            const conf = `${(result.gatekeeper.confidence * 100).toFixed(1)}%`;
            let text = t('gatekeeper_routed', { crop: result.crop, conf });
            if (result.gatekeeper.fallback && result.gatekeeper.raw_top_crop) {
                text += ' ' + t('gatekeeper_fallback', {
                    crop: result.gatekeeper.raw_top_crop,
                    alt: result.crop,
                });
            }
            routing.style.display = 'flex';
            routing.classList.remove('hidden');
            $id('gatekeeper-text').textContent = text;
        } else {
            routing.classList.add('hidden');
        }
    }

    renderProbabilities(result);
    hideEl($id('disease-empty'));
    showEl(container);
    animateBarsIn(container);
    showEl($id('scan-again'));
};

const renderProbabilities = (result) => {
    const probBlock = $id('result-probabilities');
    if (!probBlock) return;
    probBlock.replaceChildren();

    const heading = document.createElement('p');
    heading.className = 'prob-heading';
    heading.textContent = t('class_probabilities');
    probBlock.appendChild(heading);

    const entries = result.all_probabilities
        .map((prob, idx) => ({ prob, label: result.class_labels?.[idx] || `Class ${idx}` }))
        .filter((entry) => entry.label !== 'Invalid')
        .sort((a, b) => b.prob - a.prob);

    entries.forEach((entry, rank) => {
        const probPercent = (entry.prob * 100).toFixed(2);
        const row = document.createElement('div');
        row.className = rank === 0 ? 'prob-row top' : 'prob-row';
        const name = document.createElement('span');
        name.className = rank === 0 ? 'prob-name top' : 'prob-name';
        name.textContent = entry.label;
        name.title = entry.label;
        const track = document.createElement('div');
        track.className = 'prob-track';
        const fillBar = document.createElement('div');
        fillBar.className = 'prob-fill';
        fillBar.dataset.width = `${probPercent}%`;
        const value = document.createElement('span');
        value.className = 'prob-pct';
        value.textContent = `${probPercent}%`;
        track.appendChild(fillBar);
        row.append(name, value, track);
        probBlock.appendChild(row);
    });
};

const setupDiseaseDetection = () => {
    const form = $id('disease-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearFieldErrors(form);
        const errorBox = $id('disease-error');
        hideEl(errorBox);
        hideEl($id('disease-result'));
        hideEl($id('scan-again'));
        showEl($id('disease-empty'));
        showEl($id('disease-loading'));
        setLoadingButton('scan-btn', true);
        document.querySelector('.preview-wrap')?.classList.add('scanning');

        try {
            const crop = $id('crop-select').value;
            const file = $id('disease-image').files[0];
            if (!crop) { markFieldError('crop-select', true); throw new Error(t('choose_crop_and_image')); }
            if (!file) { markFieldError('disease-image', true); throw new Error(t('choose_crop_and_image')); }

            const imageBase64 = await fileToBase64(file);
            const response = await apiFetch('/api/detect_disease', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ crop, image: imageBase64, lang: APP_LANG }),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || t('disease_detection_failed'));
            lastDiseaseResult = result;
            recordDiseaseScan(result);
            displayDiseaseResult(result);
            showToast(t('toast_scan_done'), 'success');
        } catch (error) {
            showPreviewError(error.message);
            showToast(error.message, 'error');
        } finally {
            hideEl($id('disease-loading'));
            setLoadingButton('scan-btn', false);
            document.querySelector('.preview-wrap')?.classList.remove('scanning');
        }
    });

    $id('scan-again')?.addEventListener('click', () => {
        hideEl($id('disease-result'));
        showEl($id('disease-empty'));
        form.reset();
        previewFile(null);
        $id('crop-select').focus();
    });
};

/* ---------- Yield prediction ---------- */

const ensureChartJs = () => {
    if (window.Chart) return Promise.resolve();
    return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = '/static/js/vendor/chart.umd.min.js';
        script.onload = resolve;
        script.onerror = () => reject(new Error('chart-load-failed'));
        document.head.appendChild(script);
    });
};

let yieldTrendChart = null;

const drawYieldTrend = (history, predicted) => {
    const canvas = $id('yield-trend-chart');
    if (!canvas) return;
    const css = getComputedStyle(document.documentElement);
    const green = css.getPropertyValue('--green-600').trim() || '#16A34A';
    const amber = css.getPropertyValue('--amber-600').trim() || '#D97706';
    const muted = css.getPropertyValue('--text-2').trim() || '#64748B';

    const labels = [...history.map((row) => row.year), t('chart_next_season')];
    const values = [...history.map((row) => row.yield_t_ha), predicted];
    const pointRadii = values.map((_, i) => (i >= values.length - 2 ? 5 : 3));
    const pointColors = values.map((_, i) => (i === values.length - 1 ? amber : green));

    if (yieldTrendChart) yieldTrendChart.destroy();
    yieldTrendChart = new Chart(canvas, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label: t('chart_historical'),
                data: values,
                borderColor: green,
                borderWidth: 2.5,
                tension: 0.35,
                fill: true,
                backgroundColor: 'rgba(22, 163, 74, 0.08)',
                pointRadius: pointRadii,
                pointBackgroundColor: pointColors,
                pointBorderColor: pointColors,
            }],
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: REDUCED_MOTION ? false : { duration: 700 },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: (ctx) => ` ${Number(ctx.parsed.y).toFixed(2)} t/ha`,
                    },
                },
            },
            scales: {
                x: { grid: { display: false }, ticks: { color: muted, font: { size: 10 } } },
                y: {
                    grid: { color: 'rgba(100, 116, 139, 0.12)' },
                    ticks: {
                        color: muted, font: { size: 10 },
                        callback: (v) => `${Number(v).toFixed(1)}`,
                    },
                },
            },
        },
    });
};

const displayYieldResult = async (result) => {
    lastYieldResult = result;
    recordYieldPrediction(result.yield_prediction);

    hideEl($id('yield-empty'));

    animateValue($id('result-yield'), Number(result.yield_prediction));
    $id('yield-explanation').textContent = t('yield_explanation', {
        place: result.place,
        years: result.based_on_years,
        year: result.last_record_year,
    });

    const history = result.recent_history || [];
    const deltaEl = $id('yield-delta');
    if (deltaEl) {
        if (history.length >= 2) {
            const recent = history.slice(-5);
            const mean = recent.reduce((sum, r) => sum + r.yield_t_ha, 0) / recent.length;
            const pct = ((result.yield_prediction - mean) / mean) * 100;
            const sign = pct >= 0 ? '+' : '';
            deltaEl.textContent = t('vs_recent', { pct: `${sign}${pct.toFixed(1)}` });
            deltaEl.classList.toggle('down', pct < 0);
            deltaEl.classList.remove('hidden');
        } else {
            deltaEl.classList.add('hidden');
        }
    }

    showEl($id('yield-result'));

    try {
        await ensureChartJs();
        drawYieldTrend(history, Number(result.yield_prediction));
    } catch {
        /* chart optional; big number still shown */
    }
};

const setupYieldPrediction = () => {
    const form = $id('yield-form');
    if (!form) return;

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearFieldErrors(form);
        hideEl($id('yield-error'));
        hideEl($id('yield-result'));
        showEl($id('yield-empty'));
        showEl($id('yield-loading'));
        setLoadingButton('yield-btn', true);

        try {
            const place = $id('yield-location').value;
            if (!place) { markFieldError('yield-location', true); throw new Error(t('choose_region_first')); }

            const response = await apiFetch('/api/predict_yield', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ place }),
            });
            const result = await response.json();
            if (!response.ok) throw new Error(result.error || t('yield_prediction_failed'));
            await displayYieldResult(result);
            showToast(t('toast_yield_done'), 'success');
        } catch (error) {
            const box = $id('yield-error');
            const errorText = $id('yield-error-text');
            if (errorText) errorText.textContent = error.message;
            showEl(box);
            showToast(error.message, 'error');
        } finally {
            hideEl($id('yield-loading'));
            setLoadingButton('yield-btn', false);
        }
    });
};

/* ---------- Report download ---------- */

const downloadReport = () => {
    if (!lastDiseaseResult && !lastYieldResult) {
        showToast(t('report_nothing_yet'), 'info');
        return;
    }
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
        rows.push(['Based on years', lastYieldResult.based_on_years]);
    }
    rows.push(['Generated', new Date().toISOString()]);
    const csv = rows.map((row) => row.map((cell) => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `agrivision-report-${Date.now()}.csv`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 200);
    showToast(t('toast_report_downloaded'), 'success');
};

/* ---------- Theme toggle ---------- */

const THEME_KEY = 'agrivision_theme';

const applyTheme = (theme) => {
    document.documentElement.setAttribute('data-theme', theme);
};

const getSavedTheme = () => {
    try { return localStorage.getItem(THEME_KEY); } catch { return null; }
};

const setupTheme = () => {
    const saved = getSavedTheme();
    if (saved) {
        applyTheme(saved);
    } else if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) {
        applyTheme('dark');
    }

    $id('theme-toggle')?.addEventListener('click', () => {
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        applyTheme(next);
        try { localStorage.setItem(THEME_KEY, next); } catch { /* private mode */ }
    });

    window.matchMedia?.('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!getSavedTheme()) applyTheme(e.matches ? 'dark' : 'light');
    });
};

/* ---------- Health indicator ---------- */

const checkHealth = async () => {
    const chip = $id('health-chip');
    const text = $id('health-text');
    try {
        const response = await apiFetch('/api/health');
        const health = await response.json();
        const online = health.status === 'healthy';
        chip?.classList.toggle('online', online);
        chip?.classList.toggle('offline', !online);
        if (text) text.textContent = online ? t('status_online') : t('status_offline');
    } catch {
        chip?.classList.add('offline');
        chip?.classList.remove('online');
        if (text) text.textContent = t('status_offline');
    }
};

document.addEventListener('DOMContentLoaded', () => {
    setupTheme();
    document.body.classList.add('body-visible');
    setupSidebar();
    setupGreeting();
    setupDropzone();
    setupDiseaseDetection();
    setupYieldPrediction();
    $id('download-report')?.addEventListener('click', downloadReport);
    renderKPIs();
    checkHealth();
    setInterval(checkHealth, 30000);
    if (!REDUCED_MOTION && 'IntersectionObserver' in window) {
        const obs = new IntersectionObserver((entries) => {
            entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('visible'); obs.unobserve(e.target); } });
        }, { threshold: 0.1 });
        document.querySelectorAll('.reveal').forEach((el) => obs.observe(el));
    } else {
        document.querySelectorAll('.reveal').forEach((el) => el.classList.add('visible'));
    }
});
