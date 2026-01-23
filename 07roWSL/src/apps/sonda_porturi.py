#!/usr/bin/env python3
"""
Sondă de Porturi TCP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Instrument pentru sondarea porturilor TCP în scopuri defensive,
pentru identificarea serviciilor active și a regulilor de firewall.

Interpretarea rezultatelor:
    - DESCHIS:  SYN → SYN-ACK (serviciu activ)
    - ÎNCHIS:   SYN → RST (niciun serviciu, dar sistemul răspunde)
    - FILTRAT:  SYN → timeout (firewall DROP activ)

Exemplu de utilizare:
    python sonda_porturi.py --tinta localhost --interval 9080-9100
    python sonda_porturi.py --tinta localhost --port 9090
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import socket
import sys
import time
from pathlib import Path

# Configurare cale pentru importul modulelor locale
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Import logger unificat
try:
    from scripts.utils.logger import configureaza_logger
    logger = configureaza_logger("sonda_porturi")
except ImportError:
    import logging
    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO
    )
    logger = logging.getLogger("sonda_porturi")


# ═══════════════════════════════════════════════════════════════════════════════
# SONDARE_PORT — Verifică starea unui singur port
# ═══════════════════════════════════════════════════════════════════════════════

def sondeaza_port(host: str, port: int, timeout: float = 1.0) -> str:
    """
    Sondează un port TCP și determină starea lui.
    
    Logica de determinare:
        - connect_ex() returnează 0 → DESCHIS (SYN-ACK primit)
        - connect_ex() returnează rapid (!= 0) → ÎNCHIS (RST primit)
        - timeout → FILTRAT (niciun răspuns, probabil DROP)
    
    Args:
        host: Adresa gazdă (IP sau hostname)
        port: Portul de sondat (1-65535)
        timeout: Timeout în secunde
    
    Returns:
        Starea portului: 'deschis', 'închis', sau 'filtrat'
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        timp_start = time.time()
        # connect_ex() returnează 0 pentru succes, cod eroare altfel
        # Nu aruncă excepție ca connect()
        rezultat = sock.connect_ex((host, port))
        timp_scurs = time.time() - timp_start
        
        sock.close()
        
        if rezultat == 0:
            # Conexiune reușită = serviciu activ
            return "deschis"
        elif timp_scurs >= timeout * 0.9:
            # Timeout aproape complet = niciun răspuns = DROP probabil
            return "filtrat"
        else:
            # Răspuns rapid negativ = RST primit = port închis
            return "închis"
            
    except socket.timeout:
        return "filtrat"
    except Exception:
        return "eroare"


# ═══════════════════════════════════════════════════════════════════════════════
# SONDARE_INTERVAL — Sondează multiple porturi
# ═══════════════════════════════════════════════════════════════════════════════

def sondeaza_interval(
    host: str,
    port_start: int,
    port_final: int,
    timeout: float = 1.0
) -> dict[int, str]:
    """
    Sondează un interval de porturi.
    
    Args:
        host: Adresa gazdă
        port_start: Primul port din interval (inclusiv)
        port_final: Ultimul port din interval (inclusiv)
        timeout: Timeout per port în secunde
    
    Returns:
        Dicționar {port: stare}
    """
    rezultate = {}
    total_porturi = port_final - port_start + 1
    
    logger.info(f"Începere sondare: {host} porturi {port_start}-{port_final}")
    logger.info(f"Total porturi: {total_porturi}, Timeout: {timeout}s per port")
    print()
    
    for i, port in enumerate(range(port_start, port_final + 1), 1):
        stare = sondeaza_port(host, port, timeout)
        rezultate[port] = stare
        
        # Afișare doar pentru porturi interesante
        if stare == "deschis":
            print(f"  Port {port}: DESCHIS")
        elif stare == "filtrat":
            print(f"  Port {port}: FILTRAT (posibil DROP)")
        
        # Afișare progres la fiecare 10 porturi
        if i % 10 == 0:
            procent = (i / total_porturi) * 100
            print(f"  ... {procent:.0f}% completat ({i}/{total_porturi})")
    
    return rezultate


# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_SUMAR — Rezumat rezultate
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_sumar(rezultate: dict[int, str]):
    """Afișează sumarul rezultatelor sondării."""
    deschise = [p for p, s in rezultate.items() if s == "deschis"]
    inchise = [p for p, s in rezultate.items() if s == "închis"]
    filtrate = [p for p, s in rezultate.items() if s == "filtrat"]
    
    print()
    logger.info("=" * 50)
    logger.info("SUMAR SONDARE")
    logger.info("=" * 50)
    print()
    print(f"  Porturi deschise:  {len(deschise)}")
    if deschise:
        print(f"    {', '.join(map(str, deschise))}")
    
    print(f"  Porturi închise:   {len(inchise)}")
    print(f"  Porturi filtrate:  {len(filtrate)}")
    if filtrate:
        print(f"    (primele 10: {', '.join(map(str, filtrate[:10]))})")
    
    print()
    logger.info("Interpretare:")
    logger.info("  DESCHIS  = SYN-ACK primit, serviciu activ")
    logger.info("  ÎNCHIS   = RST primit, niciun serviciu")
    logger.info("  FILTRAT  = Timeout, firewall DROP activ")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Sondă de porturi TCP pentru analiza defensivă",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python sonda_porturi.py --tinta localhost --interval 9080-9100
  python sonda_porturi.py --tinta localhost --port 9090
  python sonda_porturi.py --tinta 10.0.7.100 --timeout 2.0
        """
    )
    parser.add_argument(
        "--tinta", "-t",
        default="localhost",
        help="Adresa țintă (implicit: localhost)"
    )
    parser.add_argument(
        "--interval", "-r",
        default="9080-9100",
        help="Interval de porturi (implicit: 9080-9100)"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.0,
        help="Timeout per port în secunde (implicit: 1.0)"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        help="Sondează un singur port"
    )
    args = parser.parse_args()

    logger.info("=" * 50)
    logger.info("Sondă Porturi TCP - Săptămâna 7")
    logger.info("=" * 50)
    print()

    if args.port:
        # Sondare port unic
        stare = sondeaza_port(args.tinta, args.port, args.timeout)
        logger.info(f"Port {args.tinta}:{args.port} = {stare.upper()}")
    else:
        # Parsare interval
        try:
            parti = args.interval.split("-")
            port_start = int(parti[0])
            port_final = int(parti[1]) if len(parti) > 1 else port_start
        except ValueError:
            logger.error("Format interval invalid. Folosiți: START-FINAL")
            return 1
        
        rezultate = sondeaza_interval(
            args.tinta,
            port_start,
            port_final,
            args.timeout
        )
        
        afiseaza_sumar(rezultate)

    return 0


if __name__ == "__main__":
    sys.exit(main())
