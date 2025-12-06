import json
import os
from bs4 import BeautifulSoup

# JSON 규칙 불러오기
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "../data/ad_keywords.json"), "r", encoding="utf-8") as f:
    AD_KEYWORDS = json.load(f)

with open(os.path.join(BASE_DIR, "../data/css_remove_list.json"), "r", encoding="utf-8") as f:
    CSS_REMOVE_LIST = json.load(f)


def remove_ads_and_css(soup: BeautifulSoup) -> BeautifulSoup:
    """CSS 셀렉터 + 키워드 기반으로 광고/불필요 요소 제거"""

    # 1) CSS 셀렉터로 제거
    for selector in CSS_REMOVE_LIST.get("selectors", []):
        for tag in soup.select(selector):
            tag.decompose()

    # 2) 키워드 기반 광고 제거 (너무 공격적이지 않게 완화)
    for keyword in AD_KEYWORDS.get("keywords", []):
        # 문서 내 모든 텍스트 노드 탐색
        for text_node in soup.find_all(string=True):
            if keyword in text_node.lower():
                parent = text_node.parent
                if not parent:
                    continue

                # ✅ 본문 컨테이너는 절대 지우지 않기
                if parent.get("id") in ["dic_area", "contents"]:
                    continue

                # 그 외 요소만 제거
                parent.decompose()

    return soup
