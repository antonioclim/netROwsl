#!/usr/bin/env python3
"""
Asistent de Instalare a Cerințelor Preliminare
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Ghidează utilizatorul prin procesul de instalare a componentelor necesare.
"""

import subprocess
import sys
import shutil
import webbrowser
from pathlib import Path


# Coduri ANSI pentru culori în terminal
class Culori:
    ANTET = '\033[95m'
    ALBASTRU = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROȘU = '\033[91m'
    SFÂRȘIT = '\033[0m'
    BOLD = '\033[1m'


def afișează_antet(text: str) -> None:
    """Afișează un antet formatat."""
    print(f"\n{Culori.BOLD}{Culori.ALBASTRU}{'=' * 60}{Culori.SFÂRȘIT}")
    print(f"{Culori.BOLD}{Culori.ALBASTRU}{text}{Culori.SFÂRȘIT}")
    print(f"{Culori.BOLD}{Culori.ALBASTRU}{'=' * 60}{Culori.SFÂRȘIT}\n")


def afișează_succes(text: str) -> None:
    """Afișează un mesaj de succes."""
    print(f"{Culori.VERDE}✓ {text}{Culori.SFÂRȘIT}")


def afișează_eroare(text: str) -> None:
    """Afișează un mesaj de eroare."""
    print(f"{Culori.ROȘU}✗ {text}{Culori.SFÂRȘIT}")


def afișează_avertisment(text: str) -> None:
    """Afișează un avertisment."""
    print(f"{Culori.GALBEN}⚠ {text}{Culori.SFÂRȘIT}")


def afișează_info(text: str) -> None:
    """Afișează un mesaj informativ."""
    print(f"{Culori.CYAN}ℹ {text}{Culori.SFÂRȘIT}")


def verifică_comandă(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(cmd) is not None


def deschide_url(url: str) -> None:
    """Deschide un URL în browserul implicit."""
    try:
        webbrowser.open(url)
        afișează_info(f"S-a deschis în browser: {url}")
    except Exception as e:
        afișează_eroare(f"Nu s-a putut deschide browserul: {e}")
        afișează_info(f"Deschideți manual: {url}")


def solicită_confirmare(mesaj: str) -> bool:
    """Solicită confirmare de la utilizator."""
    while True:
        răspuns = input(f"{mesaj} (d/n): ").strip().lower()
        if răspuns in ['d', 'da', 'y', 'yes']:
            return True
        elif răspuns in ['n', 'nu', 'no']:
            return False
        print("Vă rugăm răspundeți cu 'd' (da) sau 'n' (nu)")


def instalează_python() -> None:
    """Ghidează instalarea Python."""
    afișează_antet("Instalare Python 3.11+")
    
    if sys.version_info >= (3, 11):
        afișează_succes(f"Python {sys.version_info.major}.{sys.version_info.minor} este deja instalat!")
        return
    
    afișează_avertisment(f"Versiune curentă: Python {sys.version_info.major}.{sys.version_info.minor}")
    afișează_info("Este necesară versiunea 3.11 sau mai recentă.")
    
    print("\nPași pentru instalare:")
    print("1. Descărcați Python 3.11+ de pe python.org")
    print("2. La instalare, bifați 'Add Python to PATH'")
    print("3. Reporniți terminalul după instalare")
    
    if solicită_confirmare("Doriți să deschid pagina de descărcare?"):
        deschide_url("https://www.python.org/downloads/")


def instalează_docker() -> None:
    """Ghidează instalarea Docker Desktop."""
    afișează_antet("Instalare Docker Desktop")
    
    if verifică_comandă("docker"):
        afișează_succes("Docker este deja instalat!")
        
        # Verificare dacă rulează
        try:
            rezultat = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                afișează_succes("Docker daemon rulează corect.")
            else:
                afișează_avertisment("Docker este instalat dar nu rulează.")
                afișează_info("Porniți Docker Desktop din Start Menu.")
        except Exception:
            afișează_avertisment("Nu s-a putut verifica starea Docker.")
        return
    
    print("\nPași pentru instalare:")
    print("1. Descărcați Docker Desktop de pe docker.com")
    print("2. Rulați installer-ul")
    print("3. În timpul instalării, selectați 'Use WSL 2 instead of Hyper-V'")
    print("4. Reporniți computerul după instalare")
    print("5. La prima pornire, acceptați termenii de licență")
    
    if solicită_confirmare("Doriți să deschid pagina de descărcare Docker?"):
        deschide_url("https://www.docker.com/products/docker-desktop/")


def instalează_wsl2() -> None:
    """Ghidează activarea WSL2."""
    afișează_antet("Activare WSL2")
    
    print("WSL2 (Windows Subsystem for Linux 2) este necesar pentru Docker.")
    print("\nPentru a activa WSL2, rulați în PowerShell ca Administrator:")
    print()
    print("  wsl --install")
    print()
    print("Aceasta va:")
    print("  - Activa componentele Windows necesare")
    print("  - Instala kernel-ul WSL2")
    print("  - Descărca distribuția Ubuntu implicit")
    print()
    print("După instalare, reporniți computerul.")
    
    afișează_info("Dacă wsl --install nu funcționează, încercați:")
    print("  dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart")
    print("  dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart")


def instalează_wireshark() -> None:
    """Ghidează instalarea Wireshark."""
    afișează_antet("Instalare Wireshark")
    
    căi_wireshark = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    if any(cale.exists() for cale in căi_wireshark):
        afișează_succes("Wireshark este deja instalat!")
        return
    
    print("Wireshark este folosit pentru analiza traficului de rețea.")
    print("\nPași pentru instalare:")
    print("1. Descărcați Wireshark de pe wireshark.org")
    print("2. Rulați installer-ul cu opțiunile implicite")
    print("3. Instalați Npcap când vi se solicită (necesar pentru captură)")
    
    if solicită_confirmare("Doriți să deschid pagina de descărcare Wireshark?"):
        deschide_url("https://www.wireshark.org/download.html")


def instalează_pachete_python() -> None:
    """Instalează pachetele Python necesare."""
    afișează_antet("Instalare Pachete Python")
    
    pachete = ["docker", "requests", "pyyaml"]
    pachete_lipsă = []
    
    for pachet in pachete:
        try:
            __import__(pachet.replace("pyyaml", "yaml"))
            afișează_succes(f"Pachetul '{pachet}' este instalat")
        except ImportError:
            pachete_lipsă.append(pachet)
            afișează_avertisment(f"Pachetul '{pachet}' lipsește")
    
    if not pachete_lipsă:
        afișează_succes("Toate pachetele Python sunt instalate!")
        return
    
    if solicită_confirmare(f"Doriți să instalez pachetele lipsă? ({', '.join(pachete_lipsă)})"):
        for pachet in pachete_lipsă:
            print(f"\nInstalare {pachet}...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", pachet],
                    check=True
                )
                afișează_succes(f"{pachet} instalat cu succes")
            except subprocess.CalledProcessError:
                afișează_eroare(f"Eroare la instalarea {pachet}")
                afișează_info(f"Încercați manual: pip install {pachet}")


def afișează_meniu() -> None:
    """Afișează meniul principal."""
    print("\n" + "=" * 60)
    print("Asistent de Instalare - Săptămâna 2")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()
    print("Selectați ce doriți să instalați:")
    print()
    print("  1. Python 3.11+")
    print("  2. Docker Desktop")
    print("  3. WSL2 (Windows Subsystem for Linux)")
    print("  4. Wireshark")
    print("  5. Pachete Python (docker, requests, pyyaml)")
    print("  6. Verificare completă a mediului")
    print("  7. Instalare tot (ghidare completă)")
    print()
    print("  0. Ieșire")
    print()


def main() -> int:
    """Funcția principală."""
    afișează_antet("Asistent de Instalare - Laborator Rețele de Calculatoare")
    
    while True:
        afișează_meniu()
        
        try:
            alegere = input("Alegerea dumneavoastră: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n")
            afișează_info("La revedere!")
            return 0
        
        if alegere == "0":
            afișează_info("La revedere!")
            return 0
        elif alegere == "1":
            instalează_python()
        elif alegere == "2":
            instalează_docker()
        elif alegere == "3":
            instalează_wsl2()
        elif alegere == "4":
            instalează_wireshark()
        elif alegere == "5":
            instalează_pachete_python()
        elif alegere == "6":
            # Rulare script de verificare
            script_verificare = Path(__file__).parent / "verify_environment.py"
            if script_verificare.exists():
                subprocess.run([sys.executable, str(script_verificare)])
            else:
                afișează_eroare("Script-ul de verificare nu a fost găsit!")
        elif alegere == "7":
            # Ghidare completă
            instalează_python()
            input("\nApăsați Enter pentru a continua...")
            
            instalează_wsl2()
            input("\nApăsați Enter pentru a continua...")
            
            instalează_docker()
            input("\nApăsați Enter pentru a continua...")
            
            instalează_wireshark()
            input("\nApăsați Enter pentru a continua...")
            
            instalează_pachete_python()
            
            afișează_antet("Instalare Completă")
            afișează_info("Toate componentele au fost configurate sau ghidate.")
            afișează_info("Rulați 'python setup/verify_environment.py' pentru verificare.")
        else:
            afișează_eroare("Opțiune invalidă. Încercați din nou.")
        
        input("\nApăsați Enter pentru a reveni la meniu...")


if __name__ == "__main__":
    sys.exit(main())
