from bs4 import BeautifulSoup

def remove_empty_tags(soup: BeautifulSoup) -> BeautifulSoup:
    """내용 없는 불필요 태그 제거"""
    for tag in soup.find_all():
        # 태그 안에 텍스트가 없고, 자식 태그도 없으면 제거
        if not tag.text.strip() and not tag.find():
            tag.decompose()
    return soup
