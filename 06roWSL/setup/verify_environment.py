#!/usr/bin/env python3
"""
Script de verificare a mediului
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt instalate și configurate corect
pentru laboratorul Săptămânii 6 (NAT/PAT & SDN).
"""

from __future__ import annotations

import subprocess
import sys
import shutil
import platform
from pathlib import Path
from typing import Callable, Optional


class Verificator:
    """Ajutor pentru verificarea mediului cu urmărire trecut/eșuat/avertisment."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
        self.avertismente = 0
        
    def verifica(self, nume: str, conditie: bool, indiciu_reparare: str = "") -> bool:
        """Înregistrează un rezultat al verificării."""
        if conditie:
            print(f"  [OK]    {nume}")
            self.trecute += 1
        else:
            print(f"  [EȘUAT] {nume}")
            if indiciu_reparare:
                print(f"          Remediere: {indiciu_reparare}")
            self.esuate += 1
        return conditie
    
    def avertizeaza(self, nume: str, mesaj: str) -> None:
        """Înregistrează un avertisment."""
        print(f"  [AVERT] {nume}: {mesaj}")
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
            print("\n✓ Mediul este pregătit pentru laboratorul Săptămânii 6!")
            return 0
        else:
            print("\n✗ Te rugăm să repari problemele de mai sus înainte de a continua.")
            print("  Rulează: python setup/install_prerequisites.py")
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
    indeplineste = versiune >= (3, 11)
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


def verifica_docker_compose() -> bool:
    """Verifică dacă Docker Compose este disponibil."""
    succes, _ = ruleaza_comanda(["docker", "compose", "version"])
    return succes


def verifica_wsl2() -> tuple[bool, str]:
    """Verifică dacă rulează în WSL2 sau dacă WSL2 este disponibil."""
    # Verifică dacă rulăm în interiorul WSL
    if Path("/proc/version").exists():
        try:
            with open("/proc/version", "r") as f:
                continut = f.read().lower()
                if "microsoft" in continut or "wsl" in continut:
                    # Verifică versiunea WSL
                    if "wsl2" in continut:
                        return True, "Rulează în WSL2"
                    # Încearcă să determine versiunea altfel
                    succes, output = ruleaza_comanda(["uname", "-r"])
                    if succes and "microsoft" in output.lower():
                        return True, "Rulează în WSL"
        except Exception:
            pass
    
    # Verifică dacă WSL este disponibil din Windows
    if platform.system() == "Windows":
        succes, output = ruleaza_comanda(["wsl", "--status"])
        if succes:
            if "WSL 2" in output or "Default Version: 2" in output:
                return True, "WSL2 disponibil"
        return False, "WSL2 nu este configurat"
    
    # Linux nativ
    if platform.system() == "Linux":
        return True, "Linux nativ"
    
    return False, "Platformă necunoscută"


def verifica_wireshark() -> bool:
    """Verifică dacă Wireshark este instalat."""
    # Căi Windows
    cai_windows = [
        Path(r"C:\Program Files\Wireshark\Wireshark.exe"),
        Path(r"C:\Program Files (x86)\Wireshark\Wireshark.exe"),
    ]
    
    for cale in cai_windows:
        if cale.exists():
            return True
    
    # Verifică în PATH (Linux/WSL)
    return verifica_comanda("wireshark") or verifica_comanda("tshark")


def verifica_mininet() -> bool:
    """Verifică dacă Mininet este instalat (pentru WSL/Linux)."""
    return verifica_comanda("mn")


def verifica_ovs() -> bool:
    """Verifică dacă Open vSwitch este instalat."""
    return verifica_comanda("ovs-vsctl")


def main() -> int:
    """Rutina principală de verificare."""
    print()
    print("=" * 60)
    print("Verificarea mediului pentru laboratorul Săptămânii 6")
    print("Disciplina REȚELE DE CALCULATOARE - ASE | de Revolvix")
    print("=" * 60)
    print()
    
    v = Verificator()
    
    # Mediul Python
    print("Mediul Python:")
    py_ok, py_versiune = verifica_versiune_python()
    v.verifica(
        f"Python {py_versiune}",
        py_ok,
        "Instalează Python 3.11 sau ulterior de pe python.org"
    )
    
    # Pachete Python necesare
    pachete_necesare = [
        ("docker", "pip install docker"),
        ("requests", "pip install requests"),
        ("yaml", "pip install pyyaml"),
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
    print("\nMediul Docker:")
    v.verifica(
        "Docker instalat",
        verifica_comanda("docker"),
        "Instalează Docker Desktop de pe docker.com"
    )
    
    v.verifica(
        "Docker Compose (v2)",
        verifica_docker_compose(),
        "Docker Compose ar trebui să vină cu Docker Desktop"
    )
    
    docker_ruleaza = verifica_docker_ruleaza()
    v.verifica(
        "Daemon Docker rulează",
        docker_ruleaza,
        "Pornește aplicația Docker Desktop"
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
            "Activează containerele privilegiate în setările Docker Desktop"
        )
    
    # Mediul WSL2
    print("\nMediul platformei:")
    wsl_ok, wsl_status = verifica_wsl2()
    v.verifica(f"WSL2/Linux: {wsl_status}", wsl_ok, "Activează WSL2: wsl --install")
    
    # Instrumente de rețea
    print("\nInstrumente de rețea:")
    
    wireshark_ok = verifica_wireshark()
    v.verifica(
        "Wireshark disponibil",
        wireshark_ok,
        "Instalează Wireshark de pe wireshark.org"
    )
    
    # Verifică tshark (Wireshark CLI)
    if verifica_comanda("tshark"):
        v.verifica("tshark (CLI)", True)
    else:
        v.avertizeaza("tshark", "Analiză de pachete CLI nu este disponibilă")
    
    # Instrumente specifice WSL (opționale dar recomandate)
    print("\nInstrumente WSL/Linux (opționale pentru modul Docker):")
    
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
    print("\nInstrumente opționale:")
    
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
    
    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
