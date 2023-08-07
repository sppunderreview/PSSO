from tqdm import tqdm
import pickle
import requests
import sys
import json

import os.path

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

headers = {'API-KEY': '?'}

def download(hashS):
    filePath = "data/"+hashS+".zip"
    if os.path.isfile(filePath):
        return
    filePath = "samples/"+hashS+".elf"
    if os.path.isfile(filePath):
        return
    r = requests.post('https://mb-api.abuse.ch/api/v1/', data={"query": "get_file", "sha256_hash": hashS}, verify=True, headers=headers)
    r.raise_for_status()
    data = r.content
    with open(filePath, 'wb') as f:
        f.write(data)

with open("selectedByFamily", "rb") as f:
	selectedByFamily = pickle.load(f)

selectedByFamily = [idS for idS in selectedByFamily]
print(len(selectedByFamily))

for idS in tqdm(selectedByFamily):
	try:
		download(idS)
	except Exception as e:
		print(e)
