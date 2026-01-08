#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 14 în mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
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


class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'


class Verificator:
    """Clasă pentru verificarea cerințelor de mediu."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0
    
    def verifica(self, nume: str, conditie: bool, indicatie: str = "") -> None:
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  {Culori.VERDE}[✓ OK]{Culori.FINAL} {nume}")
            self.reusit += 1
        else:
            print(f"  {Culori.ROSU}[✗ EȘUAT]{Culori.FINAL} {nume}")
            if indicatie:
                print(f"           Rezolvare: {indicatie}")
            self.esuat += 1
    
    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  {Culori.GALBEN}[⚠ ATENȚIE]{Culori.FINAL} {nume}: {mesaj}")
        self.avertismente += 1
    
    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
        print(f"Rezultate: {self.reusit} trecute, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print(f"\n{Culori.VERDE}✓ Mediul este pregătit pentru laboratorul Săptămânii 14!{Culori.FINAL}")
            return 0
        else:
            print(f"\n{Culori.ROSU}✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.{Culori.FINAL}")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
    return shutil.which(cmd) is not None


def verifica_docker_activ() -> bool:
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
    return sys.version_info


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat."""
    # Verifică calea standard pe Windows (din WSL)
    cai_posibile = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    return any(cale.exists() for cale in cai_posibile) or verifica_comanda("wireshark")


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este corectă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src/exercises",
        "tests"
    ]
    for director in directoare_necesare:
        if not (radacina / director).exists():
            return False
    return True


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil (nu e utilizat)."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        sock.close()
        # result == 0 means port is in use (connection succeeded)
        # result != 0 means port is available
        return result != 0
    except Exception:
        return True


def main():
    """Funcția principală de verificare."""
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Verificarea Mediului - Laboratorul Săptămânii 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Recapitulare Integrată și Evaluare Proiect{Culori.FINAL}")
    print(f"{Culori.CYAN}Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    v = Verificator()
    
    # Verificare WSL2
    print(f"{Culori.BOLD}Mediul WSL2:{Culori.FINAL}")
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
    print(f"\n{Culori.BOLD}Mediul Python:{Culori.FINAL}")
    ver = verifica_versiune_python()
    v.verifica(
        f"Python {ver.major}.{ver.minor}.{ver.micro}",
        ver >= (3, 8),
        "Instalați Python 3.8 sau mai recent: sudo apt install python3"
    )
    
    # Verificare pachete Python necesare
    print(f"\n{Culori.BOLD}Pachete Python:{Culori.FINAL}")
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
    
    # Verificare mediu Docker
    print(f"\n{Culori.BOLD}Mediul Docker:{Culori.FINAL}")
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
        print(f"  {Culori.CYAN}[INFO]{Culori.FINAL} Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            import time
            time.sleep(2)
            docker_ruleaza = verifica_docker_activ()
            if docker_ruleaza:
                print(f"  {Culori.VERDE}[INFO]{Culori.FINAL} Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon Docker activ",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )
    
    # Portainer (Management Vizual)
    print(f"\n{Culori.BOLD}Portainer (Management Vizual):{Culori.FINAL}")
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
    print(f"\n{Culori.BOLD}Instrumente de Rețea:{Culori.FINAL}")
    v.verifica(
        "Wireshark disponibil (Windows)",
        verifica_wireshark(),
        "Instalați Wireshark de pe wireshark.org"
    )
    
    if verifica_comanda("curl"):
        v.verifica("curl instalat", True)
    else:
        v.avertizeaza("curl", "Instalați cu: sudo apt install curl")
    
    if verifica_comanda("nc") or verifica_comanda("netcat"):
        v.verifica("netcat (nc) instalat", True)
    else:
        v.avertizeaza("netcat", "Instalați cu: sudo apt install netcat")
    
    # Verificare structură proiect
    print(f"\n{Culori.BOLD}Structura Proiectului:{Culori.FINAL}")
    v.verifica(
        "Structură directoare corectă",
        verifica_structura_proiect(),
        "Verificați că arhiva a fost extrasă corect"
    )
    
    # Verificare disponibilitate porturi
    # NOTĂ: Portul 9000 ar trebui să fie utilizat de Portainer!
    #       Echo server folosește portul 9090
    print(f"\n{Culori.BOLD}Disponibilitate Porturi:{Culori.FINAL}")
    porturi_lab = [
        (8080, "Load Balancer"),
        (8001, "Backend 1"),
        (8002, "Backend 2"),
        (9090, "Echo Server")
    ]
    for port, serviciu in porturi_lab:
        if verifica_port_disponibil(port):
            v.verifica(f"Port {port} ({serviciu})", True)
        else:
            v.avertizeaza(f"Port {port} ({serviciu})", f"utilizat - verificați cu: sudo ss -tlnp | grep {port}")
    
    # Verifică portul 9000 - ar trebui să fie utilizat de Portainer
    if not verifica_port_disponibil(9000):
        # Port 9000 is in use, which is good if it's Portainer
        if verifica_portainer_ruleaza():
            v.verifica("Port 9000 (Portainer)", True)
        else:
            v.avertizeaza("Port 9000", "utilizat dar nu de Portainer - poate fi conflict!")
    else:
        v.avertizeaza("Port 9000 (Portainer)", "liber - Portainer ar trebui să ruleze aici")
    
    # Instrumente opționale
    print(f"\n{Culori.BOLD}Instrumente Opționale:{Culori.FINAL}")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")
    
    # Afișare informații de acces
    print()
    print(f"{Culori.BOLD}{'-' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Puncte de Acces:{Culori.FINAL}")
    print(f"  • Portainer:       {PORTAINER_URL}")
    print(f"  • Load Balancer:   http://localhost:8080")
    print(f"  • Backend App 1:   http://localhost:8001")
    print(f"  • Backend App 2:   http://localhost:8002")
    print(f"  • Echo Server:     tcp://localhost:9090")
    print(f"{Culori.BOLD}{'-' * 60}{Culori.FINAL}")
    
    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
