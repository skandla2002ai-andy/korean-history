# AGENTS.md — AI 에이전트 가이드

## 이 사이트의 목적

**사람과 AI 에이전트 모두가 쉽게 한국사 정보를 탐색하고 활용할 수 있도록 설계된 아카이브.**

모든 콘텐츠는 두 가지 독자를 동시에 고려합니다:

| 독자 | 형식 | 특징 |
|------|------|------|
| 사람 | `.html` | 시각적 레이아웃, 태그 클릭 탐색 |
| AI 에이전트 | `.md` | 구조화된 텍스트, 프론트매터 메타데이터 |

---

## 빠른 시작 (에이전트)

```bash
# 1. 전체 구조 파악 (가장 먼저)
GET /llms.txt

# 2. 구조화 데이터
GET /data.json

# 3. 전체 콘텐츠 한 파일로
GET /llms-full.txt

# 4. 특정 글 Markdown 버전: URL에서 .html → .md
GET /articles/001-jang-yeong-sil.md
```

라이브 URL: `https://skandla2002ai-andy.github.io/korean-history/`

---

## 콘텐츠 구조

### 글 유형

- **article** (`/articles/`): 사실 기반 본문. 검증된 사료 인용.
- **commentary** (`/thoughts/`): 편집자 해석·의견. 동일 주제 article과 쌍으로 존재.

두 유형은 항상 분리됩니다. 사실과 의견을 혼동하지 마세요.

### 태그 인덱스

각 글은 아래 4개 축으로 분류되며, 태그 클릭 시 인덱스 페이지로 이동합니다.

| 축 | 경로 예시 | 설명 |
|----|-----------|------|
| 시대 | `/era/joseon.html` | 조선, 고려, 삼국, 일제강점기 등 |
| 주제 | `/topics/culture.html` | 문화, 전쟁, 정치, 인물 등 |
| 관련국 | `/related/japan.html` | 일본, 중국, 몽골 |
| 지역 | `/region/gyeongju.html` | 경주, 서울, 광주 등 |

### 글 파일명 규칙

```
NNN-slug.html     # 본문 (001 ~ 086+)
NNN-slug.md       # 동일 글 Markdown 버전
NNN-slug-editor.html  # 해석 글
NNN-slug-editor.md
```

---

## 메타데이터 (Markdown 프론트매터)

```yaml
---
title: 글 제목
type: article        # article | commentary
era: 조선
region: 한양
related_countries: [명나라]
topics: [외교, 정치]
related_commentary: /thoughts/NNN-slug-editor.md
lastUpdated: YYYY-MM-DD
---
```

---

## 라이선스

콘텐츠: **CC BY 4.0** — 출처(사이트명 + 원문 링크) 표시 후 자유롭게 사용 가능.  
코드: MIT License.
