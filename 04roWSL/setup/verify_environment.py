#!/usr/bin/env python3
"""
Script de Verificare Mediu
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
from pathlib import Path


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
        print("\n" + "=" * 50)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("\033[92mMediul este pregătit!\033[0m")
            return 0
        else:
            print("\033[91mVă rugăm să remediați problemele de mai sus înainte de a continua.\033[0m")
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


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil."""
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = rezultat.stdout.decode() + rezultat.stderr.decode()
        return "WSL 2" in output or "Default Version: 2" in output
    except Exception:
        return False


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            rezultat = s.connect_ex(('localhost', port))
            return rezultat != 0  # Port disponibil dacă conexiunea eșuează
    except Exception:
        return True


def main():
    """Funcția principală."""
    print("=" * 50)
    print("Verificare Mediu pentru Laboratorul Săptămâna 4")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 50)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("\033[1mMediu Python:\033[0m")
    versiune_py = sys.version_info
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 8),
        "Instalați Python 3.8 sau mai nou de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = ["struct", "socket", "threading", "binascii"]
    for pachet in pachete_necesare:
        try:
            __import__(pachet)
            v.verifica(f"Modul Python: {pachet}", True)
        except ImportError:
            v.verifica(f"Modul Python: {pachet}", False, f"Modul standard lipsă")

    # Verificare pachete opționale
    print("\n\033[1mPachete Opționale:\033[0m")
    pachete_optionale = [("docker", "pip install docker"), 
                         ("yaml", "pip install pyyaml"),
                         ("requests", "pip install requests")]
    for pachet, instalare in pachete_optionale:
        try:
            __import__(pachet)
            v.verifica(f"Pachet Python: {pachet}", True)
        except ImportError:
            v.avertizeaza(f"Pachet Python: {pachet}", f"Opțional - {instalare}")

    # Verificare mediu Docker
    print("\n\033[1mMediu Docker:\033[0m")
    v.verifica("Docker instalat", verifica_comanda("docker"), 
               "Instalați Docker Desktop de pe docker.com")
    
    docker_compose_ok = False
    if verifica_comanda("docker"):
        rezultat = subprocess.run(["docker", "compose", "version"], 
                                  capture_output=True)
        docker_compose_ok = rezultat.returncode == 0
    v.verifica("Docker Compose instalat", docker_compose_ok,
               "Docker Compose ar trebui să vină cu Docker Desktop")
    v.verifica("Daemon Docker activ", verifica_docker_activ(),
               "Porniți aplicația Docker Desktop")

    # Verificare mediu WSL2
    print("\n\033[1mMediu WSL2:\033[0m")
    v.verifica("WSL2 disponibil", verifica_wsl2(),
               "Activați WSL2: wsl --install")

    # Verificare instrumente rețea
    print("\n\033[1mInstrumente Rețea:\033[0m")
    cale_wireshark = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    v.verifica("Wireshark disponibil", 
               cale_wireshark.exists() or verifica_comanda("wireshark"),
               "Instalați Wireshark de pe wireshark.org")

    # Verificare disponibilitate porturi
    print("\n\033[1mDisponibilitate Porturi:\033[0m")
    porturi = [
        (5400, "Protocol TEXT"),
        (5401, "Protocol BINAR"),
        (5402, "Senzor UDP"),
        (9443, "Portainer")
    ]
    for port, descriere in porturi:
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
    directoare_necesare = ["src", "scripts", "docker", "tests"]
    for director in directoare_necesare:
        cale = radacina_proiect / director
        v.verifica(f"Director {director}/", cale.is_dir())

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
