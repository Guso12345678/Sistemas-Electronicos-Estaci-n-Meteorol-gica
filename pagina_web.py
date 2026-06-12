from flask import Flask, jsonify, render_template
from smbus2 import SMBus
from bme280 import BME280

app = Flask(__name__)

# Inicializa el sensor BME280
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/data')
def data():
    temperatura = bme280.get_temperature()
    presion = bme280.get_pressure()
    humedad = bme280.get_humidity()
    return jsonify({'temperatura': temperatura, 'presion': presion, 'humedad': humedad})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
