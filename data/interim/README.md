The movie data is obtained from Kaggle's TMDB dataset: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data. The link contains a zip file that contains two csv files: tmdb_credits.csv, tmdb_movies.csv.
The "tmdb_credits.csv" file contains cast and crew data including names, character names, job title, and the order of billed actors. The "tmdb_movies.csv" file contains all other information regarding each movie including title, budget, revenue, language, popularity, runtime, vote data, and release date. 

The "cleaning_data.py" script contains the code to conduct the initial cleaning of the raw csv files. After cleaning the data from the raw csv files, the data was then saved as files with the suffix "*_cleaned.csv". The "cleaning_data.py" script also flattens any nested JSON data found in the raw csv files and creates separate csv files following a process similar to database normalization. Each separate csv file can be considered a table within a relational database with a foreign key linking all tables.


For the "tmdb_movies.csv" file:
-- 'original_title' and 'homepage' columns were removed. 
-- 'id' column was renamed to 'movie_id'
-- 'movie_id' and 'title' columns are used for a multi-level index. The 'movie_id' index is considered the foreign key that can be used to link any table created from TMDB dataset.
-- columns with nested JSON data (i.e., list of dictionaries) were separated from non-JSON columns. The columns with nested JSON data: 'genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages'. Each column of JSON data was flattened and combined with the same ['movie_id', 'title'] multi-level index. The resulting table from flattening the JSON data was then saved in separate csv files (i.e., tables).  
-- not many issues regarding special characters or missing data as the data was obtained from Kaggle
-- the 'release_date' column is in a format that can be easily interpreted by pandas' read_csv method by setting infer_datetime_format=True

For the "tmdb_credits.csv" file:
-- 'movie_id' and 'title' columns are used for a multi-level index. The 'movie_id' index is considered the foreign key that can be used to link any table created from TMDB dataset.
-- columns with nested JSON data (i.e., list of dictionaries) were separated from non-JSON columns. The columns with nested JSON data: 'cast', 'crew'. Each column of JSON data was flattened and combined with the same ['movie_id', 'title'] multi-level index. The resulting table from flattening the JSON data was then saved in separate csv files (i.e., tables).  
-- not many issues regarding special characters or missing data as the data was obtained from Kaggle


The 'budget' data in "tmdb_movies.csv" represents wordwide box-office gross and matches the data from http://www.boxofficemojo.com/alltime/world/.
The 'revenue' data matches cost estimates in https://en.wikipedia.org/wiki/List_of_most_expensive_films and is not adjusted for inflation.
No obvious outliers were discovered after investigating the data. There were some missing values, but were not considered of consequence as they were only an issue for films on lower end of spectrum for budget and revenue.
