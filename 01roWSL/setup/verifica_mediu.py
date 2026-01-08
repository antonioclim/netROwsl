#!/usr/bin/env python3
"""
Script de Verificare a Mediului de Lucru
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Optional, Tuple


class Verificator:
    """Clasă pentru verificarea cerințelor sistemului."""
    
    def __init__(self) -> None:
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sfat_rezolvare: str = "") -> None:
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [REUȘIT] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT]  {nume}")
            if sfat_rezolvare:
                print(f"           Soluție: {sfat_rezolvare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul verificărilor și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, "
              f"{self.avertismente} avertismente")
        if self.esuat == 0:
            print("✓ Mediul de lucru este pregătit!")
            return 0
        else:
            print("✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
    return shutil.which(cmd) is not None


def verifica_docker_ruleaza() -> bool:
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
        # Verifică dacă suntem în WSL
        if not os.path.exists("/proc/version"):
            return False
        
        with open("/proc/version", "r") as f:
            version_info = f.read().lower()
        
        # Verifică că este WSL (nu nativ Linux)
        if "microsoft" not in version_info and "wsl" not in version_info:
            return False
        
        # Verifică WSL2 vs WSL1
        # WSL2 are kernel Microsoft, WSL1 nu
        if "wsl2" in version_info:
            return True
        
        # Alternativ, verifică prin /proc/sys/fs/binfmt_misc
        # sau prezența /run/WSL
        return os.path.exists("/run/WSL") or "microsoft-standard" in version_info
        
    except Exception:
        return False


def verifica_ubuntu_versiune() -> Tuple[bool, str]:
    """Verifică versiunea Ubuntu."""
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read()
            
            # Extrage VERSION_ID
            for line in content.split("\n"):
                if line.startswith("VERSION_ID="):
                    version = line.split("=")[1].strip('"')
                    # Verifică dacă este 22.04
                    is_correct = version.startswith("22.04")
                    return is_correct, version
        
        # Fallback: folosește lsb_release
        rezultat = subprocess.run(
            ["lsb_release", "-rs"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            version = rezultat.stdout.strip()
            is_correct = version.startswith("22.04")
            return is_correct, version
        
        return False, "necunoscut"
    except Exception:
        return False, "necunoscut"


def verifica_versiune_python() -> tuple[int, int, int]:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


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
    """Verifică dacă Wireshark este instalat (pe Windows, accesibil din WSL)."""
    # Verifică în locații comune pe Windows (accesibile din WSL)
    cai_wireshark = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    return any(cale.exists() for cale in cai_wireshark)


def verifica_portainer_ruleaza() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        # Verifică dacă containerul Portainer există și rulează
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        # Verifică alternativ dacă portul 9000 răspunde
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


def afiseaza_info_portainer() -> None:
    """Afișează informații despre cum să pornești Portainer."""
    print("\n  Cum să pornești Portainer:")
    print("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print("    -v portainer_data:/data portainer/portainer-ce:latest")
    print("\n  După pornire, accesează: http://localhost:9000")
    print("  Credențiale: stud / studstudstud")


def main() -> int:
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificarea Mediului pentru Laboratorul Săptămânii 1")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare mediu WSL2
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
    major, minor, patch = verifica_versiune_python()
    v.verifica(
        f"Python {major}.{minor}.{patch}",
        (major, minor) >= (3, 11),
        "Instalați Python 3.11 sau mai recent: sudo apt install python3.11"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "yaml": "pip install pyyaml --break-system-packages",
    }
    
    for pachet, comanda_instalare in pachete_necesare.items():
        nume_import = "yaml" if pachet == "yaml" else pachet
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(nume_import),
            comanda_instalare
        )

    # Verificare pachete Python pentru analiză rețea (opționale dar recomandate)
    pachete_retea = {
        "scapy": "pip install scapy --break-system-packages",
        "dpkt": "pip install dpkt --break-system-packages",
    }
    
    print("\nPachete Analiză Rețea (opționale):")
    for pachet, comanda_instalare in pachete_retea.items():
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet}", True)
        else:
            v.avertizeaza(pachet, f"Recomandat pentru analiză avansată. Instalare: {comanda_instalare}")

    # Verificare Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    v.verifica(
        "Docker Compose instalat",
        verifica_docker_compose(),
        "Instalați Docker Compose: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifica_docker_ruleaza()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            docker_ruleaza = verifica_docker_ruleaza()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon-ul Docker rulează",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )

    # Verificare Portainer (doar dacă Docker rulează)
    print("\nPortainer (Management Vizual):")
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

    # Verificare instrumente de rețea
    print("\nInstrumente de Rețea:")
    v.verifica(
        "Wireshark disponibil (Windows)",
        verifica_wireshark(),
        "Instalați Wireshark de pe wireshark.org (pe Windows)"
    )

    # Verificare structura proiectului
    print("\nStructura Proiectului:")
    v.verifica(
        "Directoare necesare prezente",
        verifica_structura_proiect(),
        "Clonați repository-ul complet: git clone https://github.com/antonioclim/netROwsl.git"
    )

    # Verificări opționale
    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("code") or os.path.exists("/mnt/c/Users"):
        # Verifică VS Code în Windows
        vscode_paths = [
            Path("/mnt/c/Program Files/Microsoft VS Code/Code.exe"),
            Path("/mnt/c/Users") / os.environ.get("USER", "stud") / "AppData/Local/Programs/Microsoft VS Code/Code.exe"
        ]
        if any(p.exists() for p in vscode_paths) or verifica_comanda("code"):
            v.verifica("VS Code disponibil", True)
        else:
            v.avertizeaza("VS Code", "Recomandat pentru editarea codului")
    else:
        v.avertizeaza("VS Code", "Recomandat pentru editarea codului")

    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:     http://localhost:9000")
    print(f"  • Container Lab: docker exec -it week1_lab bash")
    print(f"  • Port TCP:      localhost:9090")
    print(f"  • Port UDP:      localhost:9091")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
