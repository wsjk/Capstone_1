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

from movie_scraper import row_scrape_movie_data

import tqdm

def get_data_paths():
    current_file_path=os.path.abspath(os.path.join("__file__" ,"../../.."))

    #location of raw csv data from Kaggle
    raw_data_path = os.path.join(current_file_path,'data','raw')


    #location of raw csv data from Kaggle
    interim_data_path = os.path.join(current_file_path,'data','interim')

    #location to save cleaned csv files
    ext_data_path = os.path.join(current_file_path,'data','processed')

    return current_file_path, raw_data_path, interim_data_path, ext_data_path

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
        dict_of_dfs[col] = new_df.set_index(keys=['movie_id', 'title'])
    return dict_of_dfs

def get_budget_revenue_data(missing_movies):
    ### Find missing budget, revenue data 

    #manually correct dataframe values
    missing_movies['movie_url'] = np.nan    

    # obtain correct budget/revenue data from the-numbers.com
    tqdm.tqdm.pandas()
    missing_movies = missing_movies.progress_apply(row_scrape_movie_data, axis=1)
    found_movies = missing_movies.dropna(axis=0, how='any')


def clean_credits_data(credits_data_file, ext_data_path):
    tmdb_credit_df = pd.read_csv(credits_data_file, header=0)

    #columns with JSON data
    json_columns = ['cast','crew'] #JSON data columns

    tmdb_credit_df = tmdb_credit_df.assign(cast=tmdb_credit_df.cast.apply(json.loads), crew=tmdb_credit_df.crew.apply(json.loads))
    tmdb_credit_dict = tmdb_credit_df.to_dict('r')
    #multi-index labels and foreign key for other TMDB tables
    meta_list = ['movie_id', 'title']
    tmdb_credit_dfs = normalize_dfs(tmdb_credit_dict, json_columns, meta_list)
    
    #save clean data in new csv files
    for i in tmdb_credit_dfs.keys():
        tmdb_credit_dfs[i].to_csv(os.path.join(ext_data_path,'tmdb_' + i + '_credit_final.csv'), index=True)


    ##################################################
    ############ Clean TMDB Movie dataset ############
    ##################################################

def clean_movies_data(movie_data_file, interim_data_path, ext_data_path):
    #TMDB: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data

    #columns with JSON data
    json_columns = ['genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages']
    #multi-index labels and foreign key for other TMDB tables
    meta_list = ['movie_id', 'title']

    tmdb_movie_df = pd.read_csv(movie_data_file, header=0)
    tmdb_movie_df = tmdb_movie_df.rename(columns={'id':meta_list[0]})

    #replace missing date for one movie
    date_mask = tmdb_movie_df.movie_id == 380097
    tmdb_movie_df.loc[date_mask,'release_date'] = dt(2014,12,31)

    # fixing titles for a handful of movies
    wrong_titles = {9396: "Crocodile Dundee 2", 9644: "Loaded Weapon 1", 1011: "Richie Rich", 11658: "Tae Guik Gi: The Brotherhood of War", 
        367961: "Savva. Serdtse voyna", 25353: 'La véritable histoire du Chat Botté', 290864: 'Kung Fu Killer', 
        30379: 'Megiddo: Omega Code 2', 46435: 'Topsy Turvy', 12154: '3 Men and a Baby', 91586: 'Insidious Chapter 2'}

    for movie_id, title in wrong_titles.items():
        title_mask = tmdb_movie_df.movie_id == movie_id
        tmdb_movie_df.loc[title_mask,'title'] = title

    print('cleaning non json')
    clean_no_json(tmdb_movie_df, meta_list, json_columns, interim_data_path, ext_data_path)
    print('cleaning json')
    clean_json(tmdb_movie_df, meta_list, json_columns, ext_data_path)

    
def clean_no_json(tmdb_movie_df, meta_list, json_columns, interim_data_path, ext_data_path):

    #remove JSON columns from dataframe and clean data
    tmdb_movie_df_no_json = tmdb_movie_df.drop(json_columns + ['original_title', 'homepage'], axis=1)
    #tmdb_movie_df_no_json = tmdb_movie_df_no_json.set_index(meta_list)
    tmdb_movie_df_no_json.release_date = pd.to_datetime(tmdb_movie_df_no_json.release_date, infer_datetime_format=True)

    #separate data without JSON data to different file
    #movie_id and title can be used as primary key
    tmdb_movie_df_no_json.to_csv(os.path.join(interim_data_path,'tmdb_movie_main_cleaned.csv'), index_label=meta_list)

    # check if webscraper data already exists
    if not os.path.exists(os.path.join(interim_data_path,'found_movies.csv')):
        #some movies have $0 for revenue and budget
        missing_movies = tmdb_movie_df_no_json[(tmdb_movie_df_no_json.budget < 1) | (tmdb_movie_df_no_json.revenue < 1)].reindex(columns=['movie_id', 'title', 'budget', 'revenue', 'release_date'])
        #fill in incorrect budget and revenue data via web scraper
        scraped_movies = get_budget_revenue_data(missing_movies)

        #only keep movies that the scraper could find data for
        found_movies = scraped_movies[(scraped_movies.budget > 1)|(scraped_movies.revenue > 1)]
        
        #save webscraper as csv
        found_movies.to_csv(os.path.join(interim_data_path,'found_movies.csv'))
    else:
        found_movies = pd.read_csv(os.path.join(interim_data_path,'found_movies.csv'))

    #replace incorrect $0 values for budget & revenue with correct data from webscraper
    merged = tmdb_movie_df_no_json.merge(right=found_movies, how='left', on=['movie_id', 'title'])
    merged['budget'] = np.max(merged[['budget_x', 'budget_y']], axis=1)
    merged['revenue'] = np.max(merged[['revenue_x', 'revenue_y']], axis=1)

    #fill in nan in release_date from left join with early date, and np.max() to choose the correct release_date
    merged['release_date_x'] = pd.to_datetime(merged['release_date_x'],infer_datetime_format=True)
    merged['release_date_y'] = pd.to_datetime(merged['release_date_x'],infer_datetime_format=True)
    merged['release_date_x'].fillna(dt(1900,1,1), inplace=True)
    merged['release_date_y'].fillna(dt(1900,1,1), inplace=True)
    merged['release_date'] = np.max(merged[['release_date_x', 'release_date_y']], axis=1)


    merged = merged.drop(labels=['budget_x', 'budget_y','revenue_x', 'revenue_y', 'release_date_x', 'release_date_y', 'movie_url'], axis=1)
    #if some budget & revenue data is still be missing, filter out those movies
    final_movie_df = merged[(merged.budget > 1) & (merged.revenue > 1)]
    final_movie_df.to_csv(os.path.join(ext_data_path,'tmdb_movie_main_final.csv'))

def clean_json(tmdb_movie_df, meta_list, json_columns, ext_data_path):
    tmdb_movie_df_rest = tmdb_movie_df[['movie_id','title'] + json_columns]

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
        tmdb_movie_dfs[i].to_csv(os.path.join(ext_data_path,'tmdb_movie_' + i + '_final.csv'))

if __name__ == "__main__":

    current_file_path, raw_data_path, interim_data_path, ext_data_path = get_data_paths()
    data_files = get_data_files(raw_data_path)
    print("cleaning credits")
    clean_credits_data(data_files[0], ext_data_path)
    print("cleaning movies")
    clean_movies_data(data_files[1], interim_data_path, ext_data_path)
