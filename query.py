import sqlite3
try:
    c = sqlite3.connect('runtime/settings.sqlite')
    row = c.execute("SELECT refresh_token FROM combos WHERE email='RoksanaWaqia8690@hotmail.com'").fetchone()
    if row:
        print(f"Token from DB: {row[0][:30]}...")
    else:
        print("Not found in DB")
except Exception as e:
    print("Error:", e)
