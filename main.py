import urllib.request
import re

MAL_URL = "https://myanimelist.net/users.php?q={0}&show={1}"
USER_MULTIPLIER = 24
INTERVAL = 0.5


def search_users(username):
    i = 0
    pages_left = True

    while pages_left:
        try:
            url = MAL_URL.format(username, i * USER_MULTIPLIER)
            request = urllib.request.urlopen(url)
            i += 1

            yield request.read().decode("utf-8")

        except urllib.error.HTTPError:
            pages_left = False


def parse_usernames(html_page):
    names = set()

    for match in re.finditer(r"href=\"\/profile\/(\w+)\"", html_page):
        names.add(match.group(1))

    return names


def get_users(username):
    for results in search_users(username):
        names = parse_usernames(results)

        with open("mal_usernames.txt", "a") as file:
            for name in names:
                file.write(name + "\n")


if __name__ == "__main__":
    get_users("oikai")
