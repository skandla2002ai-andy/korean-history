#!/usr/bin/env python3
"""
한국사 아카이브 자동 글 생성 스크립트
_data/story-candidates.json에서 다음 미작성 이야기를 찾아
articles/{slug}.html 과 thoughts/{slug}-editor.html 을 생성한다.
"""

import json
import os
import re
import sys
from pathlib import Path

import anthropic


def get_existing_slugs() -> set[str]:
    return {f.stem for f in Path("articles").glob("*.html")}


def get_next_candidate() -> dict | None:
    with open("_data/story-candidates.json", encoding="utf-8") as f:
        data = json.load(f)
    existing = get_existing_slugs()
    for c in data["candidates"]:
        if c["slug"] not in existing:
            return c
    return None


def extract_html(text: str) -> str:
    """모델 응답에서 순수 HTML만 추출한다."""
    # 코드 블록 안에 감싸진 경우 처리
    m = re.search(r"```html\s*([\s\S]*?)```", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # DOCTYPE으로 시작하는 부분 추출
    m = re.search(r"(<!DOCTYPE[\s\S]*</html>)", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    return text.strip()


def read_reference(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def generate_article(client: anthropic.Anthropic, candidate: dict) -> str:
    ref = read_reference("articles/jangbogo.html")
    topics_str = ", ".join(candidate["topics"])

    prompt = f"""당신은 한국사 아카이브(https://skandla2002ai-andy.github.io/korean-history/) 편집자입니다.
아래 이야기에 대해 **사실 기반 본문** HTML 파일을 작성하세요.

### 이야기 정보
- slug: {candidate['slug']}
- 제목: {candidate['title']}
- 시대: {candidate['era']}
- 주제: {topics_str}
- 지역: {candidate.get('region', '전국')}
- 요약: {candidate['summary']}
- 핵심 관점: {candidate['angle']}

### 기존 글 참고 (HTML 구조를 그대로 따를 것)
{ref}

### 작성 규칙
1. <!DOCTYPE html> 부터 </html> 까지 완전한 HTML만 출력 (다른 설명 없이)
2. CSS 디자인 시스템 유지 (--bg:#f7f4ed, --ink:#211f1a, --accent:#8a1c1c, --fact:#1f5c3d, --opinion:#9a6b1c)
3. <span class="kind">● 사실 기반 본문 / Article</span>
4. .tag 링크는 era/, topics/, region/, related/ 디렉토리의 기존 파일로 연결
5. h2 섹션 3~5개 (개요 포함)
6. 검증된 역사적 사실만 서술, 출처 섹션(<div class="references">) 포함
7. 편집자 의견 카드: /korean-history/thoughts/{candidate['slug']}-editor.html
8. 본문 600~1000자
9. 한국어 작성
10. <title> 태그: "{candidate['title']} — 한국사 아카이브"
"""

    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return extract_html(msg.content[0].text)


def generate_commentary(client: anthropic.Anthropic, candidate: dict) -> str:
    ref = read_reference("thoughts/jang-yeongshil-editor.html")

    prompt = f"""당신은 한국사 아카이브 편집자입니다.
아래 이야기에 대해 **편집자 의견(commentary)** HTML 파일을 작성하세요.

### 이야기 정보
- slug: {candidate['slug']}
- 제목: {candidate['title']}
- 시대: {candidate['era']}
- 핵심 관점: {candidate['angle']}
- 요약: {candidate['summary']}

### 기존 편집자 의견 참고 (HTML 구조를 그대로 따를 것)
{ref}

### 작성 규칙
1. <!DOCTYPE html> 부터 </html> 까지 완전한 HTML만 출력
2. <span class="kind">● 편집자 의견 / Commentary</span>
3. badge: <span class="badge bc">commentary</span>
4. 편집자의 주관적 시각으로 역사적 의미 해석
5. 독자가 다시 생각해볼 만한 질문을 던지는 방식
6. 분량: 400~700자
7. 사실 기반 본문 링크: /korean-history/articles/{candidate['slug']}.html
8. 한국어 작성
9. <title> 태그: "[편집자 의견] {candidate['title']} — 한국사 아카이브"
"""

    msg = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return extract_html(msg.content[0].text)


def set_gha_output(key: str, value: str) -> None:
    """GitHub Actions output 변수 설정."""
    gha_output = os.environ.get("GITHUB_OUTPUT")
    if gha_output:
        with open(gha_output, "a", encoding="utf-8") as f:
            f.write(f"{key}={value}\n")
    else:
        print(f"OUTPUT {key}={value}")


def main() -> None:
    candidate = get_next_candidate()

    if not candidate:
        print("✅ 모든 이야기가 완성되었습니다!")
        set_gha_output("skipped", "true")
        sys.exit(0)

    print(f"📝 생성 중: [{candidate['id']}] {candidate['title']}")

    client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경변수 자동 사용

    # 사실 기반 본문
    article_html = generate_article(client, candidate)
    article_path = Path(f"articles/{candidate['slug']}.html")
    article_path.write_text(article_html, encoding="utf-8")
    print(f"✓ 사실 기반 본문: {article_path}")

    # 편집자 의견
    commentary_html = generate_commentary(client, candidate)
    commentary_path = Path(f"thoughts/{candidate['slug']}-editor.html")
    commentary_path.write_text(commentary_html, encoding="utf-8")
    print(f"✓ 편집자 의견: {commentary_path}")

    set_gha_output("title", candidate["title"])
    set_gha_output("slug", candidate["slug"])
    set_gha_output("skipped", "false")


if __name__ == "__main__":
    main()
