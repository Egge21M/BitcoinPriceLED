# ------- EDIT -------

# Testmode
# If testing is set to True prices will get updated every 30 seconds
testing = False

# Interval
# Sets the time (in seconds) that the script will wait before getting a net price and updating the trend (default: 900)
# Warning: Small intervals (e.g. 1-10) will result in alot of requests and might get your IP address banned by the API provider.
interval = 900

# Static
# If static is set to True LEDs won't update to represent the Bitcoin price trend, they will have the color defined in staticColor 
static = False
staticColor = (0,0,0)

# Nightmode
# If nightmode is set to True LEDs will be dimmed at certrain times (beginnSleep - stopSleep).
nightmode = True
beginSleep = 22
stopSleep = 7


# ------- DON'T EDIT -------


# LED Strip Config
# If you use the Waveshare LED HAT, recommended on GitHub, you should not need to change these
LED_COUNT = 32
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 5
LED_BRIGHTNESS = 100
LED_INVERT = False