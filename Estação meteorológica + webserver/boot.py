import socket, network
from machine import Pin, SoftI2C
import esp, gc, dht
from bmp180 import BMP180

# gerenciador de memória
esp.osdebug(None)
gc.collect()

# dados da rede
ssid = 'SUBSTITUA_PELO_SEU_SSID'
password = 'SUBSTITUA_PELA_SUA_SENHA'

# configurando como cliente
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# caso já esteja conectado
if wlan.isconnected() == False:
    wlan.connect(ssid, password)

# espere conectar
while wlan.isconnected() == False:
    pass

print('connected!')
print(wlan.ifconfig())

# atribuição de pinos da Franzininho 
i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

# configurando DHT
d = dht.DHT11(Pin(15))

# configurando BMP180
bmp180 = BMP180(i2c)
bmp180.oversample_sett = 2
bmp180.baseline = 101325

# configurando pino do MQ135
mq135= Pin(5,Pin.IN)

#configurando sensor de chuva
sensor_chuva= Pin(2, Pin.IN)