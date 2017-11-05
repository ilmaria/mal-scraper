import json
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import argparse

ANIME_LIST = 'data/mal_users.json'
TARGET = 'Limpparipoju'

def get_target():
    user_ids = {}

    with open(ANIME_LIST, 'r') as file:
        for i, line in enumerate(file):
            try:
                entry = json.loads(line)
                if entry['user_name'] == TARGET:
                    print('Found user on line:' + str(i))
                    with open(TARGET + '.json', 'w') as target_values:
                        target_values.write(json.dumps(entry) + '\n')
                    break

            except ValueError:
                print("Error with processing user_ids. Current line: " + str(i) + "\n\n")

def main():
    parser = argparse.ArgumentParser(description='Calculate similarity.')
    parser.add_argument("-a", "--animelist", dest="animelist",
                        help="select anime list")
    args = parser.parse_args()
    
    with open(TARGET + '.json', 'r') as target:
        target_entry = json.loads(target.read())
        target_anime_ids = []
        target_anime_ratings = []
        similarities = []

        for anime in target_entry['anime_list']:
            target_anime_ids.append(int(anime['anime_id']))
            target_anime_ratings.append(int(anime['score']))

        res_len = 0
        with open(args.animelist + '.result.txt', 'a') as res:
            pass 
        with open(args.animelist + '.result.txt', 'r') as res:
            for line in res:
                res_len += 1
                similarities.append(tuple(line.split()))
            print('length ' + str(res_len))
            
        with open(args.animelist + '.result.txt', 'a') as res:
            with open(args.animelist, 'r') as file:
                for i, line in enumerate(file):
                    if i < res_len:
                        continue
                    try:
                        entry = json.loads(line)
                        anime_ratings = [0] * len(target_anime_ratings)

                        for j, anime_id in enumerate(target_anime_ids):
                            for anime in entry['anime_list']:
                                id = int(anime['anime_id'])
                                if id == anime_id:
                                    anime_ratings[j] = int(anime['score'])

                        similarity = cosine_similarity(np.array(target_anime_ratings).reshape(1, -1), np.array(anime_ratings).reshape(1, -1))
                        similarities.append((entry['user_name'], similarity))

                    except ValueError as e:
                        print("Error while processing ratings. Current line: " + str(i) + "\n" + str(e) + "\n")

                    name, similarity = similarities[i]
                    res.write('{} {}\n'.format(similarity[0][0], name))
                    
                    if i % 100 == 0:
                        print('Processed: ' + str(i) + ' lines\n')
                

if __name__ == '__main__':
    main()
