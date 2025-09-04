#!/usr/bin/env python3
import os
import re
from pathlib import Path

def add_scripts_to_html_files():
    # Scripts to add before </head>
    head_scripts = '''<script src="./access-control.js"></script>
  <script src="./block.js"></script>
  <script src="./error-handler/link-checker.js"></script>
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-5920367457745298"
     crossorigin="anonymous"></script>'''

    # Script to add after <body>
    body_script = '''<script>
      // Initialize access control for protected page
      if (!accessControl.initProtectedPage()) {
        throw new Error('Access denied - redirecting to index.html');
      }
    </script>'''

    # Find all HTML files recursively
    html_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))

    for html_file in html_files:
        print(f"Processing: {html_file}")
        
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Calculate relative path for scripts
            relative_depth = html_file.count('/') - 1
            relative_prefix = '../' * relative_depth if relative_depth > 0 else './'
            
            # Adjust script paths based on file location
            adjusted_head_scripts = head_scripts.replace('./', relative_prefix)

            modified = False
            new_content = content

            # Check and add head scripts
            if './access-control.js' not in content and 'access-control.js' not in content:
                if '</head>' in content:
                    new_content = new_content.replace('</head>', f'{adjusted_head_scripts}\n</head>')
                    modified = True
                elif '<head>' in content:
                    new_content = new_content.replace('<head>', f'<head>\n{adjusted_head_scripts}')
                    modified = True

            # Check and add body script
            if 'accessControl.initProtectedPage' not in content:
                if '<body>' in content:
                    new_content = new_content.replace('<body>', f'<body>\n{body_script}')
                    modified = True
                elif '<body ' in content:  # Handle <body with attributes
                    body_match = re.search(r'<body[^>]*>', new_content)
                    if body_match:
                        body_tag = body_match.group(0)
                        new_content = new_content.replace(body_tag, f'{body_tag}\n{body_script}')
                        modified = True

            # Write changes if modifications were made
            if modified:
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"✓ Updated: {html_file}")
            else:
                print(f"✓ Already has scripts: {html_file}")

        except Exception as e:
            print(f"✗ Error processing {html_file}: {e}")

if __name__ == "__main__":
    add_scripts_to_html_files()
