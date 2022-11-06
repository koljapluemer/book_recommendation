# stealing from https://towardsdatascience.com/recommendation-system-matrix-factorization-d61978660b4b
# ...but slapping the big dataset on it

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


from time import sleep
from tqdm import tqdm

import numpy

# steps *was* 5000
def matrix_factorization(R, P, Q, K, steps=10, alpha=0.0002, beta=0.02):
    '''
    R: rating matrix
    P: |U| * K (User features matrix)
    Q: |D| * K (Item features matrix)
    K: latent features
    steps: iterations
    alpha: learning rate
    beta: regularization parameter'''
    Q = Q.T

    for step in tqdm(range(steps)):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    # calculate error
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])

                    for k in range(K):
                        # calculate gradient with a and beta parameter
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])

        eR = numpy.dot(P,Q)

        e = 0

        for i in range(len(R)):

            for j in range(len(R[i])):

                if R[i][j] > 0:

                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)

                    for k in range(K):

                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        # 0.001: local minimum
        if e < 0.001:

            break

    return P, Q.T



def test():
    with open('reviews_filtered.json') as f:
        data = json.load(f)

    # create a pivot table with book_id as columns and user_id as rows
    df = pd.DataFrame(data)
    book_pivot = df.pivot(index='user_id', columns='book_id', values='rating')
    book_pivot.fillna(0, inplace=True)
    print('========= I created a pivot table (of users and book ids [hopefully]). Here is the head.')
    print('PIVOT TABLE:', book_pivot.head())

    # ADD MY OWN STUFF
    # open data/my_books.csv
    # read it into a dataframe
    with open('data/my_books.csv') as f:
        my_books = pd.read_csv(f)

    # create a dictionary from 'Book Id' and 'My Rating' columns
    # have the id be a string
    my_books_dict = my_books.set_index('Book Id')['My Rating'].to_dict()
    # convert keys to strings
    my_books_dict_full = {str(k):v for k,v in my_books_dict.items()} 
    # if book_id is not in the columns list of book_pivot, remove it from the dictionary
    my_books_dict = {k:v for k,v in my_books_dict_full.items() if k in book_pivot.columns}
    
    # print list with all my book ids
    id_list = list(my_books_dict.keys())
    print('========= Here are my book ids:')
    print(id_list)
    print('CREATE A DICTIONARY FROM MY BOOKS (first 5):', list(my_books_dict.items())[:5])
    print('number of items in my_books_dict:', len(my_books_dict))

    print('number of columns in book_pivot:', len(book_pivot.columns))
    # add my books to the pivot table
    # ignore columns that are not already in the pivot table
            
    book_pivot = pd.concat([book_pivot, pd.DataFrame.from_records([my_books_dict])])
    print('number of columns in book_pivot:', len(book_pivot.columns))

    # fill in Nan values with 0
    book_pivot.fillna(0, inplace=True)

    # print the row for my user
    print('========= Here is the row for my user:')
    print(book_pivot.tail())


    # create a nested array from the rows of the pivot table
    R = book_pivot.values

    # R = [
    #     [5,3,0,1],
    #     [4,0,0,1],
    #     [1,1,0,5],
    #     [1,0,0,4],
    #     [0,1,5,4],
    #     [2,1,3,0],
    #     ]

    R = numpy.array(R)
    # N: num of User
    N = len(R)
    # M: num of Movie
    M = len(R[0])
    # Num of Features
    K = 3

    
    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)

    
    print("Starting Matrix Factor")
    nP, nQ = matrix_factorization(R, P, Q, K)
    nR = numpy.dot(nP, nQ.T)
    return nR


matrix = test()
# save matrix to file
with open('data/matrix.json', 'w') as f:
    json.dump(matrix.tolist(), f)
print(matrix)
