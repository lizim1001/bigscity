#!/usr/bin/env python3
"""
Fix website issues:
1. Remove Jimdo advertisements from all HTML files
2. Copy correct content from students-alumni to publications for duplicate items
"""
import os
import re
from pathlib import Path
import shutil

def remove_jimdo_ad(html_content):
    """Remove Jimdo advertisement from HTML content"""
    # Pattern to match the Jimdo free footer ad div
    pattern = r'<div class="jimdo-free-footer-ad\s*">.*?</div>\s*'
    cleaned = re.sub(pattern, '', html_content, flags=re.DOTALL)
    return cleaned

def process_html_files(root_dir):
    """Process all HTML files to remove Jimdo ads"""
    html_files = list(Path(root_dir).rglob('*.html'))
    processed_count = 0

    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if Jimdo ad exists
            if 'jimdo-free-footer-ad' in content:
                cleaned_content = remove_jimdo_ad(content)

                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                processed_count += 1
                print(f"Removed Jimdo ad from: {html_file}")
        except Exception as e:
            print(f"Error processing {html_file}: {e}")

    print(f"\nTotal files processed: {processed_count}")
    return processed_count

def fix_publications_404():
    """Copy correct content from students-alumni to publications for items with 404"""
    pub_dir = Path('publications')
    students_dir = Path('students-alumni')

    # Check mevar specifically first
    mevar_name = 'mevar-mobility-enhanced-vehicle-trajectory-reconstruction-with-camera-sensing-network'
    pub_mevar = pub_dir / mevar_name / 'index.html'
    students_mevar = students_dir / mevar_name / 'index.html'

    if pub_mevar.exists() and students_mevar.exists():
        try:
            # Read both files
            with open(pub_mevar, 'r', encoding='utf-8') as f:
                pub_content = f.read()
            with open(students_mevar, 'r', encoding='utf-8') as f:
                students_content = f.read()

            # Check if publication version has 404
            if 'Page Not Found' in pub_content or 'name="jimdo-status-code" content="404"' in pub_content:
                print(f"Found 404 in publications/{mevar_name}, copying from students-alumni...")

                # Remove Jimdo ad from the source content
                cleaned_content = remove_jimdo_ad(students_content)

                # Write to publications
                with open(pub_mevar, 'w', encoding='utf-8') as f:
                    f.write(cleaned_content)

                print(f"Successfully copied corrected content to publications/{mevar_name}")
                return True
            else:
                print(f"No 404 detected in publications/{mevar_name}")
        except Exception as e:
            print(f"Error fixing mevar publication: {e}")

    return False

if __name__ == '__main__':
    print("=" * 60)
    print("Starting website fixes...")
    print("=" * 60)

    # Fix the 404 issue
    print("\n1. Fixing publications 404 issue...")
    fix_publications_404()

    # Remove Jimdo ads from all HTML files
    print("\n2. Removing Jimdo advertisements...")
    process_html_files('.')

    print("\n" + "=" * 60)
    print("All fixes completed!")
    print("=" * 60)
