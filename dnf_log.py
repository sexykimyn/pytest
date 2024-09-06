import os
import re
from datetime import datetime
import webbrowser
from collections import deque
import sys

# 로그 파일 경로 설정 (리눅스에서 실행될 로그 파일 경로로 설정)
log_file_path = "/var/log/dnf.log"  # 예시
output_html_path = "/root/py/pytest/dnf_log.html"  # 변환된 HTML 파일 경로

# 날짜 및 시간 형식 변경 함수
def format_datetime(dt):
    year = dt.strftime("%y년")
    month = dt.strftime("%m월").lstrip("0")
    day = dt.strftime("%d일").lstrip("0")
    
    hour = dt.hour
    am_pm = "오전" if hour < 12 else "오후"
    if hour > 12:
        hour -= 12
    elif hour == 0:
        hour = 12
    
    formatted_date = f"{year} {month} {day}"
    formatted_time = f"{am_pm} {hour}시 {dt.minute:02d}분 {dt.second:02d}초"
    
    return formatted_date, formatted_time

# 로그 파일 읽기 및 파싱
def parse_log_file(file_path, num_lines=100):
    pattern = r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{4}) (\w+) (.+)"
    parsed_logs = deque(maxlen=num_lines)
    try:
        with open(file_path, "r") as file:
            for line in file:
                match = re.match(pattern, line)
                if match:
                    timestamp_str, log_level, message = match.groups()
                    timestamp = datetime.strptime(
                        timestamp_str[:-5], "%Y-%m-%dT%H:%M:%S"
                    )
                    formatted_date, formatted_time = format_datetime(timestamp)
                    parsed_logs.append(
                        {
                            "date": formatted_date,
                            "time": formatted_time,
                            "log_level": log_level,
                            "message": message.strip(),
                        }
                    )
    except FileNotFoundError:
        print(f"오류: '{file_path}' 파일을 찾을 수 없습니다.")
        sys.exit(1)
    except PermissionError:
        print(f"오류: '{file_path}' 파일을 읽을 권한이 없습니다.")
        sys.exit(1)
    except Exception as e:
        print(f"오류 발생: {str(e)}")
        sys.exit(1)
    return list(parsed_logs)

# 로그 데이터를 HTML로 변환
def convert_to_html(parsed_logs):
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>로그 파서 결과</title>
        <style>
            body { font-family: Arial, sans-serif; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            /* 날짜 및 시간 열의 고정 너비 설정 및 줄바꿈 방지 */
            .datetime-col { 
                white-space: nowrap;  /* 자동 줄바꿈 방지 */
                width: 250px;         /* 열 너비 고정 */
            }
        </style>
    </head>
    <body>
        <h1>파싱된 로그</h1>
        <table>
            <tr>
                <th class="datetime-col">날짜 및 시간</th>
                <th>로그 레벨</th>
                <th>메시지</th>
            </tr>
    """
    # 날짜와 시간을 하나로 합쳐서 가로로 출력
    for log in parsed_logs:
        datetime_combined = f"{log['date']} {log['time']}"
        html_content += f"""
            <tr>
                <td class="datetime-col">{datetime_combined}</td>
                <td>{log['log_level']}</td>
                <td>{log['message']}</td>
            </tr>
        """
    html_content += """
        </table>
    </body>
    </html>
    """
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
    # 로그 파싱
    logs = parse_log_file(log_file_path)
    
    # 로그 데이터 확인 (디버깅용)
    print(f"파싱된 로그 {len(logs)}줄")
    for log in logs[:5]:  # 일부 로그만 출력해서 확인
        print(log)
    
    # HTML 변환 및 저장
    html_content = convert_to_html(logs)
    write_html_file(html_content, output_html_path)
    
    # 웹 브라우저로 HTML 파일 자동 실행
    open_in_browser(output_html_path)
    print(f"HTML 파일이 {output_html_path}에 저장되었습니다.")
