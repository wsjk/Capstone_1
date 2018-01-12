
#
import pandas as pd
import numpy as np
import glob
import os
import csv
import re
import ast
from pandas.io.json import json_normalize
from pandas.io import json

current_file_path = os.path.abspath(os.path.join("__file__" ,"../.."))

#location of raw csv data from Kaggle
raw_data_path = os.path.join(current_file_path,'raw')

#location to save cleaned csv files
ext_data_path = os.path.join(current_file_path,'external')

#list of raw csv files to clean
data_files = glob.glob(os.path.join(raw_data_path, '*.csv'), recursive=False)


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


if __name__ == "__main__":

    ############################################
    ############ Clean IMDB dataset ############
    ############################################

    #IMDB: https://www.kaggle.com/orgesleka/imdbmovies/data

    # clean csv data from Kaggle's IMDB dataset
    ###imdb_df = pd.read_csv(data_files[0], header=0, escapechar='\\')
    #imdb_df.head()

    #removes unnecessary data
    ###imdb_movie_df = imdb_df[imdb_df.type == 'video.movie']
    ###imdb_movie_df = imdb_movie_df.drop(['wordsInTitle'],axis=1)

    #save cleaned IMDB data
    ###imdb_movie_df.to_csv(os.path.join(ext_data_path,'imdb_cleaned.csv'),escapechar='\\', index=False)



    ####################################################
    ############ Clean TMDB Credits dataset ############
    ####################################################

    #TMDB: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data

    tmdb_credit_df = pd.read_csv(data_files[1])

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

    #TMDB: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data

    tmdb_movie_df = pd.read_csv(data_files[-1], header=0)

    print(tmdb_movie_df.info())

    #columns with JSON data
    json_columns = ['genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages']

    #multi-index labels and foreign key for other TMDB tables
    meta_list = ['movie_id', 'title']
    tmdb_movie_df_no_json = tmdb_movie_df.drop(json_columns + ['original_title'], axis=1)
    tmdb_movie_df_no_json = tmdb_movie_df_no_json.rename(columns={'id':meta_list[0]})
    tmdb_movie_df_no_json = tmdb_movie_df_no_json.set_index(meta_list)

    #separate data without JSON data to different file
    #'movie_id' can be used as primary key
    tmdb_movie_df_no_json.to_csv(os.path.join(ext_data_path,'tmdb_movie_main_cleaned.csv'), index_label=meta_list)
    print(tmdb_movie_df_no_json.info())

    tmdb_movie_df_rest = tmdb_movie_df[['id','title'] + json_columns]
    tmdb_movie_df_rest = tmdb_movie_df_rest.rename(columns={'id':meta_list[0]})
    
    print(tmdb_movie_df_rest.info())

    tmdb_movie_dicts = {}
    for i in json_columns:
        small_df = tmdb_movie_df_rest[ meta_list + [i]]
        small_df = small_df.assign(new=small_df[i].apply(json.loads))
        small_df = small_df.rename(columns={'new':i})
        tmdb_movie_dicts[i] = small_df.to_dict('r') 

    tmdb_movie_dfs = {}
    for i in json_columns:
        df = normalize_dfs(tmdb_movie_dicts[i], [i], meta_list)
        tmdb_movie_dfs[i] = df[i]


    for i in tmdb_movie_dfs.keys():
        tmdb_movie_dfs[i].to_csv(os.path.join(ext_data_path,'tmdb_movie_' + i + '_cleaned.csv'), index_label=meta_list)


