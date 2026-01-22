#!/usr/bin/env python3
"""
Exercițiul 5.01 – Analiza CIDR și Subnetare FLSM
================================================
CLI pentru calcularea parametrilor de rețea și împărțirea în subrețele egale.

Utilizare:
    python ex_5_01_cidr_flsm.py analizeaza 192.168.10.14/26 [--detaliat] [--json]
    python ex_5_01_cidr_flsm.py invata 192.168.10.14/26
    python ex_5_01_cidr_flsm.py flsm 192.168.100.0/24 4
    python ex_5_01_cidr_flsm.py binar 192.168.10.14

Autor: Material didactic ASE-CSIE
"""

from __future__ import annotations

import argparse
import json
import sys
import logging
from pathlib import Path
from typing import List, Optional

# Import utilitar local
RADACINA = Path(__file__).resolve().parents[2]
if str(RADACINA) not in sys.path:
    sys.path.insert(0, str(RADACINA))

from src.utils.net_utils import (
    analizeaza_interfata_ipv4,
    imparte_flsm,
    interval_gazde_ipv4,
    ip_la_binar,
    ip_la_binar_punctat,
    prefix_la_masca,
    masca_la_prefix,
)

# Configurare logging
logger = logging.getLogger(__name__)


# Coduri culori ANSI
class Culori:
    HEADER = '\033[95m'
    ALBASTRU = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    BOLD = '\033[1m'
    SUBLINIAT = '\033[4m'
    SFARSIT = '\033[0m'


def coloreaza(text: str, culoare: str) -> str:
    """Aplică culoare dacă stdout este un terminal."""
    if sys.stdout.isatty():
        return f"{culoare}{text}{Culori.SFARSIT}"
    return text


def cmd_analizeaza(tinta: str, detaliat: bool = False, ca_json: bool = False) -> int:
    """Analizează o adresă IPv4 cu prefix CIDR."""
    logger.debug(f"Analiză CIDR pentru: {tinta}")
    
    try:
        info = analizeaza_interfata_ipv4(tinta)
    except ValueError as e:
        logger.error(f"Eroare la analiza {tinta}: {e}")
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    date = {
        "intrare": tinta,
        "adresa": str(info.adresa),
        "tip_adresa": info.tip_adresa,
        "retea": str(info.retea.network_address),
        "prefix": info.retea.prefixlen,
        "masca": str(info.masca),
        "masca_wildcard": str(info.wildcard),
        "broadcast": str(info.broadcast),
        "total_adrese": info.total_adrese,
        "gazde_utilizabile": info.gazde_utilizabile,
        "prima_gazda": str(info.prima_gazda) if info.prima_gazda else None,
        "ultima_gazda": str(info.ultima_gazda) if info.ultima_gazda else None,
        "este_privata": info.este_privata,
    }
    
    if ca_json:
        print(json.dumps(date, indent=2, ensure_ascii=False))
        return 0
    
    # Afișare formatată
    print()
    print(coloreaza("═" * 50, Culori.ALBASTRU))
    print(coloreaza("  Analiză IPv4 CIDR", Culori.BOLD))
    print(coloreaza("═" * 50, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Intrare:', Culori.CYAN):30} {tinta}")
    print(f"  {coloreaza('Adresa IP:', Culori.CYAN):30} {info.adresa}")
    print(f"  {coloreaza('Tip adresă:', Culori.CYAN):30} {coloreaza(info.tip_adresa.upper(), Culori.GALBEN)}")
    print()
    
    print(f"  {coloreaza('Adresa de rețea:', Culori.CYAN):30} {info.retea.network_address}/{info.retea.prefixlen}")
    print(f"  {coloreaza('Mască de rețea:', Culori.CYAN):30} {info.masca}")
    print(f"  {coloreaza('Mască wildcard:', Culori.CYAN):30} {info.wildcard}")
    print(f"  {coloreaza('Adresa broadcast:', Culori.CYAN):30} {info.broadcast}")
    print()
    
    print(f"  {coloreaza('Total adrese:', Culori.CYAN):30} {info.total_adrese}")
    print(f"  {coloreaza('Gazde utilizabile:', Culori.CYAN):30} {coloreaza(str(info.gazde_utilizabile), Culori.VERDE)}")
    print(f"  {coloreaza('Prima gazdă:', Culori.CYAN):30} {info.prima_gazda or 'N/A'}")
    print(f"  {coloreaza('Ultima gazdă:', Culori.CYAN):30} {info.ultima_gazda or 'N/A'}")
    print()
    
    print(f"  {coloreaza('Adresă privată:', Culori.CYAN):30} {'Da' if info.este_privata else 'Nu'}")
    
    if detaliat:
        print()
        print(coloreaza("─" * 50, Culori.ALBASTRU))
        print(coloreaza("  Reprezentare Binară", Culori.BOLD))
        print(coloreaza("─" * 50, Culori.ALBASTRU))
        print()
        
        addr_bin = ip_la_binar_punctat(str(info.adresa))
        mask_bin = ip_la_binar_punctat(str(info.masca))
        net_bin = ip_la_binar_punctat(str(info.retea.network_address))
        bcast_bin = ip_la_binar_punctat(str(info.broadcast))
        
        prefix = info.retea.prefixlen
        
        print(f"  {coloreaza('IP (binar):', Culori.CYAN):30}")
        print(f"    {coloreaza(addr_bin[:prefix], Culori.VERDE)}{addr_bin[prefix:]}")
        print(f"    {'─' * prefix}{'^' * (35 - prefix)} porțiunea gazdă")
        print()
        
        print(f"  {coloreaza('Mască (binar):', Culori.CYAN):30}")
        print(f"    {mask_bin}")
        print()
        
        print(f"  {coloreaza('Rețea (binar):', Culori.CYAN):30}")
        print(f"    {net_bin}")
        print()
        
        print(f"  {coloreaza('Broadcast (binar):', Culori.CYAN):30}")
        print(f"    {bcast_bin}")
        print()
        
        # Explicația calculului
        print(coloreaza("─" * 50, Culori.ALBASTRU))
        print(coloreaza("  Explicația Calculului", Culori.BOLD))
        print(coloreaza("─" * 50, Culori.ALBASTRU))
        print()
        
        biti_gazda = 32 - prefix
        print(f"  • Prefix /{prefix} = {prefix} biți pentru rețea, {biti_gazda} biți pentru gazdă")
        print(f"  • Total adrese = 2^{biti_gazda} = {2**biti_gazda}")
        print(f"  • Gazde utilizabile = 2^{biti_gazda} - 2 = {2**biti_gazda - 2}")
        print(f"  • Adresa de rețea: toți biții gazdă = 0")
        print(f"  • Adresa broadcast: toți biții gazdă = 1")
    
    print()
    return 0


def cmd_invata(tinta: str) -> int:
    """
    Mod interactiv de învățare cu predicții.
    
    Studentul face predicții înainte de a vedea rezultatul,
    apoi primește feedback imediat.
    """
    print()
    print(coloreaza("═" * 55, Culori.GALBEN))
    print(coloreaza("  Mod Învățare: Analiză CIDR cu Predicții", Culori.BOLD))
    print(coloreaza("═" * 55, Culori.GALBEN))
    print()
    print(f"  Adresa de analizat: {coloreaza(tinta, Culori.VERDE)}")
    print()
    
    # Calculează rezultatele în avans
    try:
        info = analizeaza_interfata_ipv4(tinta)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    scor = 0
    total = 4
    
    # ─────────────────────────────────────────────────────
    # Predicția 1: Gazde utilizabile
    # ─────────────────────────────────────────────────────
    print(coloreaza("─" * 55, Culori.CYAN))
    print(f"  {coloreaza('PREDICȚIA 1:', Culori.BOLD)} Câte gazde utilizabile are această rețea?")
    print()
    print(f"  Hint: Formula este 2^(32-prefix) - 2")
    print(f"        Prefixul este /{info.retea.prefixlen}")
    print()
    
    try:
        raspuns = input("  Răspunsul tău: ").strip()
        if raspuns and int(raspuns) == info.gazde_utilizabile:
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: {info.gazde_utilizabile}", Culori.ROSU))
            biti_gazda = 32 - info.retea.prefixlen
            print(f"    Explicație: 2^{biti_gazda} - 2 = {2**biti_gazda} - 2 = {info.gazde_utilizabile}")
    except (ValueError, EOFError):
        print(coloreaza(f"  → Răspunsul corect era: {info.gazde_utilizabile}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Predicția 2: Adresa de rețea
    # ─────────────────────────────────────────────────────
    print(coloreaza("─" * 55, Culori.CYAN))
    print(f"  {coloreaza('PREDICȚIA 2:', Culori.BOLD)} Care este adresa de rețea?")
    print()
    print(f"  Hint: Aplică masca pe adresa IP (operația AND)")
    print()
    
    try:
        raspuns = input("  Răspunsul tău: ").strip()
        if raspuns == str(info.retea.network_address):
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: {info.retea.network_address}", Culori.ROSU))
    except EOFError:
        print(coloreaza(f"  → Răspunsul corect era: {info.retea.network_address}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Predicția 3: Adresa de broadcast
    # ─────────────────────────────────────────────────────
    print(coloreaza("─" * 55, Culori.CYAN))
    print(f"  {coloreaza('PREDICȚIA 3:', Culori.BOLD)} Care este adresa de broadcast?")
    print()
    print(f"  Hint: Ultimii {32 - info.retea.prefixlen} biți sunt toți 1")
    print()
    
    try:
        raspuns = input("  Răspunsul tău: ").strip()
        if raspuns == str(info.broadcast):
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: {info.broadcast}", Culori.ROSU))
    except EOFError:
        print(coloreaza(f"  → Răspunsul corect era: {info.broadcast}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Predicția 4: Tip adresă
    # ─────────────────────────────────────────────────────
    print(coloreaza("─" * 55, Culori.CYAN))
    print(f"  {coloreaza('PREDICȚIA 4:', Culori.BOLD)} Este aceasta o adresă privată sau publică?")
    print()
    print(f"  Adrese private: 10.x.x.x, 172.16-31.x.x, 192.168.x.x")
    print()
    
    try:
        raspuns = input("  Răspunsul tău (privată/publică): ").strip().lower()
        corect = "privată" if info.este_privata else "publică"
        if raspuns in ["privata", "privată"] and info.este_privata:
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
            scor += 1
        elif raspuns in ["publica", "publică"] and not info.este_privata:
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: {corect}", Culori.ROSU))
    except EOFError:
        corect = "privată" if info.este_privata else "publică"
        print(coloreaza(f"  → Răspunsul corect era: {corect}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Rezultat final
    # ─────────────────────────────────────────────────────
    print(coloreaza("═" * 55, Culori.GALBEN))
    print(f"  {coloreaza('REZULTAT:', Culori.BOLD)} {scor}/{total} răspunsuri corecte")
    
    if scor == total:
        print(coloreaza("  Excelent! Ai prins conceptele.", Culori.VERDE))
    elif scor >= total // 2:
        print(coloreaza("  Bine! Mai exersează cu alte adrese.", Culori.GALBEN))
    else:
        print(coloreaza("  Recitește teoria și încearcă din nou.", Culori.ROSU))
    
    print(coloreaza("═" * 55, Culori.GALBEN))
    print()
    
    # Afișează analiza completă la final
    print(coloreaza("  Analiza completă:", Culori.BOLD))
    print()
    return cmd_analizeaza(tinta, detaliat=True, ca_json=False)


def cmd_flsm(baza: str, n_subretele: int, ca_json: bool = False) -> int:
    """Împarte o rețea în N subrețele egale."""
    logger.debug(f"FLSM: {baza} în {n_subretele} subrețele")
    
    try:
        subretele = imparte_flsm(baza, n_subretele)
    except ValueError as e:
        logger.error(f"Eroare FLSM: {e}")
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    if ca_json:
        rezultat = []
        for subretea in subretele:
            prima, ultima, utilizabile = interval_gazde_ipv4(subretea)
            rezultat.append({
                "retea": str(subretea.network_address),
                "prefix": subretea.prefixlen,
                "cidr": str(subretea),
                "broadcast": str(subretea.broadcast_address),
                "gazde_utilizabile": utilizabile,
                "prima_gazda": str(prima) if prima else None,
                "ultima_gazda": str(ultima) if ultima else None,
            })
        print(json.dumps({"baza": baza, "numar_subretele": n_subretele, "subretele": rezultat}, indent=2, ensure_ascii=False))
        return 0
    
    # Afișare formatată
    import ipaddress
    retea_baza = ipaddress.ip_network(baza, strict=True)
    biti_adaugati = n_subretele.bit_length() - 1
    prefix_nou = retea_baza.prefixlen + biti_adaugati
    
    print()
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print(coloreaza("  Subnetare FLSM (Mască de Lungime Fixă)", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Rețea de bază:', Culori.CYAN):30} {baza}")
    print(f"  {coloreaza('Număr de subrețele:', Culori.CYAN):30} {n_subretele}")
    print(f"  {coloreaza('Biți împrumutați:', Culori.CYAN):30} {biti_adaugati}")
    print(f"  {coloreaza('Prefix nou:', Culori.CYAN):30} /{prefix_nou}")
    print(f"  {coloreaza('Increment:', Culori.CYAN):30} {2**(32-prefix_nou)} adrese")
    print()
    
    print(coloreaza("─" * 60, Culori.ALBASTRU))
    print(f"  {'Nr.':>4}  {'Subrețea':<20} {'Broadcast':<18} {'Gazde':<10} {'Interval'}")
    print(coloreaza("─" * 60, Culori.ALBASTRU))
    
    for i, subretea in enumerate(subretele, 1):
        prima, ultima, utilizabile = interval_gazde_ipv4(subretea)
        interval = f"{prima}..{ultima}" if prima and ultima else "N/A"
        print(f"  {i:>4}. {str(subretea):<20} {str(subretea.broadcast_address):<18} {utilizabile:<10} {interval}")
    
    print(coloreaza("─" * 60, Culori.ALBASTRU))
    print()
    
    # Verificare total
    total_utilizabile = sum(interval_gazde_ipv4(s)[2] for s in subretele)
    print(f"  {coloreaza('Total gazde utilizabile:', Culori.VERDE)} {total_utilizabile}")
    print()
    
    return 0


def cmd_binar(ip: str) -> int:
    """Afișează reprezentarea binară a unei adrese IP."""
    try:
        import ipaddress
        addr = ipaddress.IPv4Address(ip)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    binar = ip_la_binar(ip)
    punctat = ip_la_binar_punctat(ip)
    
    print()
    print(coloreaza("═" * 50, Culori.ALBASTRU))
    print(coloreaza("  Conversie IP → Binar", Culori.BOLD))
    print(coloreaza("═" * 50, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('IP zecimal:', Culori.CYAN):25} {ip}")
    print(f"  {coloreaza('Binar complet:', Culori.CYAN):25} {binar}")
    print(f"  {coloreaza('Binar punctat:', Culori.CYAN):25} {punctat}")
    print()
    
    # Afișare pe octeți
    octeti = ip.split('.')
    print(coloreaza("  Conversie pe octeți:", Culori.CYAN))
    for i, octet in enumerate(octeti):
        oct_bin = bin(int(octet))[2:].zfill(8)
        print(f"    Octet {i+1}: {octet:>3} → {oct_bin}")
    print()
    
    return 0


def cmd_quiz() -> int:
    """Generează o întrebare quiz rapidă."""
    import random
    
    # Generează o adresă aleatorie
    octeti = [random.randint(1, 254) for _ in range(4)]
    prefix = random.choice([24, 25, 26, 27, 28, 29, 30])
    
    ip = '.'.join(map(str, octeti))
    cidr = f"{ip}/{prefix}"
    
    print()
    print(coloreaza("═" * 50, Culori.GALBEN))
    print(coloreaza("  Quiz Rapid: Analiza CIDR", Culori.BOLD))
    print(coloreaza("═" * 50, Culori.GALBEN))
    print()
    print(f"  Adresă: {coloreaza(cidr, Culori.VERDE)}")
    print()
    print("  Calculați:")
    print("  1. Adresa de rețea")
    print("  2. Adresa de broadcast")
    print("  3. Numărul de gazde utilizabile")
    print("  4. Prima și ultima gazdă utilizabilă")
    print()
    
    input(coloreaza("  Apăsați Enter pentru a vedea răspunsul...", Culori.CYAN))
    
    return cmd_analizeaza(cidr, detaliat=False, ca_json=False)


def construieste_parser() -> argparse.ArgumentParser:
    """Construiește parserul de argumente."""
    parser = argparse.ArgumentParser(
        description="Exercițiul 5.01 – Analiză CIDR și Subnetare FLSM",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  %(prog)s analizeaza 192.168.10.14/26           Analizează adresa
  %(prog)s analizeaza 192.168.10.14/26 --detaliat Cu explicații detaliate
  %(prog)s analizeaza 192.168.10.14/26 --json    Ieșire JSON
  %(prog)s invata 192.168.10.14/26               Mod învățare cu predicții
  %(prog)s flsm 192.168.100.0/24 4               Împarte în 4 subrețele
  %(prog)s flsm 10.0.0.0/24 8                    Împarte în 8 subrețele
  %(prog)s binar 192.168.1.1                     Conversie binară
  %(prog)s quiz                                  Quiz rapid aleatoriu
"""
    )
    
    subparsers = parser.add_subparsers(dest="comanda", required=True)
    
    # Subcomanda analizeaza
    p_analizeaza = subparsers.add_parser(
        "analizeaza",
        help="Analizează o adresă IPv4 cu prefix CIDR"
    )
    p_analizeaza.add_argument(
        "tinta",
        help="Adresă IPv4 cu prefix (ex: 192.168.10.14/26)"
    )
    p_analizeaza.add_argument(
        "--detaliat", "-d",
        action="store_true",
        help="Afișează explicații detaliate și reprezentare binară"
    )
    p_analizeaza.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ieșire în format JSON"
    )
    
    # Subcomanda invata (NOU!)
    p_invata = subparsers.add_parser(
        "invata",
        help="Mod învățare interactiv cu predicții"
    )
    p_invata.add_argument(
        "tinta",
        help="Adresă IPv4 cu prefix (ex: 192.168.10.14/26)"
    )
    
    # Subcomanda FLSM
    p_flsm = subparsers.add_parser(
        "flsm",
        help="Împarte o rețea în N subrețele egale (FLSM)"
    )
    p_flsm.add_argument(
        "baza",
        help="Rețea de bază în format CIDR (ex: 192.168.100.0/24)"
    )
    p_flsm.add_argument(
        "n",
        type=int,
        help="Numărul de subrețele (putere de 2)"
    )
    p_flsm.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ieșire în format JSON"
    )
    
    # Subcomanda binar
    p_binar = subparsers.add_parser(
        "binar",
        help="Afișează reprezentarea binară a unei adrese IP"
    )
    p_binar.add_argument(
        "ip",
        help="Adresă IPv4 (ex: 192.168.1.1)"
    )
    
    # Subcomanda quiz
    subparsers.add_parser(
        "quiz",
        help="Generează o întrebare quiz rapidă"
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Funcția principală."""
    parser = construieste_parser()
    args = parser.parse_args(argv)
    
    if args.comanda == "analizeaza":
        return cmd_analizeaza(args.tinta, args.detaliat, args.json)
    elif args.comanda == "invata":
        return cmd_invata(args.tinta)
    elif args.comanda == "flsm":
        return cmd_flsm(args.baza, args.n, args.json)
    elif args.comanda == "binar":
        return cmd_binar(args.ip)
    elif args.comanda == "quiz":
        return cmd_quiz()
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
