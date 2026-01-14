from googleapiclient.discovery import build

from src.gmail_service import (
    get_gmail_service,
    fetch_unread_messages,
    mark_as_read,
    load_processed_ids,
    save_processed_ids
)
from src.email_parser import parse_email
from src.sheets_service import append_to_sheet


def main():
    gmail_service, creds = get_gmail_service()
    sheets_service = build('sheets', 'v4', credentials=creds)

    processed_ids = load_processed_ids()
    message_ids = fetch_unread_messages(gmail_service)

    new_ids = set()

    for msg_id in message_ids:
        if msg_id in processed_ids:
            continue

        message = gmail_service.users().messages().get(
            userId='me',
            id=msg_id,
            format='full'
        ).execute()

        values = parse_email(message)

        append_to_sheet(sheets_service, values)
        mark_as_read(gmail_service, msg_id)

        new_ids.add(msg_id)
        print(f'Processed: {msg_id}')

    if new_ids:
        processed_ids.update(new_ids)
        save_processed_ids(processed_ids)

if __name__ == '__main__':
    main()





# cd C:\Users\ASUS\Desktop\gmail-to-sheets
# python -m src.main