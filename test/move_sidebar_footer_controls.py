from pathlib import Path

path = Path("web/static/index.html")
text = path.read_text(encoding="utf-8")
block = """    <div class="sidebar-footer-controls">
      <button id="theme-toggle-btn" class="theme-toggle-btn" aria-label="Toggle Theme" title="Toggle Theme"></button>
      <button id="lang-toggle-btn" class="lang-toggle-btn" aria-label="Toggle Language" title="Toggle Language">EN</button>
    </div>
"""
replacement = """<div class="sidebar-footer-controls">
  <button id="theme-toggle-btn" class="theme-toggle-btn" aria-label="Toggle Theme" title="Toggle Theme"></button>
  <button id="lang-toggle-btn" class="lang-toggle-btn" aria-label="Toggle Language" title="Toggle Language">EN</button>
</div>
"""
if block not in text:
    raise SystemExit("sidebar footer controls block not found")
text = text.replace(block, "", 1)
marker = "</header>\n"
if marker not in text:
    raise SystemExit("header close marker not found")
text = text.replace(marker, marker + replacement, 1)
path.write_text(text, encoding="utf-8")
