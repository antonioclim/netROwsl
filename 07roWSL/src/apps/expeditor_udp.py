#!/usr/bin/env python3
"""
Expeditor UDP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Un expeditor UDP simplu pentru testarea conectivității UDP
și demonstrarea comportamentului DROP.

NOTĂ IMPORTANTĂ: UDP este "fire-and-forget"!
    - sendto() returnează succes chiar dacă destinatarul nu există
    - Nu există confirmare de primire
    - Dacă DROP este activ, expeditorul NU va ști

Exemplu de utilizare:
    python expeditor_udp.py --host localhost --port 9091 --mesaj "Test"
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path

# Configurare cale pentru importul modulelor locale
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Import logger unificat
try:
    from scripts.utils.logger import configureaza_logger
    logger = configureaza_logger("expeditor_udp")
except ImportError:
    import logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logger = logging.getLogger("expeditor_udp")


# ═══════════════════════════════════════════════════════════════════════════════
# TRIMITERE_DATAGRAMA
# ═══════════════════════════════════════════════════════════════════════════════

def trimite_datagrama(host: str, port: int, mesaj: str) -> bool:
    """
    Trimite o datagramă UDP.
    
    NOTĂ PEDAGOGICĂ: sendto() returnează ÎNTOTDEAUNA succes pentru UDP,
    chiar dacă nu există nimeni care să asculte pe acel port!
    Aceasta este diferența fundamentală față de TCP.
    
    Args:
        host: Adresa destinație (IP sau hostname)
        port: Portul destinație
        mesaj: Mesajul de trimis (va fi encodat UTF-8)
    
    Returns:
        True dacă trimiterea a reușit (nu garantează recepția!)
    """
    try:
        # ───────────────────────────────────────────────────────────────────────
        # CREARE_SOCKET — SOCK_DGRAM = UDP
        # ───────────────────────────────────────────────────────────────────────
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        logger.info(f"Trimitere datagramă către {host}:{port}")
        logger.info(f"Conținut: {mesaj}")
        
        # ───────────────────────────────────────────────────────────────────────
        # SENDTO — Trimite datagrama (nu necesită connect() prealabil)
        # ───────────────────────────────────────────────────────────────────────
        bytes_trimisi = sock.sendto(mesaj.encode('utf-8'), (host, port))
        
        logger.info(f"Datagramă trimisă! ({bytes_trimisi} bytes)")
        logger.warning("UDP nu garantează livrarea - receptorul poate să nu primească mesajul")
        
        sock.close()
        return True
        
    except Exception as e:
        logger.error(f"Eroare la trimitere: {e}")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

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
    sys.exit(0 if succes else 1)


if __name__ == "__main__":
    main()
