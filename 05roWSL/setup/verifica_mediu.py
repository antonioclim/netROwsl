#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
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
    """Clasă pentru verificarea cerințelor sistemului."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sugestie_reparare: str = ""):
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            conditie: True dacă verificarea a trecut
            sugestie_reparare: Sugestie pentru rezolvarea problemei
        """
        if conditie:
            print(f"  [\033[92mOK\033[0m] {nume}")
            self.reusit += 1
        else:
            print(f"  [\033[91mEȘUAT\033[0m] {nume}")
            if sugestie_reparare:
                print(f"         Reparare: {sugestie_reparare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """
        Afișează un avertisment.
        
        Args:
            nume: Numele verificării
            mesaj: Mesajul de avertizare
        """
        print(f"  [\033[93mATENȚIE\033[0m] {nume}: {mesaj}")
        self.avertismente += 1

    def rezumat(self) -> int:
        """
        Afișează rezumatul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("\033[92m✓ Mediul este pregătit pentru laborator!\033[0m")
            return 0
        else:
            print("\033[91m✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def verifica_comanda_disponibila(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
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


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def verifica_pachet_python(pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(pachet)
        return True
    except ImportError:
        return False


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este completă."""
    cale_curenta = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src",
        "tests",
        "docs",
        "homework"
    ]
    
    for director in directoare_necesare:
        if not (cale_curenta / director).exists():
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
    print("=" * 60)
    print("  Verificare Mediu pentru Laborator Săptămâna 5")
    print("  Rețele de Calculatoare – ASE, Informatică Economică")
    print("  Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verifică mediul WSL2
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

    # Verifică versiunea Python
    print("\n\033[1mMediul Python:\033[0m")
    versiune = verifica_versiune_python()
    v.verifica(
        f"Python {versiune[0]}.{versiune[1]}.{versiune[2]}",
        versiune >= (3, 8),
        "Instalați Python 3.8 sau mai nou: sudo apt install python3"
    )

    # Verifică pachetele Python necesare
    pachete_necesare = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "yaml": "pip install pyyaml --break-system-packages"
    }
    
    for pachet, comanda_instalare in pachete_necesare.items():
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet}", True)
        else:
            v.avertizeaza(f"Pachet Python: {pachet}", f"Opțional - {comanda_instalare}")

    # Verifică mediul Docker
    print("\n\033[1mMediul Docker:\033[0m")
    v.verifica(
        "Docker instalat",
        verifica_comanda_disponibila("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    
    # Verifică Docker Compose
    compuse_disponibil = False
    if verifica_comanda_disponibila("docker"):
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            compuse_disponibil = rezultat.returncode == 0
        except Exception:
            pass
    
    v.verifica(
        "Docker Compose instalat",
        compuse_disponibil,
        "Instalați Docker Compose: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifica_docker_activ()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            import time
            time.sleep(2)
            docker_ruleaza = verifica_docker_activ()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemonul Docker rulează",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )

    # Verifică Portainer (doar dacă Docker rulează)
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

    # Verifică instrumentele de rețea
    print("\n\033[1mInstrumente de Rețea:\033[0m")
    v.verifica(
        "Wireshark disponibil (Windows)",
        verifica_wireshark(),
        "Instalați Wireshark de pe wireshark.org (pe Windows)"
    )

    # Verifică instrumente opționale
    print("\n\033[1mInstrumente Opționale:\033[0m")
    if verifica_comanda_disponibila("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda_disponibila("code"):
        v.verifica("VS Code disponibil", True)
    else:
        v.avertizeaza("VS Code", "Recomandat pentru editarea codului")

    # Verifică structura proiectului
    print("\n\033[1mStructura Proiectului:\033[0m")
    v.verifica(
        "Structura directoarelor completă",
        verifica_structura_proiect(),
        "Asigurați-vă că ați dezarhivat complet kitul"
    )

    # Verifică fișierul docker-compose.yml
    cale_compose = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
    v.verifica(
        "Fișier docker-compose.yml prezent",
        cale_compose.exists(),
        "Fișierul docker-compose.yml lipsește din directorul docker/"
    )

    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:       http://localhost:9000")
    print(f"  • Container Python: 10.5.0.10")
    print(f"  • Server UDP:       10.5.0.20:9999")
    print(f"  • Client UDP:       10.5.0.30")
    print("-" * 60)

    return v.rezumat()


if __name__ == "__main__":
    sys.exit(main())
