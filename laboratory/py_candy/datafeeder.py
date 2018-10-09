# -*- coding: UTF-8 -*-

# This script is used to query datafeeder's balance,
# either staked or rewards

# first, enumerate dfreputation table
# then, take each name in reputation as scope of dfregistery
# count available and staked together
# we get what we want.

import urllib.request
import json
import ast

url = 'http://api.oraclechain.io/v1/chain/get_table_rows'

reputation_values = {
    "code": "oraclemarket",
    "json": 1,
    "limit": -1,
    "lower_bound": "",
    "scope": "oraclemarket",
    "table": "dfreputation",
    "table_key": "",
    "upper_bound": ""
}

registery_values = {
    "code": "oraclemarket",
    "json": 1,
    "limit": 1,
    "key_type": "name",
    "lower_bound": "1",
    "scope": "",
    "table": "dfregistery",
    "table_key": "",
    "upper_bound": ""
}

headers = {'Content-Type': 'application/json'}

def make_request(v):
    request = urllib.request.Request(url=url, headers=headers, data=json.dumps(v).encode(encoding='UTF8'))
    response = urllib.request.urlopen(request)
    info = response.read().decode('utf8', "ignore")
    return info


def query_reputation():
    info = make_request(reputation_values)
    resp = json.loads(info)
    if  resp["rows"]:
        return resp["rows"]
    return []

def query_registery_balance(name):
    registery_values["scope"] = name
    info = make_request(registery_values)
    resp = json.loads(info)
    if resp["rows"]:
        obj = resp["rows"][0]
        if obj:
            available = ast.literal_eval(obj["available"].split(' ', 1)[0])
            staked = ast.literal_eval(obj["staked"].split(' ', 1)[0])
            return "%.4f" % (available+staked)
    return "0.0000"

if __name__ == '__main__':
    reputations = query_reputation()
    if reputations:
        for r in reputations:
            name = r["owner"]
            balance = query_registery_balance(name)
            print("%s,OCT,%s" % (name, balance))
