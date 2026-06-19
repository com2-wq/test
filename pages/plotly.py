import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

# 1. 스트림릿 페이지 설정
st.set_page_config(
    page_title="글로벌 시가총액 Top 10 주식 대시보드",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 글로벌 시가총액 Top 10 주식 대시보드 (최근 1년)")
st.markdown(
    "이 대시보드는 현재 글로벌 시가총액 상위 10개 기업의 최근 1년 동안의 주가 변화 추이를 보여줍니다."
)

# 2. 글로벌 시가총액 Top 10 기업 데이터 정의 (2026년 상반기 기준 가독 지표 반영)
# 국외 기업 및 ADR 포함 대표 10개사 정보 맵핑
TOP10_COMPANIES = {
    "NVDA": "NVIDIA",
    "GOOGL": "Alphabet (Google)",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "AMZN": "Amazon",
    "TSM": "TSMC",
    "AVGO": "Broadcom",
    "TSLA": "Tesla",
    "META": "Meta Platforms",
    "WMT": "Walmart",
}

tickers = list(TOP10_COMPANIES.keys())


# 3. 데이터 로드 함수 (캐싱 처리로 속도 최적화)
@st.cache_data(ttl=3600)  # 1시간 동안 데이터 캐싱
def load_stock_data(ticker_list):
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)

    # 데이터 다운로드
    data = yf.download(ticker_list, start=start_date, end=end_date)

    # yfinance의 MultiIndex 구조에서 'Close' 가격만 추출
    if "Close" in data.columns:
        close_data = data["Close"]
    else:
        close_data = data

    return close_data


with st.spinner("야후 파이낸스에서 실시간 데이터를 가져오는 중입니다..."):
    try:
        df_close = load_stock_data(tickers)
        # 결측치 처리 (휴장일 등)
        df_close = df_close.ffill().bfill()
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        st.stop()

# 4. 사이드바 제어 요소
st.sidebar.header("⚙️ 대시보드 옵션")

# 기업 선택 멀티셀렉트
selected_tickers = st.sidebar.multiselect(
    "시각화할 기업을 선택하세요:",
    options=tickers,
    default=tickers,
    format_func=lambda x: f"{TOP10_COMPANIES[x]} ({x})",
)

# 차트 종류 선택 (실제 주가 vs 누적 수익률)
chart_type = st.sidebar.radio(
    "차트 표시 방식:", ("실제 주가 (USD)", "누적 수익률 변화 (%)")
)

# 데이터 필터링
if not selected_tickers:
    st.warning("최소 한 개 이상의 기업을 선택해주세요.")
    st.stop()

filtered_df = df_close[selected_tickers].copy()

# 5. 메인 화면 - 시각화 레이아웃
if chart_type == "실제 주가 (USD)":
    # 5-1. 실제 주가 선그래프
    fig = px.line(
        filtered_df,
        x=filtered_df.index,
        y=selected_tickers,
        labels={"value": "주가 (USD)", "Date": "날짜", "variable": "기업명"},
        title="최근 1년 주가 추이 (종가 기준)",
    )
else:
    # 5-2. 누적 수익률 계산 (시작일 기준 100% 혹은 0%부터 시작하도록 백분율 계산)
    # 첫 거래일 가격으로 나눠 수익률 계산
    normalized_df = (filtered_df / filtered_df.iloc[0] - 1) * 100

    fig = px.line(
        normalized_df,
        x=normalized_df.index,
        y=selected_tickers,
        labels={
            "value": "누적 수익률 (%)",
            "Date": "날짜",
            "variable": "기업명",
        },
        title="최근 1년 기준 누적 수익률 비교 (%)",
    )

# 플로틀리 레이아웃 깔끔하게 조정 (한국어 기업명 매핑 적용)
for trace in fig.data:
    trace.name = f"{TOP10_COMPANIES[trace.name]} ({trace.name})"

fig.update_layout(
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=60, b=20),
)

# 스트림릿에 플로틀리 차트 렌더링
st.plotly_chart(fig, use_container_width=True)

# 6. 추가 정보 테이블 레이아웃 (카드 형태로 간단한 요약 표기)
st.subheader("📊 기업별 최근 요약 정보")
cols = st.columns(4)

for i, ticker in enumerate(selected_tickers[:4]):  # 상위 4개만 샘플 메트릭 표시
    current_price = filtered_df[ticker].iloc[-1]
    prev_price = filtered_df[ticker].iloc[0]
    total_return = ((current_price / prev_price) - 1) * 100

    with cols[i % 4]:
        st.metric(
            label=TOP10_COMPANIES[ticker],
            value=f"${current_price:,.2f}",
            delta=f"{total_return:+.2f}% (1년)",
        )

st.markdown("---")
st.dataframe(filtered_df.tail(10))  # 최신 10일치 데이터 표 형태 제공
