import requests
from urllib3 import encode_multipart_formdata


class Jenkins:

    def __init__(self):
        self.proxies = {
            'http': '127.0.0.1:8080',
            'https': '127.0.0.1:8080'
        }

        self.headers_data = {
            'Authorization': 'Basic 44Om44O844K2OuODkeOCueODr+ODvOODiQ==',
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    def get_crumb_and_cookie(self):
        res = requests.get(
            'http://127.0.0.1:8080/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)',
            headers=self.headers_data,
            proxies=self.proxies,
        )

        self.cookies = res.cookies

        self.headers_data['Jenkins-Crumb'] = res.text.split(":")[1]

    def plugin_installation(self):
        url = "http://127.0.0.1:8080/pluginManager/uploadPlugin"

        payload = {}
        payload['file'] = ('jsch.hpi', open('file\\jsch.hpi', 'rb').read())
        encode_data = encode_multipart_formdata(payload)
        data = encode_data[0]

        self.headers_data['Content-Type'] = encode_data[1]

        response = requests.post(url,
                                 headers=self.headers_data,
                                 data=data,
                                 proxies=self.proxies,
                                 cookies=self.cookies)

        print(response.status_code)


jen = Jenkins()
jen.get_crumb_and_cookie()
jen.plugin_installation()
