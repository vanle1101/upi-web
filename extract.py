import re
text = open('entry.js', encoding='utf-8').read()
urls = set(re.findall(r'"(/[^\"]+)"', text))
print([u for u in urls if 'api' in u or 'mail' in u or 'oauth' in u])
