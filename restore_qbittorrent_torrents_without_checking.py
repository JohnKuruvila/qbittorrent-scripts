import requests
import json
import os
from torf import Torrent

server_ip = ""
qbport = ""
qbusername = ""
qbpassword = ""
torrents_directory = ""

torrent_files_names_dict = {}

for torrent_file in os.listdir(torrents_directory):
    try:
        t = Torrent.read(torrents_directory + torrent_file)
        torrent_files_names_dict[t.name] = torrents_directory + torrent_file
    except:
        pass

server_ip = ""
qbport = ""
qbusername = ""
qbpassword = ""

server_address = "http://" + server_ip + ":" + qbport

s = requests.Session()
s.post(
    server_address + "/api/v2/auth/login",
    data={"username": qbusername, "password": qbpassword},
)

for torrent in json.loads(s.get(server_address + "/api/v2/torrents/info").text):
    if (
        torrent["state"] == "pausedDL"
        or torrent["state"] == "checkingUP"
        or torrent["state"] == "missingFiles"
    ):
        if torrent["name"] in torrent_files_names_dict.keys():
            print(torrent["name"])
            save_path = torrent["save_path"]
            category = torrent["category"]
            s.post(
                server_address + "/api/v2/torrents/delete",
                data={"hash": torrent["hash"], "deleteFiles": False},
            )
            files = {
                "savepath": (None, save_path),
                "skip_checking": (None, "true"),
                "category": (None, category),
                "filename": (
                    torrent_files_names_dict[torrent["name"]],
                    open(torrent_files_names_dict[torrent["name"]], "rb"),
                    "application/x-bittorrent",
                ),
            }
            s.post(
                server_address + "/api/v2/torrents/add",
                files=files,
            )

s.get(server_address + "/api/v2/auth/logout")
