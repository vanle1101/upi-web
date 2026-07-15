import os

# Đường dẫn file
index_path = r"c:\Users\lehon\OneDrive\Desktop\gpt_signup_hybrid-main\web\static\index.html"

# Phần 1 của file index.html (dòng 1 đến 779 của file gốc 1077 dòng, đã tích hợp data-i18n và font Outfit)
part1 = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<meta name="description" content="GSH internal operations console for account, session and payment workflows." />
<title>GSH Operations Console</title>
<meta name="auth-token" content="__AUTH_TOKEN__" />
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/style.css?v=__ASSET_VERSION__" />
<link rel="stylesheet" href="/static/workspace.css?v=__ASSET_VERSION__" />
<link rel="stylesheet" href="/static/mac_select.css?v=__ASSET_VERSION__" />
<link rel="stylesheet" href="/static/operations.css?v=__ASSET_VERSION__" />
</head>
<body>
<a class="skip-link" href="#tab-reg">Skip to workspace</a>
<header class="topbar">
  <div class="mac-traffic-lights">
    <span class="mac-btn close"></span>
    <span class="mac-btn minimize"></span>
    <span class="mac-btn maximize"></span>
  </div>
  <div class="brand">
    <span class="brand-mark" aria-hidden="true">
      <span class="brand-dot"></span>
    </span>
    <span class="brand-copy">
      <span class="brand-name">GSH</span>
      <span class="brand-tag" data-i18n="brand_tag">Operations Console</span>
    </span>
  </div>
  <nav class="tab-nav">
    <button class="tab-btn active" data-tab="reg" aria-label="Reg" data-i18n="reg">
      <span class="tab-glyph" aria-hidden="true"></span>
      <span class="tab-copy"><strong>Reg</strong><small>Provision accounts</small></span>
    </button>
    <button class="tab-btn" data-tab="session" aria-label="Get Session" data-i18n="session">
      <span class="tab-glyph" aria-hidden="true"></span>
      <span class="tab-copy"><strong>Get Session</strong><small>Capture auth state</small></span>
    </button>
    <button class="tab-btn" data-tab="upi" aria-label="UPI QR" data-i18n="upi">
      <span class="tab-glyph" aria-hidden="true"></span>
      <span class="tab-copy"><strong>UPI QR</strong><small>Payment issuance</small></span>
    </button>
    <button class="tab-btn" data-tab="getacc" aria-label="Get Acc" data-i18n="getacc">
      <span class="tab-glyph" aria-hidden="true"></span>
      <span class="tab-copy"><strong>Get Acc</strong><small>Extract credentials</small></span>
    </button>
    <button class="tab-btn" data-tab="settings" aria-label="Settings" data-i18n="settings">
      <span class="tab-glyph" aria-hidden="true"></span>
      <span class="tab-copy"><strong>Settings</strong><small>Runtime controls</small></span>
    </button>
  </nav>
  <div class="topbar-actions">
    <span class="rail-section-label" data-i18n="runtime_section">Runtime</span>
    <label class="toggle-wrap" data-i18n-title="headless_title" title="Bật để ẩn cửa sổ trình duyệt khi chạy">
      <input type="checkbox" id="headless-toggle" checked />
      <span class="toggle-track"><span class="toggle-thumb"></span></span>
      <span class="toggle-label" data-i18n="runtime_label">Headless</span>
    </label>

    <label class="toggle-wrap" data-i18n-title="debug_title" title="Giữ browser mở sau khi job xong (chỉ khi headed)">
      <input type="checkbox" id="debug-toggle" />
      <span class="toggle-track"><span class="toggle-thumb"></span></span>
      <span class="toggle-label" data-i18n="debug_label">Debug</span>
    </label>
    
    <div class="sidebar-footer-controls">
      <button id="theme-toggle-btn" class="theme-toggle-btn" aria-label="Toggle Theme" title="Toggle Theme"></button>
      <button id="lang-toggle-btn" class="lang-toggle-btn" aria-label="Toggle Language" title="Toggle Language">EN</button>
    </div>
  </div>
</header>

<!-- ════════════════ TAB: REG ════════════════ -->
<main class="tab-content ops-workspace ops-reg active" id="tab-reg">
  <header class="workspace-mast">
    <div class="workspace-title-group">
      <span class="workspace-kicker" data-i18n="reg_kicker">Account provisioning</span>
      <h1 data-i18n="reg_title">Registration desk</h1>
      <p data-i18n="reg_desc">Prepare identities, monitor browser work and review MFA results from one queue.</p>
    </div>
    <div class="pipeline-strip" aria-label="Registration pipeline">
      <span class="pipeline-step is-current">Mở GPT</span>
      <span class="pipeline-step">Nhập TK</span>
      <span class="pipeline-step">Đợi Code</span>
      <span class="pipeline-step">Pass</span>
      <span class="pipeline-step">2FA</span>
    </div>
  </header>

  <div class="workspace-grid">
    <aside class="control-rail">
  <section class="card card-input control-surface">
    <header class="card-head">
      <h2 data-i18n="reg_source_accounts">Source accounts</h2>
      <span class="muted card-head-note" id="input-hint" data-i18n="reg_input_hint">One combo per line: email|password|refresh_token|client_id</span>
    </header>
    <!-- Mail Mode + Worker config: 1 row, label trên / control dưới -->
    <div class="mail-mode-row">
      <label class="input-group config-field-mode">
        <span class="input-label" data-i18n="reg_mail_mode">Mail Mode</span>
        <select id="mail-mode-select"></select>
      </label>
      <label class="input-group config-field-mode">
        <span class="input-label" data-i18n="reg_reg_mode">Reg Mode</span>
        <select id="reg-mode-select">
          <option value="browser">Browser (anti-detect)</option>
          <option value="pure_request">Pure Request (HTTP only)</option>
        </select>
      </label>
      <div id="mail-mode-config-host" class="mail-mode-config-host"></div>
    </div>
    <textarea class="combo-textarea" id="combo-input" placeholder="email1@hotmail.com|pwd1|M.C548...|9e5f94bc-...&#10;email2@outlook.com|pwd2|M.C525...|9e5f94bc-..."></textarea>
    <div class="card-settings">
      <div class="card-settings-row card-settings-row-mixed">
        <label class="input-group config-field-long">
          <span class="input-label" data-i18n="reg_default_password">Default password</span>
          <input type="text" id="default-password" placeholder="Leave blank for random" data-i18n-placeholder="reg_default_password" autocomplete="off" spellcheck="false" />
        </label>
        <label class="toggle-wrap" title="Bật/tắt áp dụng proxy pool cho Reg jobs. Tắt = chạy direct (no proxy).">
          <input type="checkbox" id="proxy-toggle" checked />
          <span class="toggle-track"><span class="toggle-thumb"></span></span>
          <span class="toggle-label" data-i18n="reg_use_proxy">Proxy</span>
        </label>
        <label class="input-group config-field-short">
          <span class="input-label" data-i18n="reg_timeout">Timeout (s/job)</span>
          <input type="number" id="job-timeout" value="240" min="30" max="600" step="10" />
        </label>
      </div>
    </div>
    <div class="card-actions">
      <button id="btn-run" class="btn btn-primary" data-i18n="reg_start">Start registration</button>
      <button id="btn-stop-all" class="btn btn-danger" data-i18n="reg_stop">Stop All</button>
      <button id="btn-clear-input" class="btn btn-ghost" data-i18n="reg_clear">Clear Input</button>
      <span class="muted" id="combo-count" data-i18n="reg_combos_count">0 combos</span>
    </div>
  </section>
    </aside>

    <section class="execution-canvas">
  <section class="card card-jobs jobs-surface">
    <header class="card-head">
      <div class="panel-title-group">
        <h2 data-i18n="reg_queue_title">Execution queue</h2>
        <span class="panel-subtitle" data-i18n="reg_queue_desc">Live registration activity</span>
      </div>
      <div class="card-head-actions">
        <label class="input-group config-field-tiny" title="Số lần retry khi job bị error (0 = không retry)">
          <span class="input-label">Retry</span>
          <input type="number" id="auto-retry-max" value="0" min="0" max="10" step="1" />
        </label>
        <button id="btn-retry-failed" class="btn btn-ghost btn-small" data-i18n="reg_retry_failed" title="Retry all error & cancelled jobs">Retry Failed</button>
        <button id="btn-clear-done" class="btn btn-ghost btn-small" data-i18n="reg_clear_done" title="Remove finished jobs from memory">Clear Done</button>
        <button id="btn-clear-all" class="btn btn-ghost btn-small" data-i18n="reg_clear_all" title="Remove ALL jobs (all statuses)">Clear All</button>
        <span class="muted" id="job-summary">0 total</span>
      </div>
    </header>
    <div id="job-list" class="job-list">
      <div class="empty" data-i18n="reg_no_jobs">No jobs yet. Paste combos and click Run.</div>
    </div>
  </section>

      <section class="diagnostics-dock is-collapsed" data-dock="reg">
        <header class="dock-bar">
          <div class="dock-tabs" role="tablist" aria-label="Registration diagnostics">
            <button class="dock-tab active" type="button" role="tab" aria-selected="true" data-dock-target="reg-log" data-i18n="reg_tab_runtime">Runtime</button>
            <button class="dock-tab" type="button" role="tab" aria-selected="false" data-dock-target="reg-success" data-i18n="reg_tab_success">Success</button>
            <button class="dock-tab" type="button" role="tab" aria-selected="false" data-dock-target="reg-error" data-i18n="reg_tab_errors">Errors</button>
          </div>
          <div class="dock-context">
            <span class="dock-target" id="log-target">No job selected</span>
            <button id="btn-clear-log" class="btn btn-ghost btn-small" data-i18n="clear_log" title="Clear log viewer">Clear log</button>
            <button class="dock-collapse" type="button" data-dock-collapse data-i18n="show_details" aria-expanded="false">Show details</button>
          </div>
        </header>
        <div class="dock-panels">
          <section class="dock-panel active card card-log" role="tabpanel" data-dock-panel="reg-log">
            <pre id="log-pane" class="log-pane"></pre>
          </section>
          <section class="dock-panel card card-success" role="tabpanel" data-dock-panel="reg-success" hidden>
            <header class="dock-panel-head">
              <span data-i18n="reg_success_head">Completed account output</span>
              <button id="btn-copy-success" class="btn btn-ghost btn-small" data-i18n="copy_all">Copy all</button>
            </header>
            <pre id="success-pane" class="output-pane">Format: email|password|secret_2fa</pre>
          </section>
          <section class="dock-panel card card-error" role="tabpanel" data-dock-panel="reg-error" hidden>
            <header class="dock-panel-head">
              <span data-i18n="reg_error_head">Failed account output</span>
              <button id="btn-copy-error" class="btn btn-ghost btn-small" data-i18n="copy_all">Copy all</button>
            </header>
            <pre id="error-pane" class="output-pane">No errors yet.</pre>
          </section>
        </div>
      </section>
    </section>
  </div>
</main>

<!-- ════════════════ TAB: GET SESSION ════════════════ -->
<main class="tab-content ops-workspace ops-session" id="tab-session">
  <header class="workspace-mast">
    <div class="workspace-title-group">
      <span class="workspace-kicker" data-i18n="ses_kicker">Authentication recovery</span>
      <h1 data-i18n="ses_title">Session capture</h1>
      <p data-i18n="ses_desc">Resolve account credentials into current session payloads with visible job-level diagnostics.</p>
    </div>
    <div class="pipeline-strip pipeline-strip-session" aria-label="Session pipeline">
      <span class="pipeline-step is-current">Credentials</span>
      <span class="pipeline-step">Authorize</span>
      <span class="pipeline-step">2FA</span>
      <span class="pipeline-step">Session</span>
    </div>
  </header>

  <div class="workspace-grid">
    <aside class="control-rail">
  <section class="card card-input control-surface">
    <header class="card-head">
      <div class="panel-title-group">
        <h2 data-i18n="ses_credentials">Credentials</h2>
        <span class="panel-subtitle">email | password | secret</span>
      </div>
    </header>
    <textarea class="combo-textarea" id="ses-combo-input" placeholder="email@hotmail.com|password123|DNPARKKMM5EYOPDG...&#10;email2@hotmail.com|pass456|I77PEBZQNEBE67SU..."></textarea>
    <div class="card-settings">
      <label class="input-group settings-field-compact">
        <span class="input-label" data-i18n="reg_timeout">Timeout (s/job)</span>
        <input type="number" id="ses-job-timeout" value="120" min="30" max="600" step="10" />
      </label>
    </div>
    <div class="card-actions">
      <button id="ses-btn-run" class="btn btn-primary" data-i18n="ses_start">Get Session</button>
      <button id="ses-btn-stop-all" class="btn btn-danger" data-i18n="reg_stop">Stop All</button>
      <button id="ses-btn-clear-input" class="btn btn-ghost" data-i18n="reg_clear">Clear Input</button>
      <span class="muted" id="ses-combo-count" data-i18n="reg_combos_count">0 combos</span>
    </div>
  </section>
    </aside>

    <section class="execution-canvas">
  <section class="card card-jobs jobs-surface">
    <header class="card-head">
      <div class="panel-title-group">
        <h2 data-i18n="ses_queue_title">Session queue</h2>
        <span class="panel-subtitle" data-i18n="ses_queue_desc">Authentication and capture status</span>
      </div>
      <div class="card-head-actions">
        <button id="ses-btn-clear-done" class="btn btn-ghost btn-small" data-i18n="reg_clear_done">Clear Done</button>
        <span class="muted" id="ses-job-summary">0 total</span>
      </div>
    </header>
    <div id="ses-job-list" class="job-list">
      <div class="empty" data-i18n="ses_no_jobs">Paste combos and click Get Session.</div>
    </div>
  </section>

      <section class="diagnostics-dock is-collapsed" data-dock="session">
        <header class="dock-bar">
          <div class="dock-tabs" role="tablist" aria-label="Session diagnostics">
            <button class="dock-tab active" type="button" role="tab" aria-selected="true" data-dock-target="session-log" data-i18n="reg_tab_runtime">Runtime</button>
            <button class="dock-tab" type="button" role="tab" aria-selected="false" data-dock-target="session-error" data-i18n="reg_tab_errors">Errors</button>
          </div>
          <div class="dock-context">
            <span class="dock-target" id="ses-log-target">No job selected</span>
            <button id="ses-btn-clear-log" class="btn btn-ghost btn-small" data-i18n="clear_log" title="Clear log viewer">Clear log</button>
            <button class="dock-collapse" type="button" data-dock-collapse data-i18n="show_details" aria-expanded="false">Show details</button>
          </div>
        </header>
        <div class="dock-panels">
          <section class="dock-panel active card card-log" role="tabpanel" data-dock-panel="session-log">
            <pre id="ses-log-pane" class="log-pane"></pre>
          </section>
          <section class="dock-panel card card-error" role="tabpanel" data-dock-panel="session-error" hidden>
            <header class="dock-panel-head">
              <span data-i18n="ses_errors_head">Session capture failures</span>
              <button id="ses-btn-copy-error" class="btn btn-ghost btn-small" data-i18n="copy_all">Copy all</button>
            </header>
            <pre id="ses-error-pane" class="output-pane">No errors yet.</pre>
          </section>
        </div>
      </section>
    </section>
  </div>
</main>

<!-- ════════════════ TAB: UPI QR ════════════════ -->
<main class="tab-content ops-workspace ops-upi" id="tab-upi">
  <header class="workspace-mast">
    <div class="workspace-title-group">
      <span class="workspace-kicker" data-i18n="upi_kicker">Payment operations</span>
      <h1 data-i18n="upi_title">UPI issuance</h1>
      <p data-i18n="upi_desc">Generate, monitor and recover QR payment jobs without leaving the active queue.</p>
    </div>
    <div class="pipeline-strip pipeline-strip-upi" aria-label="UPI pipeline">
      <span class="pipeline-step is-current">Login</span>
      <span class="pipeline-step">Checkout</span>
      <span class="pipeline-step">Stripe</span>
      <span class="pipeline-step">Approve</span>
      <span class="pipeline-step">QR</span>
    </div>
  </header>

  <div class="workspace-grid">
    <aside class="control-rail">
  <section class="card card-input control-surface">
    <header class="card-head">
      <div class="panel-title-group">
        <h2 data-i18n="upi_identities">Payment identities</h2>
        <span class="panel-subtitle">Combo or API session JSON</span>
      </div>
    </header>
    <textarea class="combo-textarea" id="upi-combo-input" placeholder="email1@nik.edu.pl|GPT#xxx|TOTP_SECRET&#10;email2@nik.edu.pl|GPT#yyy|TOTP_SECRET"></textarea>
    <textarea class="combo-textarea upi-session-textarea" id="upi-session-input" placeholder='Hoặc dán API session JSON mới dòng 1 object từ https://chatgpt.com/api/auth/session&#10;{"user":{"email":"mail@example.com"},"accessToken":"eyJ...","expires":"..."}'></textarea>
    <div class="card-settings">
      <div class="card-settings-row card-settings-row-mixed">
        <label class="input-group config-field-short" title="Số luồng chạy song song">
          <span class="input-label" data-i18n="reg_reg_mode">Mode</span>
          <select id="upi-concurrency-select" class="concurrency-select" data-tab="upi">
            <option value="single">Single (1)</option>
            <option value="multi">Multi (2)</option>
            <option value="multi3">Multi (3)</option>
            <option value="multi5">Multi (5)</option>
            <option value="multi10">Multi (10)</option>
            <option value="multi20">Multi (20)</option>
            <option value="multi30">Multi (30)</option>
            <option value="multi50">Multi (50)</option>
          </select>
        </label>
        <label class="input-group config-field-short" title="Số lần retry POST /backend-api/payments/checkout/approve">
          <span class="input-label">Approve retries</span>
          <input type="number" id="upi-approve-retries" value="500" min="1" max="2000" step="1" />
        </label>
        <label class="input-group config-field-short" title="Timeout cho mỗi job (giây)">
          <span class="input-label" data-i18n="reg_timeout">Timeout (s/job)</span>
          <input type="number" id="upi-job-timeout" value="1800" min="60" max="7200" step="60" />
        </label>
        <label class="input-group config-field-short" title="Step bắt đầu áp proxy (1-6). 1 = login + checkout + stripe + approve via proxy (an toàn khi IP host non-IN). 3 = step 1-2 DIRECT, 3-6 via proxy (default — chỉ ổn nếu IP host hợp lệ).">
          <span class="input-label">Proxy from step</span>
          <select id="upi-proxy-from-step">
            <option value="1">1 — login + all (full proxy)</option>
            <option value="2">2 — checkout + later</option>
            <option value="3" selected>3 — stripe_init + later</option>
            <option value="4">4 — elements + later</option>
            <option value="5">5 — confirm + approve</option>
            <option value="6">6 — approve only</option>
          </select>
        </label>
        <span class="settings-divider" aria-hidden="true"></span>
        <label class="toggle-wrap" id="upi-notify-wrap" title="Bật để gửi QR + thông tin account qua Telegram khi job xong">
          <input type="checkbox" id="upi-notify-toggle" />
          <span class="toggle-track"><span class="toggle-thumb"></span></span>
          <span class="toggle-label" data-i18n="upi_telegram">Gửi Telegram</span>
        </label>
      </div>
      <div class="workflow-proxy-row">
        <div class="input-group workflow-proxy-field">
          <div class="workflow-proxy-heading">
            <label class="input-label" for="upi-proxy-input">UPI proxy <small>Only for UPI QR</small></label>
            <label class="toggle-wrap workflow-proxy-toggle" title="Use this proxy for UPI QR jobs">
              <input type="checkbox" id="upi-proxy-toggle" />
              <span class="toggle-track"><span class="toggle-thumb"></span></span>
              <span class="toggle-label" data-i18n="reg_use_proxy">Use proxy</span>
            </label>
          </div>
          <input type="text" id="upi-proxy-input" placeholder="host:port:user:pass (blank = direct)" spellcheck="false" autocomplete="off" />
        </div>
      </div>
    </div>
    <div class="card-actions">
      <button id="upi-btn-run" class="btn btn-primary" data-i18n="upi_start">Get UPI QR</button>
      <button id="upi-btn-stop-all" class="btn btn-danger" data-i18n="reg_stop">Stop All</button>
      <button id="upi-btn-clear-input" class="btn btn-ghost" data-i18n="reg_clear">Clear Input</button>
      <span class="muted" id="upi-combo-count" data-i18n="reg_combos_count">0 combos</span>
    </div>
  </section>
    </aside>

    <section class="execution-canvas">
  <section class="card card-jobs jobs-surface">
    <header class="card-head">
      <div class="panel-title-group">
        <h2 data-i18n="upi_queue_title">Payment queue</h2>
        <span class="panel-subtitle" data-i18n="upi_queue_desc">Checkout, approval and QR status</span>
      </div>
      <div class="card-head-actions">
        <button id="upi-btn-retry-expired-free" class="btn btn-ghost btn-small" data-i18n="upi_retry_expired" title="Retry mọi job có QR hết hạn nhưng vẫn Free">Retry Expired+Free</button>
        <button id="upi-btn-retry-failed" class="btn btn-ghost btn-small" data-i18n="reg_retry_failed" title="Retry all error & cancelled jobs">Retry Failed</button>
        <button id="upi-btn-clear-done" class="btn btn-ghost btn-small" data-i18n="reg_clear_done">Clear Done</button>
        <button id="upi-btn-clear-all" class="btn btn-ghost btn-small" data-i18n="reg_clear_all" title="Xóa TẤT CẢ jobs (mọi trạng thái)">Clear All</button>
        <span class="muted" id="upi-job-summary">0 total</span>
      </div>
    </header>
    <div id="upi-job-list" class="job-list">
      <div class="empty" data-i18n="upi_no_jobs">Paste accounts and click Get UPI QR.</div>
    </div>
  </section>

      <section class="diagnostics-dock is-collapsed" data-dock="upi">
        <header class="dock-bar">
          <div class="dock-tabs" role="tablist" aria-label="UPI diagnostics">
            <button class="dock-tab active" type="button" role="tab" aria-selected="true" data-dock-target="upi-log" data-i18n="reg_tab_runtime">Runtime</button>
            <button class="dock-tab" type="button" role="tab" aria-selected="false" data-dock-target="upi-output" data-i18n="reg_tab_success">Output</button>
            <button class="dock-tab" type="button" role="tab" aria-selected="false" data-dock-target="upi-error" data-i18n="reg_tab_errors">Errors</button>
          </div>
          <div class="dock-context">
            <span class="dock-target" id="upi-log-target">No job selected</span>
            <button class="dock-collapse" type="button" data-dock-collapse data-i18n="show_details" aria-expanded="false">Show details</button>
          </div>
        </header>
        <div class="dock-panels">
          <section class="dock-panel active card card-log" role="tabpanel" data-dock-panel="upi-log">
            <pre id="upi-log-pane" class="log-pane"></pre>
          </section>
          <section class="dock-panel card card-success" role="tabpanel" data-dock-panel="upi-output" hidden>
            <header class="dock-panel-head">
              <span data-i18n="upi_output_head">Generated payment output</span>
              <button id="upi-btn-copy-success" class="btn btn-ghost btn-small" data-i18n="copy_all">Copy all</button>
            </header>
            <pre id="upi-success-pane" class="output-pane">Format: email|password|secret_2fa</pre>
          </section>
          <section class="dock-panel card card-error" role="tabpanel" data-dock-panel="upi-error" hidden>
            <header class="dock-panel-head">
              <span data-i18n="upi_errors_head">Payment workflow failures</span>
              <button id="upi-btn-copy-error" class="btn btn-ghost btn-small" data-i18n="copy_all">Copy all</button>
            </header>
            <pre id="upi-error-pane" class="output-pane">No errors yet.</pre>
          </section>
        </div>
      </section>
    </section>
  </div>
</main>

<!-- ════════════════ TAB: GET ACC ════════════════ -->
<main class="tab-content ops-workspace ops-getacc" id="tab-getacc">
  <header class="workspace-mast">
    <div class="workspace-title-group">
      <span class="workspace-kicker" data-i18n="acc_kicker">Data extraction</span>
      <h1 data-i18n="acc_title">Get Account</h1>
      <p data-i18n="acc_desc">Paste a ChatGPT session JSON to extract the account's email, password, and 2FA secret.</p>
    </div>
  </header>

  <div class="workspace-grid">
    <aside class="control-rail">
      <section class="card card-input control-surface">
        <header class="card-head">
          <div class="panel-title-group">
            <h2 data-i18n="acc_json">JSON Payload</h2>
            <span class="panel-subtitle">Session or Reg JSON</span>
          </div>
        </header>
        <textarea id="getacc-json-input" class="combo-textarea" placeholder='{"WARNING_BANNER": "...", "user": {"email": "..."}}'></textarea>
        <div class="card-actions">
          <button id="getacc-extract-btn" class="btn btn-primary" style="width: 100%;" data-i18n="acc_start">Extract Credentials</button>
        </div>
      </section>
    </aside>

    <section class="execution-canvas">
      <section class="card card-jobs jobs-surface">
        <header class="card-head">
          <div class="panel-title-group">
            <h2 data-i18n="acc_queue_title">Extraction queue</h2>
            <span class="panel-subtitle" data-i18n="acc_queue_desc">Extracted cookies & credentials</span>
          </div>
          <div class="card-head-actions">
            <button id="getacc-btn-clear-all" class="btn btn-ghost btn-small" data-i18n="reg_clear_all" title="Remove all items">Clear All</button>
            <span class="muted" id="getacc-job-summary">0 total</span>
          </div>
        </header>
        <div id="getacc-job-list" class="job-list">
          <div class="empty" data-i18n="acc_no_jobs">No data yet. Paste JSON into the input box to begin.</div>
        </div>
      </section>
    </section>
  </div>
</main>
"""

# Đọc phần 2 từ index.html hiện tại (từ Settings page trở đi)
with open(index_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Tìm dòng bắt đầu Settings page
settings_start_idx = -1
for i, line in enumerate(lines):
    if 'id="tab-settings"' in line or "id='tab-settings'" in line or "tab-settings" in line:
        settings_start_idx = i - 1  # Lấy cả dòng comment phía trên
        break

if settings_start_idx == -1:
    print("Warning: Could not find tab-settings by id search.")
    # Thử tìm theo từ khóa TAB: SETTINGS
    for i, line in enumerate(lines):
        if "TAB: SETTINGS" in line:
            settings_start_idx = i
            break

if settings_start_idx != -1:
    print(f"Found settings at index: {settings_start_idx}")
    # Nối phần Settings và các modal
    part2_lines = lines[settings_start_idx:]
    part2 = "".join(part2_lines)
    
    # Thực hiện dịch động một số tag trong part2 (Settings) bằng Python
    part2 = part2.replace(
        '<span class="workspace-kicker">Runtime configuration</span>',
        '<span class="workspace-kicker" data-i18n="set_kicker">Runtime configuration</span>'
    )
    part2 = part2.replace(
        '<h1>System settings</h1>',
        '<h1 data-i18n="set_title">System settings</h1>'
    )
    part2 = part2.replace(
        '<p>Manage network routing and notification delivery for every workflow.</p>',
        '<p data-i18n="set_desc">Manage network routing and notification delivery for every workflow.</p>'
    )
    
    # Tìm thẻ đóng </body> và chèn thêm scripts imports của người dùng
    scripts_to_add = """<script src="/static/getacc.js?v=__ASSET_VERSION__"></script>
<script src="/static/mac_select.js?v=__ASSET_VERSION__"></script>
</body>"""
    part2 = part2.replace("</body>", scripts_to_add)
    
    # Ghép nối và ghi đè
    full_content = part1 + "\n" + part2
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    print("Success: restored index.html with all 5 tabs and i18n placeholders.")
else:
    print("Error: Could not find settings page, merge failed.")
