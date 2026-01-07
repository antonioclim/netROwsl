#!/usr/bin/env python3
"""
Script Demonstrații Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script execută demonstrații automate pentru
nivelul Sesiune (L5) și nivelul Prezentare (L6).
"""

import subprocess
import sys
import time
import struct
import zlib
import argparse
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import (
    configureaza_logger,
    afiseaza_banner,
    afiseaza_succes,
    afiseaza_eroare,
    afiseaza_info
)

logger = configureaza_logger("ruleaza_demo")


# Lista demonstrațiilor disponibile
DEMONSTRATII = {
    "endianness": {
        "titlu": "Conversie Endianness",
        "descriere": "Demonstrează diferențele între big-endian și little-endian"
    },
    "ftp_sesiune": {
        "titlu": "Sesiune FTP Completă",
        "descriere": "Simulează fluxul de autentificare și comenzi FTP"
    },
    "multi_client": {
        "titlu": "Testare Multi-Client",
        "descriere": "Demonstrează accesul concurent la serverul FTP"
    },
    "protocol_binar": {
        "titlu": "Protocol Binar Personalizat",
        "descriere": "Construirea unui mesaj cu header, payload și CRC"
    }
}


def demo_endianness():
    """Demonstrație conversie endianness."""
    afiseaza_banner("Demonstrație Endianness", "Ordinea octeților în reprezentarea binară")
    
    valoare = 0x12345678
    print(f"Valoare originală: 0x{valoare:08X} ({valoare})")
    print()
    
    # Big-endian (ordinea rețelei)
    big_endian = struct.pack(">I", valoare)
    print("Big-Endian (ordinea rețelei):")
    print(f"  Octeți: {' '.join(f'{b:02X}' for b in big_endian)}")
    print(f"  Reprezentare: {big_endian.hex()}")
    print("  Ordinea: Octetul cel mai semnificativ PRIMUL")
    print()
    
    # Little-endian (Intel/AMD)
    little_endian = struct.pack("<I", valoare)
    print("Little-Endian (Intel/AMD):")
    print(f"  Octeți: {' '.join(f'{b:02X}' for b in little_endian)}")
    print(f"  Reprezentare: {little_endian.hex()}")
    print("  Ordinea: Octetul cel mai puțin semnificativ PRIMUL")
    print()
    
    # Decodare inversă
    print("Decodare inversă (ce s-ar întâmpla la citire greșită):")
    gresit = struct.unpack("<I", big_endian)[0]
    print(f"  Dacă citim big-endian ca little-endian: 0x{gresit:08X}")
    print(f"  Diferența: {abs(valoare - gresit):,} (eroare masivă!)")
    print()
    
    afiseaza_succes("Concluzie: Folosiți ÎNTOTDEAUNA ordinea rețelei (big-endian) pentru protocoale!")


def demo_ftp_sesiune():
    """Demonstrație sesiune FTP."""
    afiseaza_banner("Demonstrație Sesiune FTP", "Fluxul de autentificare și comenzi")
    
    print("Simulare dialog FTP:")
    print("-" * 50)
    
    dialog = [
        ("SERVER", "220 Bine ați venit la serverul FTP"),
        ("CLIENT", "USER test"),
        ("SERVER", "331 Parola este necesară pentru test"),
        ("CLIENT", "PASS 12345"),
        ("SERVER", "230 Autentificare reușită"),
        ("CLIENT", "PWD"),
        ("SERVER", "257 \"/\" este directorul curent"),
        ("CLIENT", "PASV"),
        ("SERVER", "227 Entering Passive Mode (127,0,0,1,234,96)"),
        ("CLIENT", "LIST"),
        ("SERVER", "150 Se deschide conexiunea de date"),
        ("SERVER", "226 Transfer complet"),
        ("CLIENT", "QUIT"),
        ("SERVER", "221 La revedere"),
    ]
    
    for expeditor, mesaj in dialog:
        prefix = ">>>" if expeditor == "CLIENT" else "<<<"
        culoare = "\033[94m" if expeditor == "CLIENT" else "\033[92m"
        print(f"{culoare}{prefix} [{expeditor}] {mesaj}\033[0m")
        time.sleep(0.3)
    
    print("-" * 50)
    print()
    
    afiseaza_info("Observații importante:")
    print("  • Coduri 2xx = Succes")
    print("  • Coduri 3xx = Acțiune incompletă, se așteaptă mai multe date")
    print("  • Coduri 4xx/5xx = Erori")
    print("  • PASV returnează adresa pentru conexiunea de date")


def demo_multi_client():
    """Demonstrație multi-client."""
    afiseaza_banner("Demonstrație Multi-Client", "Acces concurent la serverul FTP")
    
    print("Simulare a doi clienți conectați simultan:\n")
    
    actiuni = [
        ("Client 1", "Conectare", "220 Bine ați venit"),
        ("Client 2", "Conectare", "220 Bine ați venit"),
        ("Client 1", "USER alice", "331 Parola necesară"),
        ("Client 2", "USER bob", "331 Parola necesară"),
        ("Client 1", "PASS secret1", "230 Autentificat ca alice"),
        ("Client 2", "PASS secret2", "230 Autentificat ca bob"),
        ("Client 1", "LIST", "226 Listare completă (alice)"),
        ("Client 2", "RETR fisier.txt", "226 Transfer complet (bob)"),
        ("Client 1", "QUIT", "221 La revedere alice"),
        ("Client 2", "QUIT", "221 La revedere bob"),
    ]
    
    for client, comanda, raspuns in actiuni:
        culoare = "\033[93m" if client == "Client 1" else "\033[95m"
        print(f"{culoare}[{client}] {comanda}\033[0m")
        print(f"         └─ {raspuns}")
        time.sleep(0.2)
    
    print()
    afiseaza_info("Observații:")
    print("  • Fiecare client are propria sesiune")
    print("  • Serverul gestionează conexiuni concurente")
    print("  • Autentificarea este independentă per sesiune")


def demo_protocol_binar():
    """Demonstrație protocol binar personalizat."""
    afiseaza_banner("Demonstrație Protocol Binar", "Construirea unui mesaj cu header și CRC")
    
    # Format header: MAGIC(4) + VERSIUNE(1) + TIP(1) + LUNGIME(4) + CRC(4) = 14 octeți
    MAGIC = b"FTPC"
    VERSIUNE = 1
    TIP_TEXT = 0x01
    
    payload = "Salut, lume!".encode('utf-8')
    print(f"Payload: \"{payload.decode()}\"")
    print(f"Lungime payload: {len(payload)} octeți")
    print()
    
    # Calculează CRC-32
    crc = zlib.crc32(payload) & 0xFFFFFFFF
    print(f"CRC-32: 0x{crc:08X}")
    print()
    
    # Construiește header-ul
    header = struct.pack(">4sBBII", MAGIC, VERSIUNE, TIP_TEXT, len(payload), crc)
    print("Structura header-ului:")
    print(f"  Format: >4sBBII (14 octeți)")
    print(f"  • Magic:    {MAGIC} ({header[0:4].hex()})")
    print(f"  • Versiune: {VERSIUNE} ({header[4]:02X})")
    print(f"  • Tip:      {TIP_TEXT} ({header[5]:02X}) - TEXT")
    print(f"  • Lungime:  {len(payload)} ({header[6:10].hex()})")
    print(f"  • CRC-32:   0x{crc:08X} ({header[10:14].hex()})")
    print()
    
    # Mesaj complet
    mesaj_complet = header + payload
    print("Mesaj complet (header + payload):")
    print(f"  Hex: {mesaj_complet.hex()}")
    print(f"  Lungime totală: {len(mesaj_complet)} octeți")
    print()
    
    # Verificare CRC
    crc_verificare = zlib.crc32(payload) & 0xFFFFFFFF
    if crc_verificare == crc:
        afiseaza_succes(f"Verificare CRC: REUȘITĂ (0x{crc_verificare:08X})")
    else:
        afiseaza_eroare("Verificare CRC: EȘUATĂ")


def ruleaza_demo(nume_demo: str) -> bool:
    """
    Rulează o demonstrație specifică.
    
    Argumente:
        nume_demo: Numele demonstrației de rulat
        
    Returnează:
        True dacă a reușit, False altfel
    """
    demo_functions = {
        "endianness": demo_endianness,
        "ftp_sesiune": demo_ftp_sesiune,
        "multi_client": demo_multi_client,
        "protocol_binar": demo_protocol_binar,
    }
    
    if nume_demo not in demo_functions:
        logger.error(f"Demonstrație necunoscută: {nume_demo}")
        return False
    
    try:
        demo_functions[nume_demo]()
        return True
    except Exception as e:
        logger.error(f"Eroare la rularea demonstrației: {e}")
        return False


def afiseaza_lista_demo():
    """Afișează lista demonstrațiilor disponibile."""
    afiseaza_banner("Demonstrații Disponibile", "Săptămâna 9")
    
    for nume, info in DEMONSTRATII.items():
        print(f"  \033[96m{nume}\033[0m")
        print(f"    {info['titlu']}")
        print(f"    {info['descriere']}")
        print()
    
    print("Utilizare:")
    print("  python scripts/ruleaza_demo.py --demo <nume>")
    print("  python scripts/ruleaza_demo.py --toate")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Rulează demonstrațiile pentru Săptămâna 9"
    )
    parser.add_argument(
        "--demo",
        type=str,
        choices=list(DEMONSTRATII.keys()),
        help="Numele demonstrației de rulat"
    )
    parser.add_argument(
        "--lista",
        action="store_true",
        help="Afișează lista demonstrațiilor disponibile"
    )
    parser.add_argument(
        "--toate",
        action="store_true",
        help="Rulează toate demonstrațiile"
    )
    args = parser.parse_args()

    if args.lista:
        afiseaza_lista_demo()
        return 0
    
    if args.toate:
        for nume in DEMONSTRATII.keys():
            ruleaza_demo(nume)
            print("\n" + "=" * 60 + "\n")
            time.sleep(1)
        return 0
    
    if args.demo:
        succes = ruleaza_demo(args.demo)
        return 0 if succes else 1
    
    # Fără argumente, afișează ajutor
    parser.print_help()
    print()
    afiseaza_lista_demo()
    return 0


if __name__ == "__main__":
    sys.exit(main())
