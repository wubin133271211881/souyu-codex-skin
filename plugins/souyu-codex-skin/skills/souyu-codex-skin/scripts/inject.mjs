// Codex Lite Skin injector - injects a minimal background style into the
// running Codex desktop app over CDP. Keeps the default app layout.
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.argv[process.argv.indexOf("--port") + 1] ?? 9335);
const watchMode = process.argv.includes("--watch");
const removeMode = process.argv.includes("--remove");

const artB64 = readFileSync(path.join(__dirname, "art.jpg")).toString("base64");
let artDarkB64 = artB64;
try {
  artDarkB64 = readFileSync(path.join(__dirname, "art-dark.jpg")).toString("base64");
} catch {}
const css = readFileSync(path.join(__dirname, "style.css"), "utf8")
  .split("__ART_DARK__")
  .join(`data:image/jpeg;base64,${artDarkB64}`)
  .split("__ART__")
  .join(`data:image/jpeg;base64,${artB64}`);

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
  const r = await session.send("Runtime.evaluate", { expression: styleExpr, returnByValue: true });
  return !(r.result?.exceptionDetails || r.error);
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
const sessions = new Map();
console.log(`[lite-skin] watching port ${port}`);
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
  await new Promise((r) => setTimeout(r, 2000));
}
