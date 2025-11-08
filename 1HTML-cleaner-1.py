import os
import re
import glob

class HTMLCleaner:
    def __init__(self, input_folder="input_html", output_folder="cleaned_html"):
        """
        Initialize the HTML cleaner with input and output folder paths
        """
        self.input_folder = os.path.abspath(input_folder)
        self.output_folder = os.path.abspath(output_folder)
        
        # Create output folder if it doesn't exist
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Create input folder if it doesn't exist
        os.makedirs(self.input_folder, exist_ok=True)
        
    def clean_html(self, html_file_path, output_file_path=None):
        """
        Clean the HTML file using the provided regex patterns
        """
        if not output_file_path:
            filename = os.path.basename(html_file_path)
            name, ext = os.path.splitext(filename)
            output_file_path = os.path.join(self.output_folder, filename)
        
        print(f"Cleaning HTML file: {html_file_path}")
        
        try:
            with open(html_file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # First, replace the entire DOCTYPE and head section with clean template
            doctype_and_head_pattern = r'<!DOCTYPE html\s+PUBLIC[^>]*>[\s\S]*?<head>[\s\S]*?</head>'
            clean_head = '''<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title></title>
    <link rel='stylesheet' href='https://gtlcdnstorage.blob.core.windows.net/guide/stylesheets/decision.css'>
</head>'''
            
            content = re.sub(doctype_and_head_pattern, clean_head, content, flags=re.DOTALL)
            
            # Define regex patterns to remove (replace with empty string)
            patterns_to_remove = [
                r'<style\s+type=[\'"]text\/css[\'"]>[\s\S]*?<\/style>',  # Remove CSS style blocks
                r'src="([^"]*)"',                    # Remove src attributes
                r' width="\d+" height="\d+" ',       # Remove width and height attributes
                r' style="([^"]*)"',                 # Remove style attributes
                r' id="l\d+"',                       # Remove id attributes starting with 'l' and numbers
                r' class="s\d+"',                    # Remove class attributes starting with 's' and numbers
                r' class="([^"]*)"',                 # Remove all class attributes
                r' data-list-text="[\s\S]*?"',       # Remove data-list-text attributes
                r' data-list-text="([^"]*)"',        # Remove data-list-text attributes (alternative pattern)
                r' cellspacing="0"',                 # Remove cellspacing attributes
                r'<p />',                            # Remove self-closing p tags
                r'<p><br /></p>',                    # Remove <p><br /></p> tags
                r'<p><br></p>',                      # Remove <p><br> tags
                r' border="0"',                      # Remove border="0" attribute
                r' cellpadding="0"',                  # Remove cellpadding="0" attribute
                r'bgcolor="[^"]*"'                # Remove bgcolor attributes
            ]
            
            # Apply each regex pattern
            for pattern in patterns_to_remove:
                content = re.sub(pattern, '', content, flags=re.DOTALL)
            
            # Clean up extra spaces that might be left behind
            content = re.sub(r'\s+', ' ', content)  # Multiple spaces to single space
            content = re.sub(r'>\s+<', '><', content)  # Remove spaces between tags
            
            # Additional cleanup for better formatting
            content = re.sub(r'<body[^>]*>', '<body>', content)  # Clean body tag
            content = re.sub(r'<html[^>]*>', '<html lang=\'en\'>', content)  # Ensure html has lang attribute
            
            # Format the content nicely
            content = content.replace('><', '>\n<')  # Add line breaks between tags for readability
            
            # Save cleaned content
            with open(output_file_path, 'w', encoding='utf-8') as file:
                file.write(content)
            
            print(f"Cleaned HTML saved to: {output_file_path}")
            return output_file_path
            
        except Exception as e:
            print(f"Error cleaning HTML file {html_file_path}: {str(e)}")
            return None
    
    def process_single_file(self, html_file_path):
        """
        Process a single HTML file
        """
        if not os.path.exists(html_file_path):
            print(f"File not found: {html_file_path}")
            return None
        
        if not html_file_path.lower().endswith('.html'):
            print(f"File is not an HTML file: {html_file_path}")
            return None
        
        return self.clean_html(html_file_path)
    
    def process_folder(self):
        """
        Process all HTML files in the input folder
        """
        # Find all HTML files in the input folder
        html_pattern = os.path.join(self.input_folder, "*.html")
        html_files = glob.glob(html_pattern)
        
        if not html_files:
            print(f"No HTML files found in folder: {self.input_folder}")
            print("Please place your HTML files in the input folder and try again.")
            return []
        
        print(f"Found {len(html_files)} HTML file(s) to process:") 
        for file in html_files:
            print(f"  - {os.path.basename(file)}")
        
        processed_files = []
        
        for html_file in html_files:
            print(f"\n--- Processing: {os.path.basename(html_file)} ---")
            result = self.clean_html(html_file)
            if result:
                processed_files.append(result)
        
        return processed_files
    
    def get_html_files_in_folder(self):
        """
        Get list of all HTML files in the input folder
        """
        html_pattern = os.path.join(self.input_folder, "*.html")
        return glob.glob(html_pattern)

# Usage functions
def clean_single_file(input_file_path, output_file_path=None):
    """
    Clean a single HTML file
    """
    cleaner = HTMLCleaner()
    return cleaner.process_single_file(input_file_path)

def clean_folder(input_folder="input_html", output_folder="cleaned_html"):
    """
    Clean all HTML files in a folder
    """
    cleaner = HTMLCleaner(input_folder, output_folder)
    return cleaner.process_folder()

def main():
    """
    Main function - processes all HTML files in the input folder
    """
    print("HTML Cleaner Script")
    print("==================")
    
    # Initialize cleaner with default folders
    cleaner = HTMLCleaner()
    
    print(f"Input folder: {cleaner.input_folder}")
    print(f"Output folder: {cleaner.output_folder}")
    print()
    
    # Process all HTML files in the input folder
    processed_files = cleaner.process_folder()
    
    if processed_files:
        print(f"\n✅ Successfully processed {len(processed_files)} file(s):")
        for file in processed_files:
            print(f"  - {os.path.basename(file)}")
    else:
        print("\n❌ No files were processed successfully.")
    
    print("\nProcess completed!")

if __name__ == "__main__":
    main()
