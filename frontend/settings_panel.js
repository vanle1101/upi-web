// settings_panel.js â€” Tab "Settings" vá»›i sidebar dá»c.
// Section Ä‘áº§u: cáº¥u hÃ¬nh proxy pool (repeater nhiá»u proxy URL Ä‘á»ƒ xoay vÃ²ng).
//
// Nguá»“n dá»¯ liá»‡u: backend Settings Store qua /api/proxy/pool (GET/POST) +
// /api/proxy/test-all. KHÃ”NG dÃ¹ng localStorage cho config (theo project rules).
(function () {
  "use strict";

  // â”€â”€ Auth helper (reuse pattern app.js/hme.js) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function api(path, opts) {
    opts = opts || {};
    var token =
      (window.GptUi && window.GptUi.getAuthToken && window.GptUi.getAuthToken()) || "";
    var headers = Object.assign(
      { "Content-Type": "application/json" },
      token ? { "X-API-Token": token } : {},
      opts.headers || {}
    );
    return fetch(path, Object.assign({}, opts, { headers: headers })).then(function (r) {
      if (!r.ok) {
        return r.text().then(function (t) {
          throw new Error("HTTP " + r.status + ": " + t);
        });
      }
      return r.json();
    });
  }

  var $ = function (id) { return document.getElementById(id); };

  function escHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // Mask credential khi hiá»ƒn thá»‹ tráº¡ng thÃ¡i (user:pass@host â†’ ***@host)
  function maskProxy(url) {
    if (!url) return "direct";
    var m = String(url).match(/^([a-z][a-z0-9+.-]*):\/\/([^@/]+)@(.+)$/i);
    return m ? m[1] + "://***@" + m[3] : url;
  }

  // â”€â”€ State â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  var state = {
    rows: [],          // [{id, value}] â€” danh sÃ¡ch proxy Ä‘ang edit
    mode: "round_robin",
    lastResults: null, // map proxy â†’ {ok, public_ip, detail}
    loaded: false,
    busy: false,
  };
  var _rowSeq = 0;

  var dom = {};

  function cacheDom() {
    dom.section = $("settings-section-proxies");
    dom.rowsHost = $("proxy-pool-rows");
    dom.modeSelect = $("proxy-pool-mode");
    dom.summary = $("proxy-pool-summary");
    dom.btnAdd = $("proxy-pool-add");
    dom.btnPaste = $("proxy-pool-paste");
    dom.btnTestAll = $("proxy-pool-test-all");
    dom.btnClearDead = $("proxy-pool-clear-dead");
    dom.btnSave = $("proxy-pool-save");
    dom.statusLine = $("proxy-pool-status");
    // Paste modal
    dom.pasteModal = $("proxy-paste-modal");
    dom.pasteTextarea = $("proxy-paste-textarea");
    dom.pasteClose = $("proxy-paste-close");
    dom.pasteCancel = $("proxy-paste-cancel");
    dom.pasteApply = $("proxy-paste-apply");
    // Sidebar
    dom.navItems = Array.prototype.slice.call(
      document.querySelectorAll("#tab-settings .settings-nav-item")
    );
    dom.panes = Array.prototype.slice.call(
      document.querySelectorAll("#tab-settings [data-settings-pane]")
    );
    // Telegram section
    dom.tgBotToken = $("telegram-bot-token");
    dom.tgChatId = $("telegram-chat-id");
    dom.tgSave = $("telegram-save");
    dom.tgTest = $("telegram-test");
    dom.tgStatus = $("telegram-status");
    dom.tgBadge = $("telegram-status-badge");
  }

  // â”€â”€ Sidebar section switching â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function activateSection(sectionId) {
    dom.navItems.forEach(function (btn) {
      var on = btn.dataset.settingsSection === sectionId;
      btn.classList.toggle("active", on);
      btn.setAttribute("aria-selected", on ? "true" : "false");
    });
    dom.panes.forEach(function (pane) {
      pane.classList.toggle("active", pane.dataset.settingsPane === sectionId);
    });
  }

  // â”€â”€ Row rendering â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function makeRow(value) {
    return { id: "pp-" + _rowSeq++, value: value || "" };
  }

  function renderRows() {
    if (state.rows.length === 0) {
      dom.rowsHost.innerHTML =
        '<div class="proxy-pool-empty muted">Chưa có proxy nào. Bấm "Thêm proxy" hoặc "Dán hàng loạt".</div>';
      updateSummary();
      return;
    }
    var html = state.rows
      .map(function (row, idx) {
        var res = state.lastResults ? state.lastResults[row.value.trim()] : null;
        var dotCls = "proxy-dot";
        var statusTxt = "";
        var inputCls = "proxy-pool-input";
        if (res) {
          if (res.ok) {
            dotCls = "proxy-dot proxy-dot-ok";
            statusTxt = res.public_ip && res.public_ip !== "auto" ? "IP " + escHtml(res.public_ip) : "live";
          } else {
            dotCls = "proxy-dot proxy-dot-fail";
            statusTxt = "dead";
            inputCls = "proxy-pool-input proxy-dead";
          }
        }
        return (
          '<div class="proxy-pool-row" data-row-id="' + row.id + '">' +
            '<span class="proxy-pool-index">' + (idx + 1) + "</span>" +
            '<span class="' + dotCls + '" title="' + escHtml(statusTxt || "chÆ°a test") + '"></span>' +
            '<input type="text" class="' + inputCls + '" data-row-id="' + row.id + '"' +
              ' value="' + escHtml(row.value) + '"' +
              ' placeholder="http://user:pass@host:port" spellcheck="false" autocomplete="off" />' +
            '<span class="proxy-pool-row-status">' + escHtml(statusTxt) + "</span>" +
            '<button class="icon-btn icon-danger proxy-pool-remove" data-row-id="' + row.id +
              '" type="button" title="Xóa" aria-label="Xóa proxy">' +
              (window.GptUi ? window.GptUi.icon("remove") : "×") +
            "</button>" +
          "</div>"
        );
      })
      .join("");
    dom.rowsHost.innerHTML = html;
    updateSummary();
  }

  function updateSummary() {
    var total = state.rows.filter(function (r) { return r.value.trim(); }).length;
    var live = 0;
    var dead = 0;
    if (state.lastResults) {
      state.rows.forEach(function (r) {
        var res = state.lastResults[r.value.trim()];
        if (res) { res.ok ? live++ : dead++; }
      });
    }
    var txt = total + " proxy";
    if (state.lastResults) txt += " · " + live + " live · " + dead + " dead";
    dom.summary.textContent = txt;
    dom.summary.className = "badge " + (dead > 0 ? "badge-warn" : (live > 0 ? "badge-success" : "badge-muted"));

    if (dom.btnClearDead) {
      dom.btnClearDead.style.display = dead > 0 ? "inline-block" : "none";
    }

    if (window.GptUi && window.GptUi.updateRealtimeChart) {
      window.GptUi.updateRealtimeChart("settings-realtime-chart", total, {
        color: dead > 0 ? "var(--ops-red)" : "var(--ops-green)",
        displayValue: String(total),
        label: "Settings proxy rows",
      });
    }
    var liveEl = $("settings-chart-live");
    var deadEl = $("settings-chart-dead");
    if (liveEl) liveEl.textContent = String(live);
    if (deadEl) deadEl.textContent = String(dead);
  }

  // Sync giÃ¡ trá»‹ tá»« input DOM vá» state (trÆ°á»›c khi save/test)
  function syncRowsFromDom() {
    var inputs = dom.rowsHost.querySelectorAll(".proxy-pool-input");
    Array.prototype.forEach.call(inputs, function (inp) {
      var row = state.rows.find(function (r) { return r.id === inp.dataset.rowId; });
      if (row) row.value = inp.value;
    });
  }

  function collectProxies() {
    syncRowsFromDom();
    var seen = {};
    var out = [];
    state.rows.forEach(function (r) {
      var v = r.value.trim();
      if (v && !seen[v]) { seen[v] = 1; out.push(v); }
    });
    return out;
  }

  function setStatus(text, kind) {
    dom.statusLine.textContent = text || "";
    dom.statusLine.className = "proxy-pool-status muted" + (kind ? " proxy-pool-status-" + kind : "");
  }

  // â”€â”€ Load from backend â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function load() {
    return api("/api/proxy/pool")
      .then(function (data) {
        state.mode = data.rotation_mode || "round_robin";
        dom.modeSelect.value = state.mode;
        var proxies = data.proxies || [];
        state.rows = proxies.map(function (p) { return makeRow(p); });
        if (state.rows.length === 0) state.rows.push(makeRow(""));
        state.loaded = true;

        var rt = data.runtime || {};
        var deadSet = {};
        (rt.dead || []).forEach(function(d) { deadSet[d] = true; });
        var map = {};
        proxies.forEach(function(p) {
          if (deadSet[p]) map[p] = { ok: false };
          else map[p] = { ok: true, public_ip: "auto" };
        });
        state.lastResults = map;

        renderRows();
        if (rt.total) {
          setStatus("Đã lưu " + rt.total + " proxy · " + (rt.live || 0) + " live.", null);
        }
      })
      .catch(function (err) {
        setStatus("Load cấu hình thất bại: " + err.message, "fail");
      });
  }

  // Setup auto-polling for proxy status
  setInterval(function() {
    if (!dom.section || dom.section.getAttribute("aria-hidden") === "true") return;
    if (!state.busy && document.getElementById("tab-settings").classList.contains("active")) {
      api("/api/proxy/pool").then(function(data) {
        var rt = data.runtime || {};
        var deadSet = {};
        (rt.dead || []).forEach(function(d) { deadSet[d] = true; });
        var map = state.lastResults || {};
        state.rows.forEach(function(r) {
          var p = r.value.trim();
          if (!p) return;
          if (deadSet[p]) {
            map[p] = { ok: false };
          } else if (map[p] && !map[p].ok) {
            delete map[p];
          }
        });
        state.lastResults = map;
        renderRows();
        if (rt.total) {
          setStatus("Đã lưu " + rt.total + " proxy · " + (rt.live || 0) + " live.", null);
        }
      }).catch(function(){});
    }
  }, 5000);

  // â”€â”€ Save â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function save() {
    if (state.busy) return;
    var proxies = collectProxies();
    state.busy = true;
    dom.btnSave.disabled = true;
    setStatus("Đang lưu...", null);
    api("/api/proxy/pool", {
      method: "POST",
      body: JSON.stringify({ proxies: proxies, rotation_mode: dom.modeSelect.value }),
    })
      .then(function (data) {
        state.mode = data.rotation_mode;
        // Normalize láº¡i danh sÃ¡ch theo backend (Ä‘Ã£ dedupe)
        state.rows = (data.proxies || []).map(function (p) { return makeRow(p); });
        if (state.rows.length === 0) state.rows.push(makeRow(""));
        state.lastResults = null;
        renderRows();
        var extra = data.settings_persist_error ? " (cảnh báo: " + data.settings_persist_error + ")" : "";
        setStatus("Đã lưu " + proxies.length + " proxy." + extra, data.settings_persist_error ? "fail" : "ok");
      })
      .catch(function (err) {
        setStatus("Lưu thất bại: " + err.message, "fail");
      })
      .finally(function () {
        state.busy = false;
        dom.btnSave.disabled = false;
      });
  }

  // â”€â”€ Clear Dead â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function clearDeadProxies() {
    if (!state.lastResults || state.busy) return;
    var liveProxies = [];
    state.rows.forEach(function (r) {
      var p = r.value.trim();
      if (!p) return;
      var res = state.lastResults[p];
      if (!res || res.ok) {
        liveProxies.push(p);
      }
    });

    // Náº¿u khÃ´ng cÃ²n proxy nÃ o, thÃªm 1 dÃ²ng trá»‘ng
    state.rows = liveProxies.map(function (p) { return makeRow(p); });
    if (state.rows.length === 0) state.rows.push(makeRow(""));

    // áº¨n nÃºt sau khi dá»n xong
    if (dom.btnClearDead) dom.btnClearDead.style.display = "none";

    renderRows();
    save(); // Tá»± Ä‘á»™ng lÆ°u
  }

  // â”€â”€ Test All â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function testAll() {
    if (state.busy) return;
    var proxies = collectProxies();
    if (proxies.length === 0) {
      setStatus("Không có proxy để test.", "fail");
      return;
    }
    state.busy = true;
    dom.btnTestAll.disabled = true;
    setStatus("Đang test " + proxies.length + " proxy...", null);

    state.lastResults = {};
    renderRows(); // Clear previous states

    var liveCount = 0;
    var deadCount = 0;

    var token = (window.GptUi && window.GptUi.getAuthToken && window.GptUi.getAuthToken()) || "";
    fetch("/api/proxy/test-stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(token ? { "X-API-Token": token } : {})
      },
      body: JSON.stringify({ proxies: proxies }),
    })
      .then(async function (res) {
        if (!res.ok) throw new Error("HTTP error " + res.status);
        var reader = res.body.getReader();
        var decoder = new TextDecoder("utf-8");
        var buffer = "";
        while (true) {
          var chunk = await reader.read();
          if (chunk.done) break;
          buffer += decoder.decode(chunk.value, { stream: true });
          var lines = buffer.split("\n");
          buffer = lines.pop(); // keep incomplete line
          for (var i = 0; i < lines.length; i++) {
            var line = lines[i].trim();
            if (line) {
              var item = JSON.parse(line);
              state.lastResults[item.proxy] = item;
              if (item.ok) liveCount++; else deadCount++;
              setStatus("Đang test... Live: " + liveCount + " / Dead: " + deadCount + " / Tổng: " + proxies.length, null);
              renderRows();
            }
          }
        }
        setStatus(
          "Test xong: " + liveCount + " live / " + deadCount + " dead / " + proxies.length + " tổng.",
          deadCount > 0 ? "fail" : "ok"
        );
      })
      .catch(function (err) {
        setStatus("Test thất bại: " + err.message, "fail");
      })
      .finally(function () {
        state.busy = false;
        dom.btnTestAll.disabled = false;
      });
  }

  // â”€â”€ Telegram section â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  var tgState = { loaded: false, busy: false };

  function setTgStatus(text, kind) {
    if (!dom.tgStatus) return;
    dom.tgStatus.textContent = text || "";
    dom.tgStatus.className = "proxy-pool-status muted" + (kind ? " proxy-pool-status-" + kind : "");
  }

  function setTgBadge(configured) {
    if (!dom.tgBadge) return;
    dom.tgBadge.textContent = configured ? "đã cấu hình" : "chưa cấu hình";
    dom.tgBadge.className = "badge " + (configured ? "badge-success" : "badge-muted");
  }

  function loadTelegram() {
    if (!dom.tgBotToken) return Promise.resolve();
    return api("/api/telegram/config")
      .then(function (data) {
        dom.tgBotToken.value = data.bot_token || "";
        dom.tgChatId.value = data.chat_id || "";
        setTgBadge(!!data.configured);
        tgState.loaded = true;
      })
      .catch(function (err) {
        setTgStatus("Load thất bại: " + err.message, "fail");
      });
  }

  function saveTelegram() {
    if (tgState.busy) return;
    tgState.busy = true;
    dom.tgSave.disabled = true;
    setTgStatus("Đang lưu...", null);
    api("/api/telegram/config", {
      method: "POST",
      body: JSON.stringify({
        bot_token: dom.tgBotToken.value.trim(),
        chat_id: dom.tgChatId.value.trim(),
      }),
    })
      .then(function (data) {
        setTgBadge(!!data.configured);
        var extra = data.persist_error ? " (cảnh báo: " + data.persist_error + ")" : "";
        setTgStatus("Đã lưu." + extra, data.persist_error ? "fail" : "ok");
      })
      .catch(function (err) {
        setTgStatus("Lưu thất bại: " + err.message, "fail");
      })
      .finally(function () {
        tgState.busy = false;
        dom.tgSave.disabled = false;
      });
  }

  function testTelegram() {
    if (tgState.busy) return;
    tgState.busy = true;
    dom.tgTest.disabled = true;
    setTgStatus("Đang gửi test...", null);
    // LÆ°u trÆ°á»›c rá»“i test Ä‘á»ƒ dÃ¹ng giÃ¡ trá»‹ má»›i nháº¥t.
    api("/api/telegram/config", {
      method: "POST",
      body: JSON.stringify({
        bot_token: dom.tgBotToken.value.trim(),
        chat_id: dom.tgChatId.value.trim(),
      }),
    })
      .then(function () { return api("/api/telegram/test", { method: "POST" }); })
      .then(function () { setTgStatus("Đã gửi tin test - kiểm tra Telegram.", "ok"); })
      .catch(function (err) { setTgStatus("Test thất bại: " + err.message, "fail"); })
      .finally(function () {
        tgState.busy = false;
        dom.tgTest.disabled = false;
      });
  }

  // â”€â”€ Paste modal â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function openPaste() {
    dom.pasteTextarea.value = "";
    dom.pasteModal.style.display = "flex";
    dom.pasteTextarea.focus();
  }
  function closePaste() {
    dom.pasteModal.style.display = "none";
  }
  function applyPaste() {
    var lines = dom.pasteTextarea.value.split("\n");
    syncRowsFromDom();
    var existing = {};
    state.rows.forEach(function (r) {
      var v = r.value.trim();
      if (v) existing[v] = 1;
    });
    // Bá» row rá»—ng cuá»‘i náº¿u Ä‘ang trá»‘ng
    state.rows = state.rows.filter(function (r) { return r.value.trim(); });
    var added = 0;
    lines.forEach(function (line) {
      var v = line.trim();
      if (v && !existing[v]) {
        existing[v] = 1;
        state.rows.push(makeRow(v));
        added++;
      }
    });
    if (state.rows.length === 0) state.rows.push(makeRow(""));
    state.lastResults = null;
    renderRows();
    closePaste();
    setStatus("Đã thêm " + added + " proxy. Nhớ bấm Lưu.", null);
  }

  // â”€â”€ Event wiring â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function bindEvents() {
    dom.navItems.forEach(function (btn) {
      btn.addEventListener("click", function () {
        activateSection(btn.dataset.settingsSection);
      });
    });

    dom.btnAdd.addEventListener("click", function () {
      syncRowsFromDom();
      state.rows.push(makeRow(""));
      renderRows();
      // Focus input vá»«a thÃªm
      var inputs = dom.rowsHost.querySelectorAll(".proxy-pool-input");
      if (inputs.length) inputs[inputs.length - 1].focus();
    });

    dom.btnPaste.addEventListener("click", openPaste);
    dom.btnTestAll.addEventListener("click", testAll);
    if (dom.btnClearDead) dom.btnClearDead.addEventListener("click", clearDeadProxies);
    dom.btnSave.addEventListener("click", save);

    if (dom.tgSave) dom.tgSave.addEventListener("click", saveTelegram);
    if (dom.tgTest) dom.tgTest.addEventListener("click", testTelegram);

    dom.modeSelect.addEventListener("change", function () {
      state.mode = dom.modeSelect.value;
    });

    // Delegation: remove row + input edit invalidate test result
    dom.rowsHost.addEventListener("click", function (e) {
      var btn = e.target.closest(".proxy-pool-remove");
      if (!btn) return;
      syncRowsFromDom();
      state.rows = state.rows.filter(function (r) { return r.id !== btn.dataset.rowId; });
      if (state.rows.length === 0) state.rows.push(makeRow(""));
      renderRows();
    });

    dom.rowsHost.addEventListener("input", function (e) {
      var inp = e.target.closest(".proxy-pool-input");
      if (!inp) return;
      var row = state.rows.find(function (r) { return r.id === inp.dataset.rowId; });
      if (row) row.value = inp.value;
    });

    // Paste modal
    dom.pasteClose.addEventListener("click", closePaste);
    dom.pasteCancel.addEventListener("click", closePaste);
    dom.pasteApply.addEventListener("click", applyPaste);
    dom.pasteModal.addEventListener("click", function (e) {
      if (e.target === dom.pasteModal) closePaste();
    });
  }

  // â”€â”€ Lazy-load khi má»Ÿ tab Settings láº§n Ä‘áº§u â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
  function init() {
    cacheDom();
    if (!dom.section) return; // tab khÃ´ng tá»“n táº¡i
    bindEvents();
    activateSection("telegram");

    document.addEventListener("gpt:tab", function (e) {
      if (e.detail && e.detail.tab === "settings" && !tgState.loaded) {
        loadTelegram();
      }
    });

    // Náº¿u tab settings Ä‘Ã£ active sáºµn lÃºc reload (ui.active_tab persisted)
    if (document.getElementById("tab-settings").classList.contains("active")) {
      loadTelegram();
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
