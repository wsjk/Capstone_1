<details>
<summary><h1>The Client</h1></summary>
<p>
Film studios and investors who are considering financing a film.
</p>
</details>

<details>
<summary><h1>The Problem</h1></summary>
<p>
The film industry is already a billion dollar industry and steadily growing. The global box office revenue is forecast to increase 50 billion U.S. dollars in 2020<sup><a href = https://www.statista.com/topics/964/film/>[1]</a></sup>. The film "Avatar" is the current record holder for worldwide box office revenue is $2.8 billion with an estimated budget of $237 million. The risk, however, can be as great as the reward. One of the biggest box office bombs is "13th Warrior" which claimed an estimated loss of $129 million. Film studio executives and investors are constantly inundated with sales pitches for movies. How can anyone navigate the risk and choose a profitable film to finance? What does the next box office hit look like?
</p>
</details>

<details>
<summary><h1>Directory Map</h1></summary>
<p>
The directory structure of the code supporting this project:
      
```python
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
</p>
</details>
   
<details>
<summary><h1>The Data</h1></summary>
<p>
The [TMDB data set from Kaggle](https://www.kaggle.com/tmdb/tmdb-movie-metadata/data) contains information for 5000 films. The raw and unprocessed data is located in the [`data`](https://github.com/wsjk/Capstone_1/tree/master/data) sub-directory.

The [TMDB data](https://github.com/wsjk/Capstone_1/tree/master/data/raw/tmdb-5000-movie-dataset.zip) is provided as two csv files: `tmdb_credits.csv`, `tmdb_movies.csv`.

The `tmdb_credits.csv` file contains cast and crew data including names, character names, gender, job title, and the order of billing. The `tmdb_movies.csv` file contains all other information regarding each movie including title, budget, revenue, language, popularity, runtime, viewer rating data, and release date. 

<h2>Alternative Datasets</h2>
Data could also be obtained from other movie databases such as IMDB. There is also a Python API for TMDB -- as well as IMDB -- but was not functioning properly at the time of this project. The same can also be said about the IMDB API. 
</p>
</details>


<details>
<summary><h1>Cleaning the Data</h1></summary>
<p>
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
</p>
</details>

<details>
<summary><h1>Exploring the Data </h1></summary>
<p>

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

<h2> Initial Findings </h2>
The [`import_clean_data.py`](https://github.com/wsjk/Capstone_1/tree/master/src/data/import_clean_data.py) script is used to import clean, pre-processed data for exploratory analysis. All exploratory analyses are conducted in the IPython notebooks located [here](https://github.com/wsjk/Capstone_1/tree/master/notebooks)

<h2> Budget </h2>
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

<h2> Actors </h2>
The data shows a trend in the average net revenue for veteran actors versus the average net revenue of movies from new faces as shown in the plot below. Actors with more film credits (larger bubbles) had a much lower average for net revenue and net revenue percentage. The actors with highest average net revenue and net revenue percentage are difficult to spot in the plot because they belonged to actors with a single credit. This may be evidence of regression to the mean for the level of success for an actor. The same trends have also been observed for directors.

<div>
    <a href="https://plot.ly/~wsjk/17/?share_key=v7aWcF2zjp3ObnhOao3ZP4" target="_blank" title="Plot 17" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/17.png?share_key=v7aWcF2zjp3ObnhOao3ZP4" alt="Plot 17" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

The actors whose filmography generated the most and least amount of cumulative net revenue are shown in the box plots below. The spread of net revenue generated can be large for a given actor's film credits. A boxplot of the top grossing actors (i.e., the sum of net revenue of all film credits for each actor), is show below. We can see several recognizeable actors who often play major roles (e.g., Tom Hanks and Will Smith) and the actors who are have been generated the most net revenue overall would be Harry Potters stars Rupert Grint and Daniel Radcliffe.

![box_plot_hit_actor_sum]

A boxplot of the actors who have been involved with the most amount of hit movies (i.e., net revenue > 0) shows us a slightly different list of actors. Judging by the two box plots, it appears that Tom Cruise has been both highly successful and at a consistent rate.

![box_plot_hit_actor]

The same boxplots for actors in flops are shown below. The first box plot shows that films from Shea Whigham and Neil Maskill have accumulated the greatest loss in net revenue. The second boxplot shows the actors who have the most `flops` in their filmography and Val Kilmer takes the prize for most consistent in this category.

![box_plot_flop_actor_sum]

![box_plot_flop_actor]

Although, the track record of actors are not consistent in terms of their hits and flops. The following plots show the net revenue of actors who have generated the most and least amount of net revenue. Successful actors are not necessarily consistent and suffer from highs and lows in the revenue generated from their projects. The least successful actors, on the other hand, show some consistency in their filmography.

<div>
    <a href="https://plot.ly/~wsjk/43/?share_key=h864aQXAF41jzLpz4pQgOJ" target="_blank" title="Plot 43" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/43.png?share_key=h864aQXAF41jzLpz4pQgOJ" alt="Plot 43" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

<div>
    <a href="https://plot.ly/~wsjk/45/?share_key=qDyPbKwTIBMR0mQVsIfVsV" target="_blank" title="Plot 45" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/45.png?share_key=qDyPbKwTIBMR0mQVsIfVsV" alt="Plot 45" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
 </div>


<h2> Crew </h2>
Boxplots of the crew and their respective film credits are provided for those with the most `hits` and `flops` in their list of credits.  The crew consists of anyone other than actors including directors, executive producers, editors, writers, cinematographers, and directors of photography. 

<h3> Directors </h3>
The most consistently successful director according to the boxplots of cumulative net reveue below is Joss Whedon. And Morgan J. Freeman takes the prize for being the least successful director.

![box_top_dir]


![box_worst_dir]

Looking at the revenue history of the top Directors, Joss Whedon's films may have accumulated the most revenue, but James Cameron has helmed the single most successful movie. The track record of Director's are also a little less erratic compared to actors.

<div>
    <a href="https://plot.ly/~wsjk/47/?share_key=ZmVoy1EEJx20iDyqxsdqAd" target="_blank" title="Plot 47" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/47.png?share_key=ZmVoy1EEJx20iDyqxsdqAd" alt="Plot 47" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

<h3> Writers </h3>
The clear winner for most successful writer in terms of cumulative net revenue, as well as the most successful writer/director combo, is James Cameron. Although, Cameron only has two writing credits to his name. It is also interesting to note that a majority of the successful writers are also directors.

![box_top_writer]

The least successful writers are Ken Hixon and James Gray. It is surprising to find Paul Thomas Anderson in this group considering the critical praise his films regularly receive. This provides evidence of the disparity between a film's reception by the general public and film critics.

![box_worst_writer]

<div>
    <a href="https://plot.ly/~wsjk/49/?share_key=vgDkBYbsjeEwHwIK6oEVse" target="_blank" title="Plot 49" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/49.png?share_key=vgDkBYbsjeEwHwIK6oEVse" alt="Plot 49" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>


<h3> Producers </h3>

The boxplots show that the most successful executive producer Laeta Kalogridis thanks to her involvement with Avatar and Shutter Island. For producers who have been involved in numerous films, Callum McDougall has consistently worked on very successful films such as the more recent James Bond films and Harry Potter.

![box_top_producer]

The most consistent out of the list of least successful crew members is executive producer Victor Loewy. 

![box_worst_producer]

Similar to Directors, the track record of Producers are less erratic than actors. The revenue for George Lucas over the course of his career show great success in his early years (e.g., Star Wars), a sharp dip (e.g., Howard the Duck) in the late 80's, and then an uptick again in the early 90's (e.g., Indiana Jones, Star Wars).

<div>
    <a href="https://plot.ly/~wsjk/55/?share_key=MqB4oGXxfC1SLDJDUQ8F42" target="_blank" title="Plot 55" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/55.png?share_key=MqB4oGXxfC1SLDJDUQ8F42" alt="Plot 55" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

<h3> Genres </h3>
The TMDB dataset allows for a film to have several genres associated to it. A distribution of genres associated with films show that comedies and drama hold the lion's share. 

![genre_hist]

Although genre movies are prevalent, as shown in the histogram below, most successful movies are more "complex" and use multiple genres to describe it. It appears the key number of genres may be limited to three as there is a sharp drop afterwards -- possibly indicating that sometimes movies are too complex.

![genre_count_hist]

<h3> Runtime </h3>
The histogram below shows that both `hits` and `flops` have similar distributions and both types of films generally fall around the 100 minute mark. 

![runtime_hist]

</p>
</details>

<details>
   <summary><h1> Bootstrap Analysis </h2></summary>
   <p>
Bootstrapping is used to calculate confidence intervals for several of the features that were expected to be strong predictors of a film's performance.

<h2> Budget </h2>
As mentioned earlier, the budget appears to be positively correlated with net revenue. The 95% confidence interval for the mean budget of `hits` is between $36.7 million and $40.2 million. For `flops`, there is 95% confidence that the mean of the budget is between $22.5 million and $25.4 million.

<h2> Runtime </h2>
With some bootstrapping, we observed that there was a significant difference between the runtimes of hits and flops. Most hit movies had a runtime between 109 and 110 minutes while flops were between 104 and 107 minutes long.

![figure_4]

</p>
</details>

<details>
   <summary><h1>Prediction Model</h1></summary>
The Random Forest Classifier from Python's Sci-Kit Learn library is used to develop a model to predict whether a movie will be a `hit` or a `flop` given a set of features for the film. The model will be used to provide the probability of whether a movie will be a `hit` or a `flop`.

Files related to developing, training, and running the model are located in the [`model`](https://github.com/wsjk/Capstone_1/tree/master/src/model) folder.

A Jupyter Notebook with a walkthrough of the model is provided [`model`](https://github.com/wsjk/Capstone_1/blob/master/notebooks/RandomForestClassifier.ipynb).

<h2> The Model </h2>
Random Forest models takes an ensemble approach by using Decision Trees combined with Bootstrap Aggregation (bagging) techniques. Decision Trees alone suffer from overfitting issues, but bagging helps by training Decision Trees with data created from bootstrapping the training dataset and then combining the predictions. Random Forest takes it one step further by adding randomization to the number of features included when bootstrapping the training data. The resulting predictions from the individual trees are less correlated with eachother to further reduce the variance and overfitting of the model predictions.

<h2> Feature Selection </h2>
Feature selection and processing is conducted with the Python script: [`get_features.py`](https://github.com/wsjk/Capstone_1/blob/master/src/model/get_features.py). The Python script saves the processed feature set as csv files in [`notebooks`](https://github.com/wsjk/Capstone_1/blob/master/notebooks) directory.

The total list of features used to train the model are listed below.

* Budget
* Genres Features
```bash
`genre_count`, `action`, `adventure`, `animation`, `comedy`, `crime`, `documentary`, `drama`, `family`, `fantasy`, `foreign`, `history`, `horror`, `music`, `mystery`, `romance`, `science fiction`, `tv movie`, `thriller`, `war`, `western`
```
* Cast and Crew Features
```bash
`director_unknown`, `director_male`, `director_female`, `director_credits`, `director_net_to_date`, `actor_unknown`, `actor_male`, `actor_female`, `actor_credits`, `actor_net_to_date`, `writer_unknown`, `writer_male`, `writer_female`, `writer_credits`, `writer_net_to_date`
```
* Runtime
* Release Date Features
```bash
`release_year`, `January`, `February`, `March`, `April`, `May`, `June`, `July`, `August`, `September`, `October`, `November`, `December`, `Monday`, `Tuesday`, `Wednesday`, `Thursday`, `Friday`, `Saturday`, `Sunday
```
* Language Count

Notes about feature selection:
* One-hot encoding technique on the Genre, Cast & Crew, and Release Date Features
* `genre_count` feature represent the total number of genres associated with each film
* Cast and Crew features include gender, role (e.g., Director, Producer, Writer), and their `net_to_date` -- which is the cumulative sum of the net revenue of their filmography to date
* Cast and Crew members with unknown gender are represented by feature with suffix `_unknown` 
* Release Date features originally include day of the month (1 - 31), but initial phases of training the model showed that these features had low importance

<h2> Training the Model </h2>
The process of tuning the hyperparameters of the Random Forest Classifier is split into two phases:
1.  Use sklearn.RandomizedSearchCV() to do some initial exploration of hyperparameter values 
2.  Use sklearn.GridSearchCV() to fine tune the hyperparameters using the best parameter obtained from RandomSearchCV

Step 1 of the training process is conducted in [`rf_randomsearchcv.py`](https://github.com/wsjk/Capstone_1/blob/master/src/model/rf_randomsearchcv.py). The hyperparameters varied in this process are:

```bash
param_grid = {
  "oob_score": [True,False],
  "n_estimators": np.arange(10, 500, 10),
  "max_depth": np.arange(10, 500, 10),
  "min_samples_split": np.arange(2,150,1),
  "min_samples_leaf": np.arange(2,60,1),
  "max_leaf_nodes": np.arange(2,60,1),
  'max_features': ['auto','log2','sqrt',None],
  'criterion': ['gini', 'entropy'],
              }
```

<h2> Results of Training </h2>

<h2> Results of Test Data </h2>
Feature importance

</p>
</details>

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
 

