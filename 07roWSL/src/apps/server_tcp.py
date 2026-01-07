#!/usr/bin/env python3
"""
Server TCP Echo
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un server TCP simplu care returnează (echo) mesajele primite.
Folosit pentru demonstrarea conectivității TCP și a filtrării.
"""

from __future__ import annotations

import argparse
import socket
import sys
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


def gestioneaza_client(conn: socket.socket, adresa: tuple[str, int]):
    """
    Gestionează o conexiune de client.
    
    Args:
        conn: Socket-ul conexiunii
        adresa: Tuplu (ip, port) al clientului
    """
    ip_client, port_client = adresa
    logheaza(f"Conexiune nouă de la {ip_client}:{port_client}")
    
    try:
        while True:
            date = conn.recv(4096)
            
            if not date:
                logheaza(f"Client {ip_client}:{port_client} deconectat")
                break
            
            mesaj = date.decode('utf-8', errors='replace')
            logheaza(f"Primit de la {ip_client}:{port_client}: {mesaj.strip()}")
            
            # Echo - trimite înapoi același mesaj
            conn.sendall(date)
            logheaza(f"Trimis către {ip_client}:{port_client}: {mesaj.strip()}")
            
    except ConnectionResetError:
        logheaza(f"Conexiune resetată de {ip_client}:{port_client}")
    except Exception as e:
        logheaza(f"Eroare cu {ip_client}:{port_client}: {e}")
    finally:
        conn.close()


def porneste_server(host: str, port: int):
    """
    Pornește serverul TCP echo.
    
    Args:
        host: Adresa pe care să asculte
        port: Portul pe care să asculte
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((host, port))
        server_socket.listen(5)
        
        logheaza(f"Server TCP Echo pornit pe {host}:{port}")
        logheaza("Așteptare conexiuni...")
        
        while True:
            try:
                conn, adresa = server_socket.accept()
                gestioneaza_client(conn, adresa)
            except KeyboardInterrupt:
                logheaza("Server oprit de utilizator")
                break
                
    except OSError as e:
        logheaza(f"Eroare la pornirea serverului: {e}")
        sys.exit(1)
    finally:
        server_socket.close()


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Server TCP Echo pentru Laboratorul Săptămânii 7"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Adresa pe care să asculte (implicit: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9090,
        help="Portul pe care să asculte (implicit: 9090)"
    )
    args = parser.parse_args()

    porneste_server(args.host, args.port)


if __name__ == "__main__":
    main()
