from gpiozero import Button, LED, OutputDevice, MCP3008
from time import sleep 
from enum import Enum,auto
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from bme280 import BME280
class NTC: 
    def __init__(self,t_inf,t_sup,channel): 
        self._t_inf = t_inf
        self._t_sup = t_sup
        self._adc = MCP3008(channel = channel)
    def leer_temperatura(self):
        value = self._adc.value*3.3
        return self._t_inf + value*(self._t_sup - self._t_inf)
class Humedad: 
    def __init__(self,channel): 
        self._adc = MCP3008(channel=channel)
    def leer_humedad(self): 
        valor_adc = self._adc.value
        humedad_percent = valor_adc * 100  # Conversión simple a porcentaje
        return humedad_percent
class calidad: 
    def __init__(self,channel): 
        self._adc = MCP3008(channel=channel)
    def leer_calidad(self): 
        voltaje = self._adc.value*3.3
        ppm = (voltaje - 0.4) * 100 
        return ppm

def main(): 
    ventilador = OutputDevice(20)
    ntc = NTC(0,50,0)
    humedad = Humedad(1)
    calidad1 = calidad(3)
    lista_temperaturas = []
    lista_humedades = []
    lista_presion = []
    lista_calidad = []
    led_referencia = LED(22)
    led_2 = LED(17)
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus) 
    while True: 
        temperatura = ntc.leer_temperatura()
        hum = humedad.leer_humedad()
        pres = bme280.get_pressure()
        cal = calidad1.leer_calidad()
        if temperatura > 25: 
            print(f'Temperatura muy elevada tomando un valor de: {temperatura}')
            ventilador.on()
        elif temperatura < 25: 
            print(f'La temperatura es menor de 25 grados por lo cual no hay problema: {temperatura}')
            ventilador.off()
        if hum > 60: 
            print(f'Cuidado al humedad es muy elevada recomendamos conectar el humidificador: {hum}')
        elif hum < 60: 
            print(f'Humedad correcta')
        print(f'Hay una presiona atmosferica de: {pres}')
        if cal >100:
            print(f'La calidad del aire es mala con un valor de: {cal}')
            led_referencia.on()
            led_2.off()
        elif cal < 100: 
            print(f'Toda correcto la calidad de aire en clase es buena: {cal}')
            led_referencia.off() 
            led_2.on()
        lista_temperaturas.append(temperatura)
        lista_humedades.append(hum)
        lista_presion.append(pres)
        lista_calidad.append(cal)
        sleep(3) #Se duerme un segundo para ver mejor la visualizacion 
if __name__ == "__main__": 
    try: 
        main()
    except KeyboardInterrupt: 
        print(f'Programa interrumpido por el usuario')

