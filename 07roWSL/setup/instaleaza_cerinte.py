#!/usr/bin/env python3
"""
Script de Instalare a Cerințelor Preliminare
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Ghid de instalare pentru mediul de laborator.
Notă: Acest script oferă instrucțiuni și verifică statusul,
      dar nu efectuează instalări automate din motive de securitate.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(cmd) is not None


def verifica_docker_pornit() -> bool:
    """Verifică dacă Docker rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def afiseaza_sectiune(titlu: str):
    """Afișează un titlu de secțiune formatat."""
    print()
    print("=" * 60)
    print(f"  {titlu}")
    print("=" * 60)
    print()


def verifica_si_instaleaza_python_packages():
    """Verifică și oferă instrucțiuni pentru pachetele Python."""
    afiseaza_sectiune("Pachete Python Necesare")
    
    pachete = ["PyYAML", "docker", "requests", "colorama"]
    pachete_lipsa = []
    
    for pachet in pachete:
        try:
            __import__(pachet.lower().replace("-", "_"))
            print(f"  [OK] {pachet} este instalat")
        except ImportError:
            print(f"  [LIPSĂ] {pachet}")
            pachete_lipsa.append(pachet)
    
    if pachete_lipsa:
        print()
        print("  Pentru a instala pachetele lipsă, rulați:")
        print(f"    pip install {' '.join(pachete_lipsa)}")
        print()
        print("  Sau instalați toate cerințele din fișier:")
        print("    pip install -r setup/requirements.txt")


def verifica_docker():
    """Verifică și oferă instrucțiuni pentru Docker."""
    afiseaza_sectiune("Docker Desktop")
    
    if not verifica_comanda("docker"):
        print("  [LIPSĂ] Docker nu este instalat")
        print()
        print("  Pași de instalare:")
        print("  1. Vizitați https://www.docker.com/products/docker-desktop")
        print("  2. Descărcați Docker Desktop pentru Windows")
        print("  3. Rulați installerul și urmați instrucțiunile")
        print("  4. Asigurați-vă că selectați 'Use WSL 2 backend'")
        print("  5. Reporniți calculatorul dacă vi se solicită")
        return False
    
    print("  [OK] Docker este instalat")
    
    if not verifica_docker_pornit():
        print("  [ATENȚIE] Docker nu rulează")
        print()
        print("  Pentru a porni Docker:")
        print("  1. Căutați 'Docker Desktop' în meniul Start")
        print("  2. Lansați aplicația")
        print("  3. Așteptați până când pictograma devine stabilă")
        return False
    
    print("  [OK] Docker rulează")
    return True


def verifica_wsl2():
    """Verifică și oferă instrucțiuni pentru WSL2."""
    afiseaza_sectiune("Windows Subsystem for Linux 2 (WSL2)")
    
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        iesire = rezultat.stdout.decode() + rezultat.stderr.decode()
        
        if "WSL 2" in iesire or "Default Version: 2" in iesire:
            print("  [OK] WSL2 este activat și configurat")
            return True
        else:
            print("  [ATENȚIE] WSL2 nu este versiunea implicită")
    except Exception:
        print("  [LIPSĂ] WSL nu este disponibil")
    
    print()
    print("  Pentru a activa WSL2:")
    print("  1. Deschideți PowerShell ca Administrator")
    print("  2. Rulați: wsl --install")
    print("  3. Reporniți calculatorul")
    print("  4. Rulați: wsl --set-default-version 2")
    return False


def verifica_wireshark():
    """Verifică și oferă instrucțiuni pentru Wireshark."""
    afiseaza_sectiune("Wireshark")
    
    cai_wireshark = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    gasit = any(cale.exists() for cale in cai_wireshark) or verifica_comanda("wireshark")
    
    if gasit:
        print("  [OK] Wireshark este instalat")
        return True
    
    print("  [LIPSĂ] Wireshark nu este instalat")
    print()
    print("  Pași de instalare:")
    print("  1. Vizitați https://www.wireshark.org/download.html")
    print("  2. Descărcați versiunea pentru Windows (64-bit)")
    print("  3. Rulați installerul")
    print("  4. În timpul instalării, selectați 'Install Npcap'")
    print("  5. Opțional: instalați și Wireshark command-line tools (tshark)")
    return False


def main():
    """Funcția principală - ghid de instalare."""
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   Asistent Instalare Cerințe - Săptămâna 7               ║")
    print("║   Curs REȚELE DE CALCULATOARE - ASE, Informatică         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    # Verificare Python
    afiseaza_sectiune("Verificare Python")
    versiune = sys.version_info
    if versiune >= (3, 11):
        print(f"  [OK] Python {versiune.major}.{versiune.minor}.{versiune.micro}")
    else:
        print(f"  [ATENȚIE] Python {versiune.major}.{versiune.minor}.{versiune.micro}")
        print("           Se recomandă Python 3.11 sau mai recent")
        print("           Descărcați de la https://www.python.org/downloads/")
    
    # Verificare componente
    wsl_ok = verifica_wsl2()
    docker_ok = verifica_docker()
    wireshark_ok = verifica_wireshark()
    verifica_si_instaleaza_python_packages()
    
    # Sumar
    afiseaza_sectiune("Sumar")
    
    componente = [
        ("WSL2", wsl_ok),
        ("Docker", docker_ok),
        ("Wireshark", wireshark_ok),
    ]
    
    toate_ok = all(ok for _, ok in componente)
    
    for nume, ok in componente:
        status = "[OK]" if ok else "[NECESITĂ ATENȚIE]"
        print(f"  {status} {nume}")
    
    print()
    if toate_ok:
        print("  Toate componentele principale sunt instalate!")
        print("  Rulați 'python setup/verifica_mediu.py' pentru verificare completă.")
    else:
        print("  Unele componente necesită atenție.")
        print("  Urmați instrucțiunile de mai sus pentru fiecare componentă.")
    
    print()
    return 0 if toate_ok else 1


if __name__ == "__main__":
    sys.exit(main())
