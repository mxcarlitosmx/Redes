import socket
import time

HOST = "0.0.0.0"
PORT = 65432
BUFFER_SIZE = 1024

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print("--- SERVIDOR TCP listo---")

        conn, addr = s.accept()
        with conn:
            #Recibir tamaño esperado
            filesize = int(conn.recv(BUFFER_SIZE).decode())
            conn.send(b"LISTO")
            
            print(f"Recibiendo archivo de {filesize} bytes...")
            
            #Inicio medicion
            inicio_tiempo = time.time()
            recv_bytes = 0
            num_bloques = 0
            
            with open("recibido.txt", "wb") as f:
                while recv_bytes < filesize:
                    chunk = conn.recv(BUFFER_SIZE)
                    if not chunk: break
                    
                    num_bloques += 1
                    
                    if b"EOT" in chunk:
                        clean_data = chunk.replace(b"EOT", b"")
                        f.write(clean_data)
                        recv_bytes += len(clean_data)
                        break
                    
                    f.write(chunk)
                    recv_bytes += len(chunk)

            fin_tiempo = time.time()
            #Fin de medicion

            tiempo_total = fin_tiempo - inicio_tiempo
            throughput = (recv_bytes / tiempo_total) if tiempo_total > 0 else 0

            print("\n" + "="*30)
            print("Estadisticas")
            print("="*30)
            print(f"Tamaño del archivo: {recv_bytes} bytes")
            print(f"Bloques recibidos:  {num_bloques}")
            print(f"Tiempo total:       {tiempo_total:.4f} segundos")
            print(f"Throughput:         {throughput:.2f} bytes/seg")
            print(f"Mecanismo de fin:   EOT detectado")
            print("="*30)

if __name__ == "__main__":
    iniciar_servidor()
