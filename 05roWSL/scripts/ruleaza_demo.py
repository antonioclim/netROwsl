#!/usr/bin/env python3
"""
Demonstrații Laborator Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest script rulează demonstrații automate pentru prezentări la tablă.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("ruleaza_demo")

# Importă modulele de exerciții
try:
    from src.utils.net_utils import (
        analizeaza_interfata_ipv4,
        imparte_flsm,
        aloca_vlsm,
        comprima_ipv6,
        expandeaza_ipv6,
        subretele_ipv6_din_prefix
    )
    UTILITARE_DISPONIBILE = True
except ImportError:
    UTILITARE_DISPONIBILE = False


def pauza(secunde: float = 1.0):
    """Pauză pentru efect vizual."""
    time.sleep(secunde)


def scrie_incet(text: str, intarziere: float = 0.02):
    """Scrie text caracter cu caracter pentru efect dramatic."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(intarziere)
    print()


def separator(titlu: str = ""):
    """Afișează un separator vizual."""
    print("\n" + "═" * 70)
    if titlu:
        print(f"  {titlu}")
        print("═" * 70)
    print()


def demo_cidr():
    """Demonstrație: Analiza blocurilor CIDR."""
    separator("DEMONSTRAȚIE: ANALIZA BLOCURILOR CIDR")
    
    if not UTILITARE_DISPONIBILE:
        logger.error("Modulele de utilitare nu sunt disponibile.")
        return
    
    adrese_test = [
        "192.168.10.14/26",
        "10.0.0.1/8",
        "172.16.50.100/20",
        "203.0.113.45/28"
    ]
    
    for adresa in adrese_test:
        print(f"┌─ Analiză: {adresa}")
        print("│")
        
        try:
            info = analizeaza_interfata_ipv4(adresa)
            
            print(f"│  Adresa IP:        {info.adresa_ip}")
            print(f"│  Adresa de rețea:  {info.adresa_retea}")
            print(f"│  Adresa broadcast: {info.adresa_broadcast}")
            print(f"│  Mască de rețea:   {info.masca_retea}")
            print(f"│  Prefix CIDR:      /{info.lungime_prefix}")
            print(f"│")
            print(f"│  Prima gazdă:      {info.prima_gazda}")
            print(f"│  Ultima gazdă:     {info.ultima_gazda}")
            print(f"│  Gazde utilizabile: {info.numar_gazde}")
            print(f"│")
            print(f"│  Tip adresă:       {'Privată' if info.este_privata else 'Publică'}")
            
            # Afișare binară
            octeti = str(info.adresa_ip).split('.')
            print(f"│")
            print(f"│  Reprezentare binară:")
            for i, octet in enumerate(octeti):
                binar = format(int(octet), '08b')
                print(f"│    Octet {i+1}: {octet:>3} = {binar}")
            
        except Exception as e:
            print(f"│  Eroare: {e}")
        
        print("└" + "─" * 50)
        pauza(0.5)
    
    separator()


def demo_vlsm():
    """Demonstrație: Comparație FLSM vs VLSM."""
    separator("DEMONSTRAȚIE: FLSM vs VLSM")
    
    if not UTILITARE_DISPONIBILE:
        logger.error("Modulele de utilitare nu sunt disponibile.")
        return
    
    retea_baza = "172.16.0.0/16"
    cerinte = [500, 120, 60, 30, 2]
    
    print(f"Rețea de bază: {retea_baza}")
    print(f"Cerințe departamente: {cerinte} gazde")
    print()
    
    # FLSM - toate subrețelele egale
    print("┌─ METODA FLSM (Fixed-Length Subnet Mask)")
    print("│")
    print("│  Toate subrețelele au aceeași dimensiune.")
    print("│  Dimensiunea trebuie să acomodeze cea mai mare cerință (500 gazde).")
    print("│")
    
    try:
        subretele_flsm = imparte_flsm(retea_baza, len(cerinte))
        total_alocat_flsm = 0
        total_necesar = sum(cerinte)
        
        for i, (subretea, cerinta) in enumerate(zip(subretele_flsm, cerinte)):
            gazde_disponibile = subretea.num_addresses - 2
            risipa = gazde_disponibile - cerinta
            total_alocat_flsm += gazde_disponibile
            eficienta = (cerinta / gazde_disponibile) * 100
            
            print(f"│  Dept {i+1}: {str(subretea):20} → {gazde_disponibile:5} gazde "
                  f"(cerință: {cerinta:3}, risipă: {risipa:4}, eficiență: {eficienta:5.1f}%)")
        
        eficienta_totala_flsm = (total_necesar / total_alocat_flsm) * 100
        print("│")
        print(f"│  Total alocat: {total_alocat_flsm} gazde")
        print(f"│  Total necesar: {total_necesar} gazde")
        print(f"│  Eficiență globală: {eficienta_totala_flsm:.1f}%")
        
    except Exception as e:
        print(f"│  Eroare FLSM: {e}")
    
    print("└" + "─" * 60)
    print()
    
    # VLSM - dimensiuni variabile
    print("┌─ METODA VLSM (Variable-Length Subnet Mask)")
    print("│")
    print("│  Fiecare subrețea are dimensiunea adaptată cerințelor.")
    print("│  Alocarea începe cu cele mai mari cerințe.")
    print("│")
    
    try:
        alocare_vlsm = aloca_vlsm(retea_baza, cerinte)
        total_alocat_vlsm = 0
        
        for alocare in alocare_vlsm:
            subretea = alocare['subretea']
            cerinta = alocare['cerinta']
            gazde_disponibile = subretea.num_addresses - 2
            risipa = gazde_disponibile - cerinta
            total_alocat_vlsm += gazde_disponibile
            eficienta = (cerinta / gazde_disponibile) * 100
            
            print(f"│  {str(subretea):20} → {gazde_disponibile:5} gazde "
                  f"(cerință: {cerinta:3}, risipă: {risipa:4}, eficiență: {eficienta:5.1f}%)")
        
        eficienta_totala_vlsm = (total_necesar / total_alocat_vlsm) * 100
        print("│")
        print(f"│  Total alocat: {total_alocat_vlsm} gazde")
        print(f"│  Total necesar: {total_necesar} gazde")
        print(f"│  Eficiență globală: {eficienta_totala_vlsm:.1f}%")
        
    except Exception as e:
        print(f"│  Eroare VLSM: {e}")
    
    print("└" + "─" * 60)
    
    # Comparație finală
    print()
    print("┌─ COMPARAȚIE")
    print("│")
    if 'eficienta_totala_flsm' in dir() and 'eficienta_totala_vlsm' in dir():
        imbunatatire = eficienta_totala_vlsm - eficienta_totala_flsm
        print(f"│  FLSM: {eficienta_totala_flsm:5.1f}% eficiență")
        print(f"│  VLSM: {eficienta_totala_vlsm:5.1f}% eficiență")
        print(f"│")
        print(f"│  VLSM îmbunătățește eficiența cu {imbunatatire:.1f} puncte procentuale")
    print("└" + "─" * 60)
    
    separator()


def demo_ipv6():
    """Demonstrație: Operații cu adrese IPv6."""
    separator("DEMONSTRAȚIE: OPERAȚII IPv6")
    
    if not UTILITARE_DISPONIBILE:
        logger.error("Modulele de utilitare nu sunt disponibile.")
        return
    
    adrese_test = [
        "2001:0db8:0000:0000:0000:0000:0000:0001",
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "fe80:0000:0000:0000:0000:0000:0000:0001",
        "0000:0000:0000:0000:0000:0000:0000:0001"
    ]
    
    print("┌─ COMPRIMARE IPv6")
    print("│")
    print("│  Regulile de comprimare IPv6:")
    print("│  1. Zerourile de început din fiecare grup pot fi omise")
    print("│  2. Un singur grup consecutiv de zerouri poate fi înlocuit cu ::")
    print("│")
    
    for adresa in adrese_test:
        try:
            comprimata = comprima_ipv6(adresa)
            print(f"│  {adresa}")
            print(f"│  → {comprimata}")
            print("│")
        except Exception as e:
            print(f"│  Eroare: {e}")
    
    print("└" + "─" * 60)
    print()
    
    print("┌─ EXPANDARE IPv6")
    print("│")
    
    adrese_comprimate = ["2001:db8::1", "::1", "fe80::1", "2001:db8:85a3::8a2e:370:7334"]
    
    for adresa in adrese_comprimate:
        try:
            expandata = expandeaza_ipv6(adresa)
            print(f"│  {adresa}")
            print(f"│  → {expandata}")
            print("│")
        except Exception as e:
            print(f"│  Eroare: {e}")
    
    print("└" + "─" * 60)
    print()
    
    print("┌─ GENERARE SUBREȚELE IPv6")
    print("│")
    print("│  Dintr-o alocare /48, generăm subrețele /64:")
    print("│")
    
    try:
        prefix_baza = "2001:db8:abcd::/48"
        subretele = subretele_ipv6_din_prefix(prefix_baza, 8)
        
        print(f"│  Prefix de bază: {prefix_baza}")
        print("│")
        for i, subretea in enumerate(subretele):
            print(f"│  Subrețea {i+1}: {subretea}")
    except Exception as e:
        print(f"│  Eroare: {e}")
    
    print("└" + "─" * 60)
    
    separator()


def demo_udp():
    """Demonstrație: Comunicare UDP între containere."""
    separator("DEMONSTRAȚIE: COMUNICARE UDP")
    
    print("Această demonstrație trimite mesaje UDP între containere Docker.")
    print()
    print("Arhitectura:")
    print("  ┌─────────────┐         ┌─────────────┐")
    print("  │ UDP Client  │ ──UDP──>│ UDP Server  │")
    print("  │ 10.5.0.30   │<──────  │ 10.5.0.20   │")
    print("  └─────────────┘  Echo   │ Port: 9999  │")
    print("                          └─────────────┘")
    print()
    
    # Verifică că containerele rulează
    print("Verificare containere...")
    rezultat = subprocess.run(
        ["docker", "ps", "--format", "{{.Names}}"],
        capture_output=True, text=True
    )
    
    containere_necesare = ["week5_udp-server", "week5_udp-client"]
    containere_active = rezultat.stdout.strip().split('\n')
    
    toate_active = all(c in containere_active for c in containere_necesare)
    
    if not toate_active:
        logger.error("Containerele necesare nu sunt active.")
        logger.info("Rulați mai întâi: python scripts/porneste_laborator.py")
        return
    
    print("✓ Toate containerele sunt active")
    print()
    
    # Trimite mesaje de test
    mesaje_test = [
        "Salut de la ASE!",
        "Test rețea IPv4",
        "Echo UDP funcționează",
    ]
    
    print("┌─ TRIMITERE MESAJE UDP")
    print("│")
    
    for mesaj in mesaje_test:
        print(f"│  Trimitere: '{mesaj}'")
        
        # Trimite mesajul folosind netcat
        cmd = [
            "docker", "exec", "week5_udp-client",
            "sh", "-c",
            f"echo '{mesaj}' | nc -u -w1 10.5.0.20 9999"
        ]
        
        rezultat = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        
        if rezultat.stdout:
            print(f"│  Răspuns: '{rezultat.stdout.strip()}'")
        else:
            print("│  (Server echo - mesajul a fost primit)")
        
        pauza(0.5)
    
    print("│")
    print("└" + "─" * 60)
    print()
    
    print("Pentru a captura acest trafic în Wireshark:")
    print("  1. python scripts/captureaza_trafic.py --filtru udp")
    print("  2. Rulați din nou această demonstrație")
    print("  3. Analizați pachetele capturate")
    
    separator()


# Dicționar cu toate demonstrațiile disponibile
DEMONSTRATII = {
    "cidr": {
        "functie": demo_cidr,
        "descriere": "Analiza blocurilor CIDR și reprezentare binară"
    },
    "vlsm": {
        "functie": demo_vlsm,
        "descriere": "Comparație FLSM vs VLSM pentru eficiența alocării"
    },
    "ipv6": {
        "functie": demo_ipv6,
        "descriere": "Comprimare, expandare și subnetare IPv6"
    },
    "udp": {
        "functie": demo_udp,
        "descriere": "Comunicare UDP între containere Docker"
    },
    "toate": {
        "functie": None,
        "descriere": "Rulează toate demonstrațiile în ordine"
    }
}


def main():
    parser = argparse.ArgumentParser(
        description="Rulează demonstrații pentru Săptămâna 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Demonstrații disponibile:
  cidr  - Analiza blocurilor CIDR și reprezentare binară
  vlsm  - Comparație FLSM vs VLSM pentru eficiența alocării
  ipv6  - Comprimare, expandare și subnetare IPv6
  udp   - Comunicare UDP între containere Docker
  toate - Rulează toate demonstrațiile în ordine

Exemple:
  python ruleaza_demo.py --demo cidr
  python ruleaza_demo.py --demo vlsm
  python ruleaza_demo.py --demo toate
        """
    )
    
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMONSTRATII.keys()),
        required=True,
        help="Demonstrația de rulat"
    )
    parser.add_argument(
        "--pauza", "-p",
        type=float,
        default=2.0,
        help="Pauza între demonstrații când rulați 'toate' (implicit: 2.0s)"
    )

    args = parser.parse_args()

    print()
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║     DEMONSTRAȚII LABORATOR - SĂPTĂMÂNA 5                        ║")
    print("║     Nivelul Rețea: Adresare IPv4/IPv6 și Subnetare              ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print()

    if args.demo == "toate":
        # Rulează toate demonstrațiile
        for nume, demo in DEMONSTRATII.items():
            if nume != "toate" and demo["functie"]:
                print(f"\n>>> Rulare demonstrație: {demo['descriere']}")
                demo["functie"]()
                time.sleep(args.pauza)
    else:
        # Rulează demonstrația specificată
        DEMONSTRATII[args.demo]["functie"]()

    print("\n✓ Demonstrație completă.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
