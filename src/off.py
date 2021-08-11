from rpi_ws281x import *
from config import LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_BRIGHTNESS, LED_INVERT

strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

strip.begin()

for i in range(0, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
strip.show()
exit(1)