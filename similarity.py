import numpy as np
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity


RATINGS = 'anime_ratings.txt'
TARGET = 'Limpparipoju'
USERNAMES = 'usernames.txt'

def main():
    ratings = np.loadtxt(RATINGS)
    ratings = sparse.csr_matrix(ratings)

    target = np.loadtxt(TARGET + '_ratings.txt')

    similarities = cosine_similarity(ratings, target)
    sorted_indices = similarities.argsort(axis=0)[::-1]
    top_indices = list(sorted_indices[:5])
    top_matches = [(None, None)]*5

    with open(USERNAMES, 'r') as usernames:
        for i, username in enumerate(usernames):
            if i in top_indices:
                top_matches[top_indices.index(i)] = (username, str(similarities[i][0]))

    col_width = max(len(user) for user, _ in top_matches)

    for user, similarity in top_matches:
        print(user.strip().ljust(col_width) + '\t' + similarity)


if __name__ == '__main__':
    main()
