import requests

def fetch_html(url: str) -> str:
    """
    사용자가 입력한 URL에서 HTML(웹페이지 소스코드)을 가져오는 함수.
    문제가 생기면 None을 반환합니다.
    """

    try:
        # 웹사이트에 요청 보낼 때, 우리가 '봇'이 아니라 '사람'처럼 보이게 하는 코드
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        # 요청 보내기
        response = requests.get(url, headers=headers, timeout=10)

        # 정상적으로 받아오지 못한 경우
        if response.status_code != 200:
            print(f"[fetch_html] 상태코드 오류: {response.status_code}")
            return None

        # HTML 텍스트 반환
        return response.text

    except Exception as e:
        print(f"[fetch_html] 오류 발생: {e}")
        return None
