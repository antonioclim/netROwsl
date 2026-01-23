#!/usr/bin/env python3
"""
Receptor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un receptor UDP simplu care logează datagramele primite.
Folosit pentru demonstrarea comportamentului UDP și a filtrării DROP.

Diferențe față de TCP:
    - Nu există handshake (connectionless)
    - Nu există confirmare de primire
    - recvfrom() returnează și adresa sursei
    - Fiecare datagramă este independentă

Exemplu de utilizare:
    python receptor_udp.py --host 0.0.0.0 --port 9091
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
    logger = configureaza_logger("receptor_udp")
except ImportError:
    import logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logger = logging.getLogger("receptor_udp")


# ═══════════════════════════════════════════════════════════════════════════════
# RECEPTOR_UDP — Ascultă și logează datagrame
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_receptor(host: str, port: int):
    """
    Pornește receptorul UDP.
    
    NOTĂ PEDAGOGICĂ: UDP nu are handshake sau confirmare. Dacă aplicăm DROP
    pe acest port, expeditorul NU va ști că pachetul a fost pierdut!
    
    Args:
        host: Adresa pe care să asculte ("0.0.0.0" = toate interfețele)
        port: Portul UDP (implicit: 9091)
    """
    # ───────────────────────────────────────────────────────────────────────────
    # CREARE_SOCKET — SOCK_DGRAM = UDP (datagram socket)
    # ───────────────────────────────────────────────────────────────────────────
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        sock.bind((host, port))
        logger.info(f"Receptor UDP pornit pe {host}:{port}")
        logger.info("Așteptare datagrame... (Ctrl+C pentru oprire)")
        
        nr_mesaje = 0
        
        # ───────────────────────────────────────────────────────────────────────
        # BUCLA_RECEPTIE — recvfrom() blochează până primește o datagramă
        # ───────────────────────────────────────────────────────────────────────
        while True:
            try:
                # recvfrom() returnează (date, (ip_sursa, port_sursa))
                # Spre deosebire de TCP recv(), aici primim și adresa expeditorului
                date, adresa = sock.recvfrom(4096)
                nr_mesaje += 1
                ip_sursa, port_sursa = adresa
                mesaj = date.decode('utf-8', errors='replace')
                
                logger.info(f"[#{nr_mesaje}] Datagramă de la {ip_sursa}:{port_sursa}: {mesaj.strip()}")
                
            except KeyboardInterrupt:
                logger.info(f"Receptor oprit. Total datagrame primite: {nr_mesaje}")
                break
                
    except OSError as e:
        logger.error(f"Eroare la pornirea receptorului: {e}")
        sys.exit(1)
    finally:
        sock.close()
        logger.info("Socket receptor închis")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

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
