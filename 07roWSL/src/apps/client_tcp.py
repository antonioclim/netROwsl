#!/usr/bin/env python3
"""
Client TCP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un client TCP simplu pentru testarea serverului echo
și demonstrarea comportamentului de filtrare.
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


def trimite_mesaj(host: str, port: int, mesaj: str, timeout: float = 5.0) -> bool:
    """
    Trimite un mesaj către server și așteaptă răspunsul.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
    
    Returns:
        True dacă comunicarea a reușit
    """
    logheaza(f"Conectare la {host}:{port}...")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((host, port))
        
        logheaza(f"Conectat! Trimitere mesaj: {mesaj}")
        sock.sendall(mesaj.encode())
        
        logheaza("Așteptare răspuns...")
        raspuns = sock.recv(4096).decode()
        
        logheaza(f"Răspuns primit: {raspuns.strip()}")
        
        sock.close()
        return True
        
    except ConnectionRefusedError:
        logheaza("EROARE: Conexiune refuzată (port închis sau REJECT activ)")
        return False
    except socket.timeout:
        logheaza("EROARE: Timeout (posibil DROP activ sau server indisponibil)")
        return False
    except Exception as e:
        logheaza(f"EROARE: {e}")
        return False


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Client TCP pentru Laboratorul Săptămânii 7"
    )
    parser.add_argument(
        "--host",
        default="localhost",
        help="Adresa serverului (implicit: localhost)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=9090,
        help="Portul serverului (implicit: 9090)"
    )
    parser.add_argument(
        "--mesaj", "-m",
        default="Test echo",
        help="Mesajul de trimis (implicit: 'Test echo')"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=5.0,
        help="Timeout în secunde (implicit: 5.0)"
    )
    args = parser.parse_args()

    succes = trimite_mesaj(args.host, args.port, args.mesaj, args.timeout)
    sys.exit(0 if succes else 1)


if __name__ == "__main__":
    main()
