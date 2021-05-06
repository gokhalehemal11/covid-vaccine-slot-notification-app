from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from google.oauth2 import service_account

# If modifying these scopes, delete the file token.json.
SERVICE_ACCOUNT_FILE= "keys.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

credentials= service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes= SCOPES)

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1AhtW8GNzWqyQMzLNKgZLpGGsZaDT4XEJmMH1PQgGbgw'

service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                            range="responses!A1:G4").execute()

#values = result.get('values', [])
print(result)
