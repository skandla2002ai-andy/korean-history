#!/usr/bin/env python3
"""
한국사 아카이브 품질 감사 스크립트
실행: python scripts/audit.py [--fix]

검사 항목:
  1. articles/ 의 모든 글이 해당 태그 인덱스 페이지에 등록되어 있는지
  2. _data/sources.json 의 used_in 목록이 실제 글과 일치하는지
  3. 태그 인덱스 페이지의 글 수(N편)가 실제 카드 수와 맞는지

--fix 옵션: sources.json used_in 자동 업데이트
"""

import re
import sys
import json
import os
from pathlib import Path

# Windows 터미널 UTF-8 출력
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
ARTICLES_DIR  = ROOT / "articles"
QUEUE_DIR     = ROOT / "_queue" / "articles"
TAG_DIRS = {
    "era":     ROOT / "era",
    "topics":  ROOT / "topics",
    "related": ROOT / "related",
    "region":  ROOT / "region",
}
SOURCES_FILE = ROOT / "_data" / "sources.json"

ERRORS = []
WARNINGS = []
FIXES = []


def err(msg):
    ERRORS.append(msg)
    print(f"  ❌ {msg}")


def warn(msg):
    WARNINGS.append(msg)
    print(f"  ⚠️  {msg}")


def ok(msg):
    print(f"  ✅ {msg}")


# ──────────────────────────────────────────────
# 1. 글별 태그 → 인덱스 등록 여부 확인
# ──────────────────────────────────────────────
def check_tag_index():
    print("\n[1] 태그 인덱스 등록 확인")

    articles = sorted(ARTICLES_DIR.glob("*.html"))
    if not articles:
        warn("articles/ 디렉터리가 비어 있습니다.")
        return

    numbered_missing = []
    legacy_missing = []

    for article in articles:
        content = article.read_text(encoding="utf-8")
        is_numbered = bool(re.match(r'^\d{3}-', article.stem))

        tags = re.findall(r'href="/korean-history/(era|topics|related|region)/([^"]+\.html)"', content)

        for category, tag_file in tags:
            index_path = TAG_DIRS[category] / tag_file
            if not index_path.exists():
                err(f"{article.name}: 태그 인덱스 파일 없음 → {category}/{tag_file}")
                continue

            index_content = index_path.read_text(encoding="utf-8")
            article_link = f"/korean-history/articles/{article.name}"
            if article_link not in index_content:
                if is_numbered:
                    numbered_missing.append(f"{article.name} → {category}/{tag_file}")
                else:
                    legacy_missing.append(f"{article.name} → {category}/{tag_file}")

    for m in numbered_missing:
        err(f"인덱스 미등록: {m}")

    for m in legacy_missing:
        warn(f"구형 글(번호 없음) 인덱스 미등록: {m}")

    if not numbered_missing and not legacy_missing:
        ok("모든 글이 태그 인덱스에 등록되어 있습니다.")
    elif not numbered_missing:
        ok(f"번호 있는 글은 모두 등록됨. 구형 글 {len(legacy_missing)}건은 별도 확인 필요.")


# ──────────────────────────────────────────────
# 2. 인덱스 페이지의 글 수(N편) 정확도 확인
# ──────────────────────────────────────────────
def check_index_counts():
    print("\n[2] 인덱스 페이지 글 수(N편) 정확도 확인")

    mismatch = False
    for category, tag_dir in TAG_DIRS.items():
        for index_file in sorted(tag_dir.glob("*.html")):
            content = index_file.read_text(encoding="utf-8")

            # "관련 글 (N편)" 에서 N 추출
            m = re.search(r'관련 글 \((\d+)편\)', content)
            if not m:
                continue
            declared = int(m.group(1))

            # 실제 카드 수
            actual = len(re.findall(r'class="card"', content))

            if declared != actual:
                err(f"{category}/{index_file.name}: 선언({declared}편) ≠ 실제 카드({actual}개)")
                mismatch = True

    if not mismatch:
        ok("모든 인덱스 페이지의 글 수가 정확합니다.")


# ──────────────────────────────────────────────
# 3. sources.json used_in 일치 확인 (+ --fix)
# ──────────────────────────────────────────────
def check_sources(fix=False):
    print("\n[3] sources.json used_in 정확도 확인")

    if not SOURCES_FILE.exists():
        warn("_data/sources.json 없음 — 건너뜁니다.")
        return

    data = json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
    articles = sorted(ARTICLES_DIR.glob("*.html"))

    # 각 글의 번호 추출 (앞 3자리) e.g. "001-jang..." → "001"
    def article_num(path):
        m = re.match(r'^(\d{3})-', path.stem)
        return m.group(1) if m else None

    # published + queued 합쳐서 검사
    all_articles = list(articles) + list(QUEUE_DIR.glob("*.html") if QUEUE_DIR.exists() else [])

    for source in data["sources"]:
        sid = source["id"]
        declared = set(source.get("used_in", []))

        truly_missing = []
        in_queue = []
        for num in declared:
            published = [a for a in articles if article_num(a) == num]
            queued    = [a for a in (QUEUE_DIR.glob("*.html") if QUEUE_DIR.exists() else []) if article_num(a) == num]
            if not published and not queued:
                truly_missing.append(num)
            elif not published and queued:
                in_queue.append(num)

        if truly_missing:
            warn(f"sources[{sid}].used_in: 어디에도 없는 글 번호 {truly_missing}")

        if fix:
            # 완전히 없는 번호만 제거 (큐 포함 존재하면 유지)
            valid = [n for n in declared if n not in truly_missing]
            if sorted(valid) != sorted(list(declared)):
                source["used_in"] = sorted(valid)
                FIXES.append(f"sources[{sid}].used_in 정리: 제거 {truly_missing}")

    if fix and FIXES:
        data["_meta"]["last_updated"] = __import__("datetime").date.today().isoformat()
        SOURCES_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"\n  🔧 자동 수정 완료 ({len(FIXES)}건):")
        for f in FIXES:
            print(f"     {f}")
    else:
        ok("sources.json used_in 검증 완료.")


# ──────────────────────────────────────────────
# 실행
# ──────────────────────────────────────────────
if __name__ == "__main__":
    fix_mode = "--fix" in sys.argv

    print("=" * 55)
    print("  한국사 아카이브 품질 감사")
    if fix_mode:
        print("  모드: 자동 수정 (--fix)")
    print("=" * 55)

    check_tag_index()
    check_index_counts()
    check_sources(fix=fix_mode)

    print("\n" + "=" * 55)
    print(f"  오류: {len(ERRORS)}건  |  경고: {len(WARNINGS)}건")
    print("=" * 55)

    if ERRORS:
        print("\n오류 목록:")
        for e in ERRORS:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("\n✅ 감사 통과")
        sys.exit(0)
