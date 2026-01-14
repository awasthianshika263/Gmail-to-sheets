from config import SHEET_ID, RANGE_NAME

def append_to_sheet(service, values):
    body = {'values': [values]}
    service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=RANGE_NAME,
        valueInputOption='RAW',
        insertDataOption='INSERT_ROWS',
        body=body
    ).execute()
