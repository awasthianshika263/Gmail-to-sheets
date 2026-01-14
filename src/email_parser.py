import base64
from datetime import datetime

def parse_email(message):
    payload = message['payload']
    headers = payload.get('headers', [])

    def get_header(name):
        return next((h['value'] for h in headers if h['name'] == name), '')

    from_email = get_header('From')
    subject = get_header('Subject') or '(No Subject)'
    date_raw = get_header('Date')

    # Date parsing (safe fallback)
    try:
        date_clean = date_raw.split('(')[0].strip()
        date = datetime.strptime(date_clean, '%a, %d %b %Y %H:%M:%S %z')
        date_formatted = date.strftime('%Y-%m-%d %H:%M:%S')
    except:
        date_formatted = date_raw

    body = ''
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and 'data' in part['body']:
                body = base64.urlsafe_b64decode(
                    part['body']['data']
                ).decode('utf-8', errors='ignore')
                break
    elif 'data' in payload.get('body', {}):
        body = base64.urlsafe_b64decode(
            payload['body']['data']
        ).decode('utf-8', errors='ignore')

    return [from_email, subject, date_formatted, body]
