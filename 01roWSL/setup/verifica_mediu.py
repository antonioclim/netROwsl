#!/usr/bin/env python3
"""
Script de Verificare a Mediului de Lucru
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.

ADAPTAT PENTRU: WSL2 + Ubuntu 22.04 + Docker (în WSL) + Portainer Global
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import os
from pathlib import Path
from typing import Optional


class Verificator:
    """Clasă pentru verificarea cerințelor sistemului."""
    
    def __init__(self) -> None:
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sfat_rezolvare: str = "") -> None:
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [\033[92mREUȘIT\033[0m] {nume}")
            self.reusit += 1
        else:
            print(f"  [\033[91mEȘUAT\033[0m]  {nume}")
            if sfat_rezolvare:
                print(f"           \033[93mSoluție:\033[0m {sfat_rezolvare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [\033[93mATENȚIE\033[0m] {nume}: {mesaj}")
        self.avertismente += 1

    def info(self, mesaj: str) -> None:
        """Afișează un mesaj informativ."""
        print(f"           {mesaj}")

    def sumar(self) -> int:
        """Afișează sumarul verificărilor și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: \033[92m{self.reusit} reușite\033[0m, "
              f"\033[91m{self.esuat} eșuate\033[0m, "
              f"\033[93m{self.avertismente} avertismente\033[0m")
        
        if self.esuat == 0:
            print("\n\033[92m✓ Mediul de lucru este pregătit pentru Laboratorul Săptămânii 1!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def ruleaza_in_wsl() -> bool:
    """Verifică dacă rulăm în interiorul WSL."""
    try:
        with open("/proc/version", "r") as f:
            return "microsoft" in f.read().lower()
    except:
        return False


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
    return shutil.which(cmd) is not None


def verifica_docker_ruleaza_wsl() -> bool:
    """Verifică dacă daemon-ul Docker răspunde (mediu WSL)."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def verifica_docker_ruleaza_windows() -> bool:
    """Verifică dacă Docker este accesibil din Windows prin WSL."""
    try:
        rezultat = subprocess.run(
            ["wsl", "docker", "info"],
            capture_output=True,
            timeout=15
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def verifica_docker_compose_wsl() -> bool:
    """Verifică dacă Docker Compose este disponibil în WSL."""
    try:
        # Încearcă docker-compose (stil v1, comun în WSL)
        rezultat = subprocess.run(
            ["docker-compose", "--version"],
            capture_output=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            return True
        
        # Încearcă docker compose (stil v2)
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def verifica_portainer_ruleaza() -> bool:
    """Verifică dacă containerul Portainer rulează pe portul 9000."""
    try:
        if ruleaza_in_wsl():
            rezultat = subprocess.run(
                ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            rezultat = subprocess.run(
                ["wsl", "docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=10
            )
        
        return "portainer" in rezultat.stdout.lower()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def verifica_wsl2_ubuntu_implicit() -> bool:
    """Verifică dacă Ubuntu-22.04 este distribuția WSL implicită."""
    if sys.platform != "win32":
        # Suntem în WSL, verificăm dacă e Ubuntu
        try:
            rezultat = subprocess.run(
                ["lsb_release", "-d"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return "22.04" in rezultat.stdout
        except:
            return False
    
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        iesire = (rezultat.stdout.decode(errors="ignore") + 
                  rezultat.stderr.decode(errors="ignore"))
        return "Ubuntu-22.04" in iesire or "Ubuntu" in iesire
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def verifica_wsl2_disponibil() -> bool:
    """Verifică dacă WSL2 este configurat."""
    if sys.platform != "win32":
        # Suntem deja în WSL, deci e disponibil
        return ruleaza_in_wsl()
    
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        iesire = (rezultat.stdout.decode(errors="ignore") + 
                  rezultat.stderr.decode(errors="ignore"))
        return "WSL 2" in iesire or "Default Version: 2" in iesire
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat."""
    # Căi Windows
    cai_windows = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for cale in cai_windows:
        if cale.exists():
            return True
    
    # Dacă suntem în WSL, verificăm căile Windows prin /mnt/c
    cai_wsl = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    
    for cale in cai_wsl:
        if cale.exists():
            return True
    
    # Fallback Linux/WSL
    return verifica_comanda("wireshark") or verifica_comanda("tshark")


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def obtine_versiune_docker() -> str | None:
    """Obține string-ul versiunii Docker."""
    try:
        if ruleaza_in_wsl():
            rezultat = subprocess.run(
                ["docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
        else:
            rezultat = subprocess.run(
                ["wsl", "docker", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
        if rezultat.returncode == 0:
            return rezultat.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este corectă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src/exercises",
        "tests",
        "docs",
    ]
    return all((radacina / d).is_dir() for d in directoare_necesare)


def main() -> int:
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificarea Mediului pentru Laboratorul Săptămânii 1")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix")
    print("=" * 60)
    print("\nMediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    
    in_wsl = ruleaza_in_wsl()
    if in_wsl:
        print("Detectat: Rulează în interiorul WSL")
    else:
        print("Detectat: Rulează pe Windows")

    v = Verificator()

    # Verificare mediu Python
    print("\n\033[1mMediul Python:\033[0m")
    major, minor, patch = sys.version_info[:3]
    v.verifica(
        f"Python {major}.{minor}.{patch}",
        (major, minor) >= (3, 11),
        "Instalați Python 3.11 sau mai recent de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "yaml": "pip install pyyaml",
    }
    
    for pachet, comanda_instalare in pachete_necesare.items():
        nume_afisat = "pyyaml" if pachet == "yaml" else pachet
        v.verifica(
            f"Pachet Python: {nume_afisat}",
            verifica_pachet_python(pachet),
            comanda_instalare
        )

    # Pachete opționale
    pachete_optionale = ["scapy", "dpkt"]
    for pachet in pachete_optionale:
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet} (opțional)", True)
        else:
            v.avertizeaza(pachet, f"Pachet opțional neinstalat (pip install {pachet})")

    # Verificare mediu WSL2
    print("\n\033[1mMediul WSL2:\033[0m")
    
    v.verifica(
        "WSL2 disponibil și configurat",
        verifica_wsl2_disponibil(),
        "Activați WSL2: wsl --install (necesită restart)"
    )
    
    v.verifica(
        "Ubuntu 22.04 este distribuția implicită",
        verifica_wsl2_ubuntu_implicit(),
        "Setați implicit: wsl --set-default Ubuntu-22.04"
    )

    # Verificare mediu Docker (în WSL)
    print("\n\033[1mMediul Docker (în WSL):\033[0m")
    
    if in_wsl:
        docker_instalat = verifica_comanda("docker")
    else:
        try:
            rezultat = subprocess.run(["wsl", "which", "docker"], capture_output=True, timeout=5)
            docker_instalat = rezultat.returncode == 0
        except:
            docker_instalat = False
    
    v.verifica(
        "Docker CLI disponibil în WSL",
        docker_instalat,
        "Instalați Docker în WSL: sudo apt install docker.io"
    )

    if docker_instalat:
        versiune_docker = obtine_versiune_docker()
        if versiune_docker:
            v.info(f"Versiune: {versiune_docker}")

    if in_wsl:
        docker_ruleaza = verifica_docker_ruleaza_wsl()
    else:
        docker_ruleaza = verifica_docker_ruleaza_windows()
    
    v.verifica(
        "Daemon-ul Docker rulează",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start (în Ubuntu WSL)"
    )

    if in_wsl:
        compose_ok = verifica_docker_compose_wsl()
    else:
        try:
            rezultat = subprocess.run(["wsl", "docker-compose", "--version"], capture_output=True, timeout=10)
            compose_ok = rezultat.returncode == 0
        except:
            compose_ok = False
    
    v.verifica(
        "Docker Compose disponibil",
        compose_ok,
        "Instalați: sudo apt install docker-compose"
    )

    # Portainer (Serviciu Global)
    print("\n\033[1mPortainer (Serviciu Global):\033[0m")
    
    portainer_ok = verifica_portainer_ruleaza()
    v.verifica(
        "Portainer rulează pe portul 9000",
        portainer_ok,
        "Porniți Portainer: docker start portainer"
    )
    
    if portainer_ok:
        v.info("Acces: http://localhost:9000")
        v.info("Credențiale: stud / studstudstud")

    # Instrumente de rețea
    print("\n\033[1mInstrumente de Analiză Rețea:\033[0m")
    
    v.verifica(
        "Wireshark instalat",
        verifica_wireshark(),
        "Instalați Wireshark de pe wireshark.org (pe Windows)"
    )

    if verifica_comanda("tshark"):
        v.verifica("tshark (CLI) disponibil", True)
    else:
        v.avertizeaza("tshark", "Analiza pachetelor CLI va folosi containerul Docker")

    # Instrumente opționale
    print("\n\033[1mInstrumente Opționale:\033[0m")
    
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("curl"):
        v.verifica("curl instalat", True)
    else:
        v.avertizeaza("curl", "Util pentru testarea HTTP")

    # Structura proiectului
    print("\n\033[1mStructura Proiectului:\033[0m")
    
    radacina = Path(__file__).parent.parent
    directoare_necesare = ["docker", "scripts", "src", "tests", "pcap", "artifacts"]
    
    for dir_nume in directoare_necesare:
        cale_dir = radacina / dir_nume
        v.verifica(
            f"Director: {dir_nume}/",
            cale_dir.exists(),
            f"Director lipsă: {cale_dir}"
        )

    # Verifică existența docker-compose.yml
    fisier_compose = radacina / "docker" / "docker-compose.yml"
    v.verifica(
        "docker-compose.yml prezent",
        fisier_compose.exists(),
        "Fișierul de configurare Docker lipsește"
    )

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
