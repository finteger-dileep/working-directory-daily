# AI Agent Instructions for Legal Document Processing System

## Project Overview
This is a **legal/tax document processing pipeline** that converts PDF legal documents (primarily Middle Eastern tax laws, DTAAs, and regulations) into structured HTML and JSON formats with strict formatting rules. The system handles multi-language content (English/Arabic) and maintains precise hierarchical structures (Articles, Chapters, Sections).

## Core Architecture

### Processing Pipeline Flow
```
PDF → HTML Cleaning → Structure Validation → JSON Generation → Output
```

1. **Input Stage**: Raw HTML files (converted from PDFs) in `input_html/` or `textOnly_input_html/`
2. **Cleaning Stage**: Multi-pass HTML cleanup (`1HTML-cleaner-1.py` → `2HTML-cleaner-2.py`)
3. **Output Stage**: Structured content in `cleaned_html/`, `cleaned_html2/`, and `json/`

### Key Directories
- `Prompts/`: **Critical** - Contains HTML structure templates for different document types (DTAA, Article, Decision, Guide)
- `json/`: Final output with both minified HTML (`content`) and plain text (`textOnly`) representations
- `textOnly-content/`: Intermediate JSON outputs before final processing
- `zDONE/`: Completed work organized by date (reference for patterns)

## Document Type Patterns

### Document Hierarchies (see `test/Hierarchy.md`)
- **Articles-only**: Article → Sections (e.g., Income Tax Laws)
- **Chapter-based**: Chapter → Articles → Sections (e.g., comprehensive tax codes)
- **DTAA (Double Taxation Agreements)**: Special structure with treaty preambles, protocols
- **Decisions**: Decision → Parts/Chapters → Articles
- **Guides**: Educational content with numbered sections and examples

### HTML Structure Templates
Each document type has a **strict template** in `Prompts/`:
- `Article-only.html` - Single article documents
- `DTAA-Chapter.html` / `DTAA-noChapter.html` - Treaty documents
- `Decision*.html` - Ministerial decisions
- `prompt-*-zakat-guide.html` - Tax guidance documents

**Critical Rule**: Never modify document structure; only clean styling while preserving semantic HTML.

## Development Workflows

### 1. HTML Cleaning Workflow
```python
# Two-stage cleaning process (ALWAYS use both)
python 1HTML-cleaner-1.py  # Stage 1: Remove CSS, attributes, normalize DOCTYPE
python 2HTML-cleaner-2.py  # Stage 2: Remove empty tags, unwanted wrappers
```

**What gets removed**: `style`, `class`, `id`, `data-*` attributes, inline CSS, empty `<p>` tags, `<p><br></p>` patterns
**What gets preserved**: ALL content text, semantic tags (`<h1>`, `<article>`, `<table>`, `<sup>`, footnotes)

### 2. JSON Generation Workflow
```python
# Choose the correct script based on document type:
python wtextOnly-content-latest-v2.py      # Standard articles/laws
python dtaa-textOnly-content-latest-v2.py  # DTAA documents (includes h1 extraction)
```

**Output Schema** (see `json/` examples):
```json
{
  "source": "filename.html",
  "title": "Extracted H1 content",          // DTAA only
  "content": "minified HTML with quotes",   // Single quotes, &quot; preserved
  "textOnly": "plain text without markup",  // All HTML stripped, normalized spaces
  "betaVersion": true
}
```

### 3. PDF Processing Workflow
```python
# Extract images from PDFs (for diagrams, flowcharts)
python scripts/img-extracter.py  # Outputs to scripts/cropped_images/

# Extract structured text from PDFs
python extract_pdf.py  # Experimental - extracts sections, tables, TOC
```

## Critical Coding Patterns

### BeautifulSoup Usage
```python
from bs4 import BeautifulSoup, Doctype

# ALWAYS use html5lib for structure preservation
soup = BeautifulSoup(content, "html5lib")

# Preserve special characters
content = content.replace('&quot;', '___QUOTE___')  # Before parsing
content = content.replace('___QUOTE___', '&quot;')  # After processing
```

### HTML Minification Pattern
```python
# Standard minification (see wtextOnly-content-latest-v2.py:20-38)
html_str = re.sub(r'>\s+<', '><', html_str)      # Remove inter-tag whitespace
html_str = re.sub(r'\s+', ' ', html_str)         # Normalize spaces
html_str = html_str.replace('"', "'")            # Quotes to single
```

### Text Extraction Pattern
```python
# Clean text extraction (see wtextOnly-content-latest-v2.py:40-61)
text = body.get_text(separator=' ', strip=True)
text = html.unescape(text)                       # Decode entities
text = text.replace('"', '')                     # Remove actual quotes
text = re.sub(r'\s+', ' ', text)                 # Normalize whitespace
text = text.encode('ascii', errors='ignore').decode()  # ASCII only
```

### CSS Linking Convention
All cleaned HTML uses CDN-hosted stylesheets:
- Articles: `https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/article.css`
- DTAAs: `https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/dtaa.css`
- Guides: `https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/guide.css`

## File Naming & Organization

### Input Files
- Original: `healthcare 3.html` (descriptive names)
- Minified: `healthcare 3.min.html` (created during processing)
- Pattern: Use `.min.html` suffix for minified versions

### Output Files  
- Cleaned: Same basename in `cleaned_html/` or `cleaned_html2/`
- JSON: Descriptive names like `ksa-vat-guidelines-guide.json`, `20-kwt-ktl-country-law-articles.json`
- Completed work: Date-stamped folders in `zDONE/` (format: `DD-MM-YYYY/`)

### Backup Strategy
Use `zDONE/old-data/` for versioned backups. Create dated subfolders before major changes.

## Testing & Validation

### Before Committing Changes
1. **Structure validation**: Open output HTML in browser - check rendering
2. **JSON validation**: Verify both `content` and `textOnly` fields populated
3. **Character encoding**: Ensure no mojibake (garbled Arabic/special chars)
4. **Footnote integrity**: Verify `<sup><a href='#bookmark'>` links intact

### Common Issues & Solutions
- **Issue**: HTML entities double-encoded (e.g., `&amp;quot;`)
  - **Fix**: Use `formatter=None` in BeautifulSoup decode: `soup.decode(formatter=None)`

- **Issue**: Lost footnote links after cleaning
  - **Fix**: Never remove `id` attributes on `<article>`, `<h3>`, footnote divs

- **Issue**: Table structure corrupted
  - **Fix**: Preserve `<table>`, `<tbody>`, `<tr>`, `<td>` tags; only remove attributes

## Special Considerations

### Arabic Content Handling
- Preserve right-to-left text direction
- Don't strip Arabic characters in textOnly extraction (only non-ASCII in current implementation)
- Maintain `lang='en'` in HTML root even for bilingual docs

### Legal Formatting Requirements
- **Footnotes**: Must maintain `<sup><a href='#bookmark1'>[1]</a>` → `<div id='bookmark1'>` linking
- **Article numbering**: Preserve exact formatting (e.g., "Article 1", "Article (13 bis)")
- **Chapter headers**: UPPERCASE for chapters, Title Case for articles
- **Definitions**: Special `<div class='definition-wrapper'><table class='definition'>` structure

### Performance Notes
- Large files (>1MB HTML): Process in chunks if memory issues arise
- Regex patterns: Pre-compile frequently used patterns (see `1HTML-cleaner-1.py:52-70`)
- BeautifulSoup: Use `html5lib` for correctness over speed

## Dependencies

**Python Libraries** (infer from imports):
- `BeautifulSoup4` (html5lib parser)
- `pdfplumber` (PDF text/image extraction)
- `opencv-python` (cv2) + `numpy` + `Pillow` (image processing)
- Standard library: `os`, `re`, `json`, `html`, `glob`, `pathlib`

Install with: `pip install beautifulsoup4 html5lib pdfplumber opencv-python pillow`

## Quick Reference Commands

```bash
# Process new document (full pipeline)
cp raw.html input_html/
python 1HTML-cleaner-1.py
python 2HTML-cleaner-2.py
python wtextOnly-content-latest-v2.py

# Check output
cat textOnly-content/textOnly-content-file.json | python -m json.tool

# Archive completed work
mkdir -p zDONE/$(date +%d-%m-%Y)
mv cleaned_html2/*.html zDONE/$(date +%d-%m-%Y)/
```

## Notes for AI Agents
- **Always check `Prompts/` first** when working with new document types
- **Reference `json/` examples** to understand expected output structure
- **Consult `zDONE/` folders** for working examples of completed documents
- When in doubt about structure, **preserve over remove** - legal content requires precision
- The `betaVersion: true` flag indicates documents under active development/review
