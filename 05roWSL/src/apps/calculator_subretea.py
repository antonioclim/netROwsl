#!/usr/bin/env python3
"""
Calculator de Subrețea
======================
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Instrument interactiv pentru calculele de subnetare IPv4.

Utilizare:
    python calculator_subretea.py                  Mod interactiv
    python calculator_subretea.py 192.168.1.0/24  Analiză directă
"""

import argparse
import sys
from pathlib import Path

# Import utilitar local
RADACINA = Path(__file__).resolve().parents[2]
if str(RADACINA) not in sys.path:
    sys.path.insert(0, str(RADACINA))

from src.utils.net_utils import (
    analizeaza_interfata_ipv4,
    imparte_flsm,
    aloca_vlsm,
    prefix_pentru_gazde,
    prefix_la_masca,
    masca_la_prefix,
    ip_la_binar_punctat,
)


# Coduri culori ANSI
class Culori:
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


def afiseaza_meniu():
    """Afișează meniul principal."""
    print()
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print(coloreaza("  Calculator de Subrețea - Meniu Principal", Culori.BOLD))
    print(coloreaza("═" * 60, Culori.ALBASTRU))
    print()
    print("  1. Analizează o adresă CIDR")
    print("  2. Împarte rețea în subrețele egale (FLSM)")
    print("  3. Alocare VLSM pentru cerințe multiple")
    print("  4. Calculează prefix pentru N gazde")
    print("  5. Conversie prefix ↔ mască")
    print("  6. Reprezentare binară IP")
    print()
    print("  0. Ieșire")
    print()


def optiune_analiza():
    """Opțiunea 1: Analiza CIDR."""
    print(coloreaza("\n─── Analiză CIDR ───", Culori.CYAN))
    
    cidr = input("  Introduceți adresa CIDR (ex: 192.168.10.14/26): ").strip()
    
    if not cidr:
        return
    
    try:
        info = analizeaza_interfata_ipv4(cidr)
        
        print()
        print(f"  {coloreaza('Adresa IP:', Culori.CYAN):30} {info.adresa}")
        print(f"  {coloreaza('Tip adresă:', Culori.CYAN):30} {info.tip_adresa}")
        print(f"  {coloreaza('Adresa de rețea:', Culori.CYAN):30} {info.retea.network_address}")
        print(f"  {coloreaza('Mască de rețea:', Culori.CYAN):30} {info.masca}")
        print(f"  {coloreaza('Prefix:', Culori.CYAN):30} /{info.retea.prefixlen}")
        print(f"  {coloreaza('Adresa broadcast:', Culori.CYAN):30} {info.broadcast}")
        print(f"  {coloreaza('Gazde utilizabile:', Culori.VERDE):30} {info.gazde_utilizabile}")
        print(f"  {coloreaza('Prima gazdă:', Culori.CYAN):30} {info.prima_gazda or 'N/A'}")
        print(f"  {coloreaza('Ultima gazdă:', Culori.CYAN):30} {info.ultima_gazda or 'N/A'}")
        
    except ValueError as e:
        print(coloreaza(f"  Eroare: {e}", Culori.ROSU))


def optiune_flsm():
    """Opțiunea 2: Subnetare FLSM."""
    print(coloreaza("\n─── Subnetare FLSM ───", Culori.CYAN))
    
    baza = input("  Rețea de bază (ex: 192.168.100.0/24): ").strip()
    if not baza:
        return
    
    try:
        n = int(input("  Număr de subrețele (putere de 2): ").strip())
    except ValueError:
        print(coloreaza("  Eroare: Introduceți un număr valid.", Culori.ROSU))
        return
    
    try:
        subretele = imparte_flsm(baza, n)
        
        print()
        print(f"  {'Nr.':<5} {'Subrețea':<22} {'Broadcast':<18} {'Gazde'}")
        print("  " + "─" * 55)
        
        for i, s in enumerate(subretele, 1):
            gazde = s.num_addresses - 2
            print(f"  {i:<5} {str(s):<22} {str(s.broadcast_address):<18} {gazde}")
        
    except ValueError as e:
        print(coloreaza(f"  Eroare: {e}", Culori.ROSU))


def optiune_vlsm():
    """Opțiunea 3: Alocare VLSM."""
    print(coloreaza("\n─── Alocare VLSM ───", Culori.CYAN))
    
    baza = input("  Rețea de bază (ex: 172.16.0.0/16): ").strip()
    if not baza:
        return
    
    cerinte_str = input("  Cerințe gazde, separate prin virgulă (ex: 500,120,60): ").strip()
    
    try:
        cerinte = [int(x.strip()) for x in cerinte_str.split(',')]
    except ValueError:
        print(coloreaza("  Eroare: Format invalid pentru cerințe.", Culori.ROSU))
        return
    
    try:
        alocari = aloca_vlsm(baza, cerinte)
        
        print()
        print(f"  {'Cerință':<10} {'Subrețea':<22} {'Disponibil':<12} {'Eficiență'}")
        print("  " + "─" * 55)
        
        for a in alocari:
            disponibil = a['subretea'].num_addresses - 2
            eficienta = (a['cerinta'] / disponibil) * 100
            print(f"  {a['cerinta']:<10} {str(a['subretea']):<22} {disponibil:<12} {eficienta:.1f}%")
        
    except ValueError as e:
        print(coloreaza(f"  Eroare: {e}", Culori.ROSU))


def optiune_prefix_gazde():
    """Opțiunea 4: Prefix pentru N gazde."""
    print(coloreaza("\n─── Calculator Prefix ───", Culori.CYAN))
    
    try:
        gazde = int(input("  Număr de gazde necesare: ").strip())
    except ValueError:
        print(coloreaza("  Eroare: Introduceți un număr valid.", Culori.ROSU))
        return
    
    prefix = prefix_pentru_gazde(gazde)
    disponibile = (2 ** (32 - prefix)) - 2
    
    print()
    print(f"  {coloreaza('Prefix recomandat:', Culori.VERDE):30} /{prefix}")
    print(f"  {coloreaza('Mască:', Culori.CYAN):30} {prefix_la_masca(prefix)}")
    print(f"  {coloreaza('Gazde disponibile:', Culori.CYAN):30} {disponibile}")
    print(f"  {coloreaza('Eficiență:', Culori.CYAN):30} {(gazde/disponibile)*100:.1f}%")


def optiune_conversie_masca():
    """Opțiunea 5: Conversie prefix ↔ mască."""
    print(coloreaza("\n─── Conversie Prefix/Mască ───", Culori.CYAN))
    print("  1. Prefix → Mască")
    print("  2. Mască → Prefix")
    
    alegere = input("  Alegeți (1/2): ").strip()
    
    if alegere == "1":
        try:
            prefix = int(input("  Prefix (ex: 24): ").strip().replace("/", ""))
            masca = prefix_la_masca(prefix)
            print(f"\n  /{prefix} = {coloreaza(masca, Culori.VERDE)}")
        except ValueError as e:
            print(coloreaza(f"  Eroare: {e}", Culori.ROSU))
            
    elif alegere == "2":
        masca = input("  Mască (ex: 255.255.255.0): ").strip()
        try:
            prefix = masca_la_prefix(masca)
            print(f"\n  {masca} = {coloreaza(f'/{prefix}', Culori.VERDE)}")
        except Exception as e:
            print(coloreaza(f"  Eroare: {e}", Culori.ROSU))


def optiune_binar():
    """Opțiunea 6: Reprezentare binară."""
    print(coloreaza("\n─── Reprezentare Binară ───", Culori.CYAN))
    
    ip = input("  Adresă IP (ex: 192.168.1.1): ").strip()
    
    if not ip:
        return
    
    try:
        binar = ip_la_binar_punctat(ip)
        print(f"\n  {ip} = {coloreaza(binar, Culori.VERDE)}")
        
        # Afișare pe octeți
        octeti = ip.split('.')
        print("\n  Pe octeți:")
        for i, octet in enumerate(octeti, 1):
            oct_bin = bin(int(octet))[2:].zfill(8)
            print(f"    Octet {i}: {octet:>3} = {oct_bin}")
            
    except Exception as e:
        print(coloreaza(f"  Eroare: {e}", Culori.ROSU))


def mod_interactiv():
    """Rulează calculatorul în mod interactiv."""
    print()
    print(coloreaza("╔══════════════════════════════════════════════════════════╗", Culori.ALBASTRU))
    print(coloreaza("║         Calculator de Subrețea - Săptămâna 5             ║", Culori.ALBASTRU))
    print(coloreaza("║     Rețele de Calculatoare - ASE, Informatică Economică  ║", Culori.ALBASTRU))
    print(coloreaza("╚══════════════════════════════════════════════════════════╝", Culori.ALBASTRU))
    
    while True:
        afiseaza_meniu()
        
        alegere = input(coloreaza("  Alegeți o opțiune: ", Culori.GALBEN)).strip()
        
        if alegere == "0":
            print("\n  La revedere!")
            break
        elif alegere == "1":
            optiune_analiza()
        elif alegere == "2":
            optiune_flsm()
        elif alegere == "3":
            optiune_vlsm()
        elif alegere == "4":
            optiune_prefix_gazde()
        elif alegere == "5":
            optiune_conversie_masca()
        elif alegere == "6":
            optiune_binar()
        else:
            print(coloreaza("  Opțiune invalidă.", Culori.ROSU))
        
        input("\n  Apăsați Enter pentru a continua...")


def main():
    parser = argparse.ArgumentParser(
        description="Calculator de Subrețea",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  %(prog)s                        Mod interactiv
  %(prog)s 192.168.1.0/24         Analiză directă
  %(prog)s --prefix 24            Conversie prefix → mască
"""
    )
    
    parser.add_argument(
        "cidr",
        nargs="?",
        help="Adresă CIDR pentru analiză directă"
    )
    parser.add_argument(
        "--prefix", "-p",
        type=int,
        help="Convertește prefix la mască"
    )
    
    args = parser.parse_args()
    
    if args.prefix:
        try:
            masca = prefix_la_masca(args.prefix)
            print(f"/{args.prefix} = {masca}")
        except ValueError as e:
            print(f"Eroare: {e}", file=sys.stderr)
            return 1
    elif args.cidr:
        try:
            info = analizeaza_interfata_ipv4(args.cidr)
            print(f"Rețea: {info.retea.network_address}/{info.retea.prefixlen}")
            print(f"Broadcast: {info.broadcast}")
            print(f"Gazde: {info.gazde_utilizabile}")
            print(f"Interval: {info.prima_gazda} - {info.ultima_gazda}")
        except ValueError as e:
            print(f"Eroare: {e}", file=sys.stderr)
            return 1
    else:
        mod_interactiv()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
