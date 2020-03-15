

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import sqlite3

conn = sqlite3.connect('../db.sqlite3')

def get_data_from_sqlite(table):
    query = "SELECT * FROM " + table
    data = pd.read_sql_query(query, conn)
    return data

# not efficient to write function to select only certain columns from suitable

FETCH_BOOK_QUERY = "SELECT `id`, `title`, `publisher`, `author`, `image`, `category_id`, `available` FROM `libraryapp_book` "

books = pd.read_sql_query(FETCH_BOOK_QUERY, conn)
# book_list = get_data_from_sqlite("libraryapp_book")

# rename book list dataframe columns
books = books.rename({'id':'book_id', 'title':'book_title', 'image':'book_image'}, axis=1)
print(books)
print(books.columns)

book_category = pd.read_sql_query("SELECT `id` as `category_id`, `title` as `category_title`, `image` as `category_image` FROM `libraryapp_bookcategory`", conn)

# book_category =
print(book_category)
print(book_category.columns)

# Merge book_list and book_category
book_data = pd.merge(books, book_category, on='category_id')
print(book_data)
print(book_data.columns)

ratings = pd.read_sql_query("SELECT `rating`, `book_id`, `user_id` FROM `libraryapp_bookrating`",conn)
# print(ratings.columns)

book_with_rating = pd.merge(book_data, ratings, on='book_id', how='left')
print(book_with_rating)
print(book_with_rating.columns)

book_mat = book_with_rating.pivot_table(index='user_id', columns='book_title', values='rating')
print(book_mat)

# find correlation between books
book_list_matrix = book_mat.fillna(0)
book_corr = np.corrcoef(book_list_matrix.T)
print(book_corr)

print(book_corr.shape)

# book_list = list(book_list_matrix)
book_titles = list(book_list_matrix.columns)
# book_titles = []
# for i in range(len(book_list)):
#     book_titles.append(book_list[i])

print(book_titles)

liked_book = 'DBA'
book_index = book_titles.index(liked_book)
print('Book index: %d' %book_index)

liked_book_corr = book_corr[book_index]
print(liked_book_corr)
similar_books = np.extract(liked_book_corr >= 0.1, book_titles)

print(similar_books)

blist = book_with_rating.loc[book_with_rating['user_id'] == 8]['book_title']
print(list(blist))

def get_recommendation(user_id):
    book_list = book_with_rating.loc[book_with_rating['user_id'] == user_id]['book_title']
    book_list = list(book_list)
    print(book_list)
    # get_recommendation_list(['DAA'])
    book_similarities = np.zeros(book_corr.shape[0])

    for book in book_list:
        # print(book)
        book_index = book_titles.index(book)
        # print(book_index)
        book_similarities += book_corr[book_index]
    book_preferences = []
    for i in range(len(book_titles)):
        book_preferences.append((book_titles[i],book_similarities[i]))

    return sorted(book_preferences, key= lambda x: x[1], reverse=True)


def get_recommendation_list(books_list):
    book_similarities = np.zeros(book_corr.shape[0])

    for book in books_list:
        # print(book)
        book_index = book_titles.index(book)
        # print(book_index)
        book_similarities[i] = book_corr[book_index]
    book_preferences = []
    for i in range(len(book_titles)):
        book_preferences.append((book_titles[i],book_similarities[i]))

    return sorted(book_preferences, key= lambda x: x[1], reverse=True)

print("recommendation")
print(get_recommendation(8))
