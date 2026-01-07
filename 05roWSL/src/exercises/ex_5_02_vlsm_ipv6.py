#!/usr/bin/env python3
"""
Exercițiul 5.02 – Alocare VLSM și Operații IPv6
===============================================
CLI pentru alocarea VLSM și manipularea adreselor IPv6.

Utilizare:
    python ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2
    python ex_5_02_vlsm_ipv6.py ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
    python ex_5_02_vlsm_ipv6.py ipv6-expandare "2001:db8::1"
    python ex_5_02_vlsm_ipv6.py subretele-ipv6 "2001:db8:abcd::/48" --numar 8

Autor: Material didactic ASE-CSIE
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

# Import utilitar local
RADACINA = Path(__file__).resolve().parents[2]
if str(RADACINA) not in sys.path:
    sys.path.insert(0, str(RADACINA))

from src.utils.net_utils import (
    aloca_vlsm,
    comprima_ipv6,
    expandeaza_ipv6,
    subretele_ipv6_din_prefix,
    prefix_pentru_gazde,
    interval_gazde_ipv4,
)


# Coduri culori ANSI
class Culori:
    HEADER = '\033[95m'
    ALBASTRU = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    BOLD = '\033[1m'
    SFARSIT = '\033[0m'


def coloreaza(text: str, culoare: str) -> str:
    """Aplică culoare dacă stdout este un terminal."""
    if sys.stdout.isatty():
        return f"{culoare}{text}{Culori.SFARSIT}"
    return text


def cmd_vlsm(baza: str, cerinte: List[int], ca_json: bool = False) -> int:
    """Alocă subrețele folosind VLSM pentru cerințele date."""
    try:
        alocari = aloca_vlsm(baza, cerinte)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    if ca_json:
        rezultat = []
        for alocare in alocari:
            subretea = alocare['subretea']
            rezultat.append({
                "cerinta": alocare['cerinta'],
                "retea": str(subretea.network_address),
                "prefix": subretea.prefixlen,
                "cidr": str(subretea),
                "broadcast": str(subretea.broadcast_address),
                "gazde_disponibile": subretea.num_addresses - 2,
            })
        print(json.dumps({
            "baza": baza, 
            "cerinte": cerinte, 
            "alocari": rezultat
        }, indent=2, ensure_ascii=False))
        return 0
    
    # Afișare formatată
    print()
    print(coloreaza("═" * 70, Culori.ALBASTRU))
    print(coloreaza("  Alocare VLSM (Mască de Lungime Variabilă)", Culori.BOLD))
    print(coloreaza("═" * 70, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Rețea de bază:', Culori.CYAN):30} {baza}")
    print(f"  {coloreaza('Cerințe gazde:', Culori.CYAN):30} {cerinte}")
    print()
    
    print(coloreaza("  Proces VLSM:", Culori.GALBEN))
    print("  1. Sortează cerințele descrescător")
    print("  2. Pentru fiecare cerință, alocă cel mai mic bloc suficient")
    print("  3. Avansează la următoarea adresă aliniată")
    print()
    
    print(coloreaza("─" * 70, Culori.ALBASTRU))
    print(f"  {'Nr.':<5} {'Cerință':<10} {'Subrețea':<22} {'Disponibil':<12} {'Risipă':<10} {'Eficiență'}")
    print(coloreaza("─" * 70, Culori.ALBASTRU))
    
    total_cerut = 0
    total_alocat = 0
    
    for i, alocare in enumerate(alocari, 1):
        subretea = alocare['subretea']
        cerinta = alocare['cerinta']
        disponibil = subretea.num_addresses - 2
        risipa = disponibil - cerinta
        eficienta = (cerinta / disponibil) * 100 if disponibil > 0 else 0
        
        total_cerut += cerinta
        total_alocat += disponibil
        
        culoare_eficienta = Culori.VERDE if eficienta >= 50 else Culori.GALBEN
        
        print(f"  {i:<5} {cerinta:<10} {str(subretea):<22} {disponibil:<12} {risipa:<10} "
              f"{coloreaza(f'{eficienta:.1f}%', culoare_eficienta)}")
    
    print(coloreaza("─" * 70, Culori.ALBASTRU))
    
    eficienta_totala = (total_cerut / total_alocat) * 100 if total_alocat > 0 else 0
    
    print()
    print(f"  {coloreaza('Total cerut:', Culori.CYAN):30} {total_cerut} gazde")
    print(f"  {coloreaza('Total alocat:', Culori.CYAN):30} {total_alocat} gazde")
    print(f"  {coloreaza('Risipă totală:', Culori.CYAN):30} {total_alocat - total_cerut} adrese")
    print(f"  {coloreaza('Eficiență globală:', Culori.VERDE):30} {eficienta_totala:.1f}%")
    print()
    
    return 0


def cmd_comprimare_ipv6(adresa: str, ca_json: bool = False) -> int:
    """Comprimă o adresă IPv6 la forma scurtă."""
    try:
        comprimata = comprima_ipv6(adresa)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    if ca_json:
        print(json.dumps({
            "intrare": adresa,
            "comprimata": comprimata
        }, indent=2, ensure_ascii=False))
        return 0
    
    print()
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print(coloreaza("  Comprimare Adresă IPv6", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Adresă completă:', Culori.CYAN)}")
    print(f"    {adresa}")
    print()
    print(f"  {coloreaza('Adresă comprimată:', Culori.VERDE)}")
    print(f"    {comprimata}")
    print()
    
    print(coloreaza("  Reguli de comprimare aplicate:", Culori.GALBEN))
    print("  • Zerourile de început din fiecare grup sunt omise")
    print("  • Cel mai lung șir de grupuri consecutive de zerouri → ::")
    print("  • :: poate apărea o singură dată în adresă")
    print()
    
    return 0


def cmd_expandare_ipv6(adresa: str, ca_json: bool = False) -> int:
    """Expandează o adresă IPv6 comprimată la forma completă."""
    try:
        expandata = expandeaza_ipv6(adresa)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    if ca_json:
        print(json.dumps({
            "intrare": adresa,
            "expandata": expandata
        }, indent=2, ensure_ascii=False))
        return 0
    
    print()
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print(coloreaza("  Expandare Adresă IPv6", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Adresă comprimată:', Culori.CYAN)}")
    print(f"    {adresa}")
    print()
    print(f"  {coloreaza('Adresă expandată:', Culori.VERDE)}")
    print(f"    {expandata}")
    print()
    
    # Afișare pe grupuri
    grupuri = expandata.split(':')
    print(coloreaza("  Grupuri (16 biți fiecare):", Culori.GALBEN))
    for i, grup in enumerate(grupuri, 1):
        valoare = int(grup, 16)
        print(f"    Grup {i}: {grup} = {valoare} (zecimal)")
    print()
    
    return 0


def cmd_subretele_ipv6(prefix: str, numar: int, ca_json: bool = False) -> int:
    """Generează subrețele IPv6 dintr-un prefix dat."""
    try:
        subretele = subretele_ipv6_din_prefix(prefix, numar)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    if ca_json:
        print(json.dumps({
            "prefix_baza": prefix,
            "numar_cerut": numar,
            "subretele": [str(s) for s in subretele]
        }, indent=2, ensure_ascii=False))
        return 0
    
    print()
    print(coloreaza("═" * 70, Culori.ALBASTRU))
    print(coloreaza("  Generare Subrețele IPv6", Culori.BOLD))
    print(coloreaza("═" * 70, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Prefix de bază:', Culori.CYAN):30} {prefix}")
    print(f"  {coloreaza('Subrețele cerute:', Culori.CYAN):30} {numar}")
    print()
    
    print(coloreaza("─" * 70, Culori.ALBASTRU))
    print(f"  {'Nr.':<5} {'Subrețea':<45} {'Prefix'}")
    print(coloreaza("─" * 70, Culori.ALBASTRU))
    
    for i, subretea in enumerate(subretele, 1):
        print(f"  {i:<5} {str(subretea):<45} /{subretea.prefixlen}")
    
    print(coloreaza("─" * 70, Culori.ALBASTRU))
    print()
    
    if subretele:
        print(coloreaza("  Notă:", Culori.GALBEN))
        print(f"  • Fiecare subrețea /{subretele[0].prefixlen} conține 2^{128-subretele[0].prefixlen} adrese")
        print(f"  • Pentru rețele end-user, se recomandă alocare /64")
    print()
    
    return 0


def cmd_prefix_necesar(gazde: int) -> int:
    """Calculează prefixul necesar pentru un număr dat de gazde."""
    prefix = prefix_pentru_gazde(gazde)
    adrese_disponibile = 2 ** (32 - prefix)
    gazde_utilizabile = adrese_disponibile - 2
    
    print()
    print(coloreaza("═" * 50, Culori.ALBASTRU))
    print(coloreaza("  Calculator Prefix CIDR", Culori.BOLD))
    print(coloreaza("═" * 50, Culori.ALBASTRU))
    print()
    
    print(f"  {coloreaza('Gazde necesare:', Culori.CYAN):30} {gazde}")
    print(f"  {coloreaza('Prefix recomandat:', Culori.VERDE):30} /{prefix}")
    print(f"  {coloreaza('Adrese disponibile:', Culori.CYAN):30} {adrese_disponibile}")
    print(f"  {coloreaza('Gazde utilizabile:', Culori.CYAN):30} {gazde_utilizabile}")
    print()
    
    eficienta = (gazde / gazde_utilizabile) * 100
    print(f"  {coloreaza('Eficiență:', Culori.GALBEN):30} {eficienta:.1f}%")
    print()
    
    return 0


def construieste_parser() -> argparse.ArgumentParser:
    """Construiește parserul de argumente."""
    parser = argparse.ArgumentParser(
        description="Exercițiul 5.02 – Alocare VLSM și Operații IPv6",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  %(prog)s vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2
  %(prog)s ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
  %(prog)s ipv6-expandare "2001:db8::1"
  %(prog)s subretele-ipv6 "2001:db8:abcd::/48" --numar 8
  %(prog)s prefix-necesar 100
"""
    )
    
    subparsers = parser.add_subparsers(dest="comanda", required=True)
    
    # Subcomanda VLSM
    p_vlsm = subparsers.add_parser(
        "vlsm",
        help="Alocă subrețele folosind VLSM"
    )
    p_vlsm.add_argument(
        "baza",
        help="Rețea de bază în format CIDR (ex: 172.16.0.0/16)"
    )
    p_vlsm.add_argument(
        "--cerinte", "-c",
        required=True,
        help="Lista de cerințe de gazde, separate prin virgulă (ex: 500,120,60)"
    )
    p_vlsm.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ieșire în format JSON"
    )
    
    # Subcomanda comprimare IPv6
    p_comprimare = subparsers.add_parser(
        "ipv6-comprimare",
        help="Comprimă o adresă IPv6"
    )
    p_comprimare.add_argument(
        "adresa",
        help="Adresă IPv6 completă"
    )
    p_comprimare.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ieșire în format JSON"
    )
    
    # Subcomanda expandare IPv6
    p_expandare = subparsers.add_parser(
        "ipv6-expandare",
        help="Expandează o adresă IPv6 comprimată"
    )
    p_expandare.add_argument(
        "adresa",
        help="Adresă IPv6 comprimată"
    )
    p_expandare.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ieșire în format JSON"
    )
    
    # Subcomanda subrețele IPv6
    p_subretele = subparsers.add_parser(
        "subretele-ipv6",
        help="Generează subrețele IPv6"
    )
    p_subretele.add_argument(
        "prefix",
        help="Prefix IPv6 de bază (ex: 2001:db8:abcd::/48)"
    )
    p_subretele.add_argument(
        "--numar", "-n",
        type=int,
        default=8,
        help="Numărul de subrețele de generat (implicit: 8)"
    )
    p_subretele.add_argument(
        "--json", "-j",
        action="store_true",
        help="Ieșire în format JSON"
    )
    
    # Subcomanda prefix necesar
    p_prefix = subparsers.add_parser(
        "prefix-necesar",
        help="Calculează prefixul necesar pentru N gazde"
    )
    p_prefix.add_argument(
        "gazde",
        type=int,
        help="Numărul de gazde necesare"
    )
    
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Funcția principală."""
    parser = construieste_parser()
    args = parser.parse_args(argv)
    
    if args.comanda == "vlsm":
        cerinte = [int(x.strip()) for x in args.cerinte.split(',')]
        return cmd_vlsm(args.baza, cerinte, getattr(args, 'json', False))
    elif args.comanda == "ipv6-comprimare":
        return cmd_comprimare_ipv6(args.adresa, getattr(args, 'json', False))
    elif args.comanda == "ipv6-expandare":
        return cmd_expandare_ipv6(args.adresa, getattr(args, 'json', False))
    elif args.comanda == "subretele-ipv6":
        return cmd_subretele_ipv6(args.prefix, args.numar, getattr(args, 'json', False))
    elif args.comanda == "prefix-necesar":
        return cmd_prefix_necesar(args.gazde)
    
    return 1


if __name__ == "__main__":
    sys.exit(main())
