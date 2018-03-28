#helper functions for EDA
import os
import importlib.util
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from scipy import stats
from tqdm import tqdm_notebook as tqdm
from tqdm import tqdm_pandas
import seaborn as sns
import datetime as dt
tqdm().pandas()


#bootstrap helper function
def draw_bs_reps(data, func, size=1):
    if len(data) == 1:
        x = data[0]
    else:
        x, y = data
    inds = np.arange(len(x))
    bs_reps = np.empty(size)
    
    for i in range(size):
        bs_inds = np.random.choice(inds, size=len(inds))
        bs_x = x.iloc[bs_inds]
        if len(data) > 1:
            bs_y = y.iloc[bs_inds]
            bs_reps[i] = func(bs_x, bs_y)[0] if len(func(bs_x, bs_y)) > 1 else func(bs_x, bs_y)
        else:
            bs_reps[i] = func(bs_x)
    
    return bs_reps

#helper function to compare hits and flops data
def plot_bs_comp(df, col, func, size, bins, split=True):
    if split:
        if isinstance(col, list):
            hits = draw_bs_reps([df[df.net > 0][col[0]],df[df.net > 0][col[1]]], func=func, size=size)
            flops = draw_bs_reps([df[df.net <= 0][col[0]],df[df.net <= 0][col[1]]], func=func, size=size)
        else:
            hits = draw_bs_reps([df[df.net > 0][col]], func=func, size=size)
            flops = draw_bs_reps([df[df.net <= 0][col]], func=func, size=size)
        
        print("95% CI for hits: ", np.percentile(hits, [2.5, 97.5]))
        print("95% CI for flops: ", np.percentile(flops, [2.5, 97.5]))

        _ = plt.hist(hits, normed=True, bins=bins, label="Hits")
        _ = plt.hist(flops, normed=True, bins=bins, label="Flops")
        _ = plt.xlabel(col)
        _ = plt.title('Distribution of ' + col)
    else:
        if isinstance(col, list):
            total = draw_bs_reps([df[col[0]],df[col[1]]], func=func, size=size)
        else:
            total = draw_bs_reps([df[col]], func=func, size=size)
        
        print("95% CI: ", np.percentile(total, [2.5, 97.5]))
        _ = plt.hist(total, normed=True, bins=bins, label="total")

        
    
    plt.legend()

def get_history_to_date(row, d, func, func_col):
    actor = row['name']
    movie = row['movie_id']
    current_movie_release_date = row['release_date']
    df = d[actor] 
    count = func(df[df.release_date < current_movie_release_date][func_col])
    return count

def get_rolling_history(df, col='name', new_col='credits', func=len, func_col='title', show_plot=False):
    keycols = ['movie_id', 'title', 'release_date', 'revenue']
    if func_col not in keycols:
        keycols.append(func_col)
    all_personnel = df[col].unique()
    filmography = {person: df[df[col]==person][keycols].sort_values('release_date').reset_index(drop=True) 
                    for person in tqdm(all_personnel)}
    df[new_col] = df.apply(get_history_to_date, args=(filmography, func, func_col),axis=1)
    
    if show_plot:
        bin_count, _, _ = plt.hist(df[new_col], align='left')
        print(bin_count)
        plt.show()
    return df   


def get_best_worst_personnel(df, sort_cols=('net','sum')):
    hits = df[df.net > 0]
    flops = df[df.net <= 0]

    best = hits.groupby('name')[['net', 'net_pct']].agg(
        ['count', 'max', 'min','sum', 'mean']).sort_values(sort_cols,ascending=False)

    worst = flops.groupby('name')[['net', 'net_pct']].agg(
        ['count', 'max', 'min','sum', 'mean']).sort_values(sort_cols,ascending=False)

    #Only look at actors who have been in at least one film
    best = best[best[sort_cols[0],'count']>1]
    worst = worst[worst[sort_cols[0],'count']>1]


    best_personnel = list(best.head(20).index)

    worst_personnel = list(worst.head(20).index)

    plt.figure()
    _ = df[df['name'].isin(best_personnel)].boxplot(by="name", column=sort_cols[0], figsize=(9, 8), fontsize = 14, vert=False)
    _ = plt.xlabel(sort_cols[0])
    _ = plt.ylabel('Name')
    _ = plt.suptitle("")
    plt.title('The Best')

    plt.figure()
    _ = df[df['name'].isin(worst_personnel)].boxplot(by="name", column=sort_cols[0], figsize=(9, 8), fontsize = 14, vert=False)
    _ = plt.xlabel(sort_cols[0])
    _ = plt.ylabel('Name')
    _ = plt.suptitle("")
    plt.title('The Worst')
    plt.show()

    return best_personnel, worst_personnel

def split_release_date(df):
    df2 = df.copy()
    df2['release_day'] = df['release_date'].apply(lambda x: x.day)
    df2['release_month'] = df['release_date'].apply(lambda x: x.month)
    df2['release_year'] = df['release_date'].apply(lambda x: x.year)
    df2['release_dow'] = df['release_date'].apply(lambda x: x.dayofweek)
    return df2