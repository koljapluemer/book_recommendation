import gzip
import json
import re
import os
import sys
import numpy as np
import pandas as pd
import json
from progress.bar import Bar
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from tqdm import tqdm


my_books = [59579811, 45245, 18197267, 57891574, 57891607, 997969, 18290401, 64218, 89187, 34506, 16902, 54493401, 32969945, 5771014, 3228917, 3347, 34497, 50937, 43582733, 9167158, 34502, 1966046, 47994, 54983, 833015, 48593951, 34484, 116296, 34511, 39318922, 18007564, 942337, 24113, 6547576, 1501477, 262359, 55536485, 260218, 139069, 7039888, 54870256, 54503521, 42900772, 56269264, 20804441, 24611623, 590652, 841, 12009, 39863499, 48037, 57306699, 44767458, 54930681, 19008180, 13202448, 6290281, 290583, 51738, 170448, 18122, 41637836, 40121378, 13098597, 50220199, 11127, 1319, 6683549, 4865, 25744928, 46674, 27036528, 42046112, 34507927, 13078769, 313605, 18630, 12126193, 12236203, 11275323, 16158576, 769483, 53597796, 58245377, 6708, 119322, 1845, 67896, 6324090, 56447036, 36072, 1059, 912728, 1476605, 386372, 865871, 48838, 22055262, 25506635, 5948056, 34466963, 28862, 129327, 41887005, 1950374, 21535271, 6329013, 36556202, 1215032, 12016, 40383078, 8285950, 46465, 186074, 64222]


def test_for_my_books():


    # open reviews.json.gz and check any book_id in my_books
    with gzip.open('goodreads_reviews_dedup.json.gz') as fin:
        for l in fin:
            d = json.loads(l)
            if d['book_id'] in my_books:
                print(d['book_id'])
                print(d['rating'])
                print(d['user_id'])


def get_test_lines(nr_lines):
    # get 100 lines from reviews.json.gz
    with gzip.open('goodreads_reviews_dedup.json.gz') as fin:
        for i, l in enumerate(fin):
            if i < nr_lines:
                print(l)
            else:
                break

def test_for_my_books_in_json():
    # check for my books in reviews.json
    with open('reviews_filtered.json') as f:
        data = json.load(f)

        for d in data:
            if int(d['book_id']) in my_books:
                print(d['book_id'])
                print(d['rating'])
                print('-----------')

test_for_my_books_in_json()