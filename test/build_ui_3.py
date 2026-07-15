HTML_TAB_UPI = """
                <!-- TAB: UPI -->
                <div id="tab-upi" class="tab-pane ops-workspace ops-upi">
                    <div class="bento-grid">
                        <div class="card col-span-2">
                            <h3 class="card-title" data-i18n="upi_inputs">UPI Inputs</h3>
                            <div class="input-group">
                                <label data-i18n="upi_combo">Combo Input</label>
                                <textarea id="upi-combo-input" class="styled-textarea" rows="4"></textarea>
                            </div>
                            <div class="input-group">
                                <label data-i18n="upi_session">Session Input</label>
                                <textarea id="upi-session-input" class="styled-textarea" rows="4"></textarea>
                            </div>
                            <div class="input-group">
                                <label data-i18n="upi_proxy_step">Proxy Step</label>
                                <select id="upi-proxy-from-step" class="styled-select">
                                    <option value="1">Step 1</option>
                                    <option value="2">Step 2</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label data-i18n="upi_proxy_input">Custom Proxy</label>
                                <input type="text" id="upi-proxy-input" class="styled-input">
                            </div>
                            <div class="inline-group-wrap mt-2">
                                <div class="inline-group">
                                    <label class="toggle-switch">
                                        <input type="checkbox" id="upi-proxy-toggle">
                                        <span class="slider"></span>
                                    </label>
                                    <span data-i18n="upi_use_proxy">Use Proxy</span>
                                </div>
                                <div class="inline-group">
                                    <label class="toggle-switch">
                                        <input type="checkbox" id="upi-notify-toggle">
                                        <span class="slider"></span>
                                    </label>
                                    <span data-i18n="upi_notify">Notify</span>
                                </div>
                            </div>
                        </div>
                        <div class="card">
                            <h3 class="card-title" data-i18n="upi_controls">Controls</h3>
                            <div class="input-group">
                                <label data-i18n="upi_timeout">Job Timeout (s)</label>
                                <input type="number" id="upi-job-timeout" class="styled-input" value="120">
                            </div>
                            <div class="input-group">
                                <label data-i18n="upi_retries">Approve Retries</label>
                                <input type="number" id="upi-approve-retries" class="styled-input" value="3">
                            </div>
                            <div class="button-group-vertical mt-4">
                                <button id="upi-btn-run" class="btn btn-primary" data-i18n="upi_btn_run">Get UPI QR</button>
                                <button id="upi-btn-stop-all" class="btn btn-danger" data-i18n="upi_btn_stop">Stop All</button>
                                <button id="upi-btn-retry-failed" class="btn btn-secondary" data-i18n="upi_btn_retry_failed">Retry Failed</button>
                                <button id="upi-btn-retry-expired-free" class="btn btn-secondary" data-i18n="upi_btn_retry_exp">Retry Exp/Free</button>
                                <button id="upi-btn-clear-input" class="btn btn-ghost" data-i18n="upi_btn_clear_input">Clear Input</button>
                            </div>
                        </div>
                        <div class="card col-span-3">
                            <div class="card-header-actions">
                                <h3 class="card-title" data-i18n="upi_output">Output & Logs</h3>
                                <div class="action-buttons">
                                    <button id="upi-btn-clear-done" class="btn btn-sm btn-ghost" data-i18n="upi_btn_clear_done">Clear Done</button>
                                    <button id="upi-btn-clear-all" class="btn btn-sm btn-ghost" data-i18n="upi_btn_clear_all">Clear All</button>
                                    <button id="upi-btn-copy-success" class="btn btn-sm btn-outline" data-i18n="upi_btn_copy_success">Copy Success</button>
                                    <button id="upi-btn-copy-error" class="btn btn-sm btn-outline" data-i18n="upi_btn_copy_error">Copy Error</button>
                                </div>
                            </div>
                            <div class="log-viewer">
                                <div class="log-content" id="upi-log-content"></div>
                            </div>
                        </div>
                    </div>
                </div>
"""

HTML_TAB_GETACC = """
                <!-- TAB: GETACC -->
                <div id="tab-getacc" class="tab-pane ops-workspace ops-getacc">
                    <div class="bento-grid">
                        <div class="card col-span-2">
                            <h3 class="card-title" data-i18n="getacc_inputs">Get Account Data</h3>
                            <div class="input-group">
                                <label data-i18n="getacc_json">JSON Input</label>
                                <textarea id="getacc-json-input" class="styled-textarea" rows="10" placeholder="Paste JSON here..."></textarea>
                            </div>
                        </div>
                        <div class="card">
                            <h3 class="card-title" data-i18n="getacc_controls">Controls</h3>
                            <div class="button-group-vertical">
                                <button id="getacc-extract-btn" class="btn btn-primary" data-i18n="getacc_btn_extract">Extract Credentials</button>
                                <button id="getacc-btn-clear-all" class="btn btn-danger" data-i18n="getacc_btn_clear">Clear All</button>
                            </div>
                        </div>
                    </div>
                </div>
"""

with open("test/build_ui_3.py", "w", encoding="utf-8") as f:
    f.write(f"HTML_TAB_UPI = {repr(HTML_TAB_UPI)}\n")
    f.write(f"HTML_TAB_GETACC = {repr(HTML_TAB_GETACC)}\n")
