#!/usr/bin/env python3
"""
Expeditor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un expeditor UDP simplu pentru testarea conectivității UDP
și demonstrarea comportamentului DROP.
"""

from __future__ import annotations

import argparse
import socket
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


def trimite_datagrama(host: str, port: int, mesaj: str) -> bool:
    """
    Trimite o datagramă UDP.
    
    Args:
        host: Adresa destinație
        port: Portul destinație
        mesaj: Mesajul de trimis
    
    Returns:
        True dacă trimiterea a reușit (nu garantează recepția!)
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        logheaza(f"Trimitere datagramă către {host}:{port}")
        logheaza(f"Conținut: {mesaj}")
        
        sock.sendto(mesaj.encode(), (host, port))
        
        logheaza("Datagramă trimisă!")
        logheaza("Notă: UDP nu garantează livrarea - receptorul poate să nu primească mesajul")
        
        sock.close()
        return True
        
    except Exception as e:
        logheaza(f"EROARE: {e}")
        return False


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Expeditor UDP pentru Laboratorul Săptămânii 7"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Adresa destinație (implicit: localhost)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9091,
        help="Portul destinație (implicit: 9091)"
    )
    parser.add_argument(
        "--mesaj", "-m",
        default="Test UDP",
        help="Mesajul de trimis (implicit: 'Test UDP')"
    )
    args = parser.parse_args()

    succes = trimite_datagrama(args.host, args.port, args.mesaj)
    exit(0 if succes else 1)


if __name__ == "__main__":
    main()
