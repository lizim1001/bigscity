#!/usr/bin/env python3
"""
Unify routes by removing students-alumni content and redirecting to publications.
Since 93 out of 103 items in students-alumni are duplicated in publications,
we'll redirect those to publications and keep only the unique ones in students-alumni.
"""
import os
import shutil
from pathlib import Path

def get_duplicate_items():
    """Get list of duplicate items between publications and students-alumni"""
    pub_items = set(os.listdir('publications'))
    students_items = set(os.listdir('students-alumni'))
    duplicates = pub_items & students_items
    return sorted(duplicates)

def create_redirect_html(target_path, title="Publication"):
    """Create a simple redirect HTML page"""
    redirect_html = f'''<!DOCTYPE html>
<html lang="en-US">
<head>
    <meta charset="utf-8"/>
    <meta http-equiv="refresh" content="0; url={target_path}"/>
    <title>Redirecting...</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }}
        .message {{
            font-size: 18px;
            color: #333;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="message">
        <p>This page has been moved.</p>
        <p>Redirecting to <a href="{target_path}">publications</a>...</p>
        <p>If you are not redirected automatically, <a href="{target_path}">click here</a>.</p>
    </div>
</body>
</html>'''
    return redirect_html

def unify_routes():
    """Replace students-alumni duplicates with redirects to publications"""
    duplicates = get_duplicate_items()
    print(f"Found {len(duplicates)} duplicate items to redirect")

    redirected_count = 0

    for item in duplicates:
        students_path = Path('students-alumni') / item
        if students_path.exists() and students_path.is_dir():
            # Backup first
            backup_path = Path(f'students-alumni/.backup_{item}')
            if not backup_path.exists():
                shutil.move(str(students_path), str(backup_path))

            # Create redirect directory and index.html
            students_path.mkdir(parents=True, exist_ok=True)
            redirect_file = students_path / 'index.html'

            # Calculate relative path from students-alumni to publications
            target_path = f'../../publications/{item}/index.html'
            redirect_html = create_redirect_html(target_path)

            with open(redirect_file, 'w', encoding='utf-8') as f:
                f.write(redirect_html)

            redirected_count += 1
            if redirected_count <= 10:  # Show first 10
                print(f"  Redirected: students-alumni/{item} -> publications/{item}")

    print(f"\nTotal redirected: {redirected_count} items")
    print(f"Backups saved in students-alumni/.backup_* folders")

if __name__ == '__main__':
    print("=" * 70)
    print("Unifying routes: students-alumni -> publications")
    print("=" * 70)
    unify_routes()
    print("\n" + "=" * 70)
    print("Done!")
    print("=" * 70)
