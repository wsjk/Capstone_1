import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import ast
from datetime import datetime as dt
from pandas.io.json import json_normalize
from pandas.io import json

def get_data_files(raw_data_path):
    #list of raw csv files to clean
    data_files = glob.glob(os.path.join(raw_data_path, '*.csv'), recursive=False)

    return data_files

#takes original dataframe that contains columns with json data
#and flattens json data and separates into individual dataframes
#stores separated dataframes in dictionary 
#https://stackoverflow.com/questions/48177934/flatten-or-unpack-list-of-nested-dicts-in-dataframe/48178127?noredirect=1#comment83339044_48178127
def normalize_dfs(df_dict, json_columns, meta_list):
    dict_of_dfs = {}
    for col in json_columns:
        new_df = json_normalize(df_dict, meta=meta_list,record_path = [col])
        dict_of_dfs[col] = new_df.set_index(meta_list)
    return dict_of_dfs


def clean_credits_data(credits_data_file, ext_data_path):
    tmdb_credit_df = pd.read_csv(credits_data_file, ext_data_path)

    #columns with JSON data
    json_columns = ['cast','crew'] #JSON data columns


    tmdb_credit_df = tmdb_credit_df.assign(cast=tmdb_credit_df.cast.apply(json.loads), crew=tmdb_credit_df.crew.apply(json.loads))
    tmdb_credit_dict = tmdb_credit_df.to_dict('r') 

    #multi-index labels and foreign key for other TMDB tables
    meta_list = ['movie_id', 'title']
    tmdb_credit_dfs = normalize_dfs(tmdb_credit_dict, json_columns, meta_list)


    #save clean data in new csv files
    for i in tmdb_credit_dfs.keys():
        tmdb_credit_dfs[i].to_csv(os.path.join(ext_data_path,'tmdb_' + i + '_credit_cleaned.csv'), index_label=meta_list)


    ##################################################
    ############ Clean TMDB Movie dataset ############
    ##################################################

def clean_movies_data(movie_data_file, ext_data_path):
    #TMDB: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data

    tmdb_movie_df = pd.read_csv(movie_data_file, header=0)

    #columns with JSON data
    json_columns = ['genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages']

    #multi-index labels and foreign key for other TMDB tables
    meta_list = ['movie_id', 'title']
    tmdb_movie_df_no_json = tmdb_movie_df.drop(json_columns + ['original_title', 'homepage'], axis=1)
    tmdb_movie_df_no_json = tmdb_movie_df_no_json.rename(columns={'id':meta_list[0]})
    tmdb_movie_df_no_json = tmdb_movie_df_no_json.set_index(meta_list)
    tmdb_movie_df_no_json.release_date = pd.to_datetime(tmdb_movie_df_no_json.release_date, infer_datetime_format=True)


    #replace missing date for one movie
    tmdb_movie_df_no_json[tmdb_movie_df_no_json.release_date.isnull()].release_date = dt(2014,12,31)

    #find all rows with 0 for revenue or budget
    missing_movies = tmdb_movie_df_no_json[(tmdb_movie_df_no_json.budget < 1) | (tmdb_movie_df_no_json.revenue < 1)].reindex(columns=['release_date'])
    missing_movies.sort_index(inplace=True)
    missing_movies.reset_index(level=[0,1], inplace=True)

    # obtain correct budget/revenue data from the-numbers.com
    missing_movies_dict = scrape_movie_data(missing_movies)

    #replace missing budget/revenue values in tmdb_df_no_json dataframe
    ###########
    # INSERT CODE
    ############
    #########





    #separate data without JSON data to different file
    #'movie_id' can be used as primary key
    tmdb_movie_df_no_json.to_csv(os.path.join(ext_data_path,'tmdb_movie_main_cleaned.csv'), index_label=meta_list)

    tmdb_movie_df_rest = tmdb_movie_df[['id','title'] + json_columns]
    tmdb_movie_df_rest = tmdb_movie_df_rest.rename(columns={'id':meta_list[0]})

    tmdb_movie_dicts = {}
    for i in json_columns:
        small_df = tmdb_movie_df_rest[ meta_list + [i]]
        small_df = small_df.assign(new=small_df[i].apply(json.loads))
        small_df.drop([i],axis=1, inplace=True)
        small_df = small_df.rename(columns={'new':i})
        tmdb_movie_dicts[i] = small_df.to_dict('r') 

    tmdb_movie_dfs = {}
    for i in json_columns:
        df = normalize_dfs(tmdb_movie_dicts[i], [i], meta_list)
        tmdb_movie_dfs[i] = df[i]


    for i in tmdb_movie_dfs.keys():
        tmdb_movie_dfs[i].to_csv(os.path.join(ext_data_path,'tmdb_movie_' + i + '_cleaned.csv'), index_label=meta_list)

if __name__ == "__main__":
    current_file_path=os.path.abspath(os.path.join("__file__" ,"../.."))

    #location of raw csv data from Kaggle
    raw_data_path = os.path.join(current_file_path,'raw')

    #location to save cleaned csv files
    ext_data_path = os.path.join(current_file_path,'processed')

    data_files = get_data_files(raw_data_path)
    clean_credit_data(data_files[0], ext_data_path)
    clean_movie_data(data_files[1], ext_data_path)
