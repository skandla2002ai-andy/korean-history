"""
매일 실행되는 한국사 아티클 자동 생성 스크립트.
5개 주제(조선왕조실록·고려사·발해·삼국시대·고조선)별로 1편씩 생성,
articles/<DATE>-<slug>.html/.md 로 저장한다.
"""

import anthropic
import datetime
import json
import os
import re
import sys

client = anthropic.Anthropic()

TODAY = datetime.date.today().strftime("%Y-%m-%d")
BASE_URL = "https://skandla2002ai-andy.github.io/korean-history"

TOPICS = [
    {"name": "조선왕조실록", "era": "조선"},
    {"name": "고려사",       "era": "고려"},
    {"name": "발해",         "era": "발해"},
    {"name": "삼국시대",     "era": "삼국시대"},
    {"name": "고조선",       "era": "고조선"},
]


def generate(topic: dict) -> dict:
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=2048,
        messages=[{
            "role": "user",
            "content": f"""당신은 한국사 전문 작가입니다. {topic['name']}에서 잘 알려지지 않은 흥미로운 역사적 주제를 하나 선택하여 사실 기반 글을 작성하세요.

반드시 아래 JSON 형식만 출력하세요 (다른 텍스트 없음):
{{
  "title": "글 제목 (한국어, 구체적이고 흥미롭게)",
  "slug": "english-slug-with-hyphens",
  "region": "주요 지역 (한국어)",
  "era": "{topic['era']}",
  "related_countries": ["연관 국가"],
  "topics": ["주제1", "주제2"],
  "summary": "한 줄 요약 (메타 description용, 50자 내외)",
  "sections": [
    {{"heading": "개요", "body": "200자 이상. 주제의 배경과 핵심을 소개."}},
    {{"heading": "핵심 사실", "body": "구체적인 연도·인물·사건을 포함. 목록(- ) 형태 가능."}},
    {{"heading": "역사적 의의", "body": "이 사건·주제가 한국사에 미친 영향과 현재적 의미."}}
  ]
}}"""
        }]
    )
    text = message.content[0].text.strip()
    m = re.search(r'\{[\s\S]*\}', text)
    if not m:
        raise ValueError(f"JSON 파싱 실패 ({topic['name']}): {text[:200]}")
    return json.loads(m.group())


def md_body(text: str) -> str:
    """목록 항목이 있으면 그대로, 없으면 단락으로 반환."""
    return text


def html_body(text: str) -> str:
    """간단한 마크다운 → HTML 변환 (p, ul/li)."""
    lines = text.split('\n')
    out = []
    in_ul = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('- '):
            if not in_ul:
                out.append('<ul>')
                in_ul = True
            out.append(f'  <li>{stripped[2:]}</li>')
        else:
            if in_ul:
                out.append('</ul>')
                in_ul = False
            if stripped:
                out.append(f'<p>{stripped}</p>')
    if in_ul:
        out.append('</ul>')
    return '\n'.join(out)


def build_md(data: dict, slug: str) -> str:
    related = json.dumps(data['related_countries'], ensure_ascii=False)
    topics  = json.dumps(data['topics'], ensure_ascii=False)
    sections = '\n\n'.join(
        f"## {s['heading']}\n\n{md_body(s['body'])}"
        for s in data['sections']
    )
    return f"""---
title: {data['title']}
type: article
region: {data['region']}
era: {data['era']}
related_countries: {related}
topics: {topics}
comments: false
lastUpdated: {TODAY}
---

# {data['title']}

> {data['summary']}

{sections}
"""


def build_html(data: dict, slug: str) -> str:
    tags_html = ''.join(
        f'    <a class="tag" href="/korean-history/topics/{t}.html"><b>주제</b> {t}</a>\n'
        for t in data['topics']
    )
    sections_html = '\n'.join(
        f'  <h2>{s["heading"]}</h2>\n  {html_body(s["body"])}'
        for s in data['sections']
    )
    title_esc   = data['title'].replace('"', '&quot;')
    summary_esc = data['summary'].replace('"', '&quot;')

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{data['title']} — 한국사 아카이브</title>
<meta name="description" content="{summary_esc}">
<link rel="alternate" type="text/markdown" href="/korean-history/articles/{slug}.md">
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_esc}",
  "about": {json.dumps(data['topics'], ensure_ascii=False)},
  "inLanguage": "ko",
  "dateModified": "{TODAY}",
  "author": {{"@type": "Person", "name": "Andy PAK"}}
}}
</script>
<style>
  :root{{--bg:#f7f4ed;--ink:#211f1a;--muted:#6f6a60;--accent:#8a1c1c;--line:#e0d9c9;--tag-bg:#ece5d6;--fact:#1f5c3d}}
  *{{margin:0;padding:0;box-sizing:border-box}}
  body{{background:var(--bg);color:var(--ink);font-family:'Iowan Old Style','Palatino Linotype',Georgia,serif;line-height:1.7;-webkit-font-smoothing:antialiased}}
  .wrap{{max-width:680px;margin:0 auto;padding:4rem 1.5rem 6rem}}
  .kind{{display:inline-block;font-family:'SF Mono',Menlo,monospace;font-size:.68rem;letter-spacing:.12em;text-transform:uppercase;padding:.3em .7em;border-radius:999px;margin-bottom:1.5rem;background:rgba(31,92,61,.12);color:var(--fact)}}
  h1{{font-size:clamp(2rem,5vw,2.9rem);line-height:1.1;letter-spacing:-.02em;margin-bottom:1rem;font-weight:600}}
  .lead{{font-size:1.2rem;color:var(--muted);margin-bottom:1.8rem}}
  .tags{{display:flex;flex-wrap:wrap;gap:.5rem;margin-bottom:2.5rem;padding-bottom:2rem;border-bottom:1px solid var(--line)}}
  .tag{{font-family:'SF Mono',Menlo,monospace;font-size:.78rem;background:var(--tag-bg);padding:.35em .8em;border-radius:7px;color:var(--ink);text-decoration:none;transition:background .2s}}
  .tag:hover{{background:#ddd3bd}}
  .tag b{{color:var(--accent);font-weight:600}}
  h2{{font-size:1.4rem;margin:2.5rem 0 1rem;font-weight:600}}
  p{{margin-bottom:1.1rem}}
  ul{{margin:.5rem 0 1rem 1.5rem}}
  li{{margin-bottom:.4rem}}
  .nav{{margin-bottom:2rem;font-family:'SF Mono',Menlo,monospace;font-size:.8rem}}
  .nav a{{color:var(--accent);text-decoration:none}}
  .nav a:hover{{text-decoration:underline}}
  footer{{margin-top:4rem;padding-top:1.5rem;border-top:1px solid var(--line);font-family:'SF Mono',Menlo,monospace;font-size:.8rem;color:var(--muted)}}
  footer a{{color:var(--accent)}}
</style>
</head>
<body>
<main class="wrap">
  <div class="nav"><a href="/korean-history/">← 한국사 아카이브</a></div>
  <span class="kind">● 사실 기반 본문 / Article</span>
  <h1>{data['title']}</h1>
  <p class="lead">{data['summary']}</p>
  <div class="tags">
    <a class="tag" href="/korean-history/era/{data['era']}.html"><b>시대</b> {data['era']}</a>
    <a class="tag" href="/korean-history/region/{data['region']}.html"><b>지역</b> {data['region']}</a>
{tags_html}  </div>

{sections_html}

  <footer>
    Markdown 버전: <a href="/korean-history/articles/{slug}.md">/articles/{slug}.md</a><br>
    사실 기반 본문 · 댓글 없음 · CC BY 4.0 Andy PAK
  </footer>
</main>
</body>
</html>
"""


def main():
    os.makedirs('articles', exist_ok=True)
    created = []

    for topic in TOPICS:
        print(f"생성 중: {topic['name']} ...", flush=True)
        try:
            data  = generate(topic)
            slug  = f"{TODAY}-{data['slug']}"

            with open(f"articles/{slug}.md", 'w', encoding='utf-8') as f:
                f.write(build_md(data, slug))
            with open(f"articles/{slug}.html", 'w', encoding='utf-8') as f:
                f.write(build_html(data, slug))

            created.append({'slug': slug, 'title': data['title'], 'era': topic['era']})
            print(f"  ✓ {slug}", flush=True)
        except Exception as e:
            print(f"  ✗ {topic['name']}: {e}", file=sys.stderr)

    # GitHub Actions output
    gha_output = os.environ.get('GITHUB_OUTPUT', '')
    if gha_output:
        with open(gha_output, 'a', encoding='utf-8') as f:
            f.write(f"created_count={len(created)}\n")
            f.write(f"article_titles={', '.join(a['title'] for a in created)}\n")

    print(f"\n완료: {len(created)}/5 글 생성됨")
    if len(created) == 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
