# -*- coding: utf-8 -*-
import io
PATH = "web/static/workspace.css"
s = io.open(PATH, encoding="utf-8").read()
pairs = []

# Rail: layered depth + hairline edge.
pairs.append((
"""  color: #f5f3ed;
  background: var(--rail);
  box-shadow: none;
  backdrop-filter: none;
}""",
"""  color: var(--rail-fg);
  background:
    linear-gradient(180deg, #2e312b 0%, var(--rail) 58%, #25281f 100%);
  box-shadow: inset -1px 0 0 rgba(0, 0, 0, 0.22);
  backdrop-filter: none;
}"""))

# Brand block: premium mark + softer divider spacing.
pairs.append((
""".brand {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 11px;
  padding: 0 8px 21px;
  border-bottom: 1px solid var(--rail-line);
}""",
""".brand {
  display: flex;
  align-items: center;
  min-width: 0;
  gap: 12px;
  padding: 2px 8px 20px;
  border-bottom: 1px solid var(--rail-line);
}"""))

pairs.append((
""".brand-mark {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  flex: 0 0 34px;
  border: 0;
  border-radius: 10px;
  background: #eeece4;
  box-shadow: none;
}""",
""".brand-mark {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  flex: 0 0 36px;
  border: 0;
  border-radius: 11px;
  background: linear-gradient(150deg, #f4f1e8 0%, #e4e0d2 100%);
  box-shadow: 0 1px 0 rgba(255, 255, 255, 0.18) inset, 0 3px 10px rgba(0, 0, 0, 0.28);
}"""))

pairs.append((
""".brand-dot {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  background: var(--accent);
  box-shadow: none;
  transform: rotate(45deg);
}""",
""".brand-dot {
  width: 11px;
  height: 11px;
  border-radius: 3px;
  background: linear-gradient(150deg, #5c8071 0%, var(--accent) 100%);
  box-shadow: 0 1px 2px rgba(40, 60, 50, 0.4);
  transform: rotate(45deg);
}"""))

# Nav item: clearer active state with accent left bar.
pairs.append((
""".tab-btn:hover {
  color: #fffef9;
  background: rgba(255, 255, 255, 0.055);
  transform: none;
}

.tab-btn.active {
  color: #fffef9;
  border: 0;
  background: var(--rail-soft);
  box-shadow: none;
}""",
""".tab-btn {
  position: relative;
}

.tab-btn:hover {
  color: var(--rail-fg);
  background: rgba(255, 255, 255, 0.05);
  transform: none;
}

.tab-btn.active {
  color: #fffef9;
  border: 0;
  background: linear-gradient(180deg, rgba(86, 122, 106, 0.32), rgba(86, 122, 106, 0.2));
  box-shadow: inset 0 0 0 1px rgba(140, 178, 160, 0.16);
}

.tab-btn.active::before {
  content: "";
  position: absolute;
  top: 9px;
  bottom: 9px;
  left: 0;
  width: 3px;
  border-radius: 0 3px 3px 0;
  background: #7fa996;
}"""))

# Active glyph color -> eucalyptus instead of brass-ish.
pairs.append((
""".tab-btn.active .tab-glyph {
  color: #d9c8a5;
  opacity: 1;
}""",
""".tab-btn.active .tab-glyph {
  color: #9fc4b3;
  opacity: 1;
}"""))

# Runtime controls separation: stronger label + divider breathing room.
pairs.append((
""".topbar-actions {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
  min-width: 0;
  margin-top: auto;
  padding: 17px 8px 2px;
  gap: 9px;
  border-top: 1px solid var(--rail-line);
}""",
""".topbar-actions {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  width: 100%;
  min-width: 0;
  margin-top: auto;
  padding: 18px 8px 4px;
  gap: 11px;
  border-top: 1px solid var(--rail-line);
}"""))

pairs.append((
""".rail-section-label {
  color: #96958f;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.06em;
  text-transform: none;
}""",
""".rail-section-label {
  margin-bottom: 1px;
  color: var(--rail-fg-faint);
  font-size: 10.5px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}"""))

miss = []
for old, new in pairs:
    if old not in s: miss.append(old[:45]); continue
    s = s.replace(old, new, 1)
io.open(PATH, "w", encoding="utf-8").write(s)
print("missing:", miss)
