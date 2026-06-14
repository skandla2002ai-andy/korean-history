# CLAUDE.md — Claude Code 작업 가이드

## 이 프로젝트의 핵심 목적

**사람과 AI 에이전트 모두가 쉽게 정보를 탐색·활용할 수 있는 한국사 아카이브.**

- 모든 글은 `.html`(사람용) + `.md`(에이전트용) 쌍으로 제공
- 사실 본문(`articles/`)과 편집자 해석(`thoughts/`)을 항상 분리
- 태그(시대·주제·지역·관련국) 클릭 → 인덱스 페이지로 이동하는 교차 탐색 구조
- `/llms.txt`, `/data.json`으로 에이전트가 전체 구조를 한 번에 파악 가능

---

## 저장소 구조

```
korean-history/
├── articles/           # 사실 기반 본문 (NNN-slug.html + .md)
├── thoughts/           # 편집자 해석·의견 (NNN-slug-editor.html + .md)
├── era/                # 시대 태그 인덱스 (joseon.html 등)
├── topics/             # 주제 태그 인덱스 (culture.html 등)
├── related/            # 관련국 태그 인덱스 (japan.html 등)
├── region/             # 지역 태그 인덱스 (gyeongju.html 등)
├── _queue/             # 발행 전 초안 (articles/ + thoughts/)
├── _data/              # 메타데이터 JSON
├── scripts/            # 빌드·자동화 스크립트
├── llms.txt            # 에이전트용 사이트 인덱스
├── llms-full.txt       # 전체 콘텐츠 통합본
└── data.json           # 구조화 데이터
```

## 현재 글 현황

- 발행 완료: `articles/` + `thoughts/` 각 다수 (번호 001~)
- 발행 대기: `_queue/articles/` + `_queue/thoughts/` (번호 기반 파일명)
- 태그 인덱스: `era/` 11개, `topics/` 14개, `related/` 3개, `region/` 6개

## 작업 규칙

- 글 번호는 3자리 (001, 002, …, 086, …)
- 새 글은 `_queue/`에 먼저 작성 → 검토 후 `articles/`로 이동
- 태그 인덱스에 새 글 추가 시 해당 인덱스 파일의 글 수(N편)도 함께 업데이트
- git commit은 Bash 도구 사용 (PowerShell heredoc이 한글 처리 불안정)
- 기존 파일 Write 전에 반드시 Read 먼저 실행

## 디자인 토큰

```css
--bg:#f7f4ed; --ink:#211f1a; --muted:#6f6a60;
--accent:#8a1c1c; --line:#e0d9c9;
--fact:#1f5c3d; --opinion:#9a6b1c
```

- 태그 배지(`.kind`): `background:rgba(138,28,28,.1); color:var(--accent)` (빨강)
- 글 배지(`.badge`): `background:rgba(31,92,61,.1); color:var(--fact)` (초록)
