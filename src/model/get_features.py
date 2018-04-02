import os
import glob
import importlib.util
import pandas as pd
import datetime as dt
from functools import reduce
import numpy as np
import sys
import datetime as dt
import calendar

current_file_path = os.path.abspath(os.path.join("__file__" ,"../.."))
if current_file_path[-3:] == 'src':
	current_file_path =  os.path.abspath(os.path.join("__file__" ,"../../.."))

tools_path = os.path.abspath(os.path.join(current_file_path, 'src', 'tools'))
import_data_path = os.path.join(current_file_path,'src','data')

sys.path.insert(0, tools_path)
import eda_tools as eda

sys.path.insert(0, import_data_path)
import import_clean_data as import_data
os.chdir(import_data_path)

def get_features(save_csv=True):
	data = import_data.import_clean_csv(current_file_path)

	# create dataframes from cleaned data
	movies = data['tmdb_movie_main'].set_index(['movie_id', 'title'])
	movies['release_date'] = pd.to_datetime(movies['release_date'])
	movies.drop('tagline', axis=1, inplace=True)

	#create column for target variable
	movies['net'] = movies.revenue - movies.budget
	movies['net_pct'] = movies.revenue.divide(movies.budget) - 1
	movies['target'] = movies['net'].apply(lambda x: 1 if x > 0 else -1)

	#drop unwanted columns
	movies = movies.drop(['original_language', 'overview', 'popularity', 'revenue','status','vote_average','vote_count','net','net_pct'],axis=1)

	#extract day, month, and day of week data from release_date (datetime type)
	movies = eda.split_release_date(movies)
	
	release_month = pd.get_dummies(movies['release_month'])
	release_dow = pd.get_dummies(movies['release_dow'])
	release_month.columns = [calendar.month_name[i] for i in release_month.columns]
	release_dow.columns = [calendar.day_name[i] for i in release_dow.columns]
	release_date_dfs = [release_month, release_dow]
	movies = movies.drop(['release_date','release_month', 'release_dow'], axis=1)

	#combine release date data into df
	combined_release_dates = reduce(
		lambda left,right: pd.merge(
			left,right,left_index=True, right_index=True, how='left'),
		 release_date_dfs)

	os.chdir(os.path.abspath(os.path.join(current_file_path, 'notebooks')))
	files = glob.glob('*.csv')

	#get data for other features into dict of dfs
	other_data_dfs = {}
	for file in ['Actor_credits.csv', 'Director_credits.csv']:
	    key = file.split('.')[0].lower()
	    prefix = key.split('_')[0]
	    other_data_dfs[key] = \
	        pd.read_csv(file).set_index(['movie_id','title']).rename(
	                                                                columns={
	                                                                    'name': prefix + '_name', 
	                                                                    'gender': prefix + '_gender',
	                                                                     'credits': prefix + '_credits', 
	                                                                     'net_to_date': prefix + '_net_to_date'
	                                                                    }
	                                                                )
	file = 'Genres.csv'
	key = file.split('.')[0].lower()
	other_data_dfs[key] = pd.read_csv(file).set_index(['movie_id','title'])
	other_data_dfs['genres'].columns = [i.lower() for i in other_data_dfs['genres'].columns]

	genre_cols = list(other_data_dfs['genres'].columns)

	other_data_dfs['languages'] = pd.read_csv('Languages.csv').set_index(['movie_id', 'title'])

	combined_other_data = reduce(
		lambda left,right: pd.merge(
			left,right,left_index=True, right_index=True, how='outer'
			), [i for _, i in other_data_dfs.items()])

	combined_other_data.drop(['actor_name','director_name'], axis=1,inplace=True)

	#merge othe feature dfs with main movies df
	total_df = pd.merge(movies, combined_other_data, left_index=True, right_index=True, how='outer')

	total_df = pd.merge(total_df, combined_release_dates, left_index=True, right_index=True, how='inner')

	final_df = total_df.dropna()
	if save_csv:
		final_df.to_csv('features.csv')

	return final_df

if __name__ == "__main__":
	df = get_features()
	df.to_csv('features.csv')

