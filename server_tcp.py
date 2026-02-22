import socket

# Configuración
HOST = "0.0.0.0"  # Escucha conexiones externas (Windows)
PORT = 65432
BUFFER_SIZE = 1024 # Tamaño del bloque de fragmentación

def iniciar_servidor():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"--- SERVIDOR TCP INICIADO ---")
        print(f"Esperando conexión en el puerto {PORT}...")

        conn, addr = s.accept()
        with conn:
            print(f"Conectado con el cliente: {addr}")
            
            # 1. Recibir el tamaño del archivo primero
            data_size = conn.recv(BUFFER_SIZE).decode()
            filesize = int(data_size)
            print(f"Tamaño del archivo a recibir: {filesize} bytes")
            
            # Enviar confirmación para empezar
            conn.send(b"LISTO")

            recv_bytes = 0
            with open("archivo_recibido_tcp.txt", "wb") as f:
                while recv_bytes < filesize:
                    # Recibimos en fragmentos de 1024
                    chunk = conn.recv(BUFFER_SIZE)
                    if not chunk:
                        break
                    
                    # Verificamos si el fragmento trae el marcador de fin
                    if b"EOT" in chunk:
                        # Guardamos solo los datos antes del marcador
                        clean_data = chunk.replace(b"EOT", b"")
                        f.write(clean_data)
                        recv_bytes += len(clean_data)
                        print("Mecanismo de fin 'EOT' detectado.")
                        break
                    
                    f.write(chunk)
                    recv_bytes += len(chunk)
                    print(f"Progreso: {recv_bytes}/{filesize} bytes recibidos")

            print("--- Transferencia completada con éxito ---")

if __name__ == "__main__":
    iniciar_servidor()