import os
import re
from bs4 import BeautifulSoup

# Input and output
input_file = "income-tax-law.html"
output_file = "income-tax-law-Done.html"

# Folder for separate articles
output_dir = "articles"
os.makedirs(output_dir, exist_ok=True)

# Read HTML
with open(input_file, "r", encoding="utf-8") as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

# Collect chunks
chunks = []

# Function to sanitize filenames
def sanitize_filename(name: str) -> str:
    # Remove newlines and extra spaces
    name = " ".join(name.split())
    # Replace invalid filename characters
    name = re.sub(r'[\\/*?:"<>|]', "-", name)
    # Optionally truncate filenames to 255 characters (Windows limit)
    return name[:255]

# Iterate through all headers (h3 tags inside <header>)
headers = soup.find_all("h3")
for header in headers:
    try:
        # Debug: Check if this header is inside a <header> tag
        header_parent = header.find_parent("header")
        if not header_parent:
            print(f"Skipping header (no parent <header>): {header}")
            continue  # Skip this header if no parent <header>

        # Find the next article after this header
        article = header_parent.find_next("article")
        if not article:
            print(f"Skipping header {header} (no article found)")
            continue  # Skip if no article is found after the header

        # Extract chunk (header + article)
        header_html = str(header_parent)
        article_html = str(article)
        chunk_html = header_html + "\n" + article_html
        chunks.append(chunk_html)

        # File name from h3 text
        raw_name = header.get_text(strip=True)
        file_name = sanitize_filename(raw_name) + ".html"
        file_path = os.path.join(output_dir, file_name)

        # Write to separate file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
    <html lang='en'>

    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width,initial-scale=1'>
        <link rel='stylesheet' href='https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/article.css'>
        <title>{raw_name}</title>
    </head>

    <body>
        <div class='scope'>
       
    """)
            f.write(str(header_parent))
            f.write("""
       
        <main>
    """)
            f.write(str(article))
            f.write("""
        </main>
           <footer>
            <section>            
                    <h3>Footnotes</h3>
               
            </section>
        </footer>           
        </div>
    </body>

    </html>""")
        
        print(f"✅ Successfully saved: {file_name}")

    except Exception as e:
        print(f"Error processing header: {header}. Error: {str(e)}")

# Write combined file
with open(output_file, "w", encoding="utf-8") as f:
    f.write("<!DOCTYPE html>\n<html lang='en'>\n<head>\n<meta charset='UTF-8'>\n</head>\n<body>\n")
    f.write("\n\n".join(chunks))
    f.write("\n</body>\n</html>")

print(f"✅ Combined file written as {output_file}")
print(f"Individual files stored in folder: {output_dir}")
