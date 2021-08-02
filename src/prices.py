import requests
import json

TICKER_URL = 'https://www.bitstamp.net/api/v2/ticker/'

def getPrices(pair):
    r = requests.get(TICKER_URL+pair).content
    dict = json.loads(r)
    return dict['last']