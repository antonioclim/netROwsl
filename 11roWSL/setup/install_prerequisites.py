#!/usr/bin/env python3
"""
Script de Instalare Cerințe Preliminare
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Ajută la instalarea și configurarea dependențelor necesare pentru laborator.
"""

import subprocess
import sys
import platform
import shutil
from pathlib import Path


def afiseaza_banner():
    """Afișează bannerul de instalare."""
    print("=" * 60)
    print("Instalare Cerințe Preliminare - Săptămâna 11")
    print("Laborator Rețele de Calculatoare — ASE")
    print("=" * 60)
    print()


def verifica_admin():
    """Verifică dacă scriptul rulează cu privilegii de administrator."""
    if platform.system() == "Windows":
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    else:
        import os
        return os.geteuid() == 0


def instaleaza_pachete_python():
    """Instalează pachetele Python necesare."""
    print("\n[1/4] Instalare pachete Python...")
    
    pachete = [
        "requests",
        "pyyaml",
        "dnspython",
        "paramiko",
        "pyftpdlib",
    ]
    
    for pachet in pachete:
        print(f"  Instalare {pachet}...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", pachet, "-q"],
                check=True,
                capture_output=True
            )
            print(f"  ✓ {pachet} instalat cu succes")
        except subprocess.CalledProcessError as e:
            print(f"  ✗ Eroare la instalarea {pachet}: {e}")


def verifica_docker():
    """Verifică și oferă instrucțiuni pentru Docker."""
    print("\n[2/4] Verificare Docker...")
    
    if shutil.which("docker"):
        print("  ✓ Docker este instalat")
        
        # Verifică dacă daemon-ul rulează
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True
        )
        if result.returncode == 0:
            print("  ✓ Daemon-ul Docker rulează")
        else:
            print("  ✗ Daemon-ul Docker nu rulează")
            print("  → Porniți Docker Desktop din meniul Start")
    else:
        print("  ✗ Docker nu este instalat")
        print()
        print("  Pentru a instala Docker Desktop:")
        print("  1. Accesați https://www.docker.com/products/docker-desktop")
        print("  2. Descărcați Docker Desktop pentru Windows")
        print("  3. Rulați programul de instalare")
        print("  4. Reporniți calculatorul dacă vi se cere")
        print("  5. Porniți Docker Desktop și așteptați inițializarea")


def verifica_wsl():
    """Verifică și oferă instrucțiuni pentru WSL2."""
    print("\n[3/4] Verificare WSL2...")
    
    if platform.system() != "Windows":
        print("  ℹ Nu sunteți pe Windows - WSL2 nu este necesar")
        return
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = result.stdout.decode() + result.stderr.decode()
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("  ✓ WSL2 este configurat corect")
        else:
            print("  ✗ WSL2 nu este configurat")
            afiseaza_instructiuni_wsl()
    except FileNotFoundError:
        print("  ✗ WSL nu este instalat")
        afiseaza_instructiuni_wsl()


def afiseaza_instructiuni_wsl():
    """Afișează instrucțiuni pentru instalarea WSL2."""
    print()
    print("  Pentru a instala WSL2:")
    print("  1. Deschideți PowerShell ca Administrator")
    print("  2. Rulați: wsl --install")
    print("  3. Reporniți calculatorul")
    print("  4. Configurați utilizatorul Ubuntu la prima pornire")


def verifica_wireshark():
    """Verifică și oferă instrucțiuni pentru Wireshark."""
    print("\n[4/4] Verificare Wireshark...")
    
    cale_windows = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    
    if cale_windows.exists() or shutil.which("wireshark") or shutil.which("tshark"):
        print("  ✓ Wireshark este instalat")
    else:
        print("  ✗ Wireshark nu este instalat")
        print()
        print("  Pentru a instala Wireshark:")
        print("  1. Accesați https://www.wireshark.org/download.html")
        print("  2. Descărcați versiunea pentru Windows (64-bit)")
        print("  3. Rulați programul de instalare")
        print("  4. Selectați 'Install Npcap' în timpul instalării")


def creeaza_structura_directoare():
    """Creează structura de directoare necesară."""
    print("\nCreare structură directoare...")
    
    directoare = [
        "artifacts",
        "pcap",
        "docker/volumes",
        "homework/solutions",
    ]
    
    cale_radacina = Path(__file__).parent.parent
    
    for director in directoare:
        cale = cale_radacina / director
        cale.mkdir(parents=True, exist_ok=True)
        
        # Creează .gitkeep dacă directorul este gol
        gitkeep = cale / ".gitkeep"
        if not gitkeep.exists():
            gitkeep.touch()
    
    print("  ✓ Structura directoarelor a fost creată")


def main():
    """Funcția principală de instalare."""
    afiseaza_banner()
    
    # Avertisment pentru drepturi de administrator
    if platform.system() == "Windows" and not verifica_admin():
        print("⚠ ATENȚIE: Unele operațiuni pot necesita privilegii de Administrator.")
        print("  Dacă întâmpinați probleme, rulați PowerShell ca Administrator.")
        print()
    
    # Rulează pașii de instalare
    instaleaza_pachete_python()
    verifica_docker()
    verifica_wsl()
    verifica_wireshark()
    creeaza_structura_directoare()
    
    # Sumar final
    print()
    print("=" * 60)
    print("Instalare finalizată!")
    print()
    print("Pași următori:")
    print("  1. Asigurați-vă că Docker Desktop rulează")
    print("  2. Rulați: python setup/verify_environment.py")
    print("  3. Dacă toate verificările trec, rulați: python scripts/start_lab.py")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
