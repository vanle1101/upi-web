import os

css_path = r"c:\Users\lehon\OneDrive\Desktop\gpt_signup_hybrid-main\web\static\operations.css"

premium_css = """
/* ==========================================================================
   Premium Design: Outfit Font, Sidebar Layout & Dynamic Light/Dark Mode
   ========================================================================== */

/* Apply Outfit font to the entire workspace */
:root {
  --ops-sans: "Outfit", "Geist", "Segoe UI Variable", Aptos, "Segoe UI", system-ui, sans-serif;
  --ops-display: "Outfit", "Aptos Display", "Segoe UI Variable Display", "Segoe UI", system-ui, sans-serif;
}

/* Dark theme color scheme values */
body.dark-theme {
  color-scheme: dark;
  --ops-canvas: #090d16;
  --ops-canvas-strong: #0f172a;
  --ops-surface: #1e293b;
  --ops-surface-soft: #0f172a;
  --ops-surface-blue: #1e293b;
  --ops-ink: #f3f4f6;
  --ops-ink-soft: #cbd5e1;
  --ops-muted: #94a3b8;
  --ops-faint: #64748b;
  --ops-line: #334155;
  --ops-line-soft: #1e293b;
  --ops-rail: #0f172a;
  --ops-rail-soft: #1e293b;
  --ops-code: #1e293b;
  --ops-code-soft: #0f172a;
  --ops-code-text: #f3f4f6;
  --ops-code-muted: #94a3b8;
  --ops-accent: #3b82f6;
  --ops-accent-strong: #60a5fa;
  --ops-accent-soft: #1e3a8a;
  --ops-accent-faint: #172554;
  --ops-success: #10b981;
  --ops-success-soft: #064e3b;
  --ops-danger: #ef4444;
  --ops-danger-soft: #7f1d1d;
  --ops-warning: #f59e0b;
  --ops-warning-soft: #78350f;
  --ops-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1);
  --ops-shadow-raised: 0 20px 25px -5px rgba(0, 0, 0, 0.3), 0 10px 10px -5px rgba(0, 0, 0, 0.15);
}

/* Force dark mode background and border overrides for elements with hardcoded bright colors */
body.dark-theme .control-surface,
body.dark-theme .jobs-surface,
body.dark-theme .control-surface > .card-actions,
body.dark-theme .control-surface > .card-head,
body.dark-theme .control-surface > .mail-mode-row,
body.dark-theme .control-surface > .card-settings,
body.dark-theme .workflow-proxy-row,
body.dark-theme .diagnostics-dock,
body.dark-theme .dock-bar,
body.dark-theme .dock-panel {
  background: var(--ops-surface) !important;
  border-color: var(--ops-line) !important;
  color: var(--ops-ink) !important;
}

body.dark-theme .workflow-proxy-row {
  background: var(--ops-surface-soft) !important;
}

body.dark-theme .combo-textarea {
  background: var(--ops-code) !important;
  color: var(--ops-code-text) !important;
}

body.dark-theme select,
body.dark-theme input {
  background: var(--ops-surface-soft) !important;
  color: var(--ops-ink) !important;
  border-color: var(--ops-line) !important;
}

body.dark-theme .pipeline-step {
  color: var(--ops-muted);
}
body.dark-theme .pipeline-step.is-current {
  color: var(--ops-accent-strong);
}

/* Sidebar Footer & Toggle Styling */
.sidebar-footer-controls {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-top: 4px;
}

.theme-toggle-btn,
.lang-toggle-btn {
  background: var(--ops-surface-soft);
  border: 1px solid var(--ops-line);
  border-radius: var(--ops-radius-sm);
  color: var(--ops-ink-soft);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  width: 38px;
  height: 38px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: var(--ops-shadow);
}

.theme-toggle-btn::before {
  content: "☀️";
}

body.dark-theme .theme-toggle-btn::before {
  content: "🌙";
}

.theme-toggle-btn:hover,
.lang-toggle-btn:hover {
  background: var(--ops-accent-soft);
  border-color: var(--ops-accent);
  color: var(--ops-accent);
  transform: translateY(-1px);
}

.theme-toggle-btn:active,
.lang-toggle-btn:active {
  transform: translateY(0);
}

/* Desktop Sidebar & Grid Layout */
@media (min-width: 1025px) {
  body {
    grid-template-columns: 240px minmax(0, 1fr) !important;
    grid-template-rows: minmax(0, 1fr) !important;
  }

  .topbar {
    grid-column: 1 !important;
    grid-row: 1 !important;
    position: fixed !important;
    left: 0;
    top: 0;
    width: 240px !important;
    height: 100dvh !important;
    max-height: 100dvh !important;
    border-right: 1px solid var(--ops-line) !important;
    border-bottom: none !important;
    grid-template-columns: 1fr !important;
    grid-template-rows: auto 1fr auto !important;
    padding: 24px 16px !important;
    gap: 16px !important;
    box-shadow: 2px 0 18px rgba(20, 29, 25, 0.04) !important;
    background: var(--ops-rail) !important;
    overflow-y: auto;
  }

  .tab-nav {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 8px !important;
    margin: 24px 0 !important;
  }

  .tab-btn {
    width: 100% !important;
    justify-content: flex-start !important;
    padding: 10px 14px !important;
    border-radius: var(--ops-radius) !important;
    text-align: left !important;
    border: 1px solid transparent !important;
    transition: all 0.2s ease !important;
  }

  .tab-btn.active {
    background: var(--ops-accent-soft) !important;
    border-color: var(--ops-accent) !important;
    color: var(--ops-accent) !important;
  }

  .topbar-actions {
    flex-direction: column !important;
    align-items: stretch !important;
    gap: 16px !important;
    border-top: 1px solid var(--ops-line-soft) !important;
    padding-top: 16px !important;
    width: 100% !important;
  }

  .topbar-actions label {
    width: 100% !important;
  }

  /* Main Workspace adjustments when sidebar is present */
  .tab-content {
    margin-left: 0 !important;
    height: 100dvh !important;
    overflow-y: auto;
  }

  /* Two Column Bento Grid: Left rail 400px, right content 1fr */
  .workspace-grid {
    display: grid !important;
    grid-template-columns: 420px 1fr !important;
    grid-template-rows: minmax(0, 1fr) !important;
    height: calc(100dvh - 120px) !important;
    gap: 24px !important;
    padding: 0 24px 24px 24px !important;
    align-items: stretch !important;
  }

  .control-rail {
    grid-column: 1 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 20px !important;
    overflow-y: auto !important;
  }

  .execution-canvas {
    grid-column: 2 !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 20px !important;
    height: 100% !important;
    overflow: hidden !important;
  }

  .card-jobs {
    flex: 1 1 auto !important;
    overflow-y: auto !important;
  }

  .diagnostics-dock {
    flex: 0 0 auto !important;
  }

  .diagnostics-dock.is-collapsed {
    height: 48px !important;
  }
}
"""

with open(css_path, "a", encoding="utf-8") as f:
    f.write(premium_css)

print("CSS appended successfully!")
