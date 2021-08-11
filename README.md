# BitcoinPriceLED
 
*Represents the current BTC/USD trend with a RGB LED on a Raspberry Pi Zero WH with Waveshare RGB LED HAT.*

## Hardware

* Raspberry Pi Zero WH [amazon](https://www.amazon.de/Raspberry-Pi-Zero-WH/dp/B07BHMRTTY)
* Waveshare RGB LED Hat [amazon](https://www.amazon.de/Waveshare-RGB-LED-HAT-Expansion/dp/B06ZYLC1BJ)

## Color scale

*Current trend will be displayed using different colors. Positive trend -> green light, negative trend -> red light. Saturation is used to display percentage of price movement.*

![colorscale](/Farbskala.png)

## Installation

### Assembly

### Flash the Micro SD card

### Install dependencies

```shell
sudo apt-get update
sudo apt-get install build-essential python-dev scons swig git python3 python3-pip # add -y at the end to automatically a
```

### Install LED-HAT Python Library

Use the packet installer for Python (pip) to install the rpi_ws281x Python module (which is required to control the LED-HAT using Python)

### Download BitcoinPriceLED

Use Git to clone this repository onto your Raspberry Pi

```shell
git clone https://github.com/Egge7/BitcoinPriceLED.git
```

### Creating systemd service

Create a systemd service that will execute our Python script. This will run the script on startup and in the background, so you don't need to log-in via ssh everytime your Pi looses power

```shell
# create a new service file called 'led.service'
sudo nano /etc/systemd/system/led.service
```

Insert the following lines into the service file. This will execute the Python-script on startup (after network is established) and restart whenever the service fails. It will also execute the off.py script if you stop the service (otherwise the LED panel will stay on)
```
[Unit]
Description=Bitcoin Price LED Service
After=network.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/main.py
ExecStopPost=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/off.py

[Install]
WantedBy=multi-user.target
```
Reload systemctl deamon, enable the new service

```shell
sudo systemctl daemon-reload
sudo systemctl enable led
```

Reboot to check if the new service will start on startup as intended

```shell
sudo reboot
```

