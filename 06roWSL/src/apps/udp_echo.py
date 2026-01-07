#!/usr/bin/env python3
"""
Server/Client Echo UDP pentru testarea politicilor SDN

Aplicație pentru generarea de trafic UDP și verificarea
politicilor de permitere/blocare în rețele SDN.

Planul de porturi Săptămâna 6:
    TCP_APP_PORT = 9090
    UDP_APP_PORT = 9091
    WEEK_PORT_BASE = 5600 (pentru porturi personalizate)

Utilizare:
    # Server
    python3 udp_echo.py server --bind 10.0.6.13 --port 9091
    
    # Client
    python3 udp_echo.py client --dst 10.0.6.13 --port 9091 --message "Salut UDP"

Revolvix&Hypotheticalandrei
"""

from __future__ import annotations

import argparse
import socket
import sys


def ruleaza_server(adresa_bind: str, port: int) -> None:
    """
    Server echo UDP - returnează datagramele primite.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((adresa_bind, port))
        
        print(f"[Server Echo UDP]")
        print(f"Ascultă pe {adresa_bind}:{port}")
        print("Apasă Ctrl+C pentru a opri.")
        print("-" * 40)
        
        while True:
            date, adresa_client = sock.recvfrom(1024)
            mesaj = date.decode("utf-8", errors="replace")
            
            print(f"De la {adresa_client[0]}:{adresa_client[1]}: {mesaj.strip()}")
            
            # Returnează ecoul
            sock.sendto(date, adresa_client)
            print(f"  → Ecou returnat")
            
    except KeyboardInterrupt:
        print("\nServer oprit.")
    finally:
        sock.close()


def ruleaza_client(dst: str, port: int, mesaj: str) -> None:
    """
    Client UDP - trimite datagramă și așteaptă răspunsul.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    
    try:
        print(f"[Client Echo UDP]")
        print(f"Țintă: {dst}:{port}")
        
        # Trimite
        sock.sendto(mesaj.encode(), (dst, port))
        print(f"Trimis: {mesaj}")
        
        # Așteaptă răspunsul
        raspuns, adresa_server = sock.recvfrom(1024)
        print(f"Primit: {raspuns.decode()}")
        
        print("✓ Comunicare UDP reușită!")
        
    except socket.timeout:
        print("✗ Niciun răspuns primit (timeout)!")
        print("  Cauze posibile:")
        print("  - Serverul nu rulează")
        print("  - Traficul UDP blocat de politica SDN")
        print("  - Verifică ALLOW_UDP_TO_H3 în controller")
        sys.exit(1)
    finally:
        sock.close()


def main():
    parser = argparse.ArgumentParser(description="Server/Client Echo UDP")
    subparsers = parser.add_subparsers(dest="mode")
    
    # Server
    srv = subparsers.add_parser("server")
    srv.add_argument("--bind", default="0.0.0.0")
    srv.add_argument("--port", type=int, default=9091)
    
    # Client
    cli = subparsers.add_parser("client")
    cli.add_argument("--dst", required=True)
    cli.add_argument("--port", type=int, default=9091)
    cli.add_argument("--message", default="Salut UDP")
    
    args = parser.parse_args()
    
    if args.mode == "server":
        ruleaza_server(args.bind, args.port)
    elif args.mode == "client":
        ruleaza_client(args.dst, args.port, args.message)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
