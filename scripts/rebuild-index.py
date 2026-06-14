#!/usr/bin/env python3
"""
llms.txt + data.json 자동 재생성 스크립트
실행: python scripts/rebuild-index.py

대상:
  - articles/          (구형 발행 글, 번호 없음)
  - _queue/articles/   (번호 있는 글, 001~)

출력:
  - llms.txt           (에이전트용 인덱스)
  - data.json          (구조화 데이터)
"""

import re
import json
import sys
from pathlib import Path
from datetime import date

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT       = Path(__file__).parent.parent
BASE_URL   = "https://skandla2002ai-andy.github.io/korean-history"
ARTICLES   = ROOT / "articles"
QUEUE      = ROOT / "_queue" / "articles"
TODAY      = date.today().isoformat()

# ──────────────────────────────────────────────
# HTML 파싱 헬퍼
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

def extract_tags(html):
    """태그 href에서 era/topics/related/region 분류 추출
    패턴: <a href="/korean-history/ERA/joseon.html"><b>시대</b> 조선</a>
    """
    result = {"era": [], "topics": [], "related": [], "region": []}
    # href로 카테고리 파악, <b> 이후 텍스트로 실제 값 추출
    for cat, _file, full_text in re.findall(
        r'href="/korean-history/(era|topics|related|region)/[^"]+\.html"[^>]*>(<b>[^<]+</b>\s*)([^<]+)',
        html
    ):
        value = full_text.strip()
        if value:
            result[cat].append(value)
    return result

def article_num(path):
    m = re.match(r'^(\d{3})-', path.stem)
    return int(m.group(1)) if m else 9999

def build_url(path, base_dir):
    """파일 경로 → 공개 URL"""
    rel = path.relative_to(ROOT).as_posix()
    return f"{BASE_URL}/{rel}"

def build_md_url(html_url):
    return html_url.replace(".html", ".md")

# ──────────────────────────────────────────────
# 글 목록 수집
# ──────────────────────────────────────────────

def collect_articles():
    entries = []

    # 1) 구형 발행 글 (articles/)
    for f in sorted(ARTICLES.glob("*.html")):
        html = read_utf8(f)
        tags = extract_tags(html)
        entries.append({
            "num":      9999,
            "slug":     f.stem,
            "filename": f.name,
            "title":    extract_title(html),
            "description": extract_description(html) or extract_lead(html),
            "era":      tags["era"],
            "topics":   tags["topics"],
            "related":  tags["related"],
            "region":   tags["region"],
            "html_url": build_url(f, ARTICLES),
            "md_url":   build_md_url(build_url(f, ARTICLES)),
            "source":   "published",
        })

    # 2) 번호 있는 큐 글 (_queue/articles/)
    for f in sorted(QUEUE.glob("*.html"), key=article_num):
        html = read_utf8(f)
        tags = extract_tags(html)
        num  = article_num(f)
        slug = re.sub(r'^\d{3}-', '', f.stem)
        entries.append({
            "num":      num,
            "slug":     slug,
            "filename": f.name,
            "title":    extract_title(html),
            "description": extract_description(html) or extract_lead(html),
            "era":      tags["era"],
            "topics":   tags["topics"],
            "related":  tags["related"],
            "region":   tags["region"],
            "html_url": build_url(f, QUEUE),
            "md_url":   build_md_url(build_url(f, QUEUE)),
            "source":   "queue",
        })

    return entries

# ──────────────────────────────────────────────
# 1. llms.txt 생성
# ──────────────────────────────────────────────

def build_llms_txt(entries):
    published = [e for e in entries if e["source"] == "published"]
    queued    = [e for e in entries if e["source"] == "queue"]
    total     = len(entries)

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
        f"- 시대별:   {BASE_URL}/era/",
        f"- 주제별:   {BASE_URL}/topics/",
        f"- 관련국:   {BASE_URL}/related/",
        f"- 지역별:   {BASE_URL}/region/",
        "",
        "## 출처 데이터베이스",
        "",
        f"- [{BASE_URL}/_data/sources.json]({BASE_URL}/_data/sources.json)",
        "  신뢰점수 1~5 포함 23개 공식 기관 URL",
        "",
        f"## 글 목록 (전체 {total}편 · 최종 갱신 {TODAY})",
        "",
    ]

    if published:
        lines.append(f"### 발행 완료 ({len(published)}편)")
        lines.append("")
        for e in published:
            era_str    = " · ".join(e["era"])   if e["era"]    else ""
            region_str = " · ".join(e["region"]) if e["region"] else ""
            meta       = " · ".join(filter(None, [era_str, region_str]))
            desc       = f": {meta}" if meta else ""
            lines.append(f"- [{e['title']}]({e['md_url']}){desc}")
        lines.append("")

    if queued:
        lines.append(f"### 발행 예정 큐 ({len(queued)}편)")
        lines.append("")
        for e in queued:
            era_str    = " · ".join(e["era"])    if e["era"]    else ""
            region_str = " · ".join(e["region"]) if e["region"] else ""
            meta       = " · ".join(filter(None, [era_str, region_str]))
            desc       = f": {meta}" if meta else ""
            lines.append(f"- [{e['num']:03d}. {e['title']}]({e['html_url']}){desc}")
        lines.append("")

    lines += [
        "## 라이선스",
        "",
        "콘텐츠: CC BY 4.0 — 출처(사이트명 + 원문 링크) 표시 후 자유롭게 사용 가능.",
        "코드: MIT License.",
    ]

    return "\n".join(lines) + "\n"

# ──────────────────────────────────────────────
# 2. data.json 생성
# ──────────────────────────────────────────────

def build_data_json(entries):
    published = [e for e in entries if e["source"] == "published"]
    queued    = [e for e in entries if e["source"] == "queue"]

    def entry_to_dict(e):
        return {
            "title":       e["title"],
            "description": e["description"],
            "html_url":    e["html_url"],
            "md_url":      e["md_url"],
            "era":         e["era"],
            "topics":      e["topics"],
            "related":     e["related"],
            "region":      e["region"],
            "num":         e["num"] if e["num"] != 9999 else None,
            "status":      e["source"],
        }

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
        },
        "endpoints": {
            "llms_txt":    f"{BASE_URL}/llms.txt",
            "llms_full":   f"{BASE_URL}/llms-full.txt",
            "data_json":   f"{BASE_URL}/data.json",
            "sources":     f"{BASE_URL}/_data/sources.json",
            "agents_md":   f"{BASE_URL}/AGENTS.md",
            "sitemap":     f"{BASE_URL}/sitemap.xml",
        },
        "tag_indexes": {
            "era":     f"{BASE_URL}/era/",
            "topics":  f"{BASE_URL}/topics/",
            "related": f"{BASE_URL}/related/",
            "region":  f"{BASE_URL}/region/",
        },
        "pages": [
            {"title": "소개",          "url": f"{BASE_URL}/about.md"},
            {"title": "주요 콘텐츠",  "url": f"{BASE_URL}/content.md"},
            {"title": "자주 묻는 질문","url": f"{BASE_URL}/faq.md"},
        ],
        "articles":   [entry_to_dict(e) for e in published],
        "queue":      [entry_to_dict(e) for e in queued],
    }

    return json.dumps(data, ensure_ascii=False, indent=2)

# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────

if __name__ == "__main__":
    print("글 목록 수집 중...")
    entries = collect_articles()
    print(f"  발행: {sum(1 for e in entries if e['source']=='published')}편")
    print(f"  큐:   {sum(1 for e in entries if e['source']=='queue')}편")

    print("llms.txt 생성 중...")
    llms = build_llms_txt(entries)
    (ROOT / "llms.txt").write_text(llms, encoding="utf-8")
    print(f"  → llms.txt ({len(llms)} bytes)")

    print("data.json 생성 중...")
    data = build_data_json(entries)
    (ROOT / "data.json").write_text(data, encoding="utf-8")
    print(f"  → data.json ({len(data)} bytes)")

    print("\n✅ 완료")
