import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
from re import sub
from decimal import Decimal
import numpy as np
import re
import os
import pandas as pd
import numpy as np

def row_scrape_movie_data(row, data_type):
    missing_movie_dict = {}
    url = 'https://www.the-numbers.com/'    
    url2, movie_url = "",""
    row.budget, row.revenue, row.movie_url = np.nan, np.nan, np.nan
    title, release_date = row.title, row.release_date
    title_search_url = title.replace(' ', '+')
     
    #movie title search result page url
    query = '{}search?searchterm={}&searchtype=allmatches'.format(url,title_search_url)
    search_page = requests.get(query)
    search_soup = BeautifulSoup(search_page.content, 'html.parser')

    urls = [] #to keep track of urls in search_page
    tables = search_soup.find_all('div', id='page_filling_chart')

    if 'No movie match found' in tables[1].find('p').get_text():
        return row

    # if there is more than one movie returned in search, pick the one that matches release date year
    for link in tables[1].find_all('a'):
        if "/movie" in link.get('href') or "/daily" in link.get('href'):
            urls.append(link.get('href'))

    if not urls or len(urls)<=1: #if no urls are found
        return row
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
            return row

    movie_url = url + url2
    row.movie_url = movie_url

    if url2:
        movie_page = requests.get(movie_url)
        movie_soup = BeautifulSoup(movie_page.content, 'html.parser')
        if data_type == 'financial':
            #financial details extracted from movie page
            #scrape worldwide box office revenue
            table = movie_soup.find('table', id='movie_finances')
            tds = table.find_all('td')
            box_office = []
            for i in range(len(tds)):
                if "Box Office" in tds[i].get_text():
                    money = tds[i+1].get_text()
                    box_office.append(Decimal(sub(r'[^\d.]', '', money)))
            
            if box_office:
                revenue = max(box_office)
            else:
                revenue = np.nan
                
            #scrape production budget
            heading = movie_soup.find('h2', text='Movie Details')
            tds = heading.parent.find_all('td')
            for i, td in enumerate(tds):
                if re.match('^production.+budget.+', td.get_text().lower()):
                    budget = Decimal(sub(r'[^\d.]', '', tds[i+1].get_text()))
                    break
            else:
                budget = np.nan

            row.budget = budget
            row.revenue = revenue

        elif data_type == 'runtime':
            #scrape production budget
            heading = movie_soup.find('h2', text='Movie Details')
            tds = heading.parent.find_all('td')
            for i, td in enumerate(tds):
                if re.match('^running.+time.+', td.get_text().lower()):
                    runtime =  int(tds[i+1].get_text().split()[0])
                    break
            else:
                runtime = np.nan
            row.runtime = runtime
    return row

