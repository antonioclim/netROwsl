#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică că toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 7 în mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Tuple


class Verificator:
    """Clasă pentru gestionarea verificărilor și raportarea rezultatelor."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_rezolvare: str = ""):
        """Verifică o condiție și raportează rezultatul."""
        if conditie:
            print(f"  [\033[92mOK\033[0m] {nume}")
            self.reusit += 1
        else:
            print(f"  [\033[91mEȘUAT\033[0m] {nume}")
            if indicatie_rezolvare:
                print(f"          Rezolvare: {indicatie_rezolvare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Emite un avertisment pentru o verificare opțională."""
        print(f"  [\033[93mATENȚIE\033[0m] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("\n\033[92m✓ Mediul este pregătit pentru laboratorul Săptămânii 7!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
    return shutil.which(cmd) is not None


def verifica_docker_pornit() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def porneste_docker() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    try:
        rezultat = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def verifica_wsl2() -> bool:
    """Verifică dacă rulăm în WSL2."""
    try:
        if not os.path.exists("/proc/version"):
            return False
        
        with open("/proc/version", "r") as f:
            version_info = f.read().lower()
        
        if "microsoft" not in version_info and "wsl" not in version_info:
            return False
        
        if "wsl2" in version_info:
            return True
        
        return os.path.exists("/run/WSL") or "microsoft-standard" in version_info
        
    except Exception:
        return False


def verifica_ubuntu_versiune() -> Tuple[bool, str]:
    """Verifică versiunea Ubuntu."""
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read()
            
            for line in content.split("\n"):
                if line.startswith("VERSION_ID="):
                    version = line.split("=")[1].strip('"')
                    is_correct = version.startswith("22.04")
                    return is_correct, version
        
        return False, "necunoscut"
    except Exception:
        return False, "necunoscut"


def verifica_portainer_ruleaza() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 9000))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
        return False


def verifica_versiune_python() -> tuple[bool, str]:
    """Verifică versiunea Python."""
    versiune = sys.version_info
    text_versiune = f"{versiune.major}.{versiune.minor}.{versiune.micro}"
    return versiune >= (3, 8), text_versiune


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def afiseaza_info_portainer() -> None:
    """Afișează informații despre cum să pornești Portainer."""
    print("\n  Cum să pornești Portainer:")
    print("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print("    -v portainer_data:/data portainer/portainer-ce:latest")
    print("\n  După pornire, accesează: http://localhost:9000")
    print("  Credențiale: stud / studstudstud")


def main():
    """Funcția principală de verificare a mediului."""
    print()
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 7")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare WSL2
    print("\033[1mMediul WSL2:\033[0m")
    v.verifica(
        "Rulare în WSL2",
        verifica_wsl2(),
        "Asigurați-vă că rulați în WSL2, nu nativ Linux sau WSL1"
    )
    
    ubuntu_ok, ubuntu_versiune = verifica_ubuntu_versiune()
    v.verifica(
        f"Ubuntu {ubuntu_versiune}",
        ubuntu_ok,
        "Instalați Ubuntu 22.04 ca distribuție WSL implicită"
    )

    # Verificare versiune Python
    print("\n\033[1mMediul Python:\033[0m")
    ok_python, versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py}",
        ok_python,
        "Instalați Python 3.8 sau mai recent: sudo apt install python3"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages", 
        "yaml": "pip install pyyaml --break-system-packages"
    }
    for nume_afisat, cmd_install in pachete_necesare.items():
        v.verifica(
            f"Pachet Python: {nume_afisat}",
            verifica_pachet_python(nume_afisat if nume_afisat != "yaml" else "yaml"),
            cmd_install
        )

    print("\n\033[1mMediul Docker:\033[0m")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    
    # Verificare Docker Compose
    try:
        rezultat_compose = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compose_ok = rezultat_compose.returncode == 0
    except Exception:
        compose_ok = False
    
    v.verifica(
        "Docker Compose instalat",
        compose_ok,
        "Instalați: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifica_docker_pornit()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            import time
            time.sleep(2)
            docker_ruleaza = verifica_docker_pornit()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon Docker pornit",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )

    # Portainer (Management Vizual)
    print("\n\033[1mPortainer (Management Vizual):\033[0m")
    if docker_ruleaza:
        portainer_ok = verifica_portainer_ruleaza()
        v.verifica(
            "Portainer rulează pe portul 9000",
            portainer_ok,
            "Portainer nu rulează. Vezi instrucțiunile de mai jos."
        )
        if not portainer_ok:
            afiseaza_info_portainer()
    else:
        v.avertizeaza("Portainer", "Nu se poate verifica - Docker nu rulează")

    print("\n\033[1mInstrumente de Rețea:\033[0m")
    # Verificare Wireshark
    wireshark_gasit = (
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe").exists() or
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil (Windows)",
        wireshark_gasit,
        "Instalați Wireshark de la wireshark.org"
    )

    print("\n\033[1mInstrumente Opționale:\033[0m")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("tshark"):
        v.verifica("tshark disponibil", True)
    else:
        v.avertizeaza("tshark", "Util pentru capturi din linia de comandă")

    if verifica_comanda("tcpdump"):
        v.verifica("tcpdump disponibil", True)
    else:
        v.avertizeaza("tcpdump", "Util pentru capturi în WSL")

    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:       http://localhost:9000")
    print(f"  • Server TCP Echo: localhost:9090")
    print(f"  • Receptor UDP:    localhost:9091")
    print(f"  • Filtru Pachete:  localhost:8888")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
