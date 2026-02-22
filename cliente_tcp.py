import socket
import os
import time

# Configuración
IP_SERVIDOR = "TU_IP_DE_LINUX" # <--- CAMBIA ESTO por la IP de tu VM
PORT = 65432
BUFFER_SIZE = 1024
ARCHIVO = "archivo_prueba.txt" # Asegúrate de que este archivo exista

def enviar_archivo():
    if not os.path.exists(ARCHIVO):
        print(f"Error: El archivo {ARCHIVO} no existe.")
        return

    tamano_total = os.path.getsize(ARCHIVO)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            print(f"Conectando al servidor {IP_SERVIDOR}...")
            s.connect((IP_SERVIDOR, PORT))
            
            # 1. Enviamos el tamaño del archivo
            s.sendall(str(tamano_total).encode())
            
            # Esperamos confirmación del servidor
            if s.recv(BUFFER_SIZE) == b"LISTO":
                print("Iniciando envío fragmentado...")
                
                with open(ARCHIVO, "rb") as f:
                    while True:
                        bloque = f.read(BUFFER_SIZE)
                        if not bloque:
                            # Al terminar, enviamos el marcador de fin solicitado
                            s.sendall(b"EOT")
                            break
                        s.sendall(bloque)
                
                print("¡Archivo enviado y marcador EOT entregado!")
            
        except Exception as e:
            print(f"Error durante la conexión: {e}")

if __name__ == "__main__":
    enviar_archivo()