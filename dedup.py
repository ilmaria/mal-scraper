import json


ANIME_LIST1 = 'data/anime_lists.json'
ANIME_LIST2 = 'data/anime_lists2.json'
ANIME_LIST3 = 'data/anime_lists3.json'
NAMES = 'data/usernames.txt'
OUTPUT = 'data/mal_users.json'


def main():
    names = set()
    lists = [ANIME_LIST1, ANIME_LIST2, ANIME_LIST3]

    with open(NAMES, 'w') as file:
        pass
    with open(OUTPUT, 'w') as file:
        pass

    for alist in lists:
        with open(alist, 'r') as file:
            for line in file:
                try:
                    entry = json.loads(line)
                    name = entry['user_name']

                    if name not in names:
                        names.add(name)
                        with open(OUTPUT, "a") as anime_lists:
                            anime_lists.write(json.dumps(entry) + "\n")

                except:
                    pass

    with open(NAMES, 'a') as file:
        file.write('\n'.join(names))


if __name__ == '__main__':
    main()
