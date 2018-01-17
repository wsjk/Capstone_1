The movie data is obtained from Kaggle's TMDB dataset: https://www.kaggle.com/tmdb/tmdb-movie-metadata/data. The link contains a zip file that contains two csv files: tmdb_credits.csv, tmdb_movies.csv.
The "tmdb_credits.csv" file contains cast and crew data including names, character names, job title, and the order of billed actors. The "tmdb_movies.csv" file contains all other information regarding each movie including title, budget, revenue, language, popularity, runtime, vote data, and release date. 

The "cleaning_data.py" script contains the code to conduct the initial cleaning of the raw csv files. After cleaning the data from the raw csv files, the data was then saved as files with the suffix "*_cleaned.csv". The "cleaning_data.py" script also flattens any nested JSON data found in the raw csv files and creates separate csv files following a process similar to database normalization. Each separate csv file can be considered a table within a relational database with a foreign key linking all tables.


For the "tmdb_movies.csv" file, some basic cleaning operations were used:
-- 'original_title' and 'homepage' columns were removed. 
-- 'id' column was renamed to 'movie_id'
-- 'movie_id' and 'title' columns are used for a multi-level index. The 'movie_id' index is considered the foreign key that can be used to link any table created from TMDB dataset.

The "tmdb_movies.csv" file also contained nested JSON data (i.e., list of dictionaries). The JSON and non-JSON data columns were separated to facilitate the process of handling JSON data. The columns with nested JSON data: 'genres', 'keywords', 'production_companies', 'production_countries', 'spoken_languages'. Each column of JSON data was flattened and combined with the same ['movie_id', 'title'] multi-level index. The resulting table from flattening the JSON data was then saved in separate csv files (i.e., tables).  

There were a few issues regarding special characters in movie titles and missing data for release dates. Those instances were manually corrected. 

Although no values were missing, there were numerous cases where a movie had $0 in budget and revenue. A web scraper (see movie_scraper.py) was developed in Python to obtain data from searching the database in www.the-numbers.com. The search results contained links for a movie webpage that contained budget and revenue data. The budget was referred to as "Production Budget" and the revenue was determined by taking the max value of Domestic, International, and Worldwide Box Office revenue due to the possibility that some movies only had Domestic or International revenue data. In some cases, the movie title from TMDB did not match the database in www.the-numbers.com and IMDB was cross referenced to find other possible titles. As this process was highly labor intensive, alternative titles were found for only a handful of movies as the dataset was already of significant size. For movies that returned several results from a title search, the correct result was determined based on release date. It was observed that movies with the same title would not be released within several years of each other. If the scraper was unable to find budget and revenue information on the website, the movie was deleted from the dataset. 

For the "tmdb_credits.csv" file:
-- 'movie_id' and 'title' columns are used for a multi-level index. The 'movie_id' index is considered the foreign key that can be used to link any table created from TMDB dataset.
-- columns with nested JSON data (i.e., list of dictionaries) were separated from non-JSON columns. The columns with nested JSON data: 'cast', 'crew'. Each column of JSON data was flattened and combined with the same ['movie_id', 'title'] multi-level index. The resulting table from flattening the JSON data was then saved in separate csv files (i.e., tables).  
-- no issues regarding special characters or missing data as the data was obtained from Kaggle


The 'budget' data in "tmdb_movies.csv" represents wordwide box-office gross and matches the data from http://www.boxofficemojo.com/alltime/world/.
The 'revenue' data matches cost estimates in https://en.wikipedia.org/wiki/List_of_most_expensive_films and is not adjusted for inflation.
No obvious outliers were discovered after investigating the data.
