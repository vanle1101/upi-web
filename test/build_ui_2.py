HTML_TAB_REG = """
                <!-- TAB: REGISTRATION -->
                <div id="tab-reg" class="tab-pane active ops-workspace ops-reg">
                    <div class="bento-grid">
                        <div class="card col-span-2">
                            <h3 class="card-title" data-i18n="reg_inputs">Inputs & Config</h3>
                            <div class="input-group">
                                <label data-i18n="reg_mail_mode">Mail Mode</label>
                                <select id="mail-mode-select" class="styled-select">
                                    <option value="pop3">POP3 (Standard)</option>
                                    <option value="alias">Alias (Catch-all)</option>
                                    <option value="domain">Domain (Custom)</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label data-i18n="reg_mode">Reg Mode</label>
                                <select id="reg-mode-select" class="styled-select">
                                    <option value="api">API Registration</option>
                                    <option value="web">Web Automation</option>
                                </select>
                            </div>
                            <div class="input-group">
                                <label data-i18n="reg_combo">Combo (Email:Password)</label>
                                <textarea id="combo-input" class="styled-textarea" rows="4" placeholder="email:pass..."></textarea>
                            </div>
                            <div class="input-group">
                                <label data-i18n="reg_default_pass">Default Password (if blank)</label>
                                <input type="text" id="default-password" class="styled-input" placeholder="Password123!">
                            </div>
                            <div class="inline-group">
                                <label class="toggle-switch">
                                    <input type="checkbox" id="proxy-toggle" checked>
                                    <span class="slider"></span>
                                </label>
                                <span data-i18n="reg_use_proxy">Use Proxy</span>
                            </div>
                        </div>

                        <div class="card">
                            <h3 class="card-title" data-i18n="reg_controls">Controls</h3>
                            <div class="input-group">
                                <label data-i18n="reg_timeout">Job Timeout (s)</label>
                                <input type="number" id="job-timeout" class="styled-input" value="60">
                            </div>
                            <div class="input-group">
                                <label data-i18n="reg_retry_max">Auto Retry Max</label>
                                <input type="number" id="auto-retry-max" class="styled-input" value="3">
                            </div>
                            <div class="button-group-vertical mt-4">
                                <button id="btn-run" class="btn btn-primary" data-i18n="reg_btn_run">Start Registration</button>
                                <button id="btn-stop-all" class="btn btn-danger" data-i18n="reg_btn_stop">Stop All</button>
                                <button id="btn-retry-failed" class="btn btn-secondary" data-i18n="reg_btn_retry">Retry Failed</button>
                                <button id="btn-clear-input" class="btn btn-ghost" data-i18n="reg_btn_clear_input">Clear Input</button>
                            </div>
                        </div>

                        <div class="card col-span-3">
                            <div class="card-header-actions">
                                <h3 class="card-title" data-i18n="reg_output">Output & Logs</h3>
                                <div class="action-buttons">
                                    <button id="btn-clear-done" class="btn btn-sm btn-ghost" data-i18n="reg_btn_clear_done">Clear Done</button>
                                    <button id="btn-clear-all" class="btn btn-sm btn-ghost" data-i18n="reg_btn_clear_all">Clear All</button>
                                    <button id="btn-clear-log" class="btn btn-sm btn-ghost" data-i18n="reg_btn_clear_log">Clear Log</button>
                                    <button id="btn-copy-success" class="btn btn-sm btn-outline" data-i18n="reg_btn_copy_success">Copy Success</button>
                                    <button id="btn-copy-error" class="btn btn-sm btn-outline" data-i18n="reg_btn_copy_error">Copy Error</button>
                                </div>
                            </div>
                            <div class="log-viewer">
                                <!-- Log Output Area Placeholder -->
                                <div class="log-content" id="reg-log-content"></div>
                            </div>
                        </div>
                    </div>
                </div>
"""

HTML_TAB_SESSION = """
                <!-- TAB: SESSION -->
                <div id="tab-session" class="tab-pane ops-workspace ops-session">
                    <div class="bento-grid">
                        <div class="card col-span-2">
                            <h3 class="card-title" data-i18n="ses_inputs">Session Inputs</h3>
                            <div class="input-group">
                                <label data-i18n="ses_combo">Combo (Email:Password)</label>
                                <textarea id="ses-combo-input" class="styled-textarea" rows="6" placeholder="email:pass..."></textarea>
                            </div>
                            <div class="input-group">
                                <label data-i18n="ses_timeout">Job Timeout (s)</label>
                                <input type="number" id="ses-job-timeout" class="styled-input" value="60">
                            </div>
                        </div>
                        <div class="card">
                            <h3 class="card-title" data-i18n="ses_controls">Controls</h3>
                            <div class="button-group-vertical">
                                <button id="ses-btn-run" class="btn btn-primary" data-i18n="ses_btn_run">Get Session</button>
                                <button id="ses-btn-stop-all" class="btn btn-danger" data-i18n="ses_btn_stop">Stop All</button>
                                <button id="ses-btn-clear-input" class="btn btn-ghost" data-i18n="ses_btn_clear_input">Clear Input</button>
                                <button id="ses-btn-clear-done" class="btn btn-ghost" data-i18n="ses_btn_clear_done">Clear Done</button>
                            </div>
                        </div>
                        <div class="card col-span-3">
                            <div class="card-header-actions">
                                <h3 class="card-title" data-i18n="ses_output">Output & Logs</h3>
                                <div class="action-buttons">
                                    <button id="ses-btn-clear-log" class="btn btn-sm btn-ghost" data-i18n="ses_btn_clear_log">Clear Log</button>
                                    <button id="ses-btn-copy-error" class="btn btn-sm btn-outline" data-i18n="ses_btn_copy_error">Copy Error</button>
                                </div>
                            </div>
                            <div class="log-viewer">
                                <div class="log-content" id="ses-log-content"></div>
                            </div>
                        </div>
                    </div>
                </div>
"""

with open("test/build_ui_2.py", "w", encoding="utf-8") as f:
    f.write(f"HTML_TAB_REG = {repr(HTML_TAB_REG)}\n")
    f.write(f"HTML_TAB_SESSION = {repr(HTML_TAB_SESSION)}\n")
