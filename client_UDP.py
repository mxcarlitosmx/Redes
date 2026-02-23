import socket
import os
import time

# Configuracion
IP_SERVIDOR = "192.168.1.88" 
PORT = 65432
BUFFER_SIZE = 1024
ARCHIVO = "archivo_prueba.txt"

def enviar_archivo_udp():
    if not os.path.exists(ARCHIVO):
        print("Error: No existe el archivo de prueba.")
        return

    tamano = os.path.getsize(ARCHIVO)
    # Calcular cuantos bloques de 1024 bytes salen
    num_paquetes = (tamano // BUFFER_SIZE) + (1 if tamano % BUFFER_SIZE != 0 else 0)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    print(f"Iniciando envío UDP a {IP_SERVIDOR}...")
    
    #Se envia el numero total de paquetes primero
    s.sendto(str(num_paquetes).encode(), (IP_SERVIDOR, PORT))
    time.sleep(0.5) # Breve pausa para que el servidor se prepare
    
    inicio = time.time()
    with open(ARCHIVO, "rb") as f:
        for i in range(num_paquetes):
            bloque = f.read(BUFFER_SIZE)
            if not bloque: break
            s.sendto(bloque, (IP_SERVIDOR, PORT))
            time.sleep(0.0005) 
            
    #Marcador de fin
    s.sendto(b"EOT", (IP_SERVIDOR, PORT))
    fin = time.time()
    
    print(f"Envio terminado en {fin - inicio:.4f} segundos.")
    s.close()

if __name__ == "__main__":
    enviar_archivo_udp()
