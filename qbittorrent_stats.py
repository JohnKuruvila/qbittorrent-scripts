# Gets qBittorrent stats and writes them to an InfluxDB2 instance.
import requests
import json
from datetime import datetime
from influxdb import InfluxDBClient

server_ip = ""
qbport = ""
qbusername = ""
qbpassword = ""

server_address = "http://" + server_ip + ":" + qbport

s = requests.Session()
s.get(
    server_address
    + "/api/v2/auth/login?username="
    + qbusername
    + "&password="
    + qbpassword
)
torrents = json.loads(s.get(server_address + "/api/v2/torrents/info").text)

client = InfluxDBClient(
    host="127.0.0.1", port=8086, username="", password="", database=""
)

current_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

for torrent in torrents:
    if torrent["uploaded_session"] != 0:

        s.get(server_address + "/api/v2/auth/logout")

        influxdb_data = [
            {
                "measurement": "session_upload",
                "time": current_time,
                "tags": {"torrent_name": torrent["name"]},
                "fields": {"session_upload": torrent["uploaded_session"]},
            }
        ]

        client.write_points(influxdb_data)

client.close()
