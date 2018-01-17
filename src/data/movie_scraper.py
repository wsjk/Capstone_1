import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from re import sub
from decimal import Decimal
import numpy as np
import re

from tqdm import tqdm_notebook as tqdm

import os
import importlib.util


def row_scrape_movie_data(row):
    missing_movie_dict = {}
    url = 'https://www.the-numbers.com/'
    
    url2 = ""
    movie_url = ""
    title, release_date = row.title, row.release_date
    title_search_url = title.replace(' ', '+')
    #movie title search result page url
    query = '{}search?searchterm={}&searchtype=allmatches'.format(url,title_search_url)
    search_page = requests.get(query)
    search_soup = BeautifulSoup(search_page.content, 'html.parser')

    budget, revenue = np.nan, np.nan
    urls = [] #to keep track of urls in search_page
    tables = search_soup.find_all('div', id='page_filling_chart')

    if 'No movie match found' in tables[1].find('p').get_text():
        row.budget = np.nan
        row.revenue = np.nan
        row.movie_url = np.nan
        return row

    # if there is more than one movie returned in search, pick the one that matches release date year
    for link in tables[1].find_all('a'):
        if "/movie" in link.get('href') or "/daily" in link.get('href'):
            urls.append(link.get('href'))

    if not urls: #if no urls are found
        url2 = ""
    elif len(urls) <= 1: #there should always be at least 2 links if movie title search is successful
        url2 = ""
    else:
        for i in range(0,len(urls)):
            pattern = re.compile(r'.+/daily/(.+)$')
            if 'daily' in urls[i]:
                web_release_date = dt.strptime(re.match(pattern,urls[i]).group(1), '%Y/%m/%d')
            else:
                continue
            if web_release_date.year in range(release_date.year-3,release_date.year+3):
                #if date matches, then the next href link will be the correct link
                #for financial details of the movie
                url2 = urls[i+1]
                break
        else:
            url2=""
    del search_soup, search_page
    movie_url = url + url2

    if url2:
        #financial details extracted from movie page
        movie_page = requests.get(movie_url)
        movie_soup = BeautifulSoup(movie_page.content, 'html.parser')

        #scrape worldwide box office revenue
        table = movie_soup.find('table', id='movie_finances')
        tds = table.find_all('td')
        for i in range(len(tds)):
            if tds[i].get_text() == "Worldwide Box Office":
                revenue = tds[i+1].get_text()
                break
        #scrape production budget
        heading = movie_soup.find('h2', text='Movie Details')
        tds = heading.parent.find_all('td')
        for i, td in enumerate(tds):
            if 'budget' in td.get_text().lower():
                budget = tds[i+1].get_text()
                break

    row.budget = budget
    row.revenue = revenue
    row.movie_url = movie_url
    return row

