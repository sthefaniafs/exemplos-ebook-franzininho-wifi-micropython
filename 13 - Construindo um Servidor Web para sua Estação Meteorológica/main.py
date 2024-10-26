def read_sensor():
  global temp, hum, p, alt
  temp = p = alt = hum = 0
  try:
    # coletando umidade e temperatura
    d.measure()
    temp = d.temperature()
    hum = d.humidity()
    #coletando pressão e altitude
    p = round(bmp180.pressure, 2)
    alt = round(bmp180.altitude, 2)
    msg = (b'{0:.0f},{1:.0f},{2:3.1f},{3:3.1f}'.format(temp, hum, p, alt))
    return(msg)
  except OSError as e:
    return('Failed to read sensor.')

def odor_sensor():
    if mq135.value():
        return ("Gás tóxico: não detectado")
    else:
        return ("Gás tóxico: detectado")

def rain_sensor():
    if sensor_chuva.value():
        return("Chuva: não detectada")
    else:
        return("Chuva: detectada")
        
def web_page():
    odor = odor_sensor() # obter o valor do odor
    rain = rain_sensor() # obter o valor do sensor de chuva
    html = """<!DOCTYPE HTML><html>
        <head>
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <meta http-equiv="refresh" content="3">
          <meta charset="UTF-8">
          <script src="https://kit.fontawesome.com/ae775d017c.js" crossorigin="anonymous"></script>
          <style>
            html {
             font-family: Arial;
             display: inline-block;
             margin: 0px auto;
             text-align: center;
            }
            h2 { font-size: 3.0rem; }
            p { font-size: 3.0rem; }
            .units { font-size: 2.2rem; }
            .dht-labels{
              font-size: 1.5rem;
              vertical-align:middle;
              padding-bottom: 15px;
            }
            .left-column {
              float: left;
              width: 50%; /* Define a largura da coluna esquerda */
            }
            .right-column {
              float: right;
              width: 50%; /* Define a largura da coluna direita */
            }
            
          </style>
        </head>
        <body>
            <h2>Estação Meteorológica Franzininho</h2>
            <div class="left-column">
                <p>
                    <i class="fa-solid fa-temperature-three-quarters" style="color: #f46315;"></i> 
                    <span class="dht-labels">Temperatura</span> 
                    <span>"""+str(temp)+"""</span>
                    <sup class="units">&deg;C</sup>
                </p>
                <p>
                    <i class="fas fa-tint" style="color:#00add6;"></i> 
                    <span class="dht-labels">Umidade</span>
                    <span>"""+str(hum)+"""</span>
                    <sup class="units">%</sup>
                </p>
                <p>
                   <i class="fa-solid fa-cloud-showers-heavy" style="color: #36a3f7;"></i>
                   <span class="dht-labels"><b>"""+rain+"""</b></span>
                </p>
            </div>
            
            <div class="right-column">
                <p>
                    <i class="fa-solid fa-gauge-high" style="color: #08ba46;"></i>
                    <span class="dht-labels">Pressão</span> 
                    <span>"""+str(p)+"""</span>
                    <sup class="units">Pa</sup>
                </p>
                <p>
                    <i class="fa-solid fa-mountain-sun" style="color: #296ea3;"></i>
                    <span class="dht-labels">Altitude</span>
                    <span>"""+str(alt)+"""</span>
                    <sup class="units">m</sup>
                </p>
                <p>
                    <i class="fa-solid fa-skull-crossbones" style="color: #e60000;"></i>
                    <span class="dht-labels"><b>"""+odor+"""</span>
                </p>
            </div>
            
        </body>
    </html>"""
    return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)
  
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    sensor_readings = read_sensor()
    print(sensor_readings)
    response = web_page()
    conn.send("HTTP/1.1 200 OK\n")
    conn.send("Content-Type: text/html\n")
    conn.send("Connection: close\n\n")
    conn.sendall(response)
    conn.close()