// ------------------------------
// PANEL SWITCHING
// ------------------------------
function showPanel(name) {
    document.querySelectorAll(".panel").forEach(p => p.classList.remove("active"));
    document.getElementById(`panel-${name}`).classList.add("active");
}

showPanel("run");

// ------------------------------
// API HELPERS
// ------------------------------
async function apiGet(path) {
    const res = await fetch(path);
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}

async function apiPost(path, body) {
    const res = await fetch(path, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body || {})
    });
    if (!res.ok) throw new Error(await res.text());
    return res.json();
}

// ------------------------------
// RUN MODE
// ------------------------------
async function loadModes() {
    const history = await apiGet("/api/history");
    const modes = [...new Set(history.map(h => h.mode))];

    const select = document.getElementById("modeSelect");
    select.innerHTML = "";
    modes.forEach(m => {
        const opt = document.createElement("option");
        opt.value = m;
        opt.textContent = m;
        select.appendChild(opt);
    });
}

async function runMode() {
    const mode = document.getElementById("modeSelect").value;
    const target = document.getElementById("targetInput").value;
    const optionsRaw = document.getElementById("optionsInput").value;

    let options = {};
    if (optionsRaw.trim()) {
        try { options = JSON.parse(optionsRaw); }
        catch { alert("Invalid JSON in options"); return; }
    }

    const data = await apiPost("/api/run_mode", { mode, target, options });
    document.getElementById("runOutput").textContent =
        JSON.stringify(data, null, 2);
}

// ------------------------------
// RUN LAST MODE
// ------------------------------
async function runLastMode() {
    const data = await apiPost("/api/run_last");
    alert("Last mode executed");
    document.getElementById("runOutput").textContent =
        JSON.stringify(data, null, 2);
}

// ------------------------------
// LIVE SCAN (WEBSOCKET)
// ------------------------------
let ws = null;

function startLiveScan() {
    const textarea = document.getElementById("liveIpsInput");
    const ips = textarea.value
        .split("\n")
        .map(s => s.trim())
        .filter(Boolean);

    if (!ips.length) {
        alert("Enter at least one IP");
        return;
    }

    ws = new WebSocket(`ws://${window.location.host}/ws/scan`);

    ws.onopen = () => {
        ws.send(JSON.stringify({ ips }));
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const out = document.getElementById("liveOutput");

        if (data.type === "result") {
            out.textContent += `\n[${data.ip}]\n` +
                JSON.stringify(data.data, null, 2) + "\n";
        } else if (data.type === "done") {
            out.textContent += `\n--- Scan complete (${data.count} IPs) ---\n`;
        } else if (data.type === "error") {
            out.textContent += `\n[ERROR] ${data.message}\n`;
        }

        out.scrollTop = out.scrollHeight;
    };

    document.getElementById("liveOutput").textContent =
        `Starting scan for ${ips.length} IP(s)...\n`;
}

// ------------------------------
// HISTORY
// ------------------------------
async function loadHistory() {
    const list = document.getElementById("historyList");
    list.innerHTML = "";

    const entries = await apiGet("/api/history");

    entries.forEach((e, i) => {
        const div = document.createElement("div");
        div.innerHTML = `
            <h3>[${i+1}] ${e.mode}</h3>
            <pre>${JSON.stringify(e, null, 2)}</pre>
            <hr>
        `;
        list.appendChild(div);
    });
}

// ------------------------------
// FAVORITES
// ------------------------------
async function loadFavorites() {
    const favs = await apiGet("/api/favorites");
    const list = document.getElementById("favoritesList");

    list.innerHTML = favs.map(f => `<div>${f}</div>`).join("");
}

async function addFavorite() {
    const mode = document.getElementById("favAddInput").value;
    await apiPost("/api/favorites/add", { mode });
    loadFavorites();
}

async function removeFavorite() {
    const mode = document.getElementById("favRemoveInput").value;
    await apiPost("/api/favorites/remove", { mode });
    loadFavorites();
}

// ------------------------------
// DIAGNOSTICS
// ------------------------------
async function loadDiagnostics() {
    const data = await apiGet("/api/diagnostics");
    document.getElementById("diagnosticsOutput").textContent =
        JSON.stringify(data, null, 2);
}

// ------------------------------
// STRUCTURE CHECK
// ------------------------------
async function loadStructureCheck() {
    const data = await apiGet("/api/structure_check");
    document.getElementById("structureOutput").textContent =
        data.output.join("\n");
}

// ------------------------------
// THEMES
// ------------------------------
async function loadThemes() {
    const data = await apiGet("/api/themes");
    const select = document.getElementById("themeSelect");

    select.innerHTML = "";
    data.themes.forEach(t => {
        const opt = document.createElement("option");
        opt.value = t;
        opt.textContent = t;
        select.appendChild(opt);
    });
}

async function applyTheme() {
    const theme = document.getElementById("themeSelect").value;
    await apiPost("/api/theme/set", { theme });
    alert("Theme applied");
}

// ------------------------------
// INITIAL LOAD
// ------------------------------
loadModes();
loadHistory();
loadFavorites();
loadDiagnostics();
loadStructureCheck();
loadThemes();
