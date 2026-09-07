#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查所有HTML文件的字体CSS引用
"""

import os
import sys
import re
from pathlib import Path

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

WEB_DIR = Path("F:/bigscity-web/web")

def check_font_css(html_path):
    """检查HTML文件的字体CSS引用"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    issues = []

    # 检查是否引用了font CSS
    if 'jimdo_font_css' not in content:
        issues.append("Missing jimdo_font_css link")

    # 检查font CSS路径
    font_css_pattern = r'<link href="([^"]*font[^"]*\.css[^"]*)" rel="stylesheet"[^>]*id="jimdo_font_css"'
    font_css_match = re.search(font_css_pattern, content)

    if font_css_match:
        font_css_path = font_css_match.group(1)
        # 计算绝对路径
        if font_css_path.startswith('../'):
            # 相对路径，需要计算
            pass
        else:
            pass

        # 检查路径格式是否正确
        if 'u.jimcdn.com' not in font_css_path:
            issues.append(f"Unusual font CSS path: {font_css_path}")
    else:
        issues.append("Font CSS link not found")

    return issues

def main():
    """主函数"""
    print("=" * 70)
    print("Checking font CSS references")
    print("=" * 70)

    problem_files = []

    for html_file in WEB_DIR.rglob("*.html"):
        try:
            issues = check_font_css(html_file)
            if issues:
                problem_files.append((html_file, issues))
                print(f"\n{html_file.relative_to(WEB_DIR)}:")
                for issue in issues:
                    print(f"  - {issue}")
        except Exception as e:
            print(f"  ERROR: {html_file.name}: {e}")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  Problem files: {len(problem_files)}")

    if len(problem_files) == 0:
        print("\n✓ All files have proper font CSS references")

    print("=" * 70)

if __name__ == "__main__":
    main()
