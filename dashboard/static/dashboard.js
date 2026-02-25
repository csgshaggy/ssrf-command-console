const API_BASE = "http://127.0.0.1:5001";

let logStreamInterval = null;

/* ============================
   TAB SWITCHING
============================ */
function showTab(name) {
    const tabs = document.querySelectorAll(".tab-content");
    tabs.forEach(t => t.style.display = "none");

    const el = document.getElementById(name + "-tab");
    if (el) el.style.display = "block";
}

/* ============================
   THEME TOGGLE
============================ */
function toggleTheme() {
    const body = document.body;
    if (body.classList.contains("theme-dark")) {
        body.classList.remove("theme-dark");
        body.classList.add("theme-light");
    } else {
        body.classList.remove("theme-light");
        body.classList.add("theme-dark");
    }
}

/* ============================
   SCAN LOGIC
============================ */
async function runScan() {
    const ips = document.getElementById("scan-ips").value.split(",").map(x => x.trim()).filter(Boolean);
    const workers = parseInt(document.getElementById("scan-workers").value || "10", 10);

    document.getElementById("scan-output").textContent = "Running scan...";

    try {
        const res = await fetch(`${API_BASE}/scan`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ips, workers })
        });

        const data = await res.json();
        document.getElementById("scan-output").textContent = JSON.stringify(data, null, 2);
        document.getElementById("results-output").textContent = JSON.stringify(data.summaries, null, 2);
    } catch (e) {
        document.getElementById("scan-output").textContent = "Error contacting backend.";
    }
}

/* ============================
   CONTROL PANEL HELPERS
============================ */
function setControlOutput(text) {
    document.getElementById("control-output").textContent = text;
}

function setBackendStatus(ok) {
    const hb = document.getElementById("heartbeat");
    const label = document.getElementById("heartbeat-label");

    if (ok) {
        hb.classList.add("heartbeat-ok");
        hb.classList.remove("heartbeat-bad");
        label.textContent = "Backend: Online";
    } else {
        hb.classList.add("heartbeat-bad");
        hb.classList.remove("heartbeat-ok");
        label.textContent = "Backend: Offline";
    }
}

/* ============================
   CONTROL PANEL ACTIONS
============================ */
async function cpHealth() {
    setControlOutput("Checking backend health...");
    try {
        const res = await fetch(`${API_BASE}/control/health`);
        const data = await res.json();
        setBackendStatus(true);
        setControlOutput(JSON.stringify(data, null, 2));
    } catch {
        setBackendStatus(false);
        setControlOutput("Backend unreachable.");
    }
}

async function cpPorts() {
    setControlOutput("Checking ports...");
    const res = await fetch(`${API_BASE}/control/ports`);
    const data = await res.json();
    setControlOutput(JSON.stringify(data, null, 2));
}

async function cpProcesses() {
    setControlOutput("Fetching processes...");
    const res = await fetch(`${API_BASE}/control/processes`);
    const data = await res.json();
    setControlOutput(data.processes || "No processes.");
}

async function cpManualScan() {
    setControlOutput("Running manual scan...");
    const res = await fetch(`${API_BASE}/control/manual_scan`, { method: "POST" });
    const data = await res.json();
    setControlOutput(JSON.stringify(data, null, 2));
}

async function cpLogs() {
    setControlOutput("Fetching logs...");
    const res = await fetch(`${API_BASE}/control/logs`);
    const data = await res.json();
    setControlOutput(data.logs || "No logs.");
}

/* ============================
   LOG STREAMING
============================ */
async function fetchLogsForStream() {
    try {
        const res = await fetch(`${API_BASE}/control/logs`);
        const data = await res.json();
        const existing = document.getElementById("control-output").textContent;
        const combined = (existing + "\n\n" + (data.logs || "")).trim();
        document.getElementById("control-output").textContent = combined;
        const el = document.getElementById("control-output");
        el.scrollTop = el.scrollHeight;
    } catch {
        // ignore errors during streaming
    }
}

function cpStartLogStream() {
    setControlOutput("Starting log stream...");
    if (logStreamInterval) clearInterval(logStreamInterval);
    logStreamInterval = setInterval(fetchLogsForStream, 3000);
}

function cpStopLogStream() {
    if (logStreamInterval) {
        clearInterval(logStreamInterval);
        logStreamInterval = null;
    }
    setControlOutput("Log stream stopped.");
}

/* ============================
   BACKEND RESTART
============================ */
async function cpRestartBackend() {
    setControlOutput("Restarting backend...");

    try {
        await fetch(`${API_BASE}/control/restart_backend`, { method: "POST" });
    } catch {
        // Expected: backend dies before responding
    }

    setBackendStatus(false);
    setControlOutput("Backend restarting...");

    // Auto-reconnect loop
    let attempts = 0;
    const interval = setInterval(async () => {
        attempts++;
        try {
            const res = await fetch(`${API_BASE}/control/health`);
            if (res.ok) {
                clearInterval(interval);
                setBackendStatus(true);
                setControlOutput("Backend is back online.");
            }
        } catch {
            // still offline
        }
        if (attempts > 20) {
            clearInterval(interval);
            setControlOutput("Backend did not return after restart.");
        }
    }, 500);
}

/* ============================
   INITIAL HEARTBEAT
============================ */
(async function initialHeartbeat() {
    try {
        const res = await fetch(`${API_BASE}/control/health`);
        setBackendStatus(res.ok);
    } catch {
        setBackendStatus(false);
    }
})();
