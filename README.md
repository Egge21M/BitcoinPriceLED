# BitcoinPriceLED
 
*Represents the current BTC/USD trend with a RGB LED on a Raspberry Pi Zero WH with Waveshare RGB LED HAT.*

## Hardware

* Raspberry Pi Zero WH [amazon](https://www.amazon.de/Raspberry-Pi-Zero-WH/dp/B07BHMRTTY)
* Waveshare RGB LED Hat [amazon](https://www.amazon.de/Waveshare-RGB-LED-HAT-Expansion/dp/B06ZYLC1BJ)

## Color scale

*Current trend will be displayed using different colors. Positive trend -> green light, negative trend -> red light. Saturation is used to display percentage of price movement.*

![colorscale](/Farbskala.png)

## Installation

### Creating systemd service

```shell
sudo nano /etc/systemd/system/led.service
```

`
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
`

```shell
sudo systemctl daemon-reload
sudo systemctl enable led
```

