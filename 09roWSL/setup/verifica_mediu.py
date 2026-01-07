#!/usr/bin/env python3
"""
Script Verificare Mediu
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate
și configurate corect.
"""

import subprocess
import sys
import shutil
from pathlib import Path


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
        print("\n" + "=" * 50)
        print(f"Rezultate: {self.reușite} reușite, {self.eșuate} eșuate, {self.avertismente} avertismente")
        
        if self.eșuate == 0:
            print("\033[92mMediul este pregătit!\033[0m")
            return 0
        else:
            print("\033[91mVă rugăm să remediați problemele de mai sus înainte de a continua.\033[0m")
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


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil."""
    try:
        rezultat = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = rezultat.stdout.decode() + rezultat.stderr.decode()
        return "WSL 2" in output or "Default Version: 2" in output or "Versiune implicită: 2" in output
    except Exception:
        return False


def verifica_versiune_python() -> tuple:
    """Returnează versiunea Python curentă."""
    return sys.version_info[:3]


def main():
    """Funcția principală."""
    print("=" * 50)
    print("Verificare Mediu pentru Laboratorul Săptămânii 9")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 50)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py[0]}.{versiune_py[1]}.{versiune_py[2]}",
        versiune_py >= (3, 8),
        "Instalați Python 3.8 sau mai recent de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = ["struct", "socket", "zlib"]
    for pachet in pachete_necesare:
        try:
            __import__(pachet)
            v.verifica(f"Modul Python: {pachet}", True)
        except ImportError:
            v.verifica(f"Modul Python: {pachet}", False, f"Modul standard lipsă")

    # Verificare pachete opționale
    pachete_optionale = ["docker", "yaml", "requests"]
    for pachet in pachete_optionale:
        try:
            __import__(pachet)
            v.verifica(f"Pachet Python: {pachet}", True)
        except ImportError:
            v.verifica(
                f"Pachet Python: {pachet}",
                False,
                f"pip install {pachet}"
            )

    # Verificare Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
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
        "Docker Compose ar trebui să fie inclus în Docker Desktop"
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
    
    # Wireshark
    wireshark_gasit = (
        Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil",
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

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
