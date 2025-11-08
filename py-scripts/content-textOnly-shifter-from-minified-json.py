import json

# File paths
articles_file = '14-ksa-vat-country-law-articles-decisions-delta.json'
textonly_file = 'textOnly-content/textOnly-content-file.json'
output_file = '14-ksa-vat-country-law-articles-decisions-delta.merged.json'

# Load articles JSON
with open(articles_file, 'r', encoding='utf-8') as f:
    articles_data = json.load(f)

# Load textOnly content JSON
with open(textonly_file, 'r', encoding='utf-8') as f:
    textonly_data = json.load(f)

# Build a lookup from source (e.g., 'Article 1.html') to content/textOnly
textonly_lookup = {item['source'].replace('.html','').strip(): item for item in textonly_data if 'source' in item}

# For each article, match by title (e.g., 'Article 1') to source (e.g., 'Article 1.html')
for law in articles_data.get('laws', []):
    for article in law.get('articles', []):
        title = article.get('title', '').strip()
        key = title  # e.g., 'Article 1'
        match = textonly_lookup.get(key)
        if match:
            article['content'] = match.get('content', '')
            article['textOnly'] = match.get('textOnly', '')

# Write the merged output
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(articles_data, f, ensure_ascii=False, indent=2)
