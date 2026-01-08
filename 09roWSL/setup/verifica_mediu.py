#!/usr/bin/env python3
"""
Script Verificare Mediu
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate
și configurate corect pentru laboratorul Săptămânii 9 în mediul 
WSL2 + Ubuntu 22.04 + Docker + Portainer.
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
    """
    Clasă pentru verificarea cerințelor preliminare.
    
    Atribute:
        reușite: Numărul de verificări reușite
        eșuate: Numărul de verificări eșuate
        avertismente: Numărul de avertismente
    """
    
    def __init__(self):
        """Inițializează contoarele."""
        self.reușite = 0
        self.eșuate = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_remediere: str = "") -> None:
        """
        Verifică o condiție și raportează rezultatul.
        
        Argumente:
            nume: Descrierea verificării
            conditie: True dacă verificarea a trecut
            indicatie_remediere: Sugestie pentru remediere dacă a eșuat
        """
        if conditie:
            print(f"  \033[92m[✓ OK]\033[0m {nume}")
            self.reușite += 1
        else:
            print(f"  \033[91m[✗ EȘUAT]\033[0m {nume}")
            if indicatie_remediere:
                print(f"         Remediere: {indicatie_remediere}")
            self.eșuate += 1

    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """
        Emite un avertisment.
        
        Argumente:
            nume: Descrierea elementului
            mesaj: Mesajul de avertizare
        """
        print(f"  \033[93m[⚠ ATENȚIE]\033[0m {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """
        Afișează sumarul verificărilor.
        
        Returnează:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reușite} reușite, {self.eșuate} eșuate, {self.avertismente} avertismente")
        
        if self.eșuate == 0:
            print("\n\033[92m✓ Mediul este pregătit pentru laboratorul Săptămânii 9!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.\033[0m")
            return 1


def verifica_comanda(comanda: str) -> bool:
    """Verifică dacă o comandă este disponibilă."""
    return shutil.which(comanda) is not None


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


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def main():
    """Funcția principală."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 9")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
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
        f"Python {versiune_py[0]}.{versiune_py[1]}.{versiune_py[2]}",
        versiune_py >= (3, 8),
        "Instalați Python 3.8 sau mai recent: sudo apt install python3"
    )

    # Verificare pachete Python necesare (module standard)
    pachete_necesare = ["struct", "socket", "zlib"]
    for pachet in pachete_necesare:
        try:
            __import__(pachet)
            v.verifica(f"Modul Python: {pachet}", True)
        except ImportError:
            v.verifica(f"Modul Python: {pachet}", False, f"Modul standard lipsă")

    # Verificare pachete opționale
    pachete_optionale = [
        ("docker", "pip install docker --break-system-packages"),
        ("yaml", "pip install pyyaml --break-system-packages"),
        ("requests", "pip install requests --break-system-packages")
    ]
    for pachet, cmd_install in pachete_optionale:
        try:
            __import__(pachet)
            v.verifica(f"Pachet Python: {pachet}", True)
        except ImportError:
            v.verifica(
                f"Pachet Python: {pachet}",
                False,
                cmd_install
            )

    # Verificare Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
    )
    
    # Verifică Docker Compose
    compose_v2 = False
    compose_v1 = False
    
    try:
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compose_v2 = rezultat.returncode == 0
    except Exception:
        pass
    
    if not compose_v2:
        try:
            rezultat = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True
            )
            compose_v1 = rezultat.returncode == 0
        except Exception:
            pass
    
    v.verifica(
        "Docker Compose instalat",
        compose_v2 or compose_v1,
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
    
    # Wireshark
    wireshark_gasit = (
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe").exists() or
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil (Windows)",
        wireshark_gasit,
        "Instalați Wireshark de pe wireshark.org"
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
        v.avertizeaza("curl", "Util pentru testarea HTTP/FTP")

    # Verificare structură proiect
    print("\nStructura Proiectului:")
    fisiere_necesare = [
        "docker/docker-compose.yml",
        "scripts/porneste_lab.py",
        "src/exercises/ex_9_01_endianness.py",
    ]
    
    radacina_proiect = Path(__file__).parent.parent
    
    for cale_fisier in fisiere_necesare:
        cale_completa = radacina_proiect / cale_fisier
        v.verifica(
            f"Fișier: {cale_fisier}",
            cale_completa.exists(),
            f"Fișierul lipsește: {cale_completa}"
        )

    # Afișare informații de acces
    print()
    print("-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:        {PORTAINER_URL}")
    print(f"  • Server FTP:       ftp://localhost:2121")
    print(f"  • Credențiale FTP:  test / 12345")
    print(f"  • Porturi passive:  60000-60010")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
