#!/usr/bin/env python3
"""
Test de Fum (Smoke Test)
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Verificare rapidă a funcționalității de bază a mediului de laborator.
Rulează verificări minime pentru a confirma că totul este pregătit.
"""

import sys
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class Culori:
    VERDE = "\033[92m"
    ROSU = "\033[91m"
    GALBEN = "\033[93m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


# Dezactivează culorile dacă nu este TTY
try:
    if not sys.stdout.isatty():
        Culori.VERDE = Culori.ROSU = Culori.GALBEN = Culori.RESET = Culori.BOLD = ""
except Exception:
    pass


class TestFum:
    """Clasă pentru testele de fum."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.sarite = 0
    
    def verifica(self, nume: str, conditie: bool, motiv_sarire: str = None):
        """Verifică o condiție și înregistrează rezultatul."""
        if motiv_sarire:
            print(f"  [{Culori.GALBEN}SĂRIT{Culori.RESET}]   {nume}")
            print(f"            Motiv: {motiv_sarire}")
            self.sarite += 1
        elif conditie:
            print(f"  [{Culori.VERDE}TRECUT{Culori.RESET}]  {nume}")
            self.trecute += 1
        else:
            print(f"  [{Culori.ROSU}EȘUAT{Culori.RESET}]   {nume}")
            self.esuate += 1
    
    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        total = self.trecute + self.esuate + self.sarite
        print("\n" + "=" * 50)
        print(f"{Culori.BOLD}SUMAR TEST DE FUM{Culori.RESET}")
        print("=" * 50)
        print(f"Total:   {total}")
        print(f"  {Culori.VERDE}Trecute:{Culori.RESET}  {self.trecute}")
        print(f"  {Culori.ROSU}Eșuate:{Culori.RESET}   {self.esuate}")
        print(f"  {Culori.GALBEN}Sărite:{Culori.RESET}   {self.sarite}")
        print("=" * 50)
        
        if self.esuate == 0:
            print(f"\n{Culori.VERDE}✓ Toate testele au trecut!{Culori.RESET}")
            return 0
        else:
            print(f"\n{Culori.ROSU}✗ Unele teste au eșuat!{Culori.RESET}")
            return 1


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Verifică dacă un port este deschis."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            return sock.connect_ex((host, port)) == 0
    except Exception:
        return False


def main():
    """Funcția principală."""
    print("=" * 50)
    print(f"{Culori.BOLD}TEST DE FUM - LABORATOR SĂPTĂMÂNA 13{Culori.RESET}")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 50)
    print()
    
    test = TestFum()
    
    # Test 1: Versiune Python
    print(f"{Culori.BOLD}Mediul Python:{Culori.RESET}")
    versiune = sys.version_info
    test.verifica(
        f"Python {versiune.major}.{versiune.minor}+ instalat",
        versiune >= (3, 11)
    )
    
    # Test 2: Pachete Python necesare
    print(f"\n{Culori.BOLD}Pachete Python:{Culori.RESET}")
    
    pachete = [
        ("paho.mqtt.client", "paho-mqtt"),
        ("scapy.all", "scapy"),
        ("requests", "requests"),
        ("yaml", "pyyaml"),
    ]
    
    for modul, nume_pachet in pachete:
        try:
            __import__(modul.split('.')[0])
            test.verifica(f"Pachet {nume_pachet}", True)
        except ImportError:
            test.verifica(f"Pachet {nume_pachet}", False)
    
    # Test 3: Structura proiectului
    print(f"\n{Culori.BOLD}Structura Proiectului:{Culori.RESET}")
    
    fisiere_necesare = [
        "README.md",
        "docker/docker-compose.yml",
        "src/exercises/ex_13_01_scanner_porturi.py",
        "src/exercises/ex_13_02_client_mqtt.py",
        "scripts/porneste_lab.py",
    ]
    
    for fisier in fisiere_necesare:
        cale = RADACINA_PROIECT / fisier
        test.verifica(f"Fișier {fisier}", cale.exists())
    
    # Test 4: Servicii Docker (dacă sunt pornite)
    print(f"\n{Culori.BOLD}Servicii Docker:{Culori.RESET}")
    
    servicii = [
        ("MQTT (text clar)", 1883),
        ("MQTT (TLS)", 8883),
        ("DVWA", 8080),
        ("FTP", 2121),
        ("Backdoor simulat", 6200),
    ]
    
    pentru_docker = 0
    for nume, port in servicii:
        deschis = verifica_port("localhost", port)
        if deschis:
            test.verifica(f"{nume} pe portul {port}", True)
            pentru_docker += 1
        else:
            test.verifica(
                f"{nume} pe portul {port}",
                False,
                "Serviciul nu rulează (rulați scripts/porneste_lab.py)" if pentru_docker == 0 else None
            )
    
    return test.sumar()


if __name__ == "__main__":
    sys.exit(main())
