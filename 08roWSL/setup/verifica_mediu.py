#!/usr/bin/env python3
"""
Script de Verificare a Mediului
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect.
"""

import subprocess
import sys
import shutil
import socket
from pathlib import Path

# Coduri ANSI pentru culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
RESETARE = "\033[0m"
BOLD = "\033[1m"


class Verificator:
    """Clasă pentru gestionarea verificărilor de mediu."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0

    def verifica(self, nume: str, conditie: bool, indicatie_rezolvare: str = ""):
        """Verifică o condiție și afișează rezultatul."""
        if conditie:
            print(f"  {VERDE}[OK]{RESETARE} {nume}")
            self.trecute += 1
        else:
            print(f"  {ROSU}[EROARE]{RESETARE} {nume}")
            if indicatie_rezolvare:
                print(f"           Rezolvare: {indicatie_rezolvare}")
            self.esuate += 1

    def avertizeaza(self, nume: str, mesaj: str):
        """Afișează un avertisment."""
        print(f"  {GALBEN}[ATENȚIE]{RESETARE} {nume}: {mesaj}")
        self.avertismente += 1

    def sumar(self) -> int:
        """Afișează sumarul verificărilor."""
        print()
        print("=" * 60)
        print(f"Rezultate: {self.trecute} trecute, {self.esuate} eșuate, {self.avertismente} avertismente")
        if self.esuate == 0:
            print(f"{VERDE}Mediul este pregătit!{RESETARE}")
            return 0
        else:
            print(f"{ROSU}Vă rugăm să rezolvați problemele de mai sus înainte de a continua.{RESETARE}")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în sistem."""
    return shutil.which(cmd) is not None


def verifica_docker_pornit() -> bool:
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


def verifica_wsl2() -> bool:
    """Verifică dacă WSL2 este disponibil și configurat."""
    try:
        result = subprocess.run(
            ["wsl", "--status"],
            capture_output=True,
            timeout=10
        )
        output = result.stdout.decode() + result.stderr.decode()
        return "WSL 2" in output or "Default Version: 2" in output or "Versiunea implicită: 2" in output
    except Exception:
        return False


def verifica_port_disponibil(port: int) -> bool:
    """Verifică dacă un port este disponibil pentru utilizare."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", port))
            return True
    except OSError:
        return False


def verifica_port_in_uz(port: int) -> bool:
    """Verifică dacă un port este în uz (posibil de serviciile noastre)."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(("127.0.0.1", port))
            return result == 0
    except Exception:
        return False


def main():
    """Punctul principal de intrare."""
    print()
    print("=" * 60)
    print(f"{BOLD}Verificare Mediu pentru Laboratorul Săptămânii 8{RESETARE}")
    print("Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare versiune Python
    print(f"{ALBASTRU}Mediul Python:{RESETARE}")
    py_version = sys.version_info
    v.verifica(
        f"Python {py_version.major}.{py_version.minor}.{py_version.micro}",
        py_version >= (3, 11),
        "Instalați Python 3.11 sau ulterior de pe python.org"
    )

    # Verificare pachete Python necesare
    pachete_necesare = [
        ("docker", "docker>=6.0.0"),
        ("requests", "requests>=2.28.0"),
        ("yaml", "pyyaml>=6.0"),
        ("pytest", "pytest>=7.0.0")
    ]
    
    for modul, pachet in pachete_necesare:
        try:
            __import__(modul)
            v.verifica(f"Pachet Python: {modul}", True)
        except ImportError:
            v.verifica(
                f"Pachet Python: {modul}", 
                False, 
                f"pip install {pachet} --break-system-packages"
            )

    print()
    print(f"{ALBASTRU}Mediul Docker:{RESETARE}")
    v.verifica(
        "Docker instalat", 
        verifica_comanda("docker"),
        "Instalați Docker Desktop de pe docker.com"
    )
    
    # Verificare Docker Compose V2
    compose_disponibil = False
    if verifica_comanda("docker"):
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        compose_disponibil = result.returncode == 0
    
    v.verifica(
        "Docker Compose V2 disponibil", 
        compose_disponibil,
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    v.verifica(
        "Daemon-ul Docker rulează", 
        verifica_docker_pornit(),
        "Porniți aplicația Docker Desktop"
    )

    print()
    print(f"{ALBASTRU}Mediul WSL2:{RESETARE}")
    v.verifica(
        "WSL2 disponibil", 
        verifica_wsl2(),
        "Activați WSL2: wsl --install"
    )

    print()
    print(f"{ALBASTRU}Instrumente de Rețea:{RESETARE}")
    
    # Verificare Wireshark
    wireshark_instalat = (
        Path(r"C:\Program Files\Wireshark\Wireshark.exe").exists() or
        verifica_comanda("wireshark")
    )
    v.verifica(
        "Wireshark disponibil",
        wireshark_instalat,
        "Instalați Wireshark de pe wireshark.org"
    )

    print()
    print(f"{ALBASTRU}Disponibilitate Porturi:{RESETARE}")
    
    porturi = [
        (8080, "nginx HTTP"),
        (8443, "nginx HTTPS"),
        (9443, "Portainer")
    ]
    
    for port, serviciu in porturi:
        disponibil = verifica_port_disponibil(port)
        in_uz = verifica_port_in_uz(port)
        
        if disponibil:
            v.verifica(f"Port {port} ({serviciu}) disponibil", True)
        elif in_uz:
            # Portul este în uz - ar putea fi serviciile noastre
            v.avertizeaza(
                f"Port {port} ({serviciu})", 
                "În uz - verificați dacă sunt serviciile laboratorului"
            )
        else:
            v.verifica(
                f"Port {port} ({serviciu}) disponibil", 
                False,
                f"Eliberați portul {port} sau modificați configurația"
            )

    print()
    print(f"{ALBASTRU}Structura Directoarelor:{RESETARE}")
    
    # Verificare structură proiect
    radacina_proiect = Path(__file__).parent.parent
    directoare_necesare = [
        "docker",
        "scripts",
        "src",
        "www"
    ]
    
    toate_exista = True
    for director in directoare_necesare:
        cale = radacina_proiect / director
        if not cale.is_dir():
            v.verifica(f"Director: {director}/", False, f"Creați directorul {director}")
            toate_exista = False
    
    if toate_exista:
        v.verifica("Toate directoarele necesare prezente", True)

    print()
    print(f"{ALBASTRU}Instrumente Opționale:{RESETARE}")
    if verifica_comanda("git"):
        v.verifica("Git instalat", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")
    
    if verifica_comanda("curl"):
        v.verifica("curl disponibil", True)
    else:
        v.avertizeaza("curl", "Util pentru testarea HTTP")

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
