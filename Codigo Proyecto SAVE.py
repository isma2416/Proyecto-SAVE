from machine import Pin, SPI
from ili9341 import Display, color565
from xglcd_font import XglcdFont
import network
import machine
import time
import usocket as socket
import esp
esp.osdebug(None)
import gc
gc.collect()
# Configura el UART
uart = machine.UART(1, baudrate=9600, tx=21, rx=22) 
# Define las pines utilizadas para las filas y columnas del teclado matricial
columnas = [Pin(27, Pin.IN, Pin.PULL_UP), Pin(26, Pin.IN, Pin.PULL_UP), Pin(25, Pin.IN, Pin.PULL_UP)]
filas = [Pin(32, Pin.OUT), Pin(33, Pin.OUT)]
#Define la variable que contiene los datos
Respuesta = 0
Mats=[]
# Define la matriz de teclado (2x3)
teclado = [
    ['1', '2', '3'],
    ['4', '5', '6']
]
# Configura SPI para la pantalla ILI9341
spi = SPI(1, baudrate=10000000, sck=Pin(18), mosi=Pin(23))
display = Display(spi, dc=Pin(4), cs=Pin(5), rst=Pin(17))
# Configura una fuente para la pantalla
espresso_dolce = XglcdFont('fonts/EspressoDolce18x24.c', 18, 24)

#Escanea el teclado matricial
def scan_teclado():
    for fila in range(2):
        filas[fila].value(0)
        for col in range(3):
            if columnas[col].value() == 0:
                filas[fila].value(1)  # Restaurar el valor de la fila
                return teclado[fila][col]
        filas[fila].value(1)
    return None  # Devolver None si no se ha presionado ninguna tecla


def Menu():

      C=0
      A=0
      H=0
      P=0
      display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
      display.fill_rectangle(20,280,20,20, color565 (255,0,0))
      display.draw_text(20, 270, 'Incorrecto' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
      display.fill_rectangle(230,310,10,10, color565 (255,0,0))
      
      display.fill_rectangle(50,280,20,20, color565 (0,255,0))
      display.draw_text(50, 270, 'Correcto' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
      display.fill_rectangle(80,280,20,20, color565 (255,255,255))
      display.draw_text(80, 270, 'Generar vale' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
      display.fill_rectangle(110,280,20,20, color565 (0,0,0))
      display.draw_text(110, 270, 'Entregar vale' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
      display.fill_rectangle(140,280,20,20, color565 (255,255,0))
      display.draw_text(140, 270, 'Retroceder' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
      display.fill_rectangle(170,280,20,20, color565 (0,0,255))
      display.draw_text(170, 270, 'Reportar problema' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
      
      tecladomenu()
      
def tecladomenu():
    tecla = None
    while tecla is None:
        # Escaneo del teclado matricial
        tecla = scan_teclado()
        if tecla:
            print("Tecla presionada:", tecla)
            tecla_presionada = tecla
            procesar_tecla(tecla_presionada)
def accion_tecla_1():
    print("Acción para tecla 1")
    tecladomenu()

def accion_tecla_2():
    print("Acción para tecla 2")
    pantalla_espera()
    

def accion_tecla_3():
    print("Acción para tecla 3")

# Define un diccionario que asocia las teclas con las acciones
acciones = {
    '1': accion_tecla_1,
    '2': accion_tecla_2,
    '3': accion_tecla_3
}

def displaysino():
    display.draw_text(180, 85, 'Si' , espresso_dolce,
                                  color565(0, 365, 0),color565(128, 128, 200), landscape=True)
    display.draw_text(180, 275, 'No ', espresso_dolce,
                                  color565(255, 0, 0),color565(128, 128, 200), landscape=True)
def procesar_tecla(tecla):
    # Verifica si la tecla está en el diccionario de acciones
    tecla_presionada = None
    if tecla in acciones:
        # Ejecuta la acción asociada a la tecla presionada
        acciones[tecla]()
    else:
        print("Tecla no válida")
        tecla_presionada = tecla
        
    
def pantalla_espera():
    display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
    display.draw_text(30, 295, 'Escanea tu codigo ' , espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
    ssid = 'MycroPython-AP'
    password = '70enproyecto'
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while ap.active() == False:
      pass

    print('Connection successful')
    print(ap.ifconfig())
    receive_and_display_data()
def receive_and_display_data():
    data=0
    print(data)
    while data==0:
        if uart.any():
            data = uart.read(10)  # Read up to 10 bytes of data from GM65
            if data:
                # Limit the data to 8 characters
                
                time.sleep(1)
                display.clear()#Limpia la pantalla
                display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
                print("Codigo:", data.decode('utf-8'))
                decodificado =data.decode('utf-8')#Decodifica el dato que se encuentra en data
                display.draw_text(30, 285, 'Tu codigo es: ' + decodificado[:8], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
                displaysino()
    horario(decodificado)

def horario(decodificado):
    Respuesta = None
    while Respuesta is None:
        # Escaneo del teclado matricial
        tecla = scan_teclado()
        
        if tecla == '3':
            print("Si")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            display.draw_text(30, 285, "Ingresa la hora", espresso_dolce,
                              color565(200, 200, 200), color565(128, 128, 200), landscape=True)
            global C
            C = decodificado
            hora()
            Respuesta = "Si"
        elif tecla == '1':
            print("No")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            print("No")
            display.draw_text(30, 285, "Escanea denuevo ", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(60, 285, "el codigo", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            receive_and_display_data()
            Respuesta = "No"



def hora ():
    print(hora)
    data=0
    print(data)
    while data==0:
        if uart.any():
            data = uart.read(10)  # Read up to 10 bytes of data from GM65
            if data:
                # Limit the data to 8 characters
                
                time.sleep(1)
                print("Hora:", data.decode('utf-8'))
                decodificado =data.decode('utf-8')
                display.draw_text(120, 285, 'Hora: ' + decodificado[:5], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
                displaysino()
    salon(decodificado)

def salon(decodificado):
    Respuesta = None
    while Respuesta is None:
        # Escaneo del teclado matricial
        tecla = scan_teclado()
        
        if tecla == '3':
            print("Si")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            display.draw_text(30, 285, "Escanea el salon", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(50, 285, "en que trabajaras", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
                    
            global H
            H = decodificado
            aula()
            Respuesta = "Si"
        elif tecla == '1':
            print("No")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            print("No")
            display.draw_text(30, 285, "Escanea denuevo ", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(60, 285, "la hora", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            hora ()
            Respuesta = "No"
            
def aula():
    print(aula)
    data=0
    print(data)
    while data==0:
        if uart.any():
            data = uart.read(10)  # Read up to 10 bytes of data from GM65
            if data:
                # Limit the data to 8 characters
                
                time.sleep(1)
                print("Aula", data.decode('utf-8'))
                decodificado =data.decode('utf-8')
                display.draw_text(120, 285, 'Aula: ' + decodificado[:6], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
                displaysino()
    
    Profe(decodificado)
def Profe(decodificado):
    Respuesta = None
    while Respuesta is None:
        # Escaneo del teclado matricial
        tecla = scan_teclado()
        
        if tecla == '3':
            print("Si")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            display.draw_text(30, 285, "Escanea el codigo", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(50, 285, "de tu profesor", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            global A
            A = decodificado
            Docente()
            Respuesta = "Si"
        elif tecla == '1':
            print("No")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            print("No")
            display.draw_text(30, 285, "Escanea denuevo ", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(60, 285, "el codigo de aula", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            Respuesta=1
            aula()   
            Respuesta = "No"
    
    
    
    
def Docente():
    print(Docente)
    data=0
    print(data)
    while data==0:
        if uart.any():
            data = uart.read(10)  # Read up to 10 bytes of data from GM65
            if data:
                # Limit the data to 8 characters
                
                time.sleep(1)
                print("Profesor", data.decode('utf-8'))
                decodificado =data.decode('utf-8')
                display.draw_text(120, 285, 'Profesor: ' + decodificado[:6], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
                displaysino()
    Materiales(decodificado)
    
def Materiales(decodificado):
    Respuesta = None
    while Respuesta is None:
        # Escaneo del teclado matricial
        tecla = scan_teclado()
        
        if tecla == '3':
            print("Si")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            display.draw_text(30, 285, "Escanea el codigo", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(50, 285, "de tu profesor", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            m_scaneados = []
            m_max = 13
            print("Escaneando materiales")
            for _ in range(m_max):
                data = 0
                print(data)
                while data ==0:
                    if uart.any():
                        data = uart.read(10)
                        if data:
                            time.sleep(1)
                            print("Material:", data.decode('utf-8'))
                            material_decodificado = data.decode('utf-8')
                            m_scaneados.append(material_decodificado)
                            display.draw_text(120, 300, 'Material: ' + material_decodificado[:6], espresso_dolce,
                                              color565(200, 200, 200), color565(128, 128, 200), landscape=True)
                            displaysino()
                            if input("¿Desea detener el escaneo? (y/n): ").lower() == 'y':
                                break
                        print("Escaneo de materiales completado.")
            return m_scaneados
    
                    
def Pantallafinal():
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            display.draw_text(30, 285, "Generando vale...", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(50, 285, "Espere 1 segundo", espresso_dolce,
                                         color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            print("C",C)
            print("H",H)
            print("A",A)
            print("P",P)
            time.sleep(3)
            Vale()
            
            
def Vale():
    display.clear()
    display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
    display.draw_text(40, 285, 'Codigo: ' + C[:8], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
    display.draw_text(70, 285, 'Hora: ' + H[:4], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
    display.draw_text(100, 285, 'Aula: ' + A[:6], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
    display.draw_text(130, 285, 'Profesor: ' + P[:6], espresso_dolce,
                                  color565(200, 200, 200),color565(128, 128, 200), landscape=True)
    confirmarvale()
    
def confirmarvale():
    Respuesta = None
    while Respuesta is None:
        # Escaneo del teclado matricial
        tecla = scan_teclado()
        if tecla == '3':
            print("Si")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            display.draw_text(30, 285, "Enviando vale", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            Menu()
            Respuesta = "Si"
        elif tecla == '1':
            print("No")
            display.clear()
            display.fill_rectangle(10, 10, 220, 300, color565(128, 128, 200))
            print("No")
            display.draw_text(30, 285, "Escanea denuevo ", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            display.draw_text(60, 285, "el codigo", espresso_dolce,
                                          color565(200, 200, 200),color565(128, 128, 200), landscape=True)
            Pantallafinal()
            Respuesta = "No"
    
def wifiprint():
    html = """<html><head><meta name="viewport" content="width=device-width, initial-scale=1">
    <meta http-equiv="refresh" content="10"></head>
    <body>
    <h1>Vale generado</h1>
    <p>31 de octubre</p>
    <p></p>
    <p>Valor de A: """ + str(C) + """</p>
    <p>Valor de H: """ + str(H) + """</p>
    <p>Valor de A: """ + str(A) + """</p>
    <p>Valor de P: """ + str(P) + """</p>
    </body></html>"""
    return html
    server(s)
def server(s):
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 80))
    s.listen(5) 
    print("subido al wifi")
    while True:
      conn, addr = s.accept()
      print('Got a connection from %s' % str(addr))
      request = conn.recv(1024)
      print('Content = %s' % str(request))
      response = web_page()
      conn.send(response)
      conn.close()
  
    
                            
try:
    Menu()
    
except KeyboardInterrupt:
    uart.deinit()  # Libera el UART al salir del programa

