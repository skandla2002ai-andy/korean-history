# 한국사 아카이브

> 한국사를 조사·기록·공유하는 Agent 친화 웹사이트.  
> 사람을 위한 HTML과 AI 에이전트를 위한 깨끗한 Markdown을 동시에 제공합니다.

---

## 🌐 홈페이지

**https://skandla2002ai-andy.github.io/korean-history/**

| 경로 | 설명 |
|------|------|
| `/` | 메인 페이지 |
| `/about.html` | 사이트 소개 |
| `/content.html` | 글 목록 |
| `/faq.html` | 자주 묻는 질문 |
| `/articles/` | 사실 기반 본문 글 |
| `/thoughts/` | 편집자 해석·의견 글 |

---

## 🎯 사이트 목표

1. **한국사를 정확하게 기록한다**  
   검증된 사료와 출처를 바탕으로 한 사실 본문(`article`)을 축적하여, 신뢰할 수 있는 한국사 1차 참조점을 만든다.

2. **사실과 의견을 명확히 구분한다**  
   사실 본문(`article`)과 편집자 해석(`commentary`)을 항상 분리하여, 독자와 AI 에이전트가 혼동 없이 정보를 활용할 수 있도록 한다.

3. **시대·지역·주제를 교차하여 연결한다**  
   하나의 글이 시대(era), 지역(region), 연관국(related_countries), 주제(topics) 등 여러 카테고리로 동시에 탐색될 수 있게 설계한다. 이후 세계사와의 연결로 확장한다.

4. **사람과 AI 에이전트 모두를 독자로 삼는다**  
   모든 페이지는 `.html`(사람용)과 `.md`(에이전트용) 두 버전을 쌍으로 제공한다. `/llms.txt`와 `/data.json`으로 에이전트가 전체 구조를 한눈에 파악할 수 있도록 한다.

5. **한국사를 넓게 공유한다**  
   콘텐츠는 CC BY 4.0으로 제공한다. 출처만 밝히면 누구나, 상업적 목적을 포함해 자유롭게 사용할 수 있다.

---

## 🤖 AI 에이전트를 위한 가이드

이 사이트는 에이전트 친화적으로 설계되었습니다. 아래 엔드포인트를 활용하세요.

```bash
# 사이트 전체 인덱스 (가장 먼저 읽을 것)
curl https://skandla2002ai-andy.github.io/korean-history/llms.txt

# 외부 fetch 없이 전체 콘텐츠를 한 파일로
curl https://skandla2002ai-andy.github.io/korean-history/llms-full.txt

# 기계 판독용 구조화 데이터 (JSON)
curl https://skandla2002ai-andy.github.io/korean-history/data.json

# 임의 페이지의 Markdown 버전: URL 끝에 .md 추가
curl https://skandla2002ai-andy.github.io/korean-history/about.md
curl https://skandla2002ai-andy.github.io/korean-history/articles/silla-tang.md
```

---

## 📁 저장소 구조

```
korean-history/
├── index.html / index.md       # 메인 페이지
├── about.md                    # 사이트 소개
├── content.md                  # 글 목록
├── faq.md                      # 자주 묻는 질문
├── changelog.md                # 변경 이력
├── llms.txt                    # AI 에이전트용 인덱스
├── llms-full.txt               # 전체 콘텐츠 통합본
├── data.json                   # 구조화 데이터
├── robots.txt                  # 크롤러 정책 (AI 봇 명시적 허용)
├── sitemap.xml                 # 사이트맵
├── articles/                   # 사실 기반 본문 (article)
│   └── silla-tang.html/.md    # 신라-당 외교 관계
└── thoughts/                   # 편집자 해석·의견 (commentary)
    └── silla-tang-editor.html/.md
```

---

## ✍️ 글 작성 규칙

모든 글은 frontmatter로 메타데이터를 관리합니다.

```yaml
---
title: 글 제목
type: article            # article / commentary
region: 경주
era: 통일신라
related_countries: [당나라]
topics: [외교, 정치]
comments: false
related_commentary: /thoughts/xxx.md   # 연결된 해석 글 (article일 때)
based_on: /articles/xxx.md             # 근거 본문 (commentary일 때)
lastUpdated: YYYY-MM-DD
---
```

- 원문 글은 `/articles/`에 단 하나만 둡니다. 복사본 금지.
- 모든 글은 `.html`과 `.md` 두 버전을 함께 작성합니다.

---

## 📄 라이선스

- **코드**: [MIT License](LICENSE)
- **콘텐츠**: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — 출처(사이트명 + 원문 링크) 표시 후 자유롭게 사용 가능

---

*운영: Andy PAK · 문의: [GitHub Issues](https://github.com/skandla2002ai-andy/korean-history/issues)*
