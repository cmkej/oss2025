from bs4 import BeautifulSoup
from .ad_filter import remove_ads_and_css
from .parser import remove_empty_tags
from .readability_utils import extract_main_content


# -----------------------------
# 공통 유틸 함수들
# -----------------------------
def extract_images_from_area(area):
    """본문 영역 안의 이미지 URL 추출 (lazy-loading 대응)"""
    imgs = []
    if area is None:
        return imgs

    for img in area.find_all("img"):
        src = None

        # 1) lazy-loading: data-src
        if img.get("data-src"):
            src = img["data-src"]
        # 2) data-lazy-src
        elif img.get("data-lazy-src"):
            src = img["data-lazy-src"]
        # 3) 일반 src
        elif img.get("src") and img["src"].startswith("http"):
            src = img["src"]

        if src and src.startswith("http"):
            imgs.append(src)

    return imgs


def _paragraphize(area):
    """주어진 영역에서 문단(<p>) 기준으로 HTML 다시 구성"""
    if area is None:
        return ""

    paragraphs = []

    # 1) p 태그가 있으면 p 기반 문단
    ps = area.find_all("p")
    if ps:
        for p in ps:
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(
                    f"<p style='margin-bottom:1.2em; line-height:1.7;'>{text}</p>"
                )
        if paragraphs:
            return "\n".join(paragraphs)

    # 2) p가 거의 없으면 줄바꿈(\n) 기준으로 문단 나누기
    raw_text = area.get_text("\n", strip=True)
    for block in raw_text.split("\n"):
        block = block.strip()
        if block:
            paragraphs.append(
                f"<p style='margin-bottom:1.2em; line-height:1.7;'>{block}</p>"
            )

    return "\n".join(paragraphs)


def _detect_domain(soup):
    """og:url 또는 canonical로 도메인 추출"""
    url = ""

    og = soup.find("meta", property="og:url")
    if og and og.get("content"):
        url = og["content"]

    if not url:
        link = soup.find("link", rel="canonical")
        if link and link.get("href"):
            url = link["href"]

    if "chosun.com" in url:
        return "chosun"
    if "joongang.co.kr" in url:
        return "joongang"
    if "donga.com" in url:
        return "donga"
    if "hankyung.com" in url:
        return "hankyung"
    if "mk.co.kr" in url or "maekyung.com" in url:
        return "maekyung"

    return ""


# -----------------------------
# 사이트별 전용 파서
# -----------------------------
def _parse_naver(soup):
    """네이버 뉴스 전용 파서 (dic_area + 이미지)"""
    area = soup.find(id="dic_area")
    if not area:
        return None

    # 1) 이미지 먼저 추출 (나중에 태그 지워도 이미지 URL은 남김)
    images = extract_images_from_area(area)

    # 2) 광고/불필요 요소 제거
    area = remove_ads_and_css(area)
    area = remove_empty_tags(area)

    html = _paragraphize(area)
    return html, images


def _parse_chosun(soup):
    """조선일보 전용 파서"""
    # 후보 컨테이너들 중 첫 번째로 발견되는 것 사용
    candidates = [
        "div.article-body",
        "div#news_body",
        "div[itemprop='articleBody']",
        "section.article-body",
    ]
    area = None
    for sel in candidates:
        area = soup.select_one(sel)
        if area:
            break

    if not area:
        return None

    images = extract_images_from_area(area)
    area = remove_ads_and_css(area)
    area = remove_empty_tags(area)
    html = _paragraphize(area)
    return html, images


def _parse_joongang(soup):
    """중앙일보 전용 파서"""
    candidates = [
        "div#article_body",
        "div.article_body",
        "div#story_body",
        "div[itemprop='articleBody']",
    ]
    area = None
    for sel in candidates:
        area = soup.select_one(sel)
        if area:
            break

    if not area:
        return None

    images = extract_images_from_area(area)
    area = remove_ads_and_css(area)
    area = remove_empty_tags(area)
    html = _paragraphize(area)
    return html, images


def _parse_donga(soup):
    """동아일보 전용 파서"""
    candidates = [
        "div.article_txt",
        "div#content",
        "div.article_body",
        "div#news_body",
    ]
    area = None
    for sel in candidates:
        area = soup.select_one(sel)
        if area:
            break

    if not area:
        return None

    images = extract_images_from_area(area)
    area = remove_ads_and_css(area)
    area = remove_empty_tags(area)
    html = _paragraphize(area)
    return html, images


def _parse_hankyung(soup):
    """한국경제 전용 파서"""
    candidates = [
        "div#articletxt",
        "div.article-body",
        "div#newsView",
        "div[itemprop='articleBody']",
    ]
    area = None
    for sel in candidates:
        area = soup.select_one(sel)
        if area:
            break

    if not area:
        return None

    images = extract_images_from_area(area)
    area = remove_ads_and_css(area)
    area = remove_empty_tags(area)
    html = _paragraphize(area)
    return html, images


def _parse_maekyung(soup):
    """매일경제 전용 파서"""
    candidates = [
        "div#article_content",
        "div.art_txt",
        "div#article_body",
        "section#article",
    ]
    area = None
    for sel in candidates:
        area = soup.select_one(sel)
        if area:
            break

    if not area:
        return None

    images = extract_images_from_area(area)
    area = remove_ads_and_css(area)
    area = remove_empty_tags(area)
    html = _paragraphize(area)
    return html, images


def _parse_general(html: str):
    """그 외 일반 사이트용 파서 (Readability 사용)"""
    main_html = extract_main_content(html)
    soup = BeautifulSoup(main_html, "lxml")

    images = extract_images_from_area(soup)
    soup = remove_ads_and_css(soup)
    soup = remove_empty_tags(soup)
    html_out = _paragraphize(soup)
    return html_out, images


# -----------------------------
# 외부에서 사용하는 메인 함수
# -----------------------------
def clean_html(html: str):
    """
    HTML 전체를 받아서
    - 네이버 / 조선 / 중앙 / 동아 / 한경 / 매경 전용 처리
    - 그 외는 일반(Readability) 처리
    결과: (정제된 HTML, 이미지 URL 리스트)
    """
    soup = BeautifulSoup(html, "lxml")

    # 1) 네이버 뉴스는 dic_area로 바로 감지
    parsed = _parse_naver(soup)
    if parsed:
        return parsed

    # 2) 도메인 기반으로 한국 언론사 감지
    domain = _detect_domain(soup)

    if domain == "chosun":
        parsed = _parse_chosun(soup)
        if parsed:
            return parsed

    if domain == "joongang":
        parsed = _parse_joongang(soup)
        if parsed:
            return parsed

    if domain == "donga":
        parsed = _parse_donga(soup)
        if parsed:
            return parsed

    if domain == "hankyung":
        parsed = _parse_hankyung(soup)
        if parsed:
            return parsed

    if domain == "maekyung":
        parsed = _parse_maekyung(soup)
        if parsed:
            return parsed

    # 3) 그 외 사이트는 일반 처리
    return _parse_general(html)
