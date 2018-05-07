# The Client
Film studios and investors who are considering financing a film.

# The Problem
The film industry is already a billion dollar industry and steadily growing. The global box office revenue is forecast to increase 50 billion U.S. dollars in 2020<sup>[1](https://www.statista.com/topics/964/film/)</sup>. The film "Avatar" is the current record holder for worldwide box office revenue is $2.8 billion with an estimated budget of $237 million. The risk, however, can be as great as the reward. One of the biggest box office bombs is "13th Warrior" which claimed an estimated loss of $129 million. Film studio executives and investors are constantly inundated with sales pitches for movies. How can anyone navigate the risk and choose a profitable film to finance? What does the next box office hit look like?

# Directory Map
The directory structure of the code supporting this project:
```bash
├─ data
│  ├─ raw (Kaggle dataset)
│  ├─ interim (supplementary web scraped data)
│  └─ processed (cleaned data for exploratory analysis)
│  
├─ notebooks (IPython notebooks for statistical analysis)
|
├─ report (figures for report/README.md)
|
└─ src (Python scripts)
   ├─ data (cleaning/processing data)
   ├─ tools (helper functions for analysis and visualizations)
   └─ model (Random Forest model)
```

# The Data
The [TMDB data set from Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata/data) contains information for 5000 films. The raw and unprocessed data is located in the [`data`](https://github.com/wsjk/Capstone_1/tree/master/data) sub-directory.

The [TMDB data](https://github.com/wsjk/Capstone_1/tree/master/data/raw/tmdb-5000-movie-dataset.zip) is provided as two csv files: `tmdb_credits.csv`, `tmdb_movies.csv`.

The `tmdb_credits.csv` file contains cast and crew data including names, character names, gender, job title, and the order of billing. The `tmdb_movies.csv` file contains all other information regarding each movie including title, budget, revenue, language, popularity, runtime, viewer rating data, and release date. 

# Alternative Datasets
Data could also be obtained from other movie databases such as IMDB. There is also a Python API for TMDB -- as well as IMDB -- but was not functioning properly at the time of this project. The same can also be said about the IMDB API. 

# Cleaning the Data
The [`cleaning_data.py`](https://github.com/wsjk/Capstone_1/tree/master/src/data/cleaning_data.py) script conducts the initial munging of the raw csv files. The cleaned data files are saved with *\*_cleaned.csv* suffix. The final processed data for exploratory data analysis is located in the [`processed`](https://github.com/wsjk/Capstone_1/tree/master/data/folder) subfolder.

The process of cleaning `tmdb_movies.csv` includes:
* removing `original_title` and `homepage` columns
* renaming `id` column to `movie_id`
* setting `movie_id` and `title` columns as a multi-level index. The `movie_id` index is considered the foreign key that can be used to link any table created from TMDB dataset.

The process of cleaning `tmdb_credits.csv`includes:
* same steps for `tmdb_movies.csv` 
* flattening nested JSON data
* hardcoding corrected movie titles and release dates when special characters are present 
* address incorrect and missing values for budget, revenue, and runtime data

The JSON and non-JSON data columns were separated and saved into individual csv files to facilitate the process of handling JSON data. The columns with nested JSON data: `genres`, `keywords`, `production_companies`, `production_countries`, `spoken_languages`. Each column of JSON data was flattened and combined with the same \[`movie_id`, `title`\] multi-level index. 

Although there were no null values present in the data, there were numerous cases where a movie had $0 in budget and revenue, as well as 0 minutes runtime. A web scraper (see `movie_scraper.py`) was developed in Python to obtain data from searching the database in www.the-numbers.com. The search results contained links for a movie webpage that contained budget, revenue, and runtime data. The budget was referred to as *Production Budget*, runtime was referred to as *Running Time*, and the revenue was determined by taking the max value of Domestic, International, and Worldwide Box Office revenue due to the possibility that some movies only had Domestic or International revenue data. In some cases, the movie title from TMDB did not match the database in www.the-numbers.com and IMDB was used as a reference for possible alternate titles for these films. This process became tedious and highly labor intensive. Thus, only a handful of movies were manually corrected via alternative titles as this subset of films represented a small fraction of the dataset. For movies that returned several results from a title search, the correct result was determined based on release date. It is assumed that movies with the same title would not be released within several years of each other. If the scraper was unable to find budget, revenue, and/or runtime information on the website; the movie was deleted from the dataset. Out of 5000 movies in the original dataset, 4357 remained after cleaning process.

# Exploring the Data 
Out of all the variables that affect the making of a movie and influence its success, the analysis is focused specifically on variables that can be fixed prior to film production -- and prior to a major financial commitment. When a movie is pitched to studios, and other financiers, several variables can be defined such as the director, lead actors, writer, release date, and proposed budget. 

Exploring the data led to some interesting discoveries regarding net revenue and net revenue percentage. The net revenue is the difference between production budget and worldwide box office revenue. The net revenue percentage is calculated by dividing the net revenue by the production budget. 

`net revenue = budget - revenue`

`net revenue percentage = (budget - revenue) / budget`

The dataset is split into two main categories: `hits` and `flops`. Any movie that produces a positive net revenue was considered a `hit` movie. The remaining films who failed to break even are considered `flops`. The goal of this project is to be able to predict whether a movie is a `hit` or a `flop` based on the features that could be defined at the pitching stage of a film.

The exploratory analyses conducted on the data can be found in the following notebooks:
* [Analysis of Lead_Actor Influence](https://github.com/wsjk/Capstone_1/tree/master/notebooks/statistical_analysis_actors.ipynb)
* [Analysis of Crew Influence](https://github.com/wsjk/Capstone_1/tree/master/notebooks/statistical_crew_actors.ipynb)
* [Analysis of Genre Influence](https://github.com/wsjk/Capstone_1/tree/master/notebooks/statistical_genre_actors.ipynb)
* [Analysis of Runtime Influence](https://github.com/wsjk/Capstone_1/tree/master/notebooks/statistical_runtime_actors.ipynb)
* [Analysis of Language Influence](https://github.com/wsjk/Capstone_1/tree/master/notebooks/statistical_language_actors.ipynb)

#### Initial Findings
The [`import_clean_data.py`](https://github.com/wsjk/Capstone_1/tree/master/src/data/import_clean_data.py) script is used to import clean, pre-processed data for exploratory analysis. All exploratory analyses are conducted in the IPython notebooks located [here](https://github.com/wsjk/Capstone_1/tree/master/notebooks)

A pairplot created from data in `tmdb_movies.csv` is shown below:

![pairplot]

#### Budget
As expected, there is a positive linear correlation (Pearson's r = 0.56) between budget (`budget`) and net revenue (`net`). On the other hand, the films with the highest net revenue percentage (`net_pct`) were on the lower end of spectrum for `budget`. Furthermore, the plots show that increasing `budget` past a certain threshold results in a low, and nearly constant level of `net_pct`. This may hint at the possibility that there is an optimal `budget` if the goal is to maximize `net_pct`. 

<div>
    <a href="https://plot.ly/~wsjk/1/?share_key=QwVayGJKukfjPbrzELFpe6" target="_blank" title="net vs budget" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/1.png?share_key=QwVayGJKukfjPbrzELFpe6" alt="net vs budget" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

<div>
    <a href="https://plot.ly/~wsjk/3/?share_key=xZ7pBFB5GXb1QEiaIVkkcD" target="_blank" title="net_pct vs budget" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/3.png?share_key=xZ7pBFB5GXb1QEiaIVkkcD" alt="net_pct vs budget" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

The histogram below shows the distribution of `hits` and `flops` for a range of production budgets and reinforces the idea that lower budget films generally return a profit. Although, the number of `flops` at lower budgets relative to `hits` is significant and the risk is much lower. The histogram also shows that as the budget increases, the number of `flops` relative to `hits` decreases. This could indicate that high production value can improve the chances of creating a box office hit.

<div>
    <a href="https://plot.ly/~wsjk/5/?share_key=hPHHZ17WCLTNkKC4KBcQuW" target="_blank" title="budget histogram" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/5.png?share_key=hPHHZ17WCLTNkKC4KBcQuW" alt="Plot 5" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

Film budgets appear to have ballooned throughout the years and the number of high budget flops have decreased. It is possible that studios are getting smarter about their investments when the stakes are high. 

<div>
    <a href="https://plot.ly/~wsjk/7/?share_key=iPSdQAIpl1ozVxKDg62FDf" target="_blank" title="budget vs year" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/7.png?share_key=iPSdQAIpl1ozVxKDg62FDf" alt="Plot 7" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

Plotting the log of the mean of film budgets per year, show that film budgets have increased at an exponential rate throughout time.
<div>
    <a href="https://plot.ly/~wsjk/23/?share_key=McGmihZyLzaUYmMZYXYzFg" target="_blank" title="log avg budget vs year" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/23.png?share_key=McGmihZyLzaUYmMZYXYzFg" alt="Plot 23" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

The level of net revenue that films bring have also increased as of late, but it is also important to note that the losses have been held steady. The net revenue percentage, on the other hand, does not exhibit a clear trend with time.

<div>
    <a href="https://plot.ly/~wsjk/13/?share_key=61inZB9ZBwKPO2VSae9y8x" target="_blank" title="net vs year" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/13.png?share_key=61inZB9ZBwKPO2VSae9y8x" alt="Plot 13" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

<div>
    <a href="https://plot.ly/~wsjk/15/?share_key=POPpsqV5on9GbFV9qFTzZC" target="_blank" title="net_pct vs year" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/15.png?share_key=POPpsqV5on9GbFV9qFTzZC" alt="Plot 15" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

#### Actors
The data shows a trend in the average net revenue for veteran actors versus the average net revenue of movies from new faces as shown in the plot below. Actors with more film credits (larger bubbles) had a much lower average for net revenue and net revenue percentage. The actors with highest average net revenue and net revenue percentage are difficult to spot in the plot because they belonged to actors with a single credit. This may be evidence of regression to the mean for the level of success for an actor. The same trends have also been observed for directors.

<div>
    <a href="https://plot.ly/~wsjk/17/?share_key=v7aWcF2zjp3ObnhOao3ZP4" target="_blank" title="Plot 17" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/17.png?share_key=v7aWcF2zjp3ObnhOao3ZP4" alt="Plot 17" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

The actors whose filmography generated the most and least amount of cumulative net revenue are shown in the box plots below. The spread of net revenue generated can be large for a given actor's film credits. A boxplot of the top grossing actors (i.e., the sum of net revenue of all film credits for each actor), is show below. We can see several recognizeable actors who often play major roles (e.g., Tom Hanks and Will Smith) and the actors who are have been generated the most net revenue overall would be Harry Potters stars Rupert Grint and Daniel Radcliffe.

![box_plot_hit_actor_sum]

A boxplot of the actors who have been involved with the most amount of hit movies (i.e., net revenue > 0) shows us a slightly different list of actors. Judging by the two box plots, it appears that Tom Cruise has been both highly successful and at a consistent rate.

![box_plot_hit_actor]

The same boxplots for actors in flops show lesser known actors such as Shea Whigham and Neil Maskill attached to the least successful films. In terms of amount of `flops`, Val Kilmer may be the most consistent in being associated with unsuccessful films.

![box_plot_flop_actor_sum]

![box_plot_flop_actor]

Although, the track record of actors are not consistent in terms of their hits and flops. The following plots show the net revenue of actors who have generated the most and least amount of net revenue.
<div>
    <a href="https://plot.ly/~wsjk/43/?share_key=h864aQXAF41jzLpz4pQgOJ" target="_blank" title="Plot 43" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/43.png?share_key=h864aQXAF41jzLpz4pQgOJ" alt="Plot 43" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

<div>
    <a href="https://plot.ly/~wsjk/45/?share_key=qDyPbKwTIBMR0mQVsIfVsV" target="_blank" title="Plot 45" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/45.png?share_key=qDyPbKwTIBMR0mQVsIfVsV" alt="Plot 45" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
 </div>


#### Crew
Boxplots of the crew and their respective film credits are provided for those with the most `hits` and `flops` in their list of credits.  The crew consists of anyone other than actors including directors, executive producers, editors, writers, cinematographers, directors of photography. 


###### Directors
The boxplots show that the most successful "crew" member would be executive producer Alan Fine thanks to the success of Marvel films. 
![box_top_dir]


The most consistent out of the list of least successful crew members is executive producer Brad Blackbourn. 
![box_worst_dir]

Similar to the actor track records, few cast members (e.g., directors, producers, composers) are consistently good or bad. It is Johnny Depp, however, who holds the record for being involved in the biggest flop as an executive producer for The Lone Ranger

<div>
    <a href="https://plot.ly/~wsjk/47/?share_key=ZmVoy1EEJx20iDyqxsdqAd" target="_blank" title="Plot 47" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/47.png?share_key=ZmVoy1EEJx20iDyqxsdqAd" alt="Plot 47" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

###### Writers
![box_top_writer]
![box_worst_writer]

<div>
    <a href="https://plot.ly/~wsjk/49/?share_key=vgDkBYbsjeEwHwIK6oEVse" target="_blank" title="Plot 49" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/49.png?share_key=vgDkBYbsjeEwHwIK6oEVse" alt="Plot 49" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>


###### Producers
![box_top_producer]
![box_worst_producer]

<div>
    <a href="https://plot.ly/~wsjk/55/?share_key=MqB4oGXxfC1SLDJDUQ8F42" target="_blank" title="Plot 55" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/55.png?share_key=MqB4oGXxfC1SLDJDUQ8F42" alt="Plot 55" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>



#### Genres
The TMDB dataset allows for a film to have several genres associated to it. A distribution of genres associated with films show that comedies and drama hold the lion's share. 

![genre_hist]

Although genre movies are prevalent, as shown in the histogram below, most successful movies are more "complex" and use multiple genres to describe it. It appears the key number of genres may be limited to three as there is a sharp drop afterwards -- possibly indicating that sometimes movies are too complex.

![genre_count_hist]

#### Runtime
The histogram below shows that both `hits` and `flops` have similar distributions and both types of films generally fall around the 100 minute mark. 

![runtime_hist]

# Bootstrap Analysis
Bootstrapping was utilized to calculate confidence intervals for several of the features that were expected to be strong predictors of a film's performance.

#### Budget
As mentioned earlier, the budget appears to be positively correlated with net revenue. The 95% confidence interval for the mean budget of `hits` is \[$36.7 million $40.2 million\]. For `flops`, there is 95% confidence that the mean of the budget is between $22.5 million and $25.4 million.

#### Runtime
With some bootstrapping, we observed that there was a significant difference between the runtimes of hits and flops. Most hit movies had a runtime between 109 and 110 minutes while flops were between 104 and 107 minutes long. 
![figure_4]

# Predicting a Hit Or a Flop
A Random Forest Classifier model was chosen to create model to predict whether a movie is a `hit` or a `flop`. Random Forest models takes an ensemble approach by using Decision Trees combined with Bootstrap Aggregation (Bagging) techniques. Decision Trees alone suffer from overfitting issues, but Bagging helps by training Decision Trees with data created from bootstrapping the training dataset and then combining the predictions. Random Forest takes it one step further by adding randomization to the number of features included when bootstrapping the training data. The resulting predictions from the individual trees are less correlated with eachother to further reduce the variance and overfitting of the model predictions.

#### Feature Selection
The total list of features included in the training dataset are provided below:


#### Training the Model
Tuning hyperparameters

#### Results of Training

#### Results of Test Data
Feature importance


[pairplot]: https://github.com/wsjk/Capstone_1/blob/master/report/pairplot.png "Pairplot"
[figure_2]: https://github.com/wsjk/Capstone_1/blob/master/report/boxplot_hit_actors.png "Box Plot of Top Actors"
[figure_3]: https://github.com/wsjk/Capstone_1/blob/master/report/boxplot_flop_actors.png "Box Plot of Worst Actors"
[figure_4]: https://github.com/wsjk/Capstone_1/blob/master/report/runtime.png "CI for runtime"
[figure_5]: https://github.com/wsjk/Capstone_1/blob/master/report/genre.png "CI for genre count"
[box_top_dir]: https://github.com/wsjk/Capstone_1/blob/master/report/box_plot_top_directors.png 
[box_worst_dir]: https://github.com/wsjk/Capstone_1/blob/master/report/box_plot_worst_directors.png 
[box_top_writer]: https://github.com/wsjk/Capstone_1/blob/master/report/box_plot_top_writers.png 
[box_worst_writer]: https://github.com/wsjk/Capstone_1/blob/master/report/box_plot_worst_writers.png
[box_top_producer]: https://github.com/wsjk/Capstone_1/blob/master/report/box_plot_top_producers.png 
[box_worst_producer]: https://github.com/wsjk/Capstone_1/blob/master/report/box_plot_worst_producers.png 
[runtime_hist]: https://github.com/wsjk/Capstone_1/blob/master/report/runtime_hist.jpeg
[genre_count_hist]: https://github.com/wsjk/Capstone_1/blob/master/report/genre_count_hist.jpeg
[genre_hist]: https://github.com/wsjk/Capstone_1/blob/master/report/genre_hist.jpeg
[box_plot_hit_actor_sum]: https://github.com/wsjk/Capstone_1/blob/master/report/boxplot_hit_actors_sum.png 
[box_plot_flop_actor_sum]: https://github.com/wsjk/Capstone_1/blob/master/report/boxplot_flop_actors_sum.png 
[box_plot_hit_actor]:https://github.com/wsjk/Capstone_1/blob/master/report/boxplot_hit_actors.png 
[box_plot_flop_actor]:https://github.com/wsjk/Capstone_1/blob/master/report/boxplot_flop_actors.png 
 

