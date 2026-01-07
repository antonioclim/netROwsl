#!/usr/bin/env python3
"""
Sondă de Porturi TCP
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Instrument pentru sondarea porturilor TCP în scopuri defensive,
pentru identificarea serviciilor active și a regulilor de firewall.
"""

from __future__ import annotations

import argparse
import socket
import time
from datetime import datetime


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


def sondeaza_port(host: str, port: int, timeout: float = 1.0) -> str:
    """
    Sondează un port TCP și determină starea lui.
    
    Args:
        host: Adresa gazdă
        port: Portul de sondat
        timeout: Timeout în secunde
    
    Returns:
        Starea portului: 'deschis', 'închis', sau 'filtrat'
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        
        timp_start = time.time()
        rezultat = sock.connect_ex((host, port))
        timp_scurs = time.time() - timp_start
        
        sock.close()
        
        if rezultat == 0:
            return "deschis"
        elif timp_scurs >= timeout * 0.9:
            # Timeout aproape complet - probabil DROP
            return "filtrat"
        else:
            # Răspuns rapid negativ - închis (RST primit)
            return "închis"
            
    except socket.timeout:
        return "filtrat"
    except Exception:
        return "eroare"


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
        port_start: Primul port din interval
        port_final: Ultimul port din interval
        timeout: Timeout per port
    
    Returns:
        Dicționar {port: stare}
    """
    rezultate = {}
    total_porturi = port_final - port_start + 1
    
    logheaza(f"Începere sondare: {host} porturi {port_start}-{port_final}")
    logheaza(f"Total porturi: {total_porturi}, Timeout: {timeout}s per port")
    logheaza("")
    
    for i, port in enumerate(range(port_start, port_final + 1), 1):
        stare = sondeaza_port(host, port, timeout)
        rezultate[port] = stare
        
        # Afișare progres
        if stare == "deschis":
            print(f"  Port {port}: DESCHIS")
        elif stare == "filtrat":
            print(f"  Port {port}: FILTRAT (posibil DROP)")
        
        # Afișare procent la fiecare 10 porturi
        if i % 10 == 0:
            procent = (i / total_porturi) * 100
            print(f"  ... {procent:.0f}% completat ({i}/{total_porturi})")
    
    return rezultate


def afiseaza_sumar(rezultate: dict[int, str]):
    """Afișează sumarul rezultatelor."""
    deschise = [p for p, s in rezultate.items() if s == "deschis"]
    inchise = [p for p, s in rezultate.items() if s == "închis"]
    filtrate = [p for p, s in rezultate.items() if s == "filtrat"]
    
    print()
    logheaza("=" * 50)
    logheaza("SUMAR SONDARE")
    logheaza("=" * 50)
    print()
    print(f"  Porturi deschise:  {len(deschise)}")
    if deschise:
        print(f"    {', '.join(map(str, deschise))}")
    
    print(f"  Porturi închise:   {len(inchise)}")
    print(f"  Porturi filtrate:  {len(filtrate)}")
    if filtrate:
        print(f"    (primele 10: {', '.join(map(str, filtrate[:10]))})")
    
    print()
    logheaza("Interpretare:")
    logheaza("  DESCHIS  = Serviciu activ care acceptă conexiuni")
    logheaza("  ÎNCHIS   = Niciun serviciu, portul răspunde cu RST")
    logheaza("  FILTRAT  = Firewall DROP activ, niciun răspuns")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Sondă de porturi TCP pentru analiza defensivă"
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

    logheaza("=" * 50)
    logheaza("Sondă Porturi TCP - Săptămâna 7")
    logheaza("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    logheaza("=" * 50)
    print()

    if args.port:
        # Sondare port unic
        stare = sondeaza_port(args.tinta, args.port, args.timeout)
        logheaza(f"Port {args.tinta}:{args.port} = {stare.upper()}")
    else:
        # Parsare interval
        try:
            parti = args.interval.split("-")
            port_start = int(parti[0])
            port_final = int(parti[1]) if len(parti) > 1 else port_start
        except ValueError:
            logheaza("Eroare: Format interval invalid. Folosiți: START-FINAL")
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
    exit(main())
