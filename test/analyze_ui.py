import re
from bs4 import BeautifulSoup
import json

def analyze_html(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()
            soup = BeautifulSoup(html, 'html.parser')
            
            print(f"--- Analysis for {path} ---")
            
            # Find all main tabs
            tabs = soup.find_all('main', class_=re.compile(r'tab-content|ops-workspace'))
            if not tabs:
                tabs = soup.find_all('section')
            
            if not tabs:
                print("No standard tabs found. Listing major divs.")
                tabs = soup.find_all('div', id=True)
                
            for tab in tabs:
                tab_id = tab.get('id', 'No ID')
                tab_class = ' '.join(tab.get('class', []))
                print(f"\nTab: #{tab_id} (class: {tab_class})")
                
                # List form inputs inside this tab
                inputs = tab.find_all(['input', 'select', 'textarea', 'button'])
                for inp in inputs:
                    tag = inp.name
                    inp_id = inp.get('id', '')
                    inp_name = inp.get('name', '')
                    inp_type = inp.get('type', '')
                    inp_text = inp.text.strip() if tag == 'button' else ''
                    print(f"  - {tag} [id={inp_id}] [type={inp_type}] [name={inp_name}] {inp_text}")
    except Exception as e:
        print(f"Error parsing {path}: {e}")

analyze_html('web/static/index.html')
analyze_html('web/static/_preview.html')
