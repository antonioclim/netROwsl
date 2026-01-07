#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
import platform
from pathlib import Path


class Verificator:
    """Clasă pentru verificarea cerințelor preliminare."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0
    
    def verifica(self, nume: str, conditie: bool, indiciu_remediere: str = "") -> None:
        """
        Verifică o condiție și afișează rezultatul.
        
        Args:
            nume: Numele verificării
            conditie: Rezultatul verificării (True/False)
            indiciu_remediere: Mesaj de ajutor dacă verificarea eșuează
        """
        if conditie:
            print(f"  [TRECUT] {nume}")
            self.trecute += 1
        else:
            print(f"  [EȘUAT] {nume}")
            if indiciu_remediere:
                print(f"          Remediere: {indiciu_remediere}")
            self.esuate += 1
    
    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Afișează un avertisment."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1
    
    def sumar(self) -> int:
        """
        Afișează sumarul verificărilor.
        
        Returns:
            0 dacă toate verificările au trecut, 1 altfel
        """
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.trecute} trecute, {self.esuate} eșuate, {self.avertismente} avertismente")
        if self.esuate == 0:
            print("✓ Mediul este pregătit pentru laborator!")
            return 0
        else:
            print("✗ Vă rugăm remediați problemele de mai sus înainte de a continua.")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
    return shutil.which(cmd) is not None


def verifica_docker_ruleaza() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def verifica_docker_compose() -> bool:
    """Verifică dacă Docker Compose este disponibil."""
    try:
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil (doar pe Windows)."""
    if platform.system() != "Windows":
        return True  # Nu se aplică pe alte sisteme
    
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = result.stdout.decode() + result.stderr.decode()
        return "WSL 2" in output or "Default Version: 2" in output
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


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat."""
    # Verifică calea standard pe Windows
    cale_windows = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    if cale_windows.exists():
        return True
    
    # Verifică în PATH
    return verifica_comanda("wireshark") or verifica_comanda("tshark")


def main():
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificare Mediu pentru Laboratorul Săptămânii 11")
    print("Laborator Rețele de Calculatoare — ASE, Informatică Economică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediu Python:")
    versiune_py = verifica_versiune_python()
    v.verifica(
        f"Python {versiune_py[0]}.{versiune_py[1]}.{versiune_py[2]}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai nou de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "requests": "pip install requests",
        "pyyaml": "pip install pyyaml",
    }
    for pachet, comanda_instalare in pachete_necesare.items():
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(pachet.replace("-", "_")),
            comanda_instalare
        )

    # Verificare pachete opționale
    print("\nPachete Opționale:")
    pachete_optionale = {
        "dnspython": "pip install dnspython",
        "paramiko": "pip install paramiko",
        "pyftpdlib": "pip install pyftpdlib",
    }
    for pachet, comanda in pachete_optionale.items():
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet}", True)
        else:
            v.avertizeaza(f"Pachet Python: {pachet}", f"Opțional, instalați cu: {comanda}")

    # Verificare mediu Docker
    print("\nMediu Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    v.verifica(
        "Docker Compose instalat",
        verifica_docker_compose(),
        "Docker Compose vine inclus cu Docker Desktop"
    )
    v.verifica(
        "Daemon Docker rulează",
        verifica_docker_ruleaza(),
        "Porniți aplicația Docker Desktop"
    )

    # Verificare WSL2 (doar pe Windows)
    if platform.system() == "Windows":
        print("\nMediu WSL2:")
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
    
    if verifica_comanda("curl"):
        v.verifica("curl instalat", True)
    else:
        v.avertizeaza("curl", "Recomandat pentru testare HTTP")

    # Verificare disponibilitate porturi
    print("\nDisponibilitate Porturi:")
    porturi = [8080, 8081, 8082, 8083]
    for port in porturi:
        disponibil = verifica_port_disponibil(port)
        if disponibil:
            v.verifica(f"Port {port} disponibil", True)
        else:
            v.avertizeaza(f"Port {port}", f"Portul este ocupat - unele exerciții pot necesita modificări")

    # Verificare structură directoare
    print("\nStructură Directoare:")
    directoare_necesare = ["docker", "scripts", "src", "tests"]
    cale_radacina = Path(__file__).parent.parent
    for director in directoare_necesare:
        cale = cale_radacina / director
        v.verifica(
            f"Director '{director}/' există",
            cale.exists(),
            f"Creați directorul: mkdir {director}"
        )

    # Verificare instrumente opționale
    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru control versiuni")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
