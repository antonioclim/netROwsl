#!/usr/bin/env python3
"""
Script Demonstrații Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script rulează demonstrații automate ale protocoalelor.
"""

import subprocess
import sys
import time
import socket
import struct
import argparse
import binascii
from pathlib import Path

# Adaugă rădăcina proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.network_utils import UtilitareRetea

logger = configureaza_logger("demo")


def print_titlu(titlu: str):
    """Afișează un titlu formatat."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60 + "\n")


def print_pas(numar: int, descriere: str):
    """Afișează un pas în demonstrație."""
    print(f"\n  \033[1mPasul {numar}:\033[0m {descriere}")


def print_trimis(mesaj: str):
    """Afișează un mesaj trimis."""
    print(f"    \033[94m→ TRIMIS:\033[0m {mesaj}")


def print_primit(mesaj: str):
    """Afișează un mesaj primit."""
    print(f"    \033[92m← PRIMIT:\033[0m {mesaj}")


def print_info(mesaj: str):
    """Afișează informații suplimentare."""
    print(f"    ℹ️  {mesaj}")


def demo_protocol_text():
    """Demonstrație Protocol TEXT."""
    print_titlu("DEMO 1: PROTOCOL TEXT")
    
    print("Protocolul TEXT folosește mesaje lizibile cu format: <LUNGIME> <CONȚINUT>")
    print("Serverul menține un magazin cheie-valoare și răspunde la comenzi.\n")
    
    util_retea = UtilitareRetea()
    
    # Verifică dacă serverul rulează
    if not util_retea.verifica_port_activ(5400):
        print("\033[91mEroare: Serverul TEXT nu rulează pe port 5400\033[0m")
        print("Porniți laboratorul cu: python scripts/start_lab.py")
        return False
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5400))
        sock.settimeout(5)
        
        comenzi = [
            ("4 PING", "Test conectivitate"),
            ("13 SET cheie val", "Setare valoare"),
            ("9 GET cheie", "Citire valoare"),
            ("5 COUNT", "Numărare chei"),
            ("4 KEYS", "Listare chei"),
            ("9 DEL cheie", "Ștergere cheie"),
            ("4 QUIT", "Închidere conexiune")
        ]
        
        for i, (comanda, descriere) in enumerate(comenzi, 1):
            print_pas(i, descriere)
            print_trimis(repr(comanda))
            
            sock.sendall(comanda.encode() + b'\n')
            
            if comanda == "4 QUIT":
                print_primit("Conexiune închisă")
                break
            
            raspuns = sock.recv(1024).decode().strip()
            print_primit(repr(raspuns))
            
            # Explicație
            if "PING" in comanda:
                print_info("Serverul confirmă că este activ cu PONG")
            elif "SET" in comanda:
                print_info("Valoarea a fost stocată în magazinul cheie-valoare")
            elif "GET" in comanda:
                print_info("Serverul returnează valoarea asociată cheii")
            
            time.sleep(0.5)
        
        sock.close()
        print("\n\033[92m✓ Demonstrația Protocol TEXT completă!\033[0m")
        return True
        
    except Exception as e:
        print(f"\033[91mEroare: {e}\033[0m")
        return False


def demo_protocol_binar():
    """Demonstrație Protocol BINAR."""
    print_titlu("DEMO 2: PROTOCOL BINAR")
    
    print("Protocolul BINAR folosește anteturi fixe de 14 octeți cu verificare CRC32.")
    print("Format: Magic(2) | Versiune(1) | Tip(1) | Lungime(2) | Secvență(4) | CRC32(4)\n")
    
    util_retea = UtilitareRetea()
    
    if not util_retea.verifica_port_activ(5401):
        print("\033[91mEroare: Serverul BINAR nu rulează pe port 5401\033[0m")
        print("Porniți laboratorul cu: python scripts/start_lab.py")
        return False
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 5401))
        sock.settimeout(5)
        
        print_pas(1, "Construire mesaj PING binar")
        
        # Construiește mesaj PING
        magic = b'NP'
        versiune = 1
        tip_mesaj = 0x01  # PING
        payload = b''
        lungime = len(payload)
        secventa = 1
        
        # Împachetare fără CRC
        antet_fara_crc = struct.pack('!2sBBHI', magic, versiune, tip_mesaj, lungime, secventa)
        crc = binascii.crc32(antet_fara_crc + payload) & 0xFFFFFFFF
        
        # Mesaj complet
        mesaj = struct.pack('!2sBBHII', magic, versiune, tip_mesaj, lungime, secventa, crc) + payload
        
        print(f"    Magic:     {magic.decode()}")
        print(f"    Versiune:  {versiune}")
        print(f"    Tip:       0x{tip_mesaj:02X} (PING)")
        print(f"    Lungime:   {lungime}")
        print(f"    Secvență:  {secventa}")
        print(f"    CRC32:     0x{crc:08X}")
        print(f"    Total:     {len(mesaj)} octeți")
        
        print_pas(2, "Trimitere mesaj")
        print_trimis(f"{mesaj.hex()}")
        sock.sendall(mesaj)
        
        print_pas(3, "Recepție răspuns")
        raspuns = sock.recv(1024)
        print_primit(f"{raspuns.hex()}")
        
        # Parsează răspunsul
        if len(raspuns) >= 14:
            r_magic, r_versiune, r_tip, r_lungime, r_secventa, r_crc = struct.unpack('!2sBBHII', raspuns[:14])
            print_info(f"Tip răspuns: 0x{r_tip:02X} (PONG)")
            print_info(f"CRC32 răspuns: 0x{r_crc:08X}")
        
        sock.close()
        print("\n\033[92m✓ Demonstrația Protocol BINAR completă!\033[0m")
        return True
        
    except Exception as e:
        print(f"\033[91mEroare: {e}\033[0m")
        return False


def demo_senzori_udp():
    """Demonstrație Protocol Senzor UDP."""
    print_titlu("DEMO 3: PROTOCOL SENZOR UDP")
    
    print("Protocolul UDP Senzor simulează dispozitive IoT care trimit citiri.")
    print("Fiecare datagramă are fix 23 octeți cu validare CRC32.\n")
    
    util_retea = UtilitareRetea()
    
    print_pas(1, "Construire datagrame senzor")
    
    senzori = [
        (1, 22.5, "Laborator1"),
        (2, 24.0, "Laborator2"),
        (3, 21.0, "Hol     "),
    ]
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        for sensor_id, temp, locatie in senzori:
            print(f"\n    Senzor {sensor_id}:")
            print(f"      Temperatură: {temp}°C")
            print(f"      Locație:     {locatie.strip()}")
            
            # Construiește datagrama (23 octeți)
            versiune = 1
            locatie_bytes = locatie.encode()[:10].ljust(10, b'\x00')
            rezervat = b'\x00\x00'
            
            # Împachetare fără CRC
            date_fara_crc = struct.pack('!BHf', versiune, sensor_id, temp) + locatie_bytes
            crc = binascii.crc32(date_fara_crc) & 0xFFFFFFFF
            
            # Datagramă completă
            datagrama = date_fara_crc + struct.pack('!I', crc) + rezervat
            
            print(f"      CRC32:       0x{crc:08X}")
            print(f"      Dimensiune:  {len(datagrama)} octeți")
            
            print_trimis(f"{datagrama.hex()}")
            sock.sendto(datagrama, ('localhost', 5402))
            
            time.sleep(0.5)
        
        sock.close()
        print("\n\033[92m✓ Demonstrația Senzor UDP completă!\033[0m")
        print_info("Verificați serverul UDP pentru citirile primite")
        return True
        
    except Exception as e:
        print(f"\033[91mEroare: {e}\033[0m")
        return False


def demo_detectare_erori():
    """Demonstrație Detectare Erori CRC32."""
    print_titlu("DEMO 4: DETECTARE ERORI CRC32")
    
    print("CRC32 detectează coruperea datelor în transmisie.")
    print("Vom demonstra cum o singură modificare de bit schimbă CRC-ul.\n")
    
    # Date originale
    date_originale = b"Mesaj de test pentru verificare CRC32"
    crc_original = binascii.crc32(date_originale) & 0xFFFFFFFF
    
    print_pas(1, "Date originale")
    print(f"    Mesaj:  {date_originale.decode()}")
    print(f"    Hex:    {date_originale[:20].hex()}...")
    print(f"    CRC32:  0x{crc_original:08X}")
    
    print_pas(2, "Simulare corupere (inversare 1 bit)")
    date_corupte = bytearray(date_originale)
    pozitie_corupta = 5
    bit_inversat = date_corupte[pozitie_corupta] ^ 0x01
    
    print(f"    Poziție: octetul {pozitie_corupta}")
    print(f"    Original: 0x{date_originale[pozitie_corupta]:02X} ({chr(date_originale[pozitie_corupta])})")
    print(f"    Corupt:   0x{bit_inversat:02X} ({chr(bit_inversat)})")
    
    date_corupte[pozitie_corupta] = bit_inversat
    crc_corupt = binascii.crc32(bytes(date_corupte)) & 0xFFFFFFFF
    
    print_pas(3, "Verificare CRC")
    print(f"    CRC original: 0x{crc_original:08X}")
    print(f"    CRC corupt:   0x{crc_corupt:08X}")
    
    if crc_original != crc_corupt:
        print("\n    \033[92m✓ CORUPERE DETECTATĂ!\033[0m")
        print_info("CRC-urile nu se potrivesc, datele sunt corupte")
    else:
        print("\n    \033[91m✗ Corupere nedetectată (foarte rar)\033[0m")
    
    print_pas(4, "Statistici CRC32")
    print_info("Detectează 100% din erorile de 1 bit")
    print_info("Detectează 100% din erorile de rafală ≤ 32 biți")
    print_info("Detectează 99.99999995% din erorile aleatorii")
    print_info("NU oferă securitate criptografică!")
    
    print("\n\033[92m✓ Demonstrația Detectare Erori completă!\033[0m")
    return True


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrații Laborator Săptămâna 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Demonstrații disponibile:
  1 - Protocol TEXT (TCP, mesaje text cu prefix lungime)
  2 - Protocol BINAR (TCP, anteturi fixe cu CRC32)
  3 - Senzori UDP (datagrame fixe IoT)
  4 - Detectare Erori CRC32

Exemple:
  python scripts/run_demo.py --demo 1    # Rulează demo TEXT
  python scripts/run_demo.py --demo 2    # Rulează demo BINAR
  python scripts/run_demo.py --all       # Rulează toate demonstrațiile
        """
    )
    parser.add_argument("--demo", "-d", type=int, choices=[1, 2, 3, 4],
                        help="Numărul demonstrației de rulat")
    parser.add_argument("--all", "-a", action="store_true",
                        help="Rulează toate demonstrațiile")
    
    args = parser.parse_args()
    
    if not args.demo and not args.all:
        parser.print_help()
        return 0
    
    print("\n" + "=" * 60)
    print("  DEMONSTRAȚII LABORATOR SĂPTĂMÂNA 4")
    print("  Protocoale Personalizate TEXT, BINAR și UDP")
    print("=" * 60)
    
    demonstratii = {
        1: ("Protocol TEXT", demo_protocol_text),
        2: ("Protocol BINAR", demo_protocol_binar),
        3: ("Senzori UDP", demo_senzori_udp),
        4: ("Detectare Erori CRC32", demo_detectare_erori)
    }
    
    if args.all:
        for num, (nume, func) in demonstratii.items():
            print(f"\n{'='*60}")
            print(f"  Rulare Demo {num}: {nume}")
            print(f"{'='*60}")
            func()
            if num < 4:
                print("\n  Apăsați Enter pentru demonstrația următoare...")
                try:
                    input()
                except (KeyboardInterrupt, EOFError):
                    print("\n\nÎntrerupt de utilizator.")
                    return 0
    else:
        num = args.demo
        nume, func = demonstratii[num]
        func()
    
    print("\n" + "=" * 60)
    print("  DEMONSTRAȚII FINALIZATE")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
