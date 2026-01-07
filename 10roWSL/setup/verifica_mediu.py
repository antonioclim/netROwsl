#!/usr/bin/env python3
"""
Script de Verificare a Mediului de Lucru
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
from pathlib import Path


class Verificator:
    """Clasa pentru verificarea cerințelor de mediu."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_remediere: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [TRECUT] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT] {nume}")
            if indicatie_remediere:
                print(f"          Remediere: {indicatie_remediere}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul verificărilor și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} trecute, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("✓ Mediul de lucru este pregătit!")
            return 0
        else:
            print("✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.")
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


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil și activ."""
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        iesire = rezultat.stdout.decode() + rezultat.stderr.decode()
        return "WSL 2" in iesire or "Default Version: 2" in iesire
    except Exception:
        return False


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
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    return any(cale.exists() for cale in cai_posibile) or verifica_comanda("wireshark")


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este corectă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = ["docker", "scripts", "src", "tests", "docs"]
    return all((radacina / d).exists() for d in directoare_necesare)


def verifica_porturi_disponibile() -> dict:
    """Verifică disponibilitatea porturilor necesare."""
    import socket
    
    porturi = {
        8000: "Server Web HTTP",
        5353: "Server DNS",
        2222: "Server SSH",
        2121: "Server FTP",
        9443: "Portainer",
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
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau o versiune ulterioară de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "docker",
        "requests": "requests",
        "yaml": "pyyaml",
        "flask": "flask",
        "paramiko": "paramiko",
        "dnslib": "dnslib",
        "pyftpdlib": "pyftpdlib",
    }
    
    for modul, pachet in pachete_necesare.items():
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(modul),
            f"pip install {pachet}"
        )

    # Verificare mediu Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    v.verifica(
        "Docker Compose instalat",
        verifica_docker_compose(),
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    v.verifica(
        "Daemon Docker activ",
        verifica_docker_activ(),
        "Porniți aplicația Docker Desktop"
    )

    # Verificare WSL2
    print("\nMediul WSL2:")
    v.verifica(
        "WSL2 disponibil",
        verifica_wsl2(),
        "Activați WSL2: wsl --install"
    )

    # Verificare instrumente de rețea
    print("\nInstrumente de Rețea:")
    v.verifica(
        "Wireshark disponibil",
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

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
