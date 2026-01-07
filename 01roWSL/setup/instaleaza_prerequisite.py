#!/usr/bin/env python3
"""
Asistent de Instalare a Cerințelor Preliminare
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Oferă îndrumări pentru instalarea componentelor lipsă.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path
from typing import List, Optional


def afiseaza_sectiune(titlu: str) -> None:
    """Afișează un titlu de secțiune formatat."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60 + "\n")


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(cmd) is not None


def ruleaza_comanda(cmd: List[str], descriere: str) -> bool:
    """Rulează o comandă și afișează rezultatul."""
    print(f"Se execută: {descriere}")
    print(f"  Comandă: {' '.join(cmd)}")
    
    try:
        rezultat = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if rezultat.returncode == 0:
            print("  ✓ Succes!")
            return True
        else:
            print(f"  ✗ Eșuat: {rezultat.stderr}")
            return False
    except Exception as e:
        print(f"  ✗ Eroare: {e}")
        return False


def instaleaza_pachete_python() -> None:
    """Instalează pachetele Python necesare."""
    afiseaza_sectiune("Instalarea Pachetelor Python")
    
    pachete = [
        "docker",
        "requests",
        "pyyaml",
        "scapy",
        "dpkt",
    ]
    
    print("Se vor instala următoarele pachete:")
    for pachet in pachete:
        print(f"  • {pachet}")
    
    raspuns = input("\nContinuați cu instalarea? (d/n): ").strip().lower()
    if raspuns != "d":
        print("Instalare anulată.")
        return
    
    for pachet in pachete:
        ruleaza_comanda(
            [sys.executable, "-m", "pip", "install", pachet, "--break-system-packages"],
            f"Instalare {pachet}"
        )


def afiseaza_ghid_docker() -> None:
    """Afișează ghidul de instalare Docker Desktop."""
    afiseaza_sectiune("Ghid de Instalare Docker Desktop")
    
    print("""
Docker Desktop este necesar pentru rularea containerelor de laborator.

PAȘI DE INSTALARE:

1. Descărcați Docker Desktop:
   • Accesați: https://www.docker.com/products/docker-desktop/
   • Selectați versiunea pentru Windows

2. Rulați instalatorul:
   • Executați fișierul descărcat
   • Acceptați termenii licenței
   • Selectați "Use WSL 2 instead of Hyper-V" (recomandat)

3. Configurare după instalare:
   • Reporniți calculatorul dacă vi se solicită
   • Lansați Docker Desktop
   • Așteptați ca Docker să pornească (pictograma devine verde)

4. Verificați instalarea:
   • Deschideți PowerShell
   • Rulați: docker --version
   • Rulați: docker run hello-world

NOTĂ: La prima pornire, Docker poate solicita configurarea WSL2.
      Urmați instrucțiunile afișate pentru a finaliza configurarea.
""")


def afiseaza_ghid_wsl2() -> None:
    """Afișează ghidul de instalare WSL2."""
    afiseaza_sectiune("Ghid de Instalare WSL2")
    
    print("""
WSL2 (Windows Subsystem for Linux 2) este necesar pentru Docker Desktop.

PAȘI DE INSTALARE:

1. Deschideți PowerShell ca Administrator

2. Instalați WSL2:
   wsl --install

3. Reporniți calculatorul

4. După repornire, verificați instalarea:
   wsl --status

5. Setați WSL2 ca versiune implicită (dacă nu este deja):
   wsl --set-default-version 2

NOTĂ: Windows 10 versiunea 2004 sau mai recentă este necesară.
      Pentru versiuni mai vechi, consultați documentația Microsoft.
""")


def afiseaza_ghid_wireshark() -> None:
    """Afișează ghidul de instalare Wireshark."""
    afiseaza_sectiune("Ghid de Instalare Wireshark")
    
    print("""
Wireshark este analizorul de protocoale de rețea necesar pentru laborator.

PAȘI DE INSTALARE:

1. Descărcați Wireshark:
   • Accesați: https://www.wireshark.org/download.html
   • Selectați "Windows x64 Installer"

2. Rulați instalatorul:
   • Executați fișierul descărcat
   • Acceptați termenii licenței
   • Selectați componentele (lăsați selecțiile implicite)
   • IMPORTANT: Instalați Npcap când vi se solicită

3. Configurare Npcap:
   • În timpul instalării Npcap, selectați:
     ☑ Support raw 802.11 traffic
     ☑ Install Npcap in WinPcap API-compatible mode

4. Verificați instalarea:
   • Lansați Wireshark din meniul Start
   • Ar trebui să vedeți o listă de interfețe de rețea

NOTĂ: Pentru captura de trafic Docker, selectați interfața corespunzătoare.
""")


def afiseaza_ghid_python() -> None:
    """Afișează ghidul de instalare Python."""
    afiseaza_sectiune("Ghid de Instalare Python")
    
    print("""
Python 3.11 sau mai recent este necesar pentru scripturile de laborator.

PAȘI DE INSTALARE:

1. Descărcați Python:
   • Accesați: https://www.python.org/downloads/
   • Selectați versiunea 3.11 sau mai recentă

2. Rulați instalatorul:
   • IMPORTANT: Bifați "Add Python to PATH" la început
   • Selectați "Install Now" sau "Customize installation"

3. Verificați instalarea:
   • Deschideți PowerShell
   • Rulați: python --version
   • Ar trebui să vedeți "Python 3.11.x" sau mai recent

4. Verificați pip:
   • Rulați: pip --version

NOTĂ: Dacă aveți mai multe versiuni de Python, folosiți "py -3.11" 
      pentru a specifica versiunea dorită.
""")


def meniu_principal() -> None:
    """Afișează meniul principal și gestionează interacțiunea."""
    while True:
        afiseaza_sectiune("Asistent de Instalare - Meniu Principal")
        
        print("Selectați o opțiune:\n")
        print("  1. Instalează pachetele Python necesare")
        print("  2. Ghid instalare Docker Desktop")
        print("  3. Ghid instalare WSL2")
        print("  4. Ghid instalare Wireshark")
        print("  5. Ghid instalare Python")
        print("  6. Verifică mediul de lucru")
        print("  0. Ieșire")
        
        alegere = input("\nIntroduceți numărul opțiunii: ").strip()
        
        if alegere == "1":
            instaleaza_pachete_python()
        elif alegere == "2":
            afiseaza_ghid_docker()
        elif alegere == "3":
            afiseaza_ghid_wsl2()
        elif alegere == "4":
            afiseaza_ghid_wireshark()
        elif alegere == "5":
            afiseaza_ghid_python()
        elif alegere == "6":
            print("\nSe rulează verificarea mediului...\n")
            subprocess.run([sys.executable, str(Path(__file__).parent / "verifica_mediu.py")])
        elif alegere == "0":
            print("\nLa revedere!")
            break
        else:
            print("\nOpțiune invalidă. Încercați din nou.")
        
        input("\nApăsați Enter pentru a continua...")


def main() -> int:
    """Funcția principală."""
    print("=" * 60)
    print("  Asistent de Instalare a Cerințelor Preliminare")
    print("  Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    
    meniu_principal()
    return 0


if __name__ == "__main__":
    sys.exit(main())
