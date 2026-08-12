import path from "node:path";
import { fileURLToPath } from "node:url";

setTimeout(() => process.exit(1), 12000);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const port = Number(process.argv[process.argv.indexOf("--port") + 1] ?? 9335);
const shotIdx = process.argv.indexOf("--shot");
const shotPath = shotIdx > -1 ? process.argv[shotIdx + 1] : path.join(__dirname, "check-shot.png");
let targets = null;
for (const host of ["127.0.0.1", "[::1]"]) {
  try {
    targets = await (await fetch(`http://${host}:${port}/json/list`)).json();
    break;
  } catch {}
}
const main = targets?.find((t) => t.type === "page" && t.url.startsWith("app://-/index.html") && !t.url.includes("initialRoute"));
if (!main) {
  console.error("main renderer not found");
  process.exit(1);
}
const ws = new WebSocket(main.webSocketDebuggerUrl);
await new Promise((r) => ws.addEventListener("open", r, { once: true }));
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
const expr = `(() => {
  const cs = (el, pseudo) => el ? getComputedStyle(el, pseudo) : null;
  const aside = document.querySelector("aside.app-shell-left-panel");
  const top = document.querySelector("div[class*='ApplicationMenuTopBar']");
  const mainEl = document.querySelector("main[class*='MainContentSurface']");
  const st = document.getElementById("codex-lite-skin-style");
  return {
    liteSkinClass: document.documentElement.classList.contains("lite-skin"),
    styleLen: st ? st.textContent.length : 0,
    asideBg: aside ? cs(aside).backgroundImage.slice(0, 80) : null,
    topBg: top ? cs(top).backgroundImage.slice(0, 80) : null,
    mainBg: mainEl ? cs(mainEl).backgroundImage.slice(0, 120) : null,
  };
})()`;
const r = await send("Runtime.evaluate", { expression: expr, returnByValue: true });
console.log(JSON.stringify(r.result?.result?.value ?? r.result, null, 2));
const shot = await send("Page.captureScreenshot", { format: "png" });
if (shot.result?.data) {
  const { writeFileSync } = await import("node:fs");
  writeFileSync(shotPath, Buffer.from(shot.result.data, "base64"));
  console.log("screenshot saved: " + shotPath);
}
ws.close();
setTimeout(() => process.exit(0), 300);
