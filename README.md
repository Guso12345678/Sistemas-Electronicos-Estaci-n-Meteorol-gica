# Estación Meteorológica Inteligente con Raspberry Pi

Proyecto final de la asignatura **Sistemas Electrónicos** (IMAT — Comillas ICAI).  
Estación meteorológica personal construida sobre Raspberry Pi 4 que mide temperatura, humedad, presión atmosférica y calidad del aire en tiempo real, con actuadores automáticos y un dashboard web accesible desde cualquier dispositivo.

---

## Descripción

El sistema lee continuamente cuatro variables ambientales mediante sensores conectados a los pines GPIO de la Raspberry Pi, actúa de forma autónoma sobre un ventilador y LEDs indicadores según los umbrales detectados, y expone los datos en tiempo real a través de una API REST servida con Flask y visualizada en un dashboard HTML.

---

## Estructura del proyecto

```
estacion-meteorologica/
├── proyecto_definitivo.py   # Sistema principal: lectura de sensores y control de actuadores
├── pagina_web.py            # Servidor Flask con API REST para el dashboard
├── pagina.html              # Dashboard web (actualización automática cada 3 s)
└── README.md
```

| Archivo | Descripción |
|---|---|
| `proyecto_definitivo.py` | Bucle principal: lee sensores, activa ventilador y LEDs, registra datos |
| `pagina_web.py` | Servidor Flask que expone `/data` como JSON y sirve el dashboard |
| `pagina.html` | Interfaz web con jQuery que consulta la API cada 3 segundos |

---

## Hardware utilizado

### Sensores

| Sensor | Modelo | Variable | Rango | Precisión | Interfaz |
|---|---|---|---|---|---|
| Temperatura | NTC (termistor) | Temperatura | −40 °C a 85 °C | ±0,5 °C | ADC (MCP3008) |
| Humedad | YL-69 (capacitivo) | Humedad relativa | 0 % a 100 % RH | ±2 % RH | ADC (MCP3008) |
| Presión + Temp | BME280 | Presión atmosférica | 300–1100 hPa | ±1 hPa | I²C |
| Calidad del aire | MQ-135 | CO₂ / gases | 400–5000 ppm | ±50 ppm | ADC (MCP3008) |

### Actuadores

| Componente | Pin GPIO | Control | Descripción |
|---|---|---|---|
| Ventilador | GPIO 20 | Digital on/off | Se activa cuando T > 25 °C |
| LED rojo (alerta) | GPIO 22 | Digital | Se enciende si calidad del aire > 100 ppm |
| LED verde (OK) | GPIO 17 | Digital | Se enciende si calidad del aire ≤ 100 ppm |

### Conversión analógico-digital

Los sensores NTC, YL-69 y MQ-135 proporcionan señal analógica. Se usa el **MCP3008** (ADC de 10 bits vía SPI) para convertir esas señales antes de leerlas con `gpiozero`.

---

## Cómo ejecutar

**Requisitos:** Raspberry Pi 4 con Raspberry Pi OS, sensores conectados según el esquema de hardware.

```bash
pip install gpiozero smbus2 bme280 flask
```

**Sistema principal (sensores + actuadores):**
```bash
python proyecto_definitivo.py
```

**Dashboard web:**
```bash
python pagina_web.py
```

Acceder desde cualquier dispositivo en la misma red a:
```
http://<IP-de-la-raspberry>:5000
```

---

## Lógica de control (`proyecto_definitivo.py`)

El bucle principal se ejecuta cada 3 segundos y aplica las siguientes reglas:

| Condición | Acción |
|---|---|
| Temperatura > 25 °C | Ventilador ON |
| Temperatura ≤ 25 °C | Ventilador OFF |
| Humedad > 60 % | Alerta por consola |
| Calidad del aire > 100 ppm | LED rojo ON, LED verde OFF |
| Calidad del aire ≤ 100 ppm | LED verde ON, LED rojo OFF |

Los datos se acumulan en listas en memoria (`lista_temperaturas`, `lista_humedades`, `lista_presion`, `lista_calidad`) para registro histórico.

### Clases de sensores

```python
class NTC:          # Temperatura vía divisor de tensión + ADC
class Humedad:      # Humedad capacitiva vía ADC, escala 0–100 %
class calidad:      # Calidad del aire: voltaje ADC convertido a ppm
```

---

## Dashboard web (`pagina_web.py` + `pagina.html`)

El servidor Flask expone dos rutas:

- `GET /` — sirve el dashboard HTML
- `GET /data` — devuelve JSON con los valores actuales del BME280:

```json
{
  "temperatura": 22.35,
  "presion": 1013.25,
  "humedad": 48.70
}
```

El dashboard actualiza los valores automáticamente cada 3 segundos mediante una llamada jQuery a `/data`, sin necesidad de recargar la página.

---

## Circuitos de acondicionamiento

**Sensor NTC (temperatura):** divisor de tensión con resistencia de referencia de 10 kΩ. El voltaje de salida se calcula como:

```
V_out = V_in × R_NTC / (R_NTC + R_ref)
```

**Sensor YL-69 (humedad):** resistencia pull-up con conversión ADC vía I²C/SPI mediante MCP3008.

**BME280 (presión):** comunicación I²C directa a la Raspberry Pi, sin acondicionamiento externo necesario.

**MQ-135 (calidad del aire):** divisor de tensión con resistencia de carga de ~10 kΩ para adaptar la señal al rango del ADC (máximo 5 V del sensor → 3,3 V del MCP3008).

**Ventilador:** controlado por señal PWM a 25 kHz desde un pin GPIO configurado como salida.

---

## Tecnologías

- Python 3 en Raspberry Pi 4
- `gpiozero` — control de GPIO, LEDs, actuadores y ADC (MCP3008)
- `smbus2` / `bme280` — lectura del sensor BME280 vía I²C
- `flask` — servidor web y API REST
- HTML + jQuery — dashboard con actualización en tiempo real
- Protocolo I²C y SPI para comunicación con sensores

---

## Autores

- **Guzmán Ignacio Pérez Ibarz**
- **Pablo Mauricio Güell Borrajo**

Proyecto final — Sistemas Electrónicos, Grado en Ingeniería Matemática e Inteligencia Artificial (IMAT), Comillas ICAI.
