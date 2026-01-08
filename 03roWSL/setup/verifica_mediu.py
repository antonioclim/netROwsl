#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică că toate cerințele preliminare sunt instalate și configurate corect
pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.

Utilizare:
    python3 setup/verifica_mediu.py
"""

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Tuple


class Verificator:
    """Clasă pentru verificarea cerințelor de mediu."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sugestie_remediere: str = "") -> bool:
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            conditie: True dacă verificarea a trecut
            sugestie_remediere: Sugestie pentru remediere în caz de eșec
            
        Returns:
            Rezultatul verificării
        """
        if conditie:
            print(f"  [TRECUT] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT]  {nume}")
            if sugestie_remediere:
                print(f"           Remediere: {sugestie_remediere}")
            self.esuat += 1
        return conditie

    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [AVERT]  {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """
        Afișează sumarul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} trecute, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("✓ Mediul este pregătit pentru laborator!")
            return 0
        else:
            print("✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.")
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


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


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


def verifica_structura_proiect() -> bool:
    """Verifică că structura proiectului este completă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src/exercises",
        "tests",
        "docs",
        "homework",
        "pcap",
        "artifacts"
    ]
    
    for director in directoare_necesare:
        if not (radacina / director).exists():
            return False
    return True


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat (pe Windows, accesibil din WSL)."""
    wireshark_cai = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    return any(cale.exists() for cale in wireshark_cai)


def afiseaza_info_portainer() -> None:
    """Afișează informații despre cum să pornești Portainer."""
    print("\n  Cum să pornești Portainer:")
    print("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print("    -v portainer_data:/data portainer/portainer-ce:latest")
    print("\n  După pornire, accesează: http://localhost:9000")
    print("  Credențiale: stud / studstudstud")


def main():
    """Punctul principal de intrare."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 3")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
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
    print("\nMediu Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai nou: sudo apt install python3.11"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "yaml": "pip install pyyaml --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "docker": "pip install docker --break-system-packages"
    }
    
    for pachet, comanda in pachete_necesare.items():
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(pachet),
            comanda
        )

    # Verificare pachete Python pentru analiză rețea (opționale)
    print("\nPachete Analiză Rețea (opționale):")
    pachete_retea = {
        "scapy": "pip install scapy --break-system-packages",
        "dpkt": "pip install dpkt --break-system-packages",
    }
    
    for pachet, comanda in pachete_retea.items():
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet}", True)
        else:
            v.avertizeaza(pachet, f"Recomandat pentru analiză avansată. Instalare: {comanda}")

    print("\nMediu Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    
    # Verificare Docker Compose
    docker_compose_ok = False
    if verifica_comanda("docker"):
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            docker_compose_ok = rezultat.returncode == 0
        except Exception:
            pass
    
    v.verifica(
        "Docker Compose instalat",
        docker_compose_ok,
        "Instalați Docker Compose: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifica_docker_pornit()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            docker_ruleaza = verifica_docker_pornit()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon Docker pornit",
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

    print("\nInstrumente de Rețea:")
    v.verifica(
        "Wireshark disponibil (Windows)",
        verifica_wireshark(),
        "Instalați Wireshark de pe wireshark.org (pe Windows)"
    )

    print("\nStructură Proiect:")
    v.verifica(
        "Structura directorului completă",
        verifica_structura_proiect(),
        "Clonați repository-ul complet: git clone https://github.com/antonioclim/netROwsl.git"
    )

    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    vscode_paths = [
        Path("/mnt/c/Program Files/Microsoft VS Code/Code.exe"),
        Path("/mnt/c/Users") / os.environ.get("USER", "stud") / "AppData/Local/Programs/Microsoft VS Code/Code.exe"
    ]
    if any(p.exists() for p in vscode_paths) or verifica_comanda("code"):
        v.verifica("VS Code disponibil", True)
    else:
        v.avertizeaza("VS Code", "Recomandat ca editor de cod")

    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:      http://localhost:9000")
    print(f"  • Server Echo:    localhost:8080")
    print(f"  • Tunel TCP:      localhost:9090")
    print(f"  • Receiver UDP:   172.20.0.101:5007/5008 (profil broadcast)")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
