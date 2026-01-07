#!/usr/bin/env python3
"""
Observator NAT – Aplicație pentru observarea traducerii NAT/PAT

Această aplicație demonstrează cum un server "public" vede conexiunile
din spatele unui NAT. Toate conexiunile de la hosturile private apar
ca venind de la IP-ul public al routerului NAT, diferențiate prin porturi.

Utilizare:
    # Pe server (h3 - în rețeaua publică)
    python3 nat_observer.py server --bind 203.0.113.2 --port 5000
    
    # Pe clienți (h1, h2 - în rețeaua privată)
    python3 nat_observer.py client --host 203.0.113.2 --port 5000 --msg "Salut de la h1"

Ce observăm:
- Serverul vede toate conexiunile ca venind de la 203.0.113.1 (IP-ul NAT)
- Fiecare conexiune are un port sursă diferit (esența PAT)
- Adresele private (192.168.1.x) nu sunt vizibile din exterior

Revolvix&Hypotheticalandrei
"""

from __future__ import annotations

import argparse
import socket
import sys
from datetime import datetime


def ruleaza_server(adresa_bind: str, port: int) -> None:
    """
    Pornește un server TCP care afișează IP:port sursă pentru fiecare conexiune.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((adresa_bind, port))
        sock.listen(5)
        
        print(f"[Server Observator NAT]")
        print(f"Ascultă pe {adresa_bind}:{port}")
        print(f"Așteaptă conexiuni...")
        print("-" * 60)
        
        while True:
            sock_client, adresa_client = sock.accept()
            ip_client, port_client = adresa_client
            
            try:
                # Primește mesajul
                date = sock_client.recv(1024)
                mesaj = date.decode("utf-8", errors="replace").strip()
                
                # Afișează informațiile
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] Conexiune de la {ip_client}:{port_client}")
                print(f"            Mesaj: {mesaj}")
                print()
                
                # Trimite confirmare
                raspuns = f"Primit de la {ip_client}:{port_client}\n"
                sock_client.sendall(raspuns.encode())
                
            finally:
                sock_client.close()
                
    except KeyboardInterrupt:
        print("\nServer oprit.")
    finally:
        sock.close()


def ruleaza_client(host: str, port: int, mesaj: str) -> None:
    """
    Se conectează la server și trimite un mesaj.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    
    try:
        print(f"[Client Observator NAT]")
        print(f"Se conectează la {host}:{port}...")
        
        sock.connect((host, port))
        
        # Afișează adresa locală (va fi IP-ul privat)
        adresa_locala = sock.getsockname()
        print(f"Adresă locală: {adresa_locala[0]}:{adresa_locala[1]}")
        
        # Trimite mesajul
        sock.sendall(mesaj.encode())
        print(f"Trimis: {mesaj}")
        
        # Primește răspunsul
        raspuns = sock.recv(1024).decode("utf-8", errors="replace")
        print(f"Răspuns server: {raspuns}")
        
    except socket.timeout:
        print("Conexiune expirată!")
        sys.exit(1)
    except ConnectionRefusedError:
        print("Conexiune refuzată! Serverul rulează?")
        sys.exit(1)
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(
        description="Observator NAT - demonstrație traducere PAT"
    )
    
    subparsers = parser.add_subparsers(dest="mode", help="Mod de operare")
    
    # Mod server
    server_parser = subparsers.add_parser("server", help="Pornește serverul")
    server_parser.add_argument(
        "--bind", default="0.0.0.0",
        help="Adresa de bind (implicit: 0.0.0.0)"
    )
    server_parser.add_argument(
        "--port", type=int, default=5000,
        help="Portul de ascultare (implicit: 5000)"
    )
    
    # Mod client
    client_parser = subparsers.add_parser("client", help="Pornește clientul")
    client_parser.add_argument(
        "--host", required=True,
        help="Adresa serverului"
    )
    client_parser.add_argument(
        "--port", type=int, default=5000,
        help="Portul serverului (implicit: 5000)"
    )
    client_parser.add_argument(
        "--msg", "--message", default="Salut de la clientul NAT",
        help="Mesajul de trimis"
    )
    
    args = parser.parse_args()
    
    if args.mode == "server":
        ruleaza_server(args.bind, args.port)
    elif args.mode == "client":
        ruleaza_client(args.host, args.port, args.msg)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
