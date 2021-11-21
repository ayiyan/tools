url = {
    "getjs": "https://kyfw.12306.cn/otn/HttpZF/GetJS",
    "uamtk_static": "https://kyfw.12306.cn/passport/web/auth/uamtk-static",
    "getloginbanner": "https://kyfw.12306.cn/otn/index12306/getLoginBanner",
    "checkloginverify": "https://kyfw.12306.cn/passport/web/checkLoginVerify",
    "login": "https://kyfw.12306.cn/passport/web/login",
    "userlogin": "https://kyfw.12306.cn/otn/login/userLogin",
    # "query_tic_url": "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2021-11-29&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT",
    "query": "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2021-11-29&leftTicketDTO.from_station=BJP&leftTicketDTO.to_station=SHH&purpose_codes=ADULT",
    "getpassengerdtos": "https://kyfw.12306.cn/otn/confirmPassenger/getPassengerDTOs",
    "initdc": "https://kyfw.12306.cn/otn/confirmPassenger/initDc",
    "submitorderrequest": "https://kyfw.12306.cn/otn/leftTicket/submitOrderRequest",
    "checkuser": "https://kyfw.12306.cn/otn/login/checkUser",
    "uamtk":"https://kyfw.12306.cn/passport/web/auth/uamtk",
    "uamauthclient":"https://kyfw.12306.cn/otn/uamauthclient",
    "confirmSingleForQueue":"https://kyfw.12306.cn/otn/confirmPassenger/confirmSingleForQueue",
    "checkOrderInfo":"https://kyfw.12306.cn/otn/confirmPassenger/checkOrderInfo",
    "getQueueCount":"https://kyfw.12306.cn/otn/confirmPassenger/getQueueCount"
}



headers = {
    "Host": "kyfw.12306.cn",
    "X-Requested-With": "XMLHttpRequest",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
    "Referer": "https://kyfw.12306.cn/otn/passport?redirect=/otn/"
}

city_map = {
    "SHH": "上海",
    "VNP": "北京南",
    "BJP": "北京",
    "AOH": "上海虹桥",
    "SNH": "上海南",
    "FCP": "滨海北",
    "TJP": "天津",
    "TIP": "天津南",
    "TXP": "天津西",
    "SBT": "沈阳北",
    "SOT": "沈阳南",
    "SYT": "沈阳",
}

output_tic_temp = "预定号: %s \n" \
                  "车次: %s \n" \
                  "起始站: %s \n" \
                  "终点站: %s \n" \
                  "出发时间: %s - %s \n" \
                  "到站时间: %s \n" \
                  "商务座: %s \n" \
                  "一等座: %s \n" \
                  "二等座: %s \n"

resp_message_map = {
    "result_message":"登录成功"
}

from_station = "VNP"
to_station = "SHH"
train_date = "2021-11-29"
back_train_date = ""
train_number = "G27"

############################

RAIL_DEVICEID = "<RAIL_DEVICEID>"
RAIL_EXPIRATION = "<RAIL_EXPIRATION>"

account = {
    "username": "<username>",
    "password": "<password>",
}
############################