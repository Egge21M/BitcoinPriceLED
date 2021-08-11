from prices import getPrices
import time
import atexit
from datetime import datetime
from rpi_ws281x import *
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, testing

import logging

logging.basicConfig(filename='error.log')

errorCount = 0

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)


def priceUpdater(currentPrice):
    oldPrice = currentPrice
    currentPrice = getPrices('BTCUSD')
    change = float(currentPrice) - float(oldPrice)
    changePercentage = (abs(change)/float(oldPrice))*100
    if change > 0:
        trend= '+'
    else:
        trend= '-'
    return currentPrice, oldPrice, trend, changePercentage


def exit_handler():
    strip.begin()
    for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()
                    

def colorPicker(changePercentage):
    if changePercentage > 4:
        return 0
    elif changePercentage > 3:
        return 20
    elif changePercentage > 2:
        return 40
    elif changePercentage > 1:
        return 60
    elif changePercentage >=0:
        return 80

def main():
    currentPrice = getPrices('BTCUSD')
    errorCount = 0
    while True:
        now = datetime.now()
        try:
            strip.begin()
            prices = priceUpdater(currentPrice)
            oldPrice = prices[1]
            currentPrice = prices[0]
            changePercentage = prices[3]
            trend = prices[2]
            
            if trend == '+':
                logging.info(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: +{changePercentage}%')
                r = colorPicker(changePercentage)
                g = 255
                b = 0
                errorCount= 0

            elif trend == '-':
                logging.info(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: -{changePercentage}%')
                r = 255
                g = colorPicker(changePercentage)
                b = 0
                errorCount = 0
            
            for i in range(0, strip.numPixels()):
                strip.setPixelColor(i, Color(r,g,b))
            strip.show()         


        except Exception as e:
            errorCount += 1
            logging.error(f'{now.strftime("%d/%m/%Y %H:%M:%S")} - ERROR: {e}')
            
            if errorCount > 3:
                now = datetime.now()
                logging.error(f'{now.strftime("%d/%m/%Y %H:%M:%S")} - ERROR-Mode activated - Currently {errorCount} failures in a row: {e}')
                
                for i in range(0, strip.numPixels()):
                    strip.setPixelColor(i, Color(230,0,125))
                strip.show()
    
        if testing == True:
            time.sleep(10)
        else:
            time.sleep(300)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit_handler

atexit.register(exit_handler)
