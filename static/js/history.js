// static/js/history.js — renders history-page charts from embedded JSON payloads.
document.addEventListener('DOMContentLoaded', () => {
    if (typeof Chart === 'undefined') return;

    const readJson = (id) => {
        const el = document.getElementById(id);
        if (!el) return null;
        try { return JSON.parse(el.textContent); } catch { return null; }
    };

    const yieldPayload = readJson('yield-trend-data');
    if (yieldPayload && Array.isArray(yieldPayload.trend) && yieldPayload.trend.length > 0) {
        new Chart(document.getElementById('yield-trend-chart'), {
            type: 'line',
            data: {
                labels: yieldPayload.trend.map((item) => item.date),
                datasets: [{
                    label: 'Predicted yield (t/ha)',
                    data: yieldPayload.trend.map((item) => item.yield),
                    borderColor: '#16A34A',
                    backgroundColor: 'rgba(22,163,74,0.10)',
                    tension: 0.35,
                    fill: true,
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }

    const diseasePayload = readJson('disease-count-data');
    if (diseasePayload && diseasePayload.counts && Object.keys(diseasePayload.counts).length > 0) {
        new Chart(document.getElementById('disease-count-chart'), {
            type: 'bar',
            data: {
                labels: Object.keys(diseasePayload.counts),
                datasets: [{
                    label: 'Scans',
                    data: Object.values(diseasePayload.counts),
                    backgroundColor: '#16A34A',
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });
    }
});
