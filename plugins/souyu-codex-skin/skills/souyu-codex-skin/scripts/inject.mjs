// Codex Lite Skin injector - injects a minimal background style into the
// running Codex desktop app over CDP. Keeps the default app layout.
import { readFileSync } from "node:fs";
import { existsSync, readdirSync } from "node:fs";
import http from "node:http";
import { execFileSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.argv[process.argv.indexOf("--port") + 1] ?? 9335);
const servePort = Number(process.argv[process.argv.indexOf("--serve") + 1] ?? 0);
const watchMode = process.argv.includes("--watch");
const removeMode = process.argv.includes("--remove");

let artB64 = "";
let artDarkB64 = "";
let css = "";
let skins = [];
let currentSkin = null;

function loadAssets() {
  artB64 = readFileSync(path.join(__dirname, "art.jpg")).toString("base64");
  try {
    artDarkB64 = readFileSync(path.join(__dirname, "art-dark.jpg")).toString("base64");
  } catch {
    artDarkB64 = artB64;
  }
  css = readFileSync(path.join(__dirname, "style.css"), "utf8")
    .split("__ART_DARK__")
    .join(`data:image/jpeg;base64,${artDarkB64}`)
    .split("__ART__")
    .join(`data:image/jpeg;base64,${artB64}`);
}

function loadSkins() {
  const dir = path.join(__dirname, "..", "skins");
  const list = [];
  if (existsSync(dir)) {
    for (const name of readdirSync(dir)) {
      const mf = path.join(dir, name, "skin.json");
      if (!existsSync(mf)) continue;
      try {
        const m = JSON.parse(readFileSync(mf, "utf8"));
        list.push({ id: m.id || name, label: m.label || name });
      } catch {}
    }
  }
  list.sort((a, b) => a.label.localeCompare(b.label, "zh-CN"));
  skins = list;
  currentSkin = null;
  try {
    const statePath = path.join(process.env.LOCALAPPDATA || "", "CodexLiteSkin", "state.json");
    const raw = readFileSync(statePath, "utf8").replace(/^\uFEFF/, "");
    currentSkin = JSON.parse(raw).currentSkin || null;
  } catch {}
}

function widgetScript() {
  const data = JSON.stringify({ skins, current: currentSkin });
  return `(() => {
    const DATA = ${data};
    const SERVE = "http://127.0.0.1:${servePort}";
    const ID = "codex-skin-switcher";
    const old = document.getElementById(ID);
    if (old) old.remove();
    const aside = document.querySelector("aside.app-shell-left-panel");
    if (!aside) return false;
    const wrap = document.createElement("div");
    wrap.id = ID;
    wrap.className = "codex-skin-switcher";
    const currentLabel = (DATA.skins.find((s) => s.id === DATA.current) || {}).label || "";
    const items = DATA.skins
      .map((s) =>
        '<div class="codex-skin-item-row">' +
        '<button type="button" class="codex-skin-item" data-skin="' + s.id + '">' +
        s.label + (s.id === DATA.current ? "（当前）" : "") + "</button>" +
        '<button type="button" class="codex-skin-del" data-skin="' + s.id + '" title="删除这套皮肤">✕</button>' +
        "</div>",
      )
      .join("");
    wrap.innerHTML =
      '<button type="button" class="codex-skin-btn" title="切换皮肤">' +
      '<span class="codex-skin-dot"></span>' +
      '<span class="codex-skin-btn-label">皮肤</span>' +
      '<span class="codex-skin-current"></span></button>' +
      '<div class="codex-skin-menu" hidden>' + items + "</div>";
    aside.appendChild(wrap);
    wrap.querySelector(".codex-skin-current").textContent = currentLabel;
    const menu = wrap.querySelector(".codex-skin-menu");
    wrap.querySelector(".codex-skin-btn").addEventListener("click", (e) => {
      e.stopPropagation();
      menu.hidden = !menu.hidden;
    });
    document.addEventListener("click", () => {
      document.querySelectorAll(".codex-skin-menu").forEach((m) => {
        m.hidden = true;
      });
      document.querySelectorAll(".codex-skin-del[data-confirm='1']").forEach((d) => {
        d.dataset.confirm = "";
        d.textContent = "✕";
      });
    });
    wrap.querySelectorAll(".codex-skin-item").forEach((it) => {
      it.addEventListener("click", () => {
        window.__codexSkinPending = it.dataset.skin;
        it.disabled = true;
        it.textContent = "切换中…";
      });
    });
    wrap.querySelectorAll(".codex-skin-del").forEach((del) => {
      del.addEventListener("click", (e) => {
        e.stopPropagation();
        if (del.dataset.confirm === "1") {
          window.__codexSkinPendingDelete = del.dataset.skin;
          del.disabled = true;
          del.textContent = "删除中…";
        } else {
          del.dataset.confirm = "1";
          del.textContent = "确认";
        }
      });
    });
    return true;
  })()`;
}

async function listTargets() {
  for (const host of ["127.0.0.1", "[::1]"]) {
    try {
      const res = await fetch(`http://${host}:${port}/json/list`);
      if (res.ok) return await res.json();
    } catch {}
  }
  return null;
}

const isMain = (t) =>
  t.type === "page" && t.url.startsWith("app://-/index.html") && !t.url.includes("initialRoute");

async function connect(target) {
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    ws.addEventListener("open", resolve, { once: true });
    ws.addEventListener("error", () => reject(new Error("ws error")), { once: true });
  });
  let seq = 1;
  const send = (method, params = {}) => {
    const id = seq++;
    ws.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve) => {
      const onMsg = (e) => {
        const msg = JSON.parse(String(e.data));
        if (msg.id === id) {
          ws.removeEventListener("message", onMsg);
          resolve(msg);
        }
      };
      ws.addEventListener("message", onMsg);
    });
  };
  return { ws, send };
}

async function applyTo(session) {
  const styleExpr = `(() => {
    document.documentElement.classList.add("lite-skin");
    let st = document.getElementById("codex-lite-skin-style");
    if (!st) {
      st = document.createElement("style");
      st.id = "codex-lite-skin-style";
      (document.head || document.documentElement).appendChild(st);
    }
    st.textContent = ${JSON.stringify(css)};
    return true;
  })()`;
  const r1 = await session.send("Runtime.evaluate", { expression: styleExpr, returnByValue: true });
  let ok = !(r1.result?.exceptionDetails || r1.error);
  if (ok && servePort) {
    const r2 = await session.send("Runtime.evaluate", { expression: widgetScript(), returnByValue: true });
    ok = !(r2.result?.exceptionDetails || r2.error);
  }
  return ok;
}

async function removeFrom(session) {
  const expr = `(() => {
    document.documentElement.classList.remove("lite-skin");
    const st = document.getElementById("codex-lite-skin-style");
    if (st) st.remove();
    return true;
  })()`;
  const r = await session.send("Runtime.evaluate", { expression: expr, returnByValue: true });
  return !(r.result?.exceptionDetails || r.error);
}

if (removeMode) {
  const targets = await listTargets();
  const main = targets?.find(isMain);
  if (!main) {
    console.log("no renderer; nothing to remove");
    process.exit(0);
  }
  const session = await connect(main);
  await removeFrom(session);
  session.ws.close();
  console.log("skin removed");
  process.exit(0);
}

if (!watchMode) {
  const targets = await listTargets();
  const main = targets?.find(isMain);
  if (!main) {
    console.error("Codex renderer not reachable on port " + port);
    process.exit(1);
  }
  const session = await connect(main);
  const ok = await applyTo(session);
  session.ws.close();
  console.log(ok ? "injected" : "inject failed");
  process.exit(ok ? 0 : 2);
}

// Watch mode: keep the skin applied, re-inject after reloads/restarts.
loadAssets();
loadSkins();
const sessions = new Map();
console.log(`[lite-skin] watching port ${port}`);
if (servePort) {
  http
    .createServer((req, res) => {
      res.setHeader("Access-Control-Allow-Origin", "*");
      res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
      res.setHeader("Access-Control-Allow-Headers", "Content-Type");
      if (req.method === "OPTIONS") {
        res.writeHead(204);
        res.end();
        return;
      }
      if (req.method === "POST" && req.url === "/switch") {
        let body = "";
        req.on("data", (c) => (body += c));
        req.on("end", () => {
          try {
            const { skin } = JSON.parse(body);
            execFileSync(
              process.env.PYTHON || "python",
              [path.join(__dirname, "switch_skin.py"), "--skin", skin],
              { encoding: "utf8", stdio: "pipe" },
            );
            loadAssets();
            loadSkins();
            Promise.all([...sessions.values()].map((s) => applyTo(s).catch(() => {})));
            res.writeHead(200, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ ok: true, skin }));
          } catch (e) {
            res.writeHead(500, { "Content-Type": "application/json" });
            res.end(JSON.stringify({ ok: false, error: String(e.message || e).slice(0, 200) }));
          }
        });
        return;
      }
      res.writeHead(404);
      res.end();
    })
    .listen(servePort, "127.0.0.1");
  console.log(`[lite-skin] skin switcher server on port ${servePort}`);
}
while (true) {
  const targets = await listTargets();
  const mainTargets = targets?.filter(isMain) ?? [];
  const activeIds = new Set(mainTargets.map((t) => t.id));
  for (const [id, session] of sessions) {
    if (!activeIds.has(id)) {
      session.ws.close();
      sessions.delete(id);
    }
  }
  for (const target of mainTargets) {
    if (sessions.has(target.id)) continue;
    try {
      const session = await connect(target);
      session.ws.addEventListener("message", (e) => {
        const msg = JSON.parse(String(e.data));
        if (msg.method === "Page.loadEventFired") {
          setTimeout(() => applyTo(session).catch(() => {}), 300);
        }
      });
      await applyTo(session);
      sessions.set(target.id, session);
      console.log(`[lite-skin] injected ${target.id}`);
    } catch (error) {
      console.error(`[lite-skin] inject failed: ${error.message}`);
    }
  }
  // Pick up skin-switch requests posted by the sidebar widget (DOM flag,
  // because app:// CSP blocks renderer fetch to loopback HTTP).
  for (const [, session] of sessions) {
    try {
      // Re-add the widget if React re-rendered the sidebar and dropped it
      // (appearance switches rebuild the aside without a page reload).
      const exists = await session.send("Runtime.evaluate", {
        expression: "!!document.getElementById('codex-skin-switcher')",
        returnByValue: true,
      });
      if (!(exists.result?.result?.value ?? false) && servePort) {
        await session.send("Runtime.evaluate", {
          expression: widgetScript(),
          returnByValue: true,
        });
      }
      const r = await session.send("Runtime.evaluate", {
        expression: "window.__codexSkinPending || null",
        returnByValue: true,
      });
      const pending = r.result?.result?.value;
      if (pending) {
        await session.send("Runtime.evaluate", {
          expression: "window.__codexSkinPending = null",
          returnByValue: true,
        });
        console.log(`[lite-skin] switch to ${pending}`);
        try {
          execFileSync(
            process.env.PYTHON || "python",
            [path.join(__dirname, "switch_skin.py"), "--skin", pending],
            { encoding: "utf8", stdio: "pipe" },
          );
          loadAssets();
          loadSkins();
          for (const s of sessions.values()) {
            await applyTo(s).catch(() => {});
          }
        } catch (e) {
          console.error(`[lite-skin] switch failed: ${e.message}`);
        }
      }
      const rd = await session.send("Runtime.evaluate", {
        expression: "window.__codexSkinPendingDelete || null",
        returnByValue: true,
      });
      const pendingDel = rd.result?.result?.value;
      if (pendingDel) {
        await session.send("Runtime.evaluate", {
          expression: "window.__codexSkinPendingDelete = null",
          returnByValue: true,
        });
        console.log(`[lite-skin] delete skin ${pendingDel}`);
        try {
          execFileSync(
            process.env.PYTHON || "python",
            [path.join(__dirname, "switch_skin.py"), "--delete", pendingDel],
            { encoding: "utf8", stdio: "pipe" },
          );
        } catch (e) {
          console.error(`[lite-skin] delete failed: ${e.message}`);
        }
        loadAssets();
        loadSkins();
        for (const s of sessions.values()) {
          await applyTo(s).catch(() => {});
        }
      }
    } catch {}
  }
  await new Promise((r) => setTimeout(r, 2000));
}
