#!/usr/bin/env python3
"""
Ajutor pentru instalarea cerințelor preliminare
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Asistă la instalarea software-ului necesar pentru laboratorul Săptămânii 6.
"""

from __future__ import annotations

import subprocess
import sys
import platform
from pathlib import Path


def afiseaza_sectiune(titlu: str) -> None:
    """Afișează un antet de secțiune."""
    print()
    print("=" * 60)
    print(f"  {titlu}")
    print("=" * 60)
    print()


def ruleaza_comanda(cmd: list[str], verifica: bool = True) -> bool:
    """Rulează o comandă și returnează starea de succes."""
    try:
        rezultat = subprocess.run(cmd, check=verifica)
        return rezultat.returncode == 0
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False


def instaleaza_pachete_python() -> bool:
    """Instalează pachetele Python necesare."""
    print("Instalarea pachetelor Python...")
    
    pachete = [
        "docker",
        "requests",
        "pyyaml",
    ]
    
    cmd = [sys.executable, "-m", "pip", "install", "--break-system-packages"] + pachete
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Pachetele Python au fost instalate cu succes")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Eșec la instalarea pachetelor Python: {e}")
        return False


def verifica_instalare_docker() -> bool:
    """Verifică dacă Docker este instalat și oferă îndrumare."""
    try:
        rezultat = subprocess.run(["docker", "--version"], capture_output=True)
        if rezultat.returncode == 0:
            print("✓ Docker este deja instalat")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ Docker nu este instalat")
    print()
    print("Pentru a instala Docker Desktop:")
    print("  1. Descarcă de la: https://www.docker.com/products/docker-desktop")
    print("  2. Rulează instalatorul")
    print("  3. Activează integrarea WSL2 în setările Docker Desktop")
    print()
    return False


def verifica_wsl2() -> bool:
    """Verifică disponibilitatea WSL2 pe Windows."""
    if platform.system() != "Windows":
        return True  # Nu se aplică
    
    try:
        rezultat = subprocess.run(["wsl", "--status"], capture_output=True, text=True)
        if "WSL 2" in rezultat.stdout or "Default Version: 2" in rezultat.stdout:
            print("✓ WSL2 este disponibil")
            return True
    except FileNotFoundError:
        pass
    
    print("✗ WSL2 nu este disponibil sau nu este implicit")
    print()
    print("Pentru a activa WSL2:")
    print("  1. Deschide PowerShell ca Administrator")
    print("  2. Rulează: wsl --install")
    print("  3. Repornește calculatorul")
    print("  4. Rulează: wsl --set-default-version 2")
    print()
    return False


def ofera_instructiuni_wsl() -> None:
    """Oferă instrucțiuni pentru instrumentele specifice WSL."""
    afiseaza_sectiune("Instrumente WSL/Linux (Opțional)")
    
    print("Următoarele instrumente oferă funcționalitate suplimentară în WSL/Linux:")
    print()
    print("Instalează în WSL Ubuntu:")
    print("  sudo apt-get update")
    print("  sudo apt-get install -y mininet openvswitch-switch tcpdump tshark")
    print("  pip3 install --break-system-packages os-ken scapy")
    print()
    print("Acestea sunt opționale dacă folosești containere Docker.")


def main() -> int:
    """Punct de intrare principal."""
    afiseaza_sectiune("Instalarea cerințelor preliminare Săptămâna 6")
    print("Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    
    succes = True
    
    # Verifică WSL2 (doar Windows)
    if platform.system() == "Windows":
        afiseaza_sectiune("Configurare WSL2")
        if not verifica_wsl2():
            succes = False
    
    # Verifică Docker
    afiseaza_sectiune("Instalare Docker")
    if not verifica_instalare_docker():
        succes = False
    
    # Instalează pachete Python
    afiseaza_sectiune("Pachete Python")
    if not instaleaza_pachete_python():
        succes = False
    
    # Oferă instrucțiuni WSL
    ofera_instructiuni_wsl()
    
    # Sumar
    afiseaza_sectiune("Sumar")
    
    if succes:
        print("✓ Cerințele preliminare de bază sunt pregătite!")
        print()
        print("Pași următori:")
        print("  1. Pornește Docker Desktop")
        print("  2. Rulează: python setup/verify_environment.py")
        print("  3. Rulează: python scripts/start_lab.py")
    else:
        print("✗ Unele cerințe preliminare necesită atenție")
        print()
        print("Te rugăm să rezolvi problemele de mai sus și să rulezi acest script din nou.")
    
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
