import os
from bs4 import BeautifulSoup

# Input and output paths
input_html = 'ksa-vat.html'
output_dir = 'html'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the main HTML file
with open(input_html, 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

# Find all article tags
articles = soup.find_all('article')

for article in articles:
    # Find the h1 tag inside the article's header
        header = article.find('header')
        h1 = header.find('h1') if header else None
        if h1:
            h1_text = h1.get_text(strip=True)
            filename = h1_text.replace(' ', '_').replace('/', '_')
            filename = ''.join(c for c in filename if c.isalnum() or c in ('_', '-'))
            filename += '.html'
            out_path = os.path.join(output_dir, filename)
            html_str = f'''<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <link rel='stylesheet' href='https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/article.css'>
    <title>{h1_text}</title>
</head>
<body>
    <div class='scope'>
        <main>
{str(article)}
        </main>
    </div>
</body>
</html>'''
            with open(out_path, 'w', encoding='utf-8') as out_f:
                out_f.write(html_str)
