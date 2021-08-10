from prices import getPrices
import time
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

def colorPicker(changePercentage):
    if changePercentage > 4:
        return 0
    elif changePercentage > 3:
        return 40
    elif changePercentage > 2:
        return 80
    elif changePercentage > 1:
        return 120
    elif changePercentage >=0:
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
            changePercentage = prices[3]
            trend = prices[2]
            

            if trend == '+':
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: +{changePercentage}%')
                r = colorPicker(changePercentage)
                g = 255
                b = 0
                errorCount= 0

            elif trend == '-':
                print(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: -{changePercentage}%')
                r = 255
                g = colorPicker(changePercentage)
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


