#!/usr/bin/env python3
"""
Test de Fum (Smoke Test) - Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică rapid că mediul de laborator funcționează corect.
"""

import subprocess
import sys
import socket
import time
from pathlib import Path
from typing import List, Tuple

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))


class TestFum:
    """Executor de teste de fum pentru verificarea rapidă a mediului."""
    
    def __init__(self):
        self.rezultate: List[Tuple[str, bool, str]] = []
    
    def adaugă_rezultat(self, nume: str, succes: bool, detalii: str = "") -> None:
        """Adaugă un rezultat de test."""
        self.rezultate.append((nume, succes, detalii))
    
    def verifică_python(self) -> None:
        """Verifică versiunea Python."""
        versiune = sys.version_info
        succes = versiune >= (3, 11)
        detalii = f"Python {versiune.major}.{versiune.minor}.{versiune.micro}"
        self.adaugă_rezultat("Versiune Python >= 3.11", succes, detalii)
    
    def verifică_docker(self) -> None:
        """Verifică disponibilitatea Docker."""
        try:
            rezultat = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            succes = rezultat.returncode == 0
            detalii = "Docker disponibil și rulează" if succes else "Docker indisponibil"
        except FileNotFoundError:
            succes = False
            detalii = "Docker nu este instalat"
        except subprocess.TimeoutExpired:
            succes = False
            detalii = "Timeout la verificare Docker"
        
        self.adaugă_rezultat("Docker disponibil", succes, detalii)
    
    def verifică_container_lab(self) -> None:
        """Verifică dacă containerul week2_lab rulează."""
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", "week2_lab"],
                capture_output=True,
                text=True,
                timeout=5
            )
            succes = rezultat.stdout.strip().lower() == "true"
            detalii = "Container activ" if succes else "Container inactiv"
        except Exception as e:
            succes = False
            detalii = f"Eroare: {e}"
        
        self.adaugă_rezultat("Container week2_lab", succes, detalii)
    
    def verifică_port_tcp(self, port: int = 9090) -> None:
        """Verifică disponibilitatea portului TCP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                rezultat = sock.connect_ex(("localhost", port))
                succes = rezultat == 0
                detalii = f"Port {port} accesibil" if succes else f"Port {port} închis"
        except Exception as e:
            succes = False
            detalii = f"Eroare: {e}"
        
        self.adaugă_rezultat(f"Port TCP {port}", succes, detalii)
    
    def verifică_port_udp(self, port: int = 9091) -> None:
        """Verifică răspunsul pe portul UDP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(b"ping", ("localhost", port))
                răspuns, _ = sock.recvfrom(1024)
                succes = răspuns.decode().strip() == "PONG"
                detalii = f"Port {port} răspunde: {răspuns.decode().strip()}"
        except socket.timeout:
            succes = False
            detalii = f"Port {port} - timeout (serverul poate să nu ruleze)"
        except Exception as e:
            succes = False
            detalii = f"Eroare: {e}"
        
        self.adaugă_rezultat(f"Port UDP {port}", succes, detalii)
    
    def verifică_structură_proiect(self) -> None:
        """Verifică structura directorului proiectului."""
        directoare_necesare = [
            "setup", "docker", "scripts", "src/exercises",
            "tests", "docs", "homework", "pcap"
        ]
        
        lipsă = []
        for director in directoare_necesare:
            cale = RĂDĂCINĂ_PROIECT / director
            if not cale.exists():
                lipsă.append(director)
        
        succes = len(lipsă) == 0
        if succes:
            detalii = "Toate directoarele prezente"
        else:
            detalii = f"Directoare lipsă: {', '.join(lipsă)}"
        
        self.adaugă_rezultat("Structură proiect", succes, detalii)
    
    def verifică_pachete_python(self) -> None:
        """Verifică pachetele Python necesare."""
        pachete = ["socket", "threading", "argparse", "dataclasses"]
        lipsă = []
        
        for pachet in pachete:
            try:
                __import__(pachet)
            except ImportError:
                lipsă.append(pachet)
        
        succes = len(lipsă) == 0
        detalii = "Toate pachetele disponibile" if succes else f"Lipsă: {', '.join(lipsă)}"
        self.adaugă_rezultat("Pachete Python", succes, detalii)
    
    def afișează_rezultate(self) -> int:
        """
        Afișează rezultatele testelor.
        
        Returns:
            0 dacă toate testele au trecut, 1 altfel
        """
        print()
        print("=" * 60)
        print("Rezultate Test de Fum - Săptămâna 2")
        print("=" * 60)
        print()
        
        reușite = 0
        eșuate = 0
        
        for nume, succes, detalii in self.rezultate:
            simbol = "✓" if succes else "✗"
            culoare = "\033[92m" if succes else "\033[91m"
            resetare = "\033[0m"
            
            print(f"  {culoare}{simbol}{resetare} {nume}")
            if detalii:
                print(f"      {detalii}")
            
            if succes:
                reușite += 1
            else:
                eșuate += 1
        
        print()
        print("-" * 60)
        print(f"Total: {reușite} reușite, {eșuate} eșuate")
        
        if eșuate == 0:
            print("\n✓ Mediul de laborator este pregătit!")
            return 0
        else:
            print("\n✗ Unele verificări au eșuat. Consultați instrucțiunile de mai sus.")
            return 1
    
    def rulează_toate(self) -> int:
        """
        Rulează toate testele de fum.
        
        Returns:
            Cod de ieșire
        """
        print("Rulare teste de fum...")
        print()
        
        self.verifică_python()
        self.verifică_pachete_python()
        self.verifică_structură_proiect()
        self.verifică_docker()
        self.verifică_container_lab()
        
        # Testele de port sunt opționale (depind de servere)
        # self.verifică_port_tcp(9090)
        # self.verifică_port_udp(9091)
        
        return self.afișează_rezultate()


def main() -> int:
    """Funcția principală."""
    test = TestFum()
    return test.rulează_toate()


if __name__ == "__main__":
    sys.exit(main())
