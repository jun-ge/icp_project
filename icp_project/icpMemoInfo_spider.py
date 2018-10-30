import logging
import os
import re
import execjs
import requests

from Tools.http_tools import get_page_from_selenium
from config import form_data, headers


def get_company_name(path):
    company_list = []
    return company_list


if __name__ == '__main__':
    # if not os.path.exists("./log"):
    #     os.makedirs("./log")
    # logging.basicConfig(level=logging.INFO,
    #                     filemode="a",
    #                     filename="icpMemoinfo_spider.log",
    #                     format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s', )
    path = ''
    for company in get_company_name(path):

        url = "http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action"
        headers.update(
            cookie='__jsluid=8aa5f50566e370896d4972183d1c90ed; td_cookie=18446744070730666215; __jsl_clearance=1540455555.438|0|ntK0eKIuyWC3Z2k4i6%2F%2FzrAKI7E%3D; JSESSIONID=SP-qU2q5IkDY2gXOPB6Km6fugBmo2Lxl8k8lzZknlprcINUG08kk!-1376340174')
        print(headers)
        res = requests.get(url, headers=headers)
        form_data.update({'unitName': company['COMPANY_NM'], 'verifyCode': ''})

        res = requests.post(url, data=form_data, headers=headers)
        print(res.status_code, res.headers)
        for item in res.cookies.items():
            print(item)
        print(res.text)
    # print(res.cookies)
    # js_code = re.findall('<script>(.*?)</script>', res.text)[0]
    # print(js_code)
    # js_result = execjs.compile(js_code)
    # print(js_result.call(''))
    # chrome = get_page_from_selenium(url)
    # cookie_items = chrome.get_cookies()
    # chrome.switch_to('')
    # print(chrome.page_source)
    # cookies = {'cookie': ''}
    # for cookie in cookie_items:
    #     cookies['cookie'] += cookie['name'] + '=' + cookie['value']
    #     cookies['cookie'] += '; '
    # print(cookies)
    # res = requests.get(url, cookies=cookies)
    # print(res.headers)
    # print(res.text)
