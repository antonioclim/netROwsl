#!/usr/bin/env python3
"""
Exemplu 1: Server și Client TCP de bază
Demonstrează conceptele fundamentale ale socket programming.
"""
import socket
import sys

def server(port: int = 8080):
    """Pornește un server TCP simplu."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', port))
        s.listen(5)
        print(f"[SERVER] Ascult pe portul {port}...")
        
        while True:
            conn, addr = s.accept()
            print(f"[SERVER] Conexiune de la {addr}")
            with conn:
                data = conn.recv(1024)
                print(f"[SERVER] Primit: {data.decode()}")
                response = b"OK: " + data.upper()
                conn.sendall(response)
                print(f"[SERVER] Trimis: {response.decode()}")

def client(host: str = '127.0.0.1', port: int = 8080, message: str = 'Test'):
    """Trimite un mesaj la server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[CLIENT] Trimit: {message}")
        s.sendall(message.encode())
        response = s.recv(1024)
        print(f"[CLIENT] Răspuns: {response.decode()}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'server':
        server()
    else:
        client(message=' '.join(sys.argv[1:]) if len(sys.argv) > 1 else 'Hello')
