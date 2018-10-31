import os

# from aip import AipOcr
from aip import AipOcr

CONTENTS = r"./has_done/"

APP_ID = "14631087"
API_KEY = 'oUpODVGG7dKtG1VoTaAZ2AIb'
SECRET_KEY = '86AXMDBG0Lzin3NTmMfe3g71FC6U5yUb'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)


def get_file_path(path):
    with open(path, 'rb') as fr:
        return fr.read()

options = {
    # 方向朝上
    'detect_direction': 'true',
    # 识别类型，中英文，数字
    'language_type': 'CHN_ENG'
}
# for img in os.listdir('has_done'):
#     img_rb = get_file_path(CONTENTS + img)
#     result = client.basicGeneral(img_rb, options=options)
#     print(result)


def get_verify_code(path):
    img = get_file_path(path)
    options = {
        # 方向朝上
        'detect_direction': 'true',
        # 识别类型，中英文，数字
        'language_type': 'CHN_ENG'
    }
    result = client.basicGeneral(img, options=options)
    return result['words_result'][0]['words']