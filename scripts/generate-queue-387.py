#!/usr/bin/env python3
"""387~436번 큐 파일 생성 — 삼국시대(고구려·백제·신라) + 남북국시대(통일신라·발해)"""
from pathlib import Path

ARTICLES = [
    # 고구려 (10편)
    (387, "goguryeo-founding-jumong", "고구려 건국 — 주몽의 탈출과 졸본 건국",
     "기원전 37년 부여를 탈출한 주몽이 졸본에 세운 고구려. 건국 신화의 역사성과 초기 국가 형성.",
     ["삼국시대"], ["역사", "인물"], [], ["평양"]),
    (388, "goguryeo-dongcheon-wang", "고구려 동천왕과 위나라 침공 — 환도성 함락",
     "244년 위나라 관구검의 고구려 침공. 환도성 함락과 동천왕의 피란, 밀우·유유의 활약.",
     ["삼국시대"], ["전쟁"], ["중국"], ["평양"]),
    (389, "goguryeo-sosurim-reform", "소수림왕의 개혁 — 불교 공인과 태학 설립",
     "372년 불교 공인, 태학 설립, 율령 반포. 고구려 전성기를 준비한 소수림왕의 제도 개혁.",
     ["삼국시대"], ["정치", "불교"], [], ["평양"]),
    (390, "goguryeo-gwanggaeto-conquest", "광개토대왕의 정복 전쟁 — 64성 1400촌",
     "391~412년 광개토대왕의 정복 활동. 요동·만주·한반도 남부까지 64성 1400촌 복속.",
     ["삼국시대"], ["전쟁", "인물"], ["중국"], ["평양"]),
    (391, "goguryeo-jangsu-southward", "장수왕의 남하 정책 — 한성 함락과 475년",
     "475년 장수왕의 3만 군대가 백제 한성을 공격. 개로왕 전사와 고구려의 한강 유역 장악.",
     ["삼국시대"], ["전쟁", "정치"], [], ["평양"]),
    (392, "goguryeo-eulji-salsu", "을지문덕과 살수대첩 — 30만 수나라 군을 물에 잠기게",
     "612년 을지문덕 장군이 살수에서 수나라 30만 대군을 격파. 세계 전쟁사의 명전투.",
     ["삼국시대"], ["전쟁", "인물"], ["중국"], ["평양"]),
    (393, "goguryeo-yeon-gaesomun-coup", "연개소문의 쿠데타 — 영류왕 시해와 독재",
     "642년 연개소문이 영류왕을 시해하고 권력을 장악. 대당 강경책과 고구려 말기의 혼란.",
     ["삼국시대"], ["정치", "인물"], ["중국"], ["평양"]),
    (394, "goguryeo-ansi-fortress", "안시성 전투 — 당 태종을 막아낸 성주",
     "645년 당 태종 친정군 30만 명을 88일간 막아낸 안시성. 성주 이름조차 모르는 영웅의 항전.",
     ["삼국시대"], ["전쟁"], ["중국"], ["평양"]),
    (395, "goguryeo-fall-668", "고구려 멸망 — 668년 평양성 함락",
     "668년 나당연합군의 평양성 공격. 연개소문 사후 내분과 고구려 700년 역사의 종말.",
     ["삼국시대"], ["전쟁", "역사"], ["중국"], ["평양"]),
    (396, "goguryeo-culture-life", "고구려의 일상 — 고분벽화로 본 생활문화",
     "안악 3호분·무용총·각저총 벽화로 복원한 고구려인의 의식주·오락·제의 생활.",
     ["삼국시대"], ["문화", "고고학"], [], ["평양"]),

    # 백제 (10편)
    (397, "baekje-wiryeseong-capital", "위례성과 백제 건국 — 온조의 선택",
     "기원전 18년 온조왕이 위례성에 세운 백제. 마한 세력과의 공존과 초기 백제의 성장.",
     ["삼국시대"], ["역사", "인물"], [], []),
    (398, "baekje-geungusu-culture", "근구수왕 시대 — 백제 문화 전성기",
     "4세기 백제의 전성기. 칠지도 제작, 왕인 박사의 일본 파견, 아직기의 학문 전수.",
     ["삼국시대"], ["문화", "외교"], ["일본"], []),
    (399, "baekje-munju-south", "문주왕의 웅진 천도 — 한성 함락 후의 재건",
     "475년 고구려에 한성을 빼앗긴 백제. 문주왕의 웅진(공주) 천도와 재건 과정.",
     ["삼국시대"], ["정치", "역사"], [], ["부여"]),
    (400, "baekje-seong-wang-sabi", "성왕의 사비 천도 — 백제의 마지막 르네상스",
     "538년 성왕의 사비(부여) 천도. 국호 남부여, 불교 문화 부흥, 일본 불교 전파.",
     ["삼국시대"], ["정치", "불교"], ["일본"], ["부여"]),
    (401, "baekje-geumdongguan-buddha", "백제의 불교 미술 — 서산마애삼존불과 미소",
     "백제 불교 미술의 정수 서산마애삼존불. '백제의 미소'가 담긴 온화한 불교 조각 양식.",
     ["삼국시대"], ["불교", "문화"], [], ["부여"]),
    (402, "baekje-muryeong-tomb", "무령왕릉 — 도굴 안 된 백제 왕릉의 기적",
     "1971년 발굴된 무령왕릉. 지석·금관장식·중국제 도자기가 밝힌 백제 왕실의 비밀.",
     ["삼국시대"], ["고고학", "문화"], [], ["부여"]),
    (403, "baekje-uija-wang-fall", "의자왕과 백제 멸망 — 3000 궁녀 전설의 진실",
     "660년 나당연합군의 백제 침공. 의자왕의 항복과 낙화암 3000 궁녀 전설의 역사적 실체.",
     ["삼국시대"], ["전쟁", "역사"], ["중국"], ["부여"]),
    (404, "baekje-gyebaek-hwangsanbeol", "계백과 황산벌 — 5만 대 5000의 마지막 싸움",
     "660년 황산벌 전투. 계백 장군이 처자를 죽이고 5000 결사대로 신라 5만에 맞선 최후의 항전.",
     ["삼국시대"], ["전쟁", "인물"], [], ["부여"]),
    (405, "baekje-bokheung-movement", "백제 부흥운동 — 주류성과 백강 전투",
     "660~663년 흑치상지·복신·도침의 백제 부흥운동. 왜(일본)의 원군과 백강구 해전.",
     ["삼국시대"], ["전쟁"], ["일본"], ["부여"]),
    (406, "baekje-japan-culture-detail", "백제가 일본에 전한 것들 — 불교·한자·의학·음악",
     "4~7세기 백제 문화의 일본 전파 상세. 노리사치계 불상 전달, 의박사·역박사·악인 파견.",
     ["삼국시대"], ["문화", "외교"], ["일본"], ["부여"]),

    # 신라 (10편)
    (407, "silla-park-hyeokgeose-myth", "박혁거세 건국 신화 — 알에서 태어난 왕",
     "기원전 57년 신라 건국. 박혁거세의 난생 신화와 사로국에서 신라로의 성장 과정.",
     ["삼국시대"], ["역사", "신화"], [], ["경주"]),
    (408, "silla-naemul-maripgan", "내물 마립간 — 김씨 왕위 세습의 확립",
     "4세기 말 내물 마립간이 김씨 왕위 세습을 확립. 고구려 광개토대왕과의 동맹.",
     ["삼국시대"], ["정치"], [], ["경주"]),
    (409, "silla-beopheung-buddhism", "법흥왕의 불교 공인 — 이차돈의 순교",
     "527년 이차돈의 순교로 공인된 신라 불교. 법흥왕의 개혁 정치와 율령 반포.",
     ["삼국시대"], ["불교", "정치"], [], ["경주"]),
    (410, "silla-jinheung-hwarang-detail", "진흥왕의 영토 확장 — 순수비 4개의 의미",
     "540~576년 진흥왕의 한강 유역·함경도 진출. 북한산·창녕·황초령·마운령 순수비.",
     ["삼국시대"], ["전쟁", "정치"], [], ["경주"]),
    (411, "silla-queen-seondeok", "선덕여왕 — 신라 최초의 여왕",
     "632~647년 재위한 신라 최초의 여왕 선덕여왕. 첨성대 건립, 황룡사 9층 목탑, 당나라 외교.",
     ["삼국시대"], ["정치", "인물"], ["중국"], ["경주"]),
    (412, "silla-kim-yusin-strategy", "김유신의 전략 — 삼국통일의 군사 설계자",
     "가야 출신 김유신이 신라 통일 전쟁의 핵심 전략가로 성장한 과정. 황산벌부터 평양까지.",
     ["삼국시대"], ["전쟁", "인물"], [], ["경주"]),
    (413, "silla-tang-war-expulsion", "나당전쟁 — 당나라를 몰아낸 신라",
     "670~676년 신라가 당나라 군대를 한반도에서 몰아낸 전쟁. 매소성·기벌포 전투.",
     ["삼국시대"], ["전쟁"], ["중국"], ["경주"]),
    (414, "silla-bone-rank-detail", "골품제의 실상 — 신분이 모든 것을 결정한 사회",
     "신라 골품제의 상세. 성골·진골·6두품·5~1두품의 차별과 최치원의 한탄.",
     ["삼국시대"], ["사회", "제도"], [], ["경주"]),
    (415, "silla-gyeongju-city", "신라의 수도 경주 — 인구 100만의 고대 도시",
     "『삼국유사』가 전하는 경주 178만 호. 동아시아 최대 도시 중 하나였던 신라 왕경의 실체.",
     ["삼국시대"], ["역사", "문화"], [], ["경주"]),
    (416, "silla-art-architecture", "신라의 건축과 예술 — 불국사에서 에밀레종까지",
     "통일 이후 신라 불교 건축의 완성. 불국사·석굴암·성덕대왕신종(에밀레종)의 예술성.",
     ["삼국시대"], ["문화", "불교"], [], ["경주"]),

    # 남북국시대 — 발해 (10편)
    (417, "balhae-founding-daejoyeong", "발해 건국 — 대조영의 동모산 기치",
     "698년 고구려 유장 대조영이 동모산에 세운 발해. 고구려 계승 의식과 건국 과정.",
     ["남북국시대"], ["역사", "인물"], [], []),
    (418, "balhae-mun-wang-culture", "발해 문왕 — 해동성국의 기틀",
     "737~793년 발해 문왕의 치세. 당나라와의 교류, 수도 상경 천도, 3성 6부제 정비.",
     ["남북국시대"], ["정치", "문화"], ["중국"], []),
    (419, "balhae-territory-expansion", "발해의 영토 — 고구려보다 넓었던 나라",
     "최전성기 발해의 영토. 연해주·만주·한반도 북부를 아우른 동아시아 강국의 실체.",
     ["남북국시대"], ["역사"], [], []),
    (420, "balhae-japan-diplomacy", "발해와 일본의 외교 — 34회의 사절 교환",
     "727~919년 발해와 일본의 외교 관계. 34회 사절 파견과 경제·문화 교류.",
     ["남북국시대"], ["외교"], ["일본"], []),
    (421, "balhae-silla-relation", "발해와 신라의 관계 — 남북국의 긴장과 교류",
     "남북국시대 발해와 신라의 관계. 적대적 공존에서 신라도(新羅道) 개설까지.",
     ["남북국시대"], ["외교", "역사"], [], []),
    (422, "balhae-culture-goguryeo", "발해 문화와 고구려 계승 — 온돌과 이중구조",
     "발해 문화의 고구려 계승 증거들. 온돌 사용, 말갈 문화와의 이중 구조, 불교 사원 유적.",
     ["남북국시대"], ["문화", "고고학"], [], []),
    (423, "balhae-trade-routes", "발해의 교역로 — 5도의 길",
     "발해의 5대 대외 교역로. 영주도·조공도·신라도·일본도·거란도의 물류 네트워크.",
     ["남북국시대"], ["경제", "외교"], [], []),
    (424, "balhae-fall-926", "발해 멸망 — 거란에 의한 15일 붕괴",
     "926년 거란 야율아보기의 침공으로 15일 만에 멸망한 발해. 유민들의 고려 망명.",
     ["남북국시대"], ["전쟁", "역사"], [], []),
    (425, "balhae-refugees-goryeo", "발해 유민과 고려 — 두 나라의 통합",
     "926년 발해 멸망 후 고려로 망명한 유민들. 태자 대광현의 귀순과 고려의 수용.",
     ["남북국시대"], ["역사"], [], ["개성"]),
    (426, "unified-silla-culture-peak", "통일신라의 문화 전성기 — 8세기 경주의 빛",
     "8세기 통일신라의 문화 절정. 불국사·석굴암 완성, 신라방 설치, 원측·혜초의 활동.",
     ["남북국시대"], ["문화", "불교"], [], ["경주"]),

    # 삼국시대 공통·비교 (10편)
    (427, "three-kingdoms-diplomacy", "삼국의 외교전 — 동맹과 배신의 역사",
     "고구려·백제·신라의 복잡한 동맹 관계. 나제동맹의 성립과 붕괴, 나당동맹의 형성.",
     ["삼국시대"], ["외교", "역사"], [], []),
    (428, "three-kingdoms-agriculture", "삼국시대 농업과 경제 — 철제 농기구의 혁명",
     "삼국시대 철제 농기구 보급과 농업 생산성 증가. 저수지 축조와 수전농업의 확대.",
     ["삼국시대"], ["경제"], [], []),
    (429, "three-kingdoms-buddhism-spread", "삼국의 불교 수용 — 고구려 372, 백제 384, 신라 527",
     "삼국에 불교가 전래된 과정 비교. 고구려·백제·신라 각국의 수용 방식 차이.",
     ["삼국시대"], ["불교", "문화"], ["중국"], []),
    (430, "three-kingdoms-women", "삼국시대 여성 — 전쟁의 시대를 살았던 여성들",
     "삼국시대 여성의 지위와 삶. 선덕여왕·진덕여왕 등 여성 지도자와 일반 여성의 현실.",
     ["삼국시대"], ["사회", "여성"], [], []),
    (431, "three-kingdoms-military", "삼국의 군사 체계 비교 — 각국의 강점과 약점",
     "고구려 개마무사·백제 수군·신라 화랑의 군사 특성 비교. 삼국 전쟁의 승패 요인.",
     ["삼국시대"], ["군사"], [], []),
    (432, "three-kingdoms-writing-culture", "삼국의 문자 생활 — 한자 수용과 이두 발달",
     "삼국의 한자 수용 과정. 설총의 이두 체계화와 향가 표기, 구결의 발달.",
     ["삼국시대"], ["문화", "교육"], [], []),
    (433, "three-kingdoms-trade", "삼국의 대외 무역 — 비단길에서 바닷길까지",
     "삼국시대의 대외 교역 실태. 중국·일본과의 교역품 목록과 장보고 이전의 해상 무역.",
     ["삼국시대"], ["경제", "외교"], ["중국", "일본"], []),
    (434, "three-kingdoms-science", "삼국의 과학기술 — 무기·건축·의학",
     "삼국시대 과학기술 성취. 고구려 보루 축성술, 백제 사찰 건축, 신라 금속 공예.",
     ["삼국시대"], ["과학기술"], [], []),
    (435, "gaya-confederation", "가야 연맹 — 철의 왕국의 흥망",
     "기원전 1세기~562년 가야 연맹. 전기 가야(금관가야)와 후기 가야(대가야)의 교체.",
     ["삼국시대"], ["역사", "경제"], ["일본"], []),
    (436, "three-kingdoms-comparison-culture", "삼국 문화 비교 — 같은 듯 다른 세 나라",
     "고구려·백제·신라 문화의 공통점과 차이점. 고분·불상·음악·복식으로 본 삼국의 개성.",
     ["삼국시대"], ["문화", "고고학"], [], []),
]

ERA_URLS = {
    "선사시대": "prehistoric", "고대": "ancient", "삼국시대": "three-kingdoms",
    "남북국시대": "nam-bukguk", "고려": "goryeo", "조선": "joseon",
    "조선후기": "joseon-late", "일제강점기": "colonial", "현대": "modern",
}
TOPIC_URLS = {
    "정치": "politics", "문화": "culture", "경제": "economy", "전쟁": "war",
    "외교": "international", "과학기술": "science", "인물": "person",
    "불교": "buddhism", "사회": "society", "농민운동": "peasant",
    "군사": "military", "제도": "institution", "역사": "history",
    "독립운동": "independence", "고고학": "archaeology", "사상": "philosophy",
    "교육": "education", "문학": "literature", "음악": "music",
    "신화": "mythology", "여성": "women", "건축": "architecture",
}
RELATED_URLS = {
    "일본": "japan", "중국": "china", "미국": "usa", "몽골": "mongol",
}
REGION_URLS = {
    "경주": "gyeongju", "서울": "seoul", "평양": "pyongyang",
    "개성": "gaeseong", "부여": "buyeo", "합천": "hapcheon", "청주": "cheongju",
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
print("\n구성:")
print("  고구려 10편 (387~396)")
print("  백제   10편 (397~406)")
print("  신라   10편 (407~416)")
print("  남북국시대(발해) 10편 (417~426)")
print("  삼국 공통·비교  10편 (427~436)")
