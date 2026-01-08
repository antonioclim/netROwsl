#!/usr/bin/env python3
"""
Script de verificare a mediului
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 6 (NAT/PAT & SDN) în mediul WSL2 + Ubuntu 22.04 + Docker + Portainer.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import socket
import os
from pathlib import Path
from typing import Tuple


class Verificator:
    """Ajutor pentru verificarea mediului cu urmărire trecut/eșuat/avertisment."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0
        
    def verifica(self, nume: str, conditie: bool, indiciu_reparare: str = "") -> bool:
        """Înregistrează un rezultat al verificării."""
        if conditie:
            print(f"  [\033[92mOK\033[0m]    {nume}")
            self.trecute += 1
        else:
            print(f"  [\033[91mEȘUAT\033[0m] {nume}")
            if indiciu_reparare:
                print(f"          Remediere: {indiciu_reparare}")
            self.esuate += 1
        return conditie
    
    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Înregistrează un avertisment."""
        print(f"  [\033[93mAVERT\033[0m] {nume}: {mesaj}")
        self.avertismente += 1
        
    def info(self, mesaj: str) -> None:
        """Afișează mesaj informațional."""
        print(f"  [INFO]  {mesaj}")
        
    def sumar(self) -> int:
        """Afișează sumarul și returnează codul de ieșire."""
        print()
        print("=" * 60)
        print(f"Rezultate: {self.trecute} trecute, {self.esuate} eșuate, {self.avertismente} avertismente")
        
        if self.esuate == 0:
            print("\n\033[92m✓ Mediul este pregătit pentru laboratorul Săptămânii 6!\033[0m")
            return 0
        else:
            print("\n\033[91m✗ Te rugăm să repari problemele de mai sus înainte de a continua.\033[0m")
            print("  Rulează: python3 setup/install_prerequisites.py")
            return 1


def verifica_comanda(cmd: str) -> bool:
    """Verifică dacă o comandă este disponibilă în PATH."""
    return shutil.which(cmd) is not None


def ruleaza_comanda(cmd: list[str], timeout: int = 10) -> tuple[bool, str]:
    """Rulează o comandă și returnează starea de succes și output-ul."""
    try:
        rezultat = subprocess.run(
            cmd,
            capture_output=True,
            timeout=timeout,
            text=True
        )
        return rezultat.returncode == 0, rezultat.stdout + rezultat.stderr
    except subprocess.TimeoutExpired:
        return False, "Comanda a expirat"
    except FileNotFoundError:
        return False, "Comanda nu a fost găsită"
    except Exception as e:
        return False, str(e)


def verifica_versiune_python() -> tuple[bool, str]:
    """Verifică dacă versiunea Python îndeplinește cerințele."""
    versiune = sys.version_info
    versiune_str = f"{versiune.major}.{versiune.minor}.{versiune.micro}"
    indeplineste = versiune >= (3, 8)
    return indeplineste, versiune_str


def verifica_pachet_python(pachet: str) -> bool:
    """Verifică dacă un pachet Python poate fi importat."""
    try:
        __import__(pachet)
        return True
    except ImportError:
        return False


def verifica_docker_ruleaza() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    succes, _ = ruleaza_comanda(["docker", "info"])
    return succes


def porneste_docker() -> bool:
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


def verifica_docker_compose() -> bool:
    """Verifică dacă Docker Compose este disponibil."""
    succes, _ = ruleaza_comanda(["docker", "compose", "version"])
    return succes


def verifica_wsl2() -> bool:
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


def verifica_ubuntu_versiune() -> Tuple[bool, str]:
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


def verifica_portainer_ruleaza() -> bool:
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


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat (pe Windows, accesibil din WSL)."""
    cai_windows = [
        Path("/mnt/c/Program Files/Wireshark/Wireshark.exe"),
        Path("/mnt/c/Program Files (x86)/Wireshark/Wireshark.exe"),
    ]
    
    for cale in cai_windows:
        if cale.exists():
            return True
    
    return verifica_comanda("wireshark") or verifica_comanda("tshark")


def verifica_mininet() -> bool:
    """Verifică dacă Mininet este instalat (pentru WSL/Linux)."""
    return verifica_comanda("mn")


def verifica_ovs() -> bool:
    """Verifică dacă Open vSwitch este instalat."""
    return verifica_comanda("ovs-vsctl")


def afiseaza_info_portainer() -> None:
    """Afișează informații despre cum să pornești Portainer."""
    print("\n  Cum să pornești Portainer:")
    print("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
    print("    -v /var/run/docker.sock:/var/run/docker.sock \\")
    print("    -v portainer_data:/data portainer/portainer-ce:latest")
    print("\n  După pornire, accesează: http://localhost:9000")
    print("  Credențiale: stud / studstudstud")


def main() -> int:
    """Rutina principală de verificare."""
    print()
    print("=" * 60)
    print("Verificarea mediului pentru laboratorul Săptămânii 6")
    print("Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    print("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer")
    print("=" * 60)
    print()
    
    v = Verificator()
    
    # Mediul WSL2
    print("\033[1mMediul WSL2:\033[0m")
    v.verifica(
        "Rulare în WSL2",
        verifica_wsl2(),
        "Asigurați-vă că rulați în WSL2, nu nativ Linux sau WSL1"
    )
    
    ubuntu_ok, ubuntu_versiune = verifica_ubuntu_versiune()
    v.verifica(
        f"Ubuntu {ubuntu_versiune}",
        ubuntu_ok,
        "Instalați Ubuntu 22.04 ca distribuție WSL implicită"
    )
    
    # Mediul Python
    print("\n\033[1mMediul Python:\033[0m")
    py_ok, py_versiune = verifica_versiune_python()
    v.verifica(
        f"Python {py_versiune}",
        py_ok,
        "Instalează Python 3.8 sau ulterior: sudo apt install python3"
    )
    
    # Pachete Python necesare
    pachete_necesare = [
        ("docker", "pip install docker --break-system-packages"),
        ("requests", "pip install requests --break-system-packages"),
        ("yaml", "pip install pyyaml --break-system-packages"),
    ]
    
    for pachet, cmd_instalare in pachete_necesare:
        v.verifica(
            f"Pachet Python: {pachet}",
            verifica_pachet_python(pachet),
            cmd_instalare
        )
    
    # Pachete Python opționale (pentru modul Mininet)
    pachete_optionale = ["scapy"]
    for pachet in pachete_optionale:
        if verifica_pachet_python(pachet):
            v.verifica(f"Pachet Python: {pachet}", True)
        else:
            v.avertizeaza(pachet, "Pachet opțional neinstalat (necesar pentru modul WSL)")
    
    # Mediul Docker
    print("\n\033[1mMediul Docker:\033[0m")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalează Docker în WSL: sudo apt install docker.io"
    )
    
    v.verifica(
        "Docker Compose (v2)",
        verifica_docker_compose(),
        "Instalează: sudo apt install docker-compose-plugin"
    )
    
    docker_ruleaza = verifica_docker_ruleaza()
    if not docker_ruleaza:
        print("  [INFO] Docker nu rulează. Se încearcă pornirea...")
        if porneste_docker():
            import time
            time.sleep(2)
            docker_ruleaza = verifica_docker_ruleaza()
            if docker_ruleaza:
                print("  [INFO] Docker a fost pornit cu succes!")
    
    v.verifica(
        "Daemon Docker rulează",
        docker_ruleaza,
        "Pornește Docker: sudo service docker start"
    )
    
    if docker_ruleaza:
        # Verifică dacă Docker poate rula containere privilegiate
        succes, output = ruleaza_comanda([
            "docker", "run", "--rm", "--privileged",
            "alpine", "echo", "privileged_ok"
        ], timeout=30)
        v.verifica(
            "Mod Docker privilegiat",
            succes and "privileged_ok" in output,
            "Verifică configurația Docker în WSL"
        )
    
    # Portainer (Management Vizual)
    print("\n\033[1mPortainer (Management Vizual):\033[0m")
    if docker_ruleaza:
        portainer_ok = verifica_portainer_ruleaza()
        v.verifica(
            "Portainer rulează pe portul 9000",
            portainer_ok,
            "Portainer nu rulează. Vezi instrucțiunile de mai jos."
        )
        if not portainer_ok:
            afiseaza_info_portainer()
    else:
        v.avertizeaza("Portainer", "Nu se poate verifica - Docker nu rulează")
    
    # Instrumente de rețea
    print("\n\033[1mInstrumente de rețea:\033[0m")
    
    wireshark_ok = verifica_wireshark()
    v.verifica(
        "Wireshark disponibil (Windows)",
        wireshark_ok,
        "Instalează Wireshark de pe wireshark.org"
    )
    
    # Verifică tshark (Wireshark CLI)
    if verifica_comanda("tshark"):
        v.verifica("tshark (CLI)", True)
    else:
        v.avertizeaza("tshark", "Analiză de pachete CLI nu este disponibilă")
    
    # Instrumente specifice WSL (opționale dar recomandate)
    print("\n\033[1mInstrumente WSL/Linux (opționale pentru modul Docker):\033[0m")
    
    mininet_ok = verifica_mininet()
    if mininet_ok:
        v.verifica("Mininet", True)
    else:
        v.avertizeaza("Mininet", "Nu este instalat (opțional - modul Docker disponibil)")
    
    ovs_ok = verifica_ovs()
    if ovs_ok:
        v.verifica("Open vSwitch", True)
    else:
        v.avertizeaza("Open vSwitch", "Nu este instalat (opțional - modul Docker disponibil)")
    
    # Verifică tcpdump
    if verifica_comanda("tcpdump"):
        v.verifica("tcpdump", True)
    else:
        v.avertizeaza("tcpdump", "Nu este instalat (opțional)")
    
    # Verifică iptables
    if verifica_comanda("iptables"):
        v.verifica("iptables", True)
    else:
        v.avertizeaza("iptables", "Nu este instalat (opțional - necesar pentru NAT în WSL)")
    
    # Instrumente opționale
    print("\n\033[1mInstrumente opționale:\033[0m")
    
    if verifica_comanda("git"):
        v.verifica("Git", True)
    else:
        v.avertizeaza("Git", "Recomandat pentru controlul versiunilor")
    
    if verifica_comanda("curl"):
        v.verifica("curl", True)
    else:
        v.avertizeaza("curl", "Util pentru testarea conexiunilor HTTP")
    
    if verifica_comanda("netcat") or verifica_comanda("nc"):
        v.verifica("netcat", True)
    else:
        v.avertizeaza("netcat", "Util pentru testarea conexiunilor TCP/UDP")
    
    # Afișare informații de acces
    print("\n" + "-" * 60)
    print("Puncte de Acces:")
    print(f"  • Portainer:       http://localhost:9000")
    print(f"  • Controller SDN:  localhost:6633 (OpenFlow)")
    print(f"  • Router NAT:      203.0.113.1 (TEST-NET-3)")
    print(f"  • Observator NAT:  Port 5000")
    print(f"  • TCP Echo:        Port 9090")
    print(f"  • UDP Echo:        Port 9091")
    print("-" * 60)
    
    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
