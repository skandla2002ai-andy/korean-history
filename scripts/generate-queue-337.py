#!/usr/bin/env python3
"""337~386번 큐 파일 생성"""
from pathlib import Path

ARTICLES = [
    (337, "goryeo-haeinsa-history", "해인사의 역사 — 법보종찰의 천년",
     "802년 창건된 해인사. 팔만대장경을 품은 법보종찰의 역사와 수난.",
     ["고려"], ["불교", "문화"], [], ["합천"]),
    (338, "silla-cheomseongdae-detail", "첨성대의 구조와 과학 — 돌 362개의 비밀",
     "선덕여왕 때 세워진 첨성대. 362개 돌의 배치와 천문 관측의 실체.",
     ["삼국시대"], ["과학기술"], [], ["경주"]),
    (339, "joseon-gungnyeo-system", "조선 궁녀 제도 — 입궁에서 출궁까지",
     "조선 왕실의 여성 인력 궁녀. 선발·교육·역할·일상과 궁 밖 세계.",
     ["조선"], ["사회", "문화"], [], ["서울"]),
    (340, "goguryeo-dorim-baekje", "도림의 간첩 작전 — 고구려의 백제 침투 공작",
     "5세기 고구려 승려 도림이 백제 개로왕을 속여 국력을 소진시킨 첩보전.",
     ["삼국시대"], ["전쟁", "정치"], [], []),
    (341, "joseon-sahwa-four", "조선 4대 사화 — 선비들의 피바람",
     "무오·갑자·기묘·을사 4대 사화. 훈구파와 사림파의 권력 투쟁과 대량 처형.",
     ["조선"], ["정치"], [], []),
    (342, "goryeo-choi-chung-heon", "최충헌의 집권 — 고려판 막부의 탄생",
     "1196년 최충헌이 이의민을 제거하고 권력을 장악. 60년 최씨 무신정권의 시작.",
     ["고려"], ["정치", "인물"], [], ["개성"]),
    (343, "baekje-geuncho-expansion", "근초고왕의 정복 — 백제 최전성기",
     "4세기 근초고왕의 대외 팽창. 고구려 고국원왕 전사, 마한 통합, 일본 교류.",
     ["삼국시대"], ["전쟁", "정치"], ["일본"], []),
    (344, "joseon-gwonsul-strategy", "조선의 권술 전략 — 사대와 교린",
     "조선 외교의 양대 원칙 사대(事大)와 교린(交隣). 중국·일본·여진과의 관계 설정.",
     ["조선"], ["외교"], ["중국", "일본"], []),
    (345, "goryeo-uisang-hwaeom", "의상과 화엄종 — 신라 불교의 꽃",
     "당나라 유학 후 귀국한 의상. 화엄종 개창과 부석사 창건.",
     ["삼국시대"], ["불교", "인물"], ["중국"], ["경주"]),
    (346, "joseon-slave-trade", "조선의 노비 매매 — 사람이 재산이 된 사회",
     "조선 최대 신분층 노비. 매매·세습·도망·속량의 전 과정.",
     ["조선"], ["사회", "제도"], [], []),
    (347, "goryeo-jeong-seup", "정습명의 고려 — 문신 귀족 사회의 절정",
     "11~12세기 고려 문벌 귀족 사회. 음서제·통혼권·토지 독점의 구조.",
     ["고려"], ["사회", "정치"], [], ["개성"]),
    (348, "joseon-hyang-role", "향리의 역할 — 지방 행정의 실질적 담당자",
     "중앙에서 파견된 수령을 보좌한 향리. 조선 지방 행정의 실무를 맡은 중간 계층.",
     ["조선"], ["제도", "사회"], [], []),
    (349, "silla-musok-art", "신라 금관과 귀금속 공예 — 황금의 나라",
     "경주 고분에서 출토된 신라 금관. 북방 유목문화와 신라 고유 양식의 융합.",
     ["삼국시대"], ["문화", "고고학"], [], ["경주"]),
    (350, "joseon-350th", "350번 특집 — 한국사 아카이브 350편",
     "350번째 글 특집. 한국 역사 속 350가지 장면을 돌아보며.",
     ["조선"], ["역사"], [], []),
    (351, "goryeo-manbu-bridge", "만부교 사건 — 왕건의 거란 사신 모욕",
     "942년 고려 태조가 거란 사신을 유배보내고 낙타를 굶겨 죽인 사건.",
     ["고려"], ["외교", "정치"], [], ["개성"]),
    (352, "joseon-inwang-geumdan", "인왕산과 한양 풍수 — 조선 도읍지의 비밀",
     "한양 천도와 풍수지리. 북악산·인왕산·낙산·남산이 만드는 내사산의 의미.",
     ["조선"], ["문화", "역사"], [], ["서울"]),
    (353, "silla-gyerim-origin", "계림과 신라 국호 — 닭 울음소리의 건국 신화",
     "신라 국호의 유래와 계림. 김알지 탄생 설화와 경주 계림의 역사.",
     ["삼국시대"], ["신화", "역사"], [], ["경주"]),
    (354, "joseon-chunchu-exam", "춘추관과 실록 편찬 — 왕도 볼 수 없는 기록",
     "조선왕조실록 편찬 기관 춘추관. 왕도 볼 수 없는 사관 독립의 원칙.",
     ["조선"], ["문화", "제도"], [], ["서울"]),
    (355, "goryeo-hyun-deok-wang", "고려 현종과 거란 3차 침입 — 나라의 운명을 건 전투",
     "1018년 귀주대첩. 강감찬이 거란 10만 대군을 섬멸한 고려 최대 승전.",
     ["고려"], ["전쟁", "인물"], [], ["개성"]),
    (356, "joseon-hong-daeyong-thought", "홍대용의 지전설 — 지구가 돈다는 조선 선비",
     "18세기 실학자 홍대용. 지전설·무한우주론·화이관 타파의 근대적 사유.",
     ["조선"], ["사상", "과학기술"], [], []),
    (357, "ancient-gojoseon-culture", "고조선의 8조법 — 동아시아 최초의 법전",
     "고조선의 사회를 보여주는 8조법. 살인·상해·절도를 다룬 고대 법률 체계.",
     ["고대"], ["제도", "역사"], [], []),
    (358, "joseon-gyuhap-chongseo", "규합총서 — 조선 여성이 쓴 생활 백과사전",
     "1809년 빙허각 이씨가 쓴 조선 최대 여성 생활서. 음식·의복·태교·농업 망라.",
     ["조선"], ["문화", "여성"], [], []),
    (359, "goryeo-poetry-sicho", "고려 시조의 탄생 — 청산별곡과 가시리",
     "고려 시대 발생한 속요(俗謠). 청산별곡·가시리·동동 등 민중 문학의 정수.",
     ["고려"], ["문화", "문학"], [], []),
    (360, "joseon-ikseon-minjung", "민중의 조선 — 장시·두레·계의 공동체",
     "조선 민중의 경제 공동체. 5일장 장시, 농업 협동 두레, 상호부조 계의 사회사.",
     ["조선"], ["경제", "사회"], [], []),
    (361, "silla-trade-silk-road", "신라와 실크로드 — 경주에서 발견된 서역 유물",
     "경주 고분에서 나온 로만글라스·황금보검. 신라와 중앙아시아 교류의 증거.",
     ["삼국시대"], ["문화", "외교"], [], ["경주"]),
    (362, "joseon-cheokgyeong-jeon", "척경입비 — 조선의 국경 확정",
     "세종 시대 4군 6진 개척과 국경비 건립. 두만강·압록강을 국경으로 확정한 역사.",
     ["조선"], ["정치", "군사"], [], []),
    (363, "goryeo-gam-umsik", "고려의 음식 문화 — 불교 영향과 육식 금기",
     "불교 국가 고려의 음식 문화. 채식 중심 식생활과 특별한 날의 육식 허용.",
     ["고려"], ["문화"], [], []),
    (364, "joseon-bongsugang-flood", "봉수강과 조선 치수 — 홍수와 싸운 왕조",
     "조선 시대 반복된 홍수 피해와 치수 정책. 제언(저수지)·보(洑) 축조의 역사.",
     ["조선"], ["사회", "역사"], [], []),
    (365, "ancient-buyeo-kingdom", "부여 — 고구려의 어머니 나라",
     "고조선 붕괴 후 만주에 세워진 부여. 고구려·백제의 뿌리가 된 고대 국가.",
     ["고대"], ["역사"], [], []),
    (366, "joseon-portrait-painting", "조선의 초상화 — 털 하나도 틀리면 다른 사람",
     "조선 시대 초상화의 철학과 기법. 털 하나도 다르면 다른 사람이라는 전신사조론.",
     ["조선"], ["문화", "예술"], [], []),
    (367, "goryeo-haedong-yonggung", "해동용궁사 — 바다 위의 절",
     "고려 시대 창건된 부산 해동용궁사. 벼랑 끝 사찰의 역사와 기도 문화.",
     ["고려"], ["불교", "문화"], [], ["부산"]),
    (368, "joseon-hangyang-population", "한양의 인구와 도시 — 조선 최대 도시의 일상",
     "조선 후기 한양의 인구 20만. 육의전·시전·청계천 주변 도시 생활사.",
     ["조선"], ["사회", "역사"], [], ["서울"]),
    (369, "silla-hwarang-famous", "화랑의 유명 인물들 — 김유신에서 관창까지",
     "신라 화랑 출신 주요 인물들. 김유신·관창·사다함·죽지랑의 활약.",
     ["삼국시대"], ["인물", "군사"], [], ["경주"]),
    (370, "joseon-gisul-artisan", "조선의 장인 — 匠人, 기술로 시대를 만들다",
     "조선의 관영 장인 체계. 도자기·금속·목공·직조 장인의 신분과 기술 전승.",
     ["조선"], ["사회", "문화"], [], []),
    (371, "goryeo-mongol-culture-exchange", "몽골 지배하의 고려 — 원나라 문화 유입",
     "원 간섭기 고려에 유입된 몽골 문화. 복식·음식·언어·풍습의 변화.",
     ["고려"], ["문화", "외교"], ["몽골"], []),
    (372, "joseon-gisaeng-hwang-jini", "황진이 — 기생이자 시인이자 철학자",
     "조선 최고의 기생 황진이. 시조 문학의 대가로 선비들과 지적 교류를 나눈 삶.",
     ["조선"], ["문화", "인물", "여성"], [], []),
    (373, "ancient-samhan-society", "삼한 사회의 구조 — 마한·진한·변한",
     "기원전 1세기~3세기 한반도 남부의 삼한. 소도·천군·읍락의 사회 구조.",
     ["고대"], ["역사", "고고학"], [], []),
    (374, "joseon-donhwamun-court", "돈화문과 창덕궁 — 자연과 조화를 이룬 궁궐",
     "유네스코 세계문화유산 창덕궁. 후원(비원)의 아름다움과 조선 건축 미학.",
     ["조선"], ["문화", "건축"], [], ["서울"]),
    (375, "goryeo-haesang-trade", "고려 해상 무역의 실체 — 벽란도에 온 아라비아 상인",
     "『고려도경』에 기록된 벽란도 무역. 송·일본·아라비아 상인들의 고려 방문.",
     ["고려"], ["경제", "외교"], [], ["개성"]),
    (376, "joseon-yukjo-system", "육조 직계제와 의정부 서사제 — 권력 구조의 진자운동",
     "태종의 육조직계제와 세종의 의정부서사제. 왕권과 신권 사이의 균형 실험.",
     ["조선"], ["정치", "제도"], [], ["서울"]),
    (377, "silla-godae-music", "신라의 향악 — 가야금과 삼현삼죽",
     "신라의 전통 음악 향악. 가야금·거문고·향비파 등 삼현과 대금·중금·소금 삼죽.",
     ["삼국시대"], ["문화", "음악"], [], ["경주"]),
    (378, "joseon-korean-catholics", "조선 천주교 박해 — 신앙을 위해 죽은 사람들",
     "1801년 신유박해부터 1866년 병인박해까지. 조선 천주교 순교자 1만여 명의 이야기.",
     ["조선"], ["종교", "역사"], [], []),
    (379, "goryeo-gukja-education", "고려 국자감 — 고려의 국립대학",
     "992년 설립된 고려 최고 교육기관 국자감. 유교 경전과 기술학 교육.",
     ["고려"], ["교육", "제도"], [], ["개성"]),
    (380, "joseon-gwanno-liberation", "공노비 해방 — 순조의 6만6000명 해방령",
     "1801년 순조의 공노비 해방. 6만6000여 명의 관청 노비를 양민으로 해방한 역사.",
     ["조선"], ["사회", "제도"], [], []),
    (381, "three-kingdoms-art", "삼국시대 미술 — 고구려·백제·신라의 예술 비교",
     "삼국의 미술 양식 비교. 고구려 역동성, 백제 우아함, 신라 화려함의 차이.",
     ["삼국시대"], ["문화", "고고학"], [], []),
    (382, "joseon-pansori-five", "판소리 다섯 마당 — 조선 민중 오페라",
     "춘향가·심청가·흥보가·수궁가·적벽가. 판소리 다섯 마당의 내용과 역사.",
     ["조선"], ["문화", "음악"], [], []),
    (383, "goryeo-jikji-printing", "직지 인쇄의 비밀 — 금속활자는 어떻게 만들었나",
     "고려 금속활자 제조 기술의 실체. 밀랍 주조법과 활자 조판 과정의 복원.",
     ["고려"], ["과학기술", "문화"], [], ["청주"]),
    (384, "joseon-yeongwon-castle", "북한산성 — 한양 방어의 최후 보루",
     "1711년 숙종 때 완성된 북한산성. 한양 외곽 방어 전략과 44개 성문의 구조.",
     ["조선"], ["군사", "역사"], [], ["서울"]),
    (385, "ancient-jado-sado-route", "자도·사도 항로 — 고대 한반도의 해상 교통로",
     "삼국시대 서해안과 남해안을 잇는 고대 해상 교통로. 중국·일본 교류의 물길.",
     ["삼국시대"], ["외교", "역사"], [], []),
    (386, "joseon-daehak-meaning", "대학·중용·논어·맹자 — 조선 선비의 필독서",
     "조선 과거시험의 기본 텍스트 사서(四書). 성리학 이념의 핵심 경전들.",
     ["조선"], ["교육", "사상"], [], []),
]

ERA_URLS = {
    "선사시대": "prehistoric", "고대": "ancient", "삼국시대": "three-kingdoms",
    "고려": "goryeo", "조선": "joseon", "조선후기": "joseon-late",
    "일제강점기": "colonial", "현대": "modern",
}
TOPIC_URLS = {
    "정치": "politics", "문화": "culture", "경제": "economy", "전쟁": "war",
    "외교": "international", "과학기술": "science", "인물": "person",
    "불교": "buddhism", "사회": "society", "농민운동": "peasant",
    "군사": "military", "제도": "institution", "역사": "history",
    "독립운동": "independence", "일제강점": "colonial", "고고학": "archaeology",
    "사상": "philosophy", "교육": "education", "문학": "literature",
    "음악": "music", "산업화": "industry", "신화": "mythology",
    "여성": "women", "건축": "architecture", "예술": "art",
    "종교": "religion",
}
RELATED_URLS = {
    "일본": "japan", "중국": "china", "미국": "usa", "몽골": "mongol",
}
REGION_URLS = {
    "경주": "gyeongju", "서울": "seoul", "평양": "pyongyang",
    "개성": "gaeseong", "전주": "jeonju", "부여": "buyeo",
    "합천": "hapcheon", "청주": "cheongju", "인천": "incheon",
    "부산": "busan",
}

def make_tags(eras, topics, related, regions):
    tags = []
    for e in eras:
        slug = ERA_URLS.get(e)
        if slug:
            tags.append(f'    <a class="tag" href="/korean-history/era/{slug}.html"><b>시대</b> {e}</a>')
    for t in topics:
        slug = TOPIC_URLS.get(t)
        if slug:
            tags.append(f'    <a class="tag" href="/korean-history/topics/{slug}.html"><b>주제</b> {t}</a>')
    for r in related:
        slug = RELATED_URLS.get(r)
        if slug:
            tags.append(f'    <a class="tag" href="/korean-history/related/{slug}.html"><b>관련국</b> {r}</a>')
    for rg in regions:
        slug = REGION_URLS.get(rg)
        if slug:
            tags.append(f'    <a class="tag" href="/korean-history/region/{slug}.html"><b>지역</b> {rg}</a>')
    return "\n".join(tags)

def make_html(num, slug, title, lead, eras, topics, related, regions):
    era_label = eras[0] if eras else "한국사"
    tags_html = make_tags(eras, topics, related, regions)
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — 한국사 아카이브</title>
<meta name="description" content="{lead}">
<style>
  :root{{--bg:#f7f4ed;--ink:#211f1a;--muted:#6f6a60;--accent:#8a1c1c;--line:#e0d9c9;--tag-bg:#ece5d6;--fact:#1f5c3d;--opinion:#9a6b1c}}
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
  .nav{{margin-bottom:2rem;font-family:'SF Mono',Menlo,monospace;font-size:.8rem}}
  .nav a{{color:var(--accent);text-decoration:none}}
  footer{{margin-top:4rem;padding-top:1.5rem;border-top:1px solid var(--line);font-family:'SF Mono',Menlo,monospace;font-size:.8rem;color:var(--muted)}}
  footer a{{color:var(--accent)}}
  .references{{margin-top:3rem;padding-top:1.5rem;border-top:1px solid var(--line)}}
  .references h2{{font-size:1.1rem;margin:0 0 .8rem;font-weight:600}}
  .references ol{{padding-left:1.3rem}}
  .references li{{font-size:.88rem;color:var(--muted);margin-bottom:.5rem;line-height:1.5}}
</style>
</head>
<body>
<main class="wrap">
  <div class="nav"><a href="/korean-history/">← 한국사 아카이브</a></div>
  <span class="kind">● 사실 기반 본문 / Article</span>
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
  <div class="tags">
{tags_html}
  </div>

  <h2>개요</h2>
  <p><!-- TODO: 내용 작성 --></p>

  <h2>배경과 전개</h2>
  <p><!-- TODO: 내용 작성 --></p>

  <h2>역사적 의의</h2>
  <p><!-- TODO: 내용 작성 --></p>

  <div class="references">
    <h2>참고 자료</h2>
    <ol>
      <li>한국민족문화대백과사전 — 한국학중앙연구원 (encykorea.aks.ac.kr)</li>
      <li>국사편찬위원회 한국사데이터베이스 (db.history.go.kr)</li>
    </ol>
  </div>
</main>
<footer>
  <div class="wrap" style="padding-top:0;padding-bottom:2rem">
    <a href="/korean-history/">한국사 아카이브</a> · {era_label} · CC BY 4.0
  </div>
</footer>
</body>
</html>
"""

queue_dir = Path("_queue/articles")
queue_dir.mkdir(parents=True, exist_ok=True)

created = 0
for num, slug, title, lead, eras, topics, related, regions in ARTICLES:
    fname = f"{num:03d}-{slug}.html"
    path = queue_dir / fname
    if path.exists():
        print(f"SKIP {fname}")
        continue
    path.write_text(make_html(num, slug, title, lead, eras, topics, related, regions), encoding="utf-8")
    print(f"CREATE {fname}")
    created += 1

print(f"\n=== 완료: {created}편 생성 ===")
