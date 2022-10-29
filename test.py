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


DIR = './'

def load_data(file_name, head = 100000):
    count = 0
    data = []
    with gzip.open(file_name) as fin:
        for l in fin:
            d = json.loads(l)
            count += 1
            data.append(d)

            
            # break if reaches the 100th line
            if (head is not None) and (count > head):
                break
    return data



reviews = load_data(os.path.join(DIR, 'goodreads_reviews_dedup.json.gz'))
print(np.random.choice(reviews).keys())

def create_special_dataset():
    # create a dataset as json with only the following columns: book_id, rating, user_id
    # save the dataset as a json file
    df = pd.DataFrame(reviews)
    df = df[['book_id', 'rating', 'user_id']]
    df.to_json('reviews.json', orient='records')


# create_special_dataset()
def create_reduced_dataset():
# load reviews.json with json 
    with open('reviews.json') as f:
        data = json.load(f)

        # extract a smaller dataframe only with users who have rated over 50 books
        df = pd.DataFrame(data)
        # print row count
        print('unfiltered reviews:', df.shape[0])
        df = df.groupby('user_id').filter(lambda x: len(x) > 50)
        print('filtered reviews (users):', df.shape[0])
        # extract a smaller df with only book_ids that have more than 50 reviews
        df = df.groupby('book_id').filter(lambda x: len(x) > 50)
        print('filtered reviews (books):', df.shape[0])

        # save the filtered dataset as a json file
        df.to_json('reviews_filtered.json', orient='records')

# create_reduced_dataset()


#  create a dataframe with book_id and title
def create_book_title():
    # load the books gzip file
    books = load_data(os.path.join(DIR, 'goodreads_books.json.gz'))
    df = pd.DataFrame(books)
    print('BOOKS TABLE:', df.head())
    # print column names
    print('BOOKS TABLE COLUMN', df.columns)
    df = df[['book_id', 'title']]
    df.to_json('book_title.json', orient='records')

# create_book_title()

def create_pivot():
    # load reviews_filtered.json with json
    with open('reviews_filtered.json') as f:
        data = json.load(f)

        # create a pivot table with book_id as columns and user_id as rows
        df = pd.DataFrame(data)
        book_pivot = df.pivot(index='user_id', columns='book_id', values='rating')
        book_pivot.fillna(0, inplace=True)
        print('========= I created a pivot table (of users and book ids [hopefully]). Here is the head.')
        print('PIVOT TABLE:', book_pivot.head())
 
        # create csr matrix
        csr = csr_matrix(book_pivot)
        model = NearestNeighbors(algorithm='brute')
        model.fit(csr)

        # load book_title.json with json
        with open('book_title.json') as f:
            book_title = json.load(f)
            book_title = pd.DataFrame(book_title)
            book_title.set_index('book_id', inplace=True)
            print('========= I am opening a specific table matching ids and book titles, created earlier')
            print('BOOK TITLE / ID DATAFRAME:', book_title.head())
            print('number of rows:', book_title.shape[0])

            # create a function that takes a book as input and returns the 10 most similar books
            def get_recommendations(book_id, n_recommendations):
                
                
            # make an array from the column names
            book_ids = book_pivot.columns.values
            # create an array from the 'book_id' column of book_title
            book_ids_title = book_title.index.values
            print('========= We are comparing the first 10 col names from the pivot table with the first 10 entries from the title/id reference dataframe. They *should* be similarly formatted ids')
            print('sanity check for the lists', book_ids[:10], book_ids_title[:10])
            # create a list of book_ids that are in both df and book_title
            book_ids_both = list(set(book_ids) & set(book_ids_title))
            
            # get a random book_id from the list of book_ids that are in both df and book_title
            book_id = np.random.choice(book_ids_both)
            print('THE BOOK WE ARE CHECKING: ', book_id)
           
            # print the 10 most similar books to the book title
            similar_ids = get_recommendations(book_id, 10)
            print('SIMILAR IDEAS: ', similar_ids)

            print('========= now we try to get book titles')
            # find book_id in book_title df and print the corresponding name
            title_of_reference_book = book_title.loc[book_id, 'title']
            print('TITLE OF REFERENCE BOOK: ', title_of_reference_book)
            print('..............and we recommend.........')
            # now, loop the similar_ids and also find their titles
            for id in similar_ids:
                print("checking id", id)
                try:
                    title_of_recommendation = book_title.loc[id, 'title']
                    print("TITLE", title_of_recommendation)
                except:
                    print("could not find book")
            
create_pivot()

