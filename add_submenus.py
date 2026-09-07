#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为seminars和readings添加子菜单导航
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

def add_seminars_submenu(html_path):
    """为seminars页面添加子菜单"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 计算相对路径前缀
    rel_depth = len(html_path.relative_to(WEB_DIR).parts) - 1
    rel_prefix = "../" * rel_depth if rel_depth > 0 else ""

    seminars_prefix = rel_prefix + "seminars/" if rel_depth > 0 else "seminars/"

    # 查找Seminars的导航项
    pattern = r'(<li id="cc-nav-view-2257750712"><a href="[^"]*seminars/index\.html"[^>]*><span>Seminars</span></a></li>)'

    
    # 创建带子菜单的Seminars项
    submenu = f'''<li id="cc-nav-view-2257750712"><a href="{seminars_prefix}index.html" class="level_1"><span>Seminars</span></a></li>
<li><ul id="mainNav2" class="mainNav2">
<li id="cc-nav-view-2284464912"><a href="{seminars_prefix}2024/index.html" class="level_2"><span>2024</span></a></li>
<li id="cc-nav-view-2258511212"><a href="{seminars_prefix}2023-1/index.html" class="level_2"><span>2023</span></a></li>
<li id="cc-nav-view-2258511312"><a href="{seminars_prefix}2022-1/index.html" class="level_2"><span>2022</span></a></li>
<li id="cc-nav-view-2260013812"><a href="{seminars_prefix}files/index.html" class="level_2"><span>files</span></a></li>
</ul></li>'''
    
    new_content = re.sub(pattern, submenu, content)
    
    if new_content != content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def add_readings_submenu(html_path):
    """为readings页面添加子菜单"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 计算相对路径前缀
    rel_depth = len(html_path.relative_to(WEB_DIR).parts) - 1
    rel_prefix = "../" * rel_depth if rel_depth > 0 else ""

    readings_prefix = rel_prefix + "readings/" if rel_depth > 0 else "readings/"

    # 查找Readings的导航项
    pattern = r'(<li id="cc-nav-view-1436537587"><a href="[^"]*readings/index\.html"[^>]*><span>Readings</span></a></li>)'
    
    # 创建带子菜单的Readings项
    submenu = f'''<li id="cc-nav-view-1436537587"><a href="{readings_prefix}index.html" class="level_1"><span>Readings</span></a></li>
<li><ul id="mainNav2" class="mainNav2">
<li id="cc-nav-view-special-issues"><a href="{readings_prefix}special-issues/index.html" class="level_2"><span>Special Issues</span></a></li>
</ul></li>'''
    
    new_content = re.sub(pattern, submenu, content)
    
    if new_content != content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def add_visualizations_menu(html_path):
    """为visualizations添加菜单项（如果缺失）"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 检查是否已有visualizations菜单项
    if 'cc-nav-view-1436540387' in content:
        return False  # 已存在

    # 计算相对路径前缀
    rel_depth = len(html_path.relative_to(WEB_DIR).parts) - 1
    rel_prefix = "../" * rel_depth if rel_depth > 0 else ""

    viz_prefix = rel_prefix + "visualizations/" if rel_depth > 0 else "visualizations/"

    # 在LibCity后面插入Visualizations
    pattern = r'(<li id="cc-nav-view-2232851312"><a href="[^"]*libcity/index\.html"[^>]*><span>LibCity</span></a></li>)'
    
    replacement = r'\1\n<li id="cc-nav-view-1436540387"><a href="' + viz_prefix + 'index.html" class="level_1"><span>Visualizations</span></a></li>'
    
    new_content = re.sub(pattern, replacement, content)
    
    if new_content != content:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def main():
    """主函数"""
    print("=" * 70)
    print("Adding submenus to navigation")
    print("=" * 70)

    seminars_updated = 0
    readings_updated = 0
    viz_updated = 0

    # 处理所有HTML文件
    for html_file in WEB_DIR.rglob("*.html"):
        try:
            # 添加Seminars子菜单
            if add_seminars_submenu(html_file):
                seminars_updated += 1
                print(f"  Seminars submenu: {html_file.relative_to(WEB_DIR)}")

            # 添加Readings子菜单
            if add_readings_submenu(html_file):
                readings_updated += 1
                print(f"  Readings submenu: {html_file.relative_to(WEB_DIR)}")

            # 添加Visualizations菜单项
            if add_visualizations_menu(html_file):
                viz_updated += 1
                print(f"  Visualizations menu: {html_file.relative_to(WEB_DIR)}")

        except Exception as e:
            print(f"  ERROR: {html_file.name}: {e}")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  Seminars submenu added: {seminars_updated} files")
    print(f"  Readings submenu added: {readings_updated} files")
    print(f"  Visualizations menu added: {viz_updated} files")
    print("=" * 70)

if __name__ == "__main__":
    main()
