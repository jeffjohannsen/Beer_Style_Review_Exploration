import warnings
warnings.filterwarnings('ignore')
from pymongo import MongoClient
import pprint
import copy
import pandas as pd
# Requests sends and receives HTTP requests.
import requests
# Beautiful Soup parses HTML documents in python.
from bs4 import BeautifulSoup


def scrape_brewery_lists(states_to_scrape, collection_to_save_in):
    client = MongoClient('localhost', 27017)

    states = states_to_scrape
    # state = 'washington'
    for state in states:
        base_url = f'https://www.brewtrail.com/{state}-breweries/'

        r = requests.get(base_url)
        status_code = r.status_code
        if status_code != 200:
            print(f'non-200 status code error for {state}.')
            continue

        soup = BeautifulSoup(r.content, "html")
        # print(soup.prettify())
        div = soup.find("div", {"class": "large-8 columns panel-content"})
        table = div.find("table")
        # print(table.prettify())
        rows = table.find_all("tr")

        all_rows = []
        empty_row = {"brewery_name": None, "brewery_location": None}

        # The first row contains header information, so we are skipping it.
        for row in rows[1:]:
            new_row = copy.copy(empty_row)
            # A list of all the entries in the row.
            columns = row.find_all("td")
            new_row['brewery_name'] = columns[0].text.strip()
            new_row['brewery_location'] = columns[2].text.strip()
            all_rows.append(new_row)

        # pprint.pprint(all_rows[:10])

        db = client.brewery_location_info
        collection = db[collection_to_save_in]

        for row in all_rows:
            collection.insert_one(row)

if __name__ == '__main__':
    
    states = ['colorado', 'california', 'oregon', 'michigan', 'washington']
    scrape_brewery_lists(states, 'Combined_Breweries')