import os
import json
import re
import html
from bs4 import BeautifulSoup, Doctype

HTML_FOLDER = "textOnly_input_html"
OUTPUT_FOLDER = "textOnly-content"
OUTPUT_FILE = "textOnly-content-file.json"

# HTML_FOLDER = "articles"
# OUTPUT_FOLDER = "textOnly-content"
# OUTPUT_FILE = "done-81-articles.json"


os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def minify_html_clean(html_content):
    # Preserve &quot; before parsing
    html_content = html_content.replace('&quot;', '___QUOTE___')

    # Use html5lib to preserve structure and spacing
    soup = BeautifulSoup(html_content, "html5lib")

    # Extract and decode HTML without entity conversion
    doctype = "<!DOCTYPE html>" if any(isinstance(x, Doctype) for x in soup.contents) else ""
    html_str = soup.decode(formatter=None)

    # Minify
    html_str = re.sub(r'>\s+<', '><', html_str)
    html_str = re.sub(r'\s+', ' ', html_str)

    # Replace actual double quotes with single quotes
    html_str = html_str.replace('"', "'")

    # Restore &quot;
    html_str = html_str.replace('___QUOTE___', '&quot;')

    # Ensure doctype is only added once
    html_str = re.sub(r'<!DOCTYPE html>', '', html_str, flags=re.IGNORECASE)

    return doctype + html_str.strip()

def extract_clean_text_from_body_only(html_content):
    soup = BeautifulSoup(html_content, "html5lib")
    body = soup.body
    if not body:
        return ""

    # Remove attributes
    for tag in body.find_all(True):
        tag.attrs = {}

    # Extract and clean text
    text = body.get_text(separator=' ', strip=True)
    text = html.unescape(text)

    # Remove actual quotes from &quot;
    text = text.replace('"', '')

    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\[ ', '[', text)
    text = re.sub(r' \]', ']', text)
    text = text.encode('ascii', errors='ignore').decode()

    return text.strip()

def process_html_files():
    combined_output = []

    for filename in os.listdir(HTML_FOLDER):
        if not filename.endswith(".html"):
            continue

        filepath = os.path.join(HTML_FOLDER, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            html_content = f.read()

        result = {
            "source": filename,
            "content": minify_html_clean(html_content),
            "textOnly": extract_clean_text_from_body_only(html_content),
            "betaVersion": "true"
        }

        combined_output.append(result)
        print(f"Processed: {filename}")

    output_path = os.path.join(OUTPUT_FOLDER, OUTPUT_FILE)
    with open(output_path, "w", encoding="utf-8") as out_file:
        json.dump(combined_output, out_file, indent=2, ensure_ascii=False)

    print(f"\nAll files processed. Output saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    process_html_files()
