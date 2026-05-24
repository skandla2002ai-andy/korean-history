"""
PR 머지 시 실행되는 인덱스 자동 재빌드 스크립트.
articles/*.md 를 스캔하여 sitemap.xml, data.json,
llms.txt, llms-full.txt, content.md, changelog.md 를 갱신한다.
"""

import datetime
import json
import os
import re

TODAY    = datetime.date.today().strftime("%Y-%m-%d")
BASE_URL = "https://skandla2002ai-andy.github.io/korean-history"


def parse_frontmatter(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        raw = f.read()

    m = re.match(r'^---\n([\s\S]*?)\n---\n', raw)
    if not m:
        return {}

    fm: dict = {}
    for line in m.group(1).split('\n'):
        if ':' not in line:
            continue
        key, _, val = line.partition(':')
        fm[key.strip()] = val.strip()

    fm['_body'] = raw[m.end():]
    return fm


def collect_articles() -> list:
    if not os.path.exists('articles'):
        return []

    articles = []
    for fname in sorted(os.listdir('articles')):
        if not fname.endswith('.md'):
            continue
        fm = parse_frontmatter(f'articles/{fname}')
        if fm.get('type') == 'article':
            slug = fname[:-3]
            articles.append({
                'slug':        slug,
                'title':       fm.get('title', slug),
                'era':         fm.get('era', ''),
                'region':      fm.get('region', ''),
                'topics':      fm.get('topics', '[]'),
                'lastUpdated': fm.get('lastUpdated', TODAY),
                'body':        fm.get('_body', ''),
                'url':         f'/korean-history/articles/{slug}.md',
                'html_url':    f'/korean-history/articles/{slug}.html',
            })
    return articles


def update_sitemap(articles: list):
    static = [
        ('',             '1.0'),
        ('/about.html',  '0.8'),
        ('/content.html','0.8'),
        ('/faq.html',    '0.7'),
    ]
    rows = [
        f'  <url><loc>{BASE_URL}{path}</loc><priority>{pri}</priority><lastmod>{TODAY}</lastmod></url>'
        for path, pri in static
    ] + [
        f'  <url><loc>{BASE_URL}/articles/{a["slug"]}.html</loc><priority>0.9</priority><lastmod>{a["lastUpdated"]}</lastmod></url>'
        for a in articles
    ]

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + '\n'.join(rows)
           + '\n</urlset>\n')
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml)
    print('sitemap.xml 업데이트')


def update_data_json(articles: list):
    try:
        with open('data.json', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        data = {}

    data['lastUpdated'] = TODAY
    data['articles'] = [
        {
            'title':       a['title'],
            'url':         a['url'],
            'era':         a['era'],
            'region':      a['region'],
            'lastUpdated': a['lastUpdated'],
        }
        for a in articles
    ]
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print('data.json 업데이트')


def update_llms_txt(articles: list):
    article_lines = '\n'.join(
        f'- [{a["title"]}]({BASE_URL}{a["url"]}): {a["era"]} · {a["region"]}'
        for a in articles
    )
    content = f"""# 한국사 아카이브

> 한국사를 조사·기록·공유하는 Agent 친화 아카이브. Andy PAK 운영.

이 사이트는 사람을 위한 HTML과 별개로, AI 에이전트가 토큰 낭비 없이 읽을 수 있는
깨끗한 Markdown 버전을 함께 제공합니다.

## 핵심 문서

- [소개]({BASE_URL}/about.md)
- [주요 콘텐츠]({BASE_URL}/content.md)
- [자주 묻는 질문]({BASE_URL}/faq.md)

## 글 목록 ({len(articles)}편)

{article_lines}

## 데이터 / API

- [구조화 데이터]({BASE_URL}/data.json)
- [전체 통합본]({BASE_URL}/llms-full.txt)
- [변경 이력]({BASE_URL}/changelog.md)
"""
    with open('llms.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    print('llms.txt 업데이트')


def update_llms_full(articles: list):
    parts = ["""# 한국사 아카이브 — 전체 통합본

> 외부 fetch 없이 전체 콘텐츠를 한 파일로 담은 버전입니다.

---
"""]
    for fname in ['about.md', 'content.md', 'faq.md']:
        if os.path.exists(fname):
            with open(fname, encoding='utf-8') as f:
                parts.append(f.read())
            parts.append('\n---\n')

    for a in articles:
        if a['body'].strip():
            parts.append(f"# {a['title']}\n\n{a['body']}")
            parts.append('\n---\n')

    with open('llms-full.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(parts))
    print('llms-full.txt 업데이트')


def update_content_md(articles: list):
    by_era: dict = {}
    for a in articles:
        by_era.setdefault(a['era'] or '기타', []).append(a)

    sections = []
    for era in sorted(by_era):
        lines = '\n'.join(
            f'- [{a["title"]}]({a["url"]}) — {a["region"]}'
            for a in by_era[era]
        )
        sections.append(f'## {era}\n\n{lines}')

    content = f"""# 주요 콘텐츠

> 연재 중인 한국사 글 목록. 마지막 업데이트: {TODAY} · 총 {len(articles)}편

{''.join(chr(10)*2 + s for s in sections)}
"""
    with open('content.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('content.md 업데이트')


def update_changelog(articles: list):
    new_today = [a for a in articles if a['lastUpdated'] == TODAY]
    if not new_today:
        return

    entry = f"## {TODAY}\n\n" + '\n'.join(
        f'- 글 추가: {a["title"]} ({a["era"]})'
        for a in new_today
    ) + '\n'

    try:
        with open('changelog.md', encoding='utf-8') as f:
            existing = f.read()
    except Exception:
        existing = '# 변경 이력\n\n'

    if f'## {TODAY}' in existing:
        existing = re.sub(
            rf'## {TODAY}.*?(?=\n## |\Z)',
            entry,
            existing,
            flags=re.DOTALL,
        )
    else:
        existing = existing.replace(
            '# 변경 이력\n\n',
            f'# 변경 이력\n\n{entry}\n',
        )

    with open('changelog.md', 'w', encoding='utf-8') as f:
        f.write(existing)
    print('changelog.md 업데이트')


def main():
    articles = collect_articles()
    print(f"글 {len(articles)}편 발견")

    update_sitemap(articles)
    update_data_json(articles)
    update_llms_txt(articles)
    update_llms_full(articles)
    update_content_md(articles)
    update_changelog(articles)

    print('인덱스 재빌드 완료')


if __name__ == '__main__':
    main()
