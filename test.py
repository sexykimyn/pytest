import os
import re
from datetime import datetime
import webbrowser

# 로그 파일 경로 설정 (리눅스에서 실행될 로그 파일 경로로 설정)
log_file_path = "/var/log/syslog"  # 예시
output_html_path = "/root/py/dnf.html"  # 변환된 HTML 파일 경로

# 로그 파일 읽기
def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.readlines()
    except FileNotFoundError:
        print(f"로그 파일을 찾을 수 없습니다: {file_path}")
        return []

# 날짜 및 시간 포맷 변경 함수
def format_datetime(log_line):
    # "Sep 6 09:06:32" 형식의 로그에서 날짜와 시간 추출
    pattern = r"([A-Za-z]{3})\s+(\d+)\s+(\d{2}):(\d{2}):(\d{2})"
    
    match = re.search(pattern, log_line)
    if match:
        month_str, day, hour, minute, second = match.groups()

        # 월 이름을 숫자로 변환
        month_map = {
            "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
            "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
        }
        month = month_map.get(month_str, 1)
        
        # 현재 연도
        year = datetime.now().year % 100  # 예: 2024년 -> 24로 출력
        log_datetime = datetime(year=year, month=month, day=int(day), hour=int(hour), minute=int(minute), second=int(second))
        
        # "24년 9월 6일" 형식
        formatted_date = log_datetime.strftime(f"%y년 {month}월 {day}일")
        
        # "오전 9시 6분 32초" 형식
        formatted_time = log_datetime.strftime("%p %I시 %M분 %S초").replace("AM", "오전").replace("PM", "오후")

        return f"{formatted_date} {formatted_time}"
    return log_line  # 날짜/시간 형식이 아닐 경우 그대로 반환

# 로그 데이터를 HTML로 변환
def convert_to_html(log_data):
    html_content = """
    <html>
    <head>
        <title>Log File</title>
        <style>
            body { font-family: Arial, sans-serif; }
            pre { background-color: #f4f4f4; padding: 10px; }
            .log-line { margin-bottom: 5px; }
        </style>
    </head>
    <body>
        <h1>Log File Contents</h1>
        <pre>
    """
    for line in log_data:
        formatted_line = format_datetime(line)
        html_content += f'<div class="log-line">{formatted_line}</div>'
    
    html_content += "</pre>\n</body>\n</html>"
    return html_content

# HTML 파일 저장
def write_html_file(html_content, output_path):
    with open(output_path, 'w') as file:
        file.write(html_content)

# HTML 파일을 웹 브라우저에서 열기
def open_in_browser(output_path):
    webbrowser.open(f'file://{output_path}')

# 메인 실행 함수
if __name__ == "__main__":
    logs = read_log_file(log_file_path)
    html_content = convert_to_html(logs)
    write_html_file(html_content, output_html_path)
    
    # 웹 브라우저로 HTML 파일 자동 실행
    open_in_browser(output_html_path)

    print(f"HTML 파일이 {output_html_path}에 저장되었습니다.")
