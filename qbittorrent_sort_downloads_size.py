import requests
import json
import time

# qbittorrent credentials
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
torrents = json.loads(
    s.get(server_address + "/api/v2/torrents/info?filter=downloading").text
)

torrent_dict = {torrent["total_size"]: torrent["hash"] for torrent in torrents}
sorted_hash_array = [torrent_dict[size] for size in sorted(torrent_dict.keys())]

for torrent_hash in sorted_hash_array:
    print(
        s.post(
            server_address + "/api/v2/torrents/bottomPrio",
            data={"hashes": torrent_hash},
        )
    )

s.get(server_address + "/api/v2/auth/logout")
