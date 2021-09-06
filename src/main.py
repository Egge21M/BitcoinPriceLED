from os import stat
import time
import atexit
from datetime import datetime
from rpi_ws281x import *

from prices import getPrices
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT
from config import testing, nightmode, beginSleep, stopSleep, static, staticColor, interval

import logging

logging.basicConfig(filename='/home/pi/BitcoinPriceLED/led.log', filemode='w', level=logging.DEBUG)

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
    if changePercentage > 2.5:
        return 0
    elif changePercentage > 0.5:
        return 90
    elif changePercentage >=0:
        return 180

def staticLight():
    strip.begin()
    while True:
        
        # Checks nightmode and adjusts brightness accordingly
        now = datetime.now()
        hour = int(now.strftime('%H'))
        if nightmode == True and hour >= beginSleep or hour < stopSleep:
            strip.setBrightness(1)
        else:
            strip.setBrightness(100)
        
        for i in range(0, strip.numPixels()):
                strip.setPixelColor(i, Color(staticColor))
        strip.show()
        time.sleep(900)


def main():
    currentPrice = getPrices('BTCUSD')
    errorCount = 0
    strip.begin()
    while True:
        now = datetime.now()
        
        # Checks nightmode and adjusts brightness accordingly

        hour = int(now.strftime('%H'))
        if nightmode == True and hour >= beginSleep or hour < stopSleep:
            strip.setBrightness(1)
            nightmodeActive = True
        else:
            strip.setBrightness(100)
            nightmodeActive = False
        brightness = strip.getBrightness()

        try:
            prices = priceUpdater(currentPrice)
            oldPrice = prices[1]
            currentPrice = prices[0]
            changePercentage = prices[3]
            trend = prices[2]
            
            if trend == '+':
                logging.info(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: +{changePercentage}% - Nightmode: {nightmodeActive}, Brightness: {brightness}')
                r = colorPicker(changePercentage)
                g = 255
                b = 0
                errorCount= 0

            elif trend == '-':
                logging.info(f'Uhrzeit: {now.strftime("%H:%M:%S")} - Alter Preis: {oldPrice}, aktueller Preis: {currentPrice}, Trend: -{changePercentage}% - Nightmode: {nightmodeActive}, Brightness: {brightness}')
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

        time.sleep(interval)


if __name__ == "__main__":
    try:
        if static != True:
            main()
        else:
            staticLight()
    except KeyboardInterrupt:
        exit_handler

atexit.register(exit_handler)
