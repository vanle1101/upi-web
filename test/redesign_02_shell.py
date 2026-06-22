# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()

pairs = []

# Body background: subtle warm stone wash (top slightly lighter) for depth.
pairs.append((
"""body {
  display: grid;
  grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
  grid-template-rows: 100dvh;
  height: 100dvh;
  overflow: hidden;
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.45;
}""",
"""body {
  display: grid;
  grid-template-columns: var(--sidebar-width) minmax(0, 1fr);
  grid-template-rows: 100dvh;
  height: 100dvh;
  overflow: hidden;
  font-family: var(--font-sans);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
  text-rendering: optimizeLegibility;
  font-feature-settings: "ss01", "cv01", "cv11";
}"""))

# Page surface gradient (warm stone, gently deeper toward the bottom).
pairs.append((
""".ops-workspace,
.settings-page {
  color: var(--ink);
  background: var(--page);
}""",
""".ops-workspace,
.settings-page {
  color: var(--ink);
  background:
    radial-gradient(140% 120% at 0% 0%, rgba(255, 253, 247, 0.55), transparent 46%),
    linear-gradient(180deg, var(--page) 0%, var(--page-deep) 100%);
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:40]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
