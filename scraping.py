import numpy as np 
import pandas as pd 
import requests  
import re
from bs4 import BeautifulSoup  
from tqdm import tqdm
import json

movies = pd.read_csv('data/link.csv') 

def construct_url(imdbId):
    url = ''
    num_of_zeros = 7 - len(str(imdbId))
    url = 'http://www.imdb.com/title/tt' + '0'*num_of_zeros + str(imdbId)
    return url

movies['imdb_url'] = movies['imdbId']
movies['imdb_url'] = movies['imdb_url'].apply(construct_url)

CACHE_FNAME = "poster_urls.json"

try:
    cache_file = open(CACHE_FNAME,"r")
    CACHE_DICTION = json.loads(cache_file.read())
    cache_file.close()
except:
    CACHE_DICTION = {}

imdb_urls = list(movies['imdb_url'])

records = [] 
for url in tqdm(imdb_urls[:]):
    if url in CACHE_DICTION:
        print('Get from cache')
        poster_url = CACHE_DICTION[url]
    else:
        print('Requesting')
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')  
        results = soup.find_all('div', attrs={'class':'poster'}) 
        print(url, results)
        if results == []: 
            continue
        else: 
            first_result = results[0] 
            poster_url = first_result.find('img')['src'] 
            CACHE_DICTION[url] = poster_url
            dumped_json_cache = json.dumps(CACHE_DICTION)
            f = open(CACHE_FNAME,'w')
            f.write(dumped_json_cache)
            f.close()