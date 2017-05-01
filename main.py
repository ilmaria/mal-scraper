import urllib.request
import re
import os.path as path
import string
import itertools
import sys
from datetime import datetime
import random as r
import time

MAL_URL = "https://myanimelist.net/users.php?q={0}&show={1}"
USER_MULTIPLIER = 24
INTERVAL_START = 0.2
INTERVAL_END = 0.6
LOG_FILE = "events.log"
DATA_DIR = "data"


def search_users(username):
    i = 0
    pages_left = True

    while pages_left:
        try:
            url = MAL_URL.format(username, i * USER_MULTIPLIER)
            request = urllib.request.urlopen(url)
            i += 1

            yield request.read().decode("utf-8")

            time.sleep(r.uniform(INTERVAL_START, INTERVAL_END))

        except urllib.error.HTTPError:
            pages_left = False
        except:
            with open(LOG_FILE, "a") as log:
                exc_info = sys.exc_info()
                log.write(str(datetime.utcnow()) + "\n")
                log.write(str(exc_info[0]) + " ")
                log.write(str(exc_info[1]) + "\n\n")


def parse_usernames(html_page):
    names = set()

    for match in re.finditer(r"href=\"\/profile\/(\w+)\"", html_page):
        names.add(match.group(1))

    return names


def get_users(username):
    for results in search_users(username):
        names = parse_usernames(results)

        with open(path.join(DATA_DIR, "mal_usernames.txt"), "a") as file:
            for name in names:
                file.write(name + "\n")


def main():
    perms = itertools.permutations(string.ascii_lowercase, 3)

    os.makedirs(DATA_DIR, exist_ok=True)

    for prefix in perms:
        get_users(prefix)


if __name__ == "__main__":
    main()
