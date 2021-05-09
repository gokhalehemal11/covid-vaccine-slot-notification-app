# importing the required libraries
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from datetime import datetime
import random
import json

def sendMailToCorrespondingUsers(Data, result):
	print("Mail: ", Data)
	print("Message: ", result)

def switchHeader():
	headersList= [
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
			'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
			]

	return random.choice(headersList)

def switchLanguage():
	langList= ['en-US', 'hi-IN']
	return random.choice(langList)

def setuAPIReq(URL, PARAMS, peopleData, age_limit, HEADERS= {}):

	AvlfFlag= False
	resData= dict()

	r = requests.get(URL, headers= HEADERS, params= PARAMS, timeout=5)
	if r.status_code == 200:
		responseData= r.json()
		#print("Response Data", responseData)
		if len(responseData['centers']) > 0:
			for center in responseData['centers']:
				for session in center['sessions']:
					if session['available_capacity'] == 0:
						continue
					if age_limit != 0:
						if session['min_age_limit'] != age_limit:
							continue
						resData['vaccine']= session['vaccine']
						resData['center']= center['name']
						resData['nearest_date']= session['date']
						AvlfFlag= True
					else:
						resData['vaccine']= session['vaccine']
						resData['center']= center['name']
						resData['nearest_date']= session['date']
						AvlfFlag= True

		if AvlfFlag:
			sendMailToCorrespondingUsers(list(set(peopleData)), resData)

	else:
		HEADERS = {
    	'User-Agent': switchHeader(),
		'accept-Language': switchLanguage(),
		'content': 'application/json'
		}
		setuAPIReq(URL, PARAMS, peopleData, age_limit, HEADERS)

def GetDataFromGoogleSheets():
	# define the scope
	scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

	# add credentials to the account
	creds = ServiceAccountCredentials.from_json_keyfile_name('keys.json', scope)

	# authorize the clientsheet 
	client = gspread.authorize(creds)

	# get the instance of the Spreadsheet
	sheet = client.open('VaccineSlotApp')

	# get the first sheet of the Spreadsheet
	sheet_instance = sheet.get_worksheet(0)

	# get all the records of the data
	records_data = sheet_instance.get_all_records()

	# view the data
	print("All records", records_data)
	print()

	sort_by_pincode= dict()
	sort_by_district= dict()
	sort_by_agelimit= dict()
	for record in records_data:
		if record['District'] != '':
			if record['District'] not in sort_by_district:
				sort_by_district[record['District']]= [record]
			else:
				sort_by_district[record['District']].append(record)

		if record['Pincode'] != '':
			if record['Pincode'] not in sort_by_pincode:
				sort_by_pincode[record['Pincode']]= [record]
			else:
				sort_by_pincode[record['Pincode']].append(record)

		if record['AgeLimit'] not in sort_by_agelimit:
			sort_by_agelimit[record['AgeLimit']]= [record]
		else:
			sort_by_agelimit[record['AgeLimit']].append(record)

	return [sort_by_district, sort_by_pincode, sort_by_agelimit]

def GetDataFromSetuAPI():
	# Get today's date
	today_date= datetime.today().strftime('%d-%m-%Y')

	sort_by_district, sort_by_pincode, sort_by_agelimit= GetDataFromGoogleSheets()

	ageset45 = list()
	ageset18 = list()
	agesetall = list()
	
	print(sort_by_agelimit)
	print()
	if 45 in sort_by_agelimit:
		ageset45= sort_by_agelimit[45]
	if 18 in sort_by_agelimit:
		ageset18= sort_by_agelimit[18]
	if 0 in sort_by_agelimit:		
		agesetall= sort_by_agelimit[0]

	for pincode in sort_by_pincode.keys():

		peopleDataSet= sort_by_pincode[pincode]

		PARAMS= {'pincode': pincode, 'date': today_date}
		URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"

		print("Pincode "+str(pincode)+" API Call: ")

		pdata45= [i['Email'] for i in ageset45 for j in peopleDataSet if i['Pincode']==j['Pincode']]
		pdata18= [i['Email'] for i in ageset18 for j in peopleDataSet if i['Pincode']==j['Pincode']]
		pdataall= [i['Email'] for i in agesetall for j in peopleDataSet if i['Pincode']==j['Pincode']]

		if len(pdata45) > 0:
			setuAPIReq(URL, PARAMS, pdata45, 45)
		if len(pdata18) > 0:
			setuAPIReq(URL, PARAMS, pdata18, 18)
		if len(pdataall) > 0:
			setuAPIReq(URL, PARAMS, pdataall, 0)
		print()

	for district_id in sort_by_district:

		peopleDataSet= sort_by_district[district_id]

		PARAMS= {'district_id': district_id, 'date': today_date}
		URL= "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"

		print("District "+str(district_id)+" API Call: ")

		pdata45= [i['Email'] for i in ageset45 for j in peopleDataSet if i['District']==j['District']]
		pdata18= [i['Email'] for i in ageset18 for j in peopleDataSet if i['District']==j['District']]
		pdataall= [i['Email'] for i in agesetall for j in peopleDataSet if i['District']==j['District']]

		if len(pdata45) > 0:
			setuAPIReq(URL, PARAMS, pdata45, 45)
		if len(pdata18) > 0:
			setuAPIReq(URL, PARAMS, pdata18, 18)
		if len(pdataall) > 0:
			setuAPIReq(URL, PARAMS, pdataall, 0)
		print()


if __name__ == '__main__':
	GetDataFromSetuAPI()