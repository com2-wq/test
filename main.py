import streamlit as st
import random
import time

# 1. 페이지 설정 (이모지 타이틀)
st.set_page_config(
    page_title="2026 월드컵 우승 예측기 ⚽",
    page_icon="🏆",
    layout="centered"
)

# 2. 2026 월드컵 실제 조 편성 데이터
GROUPS = {
    "Group A 🇲🇽🇿🇦🇰🇷🇨🇿": ["멕시코 🇲🇽", "남아공 🇿🇦", "대한민국 🇰🇷", "체코 🇨🇿"],
    "Group B 🇨🇦🇨🇭🇶🇦🇧🇦": ["캐나다 🇨🇦", "스위스 🇨🇭", "카타르 🇶🇦", "보스니아 🇧🇦"],
    "Group C 🇧🇷🇲🇦🇭🇹🇸🇨": ["브라질 🇧🇷", "모로코 🇲🇦", "아이티 🇭🇹", "스코틀랜드 🏴󠁧󠁢󠁳󠁣󠁴󠁿"],
    "Group D 🇺🇸🇵🇾🇦🇺🇹🇷": ["미국 🇺🇸", "파라과이 🇵🇾", "호주 🇦🇺", "튀르키예 🇹🇷"],
    "Group E 🇩🇪🇨🇼🇨🇮🇪🇨": ["독일 🇩🇪", "퀴라소 🇨🇼", "코트디부아르 🇨🇮", "에콰도르 🇪🇨"],
    "Group F 🇳🇱🇯🇵🇹🇳🇸🇪": ["네덜란드 🇳🇱", "일본 🇯🇵", "튀니지 🇹🇳", "스웨덴 🇸🇪"],
    "Group G 🇧🇪🇪🇬🇮🇷🇳🇿": ["벨기에 🇧🇪", "이집트 🇪🇬", "이란 🇮🇷", "뉴질랜드 🇳🇿"],
    "Group H 🇪🇸🇨🇻🇸🇦🇺🇾": ["스페인 🇪🇸", "카보베르데 🇨🇻", "사우디아라비아 🇸🇦", "우루과이 🇺🇾"],
    "Group I 🇫🇷🇸🇳🇮🇶🇳🇴": ["프랑스 🇫🇷", "세네갈 🇸🇳", "이라크 🇮🇶", "노르웨이 🇳🇴"],
    "Group J 🇦🇷🇩🇿🇦🇹🇯🇴": ["아르헨티나 🇦🇷", "알제리 🇩🇿", "오스트리아 🇦🇹", "요르단 🇯🇴"],
    "Group K 🇵🇹🇺🇿🇨🇴🇨🇩": ["포르투갈 🇵🇹", "우즈베키스탄 🇺🇿", "콜롬비아 🇨🇴", "콩고민주공화국 🇨🇩"],
    "Group L 🏴󠁧󠁢󠁥󠁮󠁧󠁿🇭🇷🇬🇭🇵🇦": ["잉글랜드 🏴󠁧󠁢󠁥󠁮󠁧󠁿", "크로아티아 🇭🇷", "가나 🇬🇭", "파나마 🇵🇦"]
}

# 모든 팀 리스트업
ALL_TEAMS = []
for teams in GROUPS.values():
    ALL_TEAMS.extend(teams)
ALL_TEAMS = sorted(ALL_TEAMS)

# 3. 헤더 및 인트로
st.title("🏆 2026 FIFA 월드컵 우승 예측 ⚽")
st.markdown("""
    올해 펼쳐지는 **북중미 월드컵(미국·유산·멕시코 공동 개최)**의 승자는 과연 누가 될까요?  
    시뮬레이터를 통해 가상 매치와 최종 우승국을 예측해 보세요! ✨
""")
st.write("---")

# 4. 기능 1: 개별 매치 스코어 예측
st.header("🥊 1:1 빅매치 결과 예측")
st.subheader("원하는 두 팀을 골라 경기 결과를 시뮬레이션해 보세요!")

col1, col2 = st.columns(2)
with col1:
    team_a = st.selectbox("🏠 홈 팀 선택", ALL_TEAMS, index=ALL_TEAMS.index("대한민국 🇰🇷"))
with col2:
    team_b = st.selectbox("✈️ 원정 팀 선택", ALL_TEAMS, index=ALL_TEAMS.index("브라질 🇧🇷"))

if st.button("🎲 매치 시뮬레이션 시작!", key="match_btn"):
    if team_a == team_b:
        st.warning("⚠️ 서로 다른 두 팀을 선택해 주세요!")
    else:
        with st.spinner("⏳ 심판이 휘슬을 불 준비를 하고 있습니다..."):
            time.sleep(1.5)
            
        # 스코어 랜덤 생성
        score_a = random.randint(0, 4)
        score_b = random.randint(0, 4)
        
        # 결과 연출
        st.balloons()
        st.success("✨ 경기 종료! 전광판을 확인하세요!")
        
        # 전광판 스타일링
        st.markdown(f"""
        <div style="background-color:#1e1e1e; padding:20px; border-radius:10px; text-align:center; color:white;">
            <h2 style="margin:0; color:#ffcc00;">⚽ MATCH RESULT ⚽</h2>
            <div style="display:flex; justify-content:space-around; align-items:center; margin-top:20px;">
                <div><h3>{team_a}</h3></div>
                <div><h1 style="font-size:50px; color:#00ffcc;">{score_a} : {score_b}</h1></div>
                <div><h3>{team_b}</h3></div>
            </div>
        </div>
        """, unsafe_html=True)
        
        # 위트 있는 멘트 추가
        if score_a > score_b:
            st.write(f"🎉 **{team_a}**이(가) 환상적인 경기력으로 **{team_b}**을 꺾고 승리했습니다! 🥳")
        elif score_b > score_a:
            st.write(f"🎉 **{team_b}**이(가) 극적인 골을 터트리며 **{team_a}**을 상대로 승리를 거둡니다! 🥳")
        else:
            st.write(f"🤝 두 팀은 치열한 공방전 끝에 **무승부**로 경기를 마쳤습니다! 연장전으로 갈까요? 🤔")

st.write("---")

# 5. 기능 2: 2026 월드컵 전체 우승팀 원클릭 예측
st.header("🔮 슈퍼컴퓨터 우승국 원클릭 예측")
st.write("48개 진출국 중에서 슈퍼컴퓨터 알고리즘(랜덤 피킹)이 최종 우승 확률이 가장 높은 나라를 찍어줍니다!")

if st.button("👑 우승 트로피의 주인은? (클릭)", key="champion_btn"):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # 분석하는 척하는 유쾌한 애니메이션 효과
    phrases = ["📊 역대 월드컵 데이터 분석 중...", "🏃 선수들의 컨디션 체크 중...", "🌤️ 경기 당일 날씨 예측 중...", "🔮 미래 예측소 가동 중..."]
    for percent_complete in range(100):
        time.sleep(0.02)
        progress_bar.progress(percent_complete + 1)
        if percent_complete % 25 == 0:
            status_text.text(phrases[percent_complete // 25])
            
    status_text.text("🎯 분석 완료!")
    
    # 우승국 추첨
    champion = random.choice(ALL_TEAMS)
    
    # 축하 연출
    st.snow()
    
    st.markdown(f"""
    <div style="background-color:#0f2027; padding:30px; border-radius:15px; text-align:center; border: 3px solid #gold; color:white;">
        <h1 style="font-size:40px; color:#ffd700;">🥇 2026 월드컵 우승국 예측 🥇</h1>
        <br>
        <h2 style="font-size:45px; color:#ffffff; background-color:#203a43; display:inline-block; padding:10px 30px; border-radius:10px;">
            {champion}
        </h2>
        <p style="margin-top:20px; color:#a8ff78; font-size:18px;">✨ 축하합니다! 슈퍼컴퓨터가 예측한 우승의 주인공입니다! ✨</p>
    </div>
    """, unsafe_html=True)

st.write("---")

# 6. 사이드바 조 편성 안내
st.sidebar.title("📅 2026 월드컵 공식 조 편성")
st.sidebar.info("48개국이 12개 조로 나뉘어 치열한 예선을 펼칩니다.")
for group_name, teams in GROUPS.items():
    st.sidebar.markdown(f"**{group_name}**")
    for t in teams:
        st.sidebar.write(f"- {t}")
