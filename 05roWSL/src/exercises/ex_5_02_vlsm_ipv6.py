#!/usr/bin/env python3
"""
Exercițiul 5.02 – Alocare VLSM și Operații IPv6
===============================================
CLI pentru alocarea VLSM și manipularea adreselor IPv6.

Utilizare:
    python ex_5_02_vlsm_ipv6.py vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2
    python ex_5_02_vlsm_ipv6.py invata-vlsm 192.168.0.0/24 --cerinte 60,20,10,2
    python ex_5_02_vlsm_ipv6.py ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
    python ex_5_02_vlsm_ipv6.py ipv6-expandare "2001:db8::1"
    python ex_5_02_vlsm_ipv6.py subretele-ipv6 "2001:db8:abcd::/48" --numar 8

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
    aloca_vlsm,
    comprima_ipv6,
    expandeaza_ipv6,
    subretele_ipv6_din_prefix,
    prefix_pentru_gazde,
    interval_gazde_ipv4,
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
    SFARSIT = '\033[0m'


def coloreaza(text: str, culoare: str) -> str:
    """Aplică culoare dacă stdout este un terminal."""
    if sys.stdout.isatty():
        return f"{culoare}{text}{Culori.SFARSIT}"
    return text


def cmd_vlsm(baza: str, cerinte: List[int], ca_json: bool = False) -> int:
    """Alocă subrețele folosind VLSM pentru cerințele date."""
    logger.debug(f"VLSM: {baza} cu cerințe {cerinte}")
    
    try:
        alocari = aloca_vlsm(baza, cerinte)
    except ValueError as e:
        logger.error(f"Eroare VLSM: {e}")
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


def cmd_invata_vlsm(baza: str, cerinte: List[int]) -> int:
    """
    Mod interactiv de învățare VLSM cu predicții.
    
    Studentul face predicții pentru fiecare pas al algoritmului VLSM,
    apoi primește feedback imediat.
    """
    print()
    print(coloreaza("═" * 60, Culori.GALBEN))
    print(coloreaza("  Mod Învățare: VLSM cu Predicții", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.GALBEN))
    print()
    print(f"  Rețea de bază: {coloreaza(baza, Culori.VERDE)}")
    print(f"  Cerințe originale: {coloreaza(str(cerinte), Culori.VERDE)}")
    print()
    
    # Calculează rezultatele în avans
    try:
        alocari = aloca_vlsm(baza, cerinte)
    except ValueError as e:
        print(coloreaza(f"Eroare: {e}", Culori.ROSU), file=sys.stderr)
        return 1
    
    scor = 0
    total_intrebari = 0
    
    # Cerințele sortate
    cerinte_sortate = sorted(cerinte, reverse=True)
    
    # ─────────────────────────────────────────────────────
    # Predicția 1: Ordinea de sortare
    # ─────────────────────────────────────────────────────
    print(coloreaza("─" * 60, Culori.CYAN))
    print(f"  {coloreaza('PASUL 1:', Culori.BOLD)} În ce ordine trebuie procesate cerințele în VLSM?")
    print()
    print("  Hint: VLSM alocă întâi subrețelele care au nevoie de mai mult spațiu")
    print()
    
    total_intrebari += 1
    try:
        raspuns = input("  Răspunsul tău (numerele separate prin virgulă): ").strip()
        raspuns_lista = [int(x.strip()) for x in raspuns.split(',') if x.strip()]
        
        if raspuns_lista == cerinte_sortate:
            print(coloreaza("  ✓ Corect! Sortăm descrescător pentru aliniere optimă.", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: {cerinte_sortate}", Culori.ROSU))
            print("    Explicație: Alocăm întâi cerințele mari pentru a evita fragmentarea.")
    except (ValueError, EOFError):
        print(coloreaza(f"  → Răspunsul corect era: {cerinte_sortate}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Predicția 2: Prefix pentru prima cerință (cea mai mare)
    # ─────────────────────────────────────────────────────
    prima_cerinta = cerinte_sortate[0]
    prefix_corect = prefix_pentru_gazde(prima_cerinta)
    
    print(coloreaza("─" * 60, Culori.CYAN))
    print(f"  {coloreaza('PASUL 2:', Culori.BOLD)} Ce prefix CIDR e necesar pentru {prima_cerinta} gazde?")
    print()
    print("  Formula: prefix = 32 - ceil(log2(gazde + 2))")
    print(f"  Calculează: 32 - ceil(log2({prima_cerinta} + 2))")
    print()
    
    total_intrebari += 1
    try:
        raspuns = input("  Prefixul necesar (doar numărul, ex: 26): ").strip()
        if raspuns.startswith('/'):
            raspuns = raspuns[1:]
        
        if int(raspuns) == prefix_corect:
            gazde_disp = 2 ** (32 - prefix_corect) - 2
            print(coloreaza(f"  ✓ Corect! /{prefix_corect} oferă {gazde_disp} gazde.", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: /{prefix_corect}", Culori.ROSU))
            import math
            calc = math.ceil(math.log2(prima_cerinta + 2))
            print(f"    Calcul: ceil(log2({prima_cerinta + 2})) = {calc}, prefix = 32 - {calc} = {prefix_corect}")
    except (ValueError, EOFError):
        print(coloreaza(f"  → Răspunsul corect era: /{prefix_corect}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Predicția 3: Adresa primei subrețele
    # ─────────────────────────────────────────────────────
    prima_subretea = alocari[0]['subretea']
    
    print(coloreaza("─" * 60, Culori.CYAN))
    print(f"  {coloreaza('PASUL 3:', Culori.BOLD)} Care este prima subrețea alocată?")
    print()
    print(f"  Rețeaua de bază este: {baza}")
    print(f"  Prefixul necesar este: /{prefix_corect}")
    print()
    
    total_intrebari += 1
    try:
        raspuns = input("  Prima subrețea (ex: 192.168.0.0/26): ").strip()
        
        if raspuns == str(prima_subretea):
            print(coloreaza("  ✓ Corect!", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Răspuns corect: {prima_subretea}", Culori.ROSU))
    except EOFError:
        print(coloreaza(f"  → Răspunsul corect era: {prima_subretea}", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Predicția 4: Eficiența
    # ─────────────────────────────────────────────────────
    total_cerut = sum(cerinte)
    total_alocat = sum(a['subretea'].num_addresses - 2 for a in alocari)
    eficienta_reala = round((total_cerut / total_alocat) * 100)
    
    print(coloreaza("─" * 60, Culori.CYAN))
    print(f"  {coloreaza('PASUL 4:', Culori.BOLD)} Estimează eficiența totală a alocării.")
    print()
    print(f"  Total gazde cerute: {total_cerut}")
    print("  Eficiența = (gazde cerute / gazde alocate) × 100%")
    print()
    
    total_intrebari += 1
    try:
        raspuns = input("  Eficiența estimată (ex: 75): ").strip()
        raspuns = int(raspuns.replace('%', ''))
        
        # Acceptă răspuns în intervalul ±10%
        if abs(raspuns - eficienta_reala) <= 10:
            print(coloreaza(f"  ✓ Apropiat! Eficiența reală: {eficienta_reala}%", Culori.VERDE))
            scor += 1
        else:
            print(coloreaza(f"  ✗ Eficiența reală: {eficienta_reala}%", Culori.ROSU))
            print(f"    Calcul: {total_cerut} / {total_alocat} × 100 = {eficienta_reala}%")
    except (ValueError, EOFError):
        print(coloreaza(f"  → Eficiența reală: {eficienta_reala}%", Culori.GALBEN))
    print()
    
    # ─────────────────────────────────────────────────────
    # Rezultat final
    # ─────────────────────────────────────────────────────
    print(coloreaza("═" * 60, Culori.GALBEN))
    print(f"  {coloreaza('REZULTAT:', Culori.BOLD)} {scor}/{total_intrebari} răspunsuri corecte")
    
    if scor == total_intrebari:
        print(coloreaza("  Excelent! Ai înțeles algoritmul VLSM.", Culori.VERDE))
    elif scor >= total_intrebari // 2:
        print(coloreaza("  Bine! Mai exersează cu alte cerințe.", Culori.GALBEN))
    else:
        print(coloreaza("  Recitește teoria VLSM și încearcă din nou.", Culori.ROSU))
    
    print(coloreaza("═" * 60, Culori.GALBEN))
    print()
    
    # Afișează alocarea completă
    print(coloreaza("  Alocarea VLSM completă:", Culori.BOLD))
    print()
    return cmd_vlsm(baza, cerinte, ca_json=False)


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
  %(prog)s invata-vlsm 192.168.0.0/24 --cerinte 60,20,10,2
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
    
    # Subcomanda invata-vlsm (NOU!)
    p_invata = subparsers.add_parser(
        "invata-vlsm",
        help="Mod învățare VLSM interactiv cu predicții"
    )
    p_invata.add_argument(
        "baza",
        help="Rețea de bază în format CIDR (ex: 192.168.0.0/24)"
    )
    p_invata.add_argument(
        "--cerinte", "-c",
        required=True,
        help="Lista de cerințe de gazde, separate prin virgulă (ex: 60,20,10,2)"
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
    elif args.comanda == "invata-vlsm":
        cerinte = [int(x.strip()) for x in args.cerinte.split(',')]
        return cmd_invata_vlsm(args.baza, cerinte)
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
