import os
import random
import re


import time
from selenium import webdriver

from Tools.http_tools import Response
from config import headers

opt = webdriver.ChromeOptions()
opt.set_headless()
chrome = webdriver.Chrome(options=opt)
chrome.get('http://www.miitbeian.gov.cn/getVerifyCode?' + str(random.randint(0, 99)))
# print(chrome.page_source)
cookie_list = chrome.get_cookies()
print(cookie_list)
cookie = {'cookie': ''}
for item in cookie_list:
    cookie['cookie'] += item['name'] + '=' + item['value']
    cookie['cookie'] += '; '

# chrome.quit()
headers.update(cookie)
print(headers)
verifyCode_url = 'http://www.miitbeian.gov.cn/getVerifyCode?' + str(random.randint(0, 99))
url = 'http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action'
res = Response().get_response(url)
print(res.cookies.items(), res.status_code)
print(res.content)

# if not os.path.exists("verifyCode_images"):
#     os.mkdir('verifyCode_images')
# with open('verifyCode_images\\' + str(int(time.time() * 1000)) + str(random.randint(100, 999)) + '.jpeg', 'wb') as fw:
#     print(res.content)
#     fw.write(res.content)
# headers.update({'cookies': res.cookies.get_dict()})
# res = requests.get('http://www.miitbeian.gov.cn/getVerifyCode?' + str(random.randint(0, 99)), headers=headers,
#                    cookies=res.cookies)
# print(res.status_code)
