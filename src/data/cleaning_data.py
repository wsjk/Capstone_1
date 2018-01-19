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

#import tqdm
from tqdm import tqdm

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

def get_movie_data(missing_movies, data_type, fpath):
    ### Find missing budget, revenue data 

    #manually correct dataframe values
    missing_movies['movie_url'] = np.nan    

    # obtain correct budget/revenue data from the-numbers.com
    csv_file_path = os.path.join(interim_data_path,'found_' + data_type + '.csv')
    with tqdm(total=len(missing_movies)) as pbar:
        for row in missing_movies.iloc[38:].iterrows():
            found_movie = row_scrape_movie_data(row[1], data_type)
            found_movie = pd.DataFrame(found_movie).transpose()
            if os.path.exists(csv_file_path):
                found_movie.to_csv(csv_file_path, mode='a', header=False, index=False)
            else:
                found_movie.to_csv(csv_file_path, index=False)
            pbar.update()
    return found_movies


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

    #zero out budget for movies with incorrect data so that they will be considered in webscraper section
    wrong_budgets = [23827, 2667, 985, 692]
    for movie_id in wrong_budgets:
        title_mask = tmdb_movie_df.movie_id == movie_id
        tmdb_movie_df.loc[title_mask,'budget'] = 0

    # fixing titles for a handful of movies
    wrong_titles = {9396: "Crocodile Dundee 2", 9644: "Loaded Weapon 1", 1011: "Richie Rich", 11658: "Tae Guik Gi: The Brotherhood of War", 
        367961: "Savva. Serdtse voyna", 25353: 'La véritable histoire du Chat Botté', 290864: 'Kung Fu Killer', 
        30379: 'Megiddo: Omega Code 2', 46435: 'Topsy Turvy', 12154: '3 Men and a Baby', 91586: 'Insidious Chapter 2', 85000: 'Texas Chainsaw Massacre',
        16340: 'Rugrats in Paris'}

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
    if not os.path.exists(os.path.join(interim_data_path,'found_financial.csv')):
        #some movies have $0 for revenue and budget
        missing_financial = tmdb_movie_df_no_json[
                            (tmdb_movie_df_no_json.budget < 1000) | (tmdb_movie_df_no_json.revenue < 1000)
                            ].reindex(columns=['movie_id', 'title', 'budget', 'revenue', 'release_date'])

        missing_financial.to_csv(os.path.join(interim_data_path,'test.csv'))
        missing_financial = missing_financial[missing_financial.budget > 0].sort_values('budget')
        
        #fill in incorrect budget and revenue data via web scraper
        found_financial = get_movie_data(missing_financial, 'financial', interim_data_path)

    else:
        found_financial = pd.read_csv(os.path.join(interim_data_path,'found_financial.csv'))

    for row in found_financial.iterrows():
        financial_mask = tmdb_movie_df_no_json.movie_id == row[1].movie_id
        tmdb_movie_df_no_json.loc[financial_mask,'budget'] = row[1].budget
        tmdb_movie_df_no_json.loc[financial_mask,'revenue'] = row[1].revenue

    # check if webscraper data already exists
    if not os.path.exists(os.path.join(interim_data_path,'found_runtime.csv')):
        #some movies have $0 for revenue and budget
        missing_runtime = tmdb_movie_df_no_json[tmdb_movie_df_no_json.runtime < 1].reindex(columns=['movie_id', 'title', 'release_date','runtime'])
        #fill in incorrect budget and revenue data via web scraper
        scraped_movies = get_movie_data(missing_runtime, 'runtime', interim_data_path)
        
        #save webscraper as csv
        #found_runtime.to_csv(os.path.join(interim_data_path,'found_runtime.csv'), index=False)
    else:
        found_runtime = pd.read_csv(os.path.join(interim_data_path,'found_runtime.csv'))

    for row in found_runtime.iterrows():
        runtime_mask = tmdb_movie_df_no_json.movie_id == row[1].movie_id
        tmdb_movie_df_no_json.loc[runtime_mask,'runtime'] = row[1].runtime

    #remove movies where runtime data could not be found
    final_movie_df = tmdb_movie_df_no_json.dropna(subset=['budget', 'revenue', 'runtime'],how='any')
    final_movie_df = final_movie_df[final_movie_df['runtime'] > 0]
    final_movie_df = final_movie_df[(final_movie_df.budget > 1000) & (final_movie_df.revenue > 500)]


    #if some budget & revenue data is still be missing, filter out those movies
    final_movie_df.to_csv(os.path.join(ext_data_path,'tmdb_movie_main_final.csv'), index=False)

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
        tmdb_movie_dfs[i].to_csv(os.path.join(ext_data_path,'tmdb_movie_' + i + '_final.csv'), index=True)

if __name__ == "__main__":

    current_file_path, raw_data_path, interim_data_path, ext_data_path = get_data_paths()
    data_files = get_data_files(raw_data_path)
    print("cleaning movies")
    clean_movies_data(data_files[1], interim_data_path, ext_data_path)
    print("cleaning credits")
    clean_credits_data(data_files[0], ext_data_path)
