from googleapiclient.discovery import build
from google.oauth2 import service_account
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import gspread

# If modifying these scopes, delete the file token.json.
SERVICE_ACCOUNT_FILE= "keys.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

#credentials= None
#credentials= service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes= SCOPES)

# The ID and range of a sample spreadsheet.
#SPREADSHEET_ID = '1AhtW8GNzWqyQMzLNKgZLpGGsZaDT4XEJmMH1PQgGbgw'

#service = build('sheets', 'v4', credentials=credentials)

# Call the Sheets API
#sheet = service.spreadsheets()
#result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
#                            range="responses!A1:G4").execute()

#values = result.get('values', [])
# add credentials to the account
creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, SCOPES)

# authorize the clientsheet 
client = gspread.authorize(creds)

# get the instance of the Spreadsheet
sheet = client.open('VaccineSlotApp')

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# get all the records of the data
records_data = sheet_instance.get_all_records()

# view the data

print(records_data)
