# -*- coding: utf-8 -*-
import io, re
for p in ("web/static/workspace.css", "web/static/style.css"):
    s = io.open(p, encoding="utf-8").read()
    # strip comments + string contents roughly for brace balance
    code = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    opens = code.count("{")
    closes = code.count("}")
    print(f"{p}: open={opens} close={closes} balanced={opens==closes}")
