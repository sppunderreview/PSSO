from tqdm import tqdm
import pickle
import requests
import sys
import json
import os.path

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'API-KEY': '?'}

def getJson(hashS):
    r = requests.post('https://mb-api.abuse.ch/api/v1/', data={"query": "get_info", "hash": hashS}, verify=False, headers=headers)
    r.raise_for_status()
    dataJson = r.json()
    return dataJson

with open("elf.csv", "r",encoding='utf-8') as f:
    for l in tqdm(f.readlines()):
        idS = l.strip().split(",")[1]
        
        try:
            jsonPath = "metadata/"+idS+".json"
            if os.path.isfile(jsonPath) == False:
                dataJson = getJson(idS)
                with open(jsonPath, "w") as f:
                    json.dump(dataJson, f)
        except Exception:
            pass



