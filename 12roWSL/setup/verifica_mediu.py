#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
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

    def verifica(self, nume: str, conditie: bool, sugestie_remediere: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  [REUȘIT] {nume}")
            self.reusit += 1
        else:
            print(f"  [EȘUAT]  {nume}")
            if sugestie_remediere:
                print(f"           Remediere: {sugestie_remediere}")
            self.esuat += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  [ATENȚIE] {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print("\n" + "=" * 60)
        print(f"Rezultate: {self.reusit} reușite, {self.esuat} eșuate, {self.avertismente} avertismente")
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


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil."""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            rezultat = s.connect_ex(('localhost', port))
            return rezultat != 0  # Portul e disponibil dacă conexiunea eșuează
    except Exception:
        return True


def main():
    print("=" * 60)
    print("Verificarea Mediului pentru Laboratorul Săptămânii 12")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print("Mediul Python:")
    versiune_py = sys.version_info
    v.verifica(
        f"Python {versiune_py.major}.{versiune_py.minor}.{versiune_py.micro}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai nou de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "grpc": "grpcio",
        "google.protobuf": "protobuf",
        "docker": "docker",
        "requests": "requests",
        "yaml": "pyyaml",
        "colorama": "colorama"
    }
    
    print("\nPachete Python:")
    for modul, pachet in pachete_necesare.items():
        try:
            __import__(modul)
            v.verifica(f"Pachet: {pachet}", True)
        except ImportError:
            v.verifica(
                f"Pachet: {pachet}", 
                False, 
                f"pip install {pachet} --break-system-packages"
            )

    # Verificare mediu Docker
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat", 
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    
    compune_ok = False
    if verifica_comanda("docker"):
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compune_ok = rezultat.returncode == 0
    
    v.verifica(
        "Docker Compose instalat",
        compune_ok,
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    v.verifica(
        "Daemon Docker pornit",
        verifica_docker_pornit(),
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
    
    wireshark_path = Path(r"C:\Program Files\Wireshark\Wireshark.exe")
    v.verifica(
        "Wireshark disponibil",
        wireshark_path.exists() or verifica_comanda("wireshark"),
        "Instalați Wireshark de pe wireshark.org"
    )

    # Verificare porturi necesare
    print("\nDisponibilitatea Porturilor:")
    porturi = {
        1025: "Server SMTP",
        6200: "Server JSON-RPC",
        6201: "Server XML-RPC",
        6251: "Server gRPC",
        9443: "Portainer"
    }
    
    for port, serviciu in porturi.items():
        disponibil = verifica_port_disponibil(port)
        if disponibil:
            v.verifica(f"Port {port} ({serviciu})", True)
        else:
            v.avertizeaza(
                f"Port {port}",
                f"Ocupat - {serviciu} nu va putea porni"
            )

    # Instrumente opționale
    print("\nInstrumente Opționale:")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")
    
    if verifica_comanda("nc") or verifica_comanda("ncat"):
        v.verifica("Netcat disponibil", True)
    else:
        v.avertizeaza("Netcat", "Util pentru testarea manuală SMTP")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
