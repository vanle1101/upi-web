/* gpt_signup_hybrid — frontend logic */
(() => {
  'use strict';

  // ── Auth ────────────────────────────────────────────────────────────
  const _LS_TOKEN = 'gpt_reg.auth_token';

  function getAuthToken() {
    // 1. Meta tag (injected server-side khi loopback bind)
    const meta = document.querySelector('meta[name="auth-token"]');
    const metaVal = (meta && meta.content) || '';
    if (metaVal && metaVal !== '__AUTH_TOKEN__') return metaVal;
    // 2. URL query param ?token=... (cho non-loopback access)
    const params = new URLSearchParams(window.location.search);
    const urlToken = params.get('token') || '';
    if (urlToken) {
      localStorage.setItem(_LS_TOKEN, urlToken);
      return urlToken;
    }
    // 3. localStorage (previously entered)
    let stored = localStorage.getItem(_LS_TOKEN) || '';
    if (!stored && window.location.hostname !== '127.0.0.1' && window.location.hostname !== 'localhost') {
       stored = prompt('Vercel Static UI: Please enter the API Auth Token (see backend startup logs):');
       if (stored) {
         stored = stored.trim();
         localStorage.setItem(_LS_TOKEN, stored);
       }
    }
    return stored || '';
  }
  function withTokenQuery(url) {
    const t = getAuthToken();
    if (!t) return url;
    const sep = url.includes('?') ? '&' : '?';
    return url + sep + 'token=' + encodeURIComponent(t);
  }

  // ── SseBus — unified SSE multiplexer (frontend) ─────────────────
  const SseBus = (() => {
    let _es = null;
    let _reconnectTimer = null;
    const _handlers = new Map(); // channel -> [callback, ...]

    function connect() {
      if (_es && _es.readyState !== 2) return;
      _disconnect();
      const url = withTokenQuery('/api/sse');
      _es = new EventSource(url);

      _es.onmessage = (e) => {
        let data;
        try { data = JSON.parse(e.data); } catch (_) { return; }
        const channel = data.channel;
        if (!channel) return;
        const cbs = _handlers.get(channel);
        if (cbs) cbs.forEach(cb => cb(data));
      };

      _es.onerror = () => {
        _disconnect();
        _reconnectTimer = setTimeout(connect, 3000);
      };
    }

    function on(channel, callback) {
      if (!_handlers.has(channel)) _handlers.set(channel, []);
      _handlers.get(channel).push(callback);
    }

    function _disconnect() {
      if (_reconnectTimer) { clearTimeout(_reconnectTimer); _reconnectTimer = null; }
      if (_es) { try { _es.close(); } catch (_) {} _es = null; }
    }

    return { connect, on };
  })();
  window.SseBus = SseBus;

  // ── LocalStorage keys ─────────────────────────────────────────────
  // NOTE: Chỉ textarea drafts giữ ở localStorage (ngoài scope unified-settings-store).
  // Tất cả runtime config đã migrate sang Settings store (DB-backed).
  const LS_INPUT_REG = 'gpt_reg.input.reg';

  // Helper: persist textarea content vào localStorage. Lưu cả khi rỗng để
  // phân biệt "user đã xóa tay" vs "chưa từng nhập" — chỉ xóa key khi
  // user bấm Clear Input.
  function persistTextarea(key, value) {
    try { localStorage.setItem(key, value); } catch (e) { /* quota — bỏ qua */ }
  }
  function clearPersistedTextarea(key) {
    try { localStorage.removeItem(key); } catch (e) { /* ignore */ }
  }
  // Expose để các tab khác (session.js, link.js) dùng chung pattern
  window.GptUi = Object.assign(window.GptUi || {}, {
    persistTextarea,
    clearPersistedTextarea,
  });

  // ── Error alert sound (Web Audio API — works in background tabs) ──
  let _audioCtx = null;
  function _getAudioCtx() {
    if (!_audioCtx) _audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    if (_audioCtx.state === 'suspended') _audioCtx.resume();
    return _audioCtx;
  }
  function playErrorAlert() {
    try {
      const ctx = _getAudioCtx();
      const now = ctx.currentTime;
      // 3 beeps: 880Hz, loud, short — unmissable
      for (let i = 0; i < 3; i++) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'square';
        osc.frequency.value = 880;
        gain.gain.value = 0.5;
        const t = now + i * 0.25;
        osc.start(t);
        osc.stop(t + 0.15);
      }
    } catch (e) { /* AudioContext not available */ }
  }
  function playSuccessAlert() {
    try {
      const ctx = _getAudioCtx();
      const now = ctx.currentTime;
      // Tiếng "ting" dịu: 2 nốt đi lên (C6 -> E6) sine, ngắn + nhẹ.
      const notes = [
        { freq: 1046.5, t: 0.0 },
        { freq: 1318.5, t: 0.12 },
      ];
      for (const n of notes) {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.type = 'sine';
        osc.frequency.value = n.freq;
        const t = now + n.t;
        // envelope: attack nhanh roi decay muot -> nghe nhu chuong "ting"
        gain.gain.setValueAtTime(0.0001, t);
        gain.gain.exponentialRampToValueAtTime(0.35, t + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);
        osc.start(t);
        osc.stop(t + 0.5);
      }
    } catch (e) { /* AudioContext not available */ }
  }
  // Unlock AudioContext on first user interaction (required by browsers)
  function _unlockAudio() {
    try { _getAudioCtx(); } catch (e) { }
    document.removeEventListener('click', _unlockAudio);
    document.removeEventListener('keydown', _unlockAudio);
  }
  document.addEventListener('click', _unlockAudio);
  document.addEventListener('keydown', _unlockAudio);

  // Expose for session.js and link.js
  window.GptUi = Object.assign(window.GptUi || {}, { playErrorAlert, playSuccessAlert });

  // ── State ─────────────────────────────────────────────────────────
  const state = {
    jobs: new Map(),          // id → job dict
    order: [],                // job id order
    activeJobId: null,        // job đang xem log
    maxConcurrent: 3,
    mode: 'multi',
    headless: true,
    debug: false,
    useProxy: false,
    mailModes: [],            // [{id, label, input_placeholder, input_help, config_schema}]
    currentMailMode: 'outlook',
  };

  // ── DOM refs ──────────────────────────────────────────────────────
  const $ = (id) => document.getElementById(id);
  const dom = {
    comboInput: $('combo-input'),
    btnRun: $('btn-run'),
    btnStopAll: $('btn-stop-all'),
    btnClearInput: $('btn-clear-input'),
    comboCount: $('combo-count'),
    defaultPassword: $('default-password'),
    jobTimeout: $('job-timeout'),
    autoRetryMax: $('auto-retry-max'),
    jobList: $('job-list'),
    jobSummary: $('job-summary'),
    logPane: $('log-pane'),
    logTarget: $('log-target'),
    btnClearLog: $('btn-clear-log'),
    successPane: $('success-pane'),
    errorPane: $('error-pane'),
    btnCopySuccess: $('btn-copy-success'),
    btnCopyError: $('btn-copy-error'),
    statusPill: $('status-pill'),
    metricTotalJobs: $('metric-total-jobs'),
    metricTotalNote: $('metric-total-note'),
    metricSuccessRate: $('metric-success-rate'),
    metricSuccessNote: $('metric-success-note'),
    metricActiveRuns: $('metric-active-runs'),
    metricActiveNote: $('metric-active-note'),
    metricAvgTime: $('metric-avg-time'),
    metricAvgNote: $('metric-avg-note'),
    metricErrorRate: $('metric-error-rate'),
    metricErrorNote: $('metric-error-note'),
    insightJobsMin: $('insight-jobs-min'),
    insightSuccessRate: $('insight-success-rate'),
    insightErrorRate: $('insight-error-rate'),
    // modeSelect removed
    concurrencySelects: document.querySelectorAll('.concurrency-select'),
    headlessToggle: $('headless-toggle'),
    debugToggle: $('debug-toggle'),
    proxyToggle: $('proxy-toggle'),
    regProxyInput: $('reg-proxy-input'),
    inputHint: $('input-hint'),
    mailModeSelect: $('mail-mode-select'),
    regModeSelect: $('reg-mode-select'),
    mailModeConfigHost: $('mail-mode-config-host'),
    pipelineSteps: Array.from(
      document.querySelectorAll('#tab-reg .pipeline-strip .pipeline-step')
    ),
  };

  // ── Helpers ───────────────────────────────────────────────────────
  const icons = Object.freeze({
    stop: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="2"/></svg>',
    retry: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>',
    remove: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    copy: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
    download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
    link: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10 13a5 5 0 0 0 7.07 0l2.83-2.83a5 5 0 0 0-7.07-7.07L11 4"/><path d="M14 11a5 5 0 0 0-7.07 0L4.1 13.83a5 5 0 1 0 7.07 7.07L13 19"/></svg>',
    token: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 2l-2 2"/><path d="M7.61 13.39a5.5 5.5 0 1 0 7.78 7.78L21 15.5l-7.5-7.5-5.89 5.39Z"/><path d="m14.5 6.5 3 3"/></svg>',
    eye: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/></svg>',
    eyeOff: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m3 3 18 18"/><path d="M10.6 10.6A2 2 0 0 0 13.4 13.4"/><path d="M9.9 4.2A10.6 10.6 0 0 1 12 4c6.5 0 10 8 10 8a18.7 18.7 0 0 1-3.1 4.3"/><path d="M6.1 6.1C3.4 8 2 12 2 12s3.5 8 10 8a10.7 10.7 0 0 0 5.9-1.8"/></svg>',
    qr: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><line x1="14" y1="14" x2="14" y2="17"/><line x1="14" y1="20" x2="14" y2="21"/><line x1="17" y1="14" x2="21" y2="14"/><line x1="17" y1="17" x2="17" y2="21"/><line x1="20" y1="17" x2="21" y2="17"/><line x1="20" y1="20" x2="21" y2="20"/></svg>',
  });
  const mailModeUiCopy = Object.freeze({
    outlook: {
      input_help: 'One Outlook combo per line.',
      input_placeholder: 'email|password|refresh_token|client_id',
    },
    worker: {
      input_help: 'One iCloud email per line via Worker OTP.',
      input_placeholder: 'user@icloud.com',
    },
    gmail_advanced: {
      input_help: 'Mỗi dòng: api_url hoặc email|api_url. Pre-check mail_status=live.',
      input_placeholder: 'https://checkgmail.live/otp/...\nbrandonspencer7424@gmail.com|https://checkgmail.live/otp/...',
    },
  });

  function fmtDuration(secs) {
    if (secs == null) return '';
    if (secs < 60) return secs.toFixed(1) + 's';
    return Math.floor(secs / 60) + 'm' + Math.floor(secs % 60) + 's';
  }

  function fmtPercent(value) {
    if (!Number.isFinite(value)) return '0%';
    if (value === 0 || value === 100) return `${Math.round(value)}%`;
    return `${value.toFixed(1)}%`;
  }

  const realtimeCharts = new Map();

  function chartPath(points, width, height) {
    if (!points.length) return '';
    const min = Math.min(...points);
    const max = Math.max(...points);
    const span = Math.max(max - min, 1);
    const step = points.length > 1 ? width / (points.length - 1) : width;
    return points.map((value, idx) => {
      const x = idx * step;
      const y = height - ((value - min) / span) * (height - 10) - 5;
      return `${idx === 0 ? 'M' : 'L'}${x.toFixed(1)} ${y.toFixed(1)}`;
    }).join(' ');
  }

  function chartVisualPoints(chartId, points, opts = {}) {
    if (points.length < 2) return points;
    const min = Math.min(...points);
    const max = Math.max(...points);
    if (Math.abs(max - min) > 0.001 && points.length > 3) return points;

    const base = points[points.length - 1] || 0;
    const seed = Array.from(chartId).reduce((sum, char) => sum + char.charCodeAt(0), 0) % 17;
    const amplitude = opts.visualAmplitude || Math.max(1, Math.abs(base) * 0.075);
    return points.map((value, idx) => {
      const wave = Math.sin((idx + seed) * 1.17) + Math.cos((idx + seed) * 0.51) * 0.55;
      return value + wave * amplitude;
    });
  }

  function updateRealtimeChart(chartId, value, opts = {}) {
    const host = document.getElementById(chartId);
    if (!host) return;
    const numeric = Number.isFinite(Number(value)) ? Number(value) : 0;
    const points = realtimeCharts.get(chartId) || [];
    const maxPoints = opts.maxPoints || 36;
    if (!points.length && opts.seed !== false) {
      const seedCount = Math.min(maxPoints, 18);
      for (let i = 0; i < seedCount - 1; i += 1) points.push(numeric);
    }
    points.push(numeric);
    while (points.length > maxPoints) points.shift();
    realtimeCharts.set(chartId, points);

    const width = 260;
    const height = 72;
    const path = chartPath(chartVisualPoints(chartId, points, opts), width, height);
    const baseline = points.length
      ? `M0 ${height - 5} L${width} ${height - 5}`
      : '';
    const color = opts.color || 'var(--ops-green)';
    host.innerHTML = `
      <svg class="ops-chart-svg" viewBox="0 0 ${width} ${height}" preserveAspectRatio="none" role="img" aria-label="${escHtml(opts.label || 'Realtime chart')}">
        <path class="ops-chart-gridline" d="${baseline}"></path>
        <path class="ops-chart-fill" d="${path ? `${path} L${width} ${height} L0 ${height} Z` : ''}" style="--chart-color:${escHtml(color)}"></path>
        <path class="ops-chart-line" d="${path}" style="--chart-color:${escHtml(color)}"></path>
      </svg>
    `;
    const valueEl = document.getElementById(host.dataset.chartValueId || '');
    if (valueEl) valueEl.textContent = opts.displayValue != null ? String(opts.displayValue) : String(numeric.toFixed(1));
  }

  function computeJobStats(order, jobs) {
    const stats = { total: order.length, queued: 0, running: 0, success: 0, error: 0, cancelled: 0, finished: 0 };
    order.forEach((id) => {
      const j = jobs.get ? jobs.get(id) : jobs[id];
      if (!j) return;
      stats[j.status] = (stats[j.status] || 0) + 1;
    });
    stats.finished = (stats.success || 0) + (stats.error || 0) + (stats.cancelled || 0);
    stats.successRate = stats.finished ? ((stats.success || 0) / stats.finished) * 100 : 0;
    stats.errorRate = stats.finished ? ((stats.error || 0) / stats.finished) * 100 : 0;
    return stats;
  }

  function escHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    }[c]));
  }

  function api(path, opts = {}) {
    const token = getAuthToken();
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'X-API-Token': token } : {}),
      ...(opts.headers || {}),
    };
    return fetch(path, {
      ...opts,
      headers,
    }).then((r) => {
      if (!r.ok) return r.text().then((t) => { throw new Error(`HTTP ${r.status}: ${t}`); });
      return r.json();
    });
  }

  function icon(name) {
    return icons[name] || '';
  }

  function copyText(text) {
    // Fallback cho non-HTTPS / mobile browsers
    function fallbackCopy(str) {
      const ta = document.createElement('textarea');
      ta.value = str;
      ta.style.position = 'fixed';
      ta.style.left = '-9999px';
      ta.style.top = '-9999px';
      document.body.appendChild(ta);
      ta.focus();
      ta.select();
      let ok = false;
      try { ok = document.execCommand('copy'); } catch (_) { /* ignore */ }
      document.body.removeChild(ta);
      return ok;
    }

    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text).catch(() => {
        if (fallbackCopy(text)) return;
        return Dialog.alert({ message: 'Copy failed.' }).then(() => { throw new Error('copy failed'); });
      });
    }
    // Non-secure context: dùng fallback trực tiếp
    if (fallbackCopy(text)) return Promise.resolve();
    return Dialog.alert({ message: 'Copy failed.' }).then(() => { throw new Error('copy failed'); });
  }

  let _activeTabId = null;
  function activateTab(tabId) {
    const prevTab = _activeTabId;
    _activeTabId = tabId;
    document.querySelectorAll('.tab-btn').forEach((btn) => {
      btn.classList.toggle('active', btn.dataset.tab === tabId);
    });
    document.querySelectorAll('.tab-content').forEach((tab) => {
      tab.classList.toggle('active', tab.id === `tab-${tabId}`);
    });
    Settings.save('ui.active_tab', tabId, getAuthToken());
    document.dispatchEvent(new CustomEvent('gpt:tab', { detail: { tab: tabId, prev: prevTab } }));
  }

  function initTabs() {
    if (document.body.dataset.tabsBound === 'true') return;
    document.body.dataset.tabsBound = 'true';
    document.querySelectorAll('.tab-btn').forEach((btn) => {
      btn.addEventListener('click', () => activateTab(btn.dataset.tab));
    });
    // Tab tạm ẩn (chưa dùng được). Mở lại: bỏ khỏi danh sách + bỏ comment nút nav trong index.html.
    const hiddenTabs = ['link', 'hme'];
    let initialTab = Settings.get('ui.active_tab') || document.querySelector('.tab-btn.active')?.dataset.tab || 'reg';
    if (hiddenTabs.includes(initialTab)) initialTab = 'reg';
    activateTab(initialTab);
  }

  window.GptUi = Object.assign(window.GptUi || {}, {
    icon,
    copyText,
    activateTab,
    initTabs,
    getAuthToken,
    updateRealtimeChart,
    computeJobStats,
    fmtPercent,
    fmtDuration,
    modeToConcurrency: (mode) => {
      const map = { single: 1, multi: 2, multi3: 3, multi5: 5, multi10: 10, multi20: 20, multi30: 30, multi50: 50 };
      return map[mode] || 1;
    },
    concurrencyToMode: (c) => {
      if (c >= 50) return 'multi50';
      if (c >= 30) return 'multi30';
      if (c >= 20) return 'multi20';
      if (c >= 10) return 'multi10';
      if (c >= 5) return 'multi5';
      if (c >= 3) return 'multi3';
      if (c >= 2) return 'multi';
      return 'single';
    }
  });

  // ── Combo counter ─────────────────────────────────────────────────
  function updateComboCount() {
    const lines = dom.comboInput.value.split('\n').filter((l) => {
      const s = l.trim();
      return s && !s.startsWith('#');
    });
    dom.comboCount.textContent = `${lines.length} combo${lines.length === 1 ? '' : 's'}`;
  }

  dom.comboInput.addEventListener('input', () => {
    updateComboCount();
    persistTextarea(LS_INPUT_REG, dom.comboInput.value);
  });

  // ── Render job list ──────────────────────────────────────────────
  function renderJobs() {
    if (state.order.length === 0) {
      dom.jobList.innerHTML = '<div class="empty">No jobs yet. Paste combos and click Run.</div>';
      dom.jobSummary.textContent = '0 total';
      updateLiveMetrics({ queued: 0, running: 0, success: 0, error: 0, cancelled: 0 });
      updatePipeline(null);
      return;
    }

    const stats = { queued: 0, running: 0, success: 0, error: 0, cancelled: 0 };
    const html = state.order.map((id, idx) => {
      const j = state.jobs.get(id);
      if (!j) return '';
      stats[j.status] = (stats[j.status] || 0) + 1;
      const cls = state.activeJobId === id ? 'job is-active' : 'job';
      const actionBtn = j.status === 'running'
        ? `<button class="icon-btn icon-danger" data-action="stop" data-id="${escHtml(id)}" title="Stop">${icon('stop')}</button>`
        : `<button class="icon-btn" data-action="retry" data-id="${escHtml(id)}" title="Retry">${icon('retry')}</button>`;
      const progress = j.status === 'success' || j.status === 'error' || j.status === 'cancelled'
        ? 100
        : (j.status === 'running' ? 62 : 0);
      const progressLabel = `${progress}%`;
      const source = (j.mail_mode || 'outlook').toUpperCase();
      return `
        <div class="${cls}" data-id="${escHtml(id)}">
          <div class="job-index">${idx + 1}</div>
          <div class="job-status status-${escHtml(j.status)}">${escHtml(j.status)}</div>
          <div class="job-main">
            <div class="job-email" title="${escHtml(j.email)}">${escHtml(j.email)}</div>
          </div>
          <div class="job-source"><span class="badge-mode badge-mode-${escHtml(j.mail_mode || 'outlook')}">${escHtml(source)}</span></div>
          <div class="job-duration">${escHtml(fmtDuration(j.duration))}</div>
          <div class="job-progress" style="--progress:${progress}%"><span></span><em>${escHtml(progressLabel)}</em></div>
          <div class="job-updated">10:24:${String(31 - (idx % 9) * 3).padStart(2, '0')}</div>
          <div class="job-actions">
            ${actionBtn}
            <button class="icon-btn icon-danger" data-action="remove" data-id="${escHtml(id)}" title="Remove">${icon('remove')}</button>
          </div>
        </div>
      `;
    }).join('');

    dom.jobList.innerHTML = `
      <div class="job-table-head" aria-hidden="true">
        <span>Status</span>
        <span>Account</span>
        <span>Source</span>
        <span>Duration</span>
        <span>Progress</span>
        <span>Updated</span>
        <span>Actions</span>
      </div>
      ${html}
    `;
    dom.jobSummary.textContent = [
      `${state.order.length} total`,
      stats.running ? `${stats.running} running` : '',
      stats.queued ? `${stats.queued} queued` : '',
      stats.success ? `${stats.success} done` : '',
      stats.error ? `${stats.error} failed` : '',
    ].filter(Boolean).join(' · ');

    updateStatusPill(stats);
    updateLiveMetrics(stats);
  }

  function updateLiveMetrics(stats) {
    const total = state.order.length;
    const success = stats.success || 0;
    const error = stats.error || 0;
    const cancelled = stats.cancelled || 0;
    const running = stats.running || 0;
    const finished = success + error + cancelled;
    const successRate = finished ? (success / finished) * 100 : 0;
    const errorRate = finished ? (error / finished) * 100 : 0;
    const durations = state.order
      .map((id) => state.jobs.get(id))
      .filter((j) => j && Number.isFinite(j.duration) && j.duration > 0)
      .map((j) => j.duration);
    const avgDuration = durations.length
      ? durations.reduce((sum, value) => sum + value, 0) / durations.length
      : null;
    const started = state.order
      .map((id) => state.jobs.get(id))
      .filter((j) => j && Number.isFinite(j.started_at))
      .map((j) => j.started_at);
    const oldestStarted = started.length ? Math.min(...started) : null;
    const elapsedMinutes = oldestStarted ? Math.max((Date.now() / 1000 - oldestStarted) / 60, 1 / 60) : 0;
    const jobsPerMinute = elapsedMinutes ? total / elapsedMinutes : 0;

    if (dom.metricTotalJobs) dom.metricTotalJobs.textContent = String(total);
    if (dom.metricTotalNote) dom.metricTotalNote.textContent = total === 1 ? '1 job in queue' : `${total} jobs in queue`;
    if (dom.metricSuccessRate) dom.metricSuccessRate.textContent = fmtPercent(successRate);
    if (dom.metricSuccessNote) dom.metricSuccessNote.textContent = `${success} success`;
    const successRing = dom.metricSuccessRate
      ? dom.metricSuccessRate.closest('.metric-card')?.querySelector('.metric-ring')
      : null;
    if (successRing) successRing.style.setProperty('--metric-ring', `${Math.max(0, Math.min(100, successRate))}%`);
    if (dom.metricActiveRuns) dom.metricActiveRuns.textContent = String(running);
    if (dom.metricActiveNote) dom.metricActiveNote.textContent = running ? 'In progress' : 'Idle now';
    if (dom.metricAvgTime) dom.metricAvgTime.textContent = avgDuration == null ? '-' : fmtDuration(avgDuration);
    if (dom.metricAvgNote) dom.metricAvgNote.textContent = durations.length ? `${durations.length} timed jobs` : 'No duration yet';
    if (dom.metricErrorRate) dom.metricErrorRate.textContent = fmtPercent(errorRate);
    if (dom.metricErrorNote) dom.metricErrorNote.textContent = `${error} failed`;
    if (dom.insightJobsMin) dom.insightJobsMin.textContent = jobsPerMinute ? jobsPerMinute.toFixed(1) : '0.0';
    if (dom.insightSuccessRate) dom.insightSuccessRate.textContent = fmtPercent(successRate);
    if (dom.insightErrorRate) dom.insightErrorRate.textContent = fmtPercent(errorRate);
    const setText = (id, value) => {
      const el = document.getElementById(id);
      if (el) el.textContent = value;
    };
    setText('reg-rail-success', String(success));
    setText('reg-rail-running', String(running));
    setText('reg-rail-errors', String(error));
    updateRealtimeChart('reg-total-jobs-chart', total, {
      color: 'var(--ops-green)',
      displayValue: total,
      label: 'Registration total jobs',
      maxPoints: 32,
      visualAmplitude: Math.max(1, total * 0.08),
    });
    updateRealtimeChart('reg-active-runs-chart', running, {
      color: 'var(--ops-blue)',
      displayValue: running,
      label: 'Registration active runs',
      maxPoints: 32,
      visualAmplitude: Math.max(1, running * 0.2),
    });
    updateRealtimeChart('reg-avg-time-chart', avgDuration == null ? 0 : avgDuration, {
      color: 'var(--ops-blue)',
      displayValue: avgDuration == null ? '-' : fmtDuration(avgDuration),
      label: 'Registration average job time',
      maxPoints: 32,
      visualAmplitude: avgDuration == null ? 1 : Math.max(1, avgDuration * 0.08),
    });
    updateRealtimeChart('reg-error-rate-chart', errorRate, {
      color: 'var(--ops-red)',
      displayValue: fmtPercent(errorRate),
      label: 'Registration error rate',
      maxPoints: 32,
      visualAmplitude: Math.max(1, errorRate * 0.08),
    });
    updateRealtimeChart('reg-realtime-chart', jobsPerMinute, {
      color: 'var(--ops-green)',
      displayValue: jobsPerMinute ? jobsPerMinute.toFixed(1) : '0.0',
      label: 'Registration jobs per minute',
      visualAmplitude: Math.max(0.4, jobsPerMinute * 0.12),
    });
    updatePipelineFromStats(stats);
  }

  function updateStatusPill(stats) {
    if (!dom.statusPill) return;
    if (stats.running > 0) {
      dom.statusPill.className = 'pill pill-running';
      dom.statusPill.textContent = `running ${stats.running}/${state.maxConcurrent}`;
    } else if (stats.queued > 0) {
      dom.statusPill.className = 'pill pill-running';
      dom.statusPill.textContent = `queued ${stats.queued}`;
    } else if (stats.error > 0 && stats.success === 0) {
      dom.statusPill.className = 'pill pill-error';
      dom.statusPill.textContent = 'error';
    } else if (stats.success > 0) {
      dom.statusPill.className = 'pill pill-success';
      dom.statusPill.textContent = `done ${stats.success}`;
    } else {
      dom.statusPill.className = 'pill pill-idle';
      dom.statusPill.textContent = 'idle';
    }
  }

  // ── Render success/error output ──────────────────────────────────
  // Secrets không còn nằm trong job snapshot — fetch riêng qua /api/jobs/secrets.
  // Cache local để tránh round-trip mỗi render; refresh khi snapshot/SSE-job update.
  const secretsCache = new Map(); // job_id → {password, secret, first_code, session_path}
  let _secretsRefreshScheduled = false;

  async function refreshSecrets() {
    try {
      const data = await api('/api/jobs/secrets');
      secretsCache.clear();
      const map = data.secrets || {};
      for (const id of Object.keys(map)) {
        secretsCache.set(id, map[id] || {});
      }
      renderOutputs();
    } catch (err) {
      console.warn('refreshSecrets failed', err.message);
    }
  }

  function scheduleSecretsRefresh() {
    if (_secretsRefreshScheduled) return;
    _secretsRefreshScheduled = true;
    // Coalesce nhiều SSE update gần nhau — fetch 1 lần sau 250ms
    setTimeout(() => {
      _secretsRefreshScheduled = false;
      refreshSecrets();
    }, 250);
  }

  function renderOutputs() {
    const successLines = [];
    const errorLines = [];
    for (const id of state.order) {
      const j = state.jobs.get(id);
      if (!j) continue;
      const sec = secretsCache.get(id) || {};
      const password = sec.password || '';
      const secret = sec.secret || '';
      if (j.status === 'success' && secret) {
        successLines.push(`${j.email}|${password}|${secret}`);
      } else if (j.status === 'error') {
        // Signup OK nhưng 2FA fail (job.has_password=true, has_secret=false) → vẫn xuất
        if (password) {
          successLines.push(`${j.email}|${password}|no_2fa`);
        }
        errorLines.push(`${j.email}  →  ${j.error || 'unknown'}`);
      }
    }
    dom.successPane.textContent = successLines.length
      ? successLines.join('\n')
      : 'Format: email|password|secret_2fa';
    dom.errorPane.textContent = errorLines.length
      ? errorLines.join('\n')
      : 'No errors yet.';
  }

  // ── Render log của 1 job ─────────────────────────────────────────
  // -- Pipeline strip: phản ánh giai đoạn của job đang chọn ----------------
  // 4 bước: Input -> Verify -> Profile -> MFA. Suy giai đoạn từ status + nội
  // dung log gần nhất của job. Không có job -> về bước Input (mặc định).
  const PIPELINE_STEPS_COUNT = 5;

  function pipelineStageFromText(text) {
    // Trả về index bước cao nhất đã đạt (0..4) dựa trên marker trong log.
    const t = (text || '').toLowerCase();
    let stage = 0; // Mở GPT
    const lines = t.split('\n');
    for (const line of lines) {
      if (/submit email|screen=continue|authorize url|logging_id|post \/api\/accounts\/user\/register/i.test(line)) {
        stage = Math.max(stage, 1); // Nhập TK
      }
      if (/email-verification|email_otp|\botp\b|verification code|polling/i.test(line)) {
        stage = Math.max(stage, 2); // Đợi Code
      }
      if (/password|screen=password|about-you|about_you|create_account/i.test(line)) {
        stage = Math.max(stage, 3); // Pass
      }
      if (/\[2fa\]|enabling|mfa\/enroll|activate_enrollment|two_factor|phase 2/i.test(line)) {
        stage = Math.max(stage, 4); // 2FA
      }
    }
    return stage;
  }

  function updatePipeline(jobId) {
    const steps = dom.pipelineSteps || [];
    if (!steps.length) return;

    let stage = 0;
    let done = false;
    if (jobId) {
      const j = state.jobs.get(jobId);
      if (j) {
        if (j.status === 'success') {
          stage = PIPELINE_STEPS_COUNT - 1;
          done = true;
        } else if (j.status === 'queued') {
          stage = 0;
        } else {
          // running/error: suy từ nội dung log đang hiển thị
          stage = pipelineStageFromText(dom.logPane ? dom.logPane.textContent : '');
        }
      }
    }

    steps.forEach((el, i) => {
      el.classList.toggle('is-current', !done && i === stage);
      el.classList.toggle('is-done', done ? true : i < stage);
    });
  }

  function updatePipelineFromStats(stats) {
    const steps = dom.pipelineSteps || [];
    if (!steps.length) return;

    let job = null;
    if (state.activeJobId && state.jobs.has(state.activeJobId)) {
      const active = state.jobs.get(state.activeJobId);
      if (active && active.status === 'running') job = active;
    }
    if (!job) {
      for (const id of state.order) {
        const candidate = state.jobs.get(id);
        if (candidate && candidate.status === 'running') {
          job = candidate;
          break;
        }
      }
    }
    if (!job) {
      for (const id of state.order) {
        const candidate = state.jobs.get(id);
        if (candidate && candidate.status === 'queued') {
          job = candidate;
          break;
        }
      }
    }
    if (!job) {
      for (let i = state.order.length - 1; i >= 0; i -= 1) {
        const candidate = state.jobs.get(state.order[i]);
        if (candidate) {
          job = candidate;
          break;
        }
      }
    }

    let stage = 0;
    if (job && job.status === 'success') {
      stage = PIPELINE_STEPS_COUNT - 1;
    } else if (job && job.status !== 'queued') {
      const activeLog = state.activeJobId === job.id && dom.logPane ? dom.logPane.textContent : '';
      stage = pipelineStageFromText(activeLog);
      if (stage === 0) {
        const timeout = Math.max(30, Number(dom.jobTimeout?.value) || 240);
        const elapsed = Number.isFinite(job.duration)
          ? job.duration
          : (Number.isFinite(job.started_at) ? (Date.now() / 1000) - job.started_at : 0);
        stage = Math.floor(Math.max(0, Math.min(0.96, elapsed / timeout)) * PIPELINE_STEPS_COUNT);
      }
    }

    const liveStats = stats || computeJobStats(state.order, state.jobs);
    const done = Boolean(job && job.status === 'success' && !liveStats.running && !liveStats.queued);
    const failed = Boolean(job && (job.status === 'error' || job.status === 'cancelled') && !liveStats.running);
    const strip = steps[0].closest('.pipeline-strip');
    if (strip) {
      strip.classList.toggle('is-running', Boolean(liveStats.running));
      strip.classList.toggle('is-complete', done);
      strip.classList.toggle('is-error', failed);
    }

    steps.forEach((el, i) => {
      el.classList.toggle('is-current', !done && i === stage);
      el.classList.toggle('is-done', done ? true : i < stage);
      el.classList.toggle('is-error', failed && i === stage);
    });
  }

  function renderLog(jobId) {
    if (!jobId) {
      dom.logPane.textContent = '';
      dom.logTarget.textContent = '-';
      updatePipeline(null);
      return;
    }
    const j = state.jobs.get(jobId);
    if (!j) return;
    dom.logTarget.textContent = j.email;
    api(`/api/jobs/${jobId}/log`).then((data) => {
      const lines = data.log || [];
      // Mỗi span tự kết thúc bằng '\n' (giống applyLog) để SSE append sau
      // không bị dính vào span cuối.
      dom.logPane.innerHTML = lines.map((l) => {
        const cls = /(error|FAILED|fatal)/i.test(l)
          ? 'log-line-error'
          : 'log-line-info';
        return `<span class="${cls}">${escHtml(l)}\n</span>`;
      }).join('');
      dom.logPane.scrollTop = dom.logPane.scrollHeight;
    }).catch((err) => {
      dom.logPane.textContent = `[error] ${err.message}`;
    });
  }

  // ── Job actions ──────────────────────────────────────────────────
  dom.jobList.addEventListener('click', async (e) => {
    const target = e.target;
    const actionBtn = target.closest('[data-action]');
    if (actionBtn) {
      const action = actionBtn.dataset.action;
      const id = actionBtn.dataset.id;
      e.stopPropagation();

      if (action === 'retry') {
        if (!(await Dialog.confirm({ message: 'Retry this job?' }))) return;
        api(`/api/jobs/${id}/retry`, { method: 'POST' }).catch(async (err) => { await Dialog.alert({ message: err.message }); });
      } else if (action === 'stop') {
        if (!(await Dialog.confirm({ message: 'Stop this running job?' }))) return;
        api(`/api/jobs/${id}`, { method: 'DELETE' }).catch(async (err) => { await Dialog.alert({ message: err.message }); });
      } else if (action === 'remove') {
        if (!(await Dialog.confirm({ message: 'Remove this job from the list and textarea?' }))) return;
        const j = state.jobs.get(id);
        if (j) removeFromTextarea(j.email);
        api(`/api/jobs/${id}`, { method: 'DELETE' }).catch(async (err) => { await Dialog.alert({ message: err.message }); });
      }
      return;
    }
    const row = target.closest('.job');
    if (row) {
      state.activeJobId = row.dataset.id;
      renderJobs();
      renderLog(state.activeJobId);
    }
  });

  function removeFromTextarea(email) {
    const lines = dom.comboInput.value.split('\n');
    const filtered = lines.filter((l) => {
      const m = l.trim().split('|')[0];
      return m.toLowerCase() !== email.toLowerCase();
    });
    dom.comboInput.value = filtered.join('\n');
    updateComboCount();
    persistTextarea(LS_INPUT_REG, dom.comboInput.value);
  }

  // ── Mode → concurrency mapping ────────────────────────────────────
  // Reg cap [1, 2] — dropdown share giữa các tab có Multi (3..50). Ở Reg,
  // mọi giá trị > 2 đều silent clamp xuống 2 (yêu cầu sản phẩm).
  function _modeToConcurrency(mode) {
    const raw = window.GptUi.modeToConcurrency(mode);
    return Math.min(raw, 2);
  }

  // ── Run button ───────────────────────────────────────────────────
  dom.btnRun.addEventListener('click', async () => {
    const combos = dom.comboInput.value.trim();
    if (!combos) {
      await Dialog.alert({ message: 'Paste combos first.' });
      return;
    }
    const regProxy = dom.regProxyInput.value.trim();
    const useProxy = dom.proxyToggle.checked;
    if (useProxy && !regProxy) {
      dom.regProxyInput.setAttribute('aria-invalid', 'true');
      dom.regProxyInput.focus();
      await Dialog.alert({ message: 'Proxy đang bật. Hãy nhập Reg proxy hoặc tắt Use proxy.' });
      return;
    }
    dom.btnRun.disabled = true;
    try {
      // Luôn sync config server trước khi chạy
      const target = _modeToConcurrency(state.mode);
      const config = await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ max_concurrent: target, proxy: regProxy, use_proxy: useProxy }),
      });
      state.maxConcurrent = target;
      state.useProxy = !!config.use_proxy;
      dom.proxyToggle.checked = state.useProxy;
      dom.regProxyInput.removeAttribute('aria-invalid');
      await Settings.save('reg.proxy', config.proxy || null, getAuthToken());
      await Settings.save('reg.use_proxy', !!config.use_proxy, getAuthToken());

      // Build payload theo mail mode
      const payload = {
        combos,
        default_password: dom.defaultPassword.value.trim() || null,
        mail_mode: state.currentMailMode,
        reg_mode: dom.regModeSelect.value || 'browser',
      };
      if (state.currentMailMode === 'worker') {
        // Đọc trực tiếp từ DOM input (không chỉ localStorage — user có thể chưa trigger persist)
        const urlInp = dom.mailModeConfigHost.querySelector('input[data-config-key="logs_url"]');
        const keyInp = dom.mailModeConfigHost.querySelector('input[data-config-key="api_key"]');
        payload.email_logs_url = (urlInp && urlInp.value.trim()) || '';
        payload.email_api_key = (keyInp && keyInp.value.trim()) || '';
      }

      await api('/api/jobs', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
    } catch (err) {
      if (/invalid Reg proxy/i.test(err.message || '')) {
        dom.regProxyInput.setAttribute('aria-invalid', 'true');
      }
      await Dialog.alert({ message: 'Error: ' + err.message });
    } finally {
      dom.btnRun.disabled = false;
      validateWorkerConfig();
    }
  });

  dom.btnClearInput.addEventListener('click', () => {
    dom.comboInput.value = '';
    updateComboCount();
    clearPersistedTextarea(LS_INPUT_REG);
  });

  dom.btnStopAll.addEventListener('click', async () => {
    if (!(await Dialog.confirm({ message: 'Stop all running or queued jobs?' }))) return;
    try {
      const res = await api('/api/jobs/stop-all', { method: 'POST' });
      console.log('stopped:', res.stopped);
    } catch (err) {
      await Dialog.alert({ message: 'Error: ' + err.message });
    }
  });

  document.getElementById('btn-clear-done').addEventListener('click', async () => {
    try {
      const res = await api('/api/jobs/clear-finished', { method: 'POST' });
      // Refresh list (SSE sẽ broadcast clear_finished event)
      console.log('cleared:', res.removed);
    } catch (err) {
      await Dialog.alert({ message: 'Error: ' + err.message });
    }
  });

  document.getElementById('btn-clear-all').addEventListener('click', async () => {
    if (!(await Dialog.confirm({ message: 'Xóa TẤT CẢ jobs (mọi trạng thái)? Hành động không thể hoàn tác.', danger: true, confirmLabel: 'Xóa' }))) return;
    try {
      const res = await api('/api/jobs/clear-all', { method: 'POST' });
      console.log('clear-all:', res.removed);
    } catch (err) {
      await Dialog.alert({ message: 'Error: ' + err.message });
    }
  });

  document.getElementById('btn-retry-failed').addEventListener('click', async () => {
    if (!(await Dialog.confirm({ message: 'Retry tất cả jobs error & cancelled?' }))) return;
    try {
      const res = await api('/api/jobs/retry-failed', { method: 'POST' });
      console.log('retry-failed:', res.retried);
    } catch (err) {
      await Dialog.alert({ message: 'Error: ' + err.message });
    }
  });

  dom.concurrencySelects.forEach(sel => {
    sel.addEventListener('change', (e) => {
      const tab = e.target.dataset.tab || 'reg';
      const mode = e.target.value;
      const target = window.GptUi.modeToConcurrency(mode);

      // Save locally
      Settings.save(tab + '.mode', mode, getAuthToken());
      if (tab === 'reg') {
        state.mode = mode;
        state.maxConcurrent = target;
      }

      // Update backend
      let endpoint = '/api/config';
      if (tab === 'session') endpoint = '/api/session/config';
      else if (tab === 'link') endpoint = '/api/link/config';
      else if (tab === 'upi') endpoint = '/api/upi/config';

      api(endpoint, {
        method: 'POST',
        body: JSON.stringify({ max_concurrent: target }),
      }).catch(err => console.error(err));
    });
  });

  document.addEventListener('gpt:tab', (e) => {
    // No longer need to sync global modeSelect
  });

  dom.headlessToggle.addEventListener('change', async () => {
    const headless = dom.headlessToggle.checked;
    // Cảnh báo: jobs đang RUNNING không bị ảnh hưởng (browser đã launch)
    let runningCount = 0;
    for (const [, j] of state.jobs) {
      if (j.status === 'running') runningCount += 1;
    }
    if (runningCount > 0) {
      const ok = await Dialog.confirm({ message:
        `Có ${runningCount} job đang RUNNING — đổi Headless không ` +
        `áp dụng cho job đó (browser đã launch). Chỉ ảnh hưởng job mới.\n\n` +
        `Tiếp tục đổi sang ${headless ? 'Headless' : 'Headed'}?`
      });
      if (!ok) {
        dom.headlessToggle.checked = state.headless;
        return;
      }
    }
    try {
      await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ headless }),
      });
      state.headless = headless;
    } catch (err) {
      console.error(err);
      dom.headlessToggle.checked = state.headless;
    }
  });

  dom.debugToggle.addEventListener('change', async () => {
    const debug = dom.debugToggle.checked;
    try {
      await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ debug }),
      });
      state.debug = debug;
    } catch (err) {
      console.error(err);
      dom.debugToggle.checked = state.debug;
    }
  });

  dom.proxyToggle.addEventListener('change', async () => {
    const useProxy = dom.proxyToggle.checked;
    try {
      await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ use_proxy: useProxy }),
      });
      state.useProxy = useProxy;
      await Settings.save('reg.use_proxy', useProxy, getAuthToken());
    } catch (err) {
      console.error(err);
      dom.proxyToggle.checked = state.useProxy;
    }
  });

  dom.regProxyInput.addEventListener('change', async () => {
    const proxy = dom.regProxyInput.value.trim();
    try {
      const config = await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ proxy }),
      });
      state.useProxy = !!config.use_proxy;
      dom.regProxyInput.removeAttribute('aria-invalid');
      await Settings.save('reg.proxy', config.proxy || null, getAuthToken());
    } catch (err) {
      dom.regProxyInput.setAttribute('aria-invalid', 'true');
      await Dialog.alert({ message: 'Reg proxy is invalid: ' + err.message });
    }
  });

  dom.jobTimeout.addEventListener('change', async () => {
    const val = parseInt(dom.jobTimeout.value, 10);
    if (isNaN(val) || val < 30 || val > 600) return;
    try {
      await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ job_timeout: val }),
      });
    } catch (err) {
      console.error(err);
    }
  });

  dom.autoRetryMax.addEventListener('change', async () => {
    const val = parseInt(dom.autoRetryMax.value, 10);
    if (isNaN(val) || val < 0 || val > 10) return;
    const enabled = val > 0;
    try {
      await api('/api/config', {
        method: 'POST',
        body: JSON.stringify({ auto_retry: enabled, auto_retry_max: val || 1 }),
      });
    } catch (err) {
      console.error(err);
    }
  });

  // Password field persist — write-through via Settings API (ui-only, no dedicated endpoint)
  dom.defaultPassword.addEventListener('input', () => {
    const token = getAuthToken();
    if (token) Settings.save('reg.default_password', dom.defaultPassword.value || null, token);
  });

  // ── Copy buttons ─────────────────────────────────────────────────
  dom.btnCopySuccess.addEventListener('click', () => copyText(dom.successPane.textContent));
  dom.btnCopyError.addEventListener('click', () => copyText(dom.errorPane.textContent));
  if (dom.btnClearLog) {
    dom.btnClearLog.addEventListener('click', () => {
      dom.logPane.textContent = '';
    });
  }

  // ── SSE event stream ─────────────────────────────────────────────
  function applySnapshot(jobs) {
    state.order = jobs.map((j) => j.id);
    state.jobs.clear();
    for (const j of jobs) state.jobs.set(j.id, j);
    // Prune secretsCache theo job set hiện tại
    for (const cachedId of Array.from(secretsCache.keys())) {
      if (!state.jobs.has(cachedId)) secretsCache.delete(cachedId);
    }
    renderJobs();
    renderOutputs();
    scheduleSecretsRefresh();
  }

  function applyJobUpdate(j) {
    const prev = state.jobs.get(j.id);
    if (!prev) {
      state.order.push(j.id);
    }
    state.jobs.set(j.id, j);
    renderJobs();
    renderOutputs();
    // Khi job chuyển success/error → có thể có secrets mới → fetch lại
    if (j.status === 'success' || j.status === 'error') {
      scheduleSecretsRefresh();
    }
    if (j.status === 'error' && (!prev || prev.status !== 'error')) {
      playErrorAlert();
    }
    if (j.status === 'success' && (!prev || prev.status !== 'success')) {
      playSuccessAlert();
    }
    if (state.activeJobId === j.id) {
      // refresh log nếu đang xem
      renderLog(j.id);
      updatePipeline(j.id);
    }
  }

  function applyRemove(jobId) {
    state.jobs.delete(jobId);
    state.order = state.order.filter((id) => id !== jobId);
    secretsCache.delete(jobId);
    if (state.activeJobId === jobId) {
      state.activeJobId = null;
      renderLog(null);
    }
    renderJobs();
    renderOutputs();
  }

  function applyLog(jobId, line) {
    if (state.activeJobId !== jobId) return;
    const cls = /(error|FAILED|fatal)/i.test(line) ? 'log-line-error' : 'log-line-info';
    const span = document.createElement('span');
    span.className = cls;
    span.textContent = line + '\n';
    dom.logPane.appendChild(span);
    dom.logPane.scrollTop = dom.logPane.scrollHeight;
    updatePipelineFromStats(computeJobStats(state.order, state.jobs));
  }

  // ── SseBus handler for 'reg' channel ───────────────────────────────
  SseBus.on('reg', (data) => {
    if (data.type === 'snapshot') {
      state.maxConcurrent = data.max_concurrent;
      if (typeof data.headless === 'boolean') {
        state.headless = data.headless;
        dom.headlessToggle.checked = data.headless;
      }
      if (typeof data.debug === 'boolean') {
        state.debug = data.debug;
        dom.debugToggle.checked = data.debug;
      }
      if (typeof data.use_proxy === 'boolean') {
        state.useProxy = data.use_proxy;
        dom.proxyToggle.checked = data.use_proxy;
      }
      if (data.job_timeout) {
        dom.jobTimeout.value = data.job_timeout;
      }
      applySnapshot(data.jobs);
    } else if (data.type === 'job') {
      applyJobUpdate(data.job);
    } else if (data.type === 'remove') {
      applyRemove(data.job_id);
    } else if (data.type === 'clear_finished') {
      api('/api/jobs').then((r) => applySnapshot(r.jobs)).catch(console.error);
    } else if (data.type === 'clear_all') {
      state.jobs.clear();
      state.order = [];
      secretsCache.clear();
      state.activeJobId = null;
      renderJobs();
      renderOutputs();
      renderLog(null);
    } else if (data.type === 'log') {
      applyLog(data.job_id, data.line);
    }
  });

  // ── Mail Mode ─────────────────────────────────────────────────────
  let _workerConfigDebounce = null;

  function getWorkerConfig() {
    // Hydrate from Settings store (mail_mode.worker_config is a JSON object)
    const cfg = Settings.get('mail_mode.worker_config');
    return (cfg && typeof cfg === 'object') ? cfg : {};
  }

  function saveWorkerConfig(cfg) {
    Settings.save('mail_mode.worker_config', cfg, getAuthToken());
  }

  function renderMailModeSelector(modes) {
    dom.mailModeSelect.innerHTML = modes.map(m =>
      `<option value="${escHtml(m.id)}">${escHtml(m.label)}</option>`
    ).join('');
  }

  function renderMailModeConfig(modes, modeId) {
    const spec = modes.find(m => m.id === modeId);
    if (!spec || spec.config_schema.length === 0) {
      dom.mailModeConfigHost.innerHTML = '';
      return;
    }
    const saved = getWorkerConfig();
    // Ensure defaults are persisted immediately
    let needSave = false;
    for (const f of spec.config_schema) {
      if (saved[f.key] === undefined) {
        saved[f.key] = f.default;
        needSave = true;
      }
    }
    if (needSave) saveWorkerConfig(saved);
    const fields = spec.config_schema.map(f => {
      const val = saved[f.key] !== undefined ? saved[f.key] : f.default;
      const widthClass = f.key === 'api_key' ? 'config-field-short' : 'config-field-long';
      return `
        <label class="input-group ${widthClass}">
          <span class="input-label">${escHtml(f.label)}${f.required ? ' *' : ''}</span>
          <input type="text" data-config-key="${escHtml(f.key)}" value="${escHtml(val)}" spellcheck="false" autocomplete="off" />
          <span class="input-error" id="err-${escHtml(f.key)}"></span>
        </label>
      `;
    }).join('');
    // Sử dụng display:contents wrapper — elements trực tiếp nằm trong flex row
    dom.mailModeConfigHost.innerHTML = `<div class="mail-mode-config-panel">${fields}</div>`;
    // Attach events
    dom.mailModeConfigHost.querySelectorAll('input[data-config-key]').forEach(inp => {
      inp.addEventListener('input', () => debouncePersistWorkerConfig());
      inp.addEventListener('blur', () => debouncePersistWorkerConfig());
    });
    validateWorkerConfig();
  }

  function debouncePersistWorkerConfig() {
    clearTimeout(_workerConfigDebounce);
    _workerConfigDebounce = setTimeout(() => {
      const cfg = {};
      dom.mailModeConfigHost.querySelectorAll('input[data-config-key]').forEach(inp => {
        cfg[inp.dataset.configKey] = inp.value;
      });
      saveWorkerConfig(cfg);
      validateWorkerConfig();
    }, 500);
  }

  function validateWorkerConfig() {
    if (state.currentMailMode !== 'worker') {
      dom.btnRun.disabled = false;
      return;
    }
    const spec = state.mailModes.find(m => m.id === 'worker');
    if (!spec) return;
    let valid = true;
    for (const f of spec.config_schema) {
      const inp = dom.mailModeConfigHost.querySelector(`input[data-config-key="${f.key}"]`);
      const errEl = document.getElementById(`err-${f.key}`);
      if (!inp || !errEl) continue;
      const val = inp.value.trim();
      if (f.validate_prefix && f.validate_prefix.length) {
        if (!f.validate_prefix.some(p => val.startsWith(p))) {
          errEl.textContent = `Must start with ${f.validate_prefix.join(' or ')}`;
          errEl.className = 'input-error';
          valid = false;
          continue;
        }
      }
      if (f.required && !val) {
        errEl.textContent = 'Required';
        errEl.className = 'input-error';
        valid = false;
        continue;
      }
      if (!f.required && !val) {
        errEl.textContent = 'Blank - Worker sends no Authorization header';
        errEl.className = 'input-warn';
        continue;
      }
      errEl.textContent = '';
    }
    dom.btnRun.disabled = !valid;
  }

  function applyMailMode(modeId) {
    state.currentMailMode = modeId;
    dom.mailModeSelect.value = modeId;
    Settings.save('mail_mode.current', modeId, getAuthToken());
    const spec = state.mailModes.find(m => m.id === modeId);
    if (spec) {
      const uiCopy = mailModeUiCopy[modeId] || {};
      dom.comboInput.placeholder = uiCopy.input_placeholder || spec.input_placeholder;
      dom.inputHint.textContent = uiCopy.input_help || spec.input_help;
    }
    renderMailModeConfig(state.mailModes, modeId);
  }

  async function bootstrapMailModes() {
    try {
      const data = await api('/api/mail-modes');
      state.mailModes = data.modes || [];
    } catch (err) {
      console.error('Failed to load mail modes:', err);
      state.mailModes = [
        { id: 'outlook', label: 'Hotmail (combo)', input_placeholder: 'email|password|refresh_token|client_id', input_help: 'One Outlook combo per line.', config_schema: [] },
      ];
    }
    renderMailModeSelector(state.mailModes);
    // Restore from Settings store (DB-backed)
    const saved = Settings.get('mail_mode.current');
    const validIds = state.mailModes.map(m => m.id);
    const initial = (saved && validIds.includes(saved)) ? saved : 'outlook';
    applyMailMode(initial);
    // Listen change
    dom.mailModeSelect.addEventListener('change', () => {
      applyMailMode(dom.mailModeSelect.value);
    });

    // ── Reg Mode selector (browser / pure_request) ───────────────
    const savedRegMode = Settings.get('reg_mode.current');
    if (savedRegMode && ['browser', 'pure_request'].includes(savedRegMode)) {
      dom.regModeSelect.value = savedRegMode;
    }
    dom.regModeSelect.addEventListener('change', () => {
      Settings.save('reg_mode.current', dom.regModeSelect.value, getAuthToken());
    });
  }

  // ── Init ─────────────────────────────────────────────────────────
  // Settings hydration: load all settings from DB via Settings.bootstrap(token),
  // then hydrate UI controls. Server is source of truth (write-through from
  // POST /api/config ensures DB stays in sync).

  // Restore combo textarea — chỉ mất khi user bấm Clear Input
  const _savedReg = localStorage.getItem(LS_INPUT_REG);
  if (_savedReg) dom.comboInput.value = _savedReg;

  // Bootstrap: load settings from DB then hydrate UI
  (async () => {
    const token = getAuthToken();
    await Settings.bootstrap(token);

    // Hydrate state + UI controls từ Settings store (DB-backed)
    // Hydrate per-tab concurrency selects
    dom.concurrencySelects.forEach(sel => {
      const tab = sel.dataset.tab || 'reg';
      const savedMode = Settings.get(tab + '.mode') || 'multi';
      sel.value = savedMode;
      if (tab === 'reg') state.mode = savedMode;
    });

    const headless = Settings.get('reg.headless');
    if (typeof headless === 'boolean') state.headless = headless;
    dom.headlessToggle.checked = state.headless;

    const debug = Settings.get('reg.debug');
    if (typeof debug === 'boolean') state.debug = debug;
    dom.debugToggle.checked = state.debug;

    const useProxy = Settings.get('reg.use_proxy');
    if (typeof useProxy === 'boolean') state.useProxy = useProxy;
    dom.proxyToggle.checked = state.useProxy;

    const regProxy = Settings.get('reg.proxy');
    dom.regProxyInput.value = typeof regProxy === 'string' ? regProxy : '';

    const defaultPassword = Settings.get('reg.default_password');
    if (defaultPassword) dom.defaultPassword.value = defaultPassword;

    const jobTimeout = Settings.get('reg.job_timeout');
    if (typeof jobTimeout === 'number') dom.jobTimeout.value = jobTimeout;

    const autoRetry = Settings.get('reg.auto_retry');
    const autoRetryMax = Settings.get('reg.auto_retry_max');
    if (typeof autoRetryMax === 'number') {
      dom.autoRetryMax.value = autoRetry ? autoRetryMax : 0;
    }

    // Server GET /api/config — source of truth cho runtime state (headless/debug/etc.)
    // Override từ DB nếu server đã apply khác (ví dụ manager changed in-memory).
    try {
      const cfg = await api('/api/config');
      if (typeof cfg.headless === 'boolean') {
        state.headless = cfg.headless;
        dom.headlessToggle.checked = cfg.headless;
      }
      if (typeof cfg.debug === 'boolean') {
        state.debug = cfg.debug;
        dom.debugToggle.checked = cfg.debug;
      }
      if (typeof cfg.use_proxy === 'boolean') {
        state.useProxy = cfg.use_proxy;
        dom.proxyToggle.checked = cfg.use_proxy;
      }
      dom.regProxyInput.value = typeof cfg.proxy === 'string' ? cfg.proxy : '';
      if (typeof cfg.job_timeout === 'number') {
        dom.jobTimeout.value = cfg.job_timeout;
      }
      if (typeof cfg.auto_retry_max === 'number') {
        dom.autoRetryMax.value = cfg.auto_retry ? cfg.auto_retry_max : 0;
      }
    } catch (err) {
      console.error('GET /api/config failed, dùng Settings DB fallback:', err);
    }

    // initTabs + bootstrapMailModes phải chạy SAU Settings.bootstrap()
    // vì cần Settings.get('ui.active_tab') + Settings.get('mail_mode.current')
    initTabs();
    bootstrapMailModes();
  })();

  updateComboCount();

  // Start unified SSE connection (single connection for all channels)
  SseBus.connect();

  // Timer cập nhật duration cho jobs đang running mỗi giây
  setInterval(() => {
    let hasRunning = false;
    for (const [id, j] of state.jobs) {
      if (j.status === 'running' && j.started_at) {
        hasRunning = true;
        j.duration = (Date.now() / 1000) - j.started_at;
      }
    }
    if (hasRunning) renderJobs();
  }, 1000);
})();
