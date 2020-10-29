# WARNING: IN PROGRESS
# TODO: Finish full testing across the combined api calls 
# TODO: Test on loop of search terms
# TODO: Turn into function

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import pprint
import copy

API_KEY = ''

if __name__ == '__main__':

    # Place Search 
    # Unable to fully eliminate location bias 
    # Trying Autocomplete as a workaround

    search_term = 'Odell'

    url = f'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={search_term}&inputtype=textquery&locationbias=circle:1941370@41.973675,-105.572500&fields=formatted_address,name,rating,geometry/location,place_id&key={API_KEY}'

    resp = requests.get(url=url)
    resp.status_code

    data = json.loads(resp.text)
    status_code = data['status']
    print(status_code)

    pprint.pprint(data)


    # Places Autocomplete
    # Needs testing

    def autocomplete_search(search_terms, API_KEY):
        """[summary]

        Args:
            search_terms ([type]): [description]
            API_KEY ([type]): [description]

        Returns:
            [type]: [description]
        """
        list_of_search_terms = search_terms # import from beer_advocate dataframe
        results = []
        empty_row = {"brewery_name_original": None, "brewery_name_google": None,"brewery_address": None, "brewery_location": None, 'place_id': None, 'rating': None, 'review_count': None}
        error_1 = (0, 0)
        error_2 = (0, 0)
        successes = 0

        for term in list_of_search_terms:
            ac_search_term = "Hop Nation Brewery"
            ac_url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={term}&locationbias=circle:1941370@41.973675,-105.572500&types=establishment&key={API_KEY}'
            ac_resp = requests.get(url=ac_url)
            status_code_1 = ac_resp.status_code
            if status_code_1 != 200:
                error_1[0] += 1
                continue

            ac_data = json.loads(ac_resp.text)
            status_code_2 = ac_data['status']
            if status_code_2 not in ['OK', 'ZERO_RESULTS']:
                print(f'Error on {term}: {status_code_2}')
                continue
            elif status_code_2 != 'OK':
                error_2[0] += 1
                continue
            
            search_place_id = ac_data['predictions'][0]['place_id']
            
            # Place Details Search
            
            place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={search_place_id}&fields=name,formatted_address,geometry/location,rating,user_ratings_total&key={API_KEY}'
            details = requests.get(url=place_details_url)
            status_code_3 = details.status_code
            if status_code_3 != 200:
                error_1[1] += 1
                continue
            
            details_data = json.loads(details.text)
            status_code_4 = details_data['status']
            if status_code_4 not in ['OK', 'ZERO_RESULTS']:
                print(f'Error on {term}: {status_code_4}')
                continue
            elif status_code_4 != 'OK':
                error_2[1] += 1
                continue
            
            new_row = copy.copy(empty_row) 
            new_row['brewery_name_original'] = term
            new_row['brewery_name_google'] = details_data['result']['name']
            new_row['brewery_address'] = details_data['result']['formatted_address']
            new_row['brewery_location'] = details_data['result']['geometry']['location']
            new_row['place_id'] = ac_data['predictions'][0]['place_id']
            new_row['rating'] = details_data['result']['rating']
            new_row['review_count'] = details_data['result']['user_ratings_total']
            results.append(new_row)
            successes += 1

        return (results, f'error_1: {error_1}, error_2: {error_2}, successes: {successes}')
        
    # ac_search_term = "Hop Nation Brewery"
    
    ac_search_term_1 = 'New Glarus Brewing'
    ac_search_term_2 = ac_search_term_1[:15]
    print(ac_search_term_2)
    ac_url = f'https://maps.googleapis.com/maps/api/place/autocomplete/json?input={ac_search_term_2}&locationbias=circle:1941370@41.973675,-105.572500&types=establishment&key={API_KEY}'

    ac_resp = requests.get(url=ac_url)
    ac_resp.status_code

    ac_data = json.loads(ac_resp.text)
    ac_status_code = ac_data['status']
    print(ac_status_code)

    pprint.pprint(ac_data['predictions'][0:3])
    ac_place_id = ac_data['predictions'][0]['place_id']

    search_place_id = ac_place_id

    place_details_url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={search_place_id}&fields=name,formatted_address,geometry/location,rating,user_ratings_total&key={API_KEY}'

    details = requests.get(url=place_details_url)
    details.status_code

    details_data = json.loads(details.text)
    details_status_code = details_data['status']
    print(details_status_code)

    pprint.pprint(details_data['result'])