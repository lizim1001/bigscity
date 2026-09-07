#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查并修复可能影响字体的CSS类
特别检查包含ChatGPT界面类的元素
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
HTTRACK_DIR = Path("F:/bigscity-web/httrack/bigscity-web/smartcity-buaa.jimdoweb.com")

def compare_file_with_original(html_path):
    """对比文件与HTTrack原始文件，查找差异"""
    rel_path = html_path.relative_to(WEB_DIR)
    original_path = HTTRACK_DIR / rel_path

    if not original_path.exists():
        return None

    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            current = f.read()

        with open(original_path, 'r', encoding='utf-8') as f:
            original = f.read()

        # 检查是否有不同
        if current != original:
            # 查找特定的问题模式
            issues = []

            # 检查是否有text-token类（ChatGPT界面元素）
            if 'text-token' in current and 'text-token' not in original:
                issues.append("ChatGPT UI classes added")

            # 检查字体CSS引用
            current_font_css = re.search(r'href="([^"]*font[^"]*\.css[^"]*)"', current)
            original_font_css = re.search(r'href="([^"]*font[^"]*\.css[^"]*)"', original)

            if current_font_css and original_font_css:
                if current_font_css.group(1) != original_font_css.group(1):
                    issues.append(f"Font CSS path differs: {current_font_css.group(1)} vs {original_font_css.group(1)}")

            return issues if issues else ["File modified"]

        return None

    except Exception as e:
        return [f"Error: {str(e)}"]

def main():
    """主函数"""
    print("=" * 70)
    print("Comparing files with HTTrack originals")
    print("=" * 70)

    modified_files = []

    # 只检查主要页面
    important_files = [
        "index.html",
        "jingyuan-wang/index.html",
        "publications/index.html",
        "readings/index.html",
        "seminars/index.html"
    ]

    for rel_path_str in important_files:
        html_path = WEB_DIR / rel_path_str
        if not html_path.exists():
            continue

        issues = compare_file_with_original(html_path)
        if issues:
            modified_files.append((rel_path_str, issues))
            print(f"\n{rel_path_str}:")
            for issue in issues:
                print(f"  - {issue}")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  Modified files: {len(modified_files)}")

    if len(modified_files) == 0:
        print("\n✓ All checked files match originals")
    else:
        print("\n⚠ Files have been modified from originals")
        print("  This might affect font rendering")

    print("=" * 70)

if __name__ == "__main__":
    main()
