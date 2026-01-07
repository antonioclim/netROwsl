#!/usr/bin/env python3
"""
Asistent de Configurare Docker Desktop
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Ajută la configurarea Docker Desktop pentru mediul de laborator.
"""

import subprocess
import sys
import json
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


def verifica_docker_instalat() -> bool:
    """Verifică dacă Docker este instalat."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def verifica_docker_pornit() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return result.returncode == 0
    except Exception:
        return False


def obtine_info_docker() -> dict:
    """Obține informații despre configurația Docker."""
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
    except Exception:
        pass
    return {}


def verifica_resurse():
    """Verifică și afișează resursele Docker disponibile."""
    afiseaza_titlu("Resurse Docker Disponibile")
    
    info = obtine_info_docker()
    
    if not info:
        print(f"{ROSU}Nu se pot obține informațiile Docker.{RESETARE}")
        print("Asigurați-vă că Docker Desktop rulează.")
        return
    
    # Memorie
    memorie_bytes = info.get('MemTotal', 0)
    memorie_gb = memorie_bytes / (1024**3)
    
    print(f"\n{ALBASTRU}Memorie:{RESETARE}")
    print(f"  Total disponibil: {memorie_gb:.1f} GB")
    
    if memorie_gb < 4:
        print(f"  {ROSU}⚠ Memorie insuficientă! Se recomandă minim 4 GB.{RESETARE}")
    elif memorie_gb < 8:
        print(f"  {GALBEN}! Memorie limitată. Se recomandă 8 GB pentru performanță optimă.{RESETARE}")
    else:
        print(f"  {VERDE}✓ Memorie suficientă{RESETARE}")
    
    # CPU-uri
    cpus = info.get('NCPU', 0)
    print(f"\n{ALBASTRU}CPU-uri:{RESETARE}")
    print(f"  Disponibile: {cpus}")
    
    if cpus < 2:
        print(f"  {GALBEN}! Se recomandă minim 2 CPU-uri.{RESETARE}")
    else:
        print(f"  {VERDE}✓ CPU-uri suficiente{RESETARE}")
    
    # Spațiu pe disc
    print(f"\n{ALBASTRU}Stocare:{RESETARE}")
    result = subprocess.run(
        ["docker", "system", "df"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(result.stdout)


def verifica_retele():
    """Verifică rețelele Docker existente."""
    afiseaza_titlu("Rețele Docker")
    
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", 
             "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
            
            # Verifică dacă rețeaua laboratorului există
            if "week8" in result.stdout.lower():
                print(f"\n{VERDE}✓ Rețeaua laboratorului este deja creată.{RESETARE}")
    except Exception as e:
        print(f"{ROSU}Eroare la listarea rețelelor: {e}{RESETARE}")


def curata_resurse_nefolosite():
    """Curăță resursele Docker nefolosite."""
    afiseaza_titlu("Curățare Resurse Nefolosite")
    
    print("Aceasta va elimina:")
    print("  - Containere oprite")
    print("  - Rețele nefolosite")
    print("  - Imagini dangling (fără tag)")
    print("  - Cache de build nefolosit")
    print()
    
    raspuns = input("Continuați cu curățarea? [d/n]: ").lower().strip()
    
    if raspuns in ['d', 'da', 'y', 'yes']:
        try:
            print(f"\n{ALBASTRU}Curățare în curs...{RESETARE}")
            result = subprocess.run(
                ["docker", "system", "prune", "-f"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(result.stdout)
                print(f"{VERDE}✓ Curățare completă!{RESETARE}")
            else:
                print(f"{ROSU}Eroare: {result.stderr}{RESETARE}")
        except Exception as e:
            print(f"{ROSU}Excepție: {e}{RESETARE}")
    else:
        print("Curățare anulată.")


def afiseaza_configurare_recomandata():
    """Afișează configurarea recomandată pentru Docker Desktop."""
    afiseaza_titlu("Configurare Recomandată Docker Desktop")
    
    print("""
Pentru performanță optimă în laborator, se recomandă:

{BOLD}1. Resurse (Settings > Resources):{RESETARE}
   - Memorie: Minim 4 GB, recomandat 8 GB
   - CPU-uri: Minim 2, recomandat 4
   - Swap: 1-2 GB
   - Spațiu disc: Minim 20 GB

{BOLD}2. WSL Integration (Settings > Resources > WSL Integration):{RESETARE}
   - Activați "Enable integration with my default WSL distro"
   - Activați distribuțiile WSL pe care le folosiți

{BOLD}3. Docker Engine (Settings > Docker Engine):{RESETARE}
   Configurația JSON recomandată:
   {{
     "builder": {{
       "gc": {{
         "defaultKeepStorage": "20GB",
         "enabled": true
       }}
     }},
     "experimental": false,
     "log-driver": "json-file",
     "log-opts": {{
       "max-size": "10m",
       "max-file": "3"
     }}
   }}

{BOLD}4. General (Settings > General):{RESETARE}
   - ✓ Start Docker Desktop when you log in
   - ✓ Use Docker Compose V2

{BOLD}5. Verificare:{RESETARE}
   După modificări, reporniți Docker Desktop și verificați:
   docker info
   docker compose version
""".format(BOLD=BOLD, RESETARE=RESETARE))


def testeaza_conectivitate():
    """Testează conectivitatea Docker."""
    afiseaza_titlu("Test Conectivitate Docker")
    
    teste = [
        ("Docker instalat", ["docker", "--version"]),
        ("Daemon Docker", ["docker", "info"]),
        ("Docker Compose V2", ["docker", "compose", "version"]),
        ("Pull imagine test", ["docker", "pull", "hello-world"]),
    ]
    
    for nume, comanda in teste:
        print(f"\n{ALBASTRU}Testare: {nume}...{RESETARE}")
        try:
            result = subprocess.run(
                comanda,
                capture_output=True,
                text=True,
                timeout=60
            )
            if result.returncode == 0:
                print(f"  {VERDE}✓ {nume}: OK{RESETARE}")
                if comanda[0] == "docker" and comanda[1] in ["--version", "compose"]:
                    print(f"    {result.stdout.strip()}")
            else:
                print(f"  {ROSU}✗ {nume}: EROARE{RESETARE}")
                if result.stderr:
                    print(f"    {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            print(f"  {ROSU}✗ {nume}: TIMEOUT{RESETARE}")
        except Exception as e:
            print(f"  {ROSU}✗ {nume}: {e}{RESETARE}")


def meniu_principal():
    """Afișează meniul principal."""
    print()
    print("=" * 60)
    print(f"{BOLD}Asistent Configurare Docker Desktop{RESETARE}")
    print("Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)
    print("""
Selectați o opțiune:

  1. Verificare resurse Docker disponibile
  2. Verificare rețele Docker
  3. Curățare resurse nefolosite
  4. Afișare configurare recomandată
  5. Test conectivitate completă
  0. Ieșire
""")


def main():
    """Punctul principal de intrare."""
    if not verifica_docker_instalat():
        print(f"{ROSU}Docker nu este instalat!{RESETARE}")
        print("Instalați Docker Desktop de pe https://docker.com")
        return 1
    
    if not verifica_docker_pornit():
        print(f"{GALBEN}Docker Desktop nu rulează!{RESETARE}")
        print("Porniți Docker Desktop și așteptați inițializarea.")
        return 1
    
    while True:
        meniu_principal()
        
        try:
            alegere = input("Alegerea dvs. [0-5]: ").strip()
        except KeyboardInterrupt:
            print("\n\nLa revedere!")
            break
        
        if alegere == "0":
            print("\nLa revedere!")
            break
        elif alegere == "1":
            verifica_resurse()
        elif alegere == "2":
            verifica_retele()
        elif alegere == "3":
            curata_resurse_nefolosite()
        elif alegere == "4":
            afiseaza_configurare_recomandata()
        elif alegere == "5":
            testeaza_conectivitate()
        else:
            print(f"{ROSU}Alegere invalidă. Selectați 0-5.{RESETARE}")
        
        print()
        input("Apăsați Enter pentru a continua...")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
