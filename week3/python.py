import urllib.request
import json
import csv

description = urllib.request.urlopen(
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
).read()
mrt_info = urllib.request.urlopen(
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
).read()

description_json = json.loads(description)
mrt_info_json = json.loads(mrt_info)

mrt_attractions = {}

for result in description_json["data"]["results"]:
    for i in range(len(mrt_info_json["data"])):
        if result["SERIAL_NO"] == mrt_info_json["data"][i]["SERIAL_NO"]:
            result["MRT"] = mrt_info_json["data"][i]["MRT"]
            result["address"] = mrt_info_json["data"][i]["address"]
            result["area"] = (
                mrt_info_json["data"][i]["address"].split("  ")[1].split("區")[0] + "區"
            )
            result["filelist"] = "https://" + result["filelist"].split("https://")[1]
            if result["MRT"] not in mrt_attractions:
                mrt_attractions[result["MRT"]] = []
            mrt_attractions[result["MRT"]].append(result["stitle"])
            break

with open("spot.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for result in description_json["data"]["results"]:
        writer.writerow(
            [
                result["stitle"],
                result["area"],
                result["longitude"],
                result["latitude"],
                result["filelist"],
            ]
        )

with open("mrt.csv", "w", newline="") as file:
    writer = csv.writer(file)
    for key in mrt_attractions:
        writer.writerow([key, *mrt_attractions[key]])
