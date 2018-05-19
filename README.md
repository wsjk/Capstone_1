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

<details>
      <summary><h2>Alternative Datasets</h2></summary>
      <p>
Data could also be obtained from other movie databases such as IMDB. There is also a Python API for TMDB -- as well as IMDB -- but was not functioning properly at the time of this project. The same can also be said about the IMDB API. 
      </p>
      </details>

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

<details>
      <summary><h2> Initial Findings </h2></summary>
      <p>

The [`import_clean_data.py`](https://github.com/wsjk/Capstone_1/tree/master/src/data/import_clean_data.py) script is used to import clean, pre-processed data for exploratory analysis. All exploratory analyses are conducted in the IPython notebooks located [here](https://github.com/wsjk/Capstone_1/tree/master/notebooks)

</p>
</details>

<details>
      <summary><h3> Budget </h3></summary>
      <p>

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

</p>
</details>

<details>
      <summary><h3> Actors </h3></summary>
      <p>

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

</p>
</details>

<details>
      <summary><h3> Crew </h3></summary>
      <p>

Boxplots of the crew and their respective film credits are provided for those with the most `hits` and `flops` in their list of credits.  The crew consists of anyone other than actors including directors, executive producers, editors, writers, cinematographers, and directors of photography. 

<h3> Directors </h3>

The most consistently successful director according to the boxplots of cumulative net reveue below is Joss Whedon. And Morgan J. Freeman takes the prize for being the least successful director.

![box_top_dir]


![box_worst_dir]

Looking at the revenue history of the top Directors, Joss Whedon's films may have accumulated the most revenue, but James Cameron has helmed the single most successful movie. The track record of Director's are also a little less erratic compared to actors.

<div>
    <a href="https://plot.ly/~wsjk/47/?share_key=ZmVoy1EEJx20iDyqxsdqAd" target="_blank" title="Plot 47" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/47.png?share_key=ZmVoy1EEJx20iDyqxsdqAd" alt="Plot 47" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

</p>
</details>

<details>
      <summary><h3> Writers </h3></summary>
      <p>

The clear winner for most successful writer in terms of cumulative net revenue, as well as the most successful writer/director combo, is James Cameron. Although, Cameron only has two writing credits to his name. It is also interesting to note that a majority of the successful writers are also directors.

![box_top_writer]

The least successful writers are Ken Hixon and James Gray. It is surprising to find Paul Thomas Anderson in this group considering the critical praise his films regularly receive. This provides evidence of the disparity between a film's reception by the general public and film critics.

![box_worst_writer]

<div>
    <a href="https://plot.ly/~wsjk/49/?share_key=vgDkBYbsjeEwHwIK6oEVse" target="_blank" title="Plot 49" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/49.png?share_key=vgDkBYbsjeEwHwIK6oEVse" alt="Plot 49" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

</p>
</details>

<details>
      <summary><h3> Producers </h3></summary>
      <p>

The boxplots show that the most successful executive producer Laeta Kalogridis thanks to her involvement with Avatar and Shutter Island. For producers who have been involved in numerous films, Callum McDougall has consistently worked on very successful films such as the more recent James Bond films and Harry Potter.

![box_top_producer]

The most consistent out of the list of least successful crew members is executive producer Victor Loewy. 

![box_worst_producer]

Similar to Directors, the track record of Producers are less erratic than actors. The revenue for George Lucas over the course of his career show great success in his early years (e.g., Star Wars), a sharp dip (e.g., Howard the Duck) in the late 80's, and then an uptick again in the early 90's (e.g., Indiana Jones, Star Wars).

<div>
    <a href="https://plot.ly/~wsjk/55/?share_key=MqB4oGXxfC1SLDJDUQ8F42" target="_blank" title="Plot 55" style="display: block; text-align: center;"><img src="https://plot.ly/~wsjk/55.png?share_key=MqB4oGXxfC1SLDJDUQ8F42" alt="Plot 55" style="max-width: 100%;width: 600px;"  width="600" onerror="this.onerror=null;this.src='https://plot.ly/404.png';" /></a>
</div>

</p>
</details>

<details>
      <summary><h3> Genres </h3></summary>
      <p>

The TMDB dataset allows for a film to have several genres associated to it. A distribution of genres associated with films show that comedies and drama hold the lion's share. 

![genre_hist]

Although genre movies are prevalent, as shown in the histogram below, most successful movies are more "complex" and use multiple genres to describe it. It appears the key number of genres may be limited to three as there is a sharp drop afterwards -- possibly indicating that sometimes movies are too complex.

![genre_count_hist]

</p>
</details>

<details>
      <summary><h3> Runtime </h3></summary>
      <p>

The histogram below shows that both `hits` and `flops` have similar distributions and both types of films generally fall around the 100 minute mark. 

![runtime_hist]

</p>
</details>
</p>
</details>

<details>
   <summary><h1> Bootstrap Analysis </h1></summary>
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
      
The Random Forest algorithm is used to develop a classifier to predict whether a movie will be a `hit` or a `flop` given a set of features for the film. Random Forest Classifiers from Python's `Sci-Kit Learn` module is developed. The model will be used to provide the probability of whether a movie will be a `hit` or a `flop`.

Files related to developing, training, and running the model are located in the [`model`](https://github.com/wsjk/Capstone_1/tree/master/src/model) folder.

A Jupyter Notebook with a walkthrough of the model is provided in [`RandomForestClassifier.ipynb`](https://github.com/wsjk/Capstone_1/blob/master/notebooks/RandomForestClassifier.ipynb).

<details>
      <summary><h2> The Model </h2></summary>
            <p>

Random Forest models takes an ensemble approach by using Decision Trees combined with Bootstrap Aggregation (bagging) techniques. Decision Trees alone suffer from overfitting issues, but bagging helps by training Decision Trees with data created from bootstrapping the training dataset and then combining the predictions. Random Forest takes it one step further by adding randomization to the number of features included when bootstrapping the training data. The resulting predictions from the individual trees are less correlated with eachother to further reduce the variance and overfitting of the model predictions.

</p>
</details>

<details>
      <summary><h2> Feature Selection </h2></summary>
      <p>

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

</p>
</details>

<details>
      <summary><h2> Tuning Hyperparameters </h2></summary>
      <p>
         
The process of tuning the hyperparameters of the Random Forest Classifier is split into two phases:
1.  Use sklearn.RandomizedSearchCV() to do some initial exploration of hyperparameter values 
2.  Use sklearn.GridSearchCV() to fine tune the hyperparameters using the best parameter obtained from RandomSearchCV

Step 1 of the training process is conducted in [`rf_randomsearchcv.py`](https://github.com/wsjk/Capstone_1/blob/master/src/model/rf_randomsearchcv.py). The hyperparameter values were chosen randomly within a specific range of values. The range of values for each hyperparameter are:

```bash
{
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

The results of the RandomizedSearchCV process are shown below. The plots show the mean train (left column of plots) and test (right column of plots) scores for varying values for the hyperparameters.
            
![train_vs_test]


The hyperparameter values above provide a starting point for GridSearchCV process for Step 2 of the tuning process. The following table contains the hyperparameter values that led to the top 3 mean test and training scores from RandomizedSearchCV.

| param_criterion | param_max_depth | param_max_leaf_nodes | param_min_samples_leaf | param_min_samples_split | param_n_estimators | param_oob_score |
|:---------------:|:---------------:|:--------------------:|:----------------------:|:-----------------------:|:------------------:|:---------------:|
| gini    |310  | 49 | 4  | 2   | 370 | FALSE |
| gini    | 340 | 33 | 2  | 28  | 220 | TRUE  |
| gini    | 260 | 56 | 6  | 2   | 330 | FALSE |
| gini    | 70  | 25 | 56 | 95  | 20  | FALSE |
| entropy | 400 | 22 | 8  | 85  | 420 | TRUE  |
| gini    | 60  | 30 | 5  | 147 | 170 | TRUE  | 


Using the best hyperparameters obtained from the random search, a range of hyperparameters used for the grid search are 
```bash
{
'criterion': ['gini', 'entropy'],
'max_depth': range(60,332),
'max_leaf_nodes': range(22, 52),
'min_samples_leaf': range(2, 52),
'min_samples_split': range(2, 118),
'n_estimators': range(20, 340),
'oob_score': [False, True]
 }
```

With a `mean_test_score` of 0.61, `mean_train_score` of 0.70, and an `accuracy_score` of 0.70; the best overall parameters obtained from the grid search are
```bash
RandomForestClassifier(
bootstrap=True, class_weight=None, criterion='gini',
max_depth=330, max_features=None, max_leaf_nodes=34,
min_impurity_decrease=0.0, min_impurity_split=None,
min_samples_leaf=23, min_samples_split=109,
min_weight_fraction_leaf=0.0, n_estimators=30, n_jobs=1,
oob_score=True, random_state=42, verbose=0, warm_start=False)
```

</p>
</details>
      
<details>
      <summary><h2> Feature Importance </h2></summary>
      <p>

Sci-Kit Learn's RandomForestClassifier also provides a list of feature importance. The `budget`, `release_year`, and `runtime` features are considered the most important predictor, while some gender, genre, and release date features have no importance at all. The fact that the top features are the only continuous features in the dataset may not be coincidental. There have been some studies that show that one-hot encoding categorical variables -- which was done for this dataset -- can erode the performance of Random Forest Classifers
<sup><a href = https://roamanalytics.com/2016/10/28/are-categorical-variables-getting-lost-in-your-random-forests/>[2]</a></sup>. 

| feature | importance |
|:---------------:|:---------------:|
| budget | 0.243
| runtime | 0.060
| release_year | 0.243
| actor_unknown | 0.003 | 
| actor_male | 0.0 | 
| actor_female | 0.021 | 
| actor_credits | 0.019 | 
| actor_net_to_date | 0.054 | 
| director_unknown | 0.003 | 
| director_male | 0.0 | 
| director_female | 0.0 | 
| director_credits | 0.010 | 
| director_net_to_date | 0.145 | 
| writer_unknown | 0.005 | 
| writer_male | 0.003 | 
| writer_female | 0.006 | 
| writer_credits | 0.022 | 
| writer_net_to_date | 0.050 | 
| action | 0.003 | 
| adventure | 0.0 | 
| animation | 0.0 | 
| comedy | 0.008 | 
| crime | 0.002 | 
| documentary | 0.0 | 
| drama | 0.010| 
| family | 0.006 | 
| fantasy | 0.0 | 
| foreign | 0.0 | 
| history | 0.0 | 
| horror | 0.009 | 
| music | 0.0 | 
| mystery | 0.003 | 
| romance | 0.004 | 
| science fiction | 0.0 | 
| tv movie | 0.0 | 
| thriller | 0.0 | 
| war | 0.0 | 
| western | 0.0 | 
| genre_count | 0.023 | 
| language_count | 0.007 | 
| January | 0.0 | 
| February | 0.002 | 
| March | 0.0 | 
| April | 0.004 | 
| May | 0.0 | 
| June | 0.0 | 
| July | 0.0 | 
| August | 0.003 | 
| September | 0.001 | 
| October | 0.0 | 
| November | 0.0 | 
| December | 0.002 | 
| Monday | 0.0 | 
| Tuesday | 0.0 | 
| Wednesday | 0.013| 
| Thursday | 0.003 | 
| Friday | 0.011 | 
| Saturday | 0.0 | 
| Sunday | 0.0 | 
</p>
</details>   

<details>
 <summary><h2> Model Performance </h2></summary>
 <p>

As mentioned before, the Random Forest Classifier mean test score was 0.61. The confusion matrix from running the model on the test data set is provided below. The dataset had more `hits` than `flops` and the confusion matrix shows that the model may be more pre-disposed to classifying a film as a `hit`. 

|  |  | Actual | Actual |
|:---------------:|:---------------:|:---------------:|:---------------:|
|  |  | `flop` | `hit` |
| Predicted | `flop` | 66 | 58 | 
| Predicted | `hit` | 95 | 172 | 

       
The overall results of testing are provided below. The model provides the probability of a film being either a `hit` or a `flop`. The actual value is provided in the `target` column. The correctly classified -- and with high confidence -- the more well-known hit films such as `The Good, the Bad, and the Ugly`, `Dawn of the Planet of the Apes`, and `The Revenant`. The model, however, is not as confident at predicting `flop`s. Out of the films in the test dataset, the model predicted `ATL` to have the highest probability (0.66) of being a `flop`. The model was incorrect as `ATL` was actually a `hit`. Out of the films where the model correclty predicted a `flop`, `All the Real Girls` received the highest probability of being a `flop` at 0.63. 

On the other hand, there are also several examples of the model predicting a high probability of a `hit` for a film that turned out to be a `flop`. Out of all movies that were incorrectly predicted to be a `hit`, `The Molly Maguires` received the highest probability of 0.85. 
       
| title | hit | flop | target |
|:---------------:|:---------------:|:---------------:|:---------------:|
| The Goods: Live Hard Sell Hard | 0.43 | 0.57 | 1.0 | 
| Stiff Upper Lips | 0.51 | 0.49 | -1.0 | 
| ATL | 0.34 | 0.66 | 1.0 | 
| Censored Voices | 0.43 | 0.57 | -1.0 | 
| Fateless | 0.43 | 0.57 | -1.0 | 
| Lars and the Real Girl | 0.53 | 0.47 | -1.0 | 
| The Caveman's Valentine | 0.48 | 0.52 | -1.0 | 
| The Broken Hearts Club: A Romantic Comedy | 0.45 | 0.55 | 1.0 | 
| Abandon | 0.46 | 0.54 | -1.0 | 
| 10 Things I Hate About You | 0.49 | 0.51 | 1.0 | 
| Supercross | 0.50 | 0.50 | -1.0 | 
| Super 8 | 0.79 | 0.21 | 1.0 | 
| Dragon Blade | 0.73 | 0.27 | 1.0 | 
| The Masked Saint | 0.43 | 0.57 | -1.0 | 
| The Blue Room | 0.49 | 0.51 | 1.0 | 
| Sky High | 0.61 | 0.39 | 1.0 | 
| Remember Me | 0.48 | 0.52 | 1.0 | 
| Eve's Bayou | 0.50 | 0.50 | 1.0 | 
| The Good Night | 0.52 | 0.48 | -1.0 | 
| Beloved | 0.76 | 0.24 | -1.0 | 
| Yes | 0.50 | 0.50 | -1.0 | 
| Misconduct | 0.52 | 0.48 | -1.0 | 
| Promised Land | 0.64 | 0.36 | -1.0 | 
| Wild Grass | 0.44 | 0.56 | -1.0 | 
| A Cinderella Story | 0.51 | 0.49 | 1.0 | 
| Tsotsi | 0.37 | 0.63 | 1.0 | 
| Fish Tank | 0.49 | 0.51 | -1.0 | 
| The Devil Inside | 0.55 | 0.45 | 1.0 | 
| The Croods | 0.88 | 0.12 | 1.0 | 
| Killers | 0.82 | 0.18 | 1.0 | 
| Florence Foster Jenkins | 0.75 | 0.25 | 1.0 | 
| Maniac | 0.70 | 0.30 | -1.0 | 
| Home Run | 0.43 | 0.57 | 1.0 | 
| Another Year | 0.56 | 0.44 | 1.0 | 
| Out Cold | 0.47 | 0.53 | -1.0 | 
| Eden Lake | 0.44 | 0.56 | 1.0 | 
| RockNRolla | 0.71 | 0.29 | 1.0 | 
| Space Dogs | 0.52 | 0.48 | -1.0 | 
| The Witch | 0.52 | 0.48 | 1.0 | 
| Sugar Hill | 0.54 | 0.46 | 1.0 | 
| Twin Falls Idaho | 0.44 | 0.56 | 1.0 | 
| 16 Blocks | 0.83 | 0.17 | 1.0 | 
| Raising Victor Vargas | 0.41 | 0.59 | 1.0 | 
| The Sweeney | 0.46 | 0.54 | 1.0 | 
| Your Sister's Sister | 0.52 | 0.48 | 1.0 | 
| Law Abiding Citizen | 0.79 | 0.21 | 1.0 | 
| World Trade Center | 0.85 | 0.15 | 1.0 | 
| Slums of Beverly Hills | 0.50 | 0.50 | 1.0 | 
| Mother and Child | 0.50 | 0.50 | -1.0 | 
| Before Midnight | 0.56 | 0.44 | 1.0 | 
| Chain Letter | 0.53 | 0.47 | -1.0 | 
| Molly | 0.47 | 0.53 | -1.0 | 
| The Wraith | 0.80 | 0.20 | 1.0 | 
| Stoker | 0.61 | 0.39 | 1.0 | 
| Bon Cop Bad Cop | 0.47 | 0.53 | 1.0 | 
| Get on the Bus | 0.51 | 0.49 | 1.0 | 
| The Book of Life | 0.69 | 0.31 | 1.0 | 
| "The Good, the Bad, and the Ugly" | 0.86 | 0.14 | 1.0 | 
| The Rules of Attraction | 0.46 | 0.54 | 1.0 | 
| The Gift | 0.51 | 0.49 | 1.0 | 
| Margaret | 0.58 | 0.42 | -1.0 | 
| Miss Congeniality | 0.65 | 0.35 | 1.0 | 
| Journey to Saturn | 0.36 | 0.64 | 1.0 | 
| Close Encounters of the Third Kind | 0.83 | 0.17 | 1.0 | 
| X-Men: First Class | 0.86 | 0.14 | 1.0 | 
| Walking With Dinosaurs | 0.82 | 0.18 | 1.0 | 
| The Hateful Eight | 0.83 | 0.17 | 1.0 | 
| Two Can Play That Game | 0.50 | 0.50 | 1.0 | 
| Dawn of the Planet of the Apes | 0.84 | 0.16 | 1.0 | 
| Mozart's Sister | 0.49 | 0.51 | -1.0 | 
| I Hope They Serve Beer in Hell | 0.39 | 0.61 | -1.0 | 
| The Pirates! In an Adventure with Scientists! | 0.69 | 0.31 | 1.0 | 
| Space Jam | 0.65 | 0.35 | 1.0 | 
| Lockout | 0.56 | 0.44 | 1.0 | 
| Made | 0.44 | 0.56 | 1.0 | 
| The Names of Love | 0.53 | 0.47 | 1.0 | 
| Micmacs | 0.68 | 0.32 | -1.0 | 
| The Young Victoria | 0.60 | 0.40 | -1.0 | 
| The Purge | 0.52 | 0.48 | 1.0 | 
| Johnny Suede | 0.53 | 0.47 | -1.0 | 
| Ghost Rider: Spirit of Vengeance | 0.72 | 0.28 | 1.0 | 
| The Immigrant | 0.61 | 0.39 | -1.0 | 
| Silent Trigger | 0.48 | 0.52 | -1.0 | 
| Submarine | 0.48 | 0.52 | 1.0 | 
| Lone Survivor | 0.85 | 0.15 | 1.0 | 
| The Losers | 0.55 | 0.45 | -1.0 | 
| The Matrix | 0.68 | 0.32 | 1.0 | 
| Dreamer: Inspired By a True Story | 0.55 | 0.45 | 1.0 | 
| Dom Hemingway | 0.50 | 0.50 | -1.0 | 
| The Great Debaters | 0.49 | 0.51 | 1.0 | 
| Hard Candy | 0.41 | 0.59 | 1.0 | 
| The Last Exorcism Part II | 0.51 | 0.49 | 1.0 | 
| The Greatest Game Ever Played | 0.44 | 0.56 | -1.0 | 
| Surrogates | 0.87 | 0.13 | 1.0 | 
| A Low Down Dirty Shame | 0.69 | 0.31 | 1.0 | 
| Larry the Cable Guy: Health Inspector | 0.38 | 0.62 | -1.0 | 
| Saw V | 0.56 | 0.44 | 1.0 | 
| In the Company of Men | 0.51 | 0.49 | 1.0 | 
| Blackhat | 0.84 | 0.16 | -1.0 | 
| Big Eyes | 0.66 | 0.34 | 1.0 | 
| The Sweetest Thing | 0.66 | 0.34 | 1.0 | 
| Romance & Cigarettes | 0.38 | 0.62 | -1.0 | 
| Free Style | 0.45 | 0.55 | -1.0 | 
| Endless Love | 0.53 | 0.47 | 1.0 | 
| Shrek Forever After | 0.84 | 0.16 | 1.0 | 
| Creative Control | 0.44 | 0.56 | -1.0 | 
| Paul Blart: Mall Cop 2 | 0.79 | 0.21 | 1.0 | 
| Speedway Junky | 0.48 | 0.52 | -1.0 | 
| Akeelah and the Bee | 0.45 | 0.55 | 1.0 | 
| Corky Romano | 0.43 | 0.57 | 1.0 | 
| "Dancer |  Texas Pop. 81" | 0.51 | 0.49 | -1.0 | 
| Why Did I Get Married? | 0.70 | 0.30 | 1.0 | 
| The House Bunny | 0.67 | 0.33 | 1.0 | 
| Drowning Mona | 0.52 | 0.48 | -1.0 | 
| Wild Target | 0.60 | 0.40 | -1.0 | 
| Hostel | 0.39 | 0.61 | 1.0 | 
| Camping Sauvage | 0.43 | 0.57 | -1.0 | 
| Noah | 0.90 | 0.10 | 1.0 | 
| Radio | 0.63 | 0.37 | 1.0 | 
| Away We Go | 0.56 | 0.44 | -1.0 | 
| Fido | 0.46 | 0.54 | -1.0 | 
| Harvard Man | 0.50 | 0.50 | -1.0 | 
| A Room for Romeo Brass | 0.45 | 0.55 | -1.0 | 
| Ninja Assassin | 0.61 | 0.39 | 1.0 | 
| New Year's Eve | 0.85 | 0.15 | 1.0 | 
| TMNT | 0.57 | 0.43 | 1.0 | 
| Fifty Dead Men Walking | 0.56 | 0.44 | -1.0 | 
| Morning Glory | 0.79 | 0.21 | 1.0 | 
| Zack and Miri Make a Porno | 0.71 | 0.29 | 1.0 | 
| American Splendor | 0.40 | 0.60 | 1.0 | 
| Speed Racer | 0.82 | 0.18 | -1.0 | 
| Dawn of the Crescent Moon | 0.44 | 0.56 | -1.0 | 
| The Dead Girl | 0.56 | 0.44 | -1.0 | 
| The Rookie | 0.48 | 0.52 | 1.0 | 
| Lights Out | 0.56 | 0.44 | 1.0 | 
| 1911 | 0.64 | 0.36 | -1.0 | 
| My Big Fat Independent Movie | 0.47 | 0.53 | -1.0 | 
| Children of Heaven | 0.49 | 0.51 | 1.0 | 
| Behind Enemy Lines | 0.59 | 0.41 | 1.0 | 
| Twilight Zone: The Movie | 0.77 | 0.23 | 1.0 | 
| The Last Godfather | 0.54 | 0.46 | 1.0 | 
| Serenity | 0.63 | 0.37 | -1.0 | 
| The Other End of the Line | 0.42 | 0.58 | -1.0 | 
| Insidious | 0.70 | 0.30 | 1.0 | 
| All About Steve | 0.54 | 0.46 | 1.0 | 
| Win a Date with Tad Hamilton! | 0.57 | 0.43 | -1.0 | 
| The Skeleton Twins | 0.46 | 0.54 | 1.0 | 
| Central Intelligence | 0.84 | 0.16 | 1.0 | 
| Life During Wartime | 0.49 | 0.51 | -1.0 | 
| Basquiat | 0.42 | 0.58 | 1.0 | 
| Gunless | 0.52 | 0.48 | -1.0 | 
| Chappie | 0.81 | 0.19 | 1.0 | 
| The Terminal | 0.84 | 0.16 | 1.0 | 
| Weekend | 0.47 | 0.53 | 1.0 | 
| Takers | 0.58 | 0.42 | 1.0 | 
| Deterrence | 0.49 | 0.51 | -1.0 | 
| Bringing Down the House | 0.70 | 0.30 | 1.0 | 
| The Grudge | 0.55 | 0.45 | 1.0 | 
| Miracle at St. Anna | 0.79 | 0.21 | -1.0 | 
| Love & Basketball | 0.47 | 0.53 | 1.0 | 
| The Darkest Hour | 0.61 | 0.39 | 1.0 | 
| Frances Ha | 0.56 | 0.44 | 1.0 | 
| The World's End | 0.61 | 0.39 | 1.0 | 
| American Hustle | 0.86 | 0.14 | 1.0 | 
| Rocket Singh: Salesman of the Year | 0.46 | 0.54 | 1.0 | 
| Wild | 0.63 | 0.37 | 1.0 | 
| Something Borrowed | 0.71 | 0.29 | 1.0 | 
| Mulholland Drive | 0.52 | 0.48 | 1.0 | 
| Freddy vs. Jason | 0.55 | 0.45 | 1.0 | 
| Nacho Libre | 0.62 | 0.38 | 1.0 | 
| The Blind Side | 0.54 | 0.46 | 1.0 | 
| A Haunted House 2 | 0.70 | 0.30 | 1.0 | 
| Please Give | 0.67 | 0.33 | 1.0 | 
| One to Another | 0.41 | 0.59 | -1.0 | 
| "Mystery |  Alaska" | 0.62 | 0.38 | -1.0 | 
| Departure | 0.50 | 0.50 | -1.0 | 
| Foodfight! | 0.66 | 0.34 | -1.0 | 
| Rango | 0.88 | 0.12 | 1.0 | 
| Brokedown Palace | 0.42 | 0.58 | -1.0 | 
| Baghead | 0.49 | 0.51 | -1.0 | 
| Ponyo | 0.78 | 0.22 | 1.0 | 
| Zero Dark Thirty | 0.69 | 0.31 | 1.0 | 
| Nebraska | 0.65 | 0.35 | 1.0 | 
| X-Men | 0.66 | 0.34 | 1.0 | 
| Yoga Hosers | 0.68 | 0.32 | -1.0 | 
| Pitch Perfect 2 | 0.62 | 0.38 | 1.0 | 
| Janky Promoters | 0.67 | 0.33 | -1.0 | 
| Saved! | 0.49 | 0.51 | 1.0 | 
| Duplicity | 0.77 | 0.23 | -1.0 | 
| The Upside of Anger | 0.49 | 0.51 | 1.0 | 
| Eye of the Beholder | 0.50 | 0.50 | 1.0 | 
| Her | 0.61 | 0.39 | 1.0 | 
| Begin Again | 0.54 | 0.46 | 1.0 | 
| Friday the 13th: A New Beginning | 0.82 | 0.18 | 1.0 | 
| Slackers | 0.41 | 0.59 | -1.0 | 
| Crooklyn | 0.59 | 0.41 | -1.0 | 
| The Ladies Man | 0.43 | 0.57 | -1.0 | 
| The Adventures of Rocky & Bullwinkle | 0.62 | 0.38 | -1.0 | 
| Screwed | 0.47 | 0.53 | -1.0 | 
| The Christmas Candle | 0.52 | 0.48 | -1.0 | 
| Happy Feet | 0.85 | 0.15 | 1.0 | 
| Bucky Larson: Born to Be a Star | 0.70 | 0.30 | -1.0 | 
| Raise the Titanic | 0.76 | 0.24 | -1.0 | 
| Khumba | 0.54 | 0.46 | 1.0 | 
| Righteous Kill | 0.74 | 0.26 | 1.0 | 
| Collateral | 0.72 | 0.28 | 1.0 | 
| Nothing | 0.38 | 0.62 | -1.0 | 
| Raise Your Voice | 0.50 | 0.50 | -1.0 | 
| Salt | 0.88 | 0.12 | 1.0 | 
| Apocalypto | 0.78 | 0.22 | 1.0 | 
| Not Cool | 0.40 | 0.60 | -1.0 | 
| "South Park: Bigger |  Longer & Uncut" | 0.53 | 0.47 | 1.0 | 
| Along Came Polly | 0.61 | 0.39 | 1.0 | 
| All the Real Girls | 0.37 | 0.63 | -1.0 | 
 Wall Street: Money Never Sleeps | 0.87 | 0.13 | 1.0 | 
| Little Black Book | 0.54 | 0.46 | -1.0 | 
| Moonrise Kingdom | 0.64 | 0.36 | 1.0 | 
| Groove | 0.46 | 0.54 | 1.0 | 
| Middle of Nowhere | 0.52 | 0.48 | 1.0 | 
| Semi-Pro | 0.66 | 0.34 | -1.0 | 
| Air Bud | 0.50 | 0.50 | 1.0 | 
| J. Edgar | 0.82 | 0.18 | 1.0 | 
| The Dangerous Lives of Altar Boys | 0.42 | 0.58 | -1.0 | 
| The Visit | 0.70 | 0.30 | 1.0 | 
| You Will Meet a Tall Dark Stranger | 0.70 | 0.30 | 1.0 | 
| Eddie: The Sleepwalking Cannibal | 0.49 | 0.51 | -1.0 | 
| Shade | 0.53 | 0.47 | 1.0 | 
| Krush Groove | 0.82 | 0.18 | 1.0 | 
| The Players Club | 0.51 | 0.49 | 1.0 | 
| Teenage Mutant Ninja Turtles | 0.83 | 0.17 | 1.0 | 
| The Homesman | 0.54 | 0.46 | -1.0 | 
| Premium Rush | 0.72 | 0.28 | -1.0 | 
| Prisoners | 0.75 | 0.25 | 1.0 | 
| Beat the World | 0.48 | 0.52 | -1.0 | 
| Trance | 0.66 | 0.34 | 1.0 | 
| Grave Encounters | 0.40 | 0.60 | 1.0 | 
| LOL | 0.62 | 0.38 | -1.0 | 
| Alvin and the Chipmunks: Chipwrecked | 0.85 | 0.15 | 1.0 | 
| Skyfall | 0.88 | 0.12 | 1.0 | 
| Shanghai Surprise | 0.77 | 0.23 | -1.0 | 
| Epic Movie | 0.51 | 0.49 | 1.0 | 
| Saving Mr. Banks | 0.78 | 0.22 | 1.0 | 
| Priest | 0.69 | 0.31 | 1.0 | 
| Fled | 0.53 | 0.47 | -1.0 | 
| Funny People | 0.85 | 0.15 | -1.0 | 
| The Secret of Kells | 0.48 | 0.52 | -1.0 | 
| Joy Ride | 0.45 | 0.55 | 1.0 | 
| Plush | 0.57 | 0.43 | -1.0 | 
| Travellers and Magicians | 0.39 | 0.61 | -1.0 | 
| Steel | 0.45 | 0.55 | -1.0 | 
| Escape from Tomorrow | 0.44 | 0.56 | -1.0 | 
| The Grandmaster | 0.53 | 0.47 | 1.0 | 
| To Rome with Love | 0.76 | 0.24 | 1.0 | 
| A Very Harold & Kumar Christmas | 0.50 | 0.50 | 1.0 | 
| Free State of Jones | 0.84 | 0.16 | -1.0 | 
| For Your Consideration | 0.63 | 0.37 | -1.0 | 
| The Incredible Burt Wonderstone | 0.66 | 0.34 | -1.0 | 
| Two Lovers | 0.54 | 0.46 | -1.0 | 
| An American Carol | 0.69 | 0.31 | -1.0 | 
| The Inhabited Island | 0.62 | 0.38 | -1.0 | 
| Four Lions | 0.51 | 0.49 | 1.0 | 
| Predator 2 | 0.56 | 0.44 | 1.0 | 
| Slither | 0.55 | 0.45 | -1.0 | 
| Windsor Drive | 0.49 | 0.51 | -1.0 | 
| Men in Black 3 | 0.88 | 0.12 | 1.0 | 
| Casino Jack | 0.50 | 0.50 | -1.0 | 
| Without Limits | 0.42 | 0.58 | -1.0 | 
| Mutual Appreciation | 0.42 | 0.58 | 1.0 | 
| Turbulence | 0.62 | 0.38 | -1.0 | 
| The Perfect Man | 0.69 | 0.31 | 1.0 | 
| Trust | 0.53 | 0.47 | -1.0 | 
| The Butler | 0.56 | 0.44 | 1.0 | 
| Dumb and Dumber | 0.53 | 0.47 | 1.0 | 
| Can't Stop the Music | 0.85 | 0.15 | -1.0 | 
| Inherent Vice | 0.67 | 0.33 | -1.0 | 
| Cop Out | 0.68 | 0.32 | 1.0 | 
| Cheap Thrills | 0.50 | 0.50 | -1.0 | 
| Automata | 0.54 | 0.46 | -1.0 | 
| Jerry Maguire | 0.67 | 0.33 | 1.0 | 
| They | 0.51 | 0.49 | -1.0 | 
| Bad Moms | 0.63 | 0.37 | 1.0 | 
| Murderball | 0.35 | 0.65 | 1.0 | 
| Jonah: A VeggieTales Movie | 0.48 | 0.52 | 1.0 | 
| Sanctum | 0.62 | 0.38 | 1.0 | 
| The Pursuit of D.B. Cooper | 0.85 | 0.15 | -1.0 | 
| Fiza | 0.49 | 0.51 | -1.0 | 
| Panic Room | 0.76 | 0.24 | 1.0 | 
| The Blue Butterfly | 0.47 | 0.53 | -1.0 | 
| Think Like a Man Too | 0.73 | 0.27 | 1.0 | 
| The Boat That Rocked | 0.78 | 0.22 | -1.0 | 
| Because of Winn-Dixie | 0.53 | 0.47 | 1.0 | 
| One Hour Photo | 0.59 | 0.41 | 1.0 | 
| Land of the Lost | 0.85 | 0.15 | -1.0 | 
| Mama | 0.56 | 0.44 | 1.0 | 
| Valiant | 0.63 | 0.37 | -1.0 | 
| Man on Wire | 0.39 | 0.61 | 1.0 | 
| The 5th Quarter | 0.49 | 0.51 | -1.0 | 
| Red Riding Hood | 0.77 | 0.23 | 1.0 | 
| A Million Ways to Die in the West | 0.80 | 0.20 | 1.0 | 
| Johnson Family Vacation | 0.49 | 0.51 | 1.0 | 
| Beasts of the Southern Wild | 0.48 | 0.52 | 1.0 | 
| End of the Spear | 0.37 | 0.63 | 1.0 | 
| Dragon Nest: Warriors' Dawn | 0.69 | 0.31 | -1.0 | 
| The Molly Maguires | 0.85 | 0.15 | -1.0 | 
| Sabotage | 0.71 | 0.29 | -1.0 | 
| Marmaduke | 0.68 | 0.32 | 1.0 | 
| Ca$h | 0.49 | 0.51 | -1.0 | 
| Triangle | 0.47 | 0.53 | -1.0 | 
| What to Expect When You're Expecting | 0.83 | 0.17 | 1.0 | 
| End of Days | 0.77 | 0.23 | 1.0 | 
| 16 to Life | 0.47 | 0.53 | -1.0 | 
| Blended | 0.85 | 0.15 | 1.0 | 
| The Adventurer: The Curse of the Midas Box | 0.52 | 0.48 | -1.0 | 
| The Circle | 0.38 | 0.62 | 1.0 | 
| The Reef | 0.57 | 0.43 | 1.0 | 
| September Dawn | 0.46 | 0.54 | -1.0 | 
| The East | 0.66 | 0.34 | -1.0 | 
| Limbo | 0.63 | 0.37 | -1.0 | 
| Identity | 0.59 | 0.41 | 1.0 | 
| The Truman Show | 0.77 | 0.23 | 1.0 | 
| Taken 3 | 0.85 | 0.15 | 1.0 | 
| Hotel Transylvania 2 | 0.86 | 0.14 | 1.0 | 
| Dinner Rush | 0.46 | 0.54 | -1.0 | 
| Charlie St. Cloud | 0.77 | 0.23 | 1.0 | 
| One Man's Hero | 0.50 | 0.50 | -1.0 | 
| Quarantine | 0.49 | 0.51 | 1.0 | 
| Home on the Range | 0.63 | 0.37 | -1.0 | 
| The Book Thief | 0.69 | 0.31 | 1.0 | 
| Grindhouse | 0.78 | 0.22 | -1.0 | 
| The Yellow Handkerchief | 0.45 | 0.55 | -1.0 | 
| Malibu's Most Wanted | 0.41 | 0.59 | 1.0 | 
| Virgin Territory | 0.57 | 0.43 | -1.0 | 
| Kama Sutra - A Tale of Love | 0.50 | 0.50 | 1.0 | 
| Hostel: Part II | 0.67 | 0.33 | 1.0 | 
| The Book of Eli | 0.82 | 0.18 | 1.0 | 
| The Revenant | 0.86 | 0.14 | 1.0 | 
| Old Dogs | 0.77 | 0.23 | 1.0 | 
| Of Gods and Men | 0.47 | 0.53 | 1.0 | 
| Scream 4 | 0.82 | 0.18 | 1.0 | 
| Easy Virtue | 0.46 | 0.54 | 1.0 | 
| PCU | 0.52 | 0.48 | -1.0 | 
| Next Day Air | 0.44 | 0.56 | 1.0 | 
| Agent Cody Banks 2: Destination London | 0.45 | 0.55 | 1.0 | 
| The Original Kings of Comedy | 0.48 | 0.52 | 1.0 | 
| Dracula Untold | 0.70 | 0.30 | 1.0 | 
| Observe and Report | 0.49 | 0.51 | 1.0 | 
| Strangerland | 0.61 | 0.39 | -1.0 | 
| Prometheus | 0.84 | 0.16 | 1.0 | 
| 10 Days in a Madhouse | 0.49 | 0.51 | -1.0 | 
| The Adventures of Pinocchio | 0.45 | 0.55 | 1.0 | 
| The Express | 0.65 | 0.35 | -1.0 | 
| Rubber | 0.52 | 0.48 | -1.0 | 
| Yeh Jawaani Hai Deewani | 0.55 | 0.45 | 1.0 | 
| Diary of a Wimpy Kid: Dog Days | 0.55 | 0.45 | 1.0 | 
| Signs | 0.79 | 0.21 | 1.0 | 
| Barbarella | 0.84 | 0.16 | -1.0 | 
| Shadow Conspiracy | 0.72 | 0.28 | -1.0 | 
| Chuck & Buck | 0.44 | 0.56 | 1.0 | 
| Detroit Rock City | 0.42 | 0.58 | -1.0 | 
| Centurion | 0.58 | 0.42 | -1.0 | 
| 10th & Wolf | 0.49 | 0.51 | -1.0 | 
| Psycho Beach Party | 0.43 | 0.57 | -1.0 | 
| Penitentiary | 0.85 | 0.15 | 1.0 | 
| A Haunted House | 0.44 | 0.56 | 1.0 | 
| She Done Him Wrong | 0.83 | 0.17 | 1.0 | 
| Sinbad: Legend of the Seven Seas | 0.68 | 0.32 | -1.0 | 
| Clockstoppers | 0.62 | 0.38 | 1.0 | 
| Mad Max 2: The Road Warrior | 0.79 | 0.21 | 1.0 | 
| Race to Witch Mountain | 0.81 | 0.19 | 1.0 | 
| Interstellar | 0.89 | 0.11 | 1.0 | 
| Dudley Do-Right | 0.62 | 0.38 | -1.0 | 
| What Just Happened | 0.61 | 0.39 | -1.0 | 
| The Sleepwalker | 0.43 | 0.57 | -1.0 | 
| Shooting Fish | 0.44 | 0.56 | -1.0 | 
| Clay Pigeons | 0.49 | 0.51 | -1.0 | 
| Conspiracy Theory | 0.87 | 0.13 | 1.0 | 
| Rudderless | 0.53 | 0.47 | -1.0 | 
| Gangster Squad | 0.74 | 0.26 | 1.0 | 
| Serial Mom | 0.62 | 0.38 | -1.0 | 
| Wanderlust | 0.68 | 0.32 | -1.0 | 
| Man of the House | 0.62 | 0.38 | -1.0 | 
| The Red Violin | 0.49 | 0.51 | -1.0 | 
| The Beastmaster | 0.85 | 0.15 | 1.0 | 
| You Can Count on Me | 0.51 | 0.49 | 1.0 | 
| Pontypool | 0.43 | 0.57 | -1.0 | 
| Jawbreaker | 0.42 | 0.58 | 1.0 | 
| How Stella Got Her Groove Back | 0.54 | 0.46 | 1.0 | 
| Anywhere But Here | 0.51 | 0.49 | -1.0 | 
| Valentine's Day | 0.82 | 0.18 | 1.0 | 
| Def-Con 4 | 0.82 | 0.18 | -1.0 | 
| The Adjustment Bureau | 0.71 | 0.29 | 1.0 | 

</p>
</details>

</p>
</details>

<details>
<summary><h1> Conclusions </h1></summary>
<p>
A Random Forest Classifier was developed to predict whether a movie will be a hit or a flop at the box office. After training the model and testing it on unseen data, the model's performance peaked with an accuracy score of 0.70. The model showed some promise for predicting hit movies when it predicted a probability greater than 0.85. 
            
Recommendations for future work:
* training data should include more `flop`s as the data currently favors `hit`s
* more exploration into `cast` and `crew` related features 
* find alternative approaches to handling categorical variables to avoid one-hot encoding

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
[train_vs_test]:https://github.com/wsjk/Capstone_1/blob/master/report/train_vs_test.png
 

