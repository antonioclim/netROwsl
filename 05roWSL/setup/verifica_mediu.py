#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
from pathlib import Path


class Verificator:
    """Clasă pentru verificarea cerințelor sistemului."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sugestie_reparare: str = ""):
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            conditie: True dacă verificarea a trecut
            sugestie_reparare: Sugestie pentru rezolvarea problemei
        """
        if conditie:
            print(f"  [OK] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT] {nume}")
            if sugestie_reparare:
                print(f"         Reparare: {sugestie_reparare}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """
        Afișează un avertisment.
        
        Args:
            nume: Numele verificării
            mesaj: Mesajul de avertizare
        """
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def rezumat(self) -> int:
        """
        Afișează rezumatul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 50)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("✓ Mediul este pregătit pentru laborator!")
            return 0
        else:
            print("✗ Vă rugăm să rezolvați problemele de mai sus înainte de a continua.")
            return 1


def verifica_comanda_disponibila(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
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
    """Verifică dacă WSL2 este disponibil și configurat."""
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = rezultat.stdout.decode() + rezultat.stderr.decode()
        return "WSL 2" in output or "Default Version: 2" in output or "Versiunea implicită: 2" in output
    except Exception:
        return False


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def verifica_pachet_python(pachet: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(pachet)
        return True
    except ImportError:
        return False


def verifica_structura_proiect() -> bool:
    """Verifică dacă structura proiectului este completă."""
    cale_curenta = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src",
        "tests",
        "docs"
    ]
    
    for director in directoare_necesare:
        if not (cale_curenta / director).exists():
            return False
    
    return True


def main():
    print("=" * 60)
    print("  Verificare Mediu pentru Laborator Săptămâna 5")
    print("  Rețele de Calculatoare – ASE, Informatică Economică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verifică versiunea Python
    print("Mediul Python:")
    versiune = verifica_versiune_python()
    v.verifica(
        f"Python {versiune[0]}.{versiune[1]}.{versiune[2]}",
        versiune >= (3, 11),
        "Instalați Python 3.11 sau mai nou de la python.org"
    )

    # Verifică pachetele Python necesare
    pachete_necesare = {
        "docker": "pip install docker",
        "requests": "pip install requests",
        "yaml": "pip install pyyaml"
    }
    
    for pachet, comanda_instalare in pachete_necesare.items():
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(pachet),
            comanda_instalare
        )

    # Verifică mediul Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda_disponibila("docker"),
        "Instalați Docker Desktop de la docker.com"
    )
    
    # Verifică Docker Compose
    compuse_disponibil = False
    if verifica_comanda_disponibila("docker"):
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compuse_disponibil = rezultat.returncode == 0
    
    v.verifica(
        "Docker Compose instalat",
        compuse_disponibil,
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    v.verifica(
        "Daemonul Docker rulează",
        verifica_docker_activ(),
        "Porniți aplicația Docker Desktop"
    )

    # Verifică mediul WSL2
    print("\nMediul WSL2:")
    v.verifica(
        "WSL2 disponibil",
        verifica_wsl2(),
        "Activați WSL2: wsl --install"
    )

    # Verifică instrumentele de rețea
    print("\nInstrumente de Rețea:")
    cale_wireshark = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    v.verifica(
        "Wireshark disponibil",
        cale_wireshark.exists() or verifica_comanda_disponibila("wireshark"),
        "Instalați Wireshark de la wireshark.org"
    )

    # Verifică instrumente opționale
    print("\nInstrumente Opționale:")
    if verifica_comanda_disponibila("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda_disponibila("code"):
        v.verifica("VS Code disponibil", True)
    else:
        v.avertizeaza("VS Code", "Recomandat pentru editarea codului")

    # Verifică structura proiectului
    print("\nStructura Proiectului:")
    v.verifica(
        "Structura directoarelor completă",
        verifica_structura_proiect(),
        "Asigurați-vă că ați dezarhivat complet kitul"
    )

    # Verifică fișierul docker-compose.yml
    cale_compose = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
    v.verifica(
        "Fișier docker-compose.yml prezent",
        cale_compose.exists(),
        "Fișierul docker-compose.yml lipsește din directorul docker/"
    )

    return v.rezumat()


if __name__ == "__main__":
    sys.exit(main())
