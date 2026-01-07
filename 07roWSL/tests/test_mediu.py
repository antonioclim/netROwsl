#!/usr/bin/env python3
"""
Teste de Mediu pentru Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică că toate componentele necesare sunt instalate și funcționale.
"""

from __future__ import annotations

import subprocess
import sys
import socket
import shutil
from pathlib import Path
from datetime import datetime


class RezultatTest:
    """Clasă pentru stocarea rezultatelor testelor."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.sarit = 0
        self.rezultate: list[tuple[str, str, str]] = []
    
    def adauga(self, nume: str, status: str, detalii: str = ""):
        """Adaugă un rezultat de test."""
        self.rezultate.append((nume, status, detalii))
        
        if status == "REUȘIT":
            self.reusit += 1
        elif status == "EȘUAT":
            self.esuat += 1
        else:
            self.sarit += 1
    
    def afiseaza(self):
        """Afișează rezultatele."""
        print()
        print("=" * 60)
        print("REZULTATE TESTE MEDIU")
        print("=" * 60)
        print()
        
        for nume, status, detalii in self.rezultate:
            if status == "REUȘIT":
                simbol = "✓"
            elif status == "EȘUAT":
                simbol = "✗"
            else:
                simbol = "○"
            
            print(f"  [{simbol}] {nume}: {status}")
            if detalii:
                print(f"      {detalii}")
        
        print()
        print("-" * 60)
        print(f"Total: {self.reusit} reușit(e), {self.esuat} eșuat(e), {self.sarit} sărit(e)")
        print("=" * 60)
        
        return self.esuat == 0


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(cmd) is not None


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Verifică dacă un port este accesibil."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        rezultat = sock.connect_ex((host, port))
        sock.close()
        return rezultat == 0
    except Exception:
        return False


def ruleaza_teste():
    """Rulează toate testele de mediu."""
    rezultate = RezultatTest()
    
    print("Testare Mediu - Săptămâna 7")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print()
    print("Rulare teste...")
    print()
    
    # Test 1: Versiune Python
    versiune = sys.version_info
    if versiune >= (3, 11):
        rezultate.adauga(
            "Versiune Python",
            "REUȘIT",
            f"Python {versiune.major}.{versiune.minor}.{versiune.micro}"
        )
    else:
        rezultate.adauga(
            "Versiune Python",
            "EȘUAT",
            f"Python {versiune.major}.{versiune.minor} (necesită 3.11+)"
        )
    
    # Test 2: Docker instalat
    if verifica_comanda("docker"):
        rezultate.adauga("Docker instalat", "REUȘIT")
    else:
        rezultate.adauga("Docker instalat", "EȘUAT", "docker nu este în PATH")
    
    # Test 3: Docker rulează
    try:
        proc = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if proc.returncode == 0:
            rezultate.adauga("Docker daemon", "REUȘIT", "Daemon-ul rulează")
        else:
            rezultate.adauga("Docker daemon", "EȘUAT", "Docker nu răspunde")
    except Exception as e:
        rezultate.adauga("Docker daemon", "EȘUAT", str(e))
    
    # Test 4: Docker Compose
    try:
        proc = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        if proc.returncode == 0:
            rezultate.adauga("Docker Compose", "REUȘIT")
        else:
            rezultate.adauga("Docker Compose", "EȘUAT")
    except Exception:
        rezultate.adauga("Docker Compose", "EȘUAT", "Comandă indisponibilă")
    
    # Test 5: Pachete Python
    pachete = ["yaml", "requests"]
    for pachet in pachete:
        try:
            __import__(pachet)
            rezultate.adauga(f"Pachet Python: {pachet}", "REUȘIT")
        except ImportError:
            rezultate.adauga(f"Pachet Python: {pachet}", "EȘUAT", "Nu este instalat")
    
    # Test 6: Port TCP 9090
    if verifica_port("localhost", 9090):
        rezultate.adauga("Server TCP (port 9090)", "REUȘIT", "Serverul răspunde")
    else:
        rezultate.adauga(
            "Server TCP (port 9090)",
            "SĂRIT",
            "Serverul nu rulează (porniți cu scripts/porneste_lab.py)"
        )
    
    # Test 7: Port UDP 9091 (doar verificăm că putem crea socket)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"test", ("localhost", 9091))
        sock.close()
        rezultate.adauga("Socket UDP (port 9091)", "REUȘIT", "Socket funcțional")
    except Exception as e:
        rezultate.adauga("Socket UDP (port 9091)", "EȘUAT", str(e))
    
    # Afișare rezultate
    return rezultate.afiseaza()


def main():
    """Funcția principală."""
    succes = ruleaza_teste()
    sys.exit(0 if succes else 1)


if __name__ == "__main__":
    main()
