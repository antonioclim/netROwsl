#!/usr/bin/env python3
"""
Server/Client Echo TCP pentru testarea conectivității SDN

Aplicație simplă pentru generarea de trafic TCP și verificarea
politicilor de rețea în topologii SDN.

Planul de porturi Săptămâna 6:
    TCP_APP_PORT = 9090
    UDP_APP_PORT = 9091
    WEEK_PORT_BASE = 5600 (pentru porturi personalizate)

Utilizare:
    # Server
    python3 tcp_echo.py server --bind 10.0.6.12 --port 9090
    
    # Client
    python3 tcp_echo.py client --dst 10.0.6.12 --port 9090 --message "Salut TCP"

Revolvix&Hypotheticalandrei
"""

from __future__ import annotations

import argparse
import socket
import sys


def ruleaza_server(adresa_bind: str, port: int) -> None:
    """
    Server echo TCP - returnează mesajele primite.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((adresa_bind, port))
        sock.listen(5)
        
        print(f"[Server Echo TCP]")
        print(f"Ascultă pe {adresa_bind}:{port}")
        print("Apasă Ctrl+C pentru a opri.")
        print("-" * 40)
        
        while True:
            sock_client, adresa_client = sock.accept()
            print(f"Conexiune de la {adresa_client[0]}:{adresa_client[1]}")
            
            try:
                while True:
                    date = sock_client.recv(1024)
                    if not date:
                        break
                    
                    mesaj = date.decode("utf-8", errors="replace")
                    print(f"  Primit: {mesaj.strip()}")
                    
                    # Returnează ecoul
                    sock_client.sendall(date)
                    print(f"  Ecou returnat: {mesaj.strip()}")
                    
            finally:
                sock_client.close()
                print(f"Conexiune închisă.\n")
                
    except KeyboardInterrupt:
        print("\nServer oprit.")
    finally:
        sock.close()


def ruleaza_client(dst: str, port: int, mesaj: str) -> None:
    """
    Client TCP - trimite mesaj și afișează răspunsul.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    
    try:
        print(f"[Client Echo TCP]")
        print(f"Se conectează la {dst}:{port}...")
        
        sock.connect((dst, port))
        print(f"Conectat!")
        
        # Trimite
        sock.sendall(mesaj.encode())
        print(f"Trimis: {mesaj}")
        
        # Primește ecoul
        raspuns = sock.recv(1024).decode("utf-8", errors="replace")
        print(f"Primit: {raspuns}")
        
        if raspuns.strip() == mesaj.strip():
            print("✓ Ecou verificat - conexiune reușită!")
        
    except socket.timeout:
        print("✗ Conexiune expirată!")
        print("  Cauze posibile:")
        print("  - Serverul nu rulează")
        print("  - Politica SDN blochează traficul")
        print("  - Reguli de firewall")
        sys.exit(1)
    except ConnectionRefusedError:
        print("✗ Conexiune refuzată!")
        sys.exit(1)
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Server/Client Echo TCP")
    subparsers = parser.add_subparsers(dest="mode")
    
    # Server
    srv = subparsers.add_parser("server")
    srv.add_argument("--bind", default="0.0.0.0")
    srv.add_argument("--port", type=int, default=9090)
    
    # Client
    cli = subparsers.add_parser("client")
    cli.add_argument("--dst", required=True)
    cli.add_argument("--port", type=int, default=9090)
    cli.add_argument("--message", default="Salut TCP")
    
    args = parser.parse_args()
    
    if args.mode == "server":
        ruleaza_server(args.bind, args.port)
    elif args.mode == "client":
        ruleaza_client(args.dst, args.port, args.message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
