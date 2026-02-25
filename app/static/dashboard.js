// ============================================================
// SECTION NAVIGATION
// ============================================================
function showSection(id) {
    document.querySelectorAll('.section').forEach(sec => sec.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

// ============================================================
// SIDEBAR COLLAPSE
// ============================================================
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('collapsed');
    localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed') ? '1' : '0');
}

window.addEventListener('load', () => {
    const collapsed = localStorage.getItem('sidebarCollapsed') === '1';
    if (collapsed) document.querySelector('.sidebar').classList.add('collapsed');
});

// ============================================================
// COLLAPSIBLE PANELS
// ============================================================
function togglePanel(header) {
    const panel = header.parentElement;
    const body = panel.querySelector('.panel-body');
    const arrow = header.querySelector('.arrow');

    if (panel.classList.contains('collapsed')) {
        panel.classList.remove('collapsed');
        panel.classList.add('expanded');
        arrow.textContent = '▼';
        body.style.maxHeight = body.scrollHeight + "px";
    } else {
        panel.classList.remove('expanded');
        panel.classList.add('collapsed');
        arrow.textContent = '▶';
        body.style.maxHeight = "0px";
    }
}

window.addEventListener('load', () => {
    document.querySelectorAll('[data-panel]').forEach(panel => {
        const body = panel.querySelector('.panel-body');
        if (panel.classList.contains('expanded')) {
            body.style.maxHeight = body.scrollHeight + "px";
        } else {
            body.style.maxHeight = "0px";
        }
    });
});

// ============================================================
// THEME TOGGLE
// ============================================================
function applyTheme(theme) {
    if (theme === "light") {
        document.documentElement.classList.add("light");
    } else {
        document.documentElement.classList.remove("light");
    }
}

function toggleTheme() {
    const current = localStorage.getItem("theme") || "dark";
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem("theme", next);
    applyTheme(next);
}

window.addEventListener("load", () => {
    const saved = localStorage.getItem("theme") || "dark";
    applyTheme(saved);
});

// ============================================================
// BACKEND OPS
// ============================================================
async function callOps(path) {
    const res = await fetch(path, { method: "POST" });
    return res.json();
}

function killBackend() { callOps("/api/ops/backend/kill"); }
function restartBackend() { callOps("/api/ops/backend/restart"); }
function killMulti() { callOps("/api/ops/backend/kill-multi"); }

// ============================================================
// PID INSPECTOR MODAL
// ============================================================
function openPidModal(pid) {
    const modal = document.getElementById("pid-modal");
    const body = document.getElementById("pid-modal-body");

    body.textContent = "Loading...";

    fetch(`/api/health/pid/${pid}`)
        .then(res => res.json())
        .then(data => {
            body.textContent = JSON.stringify(data, null, 2);
        });

    modal.classList.remove("hidden");
}

function closePidModal() {
    document.getElementById("pid-modal").classList.add("hidden");
}

function killPid(pid) {
    fetch(`/api/ops/backend/kill-pid/${pid}`, { method: "POST" })
        .then(res => res.json())
        .then(() => {
            showAlert(`Killed PID ${pid}`);
        });
}

// ============================================================
// CHARTS + SPARKLINES
// ============================================================
let cpuChart, ramChart, perCoreChart, netChart, diskChart;
let cpuSpark, ramSpark, netSpark, diskSpark;

function initCharts() {
    cpuChart = new Chart(document.getElementById('cpu-chart'), {
        type: 'line',
        data: { labels: [], datasets: [{ label: 'CPU %', data: [], borderColor: '#4da3ff' }] },
        options: { animation: false }
    });

    ramChart = new Chart(document.getElementById('ram-chart'), {
        type: 'line',
        data: { labels: [], datasets: [{ label: 'RAM %', data: [], borderColor: '#ffb84d' }] },
        options: { animation: false }
    });

    perCoreChart = new Chart(document.getElementById('percore-chart'), {
        type: 'bar',
        data: { labels: [], datasets: [{ label: 'Per-Core CPU %', data: [], backgroundColor: '#4da3ff' }] },
        options: { animation: false }
    });

    netChart = new Chart(document.getElementById('net-chart'), {
        type: 'line',
        data: { labels: [], datasets: [
            { label: 'Bytes Sent', data: [], borderColor: '#66ff66' },
            { label: 'Bytes Received', data: [], borderColor: '#ff6666' }
        ]},
        options: { animation: false }
    });

    diskChart = new Chart(document.getElementById('disk-chart'), {
        type: 'line',
        data: { labels: [], datasets: [
            { label: 'Read Bytes', data: [], borderColor: '#4da3ff' },
            { label: 'Write Bytes', data: [], borderColor: '#ffb84d' }
        ]},
        options: { animation: false }
    });

    // Sparklines
    cpuSpark = new Chart(document.getElementById('cpu-spark'), {
        type: 'line',
        data: { labels: [], datasets: [{ data: [], borderColor: '#4da3ff', borderWidth: 1 }] },
        options: { animation: false, plugins: { legend: { display: false } } }
    });

    ramSpark = new Chart(document.getElementById('ram-spark'), {
        type: 'line',
        data: { labels: [], datasets: [{ data: [], borderColor: '#ffb84d', borderWidth: 1 }] },
        options: { animation: false, plugins: { legend: { display: false } } }
    });

    netSpark = new Chart(document.getElementById('net-spark'), {
        type: 'line',
        data: { labels: [], datasets: [{ data: [], borderColor: '#66ff66', borderWidth: 1 }] },
        options: { animation: false, plugins: { legend: { display: false } } }
    });

    diskSpark = new Chart(document.getElementById('disk-spark'), {
        type: 'line',
        data: { labels: [], datasets: [{ data: [], borderColor: '#4da3ff', borderWidth: 1 }] },
        options: { animation: false, plugins: { legend: { display: false } } }
    });
}

function updateCharts(payload) {
    const now = new Date().toLocaleTimeString();

    cpuChart.data.labels.push(now);
    cpuChart.data.datasets[0].data.push(payload.system.cpu);

    ramChart.data.labels.push(now);
    ramChart.data.datasets[0].data.push(payload.system.ram);

    perCoreChart.data.labels = payload.system_deep.per_cpu.map((_, i) => `CPU ${i}`);
    perCoreChart.data.datasets[0].data = payload.system_deep.per_cpu;

    netChart.data.labels.push(now);
    netChart.data.datasets[0].data.push(payload.system_deep.net_io.bytes_sent);
    netChart.data.datasets[1].data.push(payload.system_deep.net_io.bytes_recv);

    diskChart.data.labels.push(now);
    diskChart.data.datasets[0].data.push(payload.system_deep.disk_io.read_bytes);
    diskChart.data.datasets[1].data.push(payload.system_deep.disk_io.write_bytes);

    cpuChart.update();
    ramChart.update();
    perCoreChart.update();
    netChart.update();
    diskChart.update();

    // Sparklines
    cpuSpark.data.labels.push("");
    cpuSpark.data.datasets[0].data.push(payload.system.cpu);
    cpuSpark.update();

    ramSpark.data.labels.push("");
    ramSpark.data.datasets[0].data.push(payload.system.ram);
    ramSpark.update();

    netSpark.data.labels.push("");
    netSpark.data.datasets[0].data.push(payload.system_deep.net_io.bytes_sent);
    netSpark.update();

    diskSpark.data.labels.push("");
    diskSpark.data.datasets[0].data.push(payload.system_deep.disk_io.read_bytes);
    diskSpark.update();
}

// ============================================================
// LOG FILTERING
// ============================================================
function updateLogFilter() {
    const level = document.getElementById("log-level").value;
    fetch(`/api/logs/tail?limit=200&level=${level}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("logs-view").textContent = data.lines.join("\n");
        });
}

function updateLogSearch() {
    const term = document.getElementById("log-search").value.toLowerCase();
    const lines = document.getElementById("logs-view").textContent.split("\n");
    const filtered = lines.filter(l => l.toLowerCase().includes(term));
    document.getElementById("logs-view").textContent = filtered.join("\n");
}

// ============================================================
// AUDIT FILTERING
// ============================================================
function updateAuditSearch() {
    const term = document.getElementById("audit-search").value.toLowerCase();
    const lines = document.getElementById("audit-view").textContent.split("\n");
    const filtered = lines.filter(l => l.toLowerCase().includes(term));
    document.getElementById("audit-view").textContent = filtered.join("\n");
}

// ============================================================
// ALERT SYSTEM
// ============================================================
function showAlert(msg) {
    const banner = document.getElementById("alert-banner");
    banner.textContent = msg;
    banner.classList.remove("hidden");
    setTimeout(() => banner.classList.add("hidden"), 5000);
}

function checkAlerts(payload) {
    if (payload.system.cpu > 90) showAlert("High CPU usage detected");
    if (payload.system.ram > 90) showAlert("High RAM usage detected");

    payload.system_deep.disks.forEach(d => {
        if (d.percent > 90) showAlert(`Disk nearly full: ${d.mountpoint}`);
    });

    if (!payload.backend.running) showAlert("Backend is DOWN");
}

// ============================================================
// WEBSOCKET LIVE FEED
// ============================================================
window.addEventListener('load', () => {
    initCharts();

    const ws = new WebSocket(`ws://${location.host}/ws/dashboard`);

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);

        // Backend
        document.getElementById("backend-status").innerHTML =
            `Status: ${data.backend.running ? "RUNNING" : "STOPPED"}<br>PIDs: ${data.backend.pids}`;

        // System
        document.getElementById("system-stats").innerHTML =
            `CPU: ${data.system.cpu}%<br>RAM: ${data.system.ram}%<br>Load: ${data.system.load.join(", ")}`;

        // Ports
        document.getElementById("ports-stats").innerHTML =
            Object.entries(data.ports).map(([p, pid]) => `${p}: ${pid || "free"}`).join("<br>");

        // Top Processes
        document.getElementById("process-top").innerHTML =
            data.process_top.top_cpu.map(p => `${p.pid} ${p.name} — CPU ${p.cpu_percent}%`).join("<br>");

        // System Deep Dive
        document.getElementById("memory-stats").innerHTML =
            `Used: ${data.system_deep.memory.used} / ${data.system_deep.memory.total}`;

        document.getElementById("disk-usage").innerHTML =
            data.system_deep.disks.map(d => `${d.mountpoint}: ${d.percent}%`).join("<br>");

        // Backend Inspector
        document.getElementById("backend-inspector-status").innerHTML =
            `Running: ${data.backend.running}<br>PIDs: ${data.backend.pids}`;

        document.getElementById("backend-processes").innerHTML =
            data.process_top.top_cpu.map(p => `
                <div class="pid-row">
                    <span>${p.pid} — ${p.name} — CPU ${p.cpu_percent}%</span>
                    <button onclick="openPidModal(${p.pid})">Inspect</button>
                    <button onclick="killPid(${p.pid})" class="danger-btn">Kill</button>
                </div>
            `).join("");

        // Logs
        document.getElementById("logs-view").textContent = data.logs.join("\n");

        // Audit
        document.getElementById("audit-view").textContent = data.audit.join("\n");

        // Charts
        updateCharts(data);

        // Alerts
        checkAlerts(data);
    };
});
