import urllib.request as Req
import json
import csv

print("---------------------Requesting Data---------------------")
raw_spot_info = Req.urlopen(
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
).read()
spot_list = json.loads(raw_spot_info)["data"]["results"]

raw_mrt_info = Req.urlopen(
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
).read()
mrt_list = json.loads(raw_mrt_info)["data"]

print("---------------------Processing Data---------------------")
mrt_spot_dict = {}

for spot in spot_list:
    for mrt in mrt_list:
        if spot["SERIAL_NO"] == mrt["SERIAL_NO"]:
            spot["MRT"] = mrt["MRT"]
            spot["address"] = mrt["address"]
            spot["area"] = mrt["address"].split("  ")[1].split("區")[0] + "區"
            spot["filelist"] = "https://" + spot["filelist"].split("https://")[1]
            if spot["MRT"] not in mrt_spot_dict:
                mrt_spot_dict[spot["MRT"]] = []
            mrt_spot_dict[spot["MRT"]].append(spot["stitle"])
            break

print("------------------Exporting Data to CSV------------------")
with open("spot.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for spot in spot_list:
        writer.writerow(
            [
                spot["stitle"],
                spot["area"],
                spot["longitude"],
                spot["latitude"],
                spot["filelist"],
            ]
        )

with open("mrt.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for key, value in mrt_spot_dict.items():
        writer.writerow([key, *value])

print("----------------------Task Finished----------------------")
