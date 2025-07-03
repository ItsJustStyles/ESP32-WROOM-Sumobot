import board  # Librerías para accesar a I/O de la placa
from ideaboard import IdeaBoard  # Librería de funciones varias del ideaboard
from time import sleep  # Para utilizar función que detiene el código
import wifi
import socketpool

# Instanciación I/O y funciones del Ideaboard
ib = IdeaBoard()

# Configuración de Wi-Fi
ssid = "Nombre_red"
password = "Contraseña_red"

print("Conectando a Wi-Fi...")
wifi.radio.connect(ssid, password)
print("Conectado a Wi-Fi!")
print("Dirección IP:", wifi.radio.ipv4_address)

# Configuración del servidor
pool = socketpool.SocketPool(wifi.radio)
server = pool.socket(pool.AF_INET, pool.SOCK_STREAM)
server.bind((str(wifi.radio.ipv4_address), 80))
server.listen(1)
server.setblocking(True)  # Asegúrate de que el servidor esté en modo bloqueante
print("Esperando una conexión...")

# Comandos de movimiento:
def forward(speed):
    """ Mueve el robot hacia adelante """
    ib.pixel = (0, 255, 0)  # Luz verde
    ib.motor_1.throttle = -speed
    ib.motor_2.throttle = speed

def stop():
    """ Detiene los motores """
    ib.pixel = (0, 0, 0)  # Apaga la luz
    ib.motor_1.throttle = 0
    ib.motor_2.throttle = 0
def backward(speed):
    # Mueve el robot hacia atrás
    # por tiempo t, a velocidad speed = [0,1]    
    ib.pixel = (150,255,0)
    ib.motor_1.throttle = speed
    ib.motor_2.throttle = -speed
def left(speed):
    # Mueve el robot hacia la izquierda
    # por tiempo t, a velocidad speed = [0,1]    
    ib.pixel = (50,55,100)
    ib.motor_1.throttle = speed
    ib.motor_2.throttle = speed
def right(speed):
    # Mueve el robot hacia la derecha
    # por tiempo t, a velocidad speed = [0,1]    
    ib.pixel = (50,55,100)
    ib.motor_1.throttle = -speed
    ib.motor_2.throttle = -speed

min_delay = 0.01  # 10 ms
while True:
    try:
                # Aceptar nuevas conexiones
        try:
            conn, addr = server.accept()
            conn.settimeout(0.5)  # Tiempo límite para leer datos
            print(f"Conexión establecida con: {addr}")
        except OSError:
            # No hay nuevas conexiones, sigue en el loop
            continue
        
        # Usar recv_into() para recibir datos
        buffer = bytearray(15)  # Define un buffer de tamaño adecuado
        bytes_recibidos = conn.recv_into(buffer)

        if bytes_recibidos:
            request = buffer[:bytes_recibidos].decode("utf-8")
            print("Datos recibidos:", request)

            # Procesar la solicitud HTTP para extraer el estado
            if "State=F" in request:
                print("Comando recibido: Mover hacia adelante")
                forward(1)  # Mover a velocidad 1
            elif "State=B" in request:
                backward(1)
            elif "State=R" in request:
                right(1)
            elif "State=L" in request:
                left(1)
            elif "State=S" in request:
                print("Comando recibido: Detener")
                stop()  # Detener motores

            # Responder al cliente con una página HTTP simple
            response = (
                "HTTP/1.1 200 OK\n"
                "Content-Type: text/html\n"
                "Connection: close\n\n"
                "<html><body><h1>Dato recibido correctamente</h1></body></html>"
            )
            conn.send(response.encode("utf-8"))

        conn.close()

    except OSError as e:
        if e.errno == 11:  # EAGAIN o similar
            print("No hay datos disponibles actualmente, reintentando...")
        else:
            print(f"Error inesperado: {e}")

        # Cerrar conexión lo más pronto posible
        conn.close()
        time.sleep(min_delay)  # Retraso mínimo para evitar saturación del procesador
    except KeyboardInterrupt:
        print("Servidor detenido.")
        break
