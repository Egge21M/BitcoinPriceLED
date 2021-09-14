from flask import Flask, render_template, request
import os

app = Flask(__name__)

def convertToInt(color):
    cleanInput = color[-6:]
    rValue = int(cleanInput[0:2], 16)
    gValue = int(cleanInput[2:4], 16)
    bValue = int(cleanInput[4:6], 16)
    return(rValue,gValue,bValue)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/update/" ,methods=['POST'])
def updateData():
    staticChoice = request.form.get('static')
    nightmodeChoice = request.form.get('nightmode')
    beginSleep = request.form.get('startNightmode')
    stopSleep = request.form.get('stopNightmode')
    interval = request.form.get('interval')
    colorHex = request.form.get('colorValue')
    print(staticChoice)
    print(nightmodeChoice)
    print(interval)
    print(request.form)
    configFile = open('/home/pi/BitcoinPriceLED/src/config.py')
    stringList = configFile.readlines()
    configFile.close()
    
    if staticChoice == 'true':
        colorRGB = convertToInt(colorHex)
        stringList[2] = 'static=True\n'
        stringList[3] = f'staticColor ={colorRGB}\n'
    else:
        stringList[2] = 'static=False\n'
    
    if nightmodeChoice == 'true':
        stringList[4] = 'nightmode=True\n'
        stringList[5] = f'beginSleep={beginSleep}\n'
        stringList[6] = f'stopSleep={stopSleep}\n'
    else:
        stringList[4] = 'nightmode=False\n'

    if interval is not None:
        stringList[1] = f'interval={interval}\n'

    with open('/home/pi/BitcoinPriceLED/src/config.py', 'w') as file:
        newContent = ''.join(stringList)
        print(newContent)
        file.write(newContent)
    os.system('sudo systemctl restart led')

    forward_message = "Updated cofig file... restarting service"
    return render_template('index.html', forward_message=forward_message)

@app.route('/stream')
def stream():
    def generate():
        with open('/home/pi/BitcoinPriceLED/led.log') as file:
            return file.read()
    return app.response_class(generate(), mimetype='text/plain')

@app.route('/reboot')
def reboot():
    os.system('sudo reboot')
    system_message = "Rebooting LED now..."
    return render_template('index.html', system_message=system_message)

@app.route('/shutdown')
def shutdown():
    os.system('sudo shutdown -h now')
    system_message = "Shutting down now..."
    return render_template('index.html', system_message=system_message)

if __name__ == "__main__":
    app.run(host='0.0.0.0')

