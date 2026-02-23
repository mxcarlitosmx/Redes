import socket
import time

# Configuración
HOST = "0.0.0.0"
PORT = 65432
BUFFER_SIZE = 1024

def iniciar_servidor_udp():
    # Creacion socket UDP (SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, PORT))
    
    print("\n--- SERVIDOR UDP LISTO PARA ESTADÍSTICAS ---")
    
    # 1. Recibir metadatos 
    data, addr = s.recvfrom(BUFFER_SIZE)
    paquetes_esperados = int(data.decode())
    print(f"Conectado con: {addr}")
    print(f"Paquetes que el cliente promete enviar: {paquetes_esperados}")
    
    paquetes_recibidos = 0
    bytes_totales = 0
    s.settimeout(3.0) # si no llega un dato en tres segundos se termina
    
    inicio_tiempo = time.time()
    
    try:
        while True:
            data, addr = s.recvfrom(BUFFER_SIZE)
            if data == b"EOT":
                break
            paquetes_recibidos += 1
            bytes_totales += len(data)
    except socket.timeout:
        print("\n[!] Tiempo de espera agotado. Calculando perdidas...")

    fin_tiempo = time.time()
    
    # Cálculos 
    tiempo_final = fin_tiempo - inicio_tiempo 
    if paquetes_recibidos < paquetes_esperados:
        tiempo_final -= 3.0 
        
    paquetes_perdidos = paquetes_esperados - paquetes_recibidos
    porcentaje_perdida = (paquetes_perdidos / paquetes_esperados) * 100
    throughput = bytes_totales / tiempo_final if tiempo_final > 0 else 0

    # estadisticas
    print("\n" + "="*40)
    print("Estadisticas UDP")
    print("="*40)
    print(f"Paquetes enviados (Cliente): {paquetes_esperados}")
    print(f"Paquetes recibidos (Servidor): {paquetes_recibidos}")
    print(f"Paquetes perdidos:           {paquetes_perdidos}")
    print(f"Porcentaje de perdida:       {porcentaje_perdida:.2f}%")
    print(f"Tiempo total:                {tiempo_final:.4f} seg")
    print(f"Throughput:                  {throughput:.2f} bytes/seg")
    print("="*40)
    s.close()

if __name__ == "__main__":
    iniciar_servidor_udp()
