#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
import socket
import platform
from pathlib import Path

class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

class Verificator:
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0
    
    def verifica(self, nume, conditie, indicatie=""):
        if conditie:
            print(f"  {Culori.VERDE}[TRECUT]{Culori.FINAL} {nume}")
            self.reusit += 1
        else:
            print(f"  {Culori.ROSU}[EȘUAT]{Culori.FINAL} {nume}")
            if indicatie:
                print(f"         Rezolvare: {indicatie}")
            self.esuat += 1
    
    def avertizeaza(self, nume, mesaj):
        print(f"  {Culori.GALBEN}[ATENȚIE]{Culori.FINAL} {nume}: {mesaj}")
        self.avertismente += 1
    
    def sumar(self):
        print(f"\n{Culori.BOLD}{'=' * 50}{Culori.FINAL}")
        print(f"Rezultate: {self.reusit} trecute, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print(f"\n{Culori.VERDE}✓ Mediul este pregătit!{Culori.FINAL}")
            return 0
        else:
            print(f"\n{Culori.ROSU}✗ Rezolvați problemele de mai sus.{Culori.FINAL}")
            return 1

def verifica_docker_pornit():
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=15)
        return result.returncode == 0
    except:
        return False

def verifica_port_disponibil(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    try:
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result != 0
    except:
        return True

def main():
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Verificarea Mediului - Laboratorul Săptămânii 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    v = Verificator()
    
    print(f"{Culori.BOLD}Mediul Python:{Culori.FINAL}")
    ver = sys.version_info
    v.verifica(f"Python {ver.major}.{ver.minor}.{ver.micro}", ver >= (3, 10), "Instalați Python 3.10+")
    
    print(f"\n{Culori.BOLD}Pachete Python:{Culori.FINAL}")
    for pachet in ["requests", "pyyaml", "docker"]:
        try:
            __import__(pachet.replace('-', '_'))
            v.verifica(f"Pachet: {pachet}", True)
        except ImportError:
            v.verifica(f"Pachet: {pachet}", False, f"pip install {pachet}")
    
    print(f"\n{Culori.BOLD}Mediul Docker:{Culori.FINAL}")
    v.verifica("Docker instalat", shutil.which("docker") is not None, "Instalați Docker Desktop")
    v.verifica("Docker pornit", verifica_docker_pornit(), "Porniți Docker Desktop")
    
    print(f"\n{Culori.BOLD}Disponibilitate Porturi:{Culori.FINAL}")
    porturi = [(8080, "Load Balancer"), (8001, "Backend 1"), (8002, "Backend 2"), (9000, "Echo")]
    for port, serviciu in porturi:
        if verifica_port_disponibil(port):
            v.verifica(f"Port {port} ({serviciu})", True)
        else:
            v.avertizeaza(f"Port {port}", "utilizat")
    
    return v.sumar()

if __name__ == "__main__":
    sys.exit(main())
