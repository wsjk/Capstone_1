import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from tqdm import tqdm_notebook as tqdm
from tqdm import tqdm_pandas
import datetime as dt
import calendar
import pickle
import ast

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
from sklearn import utils

current_file_path = os.path.abspath(os.path.join("__file__" ,"../../.."))
nb_path = os.path.abspath(os.path.join(current_file_path, 'notebooks'))
os.chdir(nb_path)

import get_features

print(current_file_path)
features_path = os.path.abspath(os.path.join(nb_path,'features.csv'))
_ = get_features.get_features()

df = pd.read_csv(features_path)

df = df.set_index(['movie_id', 'title'])

feature_list = df.drop('target',axis=1).columns

features = np.array(df.drop('target',axis=1))
labels = df['target']

x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state = 42)

param_grid = {
  "n_estimators": np.arange(200, 400, 20),
  "max_depth": np.arange(250, 400, 10),
  "min_samples_split": np.arange(2,40,4),
  "min_samples_leaf": np.arange(1,10,1),
  "max_leaf_nodes": np.arange(30,60,5)
              }

rf = RandomForestClassifier(bootstrap=True, max_features='sqrt', criterion='gini', oob_score=True, random_state=42)

grid_search = GridSearchCV(estimator = rf, param_grid = param_grid, 
                          cv = 5, n_jobs = -1, verbose = 0, return_train_score=True)

grid_search.fit(x_train, y_train)

best_grid = grid_search.best_estimator_

filename = 'rf_final.sav'
pickle.dump(grid_search, open(filename, 'wb'))

res_df = pd.DataFrame.from_dict(grid_search.cv_results_)
res_df.to_csv('rf_final_results.csv', index=False)

print(grid_search.best_params_)
print(grid_search.best_estimator_)
print(best_grid.score(x_test,y_test))
print(confusion_matrix(best_grid.predict(x_test), y_test))
print(best_grid.predict_proba(x_test))

for feature in zip(feature_list, best_grid.feature_importances_):
    print(feature)