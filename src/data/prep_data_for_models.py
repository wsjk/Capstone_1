import os
import importlib.util
import pandas as pd
import numpy as np
import sys

current_file_path = os.path.abspath(os.path.join("__file__" ,"../../.."))
tools_path = os.path.abspath(os.path.join(current_file_path, 'src', 'tools'))
save_path = os.path.abspath(os.path.join(current_file_path, 'notebooks'))
sys.path.append(os.path.abspath(os.path.join(tools_path)))
import eda_tools as eda

def get_data():
    import_data_path = os.path.join(current_file_path,'src','data')
    spec = importlib.util.spec_from_file_location("import_clean_csv", os.path.join(import_data_path,"import_clean_data.py"))
    import_data = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(import_data)
    data = import_data.import_clean_csv(current_file_path)
    return data

def get_movies(data):
    # create dataframes from cleaned data
    movies = data['tmdb_movie_main'].set_index(['movie_id', 'title'])
    movies['release_date'] = pd.to_datetime(movies['release_date'])
    movies['net'] = movies['revenue'] - movies['budget']
    return movies

#get data for actor filmography
def get_actor_credits(data, movies, save_csv):
    cast = data['tmdb_cast_credit']
    first_billing = cast.groupby(['movie_id', 'title'], as_index=False).first()
    first_billing.set_index(['movie_id', 'title'], inplace=True)
    movies_with_actors = movies.merge(first_billing, left_index=True, right_index=True)
    
    gender = pd.get_dummies(movies_with_actors['gender'])
    gender.columns = ['unknown', 'female','male']
    movies_with_actors = movies_with_actors.merge(gender, left_index=True, right_index=True)
    actors_df = movies_with_actors.reset_index()
    binned_actors = eda.get_rolling_history(actors_df, 'name', new_col='credits', func=len, func_col='title')
    binned_actors = eda.get_rolling_history(actors_df, 'name', new_col='net_to_date', func=sum, func_col='net')
    new_df = binned_actors[['movie_id', 'title', 'name', 'unknown','male','female', 'credits', 'net_to_date']]
    if save_csv:
        new_df.to_csv(os.path.abspath(os.path.join(save_path,'Actor_credits.csv')), index=False)

    return new_df

# get filmography of crew
def get_crew_credits(data, movies, save_csv):
    crew = data['tmdb_crew_credit'].set_index(['movie_id', 'title'])
    movies_with_crew = movies.merge(crew, left_index=True, right_index=True)
    crew = crew.reset_index()

    dfs = {}
    for job in ['Producer', 'Writer', 'Director']:
        crew_dict = crew[crew.job == job].groupby(['movie_id', 'title'], as_index=False).first()
        df = pd.merge(crew_dict, movies.reset_index(), on=['movie_id','title']).sort_values('name')
        binned_crew = eda.get_rolling_history(df, 'name', new_col='credits', func=len, func_col='title')
        binned_crew = eda.get_rolling_history(df, 'name', new_col='net_to_date', func=sum, func_col='net')
        new_df = binned_crew[['movie_id','title','name','credits','net_to_date']]
        if save_csv:
        	new_df.to_csv(os.path.abspath(os.path.join(save_path, job + '_credits.csv')), index=False)
        dfs[job] = new_df
    return dfs

def get_genre_data(data,movies,save_csv):
    genres = data['tmdb_movie_genres'].set_index(['movie_id', 'title'])
    genres = genres.drop('id',axis=1)
    genre_count = genres.reset_index().groupby(['movie_id', 'title']).count()
    genre_count.columns = ['genre_count']
    genre_dummies = pd.get_dummies(genres['name']).reset_index().groupby(['movie_id', 'title']).sum()
    genre_data = genre_dummies.merge(genre_count, left_index=True, right_index=True)
    if save_csv:
        genre_data.to_csv('Genres.csv')
    return genre_data

if __name__ == "__main__":
    data = get_data()
    movies = get_movies(data)
    #crew_dfs = get_crew_credits(data, movies, save_csv=True)
    actor_df = get_actor_credits(data, movies, save_csv=True)
    #genre_df = get_genre_data(data, movies, save_csv=True)


	