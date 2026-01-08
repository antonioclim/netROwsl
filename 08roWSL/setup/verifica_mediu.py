#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 8 în mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
"""

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Tuple

# Coduri ANSI pentru culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
RESETARE = "\033[0m"
BOLD = "\033[1m"

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"


class Verificator:
    """Clasă pentru gestionarea verificărilor de mediu."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_rezolvare: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  {VERDE}[OK]{RESETARE} {nume}")
            self.trecute += 1
        else:
            print(f"  {ROSU}[EROARE]{RESETARE} {nume}")
            if indicatie_rezolvare:
                print(f"           Rezolvare: {indicatie_rezolvare}")
            self.esuate += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  {GALBEN}[ATENȚIE]{RESETARE} {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul verificărilor."""
        print()
        print("=" * 60)
        print(f"Rezultate: {self.trecute} trecute, {self.esuate} eșuate, {self.avertismente} avertismente")
        if self.esuate == 0:
            print(f"\n{VERDE}✓ Mediul este pregătit pentru laboratorul Săptămânii 8!{RESETARE}")
            return 0
        else:
            print(f"\n{ROSU}✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.{RESETARE}")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
    return shutil.which(cmd) is not None


def verifica_docker_pornit() -> bool:
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


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil pentru utilizare."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            return True
    except OSError:
        return False


def verifica_port_in_uz(port: int) -> bool:
    """Verifică dacă un port este în uz (posibil de serviciile noastre)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(("127.0.0.1", port))
            return result == 0
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


def main():
    """Punctul principal de intrare."""
    print()
    print("=" * 60)
    print(f"{BOLD}Verificare Mediu pentru Laboratorul Săptămânii 8{RESETARE}")
    print("Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare WSL2
    print(f"{ALBASTRU}Mediul WSL2:{RESETARE}")
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
    print()
    print(f"{ALBASTRU}Mediul Python:{RESETARE}")
    py_version = sys.version_info
    v.verifica(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 8),
        "Instalați Python 3.8 sau ulterior: sudo apt install python3"
    )

    # Verificare pachete Python necesare
    pachete_necesare = [
        ("docker", "pip install docker --break-system-packages"),
        ("requests", "pip install requests --break-system-packages"),
        ("yaml", "pip install pyyaml --break-system-packages")
    ]
    
    for modul, cmd_install in pachete_necesare:
        try:
            __import__(modul)
            v.verifica(f"Pachet Python: {modul}", True)
        except ImportError:
            v.verifica(
                f"Pachet Python: {modul}", 
                False, 
                cmd_install
            )

    print()
    print(f"{ALBASTRU}Mediul Docker:{RESETARE}")
    v.verifica(
        "Docker instalat", 
        verifica_comanda("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    
    # Verificare Docker Compose V2
    compose_disponibil = False
    if verifica_comanda("docker"):
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compose_disponibil = result.returncode == 0
    
    v.verifica(
        "Docker Compose V2 disponibil", 
        compose_disponibil,
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
                print(f"  {VERDE}[INFO]{RESETARE} Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon-ul Docker rulează", 
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )

    # Portainer (Management Vizual)
    print()
    print(f"{ALBASTRU}Portainer (Management Vizual):{RESETARE}")
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

    print()
    print(f"{ALBASTRU}Instrumente de Rețea:{RESETARE}")
    
    # Verificare Wireshark
    wireshark_instalat = (
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe").exists() or
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil (Windows)",
        wireshark_instalat,
        "Instalați Wireshark de pe wireshark.org"
    )

    print()
    print(f"{ALBASTRU}Disponibilitate Porturi:{RESETARE}")
    
    porturi = [
        (8080, "nginx HTTP"),
        (8443, "nginx HTTPS")
    ]
    
    for port, serviciu in porturi:
        disponibil = verifica_port_disponibil(port)
        in_uz = verifica_port_in_uz(port)
        
        if disponibil:
            v.verifica(f"Port {port} ({serviciu}) disponibil", True)
        elif in_uz:
            # Portul este în uz - ar putea fi serviciile noastre
            v.avertizeaza(
                f"Port {port} ({serviciu})", 
                "În uz - verificați dacă sunt serviciile laboratorului"
            )
        else:
            v.verifica(
                f"Port {port} ({serviciu}) disponibil", 
                False,
                f"Eliberați portul {port} sau modificați configurația"
            )

    print()
    print(f"{ALBASTRU}Structura Directoarelor:{RESETARE}")
    
    # Verificare structură proiect
    radacina_proiect = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src",
        "www"
    ]
    
    toate_exista = True
    for director in directoare_necesare:
        cale = radacina_proiect / director
        if not cale.is_dir():
            v.verifica(f"Director: {director}/", False, f"Creați directorul {director}")
            toate_exista = False
    
    if toate_exista:
        v.verifica("Toate directoarele necesare prezente", True)

    print()
    print(f"{ALBASTRU}Instrumente Opționale:{RESETARE}")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")
    
    if verifica_comanda("curl"):
        v.verifica("curl disponibil", True)
    else:
        v.avertizeaza("curl", "Util pentru testarea HTTP")

    # Afișare informații de acces
    print()
    print("-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:       {PORTAINER_URL}")
    print(f"  • Proxy HTTP:      http://localhost:8080")
    print(f"  • Proxy HTTPS:     https://localhost:8443")
    print(f"  • Backend 1:       172.28.8.21:8080 (intern)")
    print(f"  • Backend 2:       172.28.8.22:8080 (intern)")
    print(f"  • Backend 3:       172.28.8.23:8080 (intern)")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
