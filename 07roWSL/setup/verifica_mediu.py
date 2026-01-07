#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică că toate cerințele preliminare sunt instalate și configurate corect.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path


class Verificator:
    """Clasă pentru gestionarea verificărilor și raportarea rezultatelor."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_rezolvare: str = ""):
        """Verifică o condiție și raportează rezultatul."""
        if conditie:
            print(f"  [OK] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT] {nume}")
            if indicatie_rezolvare:
                print(f"          Rezolvare: {indicatie_rezolvare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Emite un avertisment pentru o verificare opțională."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print("\n" + "=" * 50)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("Mediul este pregătit!")
            return 0
        else:
            print("Vă rugăm să rezolvați problemele de mai sus înainte de a continua.")
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


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil și configurat."""
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


def verifica_versiune_python() -> tuple[bool, str]:
    """Verifică versiunea Python."""
    versiune = sys.version_info
    text_versiune = f"{versiune.major}.{versiune.minor}.{versiune.micro}"
    return versiune >= (3, 11), text_versiune


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def main():
    """Funcția principală de verificare a mediului."""
    print("=" * 50)
    print("Verificare Mediu pentru Laboratorul Săptămânii 7")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 50)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    ok_python, versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py}",
        ok_python,
        "Instalați Python 3.11 sau mai recent de la python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "docker",
        "requests": "requests", 
        "yaml": "pyyaml"
    }
    for nume_afisat, nume_import in pachete_necesare.items():
        v.verifica(
            f"Pachet Python: {nume_afisat}",
            verifica_pachet_python(nume_import),
            f"pip install {nume_afisat}"
        )

    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de la docker.com"
    )
    
    # Verificare Docker Compose
    try:
        rezultat_compose = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compose_ok = rezultat_compose.returncode == 0
    except Exception:
        compose_ok = False
    
    v.verifica(
        "Docker Compose instalat",
        compose_ok,
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    v.verifica(
        "Daemon Docker pornit",
        verifica_docker_pornit(),
        "Porniți aplicația Docker Desktop"
    )

    print("\nMediul WSL2:")
    v.verifica(
        "WSL2 disponibil",
        verifica_wsl2(),
        "Activați WSL2: wsl --install"
    )

    print("\nInstrumente de Rețea:")
    # Verificare Wireshark
    wireshark_gasit = (
        Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil",
        wireshark_gasit,
        "Instalați Wireshark de la wireshark.org"
    )

    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("tshark"):
        v.verifica("tshark disponibil", True)
    else:
        v.avertizeaza("tshark", "Util pentru capturi din linia de comandă")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
