# The Problem
The film industry is already a billion dollar industry and steadily growing. The global box office revenue is forecast to increase 50 billion U.S. dollars in 2020. The film "Avatar" is the current record holder for worldwide box office revenue is $2.8 billion with an estimated budget of $237 million. The risk, however, can be as great as the reward. One of the biggest box office bombs is "13th Warrior" which claimed an estimated loss of $129 million. Film studio executives and investors are constantly inundated with sales pitches for movies. How can anyone navigate the risk and choose a profitable film to finance? What does the next box office hit look like?


# The Client
Film studios and investors who are considering financing a film.


# The Dataset
The movie data is obtained from [Kaggle's TMDB dataset](https://www.kaggle.com/tmdb/tmdb-movie-metadata/data). The link contains a zip file that contains two csv files: `tmdb_credits.csv`, `tmdb_movies.csv`.

The `tmdb_credits.csv` file contains cast and crew data including names, character names, job title, and the order of billed actors. The `tmdb_movies.csv` file contains all other information regarding each movie including title, budget, revenue, language, popularity, runtime, viewer rating data, and release date. 

# Cleaning the Data
The `cleaning_data.py` script contains the code to conduct the initial munging of the raw csv files. After cleaning the data cleaned data files were saved with *_cleaned.csv* suffix. 

The process of cleaning `tmdb_movies.csv` includes:
* removing`original_title` and `homepage` columns
* renaming `id` column to `movie_id`
* setting`movie_id` and `title` columns as a multi-level index. The `movie_id` index is considered the foreign key that can be used to link any table created from TMDB dataset.

The process of cleaning `tmdb_credits.csv`includes:
* same steps for `tmdb_movies.csv` 
* flattening nested JSON data

The JSON and non-JSON data columns were separated and saved into individual csv files to facilitate the process of handling JSON data. The columns with nested JSON data: `genres`, `keywords`, `production_companies`, `production_countries`, `spoken_languages`. Each column of JSON data was flattened and combined with the same \[`movie_id`, `title` \] multi-level index. 

There were a few issues regarding special characters in movie titles and missing data for release dates. Those instances were manually corrected. 

Although no values were missing, there were numerous cases where a movie had $0 in budget and revenue, as well as 0 minutes runtime. A web scraper (see `movie_scraper.py`) was developed in Python to obtain data from searching the database in www.the-numbers.com. The search results contained links for a movie webpage that contained budget, revenue, and runtime data. The budget was referred to as "Production Budget", runtime was referred to as "Running Time", and the revenue was determined by taking the max value of Domestic, International, and Worldwide Box Office revenue due to the possibility that some movies only had Domestic or International revenue data. In some cases, the movie title from TMDB did not match the database in www.the-numbers.com and IMDB was cross referenced to find other possible titles. As this process was highly labor intensive, alternative titles were found for only a handful of movies as the dataset was already of significant size. For movies that returned several results from a title search, the correct result was determined based on release date. It was observed that movies with the same title would not be released within several years of each other. If the scraper was unable to find budget, revenue, and/or runtime information on the website; the movie was deleted from the dataset. Out of 5000 movies in the original dataset, 4357 remained after cleaning process.

For the "tmdb_credits.csv" file:
-- 'movie_id' and 'title' columns are used for a multi-level index. The 'movie_id' index is considered the foreign key that can be used to link any table created from TMDB dataset.
-- columns with nested JSON data (i.e., list of dictionaries) were separated from non-JSON columns. The columns with nested JSON data: 'cast', 'crew'. Each column of JSON data was flattened and combined with the same ['movie_id', 'title'] multi-level index. The resulting table from flattening the JSON data was then saved in separate csv files (i.e., tables).  
-- no issues regarding special characters or missing data as the data was obtained from Kaggle


The 'budget' data in "tmdb_movies.csv" represents wordwide box-office gross and matches the data from http://www.boxofficemojo.com/alltime/world/.
The 'revenue' data matches cost estimates in https://en.wikipedia.org/wiki/List_of_most_expensive_films and is not adjusted for inflation.
No obvious outliers were discovered after investigating the data.


Alternative Datasets
--------------------
Data could also be obtained from other movie databases such as IMDB. There is also a Python API for TMDB -- as well as IMDB -- but it is currently not functioning properly. The same can also be said about the IMDB API. 


Initial Findings
----------------
There are several variables that go into the making of a movie and influence its success. The focus of analysis so far has been on variables that can be defined prior to film production -- and prior to a major financial commitment. When a movie is pitched to studios and other financiers, several variables are already defined such as the director, lead actors, associated genres, and expected runtime. 

Exploring the data led to some interesting discoveries regarding net revenue and net revenue percentage. The net revenue is calculated by subtracing the production budget from the worldwide box office revenue. The net revenue percentage is calculated by dividing the net revenue by the production budget. It was clear that the movies with the highest net revenue also required the largest production budget. On the other hand, the lower budget that were often found at the top of the list of movies that produced the highest net revenue percentage. 

The distribution of successful movies based on release date also showed that more hits were released either at the beginning or end of the month. This is most likely explained by the fact that most major US holidays also fall at the beginning or end of the month. It was also interesting to observe that most movies for both hits and flops were released in September.

There was also a trend in the average net revenue of all credits for veteran actors versus the net revenue of movies from new faces. Actors with more film credits had a much lower average for net revenue. The highest average net revenue belonged to less experienced actors. This may be evidence regression to the mean for an actor's success.

With some bootstrapping, we observed that there was a significant difference between the runtimes of hits and flops. Most hit movies had a runtime between 109 and 110 minutes while flops were between 104 and 107 minutes long. The same method was used to observe any trends with genres. Most movies in general had between 2 and 3 genres associated with them. Dramas and comedies, however, were the most likely movies to be profitable.
