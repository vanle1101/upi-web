# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()
pairs = []

# Drawer: clearer inspector identity (paper + ring), slightly taller default.
pairs.append((
""".diagnostics-dock {
  display: flex;
  flex-direction: column;
  height: 210px;
  min-width: 0;
  min-height: 0;
  border: 0;
  border-radius: var(--radius-lg);
  background: var(--paper);
  box-shadow: var(--shadow-paper);
  overflow: hidden;
  transition: height 190ms ease;
}""",
""".diagnostics-dock {
  display: flex;
  flex-direction: column;
  height: 216px;
  min-width: 0;
  min-height: 0;
  border: 0;
  border-radius: var(--radius-lg);
  background: var(--paper);
  box-shadow: var(--shadow-paper), inset 0 0 0 1px rgba(216, 212, 200, 0.5);
  overflow: hidden;
  transition: height 190ms ease;
}"""))

# Dock bar: subtle tinted header so it reads as an inspector, not a footer.
pairs.append((
""".dock-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 46px;
  padding: 0 9px 0 13px;
  gap: 12px;
  border: 0;
  background: var(--paper);
}""",
""".dock-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 48px;
  padding: 0 10px 0 15px;
  gap: 12px;
  border: 0;
  background: linear-gradient(180deg, var(--paper) 0%, var(--paper-soft) 100%);
}"""))

# Dock tab active underline a bit thicker + rounded.
pairs.append((
""".dock-tab::after {
  content: "";
  position: absolute;
  right: 9px;
  bottom: 0;
  left: 9px;
  height: 2px;
  background: transparent;
}""",
""".dock-tab::after {
  content: "";
  position: absolute;
  right: 9px;
  bottom: 0;
  left: 9px;
  height: 2.5px;
  border-radius: 2px 2px 0 0;
  background: transparent;
}"""))

# Raw log / output panes: quiet contained zone, gentle ruled background.
pairs.append((
""".log-pane,
.output-pane {
  padding: 13px 15px;
  color: #4e534e;
  background: #f6f4ef;
  font-family: var(--font-mono);
  font-size: 11.5px;
  line-height: 1.65;
}""",
""".log-pane,
.output-pane {
  padding: 14px 16px;
  color: #4c514b;
  background:
    linear-gradient(180deg, #f5f2ea 0%, #f1ede4 100%);
  font-family: var(--font-mono);
  font-size: 11.5px;
  line-height: 1.7;
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:45]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
