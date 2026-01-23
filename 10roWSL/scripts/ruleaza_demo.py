#!/usr/bin/env python3
"""
Script de Demonstrație pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Rulează demonstrații automate ale serviciilor de laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului la calea Python

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.network_utils import TesterRetea

logger = configureaza_logger("demo")



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def pauza(mesaj: str = "Apăsați Enter pentru a continua..."):
    """Afișează un mesaj și așteaptă confirmarea utilizatorului."""
    print()
    input(f"  → {mesaj}")
    print()


def afiseaza_sectiune(titlu: str):
    """Afișează un separator de secțiune."""
    print()
    print("─" * 60)
    print(f"  {titlu}")
    print("─" * 60)
    print()


def demo_http():
    """Demonstrație serviciu HTTP."""
    afiseaza_sectiune("DEMONSTRAȚIE HTTP")
    
    print("  Testăm serverul web HTTP pe portul 8000...")
    print()
    
    # Test cu curl
    print("  1. Cerere HTTP GET către pagina principală:")
    print("  $ curl -v http://localhost:8000/")
    print()
    
    rezultat = subprocess.run(
        ["curl", "-s", "-v", "http://localhost:8000/"],
        capture_output=True,
        text=True
    )
    
    # Afișăm headerele
    for linie in rezultat.stderr.split('\n'):
        if linie.startswith('<') or linie.startswith('>'):
            print(f"     {linie}")
    
    print()
    print("  Răspuns:")
    print("     " + rezultat.stdout[:200].replace('\n', '\n     '))
    
    pauza()
    
    # Test hello.txt
    print("  2. Cerere pentru fișierul hello.txt:")
    print("  $ curl http://localhost:8000/hello.txt")
    print()
    
    rezultat = subprocess.run(
        ["curl", "-s", "http://localhost:8000/hello.txt"],
        capture_output=True,
        text=True
    )
    
    print(f"     {rezultat.stdout}")


def demo_dns():
    """Demonstrație serviciu DNS."""
    afiseaza_sectiune("DEMONSTRAȚIE DNS")
    
    print("  Testăm serverul DNS personalizat pe portul 5353...")
    print()
    
    domenii = [
        ("web.lab.local", "172.20.0.10"),
        ("ssh.lab.local", "172.20.0.22"),
        ("ftp.lab.local", "172.20.0.21"),
        ("myservice.lab.local", "10.10.10.10"),
    ]
    
    tester = TesterRetea()
    
    for domeniu, ip_asteptat in domenii:
        print(f"  Rezolvare {domeniu}:")
        print(f"  $ dig @localhost -p 5353 {domeniu} +short")
        
        succes, mesaj, ip = tester.testeaza_dns(domeniu, "localhost", 5353)
        
        if succes:
            print(f"     → {ip}")
            if ip == ip_asteptat:
                print(f"     ✓ Corect! (așteptat: {ip_asteptat})")
            else:
                print(f"     ⚠ Diferit de așteptări ({ip_asteptat})")
        else:
            print(f"     ✗ {mesaj}")
        
        print()
    
    # Test domeniu inexistent
    print("  Test domeniu inexistent:")
    print("  $ dig @localhost -p 5353 inexistent.lab.local")
    
    rezultat = subprocess.run(
        ["dig", "@localhost", "-p", "5353", "inexistent.lab.local"],
        capture_output=True,
        text=True
    )
    
    if "NXDOMAIN" in rezultat.stdout:
        print("     → NXDOMAIN (domeniu inexistent - corect!)")
    else:
        print("     → Răspuns neașteptat")


def demo_ssh():
    """Demonstrație serviciu SSH."""
    afiseaza_sectiune("DEMONSTRAȚIE SSH")
    
    print("  Testăm conectivitatea SSH pe portul 2222...")
    print()
    
    tester = TesterRetea()
    
    succes, mesaj = tester.testeaza_ssh("localhost", 2222)
    print(f"  {mesaj}")
    print()
    
    print("  Pentru conectare manuală:")
    print("  $ ssh -p 2222 labuser@localhost")
    print("  Parolă: labpass")
    print()
    
    print("  Sau folosiți scriptul Paramiko:")
    print("  $ docker exec -it week10_ssh_client python /app/paramiko_client.py")


def demo_ftp():
    """Demonstrație serviciu FTP."""
    afiseaza_sectiune("DEMONSTRAȚIE FTP")
    
    print("  Testăm serverul FTP pe portul 2121...")
    print()
    
    tester = TesterRetea()
    
    succes, mesaj = tester.testeaza_ftp("localhost", 2121)
    print(f"  {mesaj}")
    print()
    
    print("  Pentru conectare manuală:")
    print("  $ ftp localhost 2121")
    print("  Utilizator: labftp")
    print("  Parolă: labftp")
    print()
    
    print("  Sau din containerul debug cu lftp:")
    print("  $ docker exec -it week10_debug lftp -u labftp,labftp ftp-server:2121")


def demo_complet():
    """Rulează toate demonstrațiile."""
    print()
    print("=" * 60)
    print("  DEMONSTRAȚIE COMPLETĂ - LABORATORUL SĂPTĂMÂNII 10")
    print("  Servicii de Rețea: HTTP, DNS, SSH, FTP")
    print("=" * 60)
    
    demo_http()
    pauza()
    
    demo_dns()
    pauza()
    
    demo_ssh()
    pauza()
    
    demo_ftp()
    
    print()
    print("=" * 60)
    print("  DEMONSTRAȚIE FINALIZATĂ")
    print("=" * 60)



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Rulează demonstrații pentru Laboratorul Săptămânii 10"
    )
    parser.add_argument(
        "--demo",
        type=int,
        choices=[1, 2, 3, 4],
        help="Rulează o demonstrație specifică (1=HTTP, 2=DNS, 3=SSH, 4=FTP)"
    )
    parser.add_argument(
        "--toate",
        action="store_true",
        help="Rulează toate demonstrațiile"
    )
    args = parser.parse_args()

    try:
        if args.demo == 1:
            demo_http()
        elif args.demo == 2:
            demo_dns()
        elif args.demo == 3:
            demo_ssh()
        elif args.demo == 4:
            demo_ftp()
        elif args.toate or not args.demo:
            demo_complet()
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare în demonstrație: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
