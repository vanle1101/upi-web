(() => {
  "use strict";

  // â”€â”€â”€ i18n Dictionary â”€â”€â”€
  const LANG_DICT = {
    vi: {
      "brand_tag": "Operations Desk",
      "nav_reg_title": "Reg",
      "nav_reg_desc": "Cấp phát tài khoản",
      "nav_session_title": "Get Session",
      "nav_session_desc": "Khôi phục phiên",
      "nav_upi_title": "UPI QR",
      "nav_upi_desc": "Phát hành QR",
      "nav_getacc_title": "Get Acc",
      "nav_getacc_desc": "Trích xuất acc",
      "nav_settings_title": "Settings",
      "nav_settings_desc": "Cấu hình hệ thống",
      "runtime_label": "Headless",
      "debug_label": "Debug",
      "headless_title": "Bật để ẩn cửa sổ trình duyệt khi chạy",
      "debug_title": "Giữ browser mở sau khi job xong (chỉ khi không headless)",
      "runtime_section": "Runtime",

      "reg_kicker": "Cấp phát tài khoản",
      "reg_title": "Registration Desk",
      "reg_desc": "Chuẩn bị danh tính, giám sát trình duyệt và duyệt kết quả MFA từ một hàng đợi.",
      "reg_source_accounts": "Tài khoản nguồn",
      "reg_input_hint": "Mỗi dòng một combo: email|password|refresh_token|client_id",
      "reg_mail_mode": "Mail mode",
      "reg_reg_mode": "Reg mode",
      "reg_default_password": "Mật khẩu mặc định",
      "reg_timeout": "Timeout (s/job)",
      "reg_use_proxy": "Use proxy",
      "reg_start": "Start registration",
      "reg_stop": "Stop All",
      "reg_clear": "Clear Input",
      "reg_queue_title": "Execution queue",
      "reg_queue_desc": "Hoạt động đăng ký tài khoản trực tiếp",
      "reg_retry_failed": "Retry Failed",
      "reg_clear_done": "Clear Done",
      "reg_clear_all": "Clear All",
      "reg_no_jobs": "Chưa có job. Dán combo và bấm Start registration.",
      "reg_tab_runtime": "Runtime",
      "reg_tab_success": "Success",
      "reg_tab_errors": "Errors",
      "reg_success_head": "Completed account output",
      "reg_error_head": "Failed account output",

      "ses_kicker": "Khôi phục phiên",
      "ses_title": "Session capture",
      "ses_desc": "Đăng nhập tài khoản để lấy session payload hiện tại kèm log theo từng job.",
      "ses_credentials": "Credentials",
      "ses_start": "Get Session",
      "ses_queue_title": "Session queue",
      "ses_queue_desc": "Trạng thái đăng nhập và lưu phiên",
      "ses_no_jobs": "Dán combo và bấm Get Session.",
      "ses_errors_head": "Session capture failures",

      "upi_kicker": "Payment operations",
      "upi_title": "UPI QR Issuance",
      "upi_desc": "Tạo, giám sát và khôi phục job QR payment trong cùng một hàng đợi.",
      "upi_identities": "Payment identities",
      "upi_start": "Get UPI QR",
      "upi_queue_title": "Payment queue",
      "upi_queue_desc": "Trạng thái checkout, approve và QR",
      "upi_retry_expired": "Retry Expired+Free",
      "upi_no_jobs": "Dán account và bấm Get UPI QR.",
      "upi_output_head": "Generated payment output",
      "upi_errors_head": "Payment workflow failures",
      "upi_telegram": "Send Telegram",

      "acc_kicker": "Trích xuất dữ liệu",
      "acc_title": "Get Account",
      "acc_desc": "Dán JSON session ChatGPT để tách email, password và mã 2FA.",
      "acc_json": "JSON Payload",
      "acc_start": "Extract Credentials",
      "acc_queue_title": "Extraction queue",
      "acc_queue_desc": "Cookie và thông tin tài khoản đã lấy",
      "acc_no_jobs": "Chưa có dữ liệu. Dán JSON vào ô bên trái để bắt đầu.",

      "set_kicker": "Runtime configuration",
      "set_title": "System settings",
      "set_desc": "Quản lý thông báo và cấu hình vận hành chính cho @lhv_myhanh.",

      "copy_all": "Copy all",
      "clear_log": "Clear log",
      "show_details": "Show details",
      "hide_details": "Hide details"
    },
    en: {
      "brand_tag": "Operations Desk",
      "nav_reg_title": "Reg",
      "nav_reg_desc": "Provision accounts",
      "nav_session_title": "Get Session",
      "nav_session_desc": "Capture auth state",
      "nav_upi_title": "UPI QR",
      "nav_upi_desc": "Payment issuance",
      "nav_getacc_title": "Get Acc",
      "nav_getacc_desc": "Extract credentials",
      "nav_settings_title": "Settings",
      "nav_settings_desc": "Runtime controls",
      "runtime_label": "Headless",
      "debug_label": "Debug",
      "headless_title": "Run browser in background (no GUI)",
      "debug_title": "Keep browser open after job finishes (headed only)",
      "runtime_section": "Runtime",

      "reg_kicker": "Account provisioning",
      "reg_title": "Registration Desk",
      "reg_desc": "Prepare identities, monitor browser work and review MFA results from one queue.",
      "reg_source_accounts": "Source accounts",
      "reg_input_hint": "One combo per line: email|password|refresh_token|client_id",
      "reg_mail_mode": "Mail Mode",
      "reg_reg_mode": "Reg Mode",
      "reg_default_password": "Default password",
      "reg_timeout": "Timeout (s/job)",
      "reg_use_proxy": "Use Proxy",
      "reg_start": "Start registration",
      "reg_stop": "Stop All",
      "reg_clear": "Clear Input",
      "reg_queue_title": "Execution queue",
      "reg_queue_desc": "Live registration activity",
      "reg_retry_failed": "Retry Failed",
      "reg_clear_done": "Clear Done",
      "reg_clear_all": "Clear All",
      "reg_no_jobs": "No jobs yet. Paste combos and click Run.",
      "reg_tab_runtime": "Runtime",
      "reg_tab_success": "Success",
      "reg_tab_errors": "Errors",
      "reg_success_head": "Completed account output",
      "reg_error_head": "Failed account output",

      "ses_kicker": "Authentication recovery",
      "ses_title": "Session capture",
      "ses_desc": "Resolve account credentials into current session payloads with visible job-level diagnostics.",
      "ses_credentials": "Credentials",
      "ses_start": "Get Session",
      "ses_queue_title": "Session queue",
      "ses_queue_desc": "Authentication and capture status",
      "ses_no_jobs": "Paste combos and click Get Session.",
      "ses_errors_head": "Session capture failures",

      "upi_kicker": "Payment operations",
      "upi_title": "UPI QR Issuance",
      "upi_desc": "Generate, monitor and recover QR payment jobs without leaving the active queue.",
      "upi_identities": "Payment identities",
      "upi_start": "Get UPI QR",
      "upi_queue_title": "Payment queue",
      "upi_queue_desc": "Checkout, approval and QR status",
      "upi_retry_expired": "Retry Expired+Free",
      "upi_no_jobs": "Paste accounts and click Get UPI QR.",
      "upi_output_head": "Generated payment output",
      "upi_errors_head": "Payment workflow failures",
      "upi_telegram": "Send Telegram",

      "acc_kicker": "Data extraction",
      "acc_title": "Get Account",
      "acc_desc": "Paste a ChatGPT session JSON to extract the account's email, password, and 2FA secret.",
      "acc_json": "JSON Payload",
      "acc_start": "Extract Credentials",
      "acc_queue_title": "Extraction queue",
      "acc_queue_desc": "Extracted cookies & credentials",
      "acc_no_jobs": "No data yet. Paste JSON into the input box to begin.",

      "set_kicker": "Runtime configuration",
      "set_title": "System settings",
      "set_desc": "Manage notification delivery for active workflows.",

      "copy_all": "Copy all",
      "clear_log": "Clear log",
      "show_details": "Show details",
      "hide_details": "Hide details"
    }
  };

  // â”€â”€â”€ Language Translation Logic â”€â”€â”€
  function updateLanguage(lang) {
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (LANG_DICT[lang] && LANG_DICT[lang][key]) {
        // Äá»‘i vá»›i cÃ¡c button hoáº·c tag chá»©a icon, ta cáº§n giá»¯ láº¡i icon hoáº·c bá»c text phÃ¹ há»£p
        const strong = el.querySelector('strong');
        const small = el.querySelector('small');
        if (strong && small) {
          // tab navigation buttons
          const tabKeyTitle = `nav_${key}_title`;
          const tabKeyDesc = `nav_${key}_desc`;
          if (LANG_DICT[lang][tabKeyTitle]) strong.textContent = LANG_DICT[lang][tabKeyTitle];
          if (LANG_DICT[lang][tabKeyDesc]) small.textContent = LANG_DICT[lang][tabKeyDesc];
        } else {
          el.textContent = LANG_DICT[lang][key];
        }
      }
    });

    document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
      const key = el.getAttribute('data-i18n-placeholder');
      if (LANG_DICT[lang] && LANG_DICT[lang][key]) {
        el.setAttribute('placeholder', LANG_DICT[lang][key]);
      }
    });

    document.querySelectorAll('[data-i18n-title]').forEach((el) => {
      const key = el.getAttribute('data-i18n-title');
      if (LANG_DICT[lang] && LANG_DICT[lang][key]) {
        el.setAttribute('title', LANG_DICT[lang][key]);
      }
    });

    localStorage.setItem('gpt_console.lang', lang);
    document.documentElement.setAttribute('lang', lang);

    // Update language select ui if any
    const langBtn = document.getElementById('lang-toggle-btn');
    if (langBtn) {
      langBtn.textContent = lang === 'vi' ? 'EN' : 'VI';
    }
  }

  // â”€â”€â”€ Theme Toggling Logic â”€â”€â”€
  function updateTheme(theme) {
    const isDark = theme === 'dark';
    document.body.classList.toggle('dark-theme', isDark);
    localStorage.setItem('gpt_console.theme', theme);

    // Update toggle icon state
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
      themeBtn.innerHTML = isDark
        ? `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>` // Sun icon
        : `<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`; // Moon icon
    }
  }

  // Initialize theme and language on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    // Theme setup
    const savedTheme = localStorage.getItem('gpt_console.theme') || 'dark';
    updateTheme(savedTheme);

    // Language setup
    const savedLang = localStorage.getItem('gpt_console.lang') || 'vi';
    updateLanguage(savedLang);

    // Bind event listeners
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
      themeBtn.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('gpt_console.theme') || 'dark';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        updateTheme(nextTheme);
      });
    }

    const langBtn = document.getElementById('lang-toggle-btn');
    if (langBtn) {
      langBtn.addEventListener('click', () => {
        const currentLang = localStorage.getItem('gpt_console.lang') || 'vi';
        const nextLang = currentLang === 'vi' ? 'en' : 'vi';
        updateLanguage(nextLang);
      });
    }
  });


  // â”€â”€â”€ Existing Diagnostics Dock Logic â”€â”€â”€
  function activateDockPanel(dock, target) {
    const tabs = Array.from(dock.querySelectorAll("[data-dock-target]"));
    const panels = Array.from(dock.querySelectorAll("[data-dock-panel]"));
    let matched = false;

    tabs.forEach((tab) => {
      const active = tab.dataset.dockTarget === target;
      tab.classList.toggle("active", active);
      tab.setAttribute("aria-selected", active ? "true" : "false");
      tab.tabIndex = active ? 0 : -1;
      if (active) {
        matched = true;
        tab.classList.remove("has-unseen"); // da mo xem -> tat cham xanh
      }
    });

    panels.forEach((panel) => {
      const active = panel.dataset.dockPanel === target;
      panel.hidden = !active;
      panel.classList.toggle("active", active);
    });

    return matched;
  }

  function setDockCollapsed(dock, collapsed) {
    const button = dock.querySelector("[data-dock-collapse]");
    dock.classList.toggle("is-collapsed", collapsed);
    if (!button) return;
    button.setAttribute("aria-expanded", collapsed ? "false" : "true");

    const currentLang = localStorage.getItem('gpt_console.lang') || 'vi';
    if (collapsed) {
      button.textContent = currentLang === 'vi' ? 'Show details' : 'Show details';
      button.setAttribute('data-i18n', 'show_details');
    } else {
      button.textContent = currentLang === 'vi' ? 'Hide details' : 'Hide details';
      button.setAttribute('data-i18n', 'hide_details');
    }
  }

  function hasMeaningfulOutput(panel) {
    const output = panel.querySelector(".output-pane") || panel;
    const text = (output.textContent || "").trim();
    if (!text) return false;
    return !text.startsWith("No errors yet") && !text.startsWith("Format:");
  }

  function observeDockOutput(dock) {
    dock.querySelectorAll("[data-dock-panel]").forEach((panel) => {
      const target = panel.dataset.dockPanel;
      const tab = dock.querySelector(`[data-dock-target="${target}"]`);
      if (!tab || target.endsWith("-log")) return;

      const update = () => {
        const hasContent = hasMeaningfulOutput(panel);
        tab.classList.toggle("has-content", hasContent);
        // Cháº¥m xanh "chÆ°a xem": chá»‰ hiá»‡n khi cÃ³ content VÃ€ tab Ä‘ang khÃ´ng Ä‘Æ°á»£c
        // má»Ÿ. Tab Ä‘ang active -> coi nhÆ° Ä‘Ã£ xem ngay, khÃ´ng bÃ¡o "unseen".
        if (!hasContent) {
          tab.classList.remove("has-unseen");
        } else if (!tab.classList.contains("active")) {
          tab.classList.add("has-unseen");
        }
      };
      update();
      new MutationObserver(update).observe(panel, {
        childList: true,
        characterData: true,
        subtree: true,
      });
    });
  }

  function initDock(dock) {
    const tabs = Array.from(dock.querySelectorAll("[data-dock-target]"));
    if (!tabs.length) return;

    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => {
        setDockCollapsed(dock, false);
        activateDockPanel(dock, tab.dataset.dockTarget);
      });
      tab.addEventListener("keydown", (event) => {
        if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
        event.preventDefault();
        const offset = event.key === "ArrowRight" ? 1 : -1;
        const next = tabs[(index + offset + tabs.length) % tabs.length];
        activateDockPanel(dock, next.dataset.dockTarget);
        next.focus();
      });
    });

    const initial = tabs.find((tab) => tab.classList.contains("active")) || tabs[0];
    activateDockPanel(dock, initial.dataset.dockTarget);
    const collapseButton = dock.querySelector("[data-dock-collapse]");
    if (collapseButton) {
      collapseButton.addEventListener("click", () => {
        setDockCollapsed(dock, !dock.classList.contains("is-collapsed"));
      });
    }
    setDockCollapsed(dock, dock.classList.contains("is-collapsed"));
    observeDockOutput(dock);
  }

  document.querySelectorAll("[data-dock]").forEach(initDock);
})();

// --- UI Layout & Theme Logic (Appended) ---
document.addEventListener('DOMContentLoaded', () => {
    // Theme logic
    const themeBtn = document.getElementById('theme-toggle');
    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            document.body.classList.toggle('dark-theme');
            localStorage.setItem('theme', document.body.classList.contains('dark-theme') ? 'dark' : 'light');
        });

        if (localStorage.getItem('theme') === 'light') {
            document.body.classList.remove('dark-theme');
        } else {
            document.body.classList.add('dark-theme');
        }
    }

    // Sidebar Tabs logic
    const navItems = document.querySelectorAll('.sidebar-nav .nav-item');
    const tabPanes = document.querySelectorAll('.content-area .tab-pane');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(n => n.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));

            item.classList.add('active');
            const targetId = item.getAttribute('data-tab');
            const targetPane = document.getElementById(targetId);
            if(targetPane) {
                targetPane.classList.add('active');
            }
        });
    });

    // Mobile Sidebar toggle
    const mobileBtn = document.getElementById('mobile-menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (mobileBtn && sidebar) {
        mobileBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }
});
