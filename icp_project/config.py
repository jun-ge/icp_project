headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Host': 'www.miitbeian.gov.cn',
    'Referer': 'http://www.miitbeian.gov.cn/getVerifyCode?10',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3538.67 Safari/537.36',
}

form_data = {
    "siteName": "",
    "siteDomain": "",
    "siteUrl": "",
    "mainLicense": "",
    "siteIp": "",
    "condition": "5",
    "unitName": "",
    "mainUnitNature": "-1",
    "certType": "-1",
    "mainUnitCertNo": "",
    "verifyCode": "",
}

#备案信息查询--英文字段字典
data_dict = {
    'company_name': '主办单位名称',
    'company_nature': '主办单位性质',
    'permission_number': '网站备案/许可证号',
    'web_title': '网站名称',
    'web_url': '网站首页网址',
    'audit_time': '审核时间',
    'is_allow_access': '是否允许接入',
}
