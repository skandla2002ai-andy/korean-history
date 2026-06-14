#!/usr/bin/env python3
"""
GoatCounter API에서 페이지별 조회수를 가져와 data.json에 반영
실행: python scripts/fetch-stats.py

필요 환경변수:
  GOATCOUNTER_CODE   : 계정 코드 (예: korean-history-andy)
  GOATCOUNTER_TOKEN  : API 토큰 (GoatCounter 설정 > API tokens)
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path
from datetime import date

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT       = Path(__file__).parent.parent
DATA_FILE  = ROOT / "data.json"

GC_CODE  = os.environ.get("GOATCOUNTER_CODE", "")
GC_TOKEN = os.environ.get("GOATCOUNTER_TOKEN", "")

if not GC_CODE or not GC_TOKEN:
    print("❌ GOATCOUNTER_CODE 또는 GOATCOUNTER_TOKEN 미설정")
    sys.exit(1)

BASE_API = f"https://{GC_CODE}.goatcounter.com/api/v0"


def gc_get(endpoint: str) -> dict:
    url = f"{BASE_API}{endpoint}"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {GC_TOKEN}",
            "Content-Type": "application/json",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()}")
        raise


def fetch_all_hits() -> dict[str, int]:
    """전체 기간 페이지별 조회수 반환 {path: count}"""
    hits = {}
    page = 1
    print("  GoatCounter API 호출 중...")
    while True:
        data = gc_get(f"/stats/hits?limit=200&page={page}")
        items = data.get("hits", [])
        if not items:
            break
        for item in items:
            path  = item.get("path", "")
            count = item.get("count", 0)
            if path:
                hits[path] = hits.get(path, 0) + count
        # 다음 페이지 여부
        if not data.get("more", False):
            break
        page += 1
    print(f"  {len(hits)}개 경로 수집 완료")
    return hits


def path_to_slug(path: str) -> str:
    """URL 경로 → 슬러그 추출
    /korean-history/articles/admiral-yi.html → admiral-yi
    /korean-history/_queue/articles/001-sejong-hangul.html → 001-sejong-hangul
    """
    p = path.rstrip("/")
    name = p.split("/")[-1]
    return name.replace(".html", "").replace(".md", "")


def update_data_json(hits: dict[str, int]):
    if not DATA_FILE.exists():
        print("❌ data.json 없음")
        return

    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    # slug → 총 조회수 매핑
    slug_hits: dict[str, int] = {}
    for path, count in hits.items():
        slug = path_to_slug(path)
        slug_hits[slug] = slug_hits.get(slug, 0) + count  # html + md 합산

    updated = 0
    total_views = 0

    for section in ("articles", "queue"):
        for entry in data.get(section, []):
            # html_url에서 slug 추출
            url   = entry.get("html_url", "")
            slug  = path_to_slug(url)
            views = slug_hits.get(slug, 0)
            entry["view_count"] = views
            total_views += views
            if views > 0:
                updated += 1

    data["stats"]["total_views"] = total_views
    data["stats"]["stats_updated"] = date.today().isoformat()

    # 인기 글 TOP 10 (발행 완료 글만)
    published = [e for e in data.get("articles", []) if e.get("view_count", 0) > 0]
    top10 = sorted(published, key=lambda x: x["view_count"], reverse=True)[:10]
    data["top_articles"] = [
        {
            "title":      e["title"],
            "html_url":   e["html_url"],
            "view_count": e["view_count"],
            "era":        e.get("era", []),
        }
        for e in top10
    ]

    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  data.json 업데이트: {updated}개 글 조회수 반영")
    print(f"  총 조회수: {total_views:,}")
    if top10:
        print("  TOP 3:")
        for e in top10[:3]:
            print(f"    {e['view_count']:>6,}회  {e['title']}")


if __name__ == "__main__":
    print("GoatCounter 통계 수집 중...")
    hits = fetch_all_hits()
    update_data_json(hits)
    print("✅ 완료")
