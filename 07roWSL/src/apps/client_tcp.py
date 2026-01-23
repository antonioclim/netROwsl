#!/usr/bin/env python3
"""
Client TCP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un client TCP simplu pentru testarea serverului echo
și demonstrarea comportamentului de filtrare.

Comportament:
    1. Se conectează la server (handshake TCP)
    2. Trimite mesajul specificat
    3. Așteaptă răspunsul (echo)
    4. Închide conexiunea

Exemplu de utilizare:
    python client_tcp.py --host localhost --port 9090 --mesaj "Salut!"
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import socket
import sys
from datetime import datetime
from pathlib import Path

# Configurare cale pentru importul modulelor locale
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Import logger unificat
try:
    from scripts.utils.logger import configureaza_logger
    logger = configureaza_logger("client_tcp")
except ImportError:
    import logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logger = logging.getLogger("client_tcp")


# ═══════════════════════════════════════════════════════════════════════════════
# COMUNICARE_TCP — Funcția principală de trimitere mesaj
# ═══════════════════════════════════════════════════════════════════════════════

def trimite_mesaj(host: str, port: int, mesaj: str, timeout: float = 5.0) -> bool:
    """
    Trimite un mesaj către server și așteaptă răspunsul.
    
    Flux de execuție:
        1. Creare socket TCP
        2. Setare timeout pentru a evita blocarea indefinită
        3. connect() - realizează handshake-ul TCP (SYN → SYN-ACK → ACK)
        4. sendall() - trimite mesajul
        5. recv() - așteaptă răspunsul echo
        6. close() - închide conexiunea (FIN → FIN-ACK)
    
    NOTĂ PEDAGOGICĂ: Această funcție demonstrează ciclul complet de viață
    al unei conexiuni TCP - de la handshake la închidere.
    
    Args:
        host: Adresa serverului (IP sau hostname)
        port: Portul serverului (1-65535)
        mesaj: Mesajul de trimis (va fi encodat UTF-8)
        timeout: Timeout în secunde pentru operații de rețea
    
    Returns:
        True dacă comunicarea a reușit, False altfel
    """
    logger.info(f"Conectare la {host}:{port}...")
    
    # ───────────────────────────────────────────────────────────────────────────
    # CREARE_SOCKET — Pregătirea conexiunii
    # ───────────────────────────────────────────────────────────────────────────
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)  # Evită blocarea indefinită
    
    try:
        # ───────────────────────────────────────────────────────────────────────
        # CONNECT — Aici se realizează handshake-ul TCP (SYN → SYN-ACK → ACK)
        # ───────────────────────────────────────────────────────────────────────
        sock.connect((host, port))
        logger.info(f"Conectat! Trimitere mesaj: {mesaj}")
        
        # ───────────────────────────────────────────────────────────────────────
        # TRIMITERE_DATE — sendall() garantează trimiterea completă
        # ───────────────────────────────────────────────────────────────────────
        sock.sendall(mesaj.encode('utf-8'))
        
        # ───────────────────────────────────────────────────────────────────────
        # PRIMIRE_RASPUNS — Așteaptă echo de la server
        # ───────────────────────────────────────────────────────────────────────
        logger.info("Așteptare răspuns...")
        raspuns = sock.recv(4096).decode('utf-8', errors='replace')
        logger.info(f"Răspuns primit: {raspuns.strip()}")
        
        return True
        
    except ConnectionRefusedError:
        # RST de la server - port închis SAU firewall REJECT activ
        logger.error("Conexiune refuzată (port închis sau REJECT activ)")
        return False
    except socket.timeout:
        # Niciun răspuns în timpul alocat - probabil DROP activ
        logger.error("Timeout (posibil DROP activ sau server indisponibil)")
        return False
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return False
    finally:
        # IMPORTANT: Întotdeauna închide socket-ul
        sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — Punct de intrare
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală cu parsare argumente."""
    parser = argparse.ArgumentParser(
        description="Client TCP pentru Laboratorul Săptămânii 7",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python client_tcp.py                          # Test implicit localhost:9090
  python client_tcp.py --mesaj "Salut!"         # Mesaj personalizat
  python client_tcp.py --host 10.0.7.100 -p 80  # Server și port specifice
        """
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
