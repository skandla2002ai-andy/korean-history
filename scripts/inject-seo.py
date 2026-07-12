#!/usr/bin/env python3
"""
inject-seo.py — 모든 articles/ 및 thoughts/ HTML에 SEO 태그 일괄 삽입
- meta description 없으면 lead 문장에서 추출해 추가
- Open Graph 태그 (og:title, og:description, og:url, og:type) 전체 추가/갱신
- canonical URL 추가
"""

import os
import re
from pathlib import Path

BASE_URL = "https://skandla2002ai-andy.github.io/korean-history"
SITE_NAME = "한국사 아카이브"


def extract_lead(html: str) -> str:
    """lead 클래스 p 태그에서 텍스트 추출"""
    m = re.search(r'<p class="lead">(.*?)</p>', html, re.DOTALL)
    if m:
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        return text[:150]
    # lead 없으면 첫 번째 <p> 텍스트
    m2 = re.search(r'<h2>[^<]*</h2>\s*<p>(.*?)</p>', html, re.DOTALL)
    if m2:
        text = re.sub(r'<[^>]+>', '', m2.group(1)).strip()
        return text[:150]
    return ""


def extract_title(html: str) -> str:
    m = re.search(r'<title>(.*?)</title>', html)
    return m.group(1).strip() if m else ""


def process_file(path: Path, base_dir: Path):
    html = path.read_text(encoding='utf-8')
    original = html

    # URL 계산
    rel = path.relative_to(base_dir).as_posix()
    page_url = f"{BASE_URL}/{rel}"

    title = extract_title(html)
    description = extract_lead(html)

    # 기존 description 추출 (있으면 유지)
    existing_desc = re.search(r'<meta name="description" content="([^"]*)"', html)
    if existing_desc and existing_desc.group(1).strip():
        description = existing_desc.group(1).strip()

    if not description:
        description = title

    # 삽입할 SEO 블록 구성
    seo_block = ""

    # 1) meta description — 없으면 추가
    if not existing_desc:
        seo_block += f'<meta name="description" content="{description}">\n'

    # 2) canonical — 없으면 추가
    if 'rel="canonical"' not in html:
        seo_block += f'<link rel="canonical" href="{page_url}">\n'

    # 3) Open Graph — 없으면 추가
    if 'og:title' not in html:
        seo_block += f'''<meta property="og:type" content="article">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{page_url}">
<meta property="og:locale" content="ko_KR">
'''

    # 4) Twitter Card — 없으면 추가
    if 'twitter:card' not in html:
        seo_block += f'''<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
'''

    if not seo_block:
        return False  # 변경 없음

    # </head> 직전에 삽입
    html = html.replace('</head>', seo_block + '</head>', 1)

    if html != original:
        path.write_text(html, encoding='utf-8')
        return True
    return False


def main():
    base_dir = Path(__file__).parent.parent
    targets = list(base_dir.glob('articles/*.html')) + list(base_dir.glob('thoughts/*.html'))

    updated = 0
    skipped = 0
    for path in sorted(targets):
        if process_file(path, base_dir):
            updated += 1
            print(f"  OK {path.relative_to(base_dir)}")
        else:
            skipped += 1

    print(f"\n완료: {updated}개 업데이트, {skipped}개 이미 최신")


if __name__ == '__main__':
    main()
