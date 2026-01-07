#!/usr/bin/env python3
"""
Receptor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un receptor UDP simplu care logează datagramele primite.
Folosit pentru demonstrarea comportamentului UDP și a filtrării DROP.
"""

from __future__ import annotations

import argparse
import socket
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


def porneste_receptor(host: str, port: int):
    """
    Pornește receptorul UDP.
    
    Args:
        host: Adresa pe care să asculte
        port: Portul pe care să asculte
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((host, port))
        logheaza(f"Receptor UDP pornit pe {host}:{port}")
        logheaza("Așteptare datagrame...")
        
        nr_mesaje = 0
        
        while True:
            try:
                date, adresa = sock.recvfrom(4096)
                nr_mesaje += 1
                ip_sursa, port_sursa = adresa
                mesaj = date.decode('utf-8', errors='replace')
                
                logheaza(f"[#{nr_mesaje}] Datagramă de la {ip_sursa}:{port_sursa}: {mesaj.strip()}")
                
            except KeyboardInterrupt:
                logheaza(f"Receptor oprit. Total mesaje primite: {nr_mesaje}")
                break
                
    except OSError as e:
        logheaza(f"Eroare la pornirea receptorului: {e}")
    finally:
        sock.close()


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Receptor UDP pentru Laboratorul Săptămânii 7"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Adresa pe care să asculte (implicit: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9091,
        help="Portul pe care să asculte (implicit: 9091)"
    )
    args = parser.parse_args()

    porneste_receptor(args.host, args.port)


if __name__ == "__main__":
    main()
