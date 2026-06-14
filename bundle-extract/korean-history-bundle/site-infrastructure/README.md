# Agent 친화 사이트 템플릿

사람을 위한 HTML과 AI 에이전트를 위한 깨끗한 Markdown을 동시에 제공하는 사이트 템플릿입니다.

## 핵심 설계

| 파일 | 대상 | 역할 |
|------|------|------|
| `index.html`, `*.html` | 사람 | 보기 좋은 웹페이지 (시맨틱 HTML + JSON-LD 포함) |
| `index.md`, `*.md` | 에이전트 | 노이즈 없는 깨끗한 본문. 토큰 절약 |
| `llms.txt` | 에이전트 | 사이트 목차 / 진입점 (업계 표준) |
| `llms-full.txt` | 에이전트 | 전체 콘텐츠 통합본 (외부 fetch 불필요) |
| `data.json` | 에이전트 | 기계 판독용 구조화 데이터 |
| `robots.txt` | 크롤러 | AI 봇 명시적 허용 + 사이트맵 |
| `sitemap.xml` | 검색엔진 | 페이지 우선순위 |
| `.nojekyll` | GitHub Pages | `.md`/`.txt`를 가공 없이 그대로 서빙 (필수) |

## 사용 방법

1. `YOURDOMAIN.com`을 실제 도메인으로 모두 치환
2. `[대괄호]` 안의 자리표시자를 실제 콘텐츠로 채우기
3. HTML과 동일 내용의 `.md` 파일 쌍을 항상 함께 유지

## GitHub Pages 배포

```bash
# 새 repo 생성 후
git init
git add .
git commit -m "Agent 친화 사이트"
git branch -M main
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main
```

그 다음 repo Settings → Pages → Source를 `main` 브랜치로 설정하면 끝.
`.nojekyll` 파일 덕분에 `.md`/`.txt`가 그대로 서빙됩니다.

## 한계와 다음 단계

GitHub Pages는 정적 호스팅이라 `Accept: text/markdown` 헤더 기반의
콘텐츠 협상(같은 URL에서 사람=HTML, 에이전트=Markdown 자동 분기)은 불가능합니다.
대신 `.md` 경로를 명시적으로 제공하는 방식으로 우회했습니다 — GitHub 자신도
자기 문서에서 쓰는 방식입니다.

콘텐츠 협상이 꼭 필요해지면 Cloudflare Pages / Vercel / Netlify로 옮기면 됩니다
(`_headers` 파일이 이미 준비되어 있음).
