#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量清洗和规范化所有HTML文件
按照专业前端规范处理Jimdo静态网页
"""

import os
import sys
import re
from pathlib import Path
from bs4 import BeautifulSoup

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

WEB_DIR = Path("F:/bigscity-web/web")

# 全局CSS强制覆盖
GLOBAL_CSS = """
    <style>
        html, body {
            margin: 0;
        }
        .hidden { display: none; }
        .n { padding: 5px; }
        #emotion-header { position: relative; }
        #emotion-header-logo, #emotion-header-title { position: absolute; }

        /* 全局强制无衬线字体栈 */
        html, body, #cc-inner, #tp-container, #tp-content-wrapper, #content_area,
        #content_area *, .j-module, .j-text, .headline, h1, h2, h3, p, div, span, a, strong, em {
            font-family: Arial, "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif !important;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
    </style>"""

def clean_html_content(content):
    """清洗HTML内容"""

    # 1. 移除异常容器（ChatGPT界面元素）
    # 移除包含特定类的article标签及其包装，保留内部内容
    content = re.sub(
        r'<article[^>]*class="[^"]*text-token[^"]*"[^>]*>',
        '',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(r'</article>', '', content)

    # 移除包含user-message-bubble-color的div包装
    content = re.sub(
        r'<div[^>]*class="[^"]*user-message-bubble-color[^"]*"[^>]*>',
        '',
        content
    )

    # 移除whitespace-pre-wrap的div包装
    content = re.sub(
        r'<div[^>]*class="[^"]*whitespace-pre-wrap[^"]*"[^>]*>',
        '',
        content
    )

    # 清理多余的闭合div
    # 这个比较复杂，需要小心处理，这里简单处理

    # 2. 清除翻译扩展残留的脏属性
    # 移除 span="" 属性
    content = re.sub(r'\s+span=""', '', content)

    # 移除 id="tran_X_XX" 属性
    content = re.sub(r'\s+id="tran_\d+_\d+"', '', content)

    # 3. 移除所有 font-weight: 300
    content = re.sub(
        r'font-weight:\s*300;?',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 4. 移除 font-family: inherit !important
    content = re.sub(
        r'font-family:\s*inherit\s*!important;?',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 5. 统一邮箱格式（jywang@buaa.edu.cn）
    # 先找到邮箱，然后格式化
    email_pattern = r'jywang\s*@\s*buaa\.edu\.cn'

    def format_email(match):
        return '<strong style="color: #b85f00;"><a href="mailto:jywang@buaa.edu.cn" style="color: #b85f00; font-weight: bold; text-decoration: none;">jywang@buaa.edu.cn</a></strong>'

    # 匹配简单的邮箱文本并替换
    content = re.sub(
        r'(?<!href=")(?<!>)jywang@buaa\.edu\.cn(?!</a>)',
        lambda m: format_email(m) if '<a' not in content[max(0, m.start()-50):m.start()] else m.group(0),
        content
    )

    return content

def inject_global_css(content):
    """注入全局CSS"""

    # 检查是否已经有全局强制字体CSS
    if '全局强制无衬线字体栈' in content:
        return content  # 已经注入过了

    # 在</head>前注入
    if '</head>' in content:
        content = content.replace('</head>', f'{GLOBAL_CSS}\n</head>')

    return content

def process_html_file(html_path):
    """处理单个HTML文件"""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # 跳过重定向页面
        if '<META HTTP-EQUIV="Refresh"' in content:
            return False

        # 1. 清洗HTML内容
        content = clean_html_content(content)

        # 2. 注入全局CSS
        content = inject_global_css(content)

        if content != original:
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True

        return False

    except Exception as e:
        print(f"  ERROR processing {html_path.name}: {e}")
        return False

def main():
    """主函数"""
    print("=" * 70)
    print("批量清洗和规范化HTML文件")
    print("=" * 70)
    print()
    print("处理规则：")
    print("  1. 移除异常容器（ChatGPT UI元素）")
    print("  2. 清除翻译扩展脏属性")
    print("  3. 注入全局字体CSS强制覆盖")
    print("  4. 移除 font-weight: 300")
    print("  5. 统一邮箱格式")
    print()
    print("=" * 70)

    processed = 0
    skipped = 0
    errors = 0

    for html_file in WEB_DIR.rglob("*.html"):
        try:
            rel_path = html_file.relative_to(WEB_DIR)

            if process_html_file(html_file):
                processed += 1
                print(f"  ✓ Processed: {rel_path}")
            else:
                skipped += 1

        except Exception as e:
            errors += 1
            print(f"  ✗ Error: {html_file.name}: {e}")

    print()
    print("=" * 70)
    print("处理完成")
    print("=" * 70)
    print(f"  处理文件数: {processed}")
    print(f"  跳过文件数: {skipped}")
    print(f"  错误文件数: {errors}")
    print("=" * 70)

    if processed > 0:
        print()
        print("✓ HTML文件已规范化处理")
        print("  - 异常容器已清理")
        print("  - 全局字体CSS已注入")
        print("  - 字重已统一")
        print("  - 邮箱格式已规范")

if __name__ == "__main__":
    main()
