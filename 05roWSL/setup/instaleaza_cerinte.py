#!/usr/bin/env python3
"""
Asistent de Instalare Cerințe Preliminare
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Ghidează utilizatorul prin procesul de instalare a tuturor dependențelor necesare.
"""

import subprocess
import sys
import platform
import webbrowser
from pathlib import Path


def afiseaza_titlu(titlu: str):
    """Afișează un titlu formatat."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60)


def afiseaza_pas(numar: int, descriere: str):
    """Afișează un pas din proces."""
    print(f"\n[Pasul {numar}] {descriere}")
    print("-" * 40)


def asteapta_confirmare(mesaj: str = "Apăsați Enter pentru a continua..."):
    """Așteaptă confirmarea utilizatorului."""
    input(f"\n{mesaj}")


def verifica_si_instaleaza_python():
    """Verifică și ghidează instalarea Python."""
    afiseaza_pas(1, "Verificare Python")
    
    versiune = sys.version_info
    print(f"Versiune Python detectată: {versiune.major}.{versiune.minor}.{versiune.micro}")
    
    if versiune >= (3, 11):
        print("✓ Versiunea Python este compatibilă!")
        return True
    else:
        print("✗ Este necesară versiunea Python 3.11 sau mai nouă.")
        print("\nPași de instalare:")
        print("  1. Descărcați Python de la: https://www.python.org/downloads/")
        print("  2. În timpul instalării, bifați 'Add Python to PATH'")
        print("  3. Reporniți terminalul după instalare")
        
        raspuns = input("\nDoriți să deschid pagina de descărcare? (da/nu): ")
        if raspuns.lower() in ('da', 'd', 'yes', 'y'):
            webbrowser.open("https://www.python.org/downloads/")
        
        return False


def verifica_si_instaleaza_docker():
    """Verifică și ghidează instalarea Docker Desktop."""
    afiseaza_pas(2, "Verificare Docker Desktop")
    
    try:
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        if rezultat.returncode == 0:
            print(f"✓ Docker detectat: {rezultat.stdout.strip()}")
            
            # Verifică dacă rulează
            rezultat_info = subprocess.run(
                ["docker", "info"],
                capture_output=True
            )
            if rezultat_info.returncode == 0:
                print("✓ Daemonul Docker rulează!")
                return True
            else:
                print("⚠ Docker este instalat dar nu rulează.")
                print("\nPași de rezolvare:")
                print("  1. Deschideți aplicația Docker Desktop")
                print("  2. Așteptați până când pictograma devine stabilă")
                print("  3. Rulați din nou acest script")
                return False
    except FileNotFoundError:
        pass
    
    print("✗ Docker Desktop nu a fost detectat.")
    print("\nPași de instalare:")
    print("  1. Descărcați Docker Desktop de la: https://www.docker.com/products/docker-desktop")
    print("  2. Instalați aplicația")
    print("  3. În setări, activați 'Use WSL 2 based engine'")
    print("  4. Reporniți calculatorul dacă este necesar")
    
    raspuns = input("\nDoriți să deschid pagina de descărcare? (da/nu): ")
    if raspuns.lower() in ('da', 'd', 'yes', 'y'):
        webbrowser.open("https://www.docker.com/products/docker-desktop")
    
    return False


def verifica_si_activeaza_wsl2():
    """Verifică și ghidează activarea WSL2."""
    afiseaza_pas(3, "Verificare WSL2")
    
    sistem = platform.system()
    if sistem != "Windows":
        print(f"Sistem detectat: {sistem}")
        print("WSL2 este disponibil doar pe Windows. Omitem această verificare.")
        return True
    
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            text=True
        )
        output = rezultat.stdout + rezultat.stderr
        
        if "WSL 2" in output or "Default Version: 2" in output:
            print("✓ WSL2 este activat și configurat!")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠ WSL2 nu pare să fie configurat corect.")
    print("\nPași de activare:")
    print("  1. Deschideți PowerShell ca Administrator")
    print("  2. Rulați: wsl --install")
    print("  3. Reporniți calculatorul")
    print("  4. După repornire, configurați distribuția Ubuntu")
    print("  5. Setați WSL2 ca versiune implicită: wsl --set-default-version 2")
    
    return False


def verifica_si_instaleaza_wireshark():
    """Verifică și ghidează instalarea Wireshark."""
    afiseaza_pas(4, "Verificare Wireshark")
    
    cale_wireshark = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    
    if cale_wireshark.exists():
        print("✓ Wireshark este instalat!")
        return True
    
    print("✗ Wireshark nu a fost detectat.")
    print("\nPași de instalare:")
    print("  1. Descărcați Wireshark de la: https://www.wireshark.org/download.html")
    print("  2. Alegeți versiunea pentru Windows (64-bit)")
    print("  3. În timpul instalării, instalați și Npcap când vi se solicită")
    
    raspuns = input("\nDoriți să deschid pagina de descărcare? (da/nu): ")
    if raspuns.lower() in ('da', 'd', 'yes', 'y'):
        webbrowser.open("https://www.wireshark.org/download.html")
    
    return False


def instaleaza_pachete_python():
    """Instalează pachetele Python necesare."""
    afiseaza_pas(5, "Instalare Pachete Python")
    
    pachete = ["docker", "requests", "pyyaml"]
    
    print("Se vor instala următoarele pachete:")
    for pachet in pachete:
        print(f"  • {pachet}")
    
    raspuns = input("\nContinuați cu instalarea? (da/nu): ")
    if raspuns.lower() not in ('da', 'd', 'yes', 'y'):
        print("Instalare anulată.")
        return False
    
    for pachet in pachete:
        print(f"\nInstalare {pachet}...")
        rezultat = subprocess.run(
            [sys.executable, "-m", "pip", "install", pachet],
            capture_output=True,
            text=True
        )
        if rezultat.returncode == 0:
            print(f"  ✓ {pachet} instalat cu succes")
        else:
            print(f"  ✗ Eroare la instalarea {pachet}")
            print(f"    {rezultat.stderr}")
            return False
    
    print("\n✓ Toate pachetele au fost instalate!")
    return True


def main():
    afiseaza_titlu("Asistent de Instalare - Laborator Rețele de Calculatoare")
    
    print("""
Acest asistent vă va ghida prin procesul de configurare a mediului
pentru laboratorul de Rețele de Calculatoare - Săptămâna 5.

Cerințe care vor fi verificate:
  • Python 3.11 sau mai nou
  • Docker Desktop cu backend WSL2
  • WSL2 (Windows Subsystem for Linux 2)
  • Wireshark pentru analiza traficului
  • Pachete Python necesare
    """)
    
    asteapta_confirmare()
    
    rezultate = {
        "python": verifica_si_instaleaza_python(),
        "docker": verifica_si_instaleaza_docker(),
        "wsl2": verifica_si_activeaza_wsl2(),
        "wireshark": verifica_si_instaleaza_wireshark(),
    }
    
    if all(rezultate.values()):
        asteapta_confirmare()
        rezultate["pachete"] = instaleaza_pachete_python()
    
    # Rezumat final
    afiseaza_titlu("Rezumat Instalare")
    
    toate_ok = True
    for componenta, status in rezultate.items():
        simbol = "✓" if status else "✗"
        print(f"  {simbol} {componenta.capitalize()}")
        if not status:
            toate_ok = False
    
    if toate_ok:
        print("\n" + "=" * 60)
        print("  ✓ MEDIUL ESTE COMPLET CONFIGURAT!")
        print("=" * 60)
        print("\nPuteți acum să porniți laboratorul cu comanda:")
        print("  python scripts/porneste_laborator.py")
        return 0
    else:
        print("\n" + "=" * 60)
        print("  ⚠ UNELE COMPONENTE NECESITĂ ATENȚIE")
        print("=" * 60)
        print("\nRezolvați problemele indicate mai sus și rulați din nou acest script.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
