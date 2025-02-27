
import praw
import prawcore
from time import sleep
import json
import csv
import pandas as pd
import util
from multiprocessing import Pool

ALL_AUTHORS = pd.read_json('author.json', typ='series')
TARGET_DF = pd.read_csv('author.csv')
AUTHORS = TARGET_DF['author_id']
AUTHOR_DIFF = ALL_AUTHORS[~ALL_AUTHORS.isin(AUTHORS)]
print(AUTHOR_DIFF.shape)

NCHUNKS = 4
REDDITS = util.REDDITS
RANGES = util.find_ranges(AUTHOR_DIFF, NCHUNKS)
ARGS = zip(REDDITS, RANGES) 


def get_author_info(r, author):

	user = r.redditor(author)
	link = user.link_karma
	comment = user.comment_karma

	return [author, link, comment]


def get_all_author_info(arg):

	r, ranges = arg
	up, down = ranges
	for author in AUTHOR_DIFF.iloc[up:down]:
		data = ['', '', '']
		try :
			data = get_author_info(r, author)
		except:
			sleep(5)

		with open('author.csv', 'a') as f:
			wr = csv.writer(f, delimiter = ',')
			wr.writerow(data)

	return 


if __name__ == '__main__':
	with Pool(NCHUNKS) as p:
		p.map(get_all_author_info, ARGS)

