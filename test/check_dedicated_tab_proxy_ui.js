"use strict";

const fs = require("fs");
const path = require("path");
const vm = require("vm");

const root = path.resolve(__dirname, "..");
const read = (relative) => fs.readFileSync(path.join(root, relative), "utf8");

const index = read("web/static/index.html");
const app = read("web/static/app.js");
const upi = read("web/static/upi.js");
const settings = read("web/static/settings_panel.js");
const css = read("web/static/workspace.css") + "\n" + read("web/static/operations.css");

for (const [name, source] of [["app.js", app], ["upi.js", upi], ["settings_panel.js", settings]]) {
  new vm.Script(source, { filename: name });
}

const count = (source, token) => source.split(token).length - 1;
if (count(index, 'id="reg-proxy-input"') !== 1) throw new Error("Reg proxy input missing or duplicated");
if (count(index, 'id="upi-proxy-input"') !== 1) throw new Error("UPI proxy input missing or duplicated");
if (!index.includes('<textarea id="reg-proxy-input"')) throw new Error("Reg proxy must be a multiline textarea");
if (!index.includes('<textarea id="upi-proxy-input"')) throw new Error("UPI proxy must be a multiline textarea");
if (count(index, 'id="proxy-toggle"') !== 1) throw new Error("Reg proxy toggle missing or duplicated");
if (count(index, 'id="upi-proxy-toggle"') !== 1) throw new Error("UPI proxy toggle missing or duplicated");
if (!index.includes('id="settings-section-proxies"') || !index.includes('data-settings-pane="proxies" style="display:none"')) {
  throw new Error("Shared proxy settings are still visible");
}
if (!index.includes('id="settings-section-telegram"') || !index.includes('settings-section active" id="settings-section-telegram"')) {
  throw new Error("Telegram settings are not the active settings view");
}
if (!app.includes("Settings.save('reg.proxy'")) throw new Error("Reg proxy is not saved through Settings");
if (!app.includes("Settings.save('reg.use_proxy'")) throw new Error("Reg proxy toggle is not saved through Settings");
if (!upi.includes("Settings.save('upi.proxy'")) throw new Error("UPI proxy is not saved through Settings");
if (!upi.includes("Settings.save('upi.use_proxy'")) throw new Error("UPI proxy toggle is not saved through Settings");
if (!css.includes(".workflow-proxy-row")) throw new Error("Dedicated proxy field styling missing");
if (!css.includes(".workflow-proxy-toggle")) throw new Error("Dedicated proxy toggle styling missing");
if (!css.includes(".proxy-textarea")) throw new Error("Multiline proxy styling missing");

console.log("dedicated tab proxy UI: OK");
