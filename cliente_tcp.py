import socket
import os
import time

#Configuracion
IP_SERVIDOR = "192.168.1.88"
PORT = 65432
BUFFER_SIZE = 1024
ARCHIVO = "archivo_prueba.txt" 

def enviar_archivo():
    if not os.path.exists(ARCHIVO):
        print(f"Error: No se encuentra el archivo {ARCHIVO}")
        return

    tamano_total = os.path.getsize(ARCHIVO)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"Conectando al servidor {IP_SERVIDOR}...")
            s.connect((IP_SERVIDOR, PORT))
            
            #Enviar el tamaño 
            s.sendall(str(tamano_total).encode())
            
            #Esperar el "LISTO" del server
            confirmacion = s.recv(BUFFER_SIZE)
            
            if confirmacion == b"LISTO":
                print(f"Enviando {tamano_total} bytes en bloques de {BUFFER_SIZE}...")
                inicio = time.time()
                
                with open(ARCHIVO, "rb") as f:
                    while True:
                        bloque = f.read(BUFFER_SIZE)
                        if not bloque:
                            #Al terminar, enviar el marcador de fin
                            s.sendall(b"EOT")
                            break
                        s.sendall(bloque)
                
                fin = time.time()
                print(f"¡Envio completado en {fin - inicio:.4f} segundos!")
                print("Marcador EOT enviado.")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    enviar_archivo()


