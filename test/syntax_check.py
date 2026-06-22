import ast, io
for p in ("browser_phase.py","mail_providers.py","signup.py"):
    ast.parse(io.open(p,encoding="utf-8").read()); print("PY OK:", p)
