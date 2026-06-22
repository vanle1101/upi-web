# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()

OLD_ROOT = """:root {
  color-scheme: light;
  --page: #f1efe9;
  --paper: #fbfaf7;
  --paper-soft: #f6f4ee;
  --paper-strong: #ffffff;
  --ink: #252722;
  --ink-soft: #4f544e;
  --muted: #747971;
  --faint: #9a9e97;
  --line: #dedbd2;
  --line-soft: #e9e6de;
  --rail: #34342f;
  --rail-soft: #3c3c36;
  --rail-line: #4a4943;
  --accent: #4f7565;
  --accent-hover: #3f6354;
  --accent-soft: #e2ebe6;
  --danger: #a85f60;
  --danger-soft: #f4e7e5;
  --success: #4f7759;
  --warning: #9a7138;
  --focus: 0 0 0 3px rgba(79, 117, 101, 0.18);
  --shadow-paper: 0 1px 2px rgba(59, 53, 43, 0.05), 0 12px 32px rgba(59, 53, 43, 0.055);
  --radius-lg: 12px;
  --radius-md: 8px;
  --radius-sm: 6px;
  --sidebar-width: 226px;
  --font-sans: "Geist", "Segoe UI Variable", "Aptos", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "Geist Mono", "Cascadia Code", "JetBrains Mono", Consolas, monospace;
  --bg: var(--page);
  --bg-elev: var(--paper);
  --bg-elev-2: var(--paper-soft);
  --bg-soft: var(--paper-soft);
  --border: var(--line);
  --border-strong: #c9c5bb;
  --fg: var(--ink);
  --fg-mute: var(--muted);
  --fg-dim: var(--faint);
  --green: var(--success);
  --red: var(--danger);
  --yellow: var(--warning);
  --blue: var(--accent);
  --focus-ring: var(--focus);
}"""

NEW_ROOT = """:root {
  color-scheme: light;

  /* Surfaces: warm stone page, clearly lighter ivory/paper cards so they lift. */
  --page: #e7e4db;
  --page-deep: #e1ddd2;
  --paper: #fcfbf7;
  --paper-soft: #f3f0e8;
  --paper-strong: #ffffff;

  /* Ink: rich warm charcoal, never pure black. */
  --ink: #23261f;
  --ink-soft: #4b504848;
  --ink-soft: #4b5048;
  --muted: #6e736a;
  --faint: #9a9e95;

  /* Hairlines: warm, low contrast. */
  --line: #d8d4c8;
  --line-soft: #e6e1d6;

  /* Sidebar: deep olive charcoal with a clearly lighter active fill. */
  --rail: #2a2d28;
  --rail-soft: #383c34;
  --rail-line: #43463e;
  --rail-fg: #f3f1ea;
  --rail-fg-mute: #b4b3aa;
  --rail-fg-faint: #8f8e85;

  /* Primary: deep eucalyptus / forest green. */
  --accent: #466859;
  --accent-hover: #395848;
  --accent-soft: #dde8e1;
  --accent-line: #c4d6cc;

  /* Secondary: muted brass, used sparingly for editorial accents. */
  --brass: #9a7937;
  --brass-soft: #efe6d3;

  /* Status: terracotta danger, eucalyptus success, restrained amber. */
  --danger: #a55a52;
  --danger-soft: #f2e3df;
  --success: #4c7457;
  --success-soft: #dfeae0;
  --warning: #8d6c2e;
  --warning-soft: #f1e8d3;

  --focus: 0 0 0 3px rgba(70, 104, 89, 0.20);
  --shadow-paper: 0 1px 2px rgba(40, 43, 34, 0.045), 0 10px 28px rgba(40, 43, 34, 0.06);
  --shadow-pop: 0 2px 6px rgba(40, 43, 34, 0.06), 0 20px 46px rgba(40, 43, 34, 0.10);

  --radius-lg: 13px;
  --radius-md: 9px;
  --radius-sm: 6px;

  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 22px;
  --space-6: 30px;

  --sidebar-width: 232px;
  --font-sans: "Geist", "Segoe UI Variable", "Aptos", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: "Geist Mono", "Cascadia Code", "JetBrains Mono", Consolas, monospace;

  /* Legacy aliases consumed by style.css component rules. */
  --bg: var(--page);
  --bg-elev: var(--paper);
  --bg-elev-2: var(--paper-soft);
  --bg-soft: var(--paper-soft);
  --border: var(--line);
  --border-strong: #c8c3b6;
  --fg: var(--ink);
  --fg-mute: var(--muted);
  --fg-dim: var(--faint);
  --green: var(--success);
  --red: var(--danger);
  --yellow: var(--warning);
  --blue: var(--accent);
  --focus-ring: var(--focus);
}"""

if OLD_ROOT not in s:
    raise SystemExit("ROOT ANCHOR NOT FOUND")
s = s.replace(OLD_ROOT, NEW_ROOT, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("ROOT replaced")
