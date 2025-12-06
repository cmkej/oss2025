from bs4 import BeautifulSoup
from readability import Document

def extract_main_content(html: str) -> str:
    """Readability 라이브러리를 이용해 본문만 추출"""
    doc = Document(html)
    cleaned_html = doc.summary()  # HTML로 본문 추출
    return cleaned_html
