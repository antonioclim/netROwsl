#!/usr/bin/env python3
"""
Script de Verificare a Mediului de Lucru
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from pathlib import Path
from typing import Optional


class Verificator:
    """Clasă pentru verificarea cerințelor sistemului."""
    
    def __init__(self) -> None:
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sfat_rezolvare: str = "") -> None:
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [REUȘIT] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT]  {nume}")
            if sfat_rezolvare:
                print(f"           Soluție: {sfat_rezolvare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul verificărilor și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, "
              f"{self.avertismente} avertismente")
        if self.esuat == 0:
            print("✓ Mediul de lucru este pregătit!")
            return 0
        else:
            print("✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
    return shutil.which(cmd) is not None


def verifica_docker_ruleaza() -> bool:
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


def verifica_versiune_python() -> tuple[int, int, int]:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def verifica_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


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
    # Verifică în locații comune pe Windows
    cai_wireshark = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    return any(cale.exists() for cale in cai_wireshark) or verifica_comanda("wireshark")


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este corectă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src/exercises",
        "tests",
        "docs",
    ]
    return all((radacina / d).is_dir() for d in directoare_necesare)


def main() -> int:
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificarea Mediului pentru Laboratorul Săptămânii 1")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    major, minor, patch = verifica_versiune_python()
    v.verifica(
        f"Python {major}.{minor}.{patch}",
        (major, minor) >= (3, 11),
        "Instalați Python 3.11 sau mai recent de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "yaml": "pip install pyyaml --break-system-packages",
    }
    
    for pachet, comanda_instalare in pachete_necesare.items():
        nume_import = "yaml" if pachet == "yaml" else pachet
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(nume_import),
            comanda_instalare
        )

    # Verificare Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    v.verifica(
        "Docker Compose instalat",
        verifica_docker_compose(),
        "Docker Compose ar trebui să fie inclus cu Docker Desktop"
    )
    v.verifica(
        "Daemon-ul Docker rulează",
        verifica_docker_ruleaza(),
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

    # Verificare structura proiectului
    print("\nStructura Proiectului:")
    v.verifica(
        "Directoare necesare prezente",
        verifica_structura_proiect(),
        "Extrageți arhiva complet"
    )

    # Verificări opționale
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
