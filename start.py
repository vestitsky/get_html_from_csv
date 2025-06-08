import csv
import os
import requests

CSV_FILE = 'urls.csv'
OUTPUT_DIR = 'downloaded_html'

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for idx, row in enumerate(reader, start=1):
        if not row:
            continue
        url = row[0].strip()
        if not url:
            continue

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except Exception as e:
            print(f"[{idx}] ERROR {url}: {e}")
            continue

        safe_name = url.replace("://", "_").replace("/", "_").replace("?", "_")
        filename = f"{idx:03d}_{safe_name[:100]}.html"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, 'wb') as f:
            f.write(response.content)

        print(f"[{idx}] SUCCESS: {url} → {filepath}")
