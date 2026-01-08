#!/usr/bin/env python3
"""
Script de Verificare Mediu
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.

Utilizare:
    python3 setup/verify_environment.py
"""

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Tuple


class Verificator:
    """Clasă pentru verificarea componentelor mediului."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sugestie: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [\033[92mOK\033[0m] {nume}")
            self.reusit += 1
        else:
            print(f"  [\033[91mERORE\033[0m] {nume}")
            if sugestie:
                print(f"         Remediere: {sugestie}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  [\033[93mATENȚIE\033[0m] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("\033[92m✓ Mediul este pregătit pentru laborator!\033[0m")
            return 0
        else:
            print("\033[91m✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
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


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            rezultat = s.connect_ex(('localhost', port))
            return rezultat != 0  # Port disponibil dacă conexiunea eșuează
    except Exception:
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
    """Funcția principală."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămâna 4")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare mediu WSL2
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
    print("\n\033[1mMediu Python:\033[0m")
    versiune_py = sys.version_info
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 8),
        "Instalați Python 3.8 sau mai nou: sudo apt install python3"
    )

    # Verificare pachete Python necesare (standard library)
    pachete_standard = ["struct", "socket", "threading", "binascii"]
    for pachet in pachete_standard:
        try:
            __import__(pachet)
            v.verifica(f"Modul Python: {pachet}", True)
        except ImportError:
            v.verifica(f"Modul Python: {pachet}", False, f"Modul standard lipsă")

    # Verificare pachete opționale
    print("\n\033[1mPachete Opționale:\033[0m")
    pachete_optionale = [
        ("docker", "pip install docker --break-system-packages"), 
        ("yaml", "pip install pyyaml --break-system-packages"),
        ("requests", "pip install requests --break-system-packages")
    ]
    for pachet, instalare in pachete_optionale:
        try:
            __import__(pachet)
            v.verifica(f"Pachet Python: {pachet}", True)
        except ImportError:
            v.avertizeaza(f"Pachet Python: {pachet}", f"Opțional - {instalare}")

    # Verificare mediu Docker
    print("\n\033[1mMediu Docker:\033[0m")
    v.verifica("Docker instalat", verifica_comanda("docker"), 
               "Instalați Docker în WSL: sudo apt install docker.io")
    
    docker_compose_ok = False
    if verifica_comanda("docker"):
        try:
            rezultat = subprocess.run(["docker", "compose", "version"], 
                                      capture_output=True,
                                      timeout=10)
            docker_compose_ok = rezultat.returncode == 0
        except Exception:
            pass
    v.verifica("Docker Compose instalat", docker_compose_ok,
               "Instalați Docker Compose: sudo apt install docker-compose-plugin")
    
    docker_ruleaza = verifica_docker_activ()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            docker_ruleaza = verifica_docker_activ()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifica("Daemon Docker activ", docker_ruleaza,
               "Porniți Docker: sudo service docker start")

    # Verificare Portainer (doar dacă Docker rulează)
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

    # Verificare instrumente rețea
    print("\n\033[1mInstrumente Rețea:\033[0m")
    v.verifica("Wireshark disponibil (Windows)", 
               verifica_wireshark(),
               "Instalați Wireshark de pe wireshark.org (pe Windows)")

    # Verificare disponibilitate porturi
    print("\n\033[1mDisponibilitate Porturi:\033[0m")
    porturi = [
        (5400, "Protocol TEXT"),
        (5401, "Protocol BINAR"),
        (5402, "Senzor UDP"),
        (9000, "Portainer (global)")
    ]
    for port, descriere in porturi:
        if port == 9000:
            # Portainer ar trebui să fie activ, nu disponibil
            if verifica_portainer_ruleaza():
                v.verifica(f"Port {port} ({descriere})", True)
            else:
                v.avertizeaza(f"Port {port}", f"Portainer nu rulează")
        else:
            disponibil = verifica_port_disponibil(port)
            if disponibil:
                v.verifica(f"Port {port} ({descriere})", True)
            else:
                v.avertizeaza(f"Port {port}", f"În uz - {descriere} ar putea să nu pornească")

    # Verificare instrumente opționale
    print("\n\033[1mInstrumente Opționale:\033[0m")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("nc") or verifica_comanda("netcat"):
        v.verifica("Netcat disponibil", True)
    else:
        v.avertizeaza("Netcat", "Util pentru testarea protocoalelor")

    # Verificare structură proiect
    print("\n\033[1mStructură Proiect:\033[0m")
    radacina_proiect = Path(__file__).parent.parent
    directoare_necesare = ["src", "scripts", "docker", "tests", "docs", "homework"]
    for director in directoare_necesare:
        cale = radacina_proiect / director
        v.verifica(f"Director {director}/", cale.is_dir())

    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:       http://localhost:9000")
    print(f"  • Protocol TEXT:   localhost:5400")
    print(f"  • Protocol BINAR:  localhost:5401")
    print(f"  • Senzor UDP:      localhost:5402")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
