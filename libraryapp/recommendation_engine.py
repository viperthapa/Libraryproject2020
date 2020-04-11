import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# import sqlite3

# for django project use this as connection to sqlite db
from django.db import connection as conn


class RecommendationiEngine():
    """docstring for RecommendationiEngine."""

    def __init__(self):
        # conn = sqlite3.connect('../db.sqlite3')

        FETCH_BOOK_QUERY = "SELECT `id`, `title`, `publisher`, `author`, `image`, `category_id`, `available` FROM `libraryapp_book` "

        self.books = pd.read_sql_query(FETCH_BOOK_QUERY, conn)
        # book_list = get_data_from_sqlite("libraryapp_book")

        # rename book list dataframe columns
        self.books = self.books.rename(
            {'id': 'book_id', 'title': 'book_title', 'image': 'book_image'}, axis=1)

        self.books_category = pd.read_sql_query(
            "SELECT `id` as `category_id`, `title` as `category_title`, `image` as `category_image` FROM `libraryapp_bookcategory`", conn)

        # Merge book_list and book_category
        self.books_data = pd.merge(
            self.books, self.books_category, on='category_id')

        self.ratings = pd.read_sql_query(
            "SELECT `rating`, `book_id`, `user_id` FROM `libraryapp_bookrating`", conn)
        # print(ratings.columns)

        self.books_with_rating = pd.merge(
            self.books_data, self.ratings, on='book_id')

        self.books_mat = self.books_with_rating.pivot_table(
            index='user_id', columns='book_title', values='rating')

        # find correlation between books
        self.book_list_matrix = self.books_mat.fillna(0)
        self.book_corr = np.corrcoef(self.book_list_matrix.T)
        print("BOOK CORR: ", self.book_corr)

        self.book_titles = list(self.book_list_matrix)
        # book_titles = []
        # for i in range(len(book_list_matrix)):
        #     book_titles.append(book_list[i])

    def get_data_from_sqlite(self, table):
        query = "SELECT * FROM " + table
        data = pd.read_sql_query(query, conn)
        return data

    def get_recommendation(self, user_id, corr_limit):
        user_rated_books = self.books_with_rating.loc[self.books_with_rating['user_id']
                                                      == user_id]['book_title']
        books_list = list(user_rated_books)
        print('********************')
        print('User Rated Book List: ', books_list)
        # self.get_recommendation_list(book_list)
        book_similarities = np.zeros(self.book_corr.shape[0])

        book_preferences = []
        for book in books_list:
            # print(book)
            book_index = self.book_titles.index(book)
            # print(book_index)
            book_similarities += self.book_corr[book_index]

        for i in range(len(self.book_titles)):
            if book_similarities[i] > corr_limit and self.book_titles[i] not in books_list:
                # pass book title
                book_preferences.append(self.book_titles[i])

        # return sorted(book_preferences, key= lambda x: x[1], reverse=True)
        return book_preferences

    def get_recommendation_from_category(self, books_list, corr_limit):

        book_similarities = np.zeros(self.book_corr.shape[0])

        # if (len(books_list) == 1):
        #     book_index = self.book_titles.index(books_list[0])
        #     book_similarities += self.book_corr[book_index]
        #     book_preferences = []
        #     for i in range(len(self.book_titles)):
        #         if book_similarities > corr_limit:
        #             book_preferences.append(self.book_titles[i])
        #     return book_preferences

        for book in books_list:
            # print(book)
            book_index = self.book_titles.index(book)
            # print(book_index)
            book_similarities += self.book_corr[book_index]
        book_preferences = []
        for i in range(len(self.book_titles)):
            if book_similarities[i] > corr_limit:
                book_preferences.append(self.book_titles[i])
            # book_preferences.append((self.book_titles[i],book_similarities[i])

        return book_preferences
        # return sorted(book_preferences, key= lambda x: x[1], reverse=True)
