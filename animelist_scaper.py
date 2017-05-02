import urllib.request
import os.path as path
import sys
from datetime import datetime
import time
import random as r
import xml.etree.ElementTree as ET
import json


MAL_URL = "https://myanimelist.net/malappinfo.php?u={0}&status=all&type=anime"
INTERVAL_START = 0.2
INTERVAL_END = 0.5
LOG_FILE = "events.log"
DATA_DIR = "data"
USERNAMES_FILE = path.join(DATA_DIR, "mal_usernames.txt")
ANIME_LISTS_FILE = path.join(DATA_DIR, "anime_lists.json")


def get_anime_list(username):
    url = MAL_URL.format(username)
    request = urllib.request.urlopen(url)

    return ET.fromstring(request.read())


def extract_data(anime_list):
    info = anime_list.find("myinfo")
    completed = int(info.find("user_completed").text)

    if completed < 10:
        return None

    anime_data = {
        "user_name": info.find("user_name").text,
        "user_id": info.find("user_id").text,
        "anime_list": []
    }

    for anime in anime_list.findall("anime"):
        title = anime.find("series_title").text
        score = int(anime.find("my_score").text)

        if score > 0:
            anime_data["anime_list"].append((title, score))

    return anime_data


def main():
    with open(USERNAMES_FILE, "r") as file:
        for username in file:
            try:
                anime_list = get_anime_list(username.strip())
                anime_data = extract_data(anime_list)

                if anime_data is not None:
                    with open(ANIME_LISTS_FILE, "a") as anime_lists:
                        anime_lists.write(json.dumps(anime_data) + "\n")

                time.sleep(r.uniform(INTERVAL_START, INTERVAL_END))

            except:
                with open(LOG_FILE, "a") as log:
                    exc_info = sys.exc_info()
                    log.write(str(datetime.utcnow()) + "\n")
                    log.write("Current username: " + username + "\n")
                    log.write(str(exc_info[0]) + " ")
                    log.write(str(exc_info[1]) + "\n\n")
                raise


if __name__ == "__main__":
    main()
