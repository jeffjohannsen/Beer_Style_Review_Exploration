# WARNING: IN PROGRESS
# TODO: Finish testing, Turn into function

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import pprint

if __name__ == "__main__":

    url = 'https://api.foursquare.com/v2/venues/search'

    params = dict(
    client_id='',
    client_secret='',
    v='20201025',
    # ll='40.7243,-74.0018',
    # near='Denver',
    query='New Belgium',
    categoryId='50327c8591d4c4b30a586d5d', # Brewery
    limit=3
    )
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)

    print(data)

    pprint.pprint(data['response']['venues'][0])
