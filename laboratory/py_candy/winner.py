# -*- coding: UTF-8 -*-

# This script is used for query winner of candylottery.

# first, enum all winner table
# then, find all winner
# then, enum parter table, query winner's balance
# record it if balance is not zero

import urllib.request
import json

url = 'http://api.oraclechain.io/v1/chain/get_table_rows'

winner_values = {
    "code": "candylottery",
    "json": 1,
    "limit": 1,
    "lower_bound": "1",
    "scope": "candylottery",
    "table": "winner",
    "table_key": "",
    "upper_bound": ""
}

parter_values = {
    "code": "candylottery",
    "json": 1,
    "limit": 1,
    "key_type": "name",
    "lower_bound": "1",
    "scope": "candylottery",
    "table": "parter",
    "table_key": "",
    "upper_bound": ""
}

headers = {'Content-Type': 'application/json'}

unrefund = []

def make_request(v):
    request = urllib.request.Request(url=url, headers=headers, data=json.dumps(v).encode(encoding='UTF8'))
    response = urllib.request.urlopen(request)
    info = response.read().decode('utf8', "ignore")
    return info

def query_parter_balance(p):
    parter_values["lower_bound"] = p
    info = make_request(parter_values)
    resp = json.loads(info)
    if resp["rows"]:
        obj = resp["rows"][0]
        if obj:
            return obj["balance"]
    return ""

def query_winner():
    for i in range(30):
        print("querying peroid: ", i+1)
        winner_values["lower_bound"] = str(i+1)
        winner_values["upper_bound"] = str(i+2)
        info = make_request(winner_values)
        #print(info.encode('gbk', 'ignore').decode('gbk'))
        resp = json.loads(info)
        #print(resp)
        if resp["rows"]:
            # get list
            list = resp["rows"][0]["list"]
            if list:
                for w in list:
                    balance = query_parter_balance(w["name"])
                    if balance:
                        if balance != "0.0000 OCT":
                            unrefund.append((w["name"], balance))

        print("--------------------------")

if __name__ == '__main__':
    query_winner()
    print(unrefund)