from prices import getPrices
import time
from datetime import datetime
from rpi_ws281x import *
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT, testing

import logging

logging.basicConfig(filename='error.log')

errorCount = 0

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)



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

def colorPicker(trend):
    if trend > 0.4:
        return 0
    elif trend > 0.3:
        return 40
    elif trend > 0.2:
        return 80
    elif trend > 0.1:
        return 120
    elif trend >=0:
        return 160

def main():
    currentPrice = getPrices('BTCUSD')
    errorCount = 0
    while True:
        if testing == True:
            time.sleep(10)
        else:
            time.sleep(300)

        now = datetime.now()
        try:
            strip.begin()
            prices = priceUpdater(currentPrice)
            oldPrice = prices[1]
            currentPrice = prices[0]
            trend = checkTrend(oldPrice, currentPrice)

            if trend[0] == 1:
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: +{trend[1]}%')
                r = colorPicker(trend[1])
                g = 255
                b = 0
                errorCount= 0

            elif trend == 0:
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: -{trend[1]}%')
                r = 255
                g = colorPicker(trend[1])
                b = 0
                errorCount = 0

            if testing == True:
                print(r,g,b)
            
            for i in range(0, strip.numPixels()):
                strip.setPixelColor(i, Color(r,g,b))
                strip.show()
            

        except Exception as e:
            errorCount += 1
            if errorCount > 3:
                logging.error(f'ERROR-Mode activated - Currently {errorCount} failures in a row')
                for i in range(0, strip.numPixels()):
                    strip.setPixelColor(i, Color(247,147,26))
                    strip.show()
                    time.sleep(0.1)


if __name__ == "__main__":
    main()


