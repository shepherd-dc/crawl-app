import json
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Queue

import requests

from fiddler_douguo.handle_mongo import mongo_instance

queue_list = Queue()

def handle_request(url, data):
    headers = {
        "client": "4",
        "version": "6957.4",
        "device": "OPPO R17",
        "sdk": "22,5.1.1",
        "channel": "zhuzhan",
        "resolution": "852*1600",
        "display-resolution": "852*1600",
        "dpi": "2.0",
        # "android-id": "1002b5cbe22e2902",
        # "pseudo-id": "5cbe22e29021002b",
        "brand": "OPPO",
        "scale": "2.0",
        "timezone": "28800",
        "language": "zh",
        "cns": "3",
        "carrier": "CHINA+MOBILE",
        # "imsi": "460072902322646",
        "User-Agent": "Mozilla/5.0 (Linux; Android 5.1.1; OPPO R17 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36",
        "act-code": "1581521211",
        "act-timestamp": "1581521203",
        "uuid": "d4ee25ac-fff8-4ed3-8a80-eaf4759da70f",
        "battery-level": "1.00",
        "battery-state": "3",
        # "mac": "10:02:B5:CB:E2:2E",
        "imei": "866174294532268",
        "terms-accepted": "1",
        "newbie": "1",
        "reach": "10000",
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "Keep-Alive",
        # "Cookie": "duid=63010524",
        "Host": "api.douguo.net",
        # "Content-Length": "132"
    }
    # proxy = {'http':'http://163.204.247.172:9999'}
    response = requests.post(headers=headers, url=url, data=data)
    return response

def handle_index():
    url = 'http://api.douguo.net/recipe/flatcatalogs'
    data = {
        "client": "4",
        # "_session": "1581744536381866174294532268",
        # "v": "1581519805",
        "_vs": "2305",
        "sign_ran": "ff39981b7ec0e884446b7dddfb27f2a8",
        "code": "fe8351f06d479dff"
    }
    response = handle_request(url=url, data=data)

    index_item_dict = json.loads(response.text)
    for index_cate in index_item_dict['result']['cs']:
        for index_item in index_cate['cs']:
            for item in index_item['cs']:
                post_data = {
                    "client": "4",
                    # "_session": "1581744536381866174294532268",
                    "keyword": item['name'],
                    "order": "0",
                    "_vs": "11102",
                    "type": "0",
                    "auto_play_mode": "2",
                    "sign_ran": "7c955b63d19b44f36a0bb30ae4a6bf10",
                    "code": "efd0f1186179dd8b"
                }
                queue_list.put(post_data)

def handle_recipe_list(data):
    print('当前处理食材:', data['keyword'])
    recipe_list_url = 'http://api.douguo.net/recipe/v2/search/0/20'
    recipe_list_response = handle_request(url=recipe_list_url, data=data)

    recipe_list_response_dict = json.loads(recipe_list_response.text)
    for item in recipe_list_response_dict['result']['list']:
        recipe_info = {}
        recipe_info['major_ingredient'] = data['keyword']
        if item['type'] == 13:
            recipe_info['username'] = item['r']['an']
            recipe_info['cook_id'] = item['r']['id']
            recipe_info['description'] = item['r']['cookstory']
            recipe_info['recipe_name'] = item['r']['n']
            recipe_info['ingredient_list'] = item['r']['major']

            detail_url = 'http://api.douguo.net/recipe/detail/' + str(recipe_info['cook_id'])
            detail_data = {
                "client": "4",
                # "_session": "1581744536381866174294532268",
                "author_id": "0",
                "_vs": "11102",
                "_ext": '{"query":{"kw":' + recipe_info['major_ingredient'] + ',"src":"11102","idx":"13","type":"13","id":' + str(recipe_info['cook_id']) + '}}',
                "is_new_user": "1",
                "sign_ran": "995d55ba7d6711cfaa3f34a1782c7aee",
                "code": "41f844e6058c100a"
            }
            detail_response = handle_request(url=detail_url, data=detail_data)
            detail_response_dict = json.loads(detail_response.text)

            recipe_info['tips'] = detail_response_dict['result']['recipe']['tips']
            recipe_info['cook_step'] = detail_response_dict['result']['recipe']['cookstep']

            print('当前入库的菜谱是：', recipe_info['recipe_name'])

            mongo_instance.insert_item(recipe_info)

        else:
            continue


handle_index()

pool = ThreadPoolExecutor(max_workers=20)
while queue_list.qsize() > 0:
    pool.submit(handle_recipe_list, queue_list.get())

# handle_recipe_list(queue_list.get())
# print(queue_list.qsize())
