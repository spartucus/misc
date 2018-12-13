# -*- coding: UTF-8 -*-

import urllib.request
import json
import random
import sys
import hashlib

url = 'http://api-kylin.eosasia.one/v1/chain/get_table_rows'

window_values = {
    "code": "snowsnowwar4",
    "json": 1,
    "limit": -1,
    "lower_bound": "",
    "scope": "snowsnowwar4",
    "table": "window",
    "table_key": "",
    "upper_bound": ""
}

headers = {
    'Content-Type': 'application/json',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
}

def make_request(v):
    request = urllib.request.Request(url=url, headers=headers, data=json.dumps(v).encode(encoding='UTF8'))
    response = urllib.request.urlopen(request)
    info = response.read().decode('utf8', "ignore")
    return info

def query_window():
    info = make_request(window_values)
    resp = json.loads(info)
    if  resp["rows"]:
        return resp["rows"]
    return []

if __name__ == '__main__':
    windows = query_window()
    if windows:
        print(json.dumps(windows, indent=4, sort_keys=True))

        for w in windows:
            round = w["round"]
            prerandom = w["prerandom"]

            flag = 0
            while flag == 0:
                msg = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
                hm = hashlib.sha256((str(round) + prerandom + msg ).encode('utf-8')).hexdigest()
                if int(hm[0:2], 16) == round % 0xffff:
                    flag = 1
                    print("msg = ", msg)
                    print("hm = ", hm)
