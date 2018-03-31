import os
import sys
import pandas as pd
import numpy as np
from scipy import stats
from tqdm import tqdm_notebook as tqdm
from tqdm import tqdm_pandas
import datetime as dt
import calendar
import sklearn
import pickle


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


# parameters and ranges to plot
param_grid = {
  "bootstrap":[True],
  "oob_score": [True,False],
  "n_estimators": np.arange(10, 500, 10),
  "max_depth": np.arange(10, 500, 10),
  "min_samples_split": np.arange(2,150,1),
  "min_samples_leaf": np.arange(2,60,1),
  "max_leaf_nodes": np.arange(2,60,1),
  'max_features': ['auto','log2','sqrt',None],
  'criterion': ['gini', 'entropy'],
              }

rf = RandomForestClassifier()
rf_random = RandomizedSearchCV(
  estimator=rf,
  param_distributions=param_grid,
  n_iter=500,
  cv=3,
  verbose=True,
  random_state=42,
  n_jobs=-1,
  scoring='accuracy'
)

rf_random.fit(x_train, y_train)

print(rf_random.best_params_)

print(rf_random.cv_results_)

df = pd.DataFrame.from_dict(rf_random.cv_results_)
df.to_csv('random_rf_cvresults.csv',index=False)

filename = 'random_rf.sav'
pickle.dump(rf_random, open(filename, 'wb'))