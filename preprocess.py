import json


ANIME_LIST = 'data/anime_lists.json'
TARGET = 'Limpparipoju'
ANIME_NAMES = 'anime_names.txt'
RATINGS = 'anime_ratings.txt'
USERNAMES = 'usernames.txt'


def main():
    anime_ids = {}

    with open(ANIME_NAMES, 'w') as file:
        pass
    with open(RATINGS, 'w') as file:
        pass
    with open(USERNAMES, 'w') as file:
        pass

    with open(ANIME_LIST, 'r') as file:
        for line in file:
            entry = json.loads(line)

            for anime in entry['anime_list']:
                anime_ids[int(anime['anime_id'])] = 0

                with open(ANIME_NAMES, 'a') as id_file:
                    id_file.write(anime['anime_id'] + '\t' + anime['title'] + '\n')

    with open(ANIME_LIST, 'r') as file:
        for line in file:
            entry = json.loads(line)
            anime_ids = anime_ids.fromkeys(anime_ids, 0)

            for anime in entry['anime_list']:
                anime_ids[int(anime['anime_id'])] = int(anime['score'])

            if entry['user_name'] == TARGET:
                ratings_file = TARGET + '_ratings.txt'
            else:
                ratings_file = RATINGS

                with open(USERNAMES, 'a') as usernames:
                    usernames.write(entry['user_name'] + '\n')

            with open(ratings_file, 'a') as ratings:
                ratings.write(' '.join(map(lambda x: str(x), anime_ids.values())) + '\n')
                


if __name__ == '__main__':
    main()
