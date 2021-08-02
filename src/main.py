from prices import getPrices
import time
from datetime import datetime
from neopixel import *

import logging

logging.basicConfig(filename='error.log')

errorCount = 0

# LED Strip Config
LED_COUNT = 32
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 100
LED_INVERT = False

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)



def checkTrend(oldPrice, currentPrice):
    quotient = float(currentPrice) / float(oldPrice)
    if quotient >= 1: 
        trend = quotient - 1
        return 1, trend
    elif quotient < 1:
        trend = 1 - quotient
        return 0, trend

def priceUpdater(currentPrice):
    oldPrice = currentPrice
    currentPrice = getPrices('BTCUSD')
    return currentPrice, oldPrice


def run():
    currentPrice = getPrices('BTCUSD')
    errorCount = 0
    while True:
        time.sleep(300)
        try:
            strip.begin()
            prices = priceUpdater(currentPrice)
            oldPrice = prices[1]
            currentPrice = prices[0]
            trend = checkTrend(oldPrice, currentPrice)
            now = datetime.now()
            if errorCount > 3:
                logging.error(f'ERROR-Mode activated - Currently {errorCount} failures in a row')
                color = (247,147,26)
                errorCount = 0

            if trend[0] == 1:
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: +{trend[1]}%')
                color = (0, 255, 0)
                errorCount= 0

            elif trend == 0:
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: -{trend[1]}%')
                color = (255, 0, 0)
                errorCount = 0
        
        except Exception as e:
            errorCount += 1
        for i in range(0, strip.numPixels()):
            strip.setPixelColor(i, Color(color[0],color[1],color[2]))
            strip.show()
            time.sleep(0.1)


run()


