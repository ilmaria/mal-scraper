import urllib.request
import re
import os
import os.path as path
import string
import itertools
import sys
from datetime import datetime
import random as r
import time
import argparse

MAL_URL = "https://myanimelist.net/users.php?q={0}&show={1}"
USER_MULTIPLIER = 24
INTERVAL_START = 0.2
INTERVAL_END = 0.5

TS = str(time.time())
LOG_FILE = "events" + TS + ".log"
DATA_DIR = "data"
PROGRESS_FILE = "user_progress" + TS + ".log"


def search_users(username):
    i = 0
    pages_left = True

    while pages_left:
        try:
            url = MAL_URL.format(username, i * USER_MULTIPLIER)
            request = urllib.request.urlopen(url)
            i += 1

            with open(PROGRESS_FILE, "r+") as progress:
                lines = progress.readlines()
                lines[-1] = "Page: " + str(i)
                progress.seek(0)
                progress.truncate()
                progress.writelines(lines)

            yield request.read().decode("utf-8")

            time.sleep(r.uniform(INTERVAL_START, INTERVAL_END))

        except urllib.error.HTTPError as err:
            if err.code == 404:
                pages_left = False
            else:
                raise


def parse_usernames(html_page):
    names = set()

    for match in re.finditer(r"href=\"\/profile\/(\w+)\"", html_page):
        names.add(match.group(1))

    return names


def get_users(prefix):
    for results in search_users(prefix):
        names = parse_usernames(results)

        with open(path.join(DATA_DIR, "mal_usernames.txt"), "a") as file:
            for name in names:
                file.write(name + "\n")


def main():
    parser = argparse.ArgumentParser(description="Retrieve usernames from myanimelist.net")
    parser.add_argument("-c", "--continue", dest="continue_after",
                        help="retrieve usernames that come up after this 3 letter search string")
    parser.add_argument("-r", "--reverse", action="store_true",
                        help="search usernames in reversed order")
    args = parser.parse_args()

    if args.reverse:
        alphabet = reversed(string.ascii_lowercase)
    else:
        alphabet = string.ascii_lowercase

    name_prefixes = itertools.product(alphabet, repeat=3)

    os.makedirs(DATA_DIR, exist_ok=True)

    if args.continue_after is not None:
        next_prefix = None
        while next_prefix != args.continue_after:
            next_prefix = "".join(name_prefixes.__next__())

    for prefix_tuple in name_prefixes:
        prefix = "".join(prefix_tuple)

        try:
            with open(PROGRESS_FILE, "w") as progress:
                progress.write("Prefix: \"" + prefix + "\"\nPage: 0")

            get_users(prefix)
        except:
            with open(LOG_FILE, "a") as log:
                exc_info = sys.exc_info()
                log.write(str(datetime.utcnow()) + "\n")
                log.write("Current prefix: " + prefix + "\n")
                log.write(str(exc_info[0]) + " ")
                log.write(str(exc_info[1]) + "\n\n")
            raise


if __name__ == "__main__":
    main()
