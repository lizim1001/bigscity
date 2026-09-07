#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复readings导航：移除SP系列，只保留Special Issues和Visualizations
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

def fix_readings_nav(html_path):
    """修复readings导航，移除SP系列"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 计算相对路径前缀
    rel_depth = len(html_path.relative_to(WEB_DIR).parts) - 1
    rel_prefix = "../" * rel_depth if rel_depth > 0 else ""
    readings_prefix = rel_prefix + "readings/" if rel_depth > 0 else "readings/"

    # 判断是否是readings相关页面
    is_readings_page = 'readings' in str(html_path.relative_to(WEB_DIR))

    if is_readings_page:
        # 在readings页面，显示简化的子菜单（只有Special Issues和Visualizations）
        readings_nav = f'''<li id="cc-nav-view-1436537587"><a href="{readings_prefix}index.html" class="level_1"><span>Readings</span></a></li>
<li><ul id="mainNav2" class="mainNav2">
<li id="cc-nav-view-1436545387"><a href="{readings_prefix}special-issues/index.html" class="level_2"><span>Special Issues</span></a></li>
<li id="cc-nav-view-2210914512"><a href="{readings_prefix}visualizations/index.html" class="level_2"><span>Visualizations</span></a></li>
</ul></li>'''
    else:
        # 在其他页面，只显示主菜单项
        readings_nav = f'<li id="cc-nav-view-1436537587"><a href="{readings_prefix}index.html" class="level_1"><span>Readings</span></a></li>'

    # 替换readings导航
    # 首先找到readings nav及其后面的子菜单
    pattern = r'<li id="cc-nav-view-1436537587">.*?</a></li>\s*(?:<li><ul id="mainNav2".*?</ul></li>\s*)?'

    new_content = re.sub(pattern, readings_nav, content, flags=re.DOTALL)

    if new_content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """主函数"""
    print("=" * 70)
    print("Fixing readings navigation (removing SP series)")
    print("=" * 70)

    fixed_count = 0

    for html_file in WEB_DIR.rglob("*.html"):
        try:
            if fix_readings_nav(html_file):
                fixed_count += 1
                rel_path = html_file.relative_to(WEB_DIR)
                is_readings = 'readings' in str(rel_path)

                if is_readings:
                    print(f"  Fixed: {rel_path} [Readings+submenu (no SP)]")
                else:
                    print(f"  Fixed: {rel_path}")

        except Exception as e:
            print(f"  ERROR: {html_file.name}: {e}")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  Files fixed: {fixed_count}")
    print(f"  Readings submenu now only shows: Special Issues, Visualizations")
    print("=" * 70)

if __name__ == "__main__":
    main()
