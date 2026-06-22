# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()
pairs = []

# Kicker: brass editorial micro-label (sparing use of secondary accent).
pairs.append((
""".workspace-kicker {
  display: block;
  margin-bottom: 6px;
  color: var(--accent);
  font-size: 11px;
  font-weight: 620;
  letter-spacing: 0.025em;
  text-transform: none;
}""",
""".workspace-kicker {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 9px;
  color: var(--brass);
  font-size: 11px;
  font-weight: 640;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.workspace-kicker::before {
  content: "";
  width: 14px;
  height: 1.5px;
  border-radius: 2px;
  background: var(--brass);
  opacity: 0.7;
}"""))

# Title scale a touch larger + tighter.
pairs.append((
""".workspace-title-group h1 {
  margin: 0;
  color: var(--ink);
  font-size: clamp(25px, 2vw, 32px);
  font-weight: 640;
  line-height: 1.08;
  letter-spacing: -0.027em;
  text-wrap: balance;
}""",
""".workspace-title-group h1 {
  margin: 0;
  color: var(--ink);
  font-size: clamp(26px, 2.1vw, 33px);
  font-weight: 660;
  line-height: 1.06;
  letter-spacing: -0.03em;
  text-wrap: balance;
}"""))

# Pipeline strip: give it a real card-chip presence (paper + hairline + soft shadow).
pairs.append((
""".pipeline-strip {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  min-width: 350px;
  padding: 7px 11px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.52);
}""",
""".pipeline-strip {
  display: flex;
  align-items: center;
  flex: 0 0 auto;
  min-width: 350px;
  padding: 9px 16px;
  border-radius: 999px;
  background: var(--paper);
  box-shadow: 0 1px 2px rgba(40, 43, 34, 0.05), inset 0 0 0 1px rgba(216, 212, 200, 0.6);
}"""))

# Pipeline step: completed dot uses a softer brass-free eucalyptus, current gets a ring.
pairs.append((
""".pipeline-step.is-current::before {
  border-color: var(--accent);
  background: var(--accent);
  box-shadow: none;
}""",
""".pipeline-step.is-current::before {
  border-color: var(--accent);
  background: var(--accent);
  box-shadow: 0 0 0 3px rgba(70, 104, 89, 0.16);
}"""))

# Card surface: crisp paper with a faint hairline ring for definition + lift.
pairs.append((
""".card,
.settings-sidebar,
.modal-content {
  border: 0;
  border-radius: var(--radius-lg);
  color: var(--ink);
  background: var(--paper);
  box-shadow: var(--shadow-paper);
  backdrop-filter: none;
}""",
""".card,
.settings-sidebar,
.modal-content {
  border: 0;
  border-radius: var(--radius-lg);
  color: var(--ink);
  background: var(--paper);
  box-shadow: var(--shadow-paper), inset 0 0 0 1px rgba(216, 212, 200, 0.5);
  backdrop-filter: none;
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:45]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
