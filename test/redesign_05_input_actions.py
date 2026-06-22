# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()
pairs = []

# Raw input textarea: contained code zone with inset depth + ruled feel.
pairs.append((
""".combo-textarea {
  padding: 15px 16px;
  border: 0;
  color: #40443f;
  background: #f5f3ed;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.65;
  caret-color: var(--accent);
}""",
""".combo-textarea {
  padding: 16px 18px;
  border: 0;
  color: #3a3e38;
  background:
    linear-gradient(180deg, #f6f3eb 0%, #f1ede3 100%);
  box-shadow: inset 0 1px 3px rgba(40, 43, 34, 0.05);
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.7;
  white-space: pre;
  overflow: auto;
  tab-size: 2;
  caret-color: var(--accent);
}"""))

# Primary button: deep eucalyptus with subtle top highlight for premium feel.
pairs.append((
""".btn-primary {
  color: #fff;
  border-color: var(--accent);
  background: var(--accent);
  box-shadow: 0 3px 8px rgba(79, 117, 101, 0.15);
}

.btn-primary:hover {
  color: #fff;
  border-color: var(--accent-hover);
  background: var(--accent-hover);
  box-shadow: 0 4px 11px rgba(79, 117, 101, 0.18);
}""",
""".btn-primary {
  color: #fbfdfb;
  border-color: transparent;
  background: linear-gradient(180deg, #4f7263 0%, var(--accent) 100%);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.14) inset,
    0 4px 12px rgba(53, 84, 70, 0.22);
}

.btn-primary:hover {
  color: #fff;
  border-color: transparent;
  background: linear-gradient(180deg, #466a5a 0%, var(--accent-hover) 100%);
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.16) inset,
    0 6px 16px rgba(53, 84, 70, 0.26);
}

.btn-primary:active {
  box-shadow: 0 2px 7px rgba(53, 84, 70, 0.24);
}"""))

# Count / helper text alignment in actions row -> tabular, muted.
pairs.append((
""".card-actions .muted {
  margin-left: auto;
  font-family: var(--font-sans);
  font-size: 11.5px;
}""",
""".card-actions .muted {
  margin-left: auto;
  color: var(--faint);
  font-family: var(--font-sans);
  font-size: 11.5px;
  font-variant-numeric: tabular-nums;
}"""))

# Inputs: warm paper-white fields, slightly stronger focus.
pairs.append((
"""  height: 36px;
  border: 1px solid #d6d2c8;
  border-radius: var(--radius-sm);
  color: var(--ink);
  background: #fffefa;
  box-shadow: inset 0 1px 1px rgba(64, 57, 47, 0.03);
  font-family: var(--font-sans);
  font-size: 12.5px;
}""",
"""  height: 36px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  color: var(--ink);
  background: var(--paper-strong);
  box-shadow: inset 0 1px 2px rgba(40, 43, 34, 0.035);
  font-family: var(--font-sans);
  font-size: 12.5px;
  transition: border-color 150ms ease, box-shadow 150ms ease;
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:45]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
