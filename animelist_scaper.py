import urllib.request
import os.path as path
import sys
from datetime import datetime
import time
import random as r
import xml.etree.ElementTree as ET


MAL_URL = "https://myanimelist.net/malappinfo.php?u={0}&status=all&type=anime"
INTERVAL_START = 0.2
INTERVAL_END = 0.5
LOG_FILE = "events.log"
DATA_DIR = "data"
USERNAMES_FILE = path.join(DATA_DIR, "mal_usernames.txt")


def get_animelist(username):
    url = MAL_URL.format(username)
    request = urllib.request.urlopen(url)

    return ET.fromstring(request.read())


def main():
    with open(USERNAMES_FILE, "r") as file:
        for username in file:
            try:
                animelist = get_animelist(username.strip())
                ET.ElementTree(animelist).write("test.xml")

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
