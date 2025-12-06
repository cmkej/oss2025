# Web Cleaner

## 프로젝트 개요
Web Cleaner는 웹페이지에서 광고·불필요한 UI 요소를 제거하고, 핵심 본문만 깔끔하게 추출하여 보여주는 프로그램입니다. URL을 입력하면 HTML 구조를 분석해 본문을 추출하고, 이미지 표시 여부·크기 조절, 글자 크기 조절, 핵심 요약 기능을 제공합니다. 뉴스 기사 · 블로그 글 · 텍스트 분석용 데이터 등 다양한 웹 콘텐츠를 가독성 높은 형태로 변환할 수 있습니다.



## 실행 방법

### 1. 패키지 설치
```
pip install streamlit
pip install beautifulsoup4
pip install requests
pip install lxml
pip install numpy
```

### 2. 프로젝트 구조
GitHub 저장소의 파일을 다운로드하여 다음과 같은 구조로 맞춥니다:
```
project/
│── app.py
├── cleanser/
│   ├── __init__.py
│   ├── fetcher.py
│   ├── cleaner.py
│   ├── summarizer.py
│   ├── parser.py
│   ├── ad_filter.py
│   ├── readability_utils.py
│   ├── utils.py
│   │
│   └── data/
│       ├── ad_keywords.json
└────── └── css_remove_list.json
```

### 3. 실행
터미널에서 다음 명령어 입력:
```
streamlit run app.py
```

### 4. 웹 브라우저 접속
```
http://localhost:8501/
```



## 예시 URL
네이버 뉴스:
https://n.news.naver.com/article/008/0005288155?cds=news_media_pc&type=editn

ZDNET Korea:
https://zdnet.co.kr/view/?no=20251205152520

중앙일보:
https://www.joongang.co.kr/article/25387888



## 결과 화면
<img width="2849" height="1468" alt="스크린샷 2025-12-06 112100" src="https://github.com/user-attachments/assets/2c7ae78e-ee8b-4f3f-bf24-09796a319939" />

### 실행 화면
<img width="2616" height="1402" alt="image" src="https://github.com/user-attachments/assets/15b69dce-1dcf-46e6-881a-0ceee1f7b1da" />
<img width="2616" height="1402" alt="image" src="https://github.com/user-attachments/assets/a1ff9048-cfb1-4c9b-a69d-3ade48275f5c" />
<img width="2616" height="1402" alt="image" src="https://github.com/user-attachments/assets/2540ad32-515a-47ef-93b4-967b846a468b" />



## Web Cleaner 기능

### 본문 추출 기능
- HTML 구조에서 광고 · 배너 · 불필요한 태그를 제거
- 핵심 텍스트만 추출하여 깔끔하게 렌더링

### 이미지 표시 옵션
- 이미지 포함/비포함 선택
- 이미지 크기를 슬라이더로 조절 가능

### 본문 글자 크기 조절
- 사용자가 원하는 가독성에 맞게 px 단위로 조절

### 핵심 내용 요약 기능
- 문단 기반 분석 + TextRank 알고리즘 조합
- 핵심 2~3문장을 자동으로 추출



## 주요 함수 설명

### `fetch_html(url)`
- URL에서 HTML 소스를 가져오는 함수  

### `clean_html(html)`
- 광고 및 불필요한 요소 제거 후 정제된 HTML 본문과 이미지 리스트를 반환

### `extract_title(html)`
기사나 블로그 문서에서 제목을 자동으로 탐색하여 최적의 제목을 선택

### `summarize_text(text)`
- 문단 기반 분석 + TextRank 알고리즘을 이용한 핵심 문장 요약 기능을 이용하여 3문장 내외의 자연스러운 요약 생성

### Streamlit 렌더링 
- `st.session_state`를 활용 
  - 본문 추출 후 옵션 변경 시 즉시 UI 갱신  
  - 재추출 없이 이미지 크기, 글자 크기, 요약 여부 등이 바로 반영됨



## 참고 자료

+ **웹 프레임워크:** Streamlit  
+ **HTML 파싱:** BeautifulSoup4  
+ **HTTP 요청:** Requests  
+ **HTML 렌더링 엔진:** lxml  
+ **텍스트 분석 및 벡터 계산:** NumPy  

---

## 📄 라이센스
MIT License  
