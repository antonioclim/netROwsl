#!/usr/bin/env python3
"""
Script de Verificare a Mediului de Lucru
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 10 în mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
"""

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Tuple


# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"


class Verificator:
    """Clasa pentru verificarea cerințelor de mediu."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_remediere: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  \033[92m[✓ OK]\033[0m {nume}")
            self.reusit += 1
        else:
            print(f"  \033[91m[✗ EȘUAT]\033[0m {nume}")
            if indicatie_remediere:
                print(f"          Remediere: {indicatie_remediere}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  \033[93m[⚠ ATENȚIE]\033[0m {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul verificărilor și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} trecute, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("\n\033[92m✓ Mediul de lucru este pregătit pentru laboratorul Săptămânii 10!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
    return shutil.which(cmd) is not None


def verifica_docker_activ() -> bool:
    """Verifică dacă daemonul Docker rulează."""
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
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "Up" in result.stdout:
            return True
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', PORTAINER_PORT))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
        return False


def afiseaza_info_portainer() -> None:
    """Afișează informații despre cum să pornești Portainer."""
    print()
    print("  Cum să pornești Portainer:")
    print("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print("    -v portainer_data:/data portainer/portainer-ce:latest")
    print()
    print(f"  După pornire, accesează: {PORTAINER_URL}")
    print("  Credențiale: stud / studstudstud")


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info


def verifica_docker_compose() -> bool:
    """Verifică dacă Docker Compose este disponibil."""
    try:
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat."""
    cai_posibile = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    return any(cale.exists() for cale in cai_posibile) or verifica_comanda("wireshark")


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este corectă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = ["docker", "scripts", "src", "tests", "docs"]
    return all((radacina / d).exists() for d in directoare_necesare)


def verifica_porturi_disponibile() -> dict:
    """Verifică disponibilitatea porturilor necesare."""
    porturi = {
        8000: "Server Web HTTP",
        5353: "Server DNS",
        2222: "Server SSH",
        2121: "Server FTP",
    }
    
    rezultate = {}
    for port, descriere in porturi.items():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.bind(("localhost", port))
                rezultate[port] = (True, descriere)
        except OSError:
            rezultate[port] = (False, descriere)
    
    return rezultate


def main():
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 10")
    print("Laborator Rețele de Calculatoare - ASE, Informatică Economică")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare WSL2
    print("Mediul WSL2:")
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
    print("\nMediul Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 8),
        "Instalați Python 3.8 sau mai recent: sudo apt install python3"
    )

    # Verificare pachete Python necesare
    pachete_necesare = [
        ("docker", "pip install docker --break-system-packages"),
        ("requests", "pip install requests --break-system-packages"),
        ("yaml", "pip install pyyaml --break-system-packages"),
        ("flask", "pip install flask --break-system-packages"),
        ("paramiko", "pip install paramiko --break-system-packages"),
    ]
    
    for modul, remediere in pachete_necesare:
        v.verifica(
            f"Pachet Python: {modul}",
            verifica_pachet_python(modul),
            remediere
        )

    # Verificare mediu Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    v.verifica(
        "Docker Compose instalat",
        verifica_docker_compose(),
        "Instalați: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifica_docker_activ()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            import time
            time.sleep(2)
            docker_ruleaza = verifica_docker_activ()
            if docker_ruleaza:
                print(f"  \033[92m[INFO]\033[0m Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon Docker activ",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )

    # Portainer (Management Vizual)
    print("\nPortainer (Management Vizual):")
    if docker_ruleaza:
        portainer_ok = verifica_portainer_ruleaza()
        v.verifica(
            f"Portainer rulează pe portul {PORTAINER_PORT}",
            portainer_ok,
            "Portainer nu rulează. Vezi instrucțiunile de mai jos."
        )
        if not portainer_ok:
            afiseaza_info_portainer()
    else:
        v.avertizeaza("Portainer", "Nu se poate verifica - Docker nu rulează")

    # Verificare instrumente de rețea
    print("\nInstrumente de Rețea:")
    v.verifica(
        "Wireshark disponibil (Windows)",
        verifica_wireshark(),
        "Instalați Wireshark de pe wireshark.org"
    )

    # Verificare structură proiect
    print("\nStructura Proiectului:")
    v.verifica(
        "Directoare necesare prezente",
        verifica_structura_proiect(),
        "Verificați că ați extras corect arhiva"
    )

    # Verificare porturi disponibile
    print("\nDisponibilitatea Porturilor:")
    stare_porturi = verifica_porturi_disponibile()
    for port, (disponibil, descriere) in stare_porturi.items():
        if disponibil:
            v.verifica(f"Port {port} ({descriere})", True)
        else:
            v.avertizeaza(
                f"Port {port} ({descriere})",
                f"Portul este ocupat - opriți serviciul care îl folosește"
            )

    # Instrumente opționale
    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("curl"):
        v.verifica("curl instalat", True)
    else:
        v.avertizeaza("curl", "Util pentru testarea HTTP")

    if verifica_comanda("dig"):
        v.verifica("dig instalat", True)
    else:
        v.avertizeaza("dig", "Util pentru testarea DNS (apt install dnsutils)")

    # Afișare informații de acces
    print()
    print("-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:        {PORTAINER_URL}")
    print(f"  • Server Web:       http://localhost:8000")
    print(f"  • Server DNS:       localhost:5353/udp")
    print(f"  • Server SSH:       localhost:2222 (labuser/labpass)")
    print(f"  • Server FTP:       localhost:2121 (labftp/labftp)")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
