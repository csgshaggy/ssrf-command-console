// ---------- Helpers ----------

async function apiGet(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(`GET ${path} failed: ${res.status}`);
    return res.json();
}

async function apiPost(path, body = null) {
    const opts = { method: "POST", headers: {} };
    if (body !== null) {
        opts.headers["Content-Type"] = "application/json";
        opts.body = JSON.stringify(body);
    }
    const res = await fetch(path, opts);
    if (!res.ok) throw new Error(`POST ${path} failed: ${res.status}`);
    return res.json();
}

async function apiDelete(path) {
    const res = await fetch(path, { method: "DELETE" });
    if (!res.ok) throw new Error(`DELETE ${path} failed: ${res.status}`);
    return res.json();
}

// ---------- Global state ----------

let allModes = [];
let recentTargets = [];

// ---------- Tabs & sidebar ----------

function setActiveTab(tabId) {
    document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
    document.getElementById(tabId).classList.add("active");

    document.querySelectorAll(".sidebar-btn").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".sidebar-btn").forEach(b => {
        if (b.dataset.tab === tabId) b.classList.add("active");
    });
}

function setupSidebar() {
    document.querySelectorAll(".sidebar-btn").forEach(btn => {
        btn.addEventListener("click", () => setActiveTab(btn.dataset.tab));
    });
}

// ---------- Backend status ----------

async function checkBackendStatus() {
    const dot = document.getElementById("backendStatusDot");
    const text = document.getElementById("backendStatusText");

    try {
        const res = await fetch("/");
        if (res.ok) {
            dot.classList.remove("down");
            dot.classList.add("ok");
            text.textContent = "Backend: Online";
        } else {
            dot.classList.remove("ok");
            dot.classList.add("down");
            text.textContent = "Backend: Error";
        }
    } catch (e) {
        dot.classList.remove("ok");
        dot.classList.add("down");
        text.textContent = "Backend: Unreachable";
    }
}

function startBackendStatusPolling() {
    checkBackendStatus();
    setInterval(checkBackendStatus, 3000);
}

// ---------- Modes ----------

async function loadModes() {
    try {
        const modes = await apiGet("/api/modes");
        allModes = modes;
        renderModeOptions(modes);
    } catch (e) {
        console.error(e);
    }
}

function renderModeOptions(modes) {
    const select = document.getElementById("modeSelect");
    select.innerHTML = "";
    modes.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m;
        opt.textContent = m;
        select.appendChild(opt);
    });
}

function setupModeSearch() {
    const input = document.getElementById("modeSearch");
    input.addEventListener("input", () => {
        const q = input.value.toLowerCase();
        const filtered = allModes.filter(m => m.toLowerCase().includes(q));
        renderModeOptions(filtered);
    });
}

// ---------- Target suggestions ----------

function addRecentTarget(target) {
    if (!target) return;
    recentTargets = [target, ...recentTargets.filter(t => t !== target)].slice(0, 20);
}

function setupTargetSuggestions() {
    const input = document.getElementById("targetInput");
    const box = document.getElementById("targetSuggestions");

    input.addEventListener("input", () => {
        const q = input.value.toLowerCase();
        if (!q) {
            box.classList.remove("visible");
            return;
        }
        const matches = recentTargets.filter(t => t.toLowerCase().includes(q));
        if (!matches.length) {
            box.classList.remove("visible");
            return;
        }
        box.innerHTML = "";
        matches.forEach(t => {
            const div = document.createElement("div");
            div.textContent = t;
            div.addEventListener("click", () => {
                input.value = t;
                box.classList.remove("visible");
            });
            box.appendChild(div);
        });
        box.classList.add("visible");
    });

    document.addEventListener("click", (e) => {
        if (!box.contains(e.target) && e.target !== input) {
            box.classList.remove("visible");
        }
    });
}

// ---------- Run mode ----------

async function runMode() {
    const mode = document.getElementById("modeSelect").value;
    const target = document.getElementById("targetInput").value;
    const outputBox = document.getElementById("outputBox");

    if (!mode || !target) {
        outputBox.textContent = "Mode and target are required.";
        return;
    }

    outputBox.textContent = "Running...";

    try {
        const data = await apiPost("/api/run", { mode, target, options: {} });
        outputBox.textContent = JSON.stringify(data, null, 2);
        addRecentTarget(target);
        await loadHistory();
    } catch (e) {
        outputBox.textContent = `Error: ${e.message}`;
    }
}

function setupRunControls() {
    document.getElementById("runBtn").addEventListener("click", runMode);
    document.getElementById("clearOutputBtn").addEventListener("click", () => {
        document.getElementById("outputBox").textContent = "Waiting for command...";
    });

    document.addEventListener("keydown", (e) => {
        if (e.ctrlKey && e.key === "Enter") {
            e.preventDefault();
            runMode();
        }
        if (e.ctrlKey && (e.key === "r" || e.key === "R")) {
            e.preventDefault();
            setActiveTab("runTab");
        }
        if (e.ctrlKey && (e.key === "h" || e.key === "H")) {
            e.preventDefault();
            setActiveTab("historyTab");
        }
        if (e.ctrlKey && (e.key === "f" || e.key === "F")) {
            e.preventDefault();
            setActiveTab("favoritesTab");
        }
        if (e.ctrlKey && (e.key === "d" || e.key === "D")) {
            e.preventDefault();
            setActiveTab("diagnosticsTab");
        }
    });
}

// ---------- History ----------

function renderHistory(history) {
    const container = document.getElementById("historyList");
    container.innerHTML = "";

    history.forEach((entry, idx) => {
        const item = document.createElement("div");
        item.className = "list-item";

        const header = document.createElement("div");
        header.className = "list-item-header";

        const left = document.createElement("div");
        left.innerHTML = `
            <span class="badge">#${idx + 1}</span>
            <span>${entry.mode || "unknown"}</span>
            <span>→</span>
            <span>${entry.target || ""}</span>
        `;

        const right = document.createElement("div");
        right.innerHTML = `<span style="font-size:11px;color:#90a4ae;">${entry.timestamp || ""}</span>`;

        header.appendChild(left);
        header.appendChild(right);

        const body = document.createElement("div");
        body.className = "list-item-body";
        body.textContent = JSON.stringify(entry.result, null, 2);

        header.addEventListener("click", () => {
            body.classList.toggle("visible");
        });

        item.appendChild(header);
        item.appendChild(body);
        container.appendChild(item);
    });
}

async function loadHistory() {
    try {
        const history = await apiGet("/api/history");
        renderHistory(history);
    } catch (e) {
        console.error(e);
    }
}

function setupHistoryControls() {
    document.getElementById("clearHistoryBtn").addEventListener("click", async () => {
        try {
            await apiDelete("/api/history");
            await loadHistory();
        } catch (e) {
            console.error(e);
        }
    });
}

// ---------- Favorites ----------

function renderFavorites(favs) {
    const container = document.getElementById("favoritesList");
    container.innerHTML = "";

    favs.forEach(mode => {
        const item = document.createElement("div");
        item.className = "list-item";

        const header = document.createElement("div");
        header.className = "list-item-header";

        const left = document.createElement("div");
        left.innerHTML = `<span class="badge">MODE</span> <span>${mode}</span>`;

        const right = document.createElement("div");
        const runBtn = document.createElement("button");
        runBtn.className = "small-btn";
        runBtn.textContent = "Run";
        runBtn.addEventListener("click", () => {
            document.getElementById("modeSelect").value = mode;
            setActiveTab("runTab");
        });

        const removeBtn = document.createElement("button");
        removeBtn.className = "small-btn";
        removeBtn.textContent = "Remove";
        removeBtn.style.marginLeft = "4px";
        removeBtn.addEventListener("click", async () => {
            try {
                await apiDelete(`/api/favorites/${mode}`);
                await loadFavorites();
            } catch (e) {
                console.error(e);
            }
        });

        right.appendChild(runBtn);
        right.appendChild(removeBtn);

        header.appendChild(left);
        header.appendChild(right);
        item.appendChild(header);
        container.appendChild(item);
    });
}

async function loadFavorites() {
    try {
        const favs = await apiGet("/api/favorites");
        renderFavorites(favs);
    } catch (e) {
        console.error(e);
    }
}

// ---------- Diagnostics ----------

async function loadDiagnostics() {
    const box = document.getElementById("diagnosticsBox");
    box.textContent = "Running diagnostics...";
    try {
        const diag = await apiGet("/api/diagnostics");
        box.textContent = JSON.stringify(diag, null, 2);
    } catch (e) {
        box.textContent = `Error: ${e.message}`;
    }
}

function setupDiagnosticsControls() {
    document.getElementById("runDiagnosticsBtn").addEventListener("click", loadDiagnostics);
}

// ---------- Structure check ----------

async function loadStructure() {
    const box = document.getElementById("structureBox");
    box.textContent = "Checking structure...";
    try {
        const data = await apiGet("/api/structure-check");
        box.textContent = JSON.stringify(data, null, 2);
    } catch (e) {
        box.textContent = `Error: ${e.message}`;
    }
}

function setupStructureControls() {
    document.getElementById("runStructureBtn").addEventListener("click", loadStructure);
}

// ---------- Themes ----------

async function loadThemes() {
    try {
        const themes = await apiGet("/api/themes");
        const select = document.getElementById("themeSelect");
        select.innerHTML = "";
        themes.forEach(t => {
            const opt = document.createElement("option");
            opt.value = t;
            opt.textContent = t;
            select.appendChild(opt);
        });
    } catch (e) {
        console.error(e);
    }
}

async function applyTheme() {
    const theme = document.getElementById("themeSelect").value;
    const info = document.getElementById("themeInfoBox");
    try {
        const res = await apiPost(`/api/themes/${theme}`);
        info.textContent = JSON.stringify(res, null, 2);
    } catch (e) {
        info.textContent = `Error: ${e.message}`;
    }
}

function setupThemeControls() {
    document.getElementById("applyThemeBtn").addEventListener("click", applyTheme);
}

// ---------- Restart backend (UI side) ----------

function showModal(message) {
    const overlay = document.getElementById("modalOverlay");
    const msgBox = document.getElementById("modalMessage");
    msgBox.textContent = message;
    overlay.classList.add("visible");
}

function hideModal() {
    document.getElementById("modalOverlay").classList.remove("visible");
}

function setupRestartControls() {
    document.getElementById("closeModalBtn").addEventListener("click", hideModal);

    document.getElementById("restartBtn").addEventListener("click", async () => {
        // Try /api/restart if it exists; otherwise show instructions.
        try {
            const res = await apiPost("/api/restart");
            showModal("Backend restart requested via /api/restart:\n\n" + JSON.stringify(res, null, 2));
        } catch (e) {
            showModal(
`/api/restart is not available.

Use your terminal to restart:

    ./restart_backend.sh

This kills all uvicorn/watchfiles processes,
waits for port 8000 to clear, and starts a clean backend.`
            );
        }
    });
}

// ---------- Init ----------

async function init() {
    setupSidebar();
    setupModeSearch();
    setupTargetSuggestions();
    setupRunControls();
    setupHistoryControls();
    setupDiagnosticsControls();
    setupStructureControls();
    setupThemeControls();
    setupRestartControls();
    startBackendStatusPolling();

    await loadModes();
    await loadHistory();
    await loadFavorites();
    await loadDiagnostics();
    await loadStructure();
    await loadThemes();
}

window.addEventListener("DOMContentLoaded", init);
