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

### Install Python Library

### Download BitcoinPriceLED

```shell
git clone https://github.com/Egge7/BitcoinPriceLED.git
```

### Creating systemd service

```shell
sudo nano /etc/systemd/system/led.service
```

`[Unit]
Description=Bitcoin Price LED Service
After=network.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/main.py
ExecStopPost=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/off.py

[Install]
WantedBy=multi-user.target`

```shell
sudo systemctl daemon-reload
sudo systemctl enable led
```

