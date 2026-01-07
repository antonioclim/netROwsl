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
from typing import Optional


class Verificator:
    """Clasă pentru verificarea componentelor sistemului."""
    
    def __init__(self):
        self.reușite = 0
        self.eșuate = 0
        self.avertismente = 0

    def verifică(self, nume: str, condiție: bool, sugestie: str = "") -> None:
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            condiție: True dacă verificarea a trecut
            sugestie: Sugestie pentru rezolvare dacă a eșuat
        """
        if condiție:
            print(f"  [OK]    {nume}")
            self.reușite += 1
        else:
            print(f"  [EȘUAT] {nume}")
            if sugestie:
                print(f"          Soluție: {sugestie}")
            self.eșuate += 1

    def avertizează(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [ATENȚ] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """
        Afișează sumarul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reușite} reușite, {self.eșuate} eșuate, {self.avertismente} avertismente")
        
        if self.eșuate == 0:
            print("✓ Mediul de lucru este pregătit!")
            return 0
        else:
            print("✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.")
            return 1


def verifică_comandă(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
    return shutil.which(cmd) is not None


def verifică_docker_pornit() -> bool:
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


def verifică_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil și activ."""
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        ieșire = rezultat.stdout.decode() + rezultat.stderr.decode()
        return "WSL 2" in ieșire or "Default Version: 2" in ieșire
    except Exception:
        return False


def verifică_versiune_python() -> tuple:
    """Returnează versiunea Python ca tuple."""
    return sys.version_info[:3]


def verifică_pachet_python(nume_pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume_pachet)
        return True
    except ImportError:
        return False


def verifică_structura_proiect(cale_root: Path) -> bool:
    """Verifică structura directorului proiectului."""
    directoare_necesare = [
        "setup", "docker", "scripts", "src/exercises",
        "tests", "docs", "homework", "pcap", "artifacts"
    ]
    
    for director in directoare_necesare:
        if not (cale_root / director).exists():
            return False
    return True


def main() -> int:
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificarea Mediului pentru Laboratorul Săptămânii 2")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    versiune_py = verifică_versiune_python()
    v.verifică(
        f"Python {versiune_py[0]}.{versiune_py[1]}.{versiune_py[2]}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai recent de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "docker",
        "requests": "requests",
        "yaml": "pyyaml"
    }
    
    for nume_import, nume_pip in pachete_necesare.items():
        v.verifică(
            f"Pachet Python: {nume_pip}",
            verifică_pachet_python(nume_import),
            f"pip install {nume_pip}"
        )

    # Verificare mediu Docker
    print("\nMediul Docker:")
    v.verifică(
        "Docker instalat",
        verifică_comandă("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    
    # Verificare Docker Compose
    compose_disponibil = False
    if verifică_comandă("docker"):
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=5
            )
            compose_disponibil = rezultat.returncode == 0
        except Exception:
            pass
    
    v.verifică(
        "Docker Compose instalat",
        compose_disponibil,
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    v.verifică(
        "Daemon-ul Docker pornit",
        verifică_docker_pornit(),
        "Porniți aplicația Docker Desktop"
    )

    # Verificare WSL2
    print("\nMediul WSL2:")
    v.verifică(
        "WSL2 disponibil",
        verifică_wsl2(),
        "Activați WSL2: wsl --install"
    )

    # Verificare instrumente de rețea
    print("\nInstrumente de Rețea:")
    
    # Căutare Wireshark în locații comune Windows
    wireshark_căi = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    wireshark_găsit = any(cale.exists() for cale in wireshark_căi) or verifică_comandă("wireshark")
    
    v.verifică(
        "Wireshark disponibil",
        wireshark_găsit,
        "Instalați Wireshark de pe wireshark.org"
    )

    # Verificare instrumente opționale
    print("\nInstrumente Opționale:")
    if verifică_comandă("git"):
        v.verifică("Git instalat", True)
    else:
        v.avertizează("Git", "Recomandat pentru controlul versiunilor")

    if verifică_comandă("code"):
        v.verifică("VS Code disponibil", True)
    else:
        v.avertizează("VS Code", "Recomandat pentru editare cod")

    # Verificare structură proiect
    print("\nStructura Proiectului:")
    cale_proiect = Path(__file__).parent.parent
    v.verifică(
        "Structură directoare completă",
        verifică_structura_proiect(cale_proiect),
        "Verificați că arhiva a fost extrasă corect"
    )

    # Verificare spațiu pe disc
    print("\nResurse Sistem:")
    try:
        import shutil
        total, folosit, liber = shutil.disk_usage("/")
        liber_gb = liber // (1024 ** 3)
        v.verifică(
            f"Spațiu liber pe disc: {liber_gb} GB",
            liber_gb >= 5,
            "Eliberați cel puțin 5 GB de spațiu pe disc"
        )
    except Exception:
        v.avertizează("Spațiu disc", "Nu s-a putut verifica spațiul disponibil")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
