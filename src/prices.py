import requests
import json
import logging


TICKER_URL = 'https://www.bitstamp.net/api/v2/ticker/'

def getPrices(pair):
    try:
        r = requests.get(TICKER_URL+pair).content
        dict = json.loads(r)
        return dict['last']
    except Exception as e:
        logging.error(f'Error "{e}"" while getting current prices')
        return None

