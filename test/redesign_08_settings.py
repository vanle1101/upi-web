# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()
pairs = []

# Settings nav active: accent-tinted with left bar to match sidebar language.
pairs.append((
"""#tab-settings .settings-nav-item.active {
  color: var(--accent-hover);
  border: 0;
  background: var(--paper);
  box-shadow: 0 1px 5px rgba(61, 55, 44, 0.06);
}""",
"""#tab-settings .settings-nav-item.active {
  position: relative;
  color: var(--accent-hover);
  border: 0;
  background: var(--paper);
  box-shadow: var(--shadow-paper), inset 0 0 0 1px rgba(196, 214, 204, 0.7);
  font-weight: 580;
}

#tab-settings .settings-nav-item.active::before {
  content: "";
  position: absolute;
  top: 9px;
  bottom: 9px;
  left: 0;
  width: 3px;
  border-radius: 0 3px 3px 0;
  background: var(--accent);
}"""))

# Settings hint: brass code accent for editorial warmth.
pairs.append((
"""#tab-settings .settings-hint code {
  color: #4d685d;
  background: transparent;
}""",
"""#tab-settings .settings-hint code {
  padding: 1px 6px;
  border-radius: 5px;
  color: var(--accent-hover);
  background: var(--accent-soft);
  font-family: var(--font-mono);
  font-size: 11.5px;
}"""))

# Sidebar select / pill: lift contrast within the darker rail.
pairs.append((
""".topbar .pill {
  align-self: flex-start;
  min-width: 0;
  margin-top: 3px;
  padding: 4px 7px;
  border: 0;
  border-radius: var(--radius-sm);
  color: #cbc9c2;
  background: #41413b;
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.02em;
}""",
""".topbar .pill {
  align-self: flex-start;
  min-width: 0;
  margin-top: 4px;
  padding: 4px 9px;
  border: 0;
  border-radius: 999px;
  color: #d6d4cc;
  background: rgba(255, 255, 255, 0.07);
  box-shadow: inset 0 0 0 1px rgba(255, 255, 255, 0.06);
  font-family: var(--font-sans);
  font-size: 10px;
  font-weight: 620;
  letter-spacing: 0.02em;
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:45]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
