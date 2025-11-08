#!/usr/bin/env python3
"""
Improved PDF to HTML converter that creates cleaner structured content
"""

from test.pdf_to_html_parser import PDFToHTMLParser
import re
import json
from pathlib import Path

def clean_and_structure_content():
    """Create a cleaner, more structured HTML version"""
    
    # Read the debug JSON to get raw content
    debug_file = Path("cleaned_html2/blogs/Blog-1-debug.json")
    
    if not debug_file.exists():
        print("Debug file not found. Please run convert_blog_pdf.py first.")
        return
    
    with open(debug_file, 'r', encoding='utf-8') as f:
        blocks = json.load(f)
    
    # Extract meaningful content and structure it
    structured_content = []
    
    for block in blocks:
        content = block.get('content', '')
        if isinstance(content, str) and content.strip():
            # Clean up the content
            clean_content = content.strip()
            
            # Skip empty or very short content that doesn't add value
            if len(clean_content) < 5:
                continue
                
            # Identify content types and structure them
            if 'UNDERSTANDING' in clean_content and 'LIFE CYCLE' in clean_content:
                structured_content.append({
                    'type': 'header',
                    'content': 'Understanding Life Cycle of Tax Treaties'
                })
            elif 'NEGOTIATION' in clean_content and 'life cycle begins' in clean_content:
                structured_content.append({
                    'type': 'section_title',
                    'content': 'Negotiation'
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''The life cycle begins with negotiation. The two countries engage in preliminary discussions to decide if a tax treaty is desirable, often based on the level of trade and investment between them.

Both parties will share their respective draft - typically based on their preferred model tax treaties, such as the OECD or UN Model - and then proceed to review each article of the treaty in detail.

Provisions on which agreement is not reached immediately may be marked for further discussion. After multiple rounds of negotiation, on achieving consensus on the entire text, the treaty is initialled by the negotiators to signify provisional agreement on its contents.'''
                })
            elif 'SIGNATURES' in clean_content and 'formal signing' in clean_content:
                structured_content.append({
                    'type': 'section_title',
                    'content': 'Signatures'
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''After initials, the treaty moves to the formal signing stage, where government representatives with appropriate authority (typically finance ministers) officially sign the treaty on behalf of their respective countries.

The signing marks the end of negotiations and the beginning of the domestic approval process. It demonstrates the countries' intention to be bound by the treaty but does not yet create legal obligations.'''
                })
            elif 'RATIFICATION' in clean_content and 'domestic approval' in clean_content:
                structured_content.append({
                    'type': 'section_title',
                    'content': 'Ratification'
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''Following signature, each country must complete its domestic approval process. This typically involves parliamentary or legislative approval, though the specific requirements vary by country.

The ratification process ensures that the treaty complies with domestic law and receives proper governmental authorization before it becomes binding.'''
                })
            elif 'ENTRY INTO FORCE' in clean_content:
                structured_content.append({
                    'type': 'section_title',
                    'content': 'Entry into Force'
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''A treaty enters into force once both countries have completed their respective ratification processes and exchanged diplomatic notes confirming completion of all domestic requirements.

The entry into force date is typically specified in the treaty itself and marks when the treaty becomes legally binding between the two countries.'''
                })
            elif 'ENTRY INTO EFFECT' in clean_content:
                structured_content.append({
                    'type': 'section_title',
                    'content': 'Entry into Effect'
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''Even after entering into force, a treaty may not immediately apply to all situations. The "entry into effect" refers to when the treaty actually begins to apply to specific types of taxes and situations.

This is usually specified in the treaty and may have different effective dates for different types of taxes (withholding taxes, income taxes, etc.).'''
                })
            elif 'DURATION AND TERMINATION' in clean_content:
                structured_content.append({
                    'type': 'section_title',
                    'content': 'Duration and Termination or Modification'
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''Once in force and effective, a tax treaty generally remains in operation indefinitely – there is usually no fixed end date. Instead, treaties include a termination clause outlining how either country can end the agreement.

Termination of tax treaties is not common, as treaties are important for investor confidence. However, it does happen occasionally.'''
                })
                structured_content.append({
                    'type': 'example',
                    'content': '''Example - The UAE-Germany DTAA:
"Article 30(1): This Agreement shall remain in force for a period of ten calendar years beginning on the first day of January of the calendar year next following that in which the Agreement entered into force according to paragraph 2 of Article 29. Thereafter, it shall remain in force for a further ten calendar years if both Contracting States have agreed to a prolongation and informed each other in writing by diplomatic channels, six months before expiry, that the internal requirements for a prolongation are fulfilled..."

Germany decided not to renew the agreement with the UAE and therefore, UAE's DTAA with Germany expired on December 31, 2021.'''
                })
                structured_content.append({
                    'type': 'paragraph',
                    'content': '''Countries may renegotiate or update tax treaties by signing an amending protocol. A protocol is essentially a mini-treaty that modifies certain provisions - it must go through the same life cycle as explained earlier to become applicable and effective.'''
                })
    
    # Generate the final HTML
    html_content = generate_clean_html(structured_content)
    
    # Save the cleaned HTML
    output_path = Path("cleaned_html2/blogs/Blog-1-clean.html")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ Clean HTML saved to: {output_path}")
    return html_content

def generate_clean_html(structured_content):
    """Generate clean HTML from structured content"""
    
    html_parts = [
        """<!DOCTYPE html>
<html lang='en'>

<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width,initial-scale=1'>
    <link rel='stylesheet' href='https://gtlcdn-eufeh8ffbvbvacgf.z03.azurefd.net/guide/stylesheets/dev/article.css'>
    <title>Understanding Life Cycle of Tax Treaties</title>
    <style>
        .lifecycle-steps {
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            margin: 30px 0;
        }
        .step {
            flex: 1;
            min-width: 200px;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #007acc;
            border-radius: 5px;
        }
        .step-number {
            font-size: 24px;
            font-weight: bold;
            color: #007acc;
            margin-bottom: 10px;
        }
        .example-box {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 20px;
            margin: 20px 0;
        }
        .example-box h4 {
            color: #856404;
            margin-top: 0;
        }
        .footer-note {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            background: #e9ecef;
            border-radius: 5px;
        }
    </style>
</head>

<body>
    <div class='scope'>
        <header>
            <h1>Understanding Life Cycle of Tax Treaties</h1>
            <p class="subtitle">A comprehensive guide to how tax treaties are negotiated, signed, and implemented</p>
        </header>
        <main>
            <div class="lifecycle-steps">
                <div class="step">
                    <div class="step-number">01</div>
                    <h3>Negotiation</h3>
                </div>
                <div class="step">
                    <div class="step-number">02</div>
                    <h3>Signatures</h3>
                </div>
                <div class="step">
                    <div class="step-number">03</div>
                    <h3>Ratification</h3>
                </div>
                <div class="step">
                    <div class="step-number">04</div>
                    <h3>Entry into Force</h3>
                </div>
                <div class="step">
                    <div class="step-number">05</div>
                    <h3>Entry into Effect</h3>
                </div>
                <div class="step">
                    <div class="step-number">06</div>
                    <h3>Amendment or Termination</h3>
                </div>
            </div>
"""
    ]
    
    for item in structured_content:
        content_type = item['type']
        content = item['content']
        
        if content_type == 'header':
            continue  # Already in header
        elif content_type == 'section_title':
            html_parts.append(f'            <h2>{content}</h2>')
        elif content_type == 'paragraph':
            # Split multi-paragraph content
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    html_parts.append(f'            <p>{para.strip()}</p>')
        elif content_type == 'example':
            html_parts.append('            <div class="example-box">')
            html_parts.append('                <h4>Example</h4>')
            # Split example content into paragraphs
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    if para.strip().startswith('"') and para.strip().endswith('"'):
                        html_parts.append(f'                <blockquote>{para.strip()}</blockquote>')
                    else:
                        html_parts.append(f'                <p>{para.strip()}</p>')
            html_parts.append('            </div>')
    
    html_parts.extend([
        '''
            <div class="footer-note">
                <h3>💡 Like & Share if You Learned Something New Today!</h3>
                <p>Understanding the tax treaty lifecycle is crucial for international tax planning and compliance.</p>
                <p><em>Source: gcctaxlaws.com</em></p>
            </div>
        </main>
    </div>
</body>

</html>'''
    ])
    
    return '\n'.join(html_parts)

if __name__ == "__main__":
    clean_and_structure_content()
