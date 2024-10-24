import socket, network
from machine import Pin
import esp, gc

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

led = Pin(13, Pin.OUT)