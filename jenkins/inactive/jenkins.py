import requests
from base64 import b64encode

url = 'http://x.x.x.x:8080/job/<jenkins_job_name>/api/json'

auth_string=str.encode('<jenkins_account>:<jenins_password>')

secret = b64encode(auth_string)
print(secret)

payload={}

proxies={
'http':'10.x.x.x:8080',
'https':'10.x.x.x:8080'
}

headers = {
	'Authorization': 'Basic 44Om44O844K2OuODkeOCueODr+ODvOODiQ==',
	'User-Agent': 'PostmanRuntime/7.26.8',
	'Postman-Token': '<calculated when request is sent>',
	'Host': '<calculated when request is sent>',
	'Accept': '*/*',
	'Accept-Encoding': 'gzip, deflate, br',
	'Connection': 'keep-alive'
}

response = requests.get(url, headers=headers, proxies=proxies)
# response = requests.get(url, headers=headers)


# session = requests.Session()
# response = session.get(url, headers=headers)
print(response.status_code)
