#!/usr/bin/python3

# Tristan Benoit
# 2022
# These

from os import system
from os.path import isfile, join, getsize
from pathlib import Path

from tqdm import tqdm

from random import shuffle


archive = []
for path in Path('data').rglob('*'):
	pathString = str(path)
	if ".zip" in pathString:
		archive += [pathString]

for a in tqdm(archive):
	system("7z x "+a+" -pinfected   >/dev/null")


for path in Path('data').rglob('*.elf'):
	pathString = str(path)
	if pathString[-4:] == ".elf":
		nameFile = pathString.split("/")[-11]
		system("cp "+pathString+" ./samples/"+nameFile)


# To extract again
"""
archive = []
for path in Path('samples').rglob('*'):
	pathString = str(path)
	archive += [pathString]
for a in tqdm(archive):
	system("cp "+a+" "+a+".zip")

archive = []
for path in Path('samples').rglob('*'):
	pathString = str(path)
	if ".zip" in pathString:
		archive += [pathString]

for a in tqdm(archive):
	system("7z x "+a+" -pinfected   >/dev/null")
"""

# Could be usefull
"""
archive = []
for path in Path('.').rglob('*'):
	pathString = str(path)
	if ".zip" in pathString:
		archive += [pathString]

for a in archive:
	system("7z x "+a+" -pinfected -y")
"""


