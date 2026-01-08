#!/usr/bin/env python3
"""
Script de Verificare a Mediului de Lucru
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
"""

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Optional, Tuple


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


def pornește_docker() -> bool:
    """Încearcă să pornească serviciul Docker în WSL."""
    try:
        rezultat = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def verifică_wsl2() -> bool:
    """Verifică dacă rulăm în WSL2."""
    try:
        if not os.path.exists("/proc/version"):
            return False
        
        with open("/proc/version", "r") as f:
            version_info = f.read().lower()
        
        if "microsoft" not in version_info and "wsl" not in version_info:
            return False
        
        if "wsl2" in version_info:
            return True
        
        return os.path.exists("/run/WSL") or "microsoft-standard" in version_info
        
    except Exception:
        return False


def verifică_ubuntu_versiune() -> Tuple[bool, str]:
    """Verifică versiunea Ubuntu."""
    try:
        if os.path.exists("/etc/os-release"):
            with open("/etc/os-release", "r") as f:
                content = f.read()
            
            for line in content.split("\n"):
                if line.startswith("VERSION_ID="):
                    version = line.split("=")[1].strip('"')
                    is_correct = version.startswith("22.04")
                    return is_correct, version
        
        rezultat = subprocess.run(
            ["lsb_release", "-rs"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            version = rezultat.stdout.strip()
            is_correct = version.startswith("22.04")
            return is_correct, version
        
        return False, "necunoscut"
    except Exception:
        return False, "necunoscut"


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


def verifică_portainer_ruleaza() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', 9000))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
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


def verifică_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat (pe Windows, accesibil din WSL)."""
    wireshark_căi = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    return any(cale.exists() for cale in wireshark_căi)


def afișează_info_portainer() -> None:
    """Afișează informații despre cum să pornești Portainer."""
    print("\n  Cum să pornești Portainer:")
    print("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print("    -v portainer_data:/data portainer/portainer-ce:latest")
    print("\n  După pornire, accesează: http://localhost:9000")
    print("  Credențiale: stud / studstudstud")


def main() -> int:
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Verificarea Mediului pentru Laboratorul Săptămânii 2")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()

    v = Verificator()

    # Verificare mediu WSL2
    print("Mediul WSL2:")
    v.verifică(
        "Rulare în WSL2",
        verifică_wsl2(),
        "Asigurați-vă că rulați în WSL2, nu nativ Linux sau WSL1"
    )
    
    ubuntu_ok, ubuntu_versiune = verifică_ubuntu_versiune()
    v.verifică(
        f"Ubuntu {ubuntu_versiune}",
        ubuntu_ok,
        "Instalați Ubuntu 22.04 ca distribuție WSL implicită"
    )

    # Verificare versiune Python
    print("\nMediul Python:")
    versiune_py = verifică_versiune_python()
    v.verifică(
        f"Python {versiune_py[0]}.{versiune_py[1]}.{versiune_py[2]}",
        versiune_py >= (3, 11),
        "Instalați Python 3.11 sau mai recent: sudo apt install python3.11"
    )

    # Verificare pachete Python necesare
    pachete_necesare = {
        "docker": "pip install docker --break-system-packages",
        "requests": "pip install requests --break-system-packages",
        "yaml": "pip install pyyaml --break-system-packages"
    }
    
    for nume_import, comanda in pachete_necesare.items():
        v.verifică(
            f"Pachet Python: {nume_import}",
            verifică_pachet_python(nume_import),
            comanda
        )

    # Verificare pachete Python pentru analiză rețea (opționale)
    print("\nPachete Analiză Rețea (opționale):")
    pachete_retea = {
        "scapy": "pip install scapy --break-system-packages",
        "dpkt": "pip install dpkt --break-system-packages",
    }
    
    for pachet, comanda in pachete_retea.items():
        if verifică_pachet_python(pachet):
            v.verifică(f"Pachet Python: {pachet}", True)
        else:
            v.avertizează(pachet, f"Recomandat pentru analiză avansată. Instalare: {comanda}")

    # Verificare mediu Docker
    print("\nMediul Docker:")
    v.verifică(
        "Docker instalat",
        verifică_comandă("docker"),
        "Instalați Docker în WSL: sudo apt install docker.io"
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
        "Instalați Docker Compose: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifică_docker_pornit()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if pornește_docker():
            docker_ruleaza = verifică_docker_pornit()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifică(
        "Daemon-ul Docker pornit",
        docker_ruleaza,
        "Porniți Docker: sudo service docker start"
    )

    # Verificare Portainer (doar dacă Docker rulează)
    print("\nPortainer (Management Vizual):")
    if docker_ruleaza:
        portainer_ok = verifică_portainer_ruleaza()
        v.verifică(
            "Portainer rulează pe portul 9000",
            portainer_ok,
            "Portainer nu rulează. Vezi instrucțiunile de mai jos."
        )
        if not portainer_ok:
            afișează_info_portainer()
    else:
        v.avertizează("Portainer", "Nu se poate verifica - Docker nu rulează")

    # Verificare instrumente de rețea
    print("\nInstrumente de Rețea:")
    v.verifică(
        "Wireshark disponibil (Windows)",
        verifică_wireshark(),
        "Instalați Wireshark de pe wireshark.org (pe Windows)"
    )

    # Verificare instrumente opționale
    print("\nInstrumente Opționale:")
    if verifică_comandă("git"):
        v.verifică("Git instalat", True)
    else:
        v.avertizează("Git", "Recomandat pentru controlul versiunilor")

    if verifică_comandă("code") or os.path.exists("/mnt/c/Users"):
        vscode_paths = [
            Path("/mnt/c/Program Files/Microsoft VS Code/Code.exe"),
            Path("/mnt/c/Users") / os.environ.get("USER", "stud") / "AppData/Local/Programs/Microsoft VS Code/Code.exe"
        ]
        if any(p.exists() for p in vscode_paths) or verifică_comandă("code"):
            v.verifică("VS Code disponibil", True)
        else:
            v.avertizează("VS Code", "Recomandat pentru editare cod")
    else:
        v.avertizează("VS Code", "Recomandat pentru editare cod")

    # Verificare structură proiect
    print("\nStructura Proiectului:")
    cale_proiect = Path(__file__).parent.parent
    v.verifică(
        "Structură directoare completă",
        verifică_structura_proiect(cale_proiect),
        "Clonați repository-ul complet: git clone https://github.com/antonioclim/netROwsl.git"
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

    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:  http://localhost:9000")
    print(f"  • Server TCP: localhost:9090")
    print(f"  • Server UDP: localhost:9091")
    print("-" * 60)

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
