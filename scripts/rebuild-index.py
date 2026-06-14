#!/usr/bin/env python3
"""
전체 인덱스 자동 재생성 스크립트
실행: python scripts/rebuild-index.py

출력:
  - llms.txt        에이전트용 인덱스
  - data.json       구조화 데이터
  - content.html    전체 글 목록 (최신순, NEW 배지)
  - index.html      홈페이지 (최근 5편 카드)
"""

import re
import json
import sys
from pathlib import Path
from datetime import date, datetime, timedelta

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT     = Path(__file__).parent.parent
BASE_URL = "https://skandla2002ai-andy.github.io/korean-history"
ARTICLES = ROOT / "articles"
QUEUE    = ROOT / "_queue" / "articles"
THOUGHTS = ROOT / "thoughts"
TODAY    = date.today().isoformat()
NEW_DAYS = 7   # 이 기간 내 발행된 글에 NEW 배지

# ──────────────────────────────────────────────
# 파싱 헬퍼
# ──────────────────────────────────────────────

def read_utf8(path):
    return path.read_text(encoding="utf-8")

def extract_title(html):
    m = re.search(r'<title>(.+?) — 한국사 아카이브</title>', html)
    return m.group(1).strip() if m else ""

def extract_description(html):
    m = re.search(r'<meta name="description" content="([^"]+)"', html)
    return m.group(1).strip() if m else ""

def extract_lead(html):
    m = re.search(r'<p class="lead">([^<]+)</p>', html)
    return m.group(1).strip() if m else ""

def extract_published_date(html, fallback_path):
    """<meta name="published" content="YYYY-MM-DD"> 우선, 없으면 파일 수정일"""
    m = re.search(r'<meta name="published" content="([^"]+)"', html)
    if m:
        return m.group(1).strip()
    # 파일 수정 시간 fallback
    mtime = fallback_path.stat().st_mtime
    return datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")

def extract_tags(html):
    result = {"era": [], "topics": [], "related": [], "region": []}
    for cat, _b, val in re.findall(
        r'href="/korean-history/(era|topics|related|region)/[^"]+\.html"[^>]*>(<b>[^<]+</b>\s*)([^<]+)',
        html
    ):
        v = val.strip()
        if v:
            result[cat].append(v)
    return result

def article_num(path):
    m = re.match(r'^(\d{3})-', path.stem)
    return int(m.group(1)) if m else 9999

def pub_url(path):
    return f"{BASE_URL}/{path.relative_to(ROOT).as_posix()}"

def is_new(published_date_str):
    try:
        d = date.fromisoformat(published_date_str)
        return (date.today() - d).days <= NEW_DAYS
    except Exception:
        return False

# ──────────────────────────────────────────────
# 글 목록 수집
# ──────────────────────────────────────────────

def collect_articles():
    entries = []

    # 발행된 글 (articles/)
    for f in sorted(ARTICLES.glob("*.html")):
        html = read_utf8(f)
        tags = extract_tags(html)
        pub_date = extract_published_date(html, f)
        slug = f.stem

        # 연결된 편집자 글 찾기
        editor_html = THOUGHTS / f"{slug}-editor.html"
        editor = None
        if editor_html.exists():
            eh = read_utf8(editor_html)
            editor = {
                "title": extract_title(eh),
                "url": f"/korean-history/thoughts/{slug}-editor.html",
            }

        entries.append({
            "num":           9999,
            "slug":          slug,
            "filename":      f.name,
            "title":         extract_title(html),
            "description":   extract_description(html) or extract_lead(html),
            "era":           tags["era"],
            "topics":        tags["topics"],
            "related":       tags["related"],
            "region":        tags["region"],
            "html_url":      pub_url(f),
            "md_url":        pub_url(f).replace(".html", ".md"),
            "published":     pub_date,
            "is_new":        is_new(pub_date),
            "editor":        editor,
            "source":        "published",
        })

    # 큐 글 (_queue/articles/)
    for f in sorted(QUEUE.glob("*.html"), key=article_num):
        html = read_utf8(f)
        tags = extract_tags(html)
        num  = article_num(f)
        slug = re.sub(r'^\d{3}-', '', f.stem)
        entries.append({
            "num":           num,
            "slug":          slug,
            "filename":      f.name,
            "title":         extract_title(html),
            "description":   extract_description(html) or extract_lead(html),
            "era":           tags["era"],
            "topics":        tags["topics"],
            "related":       tags["related"],
            "region":        tags["region"],
            "html_url":      pub_url(f),
            "md_url":        pub_url(f).replace(".html", ".md"),
            "published":     None,
            "is_new":        False,
            "editor":        None,
            "source":        "queue",
        })

    return entries

# ──────────────────────────────────────────────
# 1. llms.txt
# ──────────────────────────────────────────────

def build_llms_txt(entries):
    published = [e for e in entries if e["source"] == "published"]
    queued    = [e for e in entries if e["source"] == "queue"]

    # 최신순 정렬
    published_sorted = sorted(published, key=lambda e: e["published"] or "", reverse=True)

    lines = [
        "# 한국사 아카이브",
        "",
        "> 한국사를 조사·기록·공유하는 Agent 친화 아카이브. Andy PAK 운영.",
        "> 사실 기반 본문(article)과 편집자 해석(commentary)을 분리하여 제공합니다.",
        "",
        "## 에이전트 빠른 시작",
        "",
        f"- 사이트 인덱스: {BASE_URL}/llms.txt",
        f"- 전체 통합본:   {BASE_URL}/llms-full.txt",
        f"- 구조화 데이터: {BASE_URL}/data.json",
        f"- 에이전트 가이드: {BASE_URL}/AGENTS.md",
        "",
        "## 핵심 문서",
        "",
        f"- [소개]({BASE_URL}/about.md)",
        f"- [주요 콘텐츠]({BASE_URL}/content.md)",
        f"- [자주 묻는 질문]({BASE_URL}/faq.md)",
        "",
        "## 태그 인덱스 (교차 탐색)",
        "",
        f"- 시대별: {BASE_URL}/era/",
        f"- 주제별: {BASE_URL}/topics/",
        f"- 관련국: {BASE_URL}/related/",
        f"- 지역별: {BASE_URL}/region/",
        "",
        "## 출처 데이터베이스",
        "",
        f"- {BASE_URL}/_data/sources.json  (신뢰점수 1~5 · 23개 공식 기관)",
        "",
        f"## 발행 완료 ({len(published_sorted)}편 · 최신순 · 갱신 {TODAY})",
        "",
    ]
    for e in published_sorted:
        parts = list(filter(None, e["era"] + e["region"]))
        meta  = " · ".join(parts)
        new_  = " [NEW]" if e["is_new"] else ""
        lines.append(f"- [{e['title']}]({e['md_url']}){': ' + meta if meta else ''}{new_}")
    lines.append("")

    lines += [
        f"## 발행 예정 큐 ({len(queued)}편)",
        "",
    ]
    for e in queued:
        parts = list(filter(None, e["era"] + e["region"]))
        meta  = " · ".join(parts)
        lines.append(f"- [{e['num']:03d}. {e['title']}]({e['html_url']}){': ' + meta if meta else ''}")
    lines.append("")

    lines += [
        "## 라이선스",
        "",
        "콘텐츠: CC BY 4.0 — 출처(사이트명 + 원문 링크) 표시 후 자유롭게 사용 가능.",
        "코드: MIT License.",
    ]
    return "\n".join(lines) + "\n"

# ──────────────────────────────────────────────
# 2. data.json
# ──────────────────────────────────────────────

def build_data_json(entries):
    published = [e for e in entries if e["source"] == "published"]
    queued    = [e for e in entries if e["source"] == "queue"]

    def to_dict(e):
        d = {
            "title":       e["title"],
            "description": e["description"],
            "html_url":    e["html_url"],
            "md_url":      e["md_url"],
            "era":         e["era"],
            "topics":      e["topics"],
            "related":     e["related"],
            "region":      e["region"],
            "num":         e["num"] if e["num"] != 9999 else None,
            "published":   e["published"],
            "is_new":      e["is_new"],
            "status":      e["source"],
        }
        if e.get("editor"):
            d["editor"] = e["editor"]
        return d

    data = {
        "name":        "한국사 아카이브",
        "url":         BASE_URL,
        "description": "한국사를 조사·기록·공유하는 Agent 친화 아카이브",
        "author":      "Andy PAK",
        "license":     "CC BY 4.0",
        "language":    "ko",
        "lastUpdated": TODAY,
        "stats": {
            "total":     len(entries),
            "published": len(published),
            "queued":    len(queued),
            "new":       sum(1 for e in published if e["is_new"]),
        },
        "endpoints": {
            "llms_txt":  f"{BASE_URL}/llms.txt",
            "llms_full": f"{BASE_URL}/llms-full.txt",
            "data_json": f"{BASE_URL}/data.json",
            "sources":   f"{BASE_URL}/_data/sources.json",
            "agents_md": f"{BASE_URL}/AGENTS.md",
            "sitemap":   f"{BASE_URL}/sitemap.xml",
        },
        "tag_indexes": {
            "era":     f"{BASE_URL}/era/",
            "topics":  f"{BASE_URL}/topics/",
            "related": f"{BASE_URL}/related/",
            "region":  f"{BASE_URL}/region/",
        },
        "pages": [
            {"title": "소개",           "url": f"{BASE_URL}/about.md"},
            {"title": "주요 콘텐츠",   "url": f"{BASE_URL}/content.md"},
            {"title": "자주 묻는 질문","url": f"{BASE_URL}/faq.md"},
        ],
        "articles": sorted(
            [to_dict(e) for e in published],
            key=lambda x: x["published"] or "",
            reverse=True
        ),
        "queue": [to_dict(e) for e in queued],
    }
    return json.dumps(data, ensure_ascii=False, indent=2)

# ──────────────────────────────────────────────
# 3. content.html — 전체 글 목록 (최신순 + NEW)
# ──────────────────────────────────────────────

ERA_ORDER = ["고조선", "삼국", "신라", "통일신라", "고려", "조선", "조선 후기", "일제강점기", "근현대", "현대"]

def era_sort_key(era_list):
    if not era_list:
        return 99
    era = era_list[0]
    for i, e in enumerate(ERA_ORDER):
        if e in era:
            return i
    return 50

def build_content_html(entries):
    published = sorted(
        [e for e in entries if e["source"] == "published"],
        key=lambda e: e["published"] or "",
        reverse=True   # 최신순
    )

    # 시대별 그룹화 (최신순 내에서 시대 헤더는 첫 등장 순)
    groups = {}
    group_order = []
    for e in published:
        era = e["era"][0] if e["era"] else "기타"
        if era not in groups:
            groups[era] = []
            group_order.append(era)
        groups[era].append(e)

    new_badge = '<span class="badge-new">NEW</span>'

    css = """<style>
  :root{--bg:#faf8f3;--ink:#1a1a17;--muted:#6b6862;--accent:#c2410c;
    --line:#e3ddd0;--fact:#1f5c3d;--opinion:#9a6b1c;--tag-bg:#ece5d6;--new:#1f5c3d}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--ink);
    font-family:'Iowan Old Style','Palatino Linotype',Georgia,serif;
    line-height:1.65;-webkit-font-smoothing:antialiased}
  .wrap{max-width:720px;margin:0 auto;padding:5rem 1.5rem 6rem}
  .eyebrow{font-family:'SF Mono','Menlo',monospace;font-size:.72rem;
    letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin-bottom:1.4rem}
  h1{font-size:clamp(2.2rem,5vw,3rem);line-height:1.05;
    letter-spacing:-.02em;font-weight:600;margin-bottom:1.5rem}
  .lead{font-size:1.2rem;color:var(--muted);margin-bottom:3rem;max-width:36ch}
  h2{font-size:1.05rem;font-family:'SF Mono','Menlo',monospace;
    letter-spacing:.04em;margin:3rem 0 1rem;padding-top:2rem;
    border-top:1px solid var(--line);font-weight:500}
  .article-group{margin-bottom:2.5rem}
  .article-row{display:flex;flex-direction:column;gap:.35rem;
    padding:.9rem 0;border-bottom:1px solid var(--line)}
  .article-row:last-child{border-bottom:none}
  .article-title{font-weight:600;font-size:1rem;display:flex;align-items:center;gap:.5rem}
  .article-title a{color:var(--ink);text-decoration:none}
  .article-title a:hover{color:var(--accent)}
  .article-meta{display:flex;flex-wrap:wrap;gap:.4rem;align-items:center}
  .badge{font-family:'SF Mono','Menlo',monospace;font-size:.7rem;padding:.2em .6em;border-radius:5px}
  .badge-article{background:rgba(31,92,61,.1);color:var(--fact)}
  .badge-new{background:var(--new);color:#fff;font-family:'SF Mono','Menlo',monospace;
    font-size:.65rem;font-weight:700;padding:.2em .55em;border-radius:4px;letter-spacing:.06em}
  .badge-date{font-family:'SF Mono','Menlo',monospace;font-size:.68rem;color:var(--muted)}
  .tag{font-family:'SF Mono','Menlo',monospace;font-size:.72rem;
    background:var(--tag-bg);padding:.2em .55em;border-radius:5px;color:var(--muted)}
  .commentary-row{display:flex;align-items:baseline;gap:.5rem;
    padding:.5rem 0 .5rem 1.2rem;border-bottom:1px solid var(--line);font-size:.92rem}
  .commentary-row:last-child{border-bottom:none}
  .commentary-row a{color:var(--opinion);text-decoration:none}
  .commentary-row a:hover{text-decoration:underline}
  .commentary-prefix{font-family:'SF Mono','Menlo',monospace;font-size:.68rem;
    color:var(--opinion);white-space:nowrap}
  .nav{margin-bottom:2rem;font-family:'SF Mono','Menlo',monospace;font-size:.8rem}
  .nav a{color:var(--accent);text-decoration:none}
  a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
  footer{margin-top:4rem;padding-top:2rem;border-top:1px solid var(--line);
    color:var(--muted);font-size:.85rem;font-family:'SF Mono','Menlo',monospace}
</style>"""

    lines = [
        '<!DOCTYPE html>',
        '<html lang="ko">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'<title>주요 콘텐츠 — 한국사 아카이브</title>',
        '<meta name="description" content="연재 중인 한국사 글 목록. 최신순 정렬, 7일 이내 발행 글에 NEW 표시.">',
        '<link rel="alternate" type="text/markdown" href="/korean-history/content.md">',
        css,
        '</head>',
        '<body>',
        '<main class="wrap">',
        '  <div class="nav"><a href="/korean-history/">← 한국사 아카이브</a></div>',
        '  <div class="eyebrow">Contents</div>',
        f'  <h1>주요 콘텐츠</h1>',
        f'  <p class="lead">발행된 글 {len(published)}편 · 최신순 정렬 · <span style="background:#1f5c3d;color:#fff;font-family:monospace;font-size:.75rem;padding:.15em .5em;border-radius:4px">NEW</span> = 7일 이내 발행</p>',
    ]

    for era in group_order:
        articles = groups[era]
        lines.append(f'  <h2>// {era}</h2>')
        lines.append('  <div class="article-group">')
        for e in articles:
            art_url  = f'/korean-history/articles/{e["slug"]}.html'
            tags_html = ""
            for t in (e["era"] + e["topics"])[:4]:
                tags_html += f'<span class="tag">{t}</span>'
            new_html  = f'  {new_badge}' if e["is_new"] else ""
            date_html = f'<span class="badge-date">{e["published"]}</span>' if e["published"] else ""
            lines += [
                '    <div class="article-row">',
                f'      <div class="article-title"><a href="{art_url}">{e["title"]}</a>{new_html}</div>',
                f'      <div class="article-meta"><span class="badge badge-article">● article</span>{date_html}{tags_html}</div>',
                '    </div>',
            ]
            if e.get("editor"):
                ed = e["editor"]
                lines += [
                    '    <div class="commentary-row">',
                    f'      <span class="commentary-prefix">✎ commentary</span>',
                    f'      <a href="{ed["url"]}">{ed["title"]}</a>',
                    '    </div>',
                ]
        lines.append('  </div>')

    lines += [
        '  <footer>',
        f'    총 {len(published)}편 발행 · 최종 갱신 {TODAY}<br>',
        '    Markdown 버전: <a href="/korean-history/content.md">/content.md</a><br>',
        '    CC BY 4.0 Andy PAK',
        '  </footer>',
        '</main>',
        '</body>',
        '</html>',
    ]
    return "\n".join(lines) + "\n"

# ──────────────────────────────────────────────
# 4. index.html — 홈 (최근 5편 카드 + NEW)
# ──────────────────────────────────────────────

def build_index_html(entries):
    published = sorted(
        [e for e in entries if e["source"] == "published"],
        key=lambda e: e["published"] or "",
        reverse=True
    )
    recent   = published[:5]
    total_p  = len(published)
    total_q  = sum(1 for e in entries if e["source"] == "queue")

    new_badge = '<span style="background:#1f5c3d;color:#fff;font-family:\'SF Mono\',monospace;font-size:.65rem;font-weight:700;padding:.15em .5em;border-radius:4px;margin-left:.4rem">NEW</span>'

    css = """<style>
  :root{--bg:#faf8f3;--ink:#1a1a17;--muted:#6b6862;--accent:#c2410c;--line:#e3ddd0;--code-bg:#f3efe6}
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:var(--bg);color:var(--ink);
    font-family:'Iowan Old Style','Palatino Linotype',Georgia,serif;
    line-height:1.65;-webkit-font-smoothing:antialiased}
  .wrap{max-width:720px;margin:0 auto;padding:5rem 1.5rem 6rem}
  .eyebrow{font-family:'SF Mono','Menlo',monospace;font-size:.72rem;
    letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin-bottom:1.4rem}
  h1{font-size:clamp(2.4rem,6vw,3.6rem);line-height:1.05;
    letter-spacing:-.02em;font-weight:600;margin-bottom:1.5rem}
  .lead{font-size:1.25rem;color:var(--muted);margin-bottom:3.5rem;max-width:32ch}
  h2{font-size:1.05rem;font-family:'SF Mono','Menlo',monospace;
    letter-spacing:.04em;margin:3rem 0 1rem;padding-top:2rem;
    border-top:1px solid var(--line);font-weight:500}
  p{margin-bottom:1.1rem}
  a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:3px}
  .cards{display:grid;gap:.6rem;margin-top:1rem}
  .card{display:block;padding:1.1rem 1.3rem;border:1px solid var(--line);
    border-radius:10px;text-decoration:none;color:var(--ink);
    transition:border-color .2s,transform .2s,background .2s}
  .card:hover{border-color:var(--accent);transform:translateX(4px);background:#fff}
  .card .t{font-weight:600;display:flex;align-items:center;gap:.4rem}
  .card .d{color:var(--muted);font-size:.92rem;margin-top:.2rem;display:block}
  .card .date{font-family:'SF Mono','Menlo',monospace;font-size:.68rem;color:var(--muted);margin-top:.3rem;display:block}
  code{font-family:'SF Mono','Menlo',monospace;font-size:.85em;
    background:var(--code-bg);padding:.15em .45em;border-radius:5px}
  pre{background:var(--code-bg);padding:1.2rem 1.4rem;border-radius:10px;
    overflow-x:auto;font-size:.85rem;line-height:1.55;margin:1rem 0}
  pre code{background:none;padding:0}
  footer{margin-top:4rem;padding-top:2rem;border-top:1px solid var(--line);
    color:var(--muted);font-size:.85rem;font-family:'SF Mono','Menlo',monospace}
</style>"""

    lines = [
        '<!DOCTYPE html>',
        '<html lang="ko">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>한국사 아카이브 — Agent 친화 사이트</title>',
        '<meta name="description" content="한국사를 조사·기록·공유하는 Agent 친화 아카이브. 사람을 위한 HTML과 AI 에이전트를 위한 깨끗한 Markdown을 동시에 제공합니다.">',
        '<link rel="alternate" type="text/markdown" href="/index.md" title="이 페이지의 Markdown 버전">',
        '<link rel="alternate" type="text/plain" href="/llms.txt" title="LLM 인덱스">',
        '<script type="application/ld+json">',
        '{',
        '  "@context": "https://schema.org",',
        '  "@type": "WebSite",',
        '  "name": "한국사 아카이브",',
        '  "url": "https://skandla2002ai-andy.github.io/korean-history",',
        '  "description": "한국사를 조사·기록·공유하는 Agent 친화 아카이브",',
        '  "inLanguage": "ko"',
        '}',
        '</script>',
        css,
        '</head>',
        '<body>',
        '<main class="wrap">',
        '  <div class="eyebrow">Human + Agent Readable</div>',
        '  <h1>한국사 아카이브</h1>',
        '  <p class="lead">한국사를 조사·기록·공유하는 사이트. 사람과 AI 에이전트 모두를 위해 설계했습니다.</p>',
        '',
        '  <h2>// 최근 발행</h2>',
        f'  <p style="font-family:\'SF Mono\',monospace;font-size:.8rem;color:var(--muted);margin-bottom:.8rem">총 {total_p}편 발행 · {total_q}편 발행 예정 · <a href="/korean-history/content.html">전체 목록 →</a></p>',
        '  <div class="cards">',
    ]

    for e in recent:
        art_url   = f'/korean-history/articles/{e["slug"]}.html'
        meta_parts = list(filter(None, e["era"] + e["region"] + e["topics"][:2]))
        meta_str   = " · ".join(meta_parts[:4])
        new_html   = new_badge if e["is_new"] else ""
        date_str   = e["published"] or ""
        lines += [
            f'    <a class="card" href="{art_url}">',
            f'      <span class="t">{e["title"]}{new_html}</span>',
            f'      <span class="d">{meta_str}</span>',
            f'      <span class="date">{date_str}</span>',
            '    </a>',
        ]

    lines += [
        '  </div>',
        '',
        '  <h2>// 사람을 위한 안내</h2>',
        '  <p>Andy PAK이 운영하는 한국사 아카이브입니다. 사실 기반 본문(<code>article</code>)과 편집자의 해석(<code>commentary</code>)을 명확히 구분하여 제공합니다. 시대·지역·연관국·주제별로 글을 탐색할 수 있습니다.</p>',
        '  <div class="cards">',
        '    <a class="card" href="/korean-history/about.html"><span class="t">소개</span><span class="d">이 사이트와 운영자에 대한 핵심 정보</span></a>',
        '    <a class="card" href="/korean-history/content.html"><span class="t">전체 글 목록</span><span class="d">시대별 · 최신순 정렬</span></a>',
        '    <a class="card" href="/korean-history/faq.html"><span class="t">자주 묻는 질문</span><span class="d">사이트 구조와 콘텐츠 방침에 대한 Q&amp;A</span></a>',
        '  </div>',
        '',
        '  <h2>// AI 에이전트를 위한 안내</h2>',
        '  <p>이 사이트는 에이전트가 토큰을 낭비하지 않도록 깨끗한 Markdown을 제공합니다:</p>',
        '  <pre><code># 사이트 전체 인덱스\n'
        f'curl {BASE_URL}/llms.txt\n\n'
        '# 임의 페이지의 Markdown 버전 (.md 추가)\n'
        f'curl {BASE_URL}/about.md\n\n'
        '# 전체 통합본\n'
        f'curl {BASE_URL}/llms-full.txt\n\n'
        '# 구조화 데이터\n'
        f'curl {BASE_URL}/data.json</code></pre>',
        '',
        '  <footer>',
        f'    총 {total_p}편 발행 · 최종 갱신 {TODAY}<br>',
        '    Markdown for agents · HTML for humans<br>',
        '    /llms.txt · /sitemap.xml · /robots.txt',
        '  </footer>',
        '</main>',
        '</body>',
        '</html>',
    ]
    return "\n".join(lines) + "\n"

# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("글 목록 수집 중...")
    entries = collect_articles()
    pub = [e for e in entries if e["source"] == "published"]
    que = [e for e in entries if e["source"] == "queue"]
    new = [e for e in pub if e["is_new"]]
    print(f"  발행: {len(pub)}편  (NEW: {len(new)}편)")
    print(f"  큐:   {len(que)}편")

    print("llms.txt 생성 중...")
    llms = build_llms_txt(entries)
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    print(f"  → {len(llms):,} bytes")

    print("data.json 생성 중...")
    data = build_data_json(entries)
    (ROOT / "data.json").write_text(data, encoding="utf-8")
    print(f"  → {len(data):,} bytes")

    print("content.html 생성 중...")
    ch = build_content_html(entries)
    (ROOT / "content.html").write_text(ch, encoding="utf-8")
    print(f"  → {len(ch):,} bytes")

    print("index.html 생성 중...")
    ih = build_index_html(entries)
    (ROOT / "index.html").write_text(ih, encoding="utf-8")
    print(f"  → {len(ih):,} bytes")

    print("\n✅ 완료")
