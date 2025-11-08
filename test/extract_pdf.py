import pdfplumber
import json
import re
from pathlib import Path

def extract_pdf_content(pdf_path):
    """Extract text, tables, and structure from PDF"""
    
    content_data = {
        'title': '',
        'sections': [],
        'tables': [],
        'footnotes': [],
        'toc': [],
        'full_text': '',
        'pages': []
    }
    
    with pdfplumber.open(pdf_path) as pdf:
        print(f"Processing PDF '{pdf_path.name}' with {len(pdf.pages)} pages...")
        
        full_text = ""
        page_texts = []
        
        for page_num, page in enumerate(pdf.pages, 1):
            page_text = page.extract_text()
            if page_text:
                page_texts.append({
                    'page_number': page_num,
                    'text': page_text.strip()
                })
                full_text += f"\n--- PAGE {page_num} ---\n{page_text}\n"
            
            tables = page.extract_tables()
            for table_idx, table in enumerate(tables):
                if table:
                    content_data['tables'].append({
                        'page': page_num,
                        'table_index': table_idx,
                        'data': table
                    })
        
        content_data['full_text'] = full_text
        content_data['pages'] = page_texts
        
        if page_texts:
            first_page = page_texts[0]['text']
            lines = first_page.split('\n')
            for line in lines[:10]:
                if line.strip() and len(line.strip()) > 10:
                    content_data['title'] = line.strip()
                    break
        
        content_data['sections'] = extract_sections(full_text)
        content_data['toc'] = extract_toc(full_text)
        content_data['footnotes'] = extract_footnotes(full_text)
    
    return content_data

def extract_sections(text):
    sections = []
    patterns = [
        r'^(\d+\.?\s+[A-Z][^\n]*)',
        r'^([A-Z][A-Z\s]+)$',
        r'^(\d+\.\d+\.?\s+[A-Z][^\n]*)',
        r'^([A-Z][a-z][^\n]*?)$',
    ]
    
    lines = text.split('\n')
    current_section = None
    section_content = []
    
    for line_num, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        
        is_header = False
        for pattern in patterns:
            if re.match(pattern, line, re.MULTILINE):
                if current_section and section_content:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(section_content).strip(),
                        'level': determine_header_level(current_section)
                    })
                current_section = line
                section_content = []
                is_header = True
                break
        
        if not is_header and current_section:
            section_content.append(line)
    
    if current_section and section_content:
        sections.append({
            'title': current_section,
            'content': '\n'.join(section_content).strip(),
            'level': determine_header_level(current_section)
        })
    
    return sections

def determine_header_level(title):
    if re.match(r'^\d+\.?\s+', title):
        return 1
    elif re.match(r'^\d+\.\d+\.?\s+', title):
        return 2
    elif re.match(r'^\d+\.\d+\.\d+\.?\s+', title):
        return 3
    elif title.isupper():
        return 1
    else:
        return 2

def extract_toc(text):
    toc_items = []
    lines = text.split('\n')
    in_toc = False
    
    for line in lines:
        line = line.strip()
        
        if any(keyword in line.lower() for keyword in ['contents', 'table of contents', 'index']):
            in_toc = True
            continue
        
        if in_toc and re.match(r'^\d+\.?\s+[A-Z]', line) and 'contents' not in line.lower():
            break
        
        if in_toc and line:
            toc_match = re.match(r'^(\d+\.?\d*\.?\s*)(.*?)\s*\.+\s*(\d+)$', line)
            if toc_match:
                toc_items.append({
                    'number': toc_match.group(1).strip(),
                    'title': toc_match.group(2).strip(),
                    'page': toc_match.group(3).strip()
                })
            elif re.match(r'^\d+\.?\d*\.?\s+', line):
                toc_items.append({
                    'number': re.match(r'^(\d+\.?\d*\.?)\s+', line).group(1),
                    'title': re.sub(r'^\d+\.?\d*\.?\s+', '', line),
                    'page': ''
                })
    
    return toc_items

def extract_footnotes(text):
    footnotes = []
    footnote_refs = re.findall(r'\[(\d+)\]|\((\d+)\)|[¹²³⁴⁵⁶⁷⁸⁹⁰]', text)
    lines = text.split('\n')
    for line in lines:
        line = line.strip()
        footnote_def = re.match(r'^(\[?\d+\]?|\(\d+\))\s*(.+)', line)
        if footnote_def and len(footnote_def.group(2)) > 10:
            footnotes.append({
                'number': footnote_def.group(1),
                'text': footnote_def.group(2)
            })
    return footnotes

if __name__ == "__main__":
    input_folder = Path("input_1")  # Input folder named 'input_1'
    output_folder = Path("output_1")  # Output folder named 'output_1'
    
    output_folder.mkdir(parents=True, exist_ok=True)
    
    pdf_files = list(input_folder.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found in the 'input_1' folder.")
    
    for pdf_file in pdf_files:
        print(f"\nStarting extraction for {pdf_file.name}...")
        content = extract_pdf_content(pdf_file)
        
        output_file = output_folder / f"{pdf_file.stem}.txt"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {content['title']}\n\n")
            f.write(f"Number of sections: {len(content['sections'])}\n")
            f.write(f"Number of tables: {len(content['tables'])}\n")
            f.write(f"Number of footnotes: {len(content['footnotes'])}\n")
            f.write(f"Number of TOC items: {len(content['toc'])}\n")
            f.write(f"Total pages: {len(content['pages'])}\n\n")
            
            f.write("=== Sections ===\n")
            for section in content['sections']:
                f.write(f"{section['title']} (Level {section['level']})\n")
                f.write(section['content'][:200] + '...\n\n')
            
            f.write("\n=== Tables ===\n")
            for table in content['tables']:
                f.write(f"Page {table['page']} - Table {table['table_index']} with {len(table['data'])} rows\n")
            
            f.write("\n=== Footnotes ===\n")
            for note in content['footnotes']:
                f.write(f"{note['number']}: {note['text'][:100]}...\n")
            
            f.write("\n=== TOC ===\n")
            for item in content['toc']:
                f.write(f"{item['number']} {item['title']} (Page {item['page']})\n")
        
        print(f"Saved extraction to {output_file}")
    
    print("\nAll PDFs processed successfully!")
