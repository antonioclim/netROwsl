#!/usr/bin/env python3
"""
Asistent de Instalare a Cerințelor Preliminare
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Ghid interactiv pentru instalarea componentelor lipsă.
"""

import subprocess
import sys
import shutil
from pathlib import Path

# Coduri ANSI pentru culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
RESETARE = "\033[0m"
BOLD = "\033[1m"


def afiseaza_titlu(titlu: str):
    """Afișează un titlu formatat."""
    print()
    print("=" * 60)
    print(f"{BOLD}{titlu}{RESETARE}")
    print("=" * 60)


def confirma(intrebare: str) -> bool:
    """Solicită confirmarea utilizatorului."""
    while True:
        raspuns = input(f"{intrebare} [d/n]: ").lower().strip()
        if raspuns in ['d', 'da', 'y', 'yes']:
            return True
        elif raspuns in ['n', 'nu', 'no']:
            return False
        print("Vă rugăm răspundeți cu 'd' pentru da sau 'n' pentru nu.")


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(cmd) is not None


def instaleaza_pachete_python():
    """Instalează pachetele Python necesare."""
    afiseaza_titlu("Instalare Pachete Python")
    
    pachete = [
        "docker>=6.0.0",
        "requests>=2.28.0", 
        "pyyaml>=6.0",
        "pytest>=7.0.0"
    ]
    
    print("Următoarele pachete vor fi instalate:")
    for pachet in pachete:
        print(f"  - {pachet}")
    print()
    
    if confirma("Continuați cu instalarea?"):
        for pachet in pachete:
            print(f"\n{ALBASTRU}Instalare {pachet}...{RESETARE}")
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pip", "install", pachet, "--break-system-packages"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    print(f"{VERDE}✓ {pachet} instalat cu succes{RESETARE}")
                else:
                    print(f"{ROSU}✗ Eroare la instalarea {pachet}{RESETARE}")
                    print(result.stderr)
            except Exception as e:
                print(f"{ROSU}✗ Excepție: {e}{RESETARE}")
        
        print(f"\n{VERDE}Instalarea pachetelor Python completă!{RESETARE}")
    else:
        print("Instalare anulată.")


def afiseaza_instructiuni_docker():
    """Afișează instrucțiunile de instalare Docker Desktop."""
    afiseaza_titlu("Instalare Docker Desktop")
    
    print("""
Docker Desktop este necesar pentru a rula containerele de laborator.

{BOLD}Pași de instalare:{RESETARE}

1. Descărcați Docker Desktop de la:
   https://www.docker.com/products/docker-desktop/

2. Rulați installerul și urmați instrucțiunile

3. În timpul instalării, asigurați-vă că opțiunea 
   "Use WSL 2 instead of Hyper-V" este bifată

4. După instalare, reporniți computerul dacă vi se solicită

5. Porniți Docker Desktop din meniul Start

6. La prima pornire, acceptați termenii și condițiile

7. Așteptați ca Docker să se inițializeze (poate dura 1-2 minute)

{BOLD}Verificare:{RESETARE}
Deschideți PowerShell și rulați:
    docker --version
    docker run hello-world

Dacă ambele comenzi funcționează, Docker este instalat corect.
""".format(BOLD=BOLD, RESETARE=RESETARE))


def afiseaza_instructiuni_wsl2():
    """Afișează instrucțiunile de configurare WSL2."""
    afiseaza_titlu("Configurare WSL2")
    
    print("""
WSL2 (Windows Subsystem for Linux 2) este necesar pentru Docker Desktop.

{BOLD}Pași de configurare:{RESETARE}

1. Deschideți PowerShell ca Administrator

2. Activați WSL:
   wsl --install

3. Reporniți computerul

4. După repornire, setați WSL2 ca versiune implicită:
   wsl --set-default-version 2

5. Verificați starea:
   wsl --status

{BOLD}Notă:{RESETARE}
Dacă utilizați Windows 10, asigurați-vă că aveți versiunea 2004 
sau ulterioară (Build 19041 sau mai mare).

{BOLD}Verificare:{RESETARE}
    wsl --list --verbose

Ar trebui să vedeți "VERSION 2" pentru distribuțiile instalate.
""".format(BOLD=BOLD, RESETARE=RESETARE))


def afiseaza_instructiuni_wireshark():
    """Afișează instrucțiunile de instalare Wireshark."""
    afiseaza_titlu("Instalare Wireshark")
    
    print("""
Wireshark este folosit pentru capturarea și analiza traficului de rețea.

{BOLD}Pași de instalare:{RESETARE}

1. Descărcați Wireshark de la:
   https://www.wireshark.org/download.html

2. Alegeți versiunea "Windows x64 Installer"

3. Rulați installerul

4. În timpul instalării:
   - Acceptați licența
   - Selectați toate componentele (implicit)
   - Instalați Npcap când vi se solicită (necesar pentru capturare)

5. Finalizați instalarea

{BOLD}Utilizare cu Docker:{RESETARE}
Pentru a captura traficul Docker, utilizați:
- Interfața "Loopback" pentru trafic localhost
- Sau tcpdump din interiorul containerelor

{BOLD}Verificare:{RESETARE}
Deschideți Wireshark din meniul Start și verificați că 
puteți vedea interfețele de rețea.
""".format(BOLD=BOLD, RESETARE=RESETARE))


def creaza_fisier_cerinte():
    """Creează fișierul requirements.txt."""
    afiseaza_titlu("Creare requirements.txt")
    
    radacina = Path(__file__).parent
    cale_cerinte = radacina / "requirements.txt"
    
    continut = """# Cerințe Python pentru Laboratorul Săptămânii 8
# Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică

# SDK Docker pentru Python
docker>=6.0.0

# Cereri HTTP
requests>=2.28.0

# Parser YAML
pyyaml>=6.0

# Framework de testare
pytest>=7.0.0

# Opțional: pentru tipuri îmbunătățite
typing-extensions>=4.0.0
"""
    
    try:
        cale_cerinte.write_text(continut, encoding='utf-8')
        print(f"{VERDE}✓ Fișierul requirements.txt a fost creat{RESETARE}")
        print(f"  Locație: {cale_cerinte}")
        print()
        print("Pentru a instala toate cerințele, rulați:")
        print(f"  pip install -r {cale_cerinte} --break-system-packages")
    except Exception as e:
        print(f"{ROSU}✗ Eroare la crearea fișierului: {e}{RESETARE}")


def meniu_principal():
    """Afișează meniul principal."""
    afiseaza_titlu("Asistent de Instalare - Laboratorul Săptămânii 8")
    
    print("""
Acest asistent vă va ajuta să instalați componentele necesare.

Selectați ce doriți să faceți:

  1. Instalare pachete Python (docker, requests, pyyaml, pytest)
  2. Instrucțiuni instalare Docker Desktop
  3. Instrucțiuni configurare WSL2
  4. Instrucțiuni instalare Wireshark
  5. Creare fișier requirements.txt
  6. Instalare completă (toate pachetele Python)
  0. Ieșire
""")


def main():
    """Punctul principal de intrare."""
    while True:
        meniu_principal()
        
        try:
            alegere = input("Alegerea dvs. [0-6]: ").strip()
        except KeyboardInterrupt:
            print("\n\nLa revedere!")
            break
        
        if alegere == "0":
            print("\nLa revedere!")
            break
        elif alegere == "1":
            instaleaza_pachete_python()
        elif alegere == "2":
            afiseaza_instructiuni_docker()
        elif alegere == "3":
            afiseaza_instructiuni_wsl2()
        elif alegere == "4":
            afiseaza_instructiuni_wireshark()
        elif alegere == "5":
            creaza_fisier_cerinte()
        elif alegere == "6":
            instaleaza_pachete_python()
        else:
            print(f"{ROSU}Alegere invalidă. Vă rugăm selectați 0-6.{RESETARE}")
        
        print()
        input("Apăsați Enter pentru a continua...")


if __name__ == "__main__":
    main()
