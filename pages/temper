import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as ob

# 1. 페이지 설정
st.set_page_config(page_title="서울 기후 변화 대시보드", layout="wide")

st.title("📈 진짜 지구온난화 체감 대시보드")
st.markdown("1907년부터 최근까지의 서울 일별 기온 데이터를 바탕으로 기후 변화를 시각화합니다.")

# 2. 데이터 로드 및 정제
@st.cache_data # 데이터를 매번 새로 읽지 않고 캐싱하여 속도를 높입니다.
def load_data():
    # CSV 읽기 (날짜 앞뒤 공백 제거)
    df = pd.read_csv("ta_20260619190504.csv")
    
    # 컬럼명 공백 제거 및 정리
    df.columns = [col.strip() for col in df.columns]
    
    # '날짜' 컬럼의 공백 제거 및 datetime 변환
    df['날짜'] = df['날짜'].astype(str).str.strip()
    df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
    
    # 결측치(빈 값) 제거
    df = df.dropna(subset=['날짜', '평균기온(℃)', '최저기온(℃)', '최고기온(℃)'])
    
    # 분석을 위한 연도, 월 추출
    df['연도'] = df['날짜'].dt.year
    df['월'] = df['날짜'].dt.month
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ 'ta_20260619190504.csv' 파일을 찾을 수 없습니다. 코드와 같은 폴더에 있는지 확인해 주세요.")
    st.stop()

# 3. 사이드바 - 분석 필터
st.sidebar.header("📊 분석 조건 설정")
year_range = st.sidebar.slider(
    "조회 연도 범위 선택",
    int(df['연도'].min()), int(df['연도'].max()),
    (int(df['연도'].min()), int(df['연도'].max()))
)

# 필터링된 데이터
filtered_df = df[(df['연도'] >= year_range[0]) & (df['연도'] <= year_range[1])]

# 4. 주요 지표 (Metric) 시각화
st.subheader("📌 서울 기후 데이터 요약")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("역대 최고 기온", f"{df['최고기온(℃)'].max()} ℃", 
              f"{df.loc[df['최고기온(℃)'].idxmax(), '날짜'].strftime('%Y-%m-%d')}")
with col2:
    st.metric("역대 최저 기온", f"{df['최저기온(℃)'].min()} ℃", 
              f"{df.loc[df['최저기온(℃)'].idxmin(), '날짜'].strftime('%Y-%m-%d')}")
with col3:
    st.metric("총 데이터 일수", f"{len(filtered_df):,} 일")
with col4:
    st.metric("선택 기간 평균 기온", f"{filtered_df['평균기온(℃)'].mean():.2f} ℃")

st.markdown("---")

# 5. 시각화 그래프 1: 연도별 평균 기온 추세 (지구온난화 지표)
st.subheader("🌡️ 연도별 연평균 기온 변화 추이")
annual_mean = filtered_df.groupby('연도')['평균기온(℃)'].mean().reset_index()

fig_trend = px.line(
    annual_mean, x='연도', y='평균기온(℃)',
    title="연도별 평균 기온 추세선 (지구온난화 경향성 확인)",
    labels={'평균기온(℃)': '연평균 기온 (℃)'},
    template="plotly_dark"
)
# 추세선(경향선) 추가
fig_trend.add_trending_line = True 
st.plotly_chart(fig_trend, use_container_width=True)

# 6. 시각화 그래프 2: 역대 가장 무더웠던 날 TOP 10 / 가장 추웠던 날 TOP 10
st.subheader("🔥/❄️ 서울 역대 가장 극단적이었던 날 TOP 10")
tab1, tab2 = st.tabs(["🥵 가장 더웠던 날 TOP 10", "🥶 가장 추웠던 날 TOP 10"])

with tab1:
    top_hot = df.sort_values(by='최고기온(℃)', ascending=False).head(10)
    top_hot['날짜'] = top_hot['날짜'].dt.strftime('%Y-%m-%d')
    fig_hot = px.bar(
        top_hot, x='최고기온(℃)', y='날짜', orientation='h',
        color='최고기온(℃)', color_continuous_scale='Reds',
        title="서울 최고 기온 순위"
    )
    fig_hot.update_yaxis(categoryorder='total ascending')
    st.plotly_chart(fig_hot, use_container_width=True)

with tab2:
    top_cold = df.sort_values(by='최저기온(℃)', ascending=True).head(10)
    top_cold['날짜'] = top_cold['날짜'].dt.strftime('%Y-%m-%d')
    fig_cold = px.bar(
        top_cold, x='최저기온(℃)', y='날짜', orientation='h',
        color='최저기온(℃)', color_continuous_scale='Blues_r',
        title="서울 최저 기온 순위"
    )
    fig_cold.update_yaxis(categoryorder='total descending')
    st.plotly_chart(fig_cold, use_container_width=True)

# 7. 데이터 프레임 확인
if st.checkbox("원본 데이터 분석 테이블 보기"):
    st.dataframe(filtered_df, use_container_width=True)
