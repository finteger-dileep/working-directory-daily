import os
import re

# Define the input and output folders
input_folder = 'cleaned_html'
output_folder = 'cleaned_html2'

# Make sure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the patterns to remove
patterns = [
    r'<p\s*/>',                            # Remove self-closing <p />
    r'<p>\s*<br\s*/?>\s*</p>',              # Remove <p><br /></p>, <p><br></p>, <p><br /> </p>, etc.
    r'<p><br\s*/?>\s*</p>',                 # Another variation for <p><br></p>
    r'<p>\s*<span>\s*<table>.*?</table>\s*</span>\s*</p>',  # Remove the <p><span><table>...</table></span></p> structure
]

# Function to clean the HTML content
def clean_html(content):
    # Apply all patterns to remove unwanted tags
    for pattern in patterns:
        content = re.sub(pattern, '', content, flags=re.DOTALL)
    return content

# Iterate over all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".html"):
        input_path = os.path.join(input_folder, filename)
        
        with open(input_path, 'r', encoding='utf-8') as file:
            html_content = file.read()
        
        # Clean the HTML content
        cleaned_content = clean_html(html_content)
        
        # Save the cleaned content to the output folder
        output_path = os.path.join(output_folder, filename)
        with open(output_path, 'w', encoding='utf-8') as file:
            file.write(cleaned_content)

        print(f"Cleaned {filename} and saved to {output_path}")

print("All files have been cleaned successfully!")
