#!/usr/bin/env python3
"""
GoatCounter 스크립트를 모든 HTML 파일에 삽입
실행: python scripts/inject-analytics.py [GOATCOUNTER_CODE]

GOATCOUNTER_CODE: goatcounter.com 계정 코드 (예: korean-history-andy)
미입력 시 환경변수 GOATCOUNTER_CODE 사용
"""

import re
import sys
import os
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent

GC_CODE = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("GOATCOUNTER_CODE", "")

if not GC_CODE:
    print("❌ GOATCOUNTER_CODE 미설정. 인수로 전달하거나 환경변수에 설정하세요.")
    sys.exit(1)

SNIPPET = f'''<script data-goatcounter="https://{GC_CODE}.goatcounter.com/count"
        async src="//gc.zgo.at/count.js"></script>'''

TARGET_DIRS = [
    ROOT / "articles",
    ROOT / "thoughts",
    ROOT / "era",
    ROOT / "topics",
    ROOT / "related",
    ROOT / "region",
]
ROOT_FILES = ["index.html", "content.html", "about.html", "faq.html"]

def inject(path: Path) -> bool:
    html = path.read_text(encoding="utf-8")
    # 이미 삽입되어 있으면 코드만 업데이트
    if "goatcounter.com/count" in html:
        # 기존 코드 업데이트 (다른 계정 코드로 변경된 경우 대비)
        new_html = re.sub(
            r'<script data-goatcounter="https://[^"]+\.goatcounter\.com/count"[^>]*>\s*</script>',
            SNIPPET,
            html
        )
        if new_html == html:
            return False  # 변경 없음
        path.write_text(new_html, encoding="utf-8")
        return True
    # </body> 바로 앞에 삽입
    if "</body>" not in html:
        return False
    new_html = html.replace("</body>", f"{SNIPPET}\n</body>")
    path.write_text(new_html, encoding="utf-8")
    return True

ok = 0
skip = 0

for d in TARGET_DIRS:
    if not d.exists():
        continue
    for f in sorted(d.glob("*.html")):
        if inject(f):
            ok += 1
        else:
            skip += 1

for name in ROOT_FILES:
    f = ROOT / name
    if f.exists():
        if inject(f):
            ok += 1
        else:
            skip += 1

print(f"✅ 삽입 완료: {ok}개  |  변경 없음: {skip}개")
print(f"   추적 URL: https://{GC_CODE}.goatcounter.com")
