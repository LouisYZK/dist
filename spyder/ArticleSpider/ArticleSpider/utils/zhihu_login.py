import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re

AGENT = "user-agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
HEADER = {
    'HOST': "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": AGENT
}
SESSION = requests.session()
SESSION.cookies = cookielib.LWPCookieJar()


def zhihu_login(account, passwd):
    if re.match(r'^1\d{10}', account):
        print("using mobile phone code logging")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": "",
            "phone_num": account,
            "password": password
        }
        resp_text = SESSION.post(post_url, data=post_data, headers=HEADER)

        # SESSION.


def get_xsrf():
    resp = requests.get('https://www.zhihu.com', headers=HEADER)
    # print(resp.text)
    match_obj = re.match('.*name="_xsrf".*value="(.*?)"', resp.text)
    if match_obj:
        print(match_obj.group(1))
    return
get_xsrf()