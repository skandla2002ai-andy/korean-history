#!/usr/bin/env python3
"""437~536번 큐 파일 생성 — 100편"""
from pathlib import Path

ARTICLES = [
    # 고려 심화 (20편)
    (437, "goryeo-taejo-founding", "왕건의 고려 건국 — 후삼국 통일의 완성",
     "918년 왕건이 세운 고려. 후백제 멸망과 935년 신라 항복으로 완성된 후삼국 통일.",
     ["고려"], ["역사", "인물"], [], ["개성"]),
    (438, "goryeo-gwangjong-reform", "광종의 개혁 — 노비안검법과 과거제",
     "949년 광종의 노비안검법 실시와 958년 과거제 도입. 호족 세력 억제와 왕권 강화.",
     ["고려"], ["정치", "제도"], [], ["개성"]),
    (439, "goryeo-seongjong-system", "성종의 제도 정비 — 고려 통치 체계의 완성",
     "981년 성종의 중앙·지방 통치 체계 정비. 최승로의 시무 28조와 유교 정치 이념 확립.",
     ["고려"], ["정치", "제도"], [], ["개성"]),
    (440, "goryeo-hyeonjong-war", "현종과 거란 전쟁 — 나라의 운명을 건 30년",
     "993·1010·1018년 거란의 3차 침입. 강조의 정변, 현종의 피난, 강감찬의 귀주대첩.",
     ["고려"], ["전쟁"], [], ["개성"]),
    (441, "goryeo-munjong-culture", "문종 시대 — 고려의 황금기",
     "1046~1083년 문종의 치세. 경제 번영, 대각국사 의천 출가, 고려 문화의 전성기.",
     ["고려"], ["문화", "정치"], [], ["개성"]),
    (442, "goryeo-injong-ijaegyeom", "이자겸의 난 — 외척 권력의 극단",
     "1126년 이자겸이 일으킨 반란. 왕의 외조부가 왕을 가둔 고려 최대 권력 다툼.",
     ["고려"], ["정치"], [], ["개성"]),
    (443, "goryeo-myocheong-rebellion", "묘청의 난 — 서경 천도 운동의 실패",
     "1135년 묘청의 서경 천도 운동과 반란. 풍수지리 사상과 자주파 대 사대파의 충돌.",
     ["고려"], ["정치", "사상"], [], ["평양"]),
    (444, "goryeo-choe-uicheong", "최우와 강화 천도 — 39년의 항쟁",
     "1232년 강화도 천도. 최우 무신정권의 항몽 결정과 39년간의 강화도 시대.",
     ["고려"], ["전쟁", "정치"], ["몽골"], ["개성"]),
    (445, "goryeo-sambyeolcho-detail", "삼별초의 항쟁 — 진도에서 제주까지",
     "1270~1273년 삼별초의 대몽 항쟁. 진도 용장성, 제주 항파두리, 마지막 저항.",
     ["고려"], ["전쟁"], ["몽골"], []),
    (446, "goryeo-gongmin-reform", "공민왕의 개혁 — 원나라 간섭 청산",
     "1356년 공민왕의 반원 개혁. 쌍성총관부 탈환, 기철 숙청, 신돈의 등용.",
     ["고려"], ["정치", "인물"], ["중국"], ["개성"]),
    (447, "goryeo-sindon-reform", "신돈의 등장 — 공민왕의 마지막 실험",
     "1365~1371년 승려 신돈의 개혁 정치. 전민변정도감, 노비 해방, 기득권과의 충돌.",
     ["고려"], ["정치", "불교"], [], ["개성"]),
    (448, "goryeo-choe-yeong-vs-yi", "최영과 이성계 — 고려의 마지막 선택",
     "요동 정벌을 주장한 최영과 위화도 회군을 단행한 이성계. 고려 멸망의 분기점.",
     ["고려"], ["전쟁", "인물"], [], ["개성"]),
    (449, "goryeo-jeong-mongju-death", "정몽주의 죽음 — 선죽교의 붉은 피",
     "1392년 선죽교에서 이방원에게 살해된 정몽주. 고려 충신의 마지막과 조선 건국.",
     ["고려"], ["인물", "정치"], [], ["개성"]),
    (450, "goryeo-printing-culture", "고려의 출판 문화 — 금속활자와 목판 인쇄",
     "세계 최초 금속활자 발명국 고려. 대장경 목판 인쇄와 금속활자 기술의 발전 과정.",
     ["고려"], ["문화", "과학기술"], [], ["개성"]),
    (451, "goryeo-architecture", "고려 건축 — 부석사 무량수전과 배흘림기둥",
     "고려 시대 목조 건축의 정수. 부석사 무량수전·봉정사 극락전·수덕사 대웅전.",
     ["고려"], ["문화", "건축"], [], []),
    (452, "goryeo-goryeosa-history", "『고려사』편찬 — 조선이 기록한 고려",
     "1451년 조선이 편찬한 『고려사』. 기전체 역사서의 구성과 고려 역사 서술의 특징.",
     ["고려"], ["문화", "역사"], [], []),
    (453, "goryeo-social-structure", "고려의 신분 구조 — 귀족·양인·천민",
     "고려 사회의 신분 체계. 문벌 귀족·향리·양인·천민·노비의 구조와 신분 이동.",
     ["고려"], ["사회", "제도"], [], []),
    (454, "goryeo-economy-land", "고려의 토지 제도 — 전시과와 농민 수탈",
     "고려 토지 제도의 핵심 전시과. 개정전시과·경정전시과와 농민 부담의 실태.",
     ["고려"], ["경제", "제도"], [], []),
    (455, "goryeo-foreign-trade-detail", "고려 대외 무역의 품목 — 비단·인삼·도자기",
     "고려 수출입 품목의 실태. 송나라 비단·약재 수입, 인삼·나전칠기·고려청자 수출.",
     ["고려"], ["경제", "외교"], ["중국"], []),
    (456, "goryeo-decline-reasons", "고려 쇠퇴의 원인 — 귀족 사회의 모순",
     "고려 멸망의 구조적 원인. 권문세족의 토지 겸병, 농민 유망, 왜구·홍건적 침입.",
     ["고려"], ["역사", "사회"], [], []),

    # 조선 심화 (20편)
    (457, "joseon-taejo-politics", "태조 이성계의 통치 — 새 왕조의 설계",
     "1392년 이성계의 즉위와 초기 통치. 한양 천도, 개국 공신, 정도전과의 관계.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (458, "joseon-taejong-power", "태종 이방원 — 피로 세운 왕권",
     "두 차례 왕자의 난으로 왕위에 오른 태종. 공신 제거, 외척 숙청, 왕권 강화 과정.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (459, "joseon-sejong-science", "세종의 과학 진흥 — 집현전과 발명의 시대",
     "세종 시대의 과학기술 혁신. 집현전, 자격루, 앙부일구, 측우기, 칠정산 편찬.",
     ["조선"], ["과학기술", "인물"], [], ["서울"]),
    (460, "joseon-sejo-six-martyrs", "세조와 사육신 — 쿠데타와 충절",
     "1455년 세조의 단종 폐위 쿠데타. 사육신의 복위 시도와 처형, 생육신의 은거.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (461, "joseon-seongjong-law", "성종과 경국대전 — 법치 국가의 완성",
     "1485년 『경국대전』 반포. 조선의 기본 법전 완성과 문화 전성기 성종의 치세.",
     ["조선"], ["정치", "제도"], [], ["서울"]),
    (462, "joseon-yeonsangun-tyranny", "연산군의 폭정 — 조선 최악의 왕",
     "무오사화·갑자사화를 일으킨 연산군. 폭정의 원인과 1506년 중종반정으로 폐위.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (463, "joseon-imjin-causes", "임진왜란의 원인 — 왜 조선은 속수무책이었나",
     "1592년 임진왜란 발발 배경. 일본의 통일과 도요토미의 야욕, 조선의 방비 태만.",
     ["조선"], ["전쟁"], ["일본"], []),
    (464, "joseon-imjin-sea-battles", "이순신의 해전 전략 — 옥포에서 노량까지",
     "임진왜란 7년 해전의 전모. 옥포·사천·한산도·명량·노량 해전의 전략과 전술.",
     ["조선"], ["전쟁", "인물"], ["일본"], []),
    (465, "joseon-gwanghaegun-detail", "광해군의 외교 — 중립 외교의 빛과 그림자",
     "광해군의 후금·명 사이 중립 외교. 인조반정 이후 재평가된 실용 외교의 실체.",
     ["조선"], ["외교", "인물"], ["중국"], []),
    (466, "joseon-injo-revolt", "인조반정 — 서인의 쿠데타",
     "1623년 서인이 광해군을 몰아낸 인조반정. 반정의 명분과 실제 동기.",
     ["조선"], ["정치"], [], ["서울"]),
    (467, "joseon-hyojong-buk", "효종의 북벌론 — 이루어지지 못한 복수",
     "병자호란 인질 출신 효종의 청나라 북벌 계획. 군비 강화의 실상과 실패 원인.",
     ["조선"], ["정치", "군사"], ["중국"], []),
    (468, "joseon-sukjong-jang-ok-jeong", "숙종과 장옥정 — 사랑과 권력의 비극",
     "인현왕후 폐위와 장희빈(장옥정)의 사사. 환국 정치의 소용돌이 속 왕실 비극.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (469, "joseon-yeongjo-sado", "영조와 사도세자 — 아버지가 아들을 죽이다",
     "1762년 영조가 사도세자를 뒤주에 가두어 죽인 임오화변. 당쟁과 부자의 비극.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (470, "joseon-jeongjo-reform", "정조의 개혁 정치 — 탕평과 규장각",
     "정조의 개혁 정치 전모. 규장각 설치, 장용영 창설, 수원 화성, 신해통공.",
     ["조선"], ["정치", "인물"], [], ["서울"]),
    (471, "joseon-sunjo-seodo", "순조의 세도정치 — 안동 김씨의 60년",
     "1800년 이후 안동 김씨·풍양 조씨 세도정치. 매관매직, 삼정 문란, 민란의 원인.",
     ["조선"], ["정치"], [], []),
    (472, "joseon-three-disorders", "삼정의 문란 — 조선 말기 민중의 고통",
     "전정·군정·환곡의 삼정 문란. 수탈 구조의 실태와 농민 봉기의 직접 원인.",
     ["조선"], ["사회", "경제"], [], []),
    (473, "joseon-hong-gyeongnae-detail", "홍경래의 난 상세 — 100일간의 저항",
     "1811년 홍경래 난의 전개 상세. 가산·정주성 전투와 100일간의 항전 끝 진압.",
     ["조선"], ["농민운동"], [], ["평양"]),
    (474, "joseon-jin-ju-uprising", "진주 농민 봉기 — 1862년 임술민란",
     "1862년 진주에서 시작된 임술민란. 유계춘의 봉기와 전국 70여 군현의 연쇄 폭발.",
     ["조선"], ["농민운동"], [], []),
    (475, "joseon-culture-late", "조선 후기 문화의 변화 — 서민 문화의 등장",
     "18~19세기 조선 후기 서민 문화. 판소리·민화·한글 소설·탈춤의 발전.",
     ["조선"], ["문화"], [], []),
    (476, "joseon-practical-science", "조선의 실용 과학 — 농서·의서·지리서",
     "조선 시대 실용 과학 출판. 『농사직설』·『동의보감』·『동국여지승람』의 의의.",
     ["조선"], ["과학기술", "문화"], [], []),

    # 근현대 심화 (20편)
    (477, "colonial-culture-movement", "일제강점기 문화 운동 — 민족 정체성 지키기",
     "1920~30년대 조선 문화 운동. 조선어학회, 조선사편수회 비판, 민족 문화 수호 활동.",
     ["일제강점기"], ["문화", "독립운동"], ["일본"], []),
    (478, "colonial-economic-exploitation", "일제 경제 수탈의 구조 — 쌀과 지하자원",
     "일제강점기 조선 경제 수탈. 미곡 수탈, 광산 채굴, 공업 배치의 식민지 경제 구조.",
     ["일제강점기"], ["경제", "일제강점"], ["일본"], []),
    (479, "colonial-education-policy", "일제 교육 정책 — 황국신민 만들기",
     "조선교육령의 변화. 일본어 강제, 조선어 교육 폐지, 황국신민서사 암송.",
     ["일제강점기"], ["교육", "일제강점"], ["일본"], []),
    (480, "independence-february-eighth", "2·8 독립선언 — 3·1운동의 불씨",
     "1919년 2월 8일 도쿄 조선 유학생들의 독립선언. 3·1운동 직전 도화선이 된 선언.",
     ["일제강점기"], ["독립운동"], ["일본"], []),
    (481, "independence-april-government", "임시정부 법통 — 대한민국 헌법의 뿌리",
     "대한민국 헌법 전문의 '임시정부 법통 계승'. 임시정부의 법적·역사적 의의.",
     ["일제강점기"], ["독립운동", "정치"], [], []),
    (482, "independence-armed-struggle", "무장 독립투쟁의 역사 — 홍범도에서 김좌진까지",
     "1910~1930년대 만주 무장 독립투쟁. 홍범도의 봉오동, 김좌진의 청산리 대첩.",
     ["일제강점기"], ["독립운동", "전쟁"], [], []),
    (483, "liberation-1945-chaos", "1945년 8월 15일 — 해방의 혼란",
     "광복 직후 한반도의 혼란. 건준 활동, 미·소 분할 점령, 신탁통치 논쟁.",
     ["현대"], ["역사", "정치"], ["미국"], []),
    (484, "korea-division-reason", "한반도 분단의 원인 — 38도선은 어떻게 그어졌나",
     "1945년 38도선 획정의 경위. 미·소 협의와 한반도 분할 점령의 역사적 과정.",
     ["현대"], ["역사", "외교"], ["미국"], []),
    (485, "korea-war-causes", "6·25 전쟁의 원인 — 왜 전쟁이 일어났나",
     "1950년 6·25 전쟁 발발 배경. 소련·중국의 지원, 김일성의 남침 결정 과정.",
     ["현대"], ["전쟁"], [], []),
    (486, "korea-war-civilian", "6·25 전쟁의 민간인 피해 — 피란과 학살",
     "한국전쟁 민간인 피해의 실상. 피란민 행렬, 부역자 처형, 거제도 포로수용소.",
     ["현대"], ["전쟁", "사회"], [], []),
    (487, "rhee-syngman-government", "이승만 정부 — 건국과 독재 사이",
     "1948~1960년 이승만 정부. 발췌개헌·사사오입 개헌, 4·19 혁명으로 하야.",
     ["현대"], ["정치", "인물"], [], ["서울"]),
    (488, "park-chunghee-economy", "박정희의 경제 개발 — 한강의 기적",
     "1960~70년대 박정희 정부의 경제 개발. 경부고속도로, 포항제철, 수출 100억 달러.",
     ["현대"], ["경제", "인물"], [], []),
    (489, "park-chunghee-dictatorship", "박정희 유신체제 — 영구 집권의 설계",
     "1972년 유신헌법. 통일주체국민회의·긴급조치·중앙정보부로 구축된 독재 체제.",
     ["현대"], ["정치"], [], []),
    (490, "chun-doo-hwan-regime", "전두환 정권 — 5·18 이후의 군부 통치",
     "1980년 5·18 이후 전두환 정권. 삼청교육대, 언론 통폐합, 야간 통행금지.",
     ["현대"], ["정치"], [], []),
    (491, "june-democracy-detail", "6월 민주항쟁 상세 — 넥타이 부대와 직선제",
     "1987년 6월 민주항쟁의 전개. 박종철·이한열 사망, 넥타이 부대 합류, 6·29 선언.",
     ["현대"], ["정치", "사회"], [], ["서울"]),
    (492, "korea-imf-recovery", "IMF 극복 — 금 모으기 운동과 구조 조정",
     "1997년 외환위기와 IMF 구제금융. 금 모으기 운동, 기업 구조조정, 극복 과정.",
     ["현대"], ["경제"], [], []),
    (493, "korea-sunshinePolicy", "햇볕정책 — 남북 화해의 10년",
     "김대중 정부의 햇볕정책. 2000년 남북정상회담, 금강산 관광, 개성공단의 성과와 한계.",
     ["현대"], ["외교", "정치"], [], []),
    (494, "korea-democracy-development", "한국 민주주의 발전 — 87년 체제의 성과",
     "1987년 직선제 이후 한국 민주주의 발전. 문민정부·국민의정부·노무현 탄핵.",
     ["현대"], ["정치"], [], []),
    (495, "korea-culture-industry", "한국 문화산업의 성장 — BTS 이전의 역사",
     "한류의 역사. 1990년대 서태지에서 한류 1.0, K-드라마, K-팝 세계화까지.",
     ["현대"], ["문화"], [], []),
    (496, "korea-women-modern", "한국 여성의 근현대 — 신여성에서 페미니즘까지",
     "근현대 한국 여성의 역사. 나혜석·박인덕 신여성 운동에서 현대 페미니즘까지.",
     ["현대"], ["사회", "여성"], [], []),

    # 선사·고대 (10편)
    (497, "paleolithic-korea", "한반도 구석기시대 — 70만 년의 흔적",
     "전곡리 구석기 유적 발굴. 아슐리안 주먹도끼 발견과 한반도 구석기 문화의 재평가.",
     ["선사시대"], ["고고학", "역사"], [], []),
    (498, "neolithic-korea", "한반도 신석기시대 — 빗살무늬토기의 사람들",
     "기원전 8000~1500년 한반도 신석기문화. 빗살무늬토기, 움집, 조개더미 유적.",
     ["선사시대"], ["고고학", "역사"], [], []),
    (499, "gojoseon-wanggeom", "고조선의 왕검성 — 한반도 최초의 도시국가",
     "고조선의 수도 왕검성의 위치 논쟁. 평양설·요동설·이동설과 고조선의 실체.",
     ["고대"], ["역사", "고고학"], [], []),
    (500, "500th-special", "500번 특집 — 한국사 아카이브 500편을 향하여",
     "한국사 아카이브 500번째 글 특집. 선사시대부터 현대까지 한국 역사의 흐름.",
     ["현대"], ["역사"], [], []),
    (501, "ancient-okjeo-dongye", "옥저와 동예 — 고구려에 흡수된 소국들",
     "함경도·강원도 지역의 고대 소국 옥저와 동예. 고구려에 복속되기까지의 역사.",
     ["고대"], ["역사"], [], []),
    (502, "ancient-mahan-confederacy", "마한 연맹 — 54개 소국의 세계",
     "한반도 중서부의 마한 54개 소국. 목지국 맹주와 백제에 흡수되는 과정.",
     ["고대"], ["역사"], [], []),
    (503, "ancient-jinhan-saro", "진한과 사로국 — 신라의 씨앗",
     "경상도 지역 진한 12국과 사로국. 신라 전신 사로국의 초기 성장과 주변 소국 통합.",
     ["고대"], ["역사"], [], ["경주"]),
    (504, "ancient-byeonhan-gaya", "변한과 초기 가야 — 철의 산지",
     "경남 해안의 변한 12국. 풍부한 철 자원과 가야 연맹으로의 발전 과정.",
     ["고대"], ["역사", "경제"], [], []),
    (505, "ancient-wa-contact", "고대 한일 관계 — 왜와의 초기 교류",
     "고대 한반도와 일본 열도의 교류. 도래인, 철기 전파, 가야·백제의 일본 이주민.",
     ["고대"], ["외교", "역사"], ["일본"], []),
    (506, "ancient-china-han-commanderies", "한사군 — 한반도의 중국 지배",
     "기원전 108년 한 무제의 고조선 멸망 후 설치된 낙랑·임둔·진번·현도 4군.",
     ["고대"], ["역사"], ["중국"], []),

    # 대한제국 (10편)
    (507, "daehan-empire-founding", "대한제국 선포 — 황제국의 꿈",
     "1897년 고종의 황제 즉위와 대한제국 선포. 자주독립 의지와 국제 정세.",
     ["조선후기"], ["정치", "역사"], [], ["서울"]),
    (508, "daehan-army-reform", "대한제국 군사 개혁 — 원수부와 근대 군대",
     "대한제국의 군사 근대화. 원수부 설치, 무관학교, 징병제 검토와 한계.",
     ["조선후기"], ["군사", "정치"], [], ["서울"]),
    (509, "daehan-independence-club", "독립협회와 만민공동회 — 민중이 만든 광장",
     "1896~1898년 독립협회 활동. 독립문 건립, 만민공동회, 의회 설립 운동.",
     ["조선후기"], ["정치", "독립운동"], [], ["서울"]),
    (510, "daehan-gabo-reform", "갑오개혁의 내용 — 신분제 폐지와 근대화",
     "1894년 갑오개혁의 구체적 내용. 신분제 폐지, 과거제 폐지, 재정 일원화.",
     ["조선후기"], ["정치", "제도"], ["일본"], []),
    (511, "daehan-eulsa-protest", "을사늑약 저항 — 황제의 눈물과 순국",
     "1905년 을사늑약에 대한 저항. 고종의 비준 거부, 민영환 자결, 황성신문 논설.",
     ["조선후기"], ["정치", "독립운동"], ["일본"], ["서울"]),
    (512, "daehan-righteous-army", "의병 운동 — 평민 의병의 전국화",
     "을미·을사·정미 의병의 발전. 신돌석 평민 의병장, 13도 연합 의병과 서울 진공 작전.",
     ["조선후기"], ["독립운동", "전쟁"], ["일본"], []),
    (513, "daehan-hague-detail", "헤이그 특사 사건 — 이준의 죽음",
     "1907년 헤이그 만국평화회의 특사 파견. 이준·이상설·이위종의 활동과 이준 순국.",
     ["조선후기"], ["외교", "독립운동"], ["일본"], []),
    (514, "daehan-annexation-process", "국권 피탈 과정 — 1905년부터 1910년까지",
     "을사늑약(1905)→정미7조약(1907)→기유각서(1909)→한일병합(1910)의 단계적 과정.",
     ["조선후기"], ["역사", "일제강점"], ["일본"], []),
    (515, "daehan-last-moments", "대한제국의 마지막 — 합병 직전의 풍경",
     "1909~1910년 대한제국 말기의 풍경. 안중근 의거, 일진회 합방 청원, 병합 직전 분위기.",
     ["조선후기"], ["역사"], ["일본"], ["서울"]),
    (516, "daehan-modern-media", "대한제국의 언론 — 독립신문과 황성신문",
     "개화기 근대 신문의 탄생. 독립신문·황성신문·대한매일신보의 역할과 논조.",
     ["조선후기"], ["문화", "역사"], [], ["서울"]),

    # 특별 주제 (20편)
    (517, "korean-food-history", "한국 음식의 역사 — 된장찌개는 언제 생겼나",
     "한국 전통 음식의 역사. 장류(된장·간장·고추장)의 기원, 김치 변천사, 밥상 문화.",
     ["조선"], ["문화"], [], []),
    (518, "korean-house-hanok", "한옥의 역사 — 자연과 함께 사는 집",
     "한국 전통 가옥 한옥의 구조와 역사. 온돌·마루·대청·사랑채의 기능과 공간 철학.",
     ["조선"], ["문화", "건축"], [], []),
    (519, "korean-clothing-history", "한복의 변천 — 삼국시대부터 현대까지",
     "한복의 역사적 변천. 삼국시대 기본형에서 조선 시대 완성형, 개화기 변화까지.",
     ["조선"], ["문화"], [], []),
    (520, "korean-medicine-history", "한국 의학의 역사 — 향약에서 한의학까지",
     "한국 전통 의학의 발전. 삼국시대 의학 도입, 향약 개발, 허준의 동의보감까지.",
     ["조선"], ["과학기술", "문화"], [], []),
    (521, "korean-music-evolution", "한국 음악의 역사 — 국악의 탄생",
     "한국 전통 음악의 발전. 아악·향악·당악의 구분, 정간보 창안, 궁중음악의 체계화.",
     ["조선"], ["문화", "음악"], [], []),
    (522, "korean-writing-history", "한국어와 문자의 역사 — 이두에서 한글까지",
     "한국어 표기의 역사. 한자 차용(이두·향찰·구결)에서 훈민정음 창제까지의 과정.",
     ["조선"], ["문화", "교육"], [], []),
    (523, "korean-religion-shamanism", "한국 무속의 역사 — 무당과 굿의 세계",
     "한국 무속 신앙의 역사. 단군 신화와 무속의 연관성, 조선 시대 무당 탄압과 생존.",
     ["조선"], ["문화", "역사"], [], []),
    (524, "korean-ceramics-history", "한국 도자기의 역사 — 청자에서 분청사기·백자까지",
     "한국 도자기 발전사. 고려청자의 비색, 조선 분청사기, 조선 백자의 미학.",
     ["고려"], ["문화"], [], []),
    (525, "korean-painting-history", "한국 회화의 역사 — 고구려 벽화에서 김홍도까지",
     "한국 회화의 통사. 고구려 벽화·고려 불화·조선 산수화·풍속화의 발전.",
     ["조선"], ["문화"], [], []),
    (526, "korean-calligraphy", "한국 서예의 역사 — 명필들의 계보",
     "한국 서예의 역사. 삼국시대 한자 수용부터 김정희 추사체까지의 서예 발전.",
     ["조선"], ["문화"], [], []),
    (527, "korean-literature-history", "한국 문학의 역사 — 향가에서 현대소설까지",
     "한국 문학 통사. 신라 향가, 고려 속요, 조선 시조·가사, 개화기 신소설.",
     ["조선"], ["문화", "문학"], [], []),
    (528, "korean-science-tech-history", "한국 과학기술의 역사 — 세계 최초의 기록들",
     "한국의 세계 최초 과학기술. 금속활자, 측우기, 거북선, 온돌의 역사적 의의.",
     ["조선"], ["과학기술"], [], []),
    (529, "korean-philosophy-history", "한국 철학의 역사 — 원효에서 실학까지",
     "한국 철학 사상의 흐름. 원효의 화쟁, 이황의 이기론, 정약용의 실학까지.",
     ["조선"], ["사상"], [], []),
    (530, "korean-sports-history", "한국 전통 스포츠 — 씨름·택견·활쏘기",
     "한국 전통 스포츠의 역사. 씨름·택견·활쏘기·격구의 유래와 시대별 변천.",
     ["조선"], ["문화"], [], []),
    (531, "korean-festival-culture", "한국 전통 축제 — 세시풍속의 1년",
     "음력 1년의 세시풍속. 설날·대보름·단오·추석·동지의 풍습과 역사적 기원.",
     ["조선"], ["문화"], [], []),
    (532, "korean-social-movement", "한국 사회 운동의 역사 — 농민에서 노동자까지",
     "조선 농민 봉기에서 현대 노동 운동까지. 동학·3·1운동·4·19·6월항쟁의 계보.",
     ["현대"], ["사회"], [], []),
    (533, "korean-diaspora-history", "한국인의 해외 이주사 — 200만의 여정",
     "조선말 이후 한국인의 해외 이주. 간도·연해주·하와이·일본으로의 이주와 정착.",
     ["일제강점기"], ["사회", "역사"], [], []),
    (534, "korean-war-memory", "전쟁의 기억 — 한국인에게 6·25란 무엇인가",
     "6·25 전쟁이 한국 사회에 남긴 상처. 이산가족, 전쟁 문학, 집단 기억의 형성.",
     ["현대"], ["사회", "문화"], [], []),
    (535, "korean-economic-history", "한국 경제사 — 가난에서 선진국까지",
     "조선 말기 빈곤에서 현재까지 한국 경제의 발전. 일제 수탈·전쟁 폐허·한강의 기적.",
     ["현대"], ["경제"], [], []),
    (536, "korean-identity-history", "한국인의 정체성 — '우리'라는 감각의 역사",
     "한국인의 민족 정체성 형성 과정. 단군 신화, 삼국 통일, 일제 저항을 통한 정체성.",
     ["현대"], ["역사", "사상"], [], []),
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
    "독립운동": "independence", "일제강점": "colonial", "고고학": "archaeology",
    "사상": "philosophy", "교육": "education", "문학": "literature",
    "음악": "music", "신화": "mythology", "여성": "women", "건축": "architecture",
}
RELATED_URLS = {
    "일본": "japan", "중국": "china", "미국": "usa", "몽골": "mongol",
}
REGION_URLS = {
    "경주": "gyeongju", "서울": "seoul", "평양": "pyongyang",
    "개성": "gaeseong", "부여": "buyeo",
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
