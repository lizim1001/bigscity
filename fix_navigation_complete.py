#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复导航栏问题：
1. 删除重复的子菜单
2. 正确配置子菜单结构
3. 子菜单只在当前页面显示
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

def fix_navigation(html_path):
    """修复单个HTML文件的导航"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 计算相对路径前缀
    rel_depth = len(html_path.relative_to(WEB_DIR).parts) - 1
    rel_prefix = "../" * rel_depth if rel_depth > 0 else ""

    # 判断当前是哪个页面
    is_seminars_page = 'seminars' in str(html_path.relative_to(WEB_DIR))
    is_readings_page = 'readings' in str(html_path.relative_to(WEB_DIR))

    # 1. 删除所有现有的重复子菜单
    # 删除独立的<li><ul>子菜单块
    content = re.sub(
        r'<li><ul id="mainNav2" class="mainNav2">.*?</ul></li>',
        '',
        content,
        flags=re.DOTALL
    )

    # 2. 重建Seminars导航
    seminars_prefix = rel_prefix + "seminars/" if rel_depth > 0 else "seminars/"

    if is_seminars_page:
        # 在seminars相关页面，显示展开的子菜单
        seminars_nav = f'''<li id="cc-nav-view-2257750712"><a href="{seminars_prefix}index.html" class="level_1"><span>Seminars</span></a></li>
<li><ul id="mainNav2" class="mainNav2">
<li id="cc-nav-view-2284464912"><a href="{seminars_prefix}2024/index.html" class="level_2"><span>2024</span></a></li>
<li id="cc-nav-view-2258511212"><a href="{seminars_prefix}2023-1/index.html" class="level_2"><span>2023</span></a></li>
<li id="cc-nav-view-2258511312"><a href="{seminars_prefix}2022-1/index.html" class="level_2"><span>2022</span></a></li>
<li id="cc-nav-view-2260013812"><a href="{seminars_prefix}files/index.html" class="level_2"><span>files</span></a></li>
</ul></li>'''
    else:
        # 在其他页面，只显示主菜单项
        seminars_nav = f'<li id="cc-nav-view-2257750712"><a href="{seminars_prefix}index.html" class="level_1"><span>Seminars</span></a></li>'

    content = re.sub(
        r'<li id="cc-nav-view-2257750712"><a href="[^"]*"[^>]*><span>Seminars</span></a></li>',
        seminars_nav,
        content
    )

    # 3. 重建Readings导航
    readings_prefix = rel_prefix + "readings/" if rel_depth > 0 else "readings/"

    if is_readings_page:
        # 在readings相关页面，显示展开的子菜单
        readings_nav = f'''<li id="cc-nav-view-1436537587"><a href="{readings_prefix}index.html" class="level_1"><span>Readings</span></a></li>
<li><ul id="mainNav2" class="mainNav2">
<li id="cc-nav-view-1436537787"><a href="{readings_prefix}sp1/index.html" class="level_2"><span>SP1</span></a></li>
<li id="cc-nav-view-1436537987"><a href="{readings_prefix}sp1-1/index.html" class="level_2"><span>SP1-1</span></a></li>
<li id="cc-nav-view-1436538087"><a href="{readings_prefix}sp1-2/index.html" class="level_2"><span>SP1-2</span></a></li>
<li id="cc-nav-view-1436538387"><a href="{readings_prefix}sp1-3/index.html" class="level_2"><span>SP1-3</span></a></li>
<li id="cc-nav-view-1436555187"><a href="{readings_prefix}sp1-3-2/index.html" class="level_2"><span>SP1-3-2</span></a></li>
<li id="cc-nav-view-1436538287"><a href="{readings_prefix}sp1-4/index.html" class="level_2"><span>SP1-4</span></a></li>
<li id="cc-nav-view-1436538487"><a href="{readings_prefix}sp1-5/index.html" class="level_2"><span>SP1-5</span></a></li>
<li id="cc-nav-view-1436538787"><a href="{readings_prefix}sp1-6/index.html" class="level_2"><span>SP1-6</span></a></li>
<li id="cc-nav-view-1436545387"><a href="{readings_prefix}special-issues/index.html" class="level_2"><span>Special Issues</span></a></li>
<li id="cc-nav-view-2210914512"><a href="{readings_prefix}visualizations/index.html" class="level_2"><span>Visualizations</span></a></li>
</ul></li>'''
    else:
        # 在其他页面，只显示主菜单项
        readings_nav = f'<li id="cc-nav-view-1436537587"><a href="{readings_prefix}index.html" class="level_1"><span>Readings</span></a></li>'

    content = re.sub(
        r'<li id="cc-nav-view-1436537587"><a href="[^"]*"[^>]*><span>Readings</span></a></li>',
        readings_nav,
        content
    )

    if content != original:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    """主函数"""
    print("=" * 70)
    print("Fixing navigation menus")
    print("=" * 70)

    fixed_count = 0

    # 处理所有HTML文件
    for html_file in WEB_DIR.rglob("*.html"):
        try:
            if fix_navigation(html_file):
                fixed_count += 1
                rel_path = html_file.relative_to(WEB_DIR)
                is_seminars = 'seminars' in str(rel_path)
                is_readings = 'readings' in str(rel_path)
                
                status = []
                if is_seminars:
                    status.append("Seminars+submenu")
                if is_readings:
                    status.append("Readings+submenu")
                    
                if status:
                    print(f"  Fixed: {rel_path} [{', '.join(status)}]")
                else:
                    print(f"  Fixed: {rel_path}")

        except Exception as e:
            print(f"  ERROR: {html_file.name}: {e}")

    print("\n" + "=" * 70)
    print("Summary")
    print("=" * 70)
    print(f"  Files fixed: {fixed_count}")
    print("=" * 70)

if __name__ == "__main__":
    main()
