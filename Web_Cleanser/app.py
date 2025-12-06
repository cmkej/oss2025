import streamlit as st
from bs4 import BeautifulSoup
from cleanser.fetcher import fetch_html
from cleanser.cleaner import clean_html
from cleanser.summarizer import summarize_text

st.set_page_config(page_title="Web Cleaner", layout="wide")

# --------------------------------
# 사이드바 옵션
# --------------------------------
st.sidebar.header("⚙️ 옵션 설정")

include_images = st.sidebar.checkbox("이미지 포함", True)
enable_summary = st.sidebar.checkbox("핵심 내용 포함", False)

image_width_percent = st.sidebar.slider("이미지 크기 (너비 %)", 30, 100, 90)
font_size = st.sidebar.slider("본문 글자 크기 (px)", 13, 22, 16)

st.sidebar.write("---")


# --------------------------------
# 메인 제목 (왼쪽 정렬)
# --------------------------------
st.markdown(
    "<h1 style='text-align:left; margin-top:10px;'>🧹 Web Cleaner</h1>",
    unsafe_allow_html=True
)


# --------------------------------
# URL 입력
# --------------------------------
url = st.text_input("URL을 입력하세요:")


# --------------------------------
# 제목 추출 함수
# --------------------------------
def extract_title(html):
    soup = BeautifulSoup(html, "lxml")

    naver_title = soup.find(class_="media_end_head_headline")
    if naver_title:
        return naver_title.get_text(strip=True)

    h1 = soup.find("h1")
    if h1:
        return h1.get_text(strip=True)

    if soup.title and soup.title.text:
        return soup.title.text.strip()

    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"]

    return "제목을 찾지 못했습니다"


# --------------------------------
# 본문 추출 버튼
# --------------------------------
if st.button("본문 추출하기"):
    if not url:
        st.warning("URL을 입력해주세요.")
    else:
        try:
            with st.spinner("본문을 추출하는 중입니다..."):
                html = fetch_html(url)
                title = extract_title(html)
                cleaned_html, images = clean_html(html)

            # 세션 저장 (옵션 변경에 따라 재렌더링)
            st.session_state["title"] = title
            st.session_state["cleaned_html"] = cleaned_html
            st.session_state["images"] = images

        except Exception as e:
            st.error(f"오류 발생: {e}")


# --------------------------------
# 세션에 본문 데이터가 있을 때 렌더링
# --------------------------------
if "cleaned_html" in st.session_state:

    title = st.session_state["title"]
    cleaned_html = st.session_state["cleaned_html"]
    images = st.session_state["images"]

    # --------------------------------
    # 기사 제목 (왼쪽 정렬)
    # --------------------------------
    st.markdown(
        f"<h1 style='text-align:left; margin-top:25px; font-size:1.9em;'>{title}</h1>",
        unsafe_allow_html=True
    )

    st.write("---")

    # --------------------------------
    # 이미지 출력 (왼쪽 정렬)
    # --------------------------------
    if include_images and images:
        for src in images:
            img_width = int(8 * image_width_percent)

            st.markdown(
                f"""
                <div style='text-align:left; margin: 15px 0;'>
                    <img src="{src}" width="{img_width}px">
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("---")

    # --------------------------------
    # 본문 출력 (왼쪽 정렬)
    # --------------------------------
    st.markdown(
        f"""
        <div style='text-align:left;'>
            <div style='font-size:{font_size}px; line-height:1.6; max-width:750px;'>
                {cleaned_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------
    # 요약 출력 → "핵심 내용" (왼쪽 정렬)
    # --------------------------------
    if enable_summary:
        st.write("---")
        st.subheader("핵심 내용")

        summary_result = summarize_text(cleaned_html, summary_count=3)

        st.markdown(
            f"""
            <div style='text-align:left;'>
                <div style='font-size:{font_size}px; line-height:1.6; max-width:750px;'>
                    {summary_result}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
