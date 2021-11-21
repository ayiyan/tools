import requests
import json
import urllib3
from urllib.parse import unquote
import copy
import re
import time
import logging
import settings

url = settings.url
account = settings.account
headers = settings.headers
city_map = settings.city_map
output_tic_temp = settings.output_tic_temp
resp_message_map = settings.resp_message_map
train_number = settings.train_number
train_date = settings.train_date
back_train_date = settings.back_train_date
username = settings.account["username"]
rail_deviceid = settings.RAIL_DEVICEID
rail_expiration = settings.RAIL_EXPIRATION

urllib3.disable_warnings()

logging.basicConfig(
    format='%(asctime)s : %(levelname)s ==> %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Login:

    def __init__(self, sessions):
        self.session = sessions.session

        self.data = {
            "username": account["username"],
            "password": account["password"],
            "appid": "otn"
        }

        # self.secretStr = None

    def login(self):
        # [1/10]
        resp = self.session.get(url["getjs"], headers=headers, verify=False)
        assert resp.status_code == 200 and resp.cookies.get("BIGipServerotn"), "lost cookies,1"

        # [2/10]
        data = {
            "appid": ""
        }

        resp = self.session.post(url["uamtk_static"], data=data, headers=headers, verify=False)
        assert resp.status_code == 200 and \
               resp.cookies.get("BIGipServerpassport") and \
               resp.cookies.get("_passport_session"), "lost cookies,2"

        # [3/10]
        resp = self.session.get(url["getloginbanner"], headers=headers, verify=False)
        assert resp.status_code == 200 and \
               resp.cookies.get("route") and resp.cookies.get("JSESSIONID"), "lost cookies,3"

        # [4/10]
        data = {
            "appid": "otn",
            "username": username
        }
        resp = self.session.post(url["checkloginverify"], data=data, headers=headers, verify=False)
        assert resp.status_code == 200, "wrong status code,4"

        self._instert_cookie()

        # [5/10]
        resp = self.session.post(url["login"], data=self.data, headers=headers, verify=False)
        assert resp.status_code == 200 and \
               resp.cookies.get("uamtk"), "lost cookies,5"

        assert resp.json()["result_message"] == resp_message_map["result_message"], "failed to login,5"

        # [6/10]
        resp = self.session.get(url["userlogin"], headers=headers, verify=False)
        assert resp.status_code == 200 and \
               resp.cookies.get("JSESSIONID"), "lost cookies,6"

        # [7/10]
        resp = self.session.post(url["uamtk"], data=self.data, headers=headers, verify=False)
        assert resp.status_code == 200 and \
               resp.cookies.get("uamtk"), "lost cookies,7"

        # [8/10]
        data = {
            "tk": self._get_tk(resp)
        }

        resp = self.session.post(url["uamauthclient"], data=data, headers=headers, verify=False)
        assert resp.status_code == 200 and \
               resp.cookies.get("tk"), "lost cookies,8"

        # [9/10]
        resp = self.session.get(url["userlogin"], headers=headers, verify=False)
        assert resp.status_code == 200, "failed to login,9"

        # [10/10]
        resp = self.session.get(url["checkuser"], headers=headers, verify=False)
        assert resp.status_code == 200 and resp.json()["data"]["flag"] is True, "no login,10"
        logging.info("login success !!!")

    def _instert_cookie(self):
        self.session.cookies.set("RAIL_DEVICEID", rail_deviceid)
        self.session.cookies.set("RAIL_EXPIRATION", rail_expiration)

    def _get_tk(self, resp):
        return resp.json()["newapptk"]


class ConfirmPassenger:
    def __init__(self, sessions):
        self.session = sessions.session

    def query_token_from_html(self):
        data = {
            "_json_att=": ""
        }

        token_info = self.session.post(url["initdc"], data=data, headers=headers, verify=False)
        html_content = token_info.text

        submit_token = re.findall('globalRepeatSubmitToken.*', html_content)
        repeat_submit_token = submit_token[0].split("=")[1]
        self.repeat_submit_token = re.findall('\w*', repeat_submit_token)[2]

        key_check_isChange = re.findall('key_check_isChange\'\:\'.*\'\,', html_content)
        key_check_isChange = key_check_isChange[0]
        key_check_isChange = key_check_isChange.split(",")[0]
        key_check_isChange = key_check_isChange.split(":")[1]
        self.key_check_isChange = key_check_isChange.strip("'")

        leftTicketStr = re.findall('leftTicketStr\'\:\'.*\'\,', html_content)[0]
        leftTicketStr = leftTicketStr.split(",")[0]
        leftTicketStr = leftTicketStr.split(":")[1]
        self.leftTicketStr = leftTicketStr.strip("'")

    def get_passenger(self):
        data = {
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.repeat_submit_token
        }
        resp = self.session.post(url["getpassengerdtos"],
                                 data=data,
                                 headers=headers,
                                 verify=False
                                 )
        passenger = resp.json()
        pax_info = passenger["data"]["normal_passengers"][0]
        self.pax_allencstr = pax_info["allEncStr"]
        self.pax_name = pax_info["passenger_name"]
        self.pax_id_no = pax_info["passenger_id_no"]
        self.pax_mobile_no = pax_info["mobile_no"]

    def check_order_info(self):
        passengerTicketStr = "O,0,1,%s,1,%s,%s,N,%s" % (
            self.pax_name,
            self.pax_id_no,
            self.pax_mobile_no,
            self.pax_allencstr
        )

        oldPassengerStr = "%s,1,%s,1_" % (
            self.pax_name,
            self.pax_mobile_no
        )
        data = {
            "cancel_flag": "2",
            "bed_level_order_num": "000000000000000000000000000000",
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "tour_flag": "dc",
            "randCode": "",
            "whatsSelect": "1",
            "sessionId": "",
            "sig": "",
            "scene": "nc_login",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.repeat_submit_token

        }

        resp = self.session.post(url["checkOrderInfo"],
                                 data=data,
                                 headers=headers,
                                 verify=False
                                 )

    def get_queue_count(self, left_ticket):
        data = {
            "train_date": time.strftime("%a %b %d %Y 00:00:00 GMT+0800",
                                        time.strptime(train_date, "%Y-%m-%d")) + ' (中国标准时间)',
            "train_no": left_ticket.train_no,
            "stationTrainCode": train_number,
            "seatType": "O",
            "fromStationTelecode": left_ticket.from_station,
            "toStationTelecode": left_ticket.to_station,
            "leftTicket": self.leftTicketStr,
            "purpose_codes": "00",
            "train_location": "P3",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.repeat_submit_token
        }

        resp = self.session.post(url["getQueueCount"],
                                 data=data,
                                 headers=headers,
                                 verify=False
                                 )
        resp_info = resp.json()
        assert resp.status_code == 200 and \
               resp_info["status"] is True and \
               len(resp_info["messages"]) == 0, "wrong info(get_queue_count) .."

    def confirm_order(self):
        passengerTicketStr = "O,0,1,%s,1,%s,%s,N,%s" % (
            self.pax_name,
            self.pax_id_no,
            self.pax_mobile_no,
            self.pax_allencstr
        )

        oldPassengerStr = "%s,1,%s,1_" % (
            self.pax_name,
            self.pax_mobile_no
        )

        data = {
            "passengerTicketStr": passengerTicketStr,
            "oldPassengerStr": oldPassengerStr,
            "randCode": "",
            "purpose_codes": "00",
            "key_check_isChange": self.key_check_isChange,
            "leftTicketStr": self.leftTicketStr,
            "train_location": "P3",
            "choose_seats": "",
            "seatDetailType": "000",
            "is_jy": "N",
            "is_cj": "Y",
            "encryptedData": "",
            "whatsSelect": "1",
            "roomType": "00",
            "dwAll": "N",
            "_json_att": "",
            "REPEAT_SUBMIT_TOKEN": self.repeat_submit_token

        }

        resp = self.session.post(url["confirmSingleForQueue"],
                                 data=data,
                                 headers=headers,
                                 verify=False
                                 )
        if resp.status_code != 200:
            print(resp.status_code)
            print(resp.text)
            raise Exception

        logging.info("Snap Up Tickets..")


class LeftTicket:
    def __init__(self, sessions):
        self.session = sessions.session

    def query_leftticket(self):
        resp = self.session.get(url["query"], headers=headers, verify=False)

        tickets = json.loads(resp.text)["data"]["result"]
        for ticket in tickets:
            tkt_list = ticket.split("|")
            content = output_tic_temp % (
                tkt_list[0],
                tkt_list[3],
                city_map[tkt_list[6]],
                city_map[tkt_list[7]],
                tkt_list[13],
                tkt_list[8],
                tkt_list[9],
                tkt_list[-16],
                tkt_list[-17],
                tkt_list[-18],
            )

            if tkt_list[3] == train_number:
                self.secretStr = copy.deepcopy(tkt_list[0])
                self.train_date = tkt_list[13]
                self.train_no = tkt_list[2]
                self.from_station = tkt_list[6]
                self.to_station = tkt_list[7]

    def submit_order_req(self):
        secretStr = unquote(self.secretStr)

        data = {
            "secretStr": secretStr,
            "train_date": train_date,
            "back_train_date": back_train_date,
            "tour_flag": "dc",
            "purpose_codes": "ADULT",
            "query_from_station_name": city_map[self.from_station],
            "query_to_station_name": city_map[self.to_station],
            "undefine": ""
        }

        resp = self.session.post(url["submitorderrequest"],
                                 data=data,
                                 headers=headers,
                                 verify=False
                                 )
        assert resp.status_code == 200, "wrong info(submit_order_req) .."


class BuyTicket:
    def __init__(self):
        self.session = requests.session()

    def take_tic_by_train_no(self):

        try:
            Login(self).login()
            left_ticket = LeftTicket(self)
            confirm_passenger = ConfirmPassenger(self)
            left_ticket.query_leftticket()
            left_ticket.submit_order_req()
            confirm_passenger.query_token_from_html()
            confirm_passenger.get_passenger()
            confirm_passenger.check_order_info()
            confirm_passenger.get_queue_count(left_ticket)
            confirm_passenger.confirm_order()

        except Exception as exp:
            logging.error(exp)


if __name__ == "__main__":
    BuyTicket().take_tic_by_train_no()
