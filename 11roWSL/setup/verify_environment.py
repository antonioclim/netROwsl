#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 11 în mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
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
    """Clasă pentru verificarea cerințelor preliminare."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0
    
    def verifica(self, nume: str, conditie: bool, indiciu_remediere: str = "") -> None:
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            conditie: Rezultatul verificării (True/False)
            indiciu_remediere: Mesaj de ajutor dacă verificarea eșuează
        """
        if conditie:
            print(f"  \033[92m[✓ OK]\033[0m {nume}")
            self.trecute += 1
        else:
            print(f"  \033[91m[✗ EȘUAT]\033[0m {nume}")
            if indiciu_remediere:
                print(f"          Remediere: {indiciu_remediere}")
            self.esuate += 1
    
    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  \033[93m[⚠ ATENȚIE]\033[0m {nume}: {mesaj}")
        self.avertismente += 1
    
    def sumar(self) -> int:
        """
        Afișează sumarul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.trecute} trecute, {self.esuate} eșuate, {self.avertismente} avertismente")
        if self.esuate == 0:
            print("\n\033[92m✓ Mediul este pregătit pentru laboratorul Săptămânii 11!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Vă rugăm remediați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
    return shutil.which(cmd) is not None


def verifica_docker_ruleaza() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def porneste_docker() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    try:
        result = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        return result.returncode == 0
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


def verifica_docker_compose() -> bool:
    """Verifică dacă Docker Compose este disponibil."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


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


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat."""
    # Verifică calea standard pe Windows (din WSL)
    cai_posibile = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    return any(cale.exists() for cale in cai_posibile) or verifica_comanda("wireshark")


def main():
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 11")
    print("Laborator Rețele de Calculatoare — ASE, Informatică Economică")
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
    print("\nMediu Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py[0]}.{versiune_py[1]}.{versiune_py[2]}",
        versiune_py >= (3, 8),
        "Instalați Python 3.8 sau mai recent: sudo apt install python3"
    )

    # Verificare pachete Python necesare
    pachete_necesare = [
        ("requests", "pip install requests --break-system-packages"),
        ("yaml", "pip install pyyaml --break-system-packages"),
    ]
    for modul, remediere in pachete_necesare:
        v.verifica(
            f"Pachet Python: {modul}",
            verifica_pachet_python(modul),
            remediere
        )

    # Verificare pachete opționale
    print("\nPachete Opționale:")
    pachete_optionale = {
        "dnspython": "pip install dnspython --break-system-packages",
        "paramiko": "pip install paramiko --break-system-packages",
        "pyftpdlib": "pip install pyftpdlib --break-system-packages",
    }
    for pachet, comanda in pachete_optionale.items():
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet}", True)
        else:
            v.avertizeaza(f"Pachet Python: {pachet}", f"Opțional, instalați cu: {comanda}")

    # Verificare mediu Docker
    print("\nMediu Docker:")
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
    
    docker_ruleaza = verifica_docker_ruleaza()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            import time
            time.sleep(2)
            docker_ruleaza = verifica_docker_ruleaza()
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
    
    if verifica_comanda("curl"):
        v.verifica("curl instalat", True)
    else:
        v.avertizeaza("curl", "Recomandat pentru testare HTTP")

    # Verificare disponibilitate porturi
    print("\nDisponibilitate Porturi:")
    porturi = [8080, 8081, 8082, 8083]
    for port in porturi:
        disponibil = verifica_port_disponibil(port)
        if disponibil:
            v.verifica(f"Port {port} disponibil", True)
        else:
            v.avertizeaza(f"Port {port}", f"Portul este ocupat - unele exerciții pot necesita modificări")

    # Verificare structură directoare
    print("\nStructură Directoare:")
    directoare_necesare = ["docker", "scripts", "src", "tests"]
    cale_radacina = Path(__file__).parent.parent
    for director in directoare_necesare:
        cale = cale_radacina / director
        v.verifica(
            f"Director '{director}/' există",
            cale.exists(),
            f"Creați directorul: mkdir {director}"
        )

    # Verificare instrumente opționale
    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru control versiuni")

    # Afișare informații de acces
    print()
    print("-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:              {PORTAINER_URL}")
    print(f"  • Echilibror de sarcină:  http://localhost:8080")
    print(f"  • Verificare stare:       http://localhost:8080/health")
    print(f"  • Status Nginx:           http://localhost:8080/nginx_status")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
