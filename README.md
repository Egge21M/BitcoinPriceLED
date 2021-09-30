# BitcoinPriceLED
 
*LED-lamp that represents the current Bitcoin price trend. Comes with a handy web-remote.*

![Prototype V1](/pictures/LED.jpg)
*BitcoinPriceLED in a prototype case made by [HODLITEMS](https://hodlitems.com/).*

## Content
[BitcoinPriceLED](#bitcoinpriceled)
  * [Hardware](#hardware)
  * [Color scale](#color-scale)
  * [🛠️ Installation](#%EF%B8%8F-installation)
    + [💿 Flashing the OS (& enabling SSH and Wifi)](#-flashing-the-os--enabling-ssh-and-wifi)
    + [🔨 Assembly](#-assembly)
    + [👨‍💻 Logging in via SSH](#-logging-in-via-ssh)
    + [🏗️ Install dependencies](#%EF%B8%8F-install-dependencies)
    + [🚧 Install LED-HAT Python Library](#-install-led-hat-python-library)
    + [📁 Download BitcoinPriceLED](#-download-bitcoinpriceled)
    + [👷 Creating systemd services](#-creating-systemd-services)
      - [Creating led.service](#creating-ledservice)
      - [Creating ledServer.service](#creating-ledserverservice)
  * [🧰 Optional: Configure your BitcoinPriceLED](#-optional-configure-your-bitcoinpriceled)
      - [🎨 Static](#-static)
      - [⏱️ Interval](#%EF%B8%8F-interval)
      - [💤 Nightmode](#-nightmode)
  * [🧡 Donations](#-donations)



## Hardware

* Raspberry Pi Zero WH [amazon](https://www.amazon.de/Raspberry-Pi-Zero-WH/dp/B07BHMRTTY)
* Waveshare RGB LED Hat [amazon](https://www.amazon.de/Waveshare-RGB-LED-HAT-Expansion/dp/B06ZYLC1BJ)
* 1A/5W USB Charger
* Micro-USB Cable

* HODLITEMS Case [HODLITEMS](https://hodlitems.com/shop/)


## Features

### Colorscale

*Current trend will be displayed using different colors. Positive trend -> green light, negative trend -> red light. Saturation is used to display percentage of price movement.*

![colorscale](/pictures/Farbskala.png)

### Web-Remote

*BitcoinPriceLED comes with a handy remote that is hosted accessible via your browser.*

![Webinterface](/pictures/Webinterface.jpg)

## 🛠️ Installation

### 💿 Flashing the OS (& enabling SSH and Wifi)

The easiest way to get your Raspberry Pi Zeros OS ready is to use the [Raspberry PI Imager](https://www.raspberrypi.org/software/). Download, install and launch the software, choose "Raspberry Pi OS Lite" from "Raspberry Pi OS (other)". Hit CTRL+Shift+X to bring up the advanced options. Enable SSH (which will be used later to control your Pi), enter a password for user "pi" and setup a custom hostname (eg. led.local). Enable Wifi and enter your WIFIs ssid and passkey.

Optional: You can also configure a timezone (which might be usefull if you plan on using time-controlled features like nightmode).

You can also download and flash the OS manually. You can find all avaiable Raspberry Pi OS [here](https://www.raspberrypi.org/software/operating-systems/).

### 🔨 Assembly

Insert your microSD card into your Raspberry Pi Zero and put the LED-HAT on. Then connect the power plug.

### 👨‍💻 Logging in via SSH

Because our device has neither a display nor any peripherals you will need to control it using SSH and another machine. On your computer open up your OS' CLI (Windows: PowerShell, MacOS/Linux: Terminal) and connect to your Pi using the follwing command

```shell
ssh pi@<hostname>
```

If you setup a custom hostname, replace <hostname> with your custom one. If you didn't you can lookup the Pis IP by checking connected devices in your routers admin panel. Your CLI will ask you for the password you chose during the OS setup.

### 🏗️ Install dependencies

Before you can run the Python-code that will make your LED light up, you will need to install some depented-upon software.

```shell
sudo apt-get update
sudo apt-get install git python3-pip
```

### 🚧 Install LED-HAT Python Library

Use the packet installer for Python (pip) to install rpi_ws281x module (which is required to control the LED-HAT using Python) and Flask (which will act as a local mini-webserver that hosts the webinterface)

```shell
sudo pip3 install rpi_ws281x flask
```

### 📁 Download BitcoinPriceLED

Use Git to clone this repository onto your Raspberry Pi

```shell
git clone https://github.com/Egge7/BitcoinPriceLED.git
```

### 👷 Creating systemd services

#### Creating led.service

Create a systemd service that will execute our Python scripts. This will run the script on startup and in the background, so you don't need to log-in via ssh everytime your Pi looses power

create a new service file called 'led.service'

```shell
sudo nano /etc/systemd/system/led.service
```

Insert the following lines into the service file. This will execute the Python-script on startup (after network is established) and restart whenever the service fails. It will also execute the off.py script if you stop the service (otherwise the LED panel will stay on)
```
[Unit]
Description=Bitcoin Price LED Service
After=network-online.target

[Service]
Type=simple
Restart=always
ExecStart=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/main.py
ExecStopPost=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/off.py

[Install]
WantedBy=multi-user.target
```
#### Creating ledServer.service

Now create a second service called ledServer.service. This second service file starts the server for the webinterface.

```shell
sudo nano /etc/systemd/system/ledServer.service
```

and insert the follwing lines into the service file.

```
[Unit]
Description=Bitcoin Price LED Server Service
After=network-online.target

[Service]
Type=simple
User=pi
Group=pi
Restart=always
ExecStart=/usr/bin/python3 /home/pi/BitcoinPriceLED/src/server/app.py

[Install]
WantedBy=multi-user.target
```

Reload systemctl deamon, enable the new services

```shell
sudo systemctl daemon-reload
sudo systemctl enable led
sudo systemctl enable ledServer
```

Reboot to check if the new service will start on startup as intended

```shell
sudo reboot
```

## 🧰 Optional: Configure your BitcoinPriceLED

By default your LED will run 24/7 and represent current price-trends in a 30 minute loop.
BitcoinPriceLED comes with a webinterface to configure your LED. In your local network, simply open <hostname of your Pi>:5000 and adjust the settings to your liking.

#### 🎨 Static

Default: False

This will stop your BitcoinPriceLED from representing the current Bitcoin prices and make it shine in a desired color. Simply switch on Staticmode and enter the HEX-Value (e.g. #FFFF00 for blue) of the desired color

#### ⏱️ Interval

Default: 900

This is the time in seconds your BitcoinPriceLED will wait before fetching a new price and calculating the trend. Please be aware that a very small interval (1-10 seconds) might result in your IP address getting blocked by the API provider.

#### 💤 Nightmode

Default: False

Nightmode dims your LED at night. In order to activate this feature set "nightmode = True" and set the time where your LED should enter and leave nightmode (beginSleep and endSleep in 24h format).

## 🧡 Donations 

Please feel free to copy, fork and alter this project as you wish. If you would like to support me, you can leave a on-chain or lightning donation in my [tip-jar](https://tallyco.in/Egge/)
