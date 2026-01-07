#!/usr/bin/env python3
"""
Ghid de Instalare Cerințe Preliminare
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script oferă instrucțiuni pentru instalarea cerințelor necesare.
NU instalează automat software - oferă doar ghidaj.
"""

import sys
import shutil
import subprocess
from pathlib import Path


def print_antet(titlu: str):
    """Afișează un antet formatat."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60)


def print_pas(numar: int, descriere: str):
    """Afișează un pas numerotat."""
    print(f"\n  \033[1mPasul {numar}:\033[0m {descriere}")


def print_comanda(comanda: str):
    """Afișează o comandă de executat."""
    print(f"    \033[94m{comanda}\033[0m")


def print_info(mesaj: str):
    """Afișează un mesaj informativ."""
    print(f"    ℹ️  {mesaj}")


def print_succes(mesaj: str):
    """Afișează un mesaj de succes."""
    print(f"    \033[92m✓ {mesaj}\033[0m")


def print_avertisment(mesaj: str):
    """Afișează un avertisment."""
    print(f"    \033[93m⚠ {mesaj}\033[0m")


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(cmd) is not None


def ghid_instalare_wsl2():
    """Ghid pentru instalarea WSL2."""
    print_antet("INSTALARE WSL2")
    
    try:
        rezultat = subprocess.run(["wsl", "--status"], capture_output=True, timeout=5)
        if rezultat.returncode == 0:
            print_succes("WSL2 pare să fie deja instalat!")
            return
    except Exception:
        pass
    
    print_pas(1, "Deschideți PowerShell ca Administrator")
    print_info("Click dreapta pe Start → Terminal Windows (Administrator)")
    
    print_pas(2, "Executați comanda de instalare WSL")
    print_comanda("wsl --install")
    
    print_pas(3, "Reporniți calculatorul când vi se solicită")
    
    print_pas(4, "După repornire, setați WSL2 ca versiune implicită")
    print_comanda("wsl --set-default-version 2")
    
    print_pas(5, "Instalați o distribuție Linux (recomandat: Ubuntu)")
    print_comanda("wsl --install -d Ubuntu")
    
    print_info("Prima pornire va dura câteva minute pentru configurare.")
    print_info("Vi se va cere să creați un utilizator și o parolă.")


def ghid_instalare_docker():
    """Ghid pentru instalarea Docker Desktop."""
    print_antet("INSTALARE DOCKER DESKTOP")
    
    if verifica_comanda("docker"):
        try:
            rezultat = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
            if rezultat.returncode == 0:
                print_succes("Docker Desktop pare să fie deja instalat și activ!")
                return
        except Exception:
            pass
    
    print_pas(1, "Descărcați Docker Desktop")
    print_info("Accesați: https://www.docker.com/products/docker-desktop/")
    print_info("Selectați versiunea pentru Windows")
    
    print_pas(2, "Rulați installerul")
    print_info("Asigurați-vă că opțiunea 'Use WSL 2 instead of Hyper-V' este selectată")
    
    print_pas(3, "După instalare, porniți Docker Desktop")
    print_info("Căutați 'Docker Desktop' în meniul Start")
    
    print_pas(4, "Configurați backend-ul WSL2")
    print_info("Settings → General → bifați 'Use the WSL 2 based engine'")
    print_info("Settings → Resources → WSL Integration → activați pentru distribuția voastră")
    
    print_pas(5, "Verificați instalarea")
    print_comanda("docker --version")
    print_comanda("docker compose version")
    print_comanda("docker run hello-world")


def ghid_instalare_wireshark():
    """Ghid pentru instalarea Wireshark."""
    print_antet("INSTALARE WIRESHARK")
    
    cale_wireshark = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    if cale_wireshark.exists():
        print_succes("Wireshark pare să fie deja instalat!")
        return
    
    print_pas(1, "Descărcați Wireshark")
    print_info("Accesați: https://www.wireshark.org/download.html")
    print_info("Selectați 'Windows x64 Installer'")
    
    print_pas(2, "Rulați installerul")
    print_info("Acceptați opțiunile implicite")
    print_avertisment("IMPORTANT: Instalați Npcap când vi se solicită!")
    print_info("Npcap este necesar pentru capturarea pachetelor")
    
    print_pas(3, "Configurare Npcap (la instalare)")
    print_info("Bifați: 'Install Npcap in WinPcap API-compatible Mode'")
    print_info("Bifați: 'Support raw 802.11 traffic'")
    
    print_pas(4, "După instalare, verificați funcționarea")
    print_info("Deschideți Wireshark și verificați că interfețele de rețea sunt vizibile")


def ghid_instalare_python():
    """Ghid pentru instalarea Python."""
    print_antet("INSTALARE PYTHON")
    
    versiune = sys.version_info
    if versiune >= (3, 8):
        print_succes(f"Python {versiune.major}.{versiune.minor}.{versiune.micro} este instalat!")
        return
    
    print_pas(1, "Descărcați Python")
    print_info("Accesați: https://www.python.org/downloads/")
    print_info("Descărcați versiunea 3.11 sau mai nouă")
    
    print_pas(2, "Rulați installerul")
    print_avertisment("IMPORTANT: Bifați 'Add Python to PATH' la început!")
    print_info("Selectați 'Customize installation' pentru opțiuni avansate")
    
    print_pas(3, "Verificați instalarea")
    print_comanda("python --version")
    print_comanda("pip --version")
    
    print_pas(4, "Instalați pachetele opționale")
    print_comanda("pip install docker pyyaml requests")


def ghid_instrumente_wsl():
    """Ghid pentru instalarea instrumentelor în WSL."""
    print_antet("INSTRUMENTE ÎN WSL (OPȚIONAL)")
    
    print_info("Aceste instrumente sunt utile pentru depanare și analiză avansată.")
    
    print_pas(1, "Deschideți terminalul WSL")
    print_comanda("wsl")
    
    print_pas(2, "Actualizați lista de pachete")
    print_comanda("sudo apt update")
    
    print_pas(3, "Instalați instrumentele de rețea")
    print_comanda("sudo apt install -y tcpdump tshark netcat-openbsd")
    
    print_pas(4, "Configurați permisiuni pentru capturare pachete")
    print_comanda("sudo usermod -aG wireshark $USER")
    print_info("Deconectați-vă și reconectați-vă pentru aplicarea modificărilor")


def main():
    """Funcția principală."""
    print("\n" + "=" * 60)
    print("  GHID INSTALARE CERINȚE PRELIMINARE")
    print("  Laborator Săptămâna 4 - Rețele de Calculatoare")
    print("  ASE București - Informatică Economică")
    print("=" * 60)
    
    print("\n\033[1mAcest script oferă instrucțiuni pas cu pas pentru instalarea")
    print("tuturor componentelor necesare pentru laborator.\033[0m")
    print("\nSelectați ce doriți să instalați:\n")
    print("  1. WSL2 (Windows Subsystem for Linux)")
    print("  2. Docker Desktop")
    print("  3. Wireshark")
    print("  4. Python")
    print("  5. Instrumente WSL (tcpdump, tshark, netcat)")
    print("  6. Toate componentele (ghid complet)")
    print("  0. Ieșire")
    
    while True:
        try:
            print()
            alegere = input("Selectați opțiunea (0-6): ").strip()
            
            if alegere == "0":
                print("\nLa revedere!")
                break
            elif alegere == "1":
                ghid_instalare_wsl2()
            elif alegere == "2":
                ghid_instalare_docker()
            elif alegere == "3":
                ghid_instalare_wireshark()
            elif alegere == "4":
                ghid_instalare_python()
            elif alegere == "5":
                ghid_instrumente_wsl()
            elif alegere == "6":
                ghid_instalare_wsl2()
                ghid_instalare_docker()
                ghid_instalare_wireshark()
                ghid_instalare_python()
                ghid_instrumente_wsl()
                print_antet("INSTALARE COMPLETĂ")
                print_info("Urmați pașii de mai sus în ordinea prezentată.")
                print_info("După instalare, rulați: python setup/verify_environment.py")
            else:
                print("Opțiune invalidă. Încercați din nou.")
                
            print("\n" + "-" * 40)
            print("Apăsați Enter pentru a continua...")
            input()
            
        except KeyboardInterrupt:
            print("\n\nÎntrerupt de utilizator. La revedere!")
            break
        except EOFError:
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
