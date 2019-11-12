import requests, time, logging
from datetime import datetime
import openpyxl

def domainion():

	logging.basicConfig(filename = 'LOG_NAME_GOES_HERE.log',
	                format = '%(name)s - %(levelname)s - %(message)s',
	                level=logging.INFO)

	login_url = "URL_FOR_LOGIN_GOES_HERE"
	ping_url = "URL_TO_PING_INSIDE_LOGIN"
	worst_time = 0
	file = 'EXCEL_EXPORT.xlsx'
	wb = openpyxl.load_workbook(filename=file)
	ws = wb['Sheet1']

	while True:
		client = requests.session()

		# Retrieve the CSRF token first
		client.get(ping_url)  # sets cookie
		csrftoken = client.cookies['csrftoken']
		login_data = dict(username="USERNAME", password="PASSWORD",
		 								csrfmiddlewaretoken=csrftoken, next='/')
		post = client.post(login_url, data=login_data, headers=dict(Referer=login_url))
		r = client.get(ping_url)
		print(r.status_code)
		timer = r.elapsed.total_seconds()
		print(timer)
		print(r.url)
		if worst_time < timer:
			print("\n")
			worst_time = timer

		logging.info("{} --- The page {} took {} seconds to load with Status code {}.".format(
			datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ping_url, timer, r.status_code))

		new_row = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ping_url, timer, r.status_code]
		ws.append(new_row)
		wb.save(file)
		time.sleep(300)
		print(f"Worst time is {worst_time}\n")

domainion()