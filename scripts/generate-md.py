#!/usr/bin/env python3
"""
HTML 글 → Markdown 변환 스크립트
실행: python scripts/generate-md.py [--all | --queue | --published]

대상:
  --queue     : _queue/articles/*.html → _queue/articles/*.md  (기본)
  --published : articles/*.html → articles/*.md
  --all       : 두 디렉터리 모두
"""

import re
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent

# ──────────────────────────────────────────────
# HTML → 텍스트 변환 헬퍼
# ──────────────────────────────────────────────

def unescape(text):
    return (text
        .replace("&amp;", "&")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("&nbsp;", " ")
        .replace("&#39;", "'")
        .replace("&quot;", '"'))

def strip_tags(html):
    """HTML 태그 제거 후 텍스트만 반환"""
    text = re.sub(r'<br\s*/?>', '\n', html)
    text = re.sub(r'<[^>]+>', '', text)
    return unescape(text).strip()

def html_to_md_inline(html):
    """인라인 서식 변환: <b> → **, <i> → *, <em> → *, 링크 제거"""
    html = re.sub(r'<b>([^<]+)</b>', r'**\1**', html)
    html = re.sub(r'<strong>([^<]+)</strong>', r'**\1**', html)
    html = re.sub(r'<i>([^<]+)</i>', r'*\1*', html)
    html = re.sub(r'<em>([^<]+)</em>', r'*\1*', html)
    html = re.sub(r'<a[^>]*>([^<]+)</a>', r'\1', html)
    html = re.sub(r'<br\s*/?>', '\n', html)
    html = re.sub(r'<[^>]+>', '', html)
    return unescape(html).strip()

def section_to_md(html_section):
    """<section> 또는 본문 블록 → Markdown 문단"""
    lines = []

    # <p> 태그
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', html_section, re.DOTALL):
        text = html_to_md_inline(m.group(1)).strip()
        if text:
            lines.append(text)
            lines.append("")

    # <ul><li> 목록
    for m in re.finditer(r'<ul[^>]*>(.*?)</ul>', html_section, re.DOTALL):
        for li in re.finditer(r'<li[^>]*>(.*?)</li>', m.group(1), re.DOTALL):
            text = html_to_md_inline(li.group(1)).strip()
            if text:
                lines.append(f"- {text}")
        lines.append("")

    # <ol><li> 목록
    for m in re.finditer(r'<ol[^>]*>(.*?)</ol>', html_section, re.DOTALL):
        for i, li in enumerate(re.finditer(r'<li[^>]*>(.*?)</li>', m.group(1), re.DOTALL), 1):
            text = html_to_md_inline(li.group(1)).strip()
            if text:
                lines.append(f"{i}. {text}")
        lines.append("")

    # <blockquote>
    for m in re.finditer(r'<blockquote[^>]*>(.*?)</blockquote>', html_section, re.DOTALL):
        text = strip_tags(m.group(1)).strip()
        if text:
            for l in text.split('\n'):
                lines.append(f"> {l.strip()}")
            lines.append("")

    # <dl><dt><dd> (사실 표 등)
    for m in re.finditer(r'<dl[^>]*>(.*?)</dl>', html_section, re.DOTALL):
        for dt, dd in zip(
            re.findall(r'<dt[^>]*>(.*?)</dt>', m.group(1), re.DOTALL),
            re.findall(r'<dd[^>]*>(.*?)</dd>', m.group(1), re.DOTALL)
        ):
            lines.append(f"**{strip_tags(dt)}**: {strip_tags(dd)}")
        lines.append("")

    # <table>
    for tbl in re.finditer(r'<table[^>]*>(.*?)</table>', html_section, re.DOTALL):
        rows = re.findall(r'<tr[^>]*>(.*?)</tr>', tbl.group(1), re.DOTALL)
        for ri, row in enumerate(rows):
            cells = [strip_tags(c) for c in re.findall(r'<t[hd][^>]*>(.*?)</t[hd]>', row, re.DOTALL)]
            if cells:
                lines.append("| " + " | ".join(cells) + " |")
                if ri == 0:
                    lines.append("| " + " | ".join(["---"] * len(cells)) + " |")
        lines.append("")

    return "\n".join(lines)

# ──────────────────────────────────────────────
# 메인 변환 함수
# ──────────────────────────────────────────────

def html_to_md(html_path: Path) -> str:
    html = html_path.read_text(encoding="utf-8")

    # 메타데이터 추출
    title_m = re.search(r'<title>(.+?) — 한국사 아카이브</title>', html)
    title = title_m.group(1).strip() if title_m else html_path.stem

    desc_m = re.search(r'<meta name="description" content="([^"]+)"', html)
    description = desc_m.group(1).strip() if desc_m else ""

    lead_m = re.search(r'<p class="lead">([^<]+)</p>', html)
    lead = lead_m.group(1).strip() if lead_m else ""

    # 태그 추출
    tags_raw = re.findall(
        r'href="/korean-history/(era|topics|related|region)/[^"]+\.html"[^>]*><b>[^<]+</b>\s*([^<]+)',
        html
    )
    tags_by_cat = {"era": [], "topics": [], "related": [], "region": []}
    for cat, val in tags_raw:
        v = val.strip()
        if v:
            tags_by_cat[cat].append(v)

    # 날짜 (있으면)
    date_m = re.search(r'<time[^>]*datetime="([^"]+)"', html)
    date_str = date_m.group(1) if date_m else ""

    # 글 번호
    num_m = re.match(r'^(\d{3})-', html_path.stem)
    num = num_m.group(1) if num_m else ""

    # ── 프론트매터
    lines = ["---"]
    lines.append(f'title: "{title}"')
    lines.append(f'type: article')
    if tags_by_cat["era"]:
        lines.append(f'era: "{tags_by_cat["era"][0]}"')
    if tags_by_cat["region"]:
        lines.append(f'region: "{tags_by_cat["region"][0]}"')
    if tags_by_cat["topics"]:
        topics_list = ", ".join(f'"{t}"' for t in tags_by_cat["topics"])
        lines.append(f'topics: [{topics_list}]')
    if tags_by_cat["related"]:
        related_list = ", ".join(f'"{r}"' for r in tags_by_cat["related"])
        lines.append(f'related_countries: [{related_list}]')
    if description:
        lines.append(f'description: "{description}"')
    if date_str:
        lines.append(f'date: "{date_str}"')
    if num:
        lines.append(f'num: {int(num)}')
    lines.append(f'source: "https://skandla2002ai-andy.github.io/korean-history"')
    lines.append(f'license: "CC BY 4.0"')
    lines.append("---")
    lines.append("")

    # ── 제목 + 리드
    lines.append(f"# {title}")
    lines.append("")
    if lead:
        lines.append(f"> {lead}")
        lines.append("")

    # ── 태그 줄
    tag_parts = []
    if tags_by_cat["era"]:
        tag_parts.append("시대: " + " · ".join(tags_by_cat["era"]))
    if tags_by_cat["topics"]:
        tag_parts.append("주제: " + " · ".join(tags_by_cat["topics"]))
    if tags_by_cat["related"]:
        tag_parts.append("관련국: " + " · ".join(tags_by_cat["related"]))
    if tags_by_cat["region"]:
        tag_parts.append("지역: " + " · ".join(tags_by_cat["region"]))
    if tag_parts:
        lines.append("**" + "  |  ".join(tag_parts) + "**")
        lines.append("")

    # ── 본문 섹션
    # <h2> 단위로 분할
    body_start = html.find('<div class="tags">')
    if body_start == -1:
        body_start = html.find('<h1>')
    body_end = html.find('<div class="references">')
    if body_end == -1:
        body_end = html.find('<footer')
    body_html = html[body_start:body_end] if body_end > body_start else html[body_start:]

    # h2 섹션들
    parts = re.split(r'(<h2>[^<]+</h2>)', body_html)
    for part in parts:
        h2 = re.match(r'<h2>([^<]+)</h2>', part)
        if h2:
            title_h2 = h2.group(1).strip()
            if title_h2 not in ("출처 및 참고 자료",):
                lines.append(f"## {title_h2}")
                lines.append("")
        else:
            md = section_to_md(part)
            if md.strip():
                lines.append(md)

    # ── 출처
    ref_m = re.search(r'<div class="references">(.*?)</(?:div|section|main)', html, re.DOTALL)
    if ref_m:
        ref_html = ref_m.group(1)
        lines.append("## 출처 및 참고 자료")
        lines.append("")
        for i, li in enumerate(re.finditer(r'<li[^>]*>(.*?)</li>', ref_html, re.DOTALL), 1):
            text = html_to_md_inline(li.group(1)).strip()
            if text:
                lines.append(f"{i}. {text}")
        lines.append("")

    return "\n".join(lines)

# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────

def process_dir(html_dir: Path):
    files = sorted(html_dir.glob("*.html"))
    ok = 0
    fail = 0
    for f in files:
        md_path = f.with_suffix(".md")
        try:
            md = html_to_md(f)
            md_path.write_text(md, encoding="utf-8")
            ok += 1
        except Exception as e:
            print(f"  ⚠️  {f.name}: {e}")
            fail += 1
    print(f"  {html_dir.name}/: {ok}개 생성, {fail}개 실패")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--queue"

    if mode in ("--queue", "--all"):
        print("_queue/articles/ .md 생성 중...")
        process_dir(ROOT / "_queue" / "articles")

    if mode in ("--published", "--all"):
        print("articles/ .md 생성 중...")
        process_dir(ROOT / "articles")

    print("\n✅ 완료")
