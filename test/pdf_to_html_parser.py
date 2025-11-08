#!/usr/bin/env python3
"""
PDF to HTML Parser
This script extracts content from PDF files and converts it to structured HTML.
"""

import PyPDF2
import pdfplumber
import re
from pathlib import Path
from typing import List, Dict, Any
import json
import argparse

class PDFToHTMLParser:
    def __init__(self):
        self.content_blocks = []
        self.metadata = {}
        
    def extract_text_with_pdfplumber(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text with better formatting using pdfplumber"""
        blocks = []
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    # Extract text with positions
                    text = page.extract_text()
                    if text:
                        # Split into paragraphs
                        paragraphs = text.split('\n\n')
                        for para in paragraphs:
                            if para.strip():
                                blocks.append({
                                    'page': page_num,
                                    'type': self.classify_text_block(para.strip()),
                                    'content': para.strip(),
                                    'raw_content': para
                                })
                    
                    # Try to extract tables
                    tables = page.extract_tables()
                    for table in tables:
                        if table:
                            blocks.append({
                                'page': page_num,
                                'type': 'table',
                                'content': table,
                                'raw_content': table
                            })
                            
        except Exception as e:
            print(f"Error with pdfplumber: {e}")
            return self.fallback_extraction(pdf_path)
            
        return blocks
    
    def fallback_extraction(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Fallback method using PyPDF2"""
        blocks = []
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text = page.extract_text()
                    if text:
                        paragraphs = text.split('\n\n')
                        for para in paragraphs:
                            if para.strip():
                                blocks.append({
                                    'page': page_num,
                                    'type': self.classify_text_block(para.strip()),
                                    'content': para.strip(),
                                    'raw_content': para
                                })
                                
        except Exception as e:
            print(f"Error with PyPDF2: {e}")
            
        return blocks
    
    def classify_text_block(self, text: str) -> str:
        """Classify text blocks based on content patterns"""
        text_clean = text.strip()
        
        # Check for headings (usually shorter, may have numbers, caps)
        if len(text_clean) < 100 and (
            text_clean.isupper() or
            re.match(r'^\d+\.?\s*[A-Z]', text_clean) or
            re.match(r'^[A-Z][A-Z\s]+$', text_clean) or
            text_clean.endswith(':')
        ):
            if len(text_clean) < 50:
                return 'h2'
            else:
                return 'h3'
        
        # Check for list items
        if re.match(r'^\s*[-•*]\s+', text_clean) or re.match(r'^\s*\d+\.\s+', text_clean):
            return 'li'
            
        # Check for quotes or important text
        if text_clean.startswith('"') and text_clean.endswith('"'):
            return 'blockquote'
            
        # Default to paragraph
        return 'p'
    
    def convert_to_html(self, blocks: List[Dict[str, Any]], title: str = "Parsed Document") -> str:
        """Convert extracted blocks to HTML"""
        html_parts = []
        
        # HTML header
        html_parts.append(f"""<!DOCTYPE html>
<html lang='en'>

<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <link rel='stylesheet' href='https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/article.css'>
    <title>{title}</title>
</head>

<body>
    <div class='scope'>
        <header>
            <h1>{title}</h1>
        </header>
        <main>""")
        
        current_list = None
        
        for block in blocks:
            content = self.escape_html(block['content'])
            block_type = block['type']
            
            if block_type == 'table':
                html_parts.append(self.format_table(block['content']))
            elif block_type == 'li':
                if current_list is None:
                    html_parts.append('            <ul>')
                    current_list = 'ul'
                # Clean list item content
                list_content = re.sub(r'^\s*[-•*]\s+', '', content)
                list_content = re.sub(r'^\s*\d+\.\s+', '', list_content)
                html_parts.append(f'                <li>{list_content}</li>')
            else:
                # Close any open list
                if current_list:
                    html_parts.append('            </ul>')
                    current_list = None
                    
                # Add the block
                if block_type in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                    html_parts.append(f'            <{block_type}>{content}</{block_type}>')
                elif block_type == 'blockquote':
                    html_parts.append(f'            <blockquote>{content}</blockquote>')
                else:
                    html_parts.append(f'            <p>{content}</p>')
        
        # Close any remaining list
        if current_list:
            html_parts.append('            </ul>')
        
        # HTML footer
        html_parts.append("""
        </main>
    </div>
</body>

</html>""")
        
        return '\n'.join(html_parts)
    
    def format_table(self, table_data: List[List[str]]) -> str:
        """Format table data as HTML table"""
        if not table_data:
            return ""
            
        html = "            <table>\n"
        
        # First row as header
        if table_data:
            html += "                <thead>\n                    <tr>\n"
            for cell in table_data[0]:
                if cell:
                    html += f"                        <th>{self.escape_html(str(cell))}</th>\n"
            html += "                    </tr>\n                </thead>\n"
            
            # Rest as body
            if len(table_data) > 1:
                html += "                <tbody>\n"
                for row in table_data[1:]:
                    html += "                    <tr>\n"
                    for cell in row:
                        if cell:
                            html += f"                        <td>{self.escape_html(str(cell))}</td>\n"
                    html += "                    </tr>\n"
                html += "                </tbody>\n"
        
        html += "            </table>\n"
        return html
    
    def escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        if not isinstance(text, str):
            text = str(text)
        return (text.replace('&', '&amp;')
                   .replace('<', '&lt;')
                   .replace('>', '&gt;')
                   .replace('"', '&quot;')
                   .replace("'", '&#x27;'))
    
    def parse_pdf_to_html(self, pdf_path: str, output_path: str = None, title: str = None) -> str:
        """Main method to parse PDF and convert to HTML"""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        # Extract title from filename if not provided
        if title is None:
            title = pdf_path.stem.replace('-', ' ').replace('_', ' ').title()
        
        print(f"Parsing PDF: {pdf_path}")
        print(f"Title: {title}")
        
        # Extract content
        blocks = self.extract_text_with_pdfplumber(str(pdf_path))
        
        if not blocks:
            print("No content extracted, trying fallback method...")
            blocks = self.fallback_extraction(str(pdf_path))
        
        print(f"Extracted {len(blocks)} content blocks")
        
        # Convert to HTML
        html_content = self.convert_to_html(blocks, title)
        
        # Save to file if output path provided
        if output_path:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTML saved to: {output_path}")
        
        return html_content
    
    def save_json_debug(self, blocks: List[Dict[str, Any]], output_path: str):
        """Save extracted blocks as JSON for debugging"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(blocks, f, indent=2, ensure_ascii=False)
        print(f"Debug JSON saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert PDF to HTML')
    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('-o', '--output', help='Output HTML file path')
    parser.add_argument('-t', '--title', help='Document title')
    parser.add_argument('--debug', action='store_true', help='Save debug JSON')
    
    args = parser.parse_args()
    
    converter = PDFToHTMLParser()
    
    try:
        # Set default output path if not provided
        if not args.output:
            pdf_path = Path(args.pdf_path)
            args.output = pdf_path.parent / f"{pdf_path.stem}.html"
        
        # Parse PDF to HTML
        html_content = converter.parse_pdf_to_html(
            args.pdf_path, 
            args.output, 
            args.title
        )
        
        # Save debug JSON if requested
        if args.debug:
            debug_path = Path(args.output).parent / f"{Path(args.pdf_path).stem}_debug.json"
            blocks = converter.extract_text_with_pdfplumber(args.pdf_path)
            converter.save_json_debug(blocks, debug_path)
        
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
