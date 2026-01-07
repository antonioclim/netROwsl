#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică că toate cerințele preliminare sunt instalate și configurate corect.

Utilizare:
    python setup/verifica_mediu.py
"""

import subprocess
import sys
import shutil
from pathlib import Path


class Verificator:
    """Clasă pentru verificarea cerințelor de mediu."""
    
    def __init__(self):
        self.reusit = 0
        self.esuat = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, sugestie_remediere: str = "") -> bool:
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            conditie: True dacă verificarea a trecut
            sugestie_remediere: Sugestie pentru remediere în caz de eșec
            
        Returns:
            Rezultatul verificării
        """
        if conditie:
            print(f"  [TRECUT] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT]  {nume}")
            if sugestie_remediere:
                print(f"           Remediere: {sugestie_remediere}")
            self.esuat += 1
        return conditie

    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [AVERT]  {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """
        Afișează sumarul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 50)
        print(f"Rezultate: {self.reusit} trecute, {self.esuat} eșuate, {self.avertismente} avertismente")
        if self.esuat == 0:
            print("✓ Mediul este pregătit pentru laborator!")
            return 0
        else:
            print("✗ Vă rugăm să remediați problemele de mai sus înainte de a continua.")
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
    """Verifică că structura proiectului este completă."""
    radacina = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src/exercises",
        "tests",
        "docs"
    ]
    
    for director in directoare_necesare:
        if not (radacina / director).exists():
            return False
    return True


def main():
    """Punctul principal de intrare."""
    print("=" * 50)
    print("Verificare Mediu pentru Laboratorul Săptămânii 3")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 50)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediu Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai nou de la python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = ["yaml", "requests"]
    for pachet in pachete_necesare:
        nume_import = "pyyaml" if pachet == "yaml" else pachet
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(pachet),
            f"pip install {nume_import}"
        )

    print("\nMediu Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de la docker.com"
    )
    
    # Verificare Docker Compose
    docker_compose_ok = False
    if verifica_comanda("docker"):
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            docker_compose_ok = rezultat.returncode == 0
        except Exception:
            pass
    
    v.verifica(
        "Docker Compose instalat",
        docker_compose_ok,
        "Docker Compose ar trebui să fie inclus în Docker Desktop"
    )
    
    v.verifica(
        "Daemon Docker pornit",
        verifica_docker_pornit(),
        "Porniți aplicația Docker Desktop"
    )

    print("\nMediu WSL2:")
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

    print("\nStructură Proiect:")
    v.verifica(
        "Structura directorului completă",
        verifica_structura_proiect(),
        "Extrageți arhiva completă WEEK3_WSLkit_RO.zip"
    )

    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")

    if verifica_comanda("code"):
        v.verifica("VS Code disponibil", True)
    else:
        v.avertizeaza("VS Code", "Recomandat ca editor de cod")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
