import time
from io import BytesIO

import pytesseract
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# from verifyCode_images.image_dispose import ImageDispose
from icp_project.Tools.common_tools.excel_tools import excel_to_dict
from icp_project.Tools.db_tools.mongo_tools import MongoClientTools
from icp_project.verifyCode_images.image_dispose import ImageDispose

data = {
    'company_name': '',
    'company_nature': '',
    'permission_number': '',
    'web_title': '',
    'web_url': '',
    'audit_time': '',
    'is_allow_access': '',
}
browser = webdriver.Chrome()
# browser.maximize_window()
wait = WebDriverWait(browser, 10)


def get_new_verifycode():
    verify_code_img_ele = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#vcode'))
    )
    verify_code_img_ele.click()
    time.sleep(1)
    # 确认验证码图片的位置
    location = verify_code_img_ele.location
    size = verify_code_img_ele.size
    left, top, right, bottom = location['x'] + 140, location['y'] + 140, location['x'] + 188 + size['width'], location[
         'y'] + 150 + size['height']
    # left, top, right, bottom = location['x'], location['y'], location['x'] + size['width'], location[
    #          'y'] + size['height']
    # 截图,获取验证码图片
    screenshot = Image.open(BytesIO(browser.get_screenshot_as_png()))
    verify_code_img = screenshot.crop((left, top, right, bottom))

    verify_code = ImageDispose(verify_code_img).dispose()
    while not verify_code:
        verify_code = get_new_verifycode()
    return verify_code


def get_page(company_name):
    count = 0
    url = "http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action"
    browser.get(url)
    input_unit_name = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#z5'))
    )
    input_unit_name.click()
    input_unit_name.clear()
    time.sleep(0.1)
    input_unit_name.send_keys(company_name)
    time.sleep(0.1)
    # 获取验证码的按钮并点击
    verify_code_get = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#getCheckCode'))
    )
    verify_code_get.click()
    time.sleep(1)
    # 找到验证码元素
    verify_code_img_ele = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#vcode'))
    )
    # ima_url = verify_code_img_ele.get_attribute('src')

    # 确认验证码图片的位置
    location = verify_code_img_ele.location
    size = verify_code_img_ele.size
    left, top, right, bottom = location['x'] + 140, location['y'] + 160, location['x'] + 188 + size['width'], location[
        'y'] + 166 + size['height']
    # left, top, right, bottom = location['x'], location['y'], location['x'] + size['width'], location[
    #     'y'] + size['height']
    # 截图,获取验证码图片
    screenshot = Image.open(BytesIO(browser.get_screenshot_as_png()))
    verify_code_img = screenshot.crop((left, top, right, bottom))

    input_verify_code = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#textfield7'))
    )
    input_verify_code.clear()
    verify_code = ImageDispose(verify_code_img).dispose()
    while not verify_code:
        verify_code = get_new_verifycode()
    input_verify_code.send_keys(verify_code)
    time.sleep(0.1)
    check_note = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#checkNote'))
    )
    print(check_note.text)
    while '错误' in check_note.text or not check_note.text:
        count += 1
        verify_code_img_ele.click()
        verify_code = get_new_verifycode()
        input_verify_code.click()
        input_verify_code.clear()
        input_verify_code.send_keys(verify_code)
        time.sleep(0.5)
        check_note = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#checkNote'))
        )
        print(check_note.text if check_note.text is not None else '空')
        if count == 12:
            data.update({'company_name': company_name})
            return data
    time.sleep(0.2)
    submit = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#button1'))
    )
    submit.click()

    text = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.text'))
    ).text
    if '没有符合条件的记录' in text:
        data.update({'info': 'no_info'})
        return data
    else:
        result = {}
        for i in range(100):
            if is_element_exist('#' + str(i)):
                tds = browser.find_elements_by_class_name('bxy')
                data.update(
                    {
                        'company_name': tds[0].text.strip(),
                        'company_nature': tds[1].text.strip(),
                        'permission_number': tds[2].text.strip(),
                        'web_title': tds[3].text.strip(),
                        'web_url': tds[4].text.strip(),
                        'audit_time': tds[5].text.strip(),
                        'is_allow_access': tds[6].text.strip(),
                    }
                )
                result.update({str(i): data})
            else:
                break
        return result


def is_element_exist(element):
    flag = True
    try:
        browser.find_element_by_id(element)
        return flag
    except Exception:
        return not flag


def img_dispose(image):
    # 转化到灰度图片
    image = image.convert('L')
    image.show()
    # 二值化
    threshold = 160
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    image.show()
    tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
    result = pytesseract.image_to_string(image, config=tessdata_dir_config)
    print(result)
    return result


if __name__ == '__main__':
    conn = MongoClientTools()
    # url = "http://www.miitbeian.gov.cn/icp/publish/query/icpMemoInfo_searchExecute.action"
    # browser = webdriver.PhantomJS()
    # browser.get(url)
    # print(browser.page_source)
    # path = r'GJX744.jpeg'
    # img_dispose(path)
    for item in excel_to_dict(r'E:\workplace\program\icp_project_temp\icp_project\ICP公司列表-1018.xls'):
        print(item)
        dict_date = get_page(item.get('COMPANY_NM'))
        conn.save(dict_date, 'icp备案')
    # res = requests.get('http://xueqiu.com/', headers=headers)
    # print(res.text)
