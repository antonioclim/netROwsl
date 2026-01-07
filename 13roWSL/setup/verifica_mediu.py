#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
from pathlib import Path


class Verificator:
    """Clasă pentru verificarea cerințelor de mediu."""

    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indiciu_remediere: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [TRECUT] {nume}")
            self.trecute += 1
        else:
            print(f"  [EȘUAT]  {nume}")
            if indiciu_remediere:
                print(f"           Remediere: {indiciu_remediere}")
            self.esuate += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.trecute} trecute, {self.esuate} eșuate, {self.avertismente} avertismente")
        if self.esuate == 0:
            print("✓ Mediul este pregătit!")
            return 0
        else:
            print("✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.")
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


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil și configurat."""
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


def main():
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 13")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai nou de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "docker",
        "requests": "requests",
        "yaml": "pyyaml",
        "paho.mqtt": "paho-mqtt",
        "scapy": "scapy"
    }
    
    for modul, pachet in pachete_necesare.items():
        try:
            __import__(modul.split('.')[0])
            v.verifica(f"Pachet Python: {pachet}", True)
        except ImportError:
            v.verifica(f"Pachet Python: {pachet}", False, f"pip install {pachet}")

    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    
    # Verificare Docker Compose
    docker_compose_ok = False
    if verifica_comanda("docker"):
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        docker_compose_ok = rezultat.returncode == 0
    
    v.verifica(
        "Docker Compose instalat",
        docker_compose_ok,
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    v.verifica(
        "Daemon Docker activ",
        verifica_docker_activ(),
        "Porniți aplicația Docker Desktop"
    )

    print("\nMediul WSL2:")
    v.verifica(
        "WSL2 disponibil",
        verifica_wsl2(),
        "Activați WSL2: wsl --install"
    )

    print("\nInstrumente de Rețea:")
    wireshark_gasit = (
        Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil",
        wireshark_gasit,
        "Instalați Wireshark de pe wireshark.org"
    )

    print("\nStructura Proiectului:")
    v.verifica(
        "Structură directoare corectă",
        verifica_structura_proiect(),
        "Verificați că arhiva a fost extrasă corect"
    )

    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("code"):
        v.verifica("VS Code disponibil", True)
    else:
        v.avertizeaza("VS Code", "Recomandat pentru editarea codului")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
