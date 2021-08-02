from prices import getPrices
import time
from datetime import datetime

import logging

logging.basicConfig(filename='error.log')

def checkTrend(oldPrice, currentPrice):
    trend = float(currentPrice) / float(oldPrice)
    return trend

def priceUpdater(currentPrice):
    oldPrice = currentPrice
    currentPrice = getPrices('BTCUSD')
    return currentPrice, oldPrice


def run():
    currentPrice = getPrices('BTCUSD')
    while True:
        time.sleep(300)
        try:
            prices = priceUpdater(currentPrice)
            oldPrice = prices[1]
            currentPrice = prices[0]
            trend = checkTrend(oldPrice, currentPrice)
            now = datetime.now()
            if trend > 1:
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: +{trend-1}%')
            elif trend < 1:
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: -{1-trend}%')
        
        except Exception as e:
            logging.error(f'Error while checking prices and trend')
            print(f'Error: Preistrend konnte nicht abgerufen werden')

run()


