import json
from pathlib import Path

def consolidate_html(input_json_path, output_html_path):
    """
    Reads JSON file and consolidates all article content into a single HTML file.
    
    Args:
        input_json_path: Path to input JSON file (e.g., '10-uae-excise-country-law-articles.json')
        output_html_path: Path to output HTML file (e.g., 'consolidated-html.html')
    """
    # Read the JSON file
    with open(input_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Start building the consolidated HTML
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html lang='en'>")
    html_parts.append("")
    html_parts.append("<head>")
    html_parts.append("    <meta charset='UTF-8'>")
    html_parts.append("    <meta name='viewport' content='width=device-width,initial-scale=1'>")
    html_parts.append("    <title>consolidated</title>")
    html_parts.append("    <link rel='stylesheet' href='https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/prod/article.css'>")
    html_parts.append("</head>")
    html_parts.append("")
    html_parts.append("<body>")
    
    # Collect all content values
    for law in data.get('laws', []):
        for article in law.get('articles', []):
            html_parts.append(article.get('content', ''))
    
    html_parts.append("</body>")
    html_parts.append("")
    html_parts.append("</html>")
    
    # Write the consolidated HTML file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_parts))
    
    print(f"Successfully created {output_html_path}")
    print(f"Processed {len(data.get('laws', []))} law(s)")
    total_articles = sum(len(law.get('articles', [])) for law in data.get('laws', []))
    print(f"Total articles: {total_articles}")


if __name__ == '__main__':
    # Define input and output paths
    input_file = '10-uae-excise-country-law-articles.json'
    output_file = 'consolidated-html.html'
    
    # Check if input file exists
    if not Path(input_file).exists():
        print(f"Error: Input file '{input_file}' not found!")
        print("Please ensure the JSON file is in the same directory as this script.")
    else:
        # Run the consolidation
        consolidate_html(input_file, output_file)