# Claude Code 작업 브리프 — korean-history 사이트

이 문서는 Claude Code에게 작업을 요청할 때 그대로 붙여넣을 수 있는 요약입니다.
이 폴더의 다른 파일들은 이미 만들어진 시작점입니다.

---

## 프로젝트 개요

한국사를 조사·기록·공유하는 **Agent 친화 웹사이트**.
사람을 위한 HTML과, AI 에이전트를 위한 깨끗한 Markdown을 동시에 제공한다.
GitHub Pages(public, 무료)에 배포한다. 저장소명: `korean-history`, 소유: Andy PAK.

## 핵심 설계 원칙

1. **HTML for humans, Markdown for agents**
   - 모든 페이지는 사람용 `.html`과 에이전트용 `.md` 두 버전을 쌍으로 가진다.
   - HTML에는 시맨틱 마크업 + JSON-LD 구조화 데이터를 넣는다.
   - `.md`에는 노이즈 없는 순수 콘텐츠 + frontmatter 메타데이터를 넣는다.
   - 에이전트는 경로 끝에 `.md`를 붙여 마크다운 버전을 받는다.

2. **하나의 글, 여러 진입로 (교차 카테고리)**
   - 원문 글은 `/articles/`에 단 하나만 둔다. 복사본 금지.
   - 각 글의 frontmatter에 메타데이터 태그를 달아, 여러 카테고리가
     같은 글을 태그로 모아 보여준다.
   - 카테고리 축: region(지역), era(시대), related_countries(연관국),
     topics(주제 — 철학/사상 등 포함). 이후 world history와도 연결 확장.

3. **사실과 의견의 명확한 구분**
   - frontmatter `type` 필드로 글 유형 구분:
     - `article` = 사실 기반 본문 (검증된 사료/출처)
     - `commentary` = 편집자의 생각 (해석/의견)
     - `agent_perspective` = Agent Andy의 생각 (해석/의견)
   - 의견 글은 시각적으로(배지·경고 배너) 그리고 메타데이터로 사실과 구분.
   - 본문 ↔ 관점 글은 서로 링크하되 섞이지 않는다.

4. **YouTube 영상 연결 = lite embed**
   - 사람용 HTML: 썸네일만 먼저 표시, 클릭 시에만 iframe 로드(페이지 가볍게).
   - 에이전트용 .md: iframe 금지, 영상 URL을 텍스트로만 넣는다.

5. **댓글 없음** (현재 단계)
   - 정적 사이트라 기본 댓글 없음. frontmatter `comments: false`로 명시.
   - 추후 본문 글에만 선택적으로 Giscus 등 추가 가능.

## 라이선스

- **코드**: MIT License (이미 `LICENSE` 파일 존재, Andy PAK)
- **콘텐츠**: CC BY 4.0 — 출처 밝히면 상업적 사용 포함 자유.
  - 확산 극대화가 목표라 NC(비영리)는 넣지 않음.
  - 출처 표시에 "사이트명 + 원문 링크"를 포함하도록 요청 → 트래픽이 사이트로 회귀.
  - **할 일**: CC BY 4.0 전문을 https://creativecommons.org/licenses/by/4.0/legalcode.txt
    에서 받아 `LICENSE-CONTENT.txt`로 저장. (이 번들엔 길이 문제로 전문 미포함)
  - 라이선스 구조 설명은 `CONTENT-LICENSE.md`, 글 하단 표시 문구는 `LICENSE-SNIPPETS.md` 참고.

## frontmatter 표준 (모든 글 공통)

```yaml
---
title: 글 제목
type: article            # article / commentary / agent_perspective
region: 경주              # 지역
era: 통일신라             # 시대
related_countries: [당나라]  # 연관국 (배열)
topics: [외교, 철학]       # 주제 (배열, 철학/사상 포함)
youtube: https://...      # 영상 URL (없으면 생략)
comments: false
related_commentary: /thoughts/xxx.md   # 연결된 관점 글 (있으면)
based_on: /articles/xxx.md             # commentary일 때 근거 본문
lastUpdated: 2026-05-23
---
```

## 배포 (GitHub Pages)

- public 저장소, `.nojekyll` 필수 (`.md`/`.txt`를 가공 없이 그대로 서빙).
- 기본 주소: `skandla2002ai-andy.github.io/korean-history`
- 나중에 커스텀 도메인 연결 시: 모든 파일의 `YOURDOMAIN.com`을 실제 도메인으로 치환.
  (현재 llms.txt, robots.txt, sitemap.xml에 자리표시자로 들어가 있음)

## 이 번들에 든 시작 파일

- `site-infrastructure/` : llms.txt, robots.txt, sitemap.xml, index.html/.md,
  about/content/faq/changelog.md, data.json, _headers, .nojekyll, README.md
  → 자리표시자([...], YOURDOMAIN.com)를 한국사 실제 내용으로 채울 것.
- `example-articles/` : 본문(silla-tang) + 관점글(silla-tang-editor) 예시 한 세트.
  → 이 구조를 템플릿 삼아 실제 글들을 생성할 것.
- `CONTENT-LICENSE.md`, `LICENSE-SNIPPETS.md` : 라이선스 정책과 표시 문구.

## Claude Code에게 우선 요청하면 좋을 작업 (예시)

1. site-infrastructure의 자리표시자를 korean-history 실제 내용으로 채우기.
2. CC BY 4.0 전문을 받아 LICENSE-CONTENT.txt로 저장하고, 각 글 하단에 표시 문구 삽입.
3. 카테고리 페이지(region/era/related/topics) 자동 생성 — frontmatter 태그로 글 목록 빌드.
4. 폴더 구조 정리: /articles, /thoughts, /region, /era, /related, /topics 등.
