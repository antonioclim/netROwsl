#!/usr/bin/env python3
"""
Pornire Laborator Săptămâna 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script pornește containerele Docker necesare pentru laborator și verifică
că toate dependințele sunt disponibile.

IMPORTANT: Portainer trebuie să ruleze deja pe portul 9000!
"""

from __future__ import annotations

import subprocess
import sys
import time
import webbrowser
import argparse
import socket
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Credențiale standard - le știi deja, dar le las aici pentru referință
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"  # parolă: stud x3


def afiseaza_banner() -> None:
    """Afișează banner-ul de pornire. Arată și info util."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  LABORATOR SĂPTĂMÂNA 1 - FUNDAMENTELE REȚELELOR".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICA_PREREQUISITE
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_docker() -> bool:
    """Verifică dacă Docker daemon rulează.
    
    Încearcă 'docker info' - dacă merge, Docker e OK.
    Dacă nu merge, probabil trebuie 'sudo service docker start'.
    """
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def verifica_portainer() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000.
    
    Portainer trebuie să fie DEJA pornit (nu îl pornim noi).
    Credențiale: stud / studstudstud
    """
    try:
        # Prima metodă: verifică containerul
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
            return True
        
        # A doua metodă: verifică portul direct
        # Uneori containerul nu apare în filtru dar portul răspunde
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', PORTAINER_PORT))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
        return False


def verifica_retea_existenta(nume_retea: str) -> bool:
    """Verifică dacă rețeaua Docker există deja."""
    try:
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={nume_retea}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        return nume_retea in rezultat.stdout
    except Exception:
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# EXECUTA_LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def porneste_mediu(docker: ManagerDocker, rebuild: bool = False) -> bool:
    """Pornește mediul de laborator cu Docker Compose.
    
    Args:
        docker: Instanța ManagerDocker
        rebuild: Dacă True, reconstruiește imaginile (durează mai mult)
        
    Returns:
        True dacă pornirea a reușit
    """
    logger.info("Se pornesc containerele de laborator...")
    
    # Dacă vrei rebuild, adaugă --build
    if rebuild:
        logger.info("(Se reconstruiesc imaginile - poate dura câteva minute)")
        succes = docker.compose_up(rebuild=True)
    else:
        succes = docker.compose_up()
    
    if succes:
        # Așteaptă puțin să pornească totul
        logger.info("Se așteaptă pornirea completă...")
        time.sleep(3)
        return True
    return False


def verifica_servicii() -> dict:
    """Verifică starea serviciilor pornite.
    
    Returns:
        Dict cu statusul fiecărui serviciu
    """
    servicii = {
        "week1_lab": False,
        "portainer": False
    }
    
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}:{{.Status}}"],
            capture_output=True,
            text=True
        )
        
        for linie in rezultat.stdout.strip().split("\n"):
            if ":" in linie:
                nume, status = linie.split(":", 1)
                if nume in servicii and "Up" in status:
                    servicii[nume] = True
                # Portainer poate avea nume diferit
                if "portainer" in nume.lower() and "Up" in status:
                    servicii["portainer"] = True
                    
    except Exception as e:
        logger.warning(f"Nu am putut verifica serviciile: {e}")
    
    return servicii


# ═══════════════════════════════════════════════════════════════════════════════
# AFISEAZA_REZULTATE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_status_final(servicii: dict) -> None:
    """Afișează statusul final într-un format ușor de citit."""
    print()
    print("=" * 60)
    print("STATUS SERVICII")
    print("=" * 60)
    
    for serviciu, activ in servicii.items():
        status = "✓ ACTIV" if activ else "✗ OPRIT"
        culoare = "\033[92m" if activ else "\033[91m"
        reset = "\033[0m"
        print(f"  {culoare}{status}{reset}  {serviciu}")
    
    print()
    print("INFORMAȚII ACCES:")
    print("-" * 60)
    print(f"  Portainer:     {PORTAINER_URL}")
    print(f"                 User: {PORTAINER_USER} / Pass: {PORTAINER_PASS}")
    print(f"  Container Lab: docker exec -it week1_lab bash")
    print(f"  TCP Port:      localhost:9090")
    print(f"  UDP Port:      localhost:9091")
    print("=" * 60)
    print()


def deschide_portainer_browser() -> None:
    """Încearcă să deschidă Portainer în browser."""
    try:
        webbrowser.open(PORTAINER_URL)
        logger.info(f"S-a deschis {PORTAINER_URL} în browser")
    except Exception:
        logger.info(f"Deschide manual: {PORTAINER_URL}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_SI_ARGUMENTE
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Funcția principală.
    
    Returns:
        0 dacă totul a mers bine, altfel cod de eroare
    """
    parser = argparse.ArgumentParser(
        description="Pornește Laboratorul Săptămânii 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python3 porneste_lab.py              # Pornire normală
  python3 porneste_lab.py --rebuild    # Reconstruiește imaginile
  python3 porneste_lab.py --status     # Doar verifică statusul
  python3 porneste_lab.py --browser    # Deschide Portainer în browser

Credențiale Portainer: stud / studstudstud
        """
    )
    parser.add_argument(
        "--rebuild", "-r",
        action="store_true",
        help="Reconstruiește imaginile Docker (durează mai mult)"
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Doar verifică și afișează statusul serviciilor"
    )
    parser.add_argument(
        "--browser", "-b",
        action="store_true",
        help="Deschide Portainer în browser după pornire"
    )
    args = parser.parse_args()

    afiseaza_banner()

    # Inițializare manager Docker
    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Doar status?
    if args.status:
        servicii = verifica_servicii()
        afiseaza_status_final(servicii)
        return 0 if all(servicii.values()) else 1

    # ═══════════════════════════════════════════════════════════════════════════
    # VERIFICARI_PRELIMINARE
    # ═══════════════════════════════════════════════════════════════════════════
    
    logger.info("=" * 60)
    logger.info("Verificare Cerințe Preliminare")
    logger.info("=" * 60)

    # 1. Docker
    logger.info("Verificare Docker...")
    if not verifica_docker():
        logger.error("Docker nu rulează!")
        logger.error("Rulează: sudo service docker start")
        logger.error("Parolă: stud")
        return 1
    logger.info("✓ Docker funcționează")

    # 2. Portainer (trebuie să existe deja)
    logger.info("Verificare Portainer...")
    if not verifica_portainer():
        logger.warning("⚠ Portainer nu rulează pe portul 9000")
        logger.warning("Pornește-l cu:")
        logger.warning("  docker start portainer")
        logger.warning("Sau creează-l dacă nu există (vezi README.md)")
        # Nu e fatal - continuăm
    else:
        logger.info(f"✓ Portainer activ pe {PORTAINER_URL}")

    # ═══════════════════════════════════════════════════════════════════════════
    # PORNIRE_MEDIU
    # ═══════════════════════════════════════════════════════════════════════════

    logger.info("")
    logger.info("=" * 60)
    logger.info("Pornire Mediu de Laborator")
    logger.info("=" * 60)

    try:
        if not porneste_mediu(docker, rebuild=args.rebuild):
            logger.error("Nu s-a putut porni mediul de laborator")
            logger.error("Verifică log-urile: docker-compose logs")
            return 1

        # Verificare finală
        servicii = verifica_servicii()
        afiseaza_status_final(servicii)

        # Deschide browser dacă s-a cerut
        if args.browser:
            deschide_portainer_browser()

        # Succes?
        if servicii.get("week1_lab", False):
            logger.info("✓ Laboratorul este pregătit!")
            logger.info("")
            logger.info("Pentru a intra în container:")
            logger.info("  docker exec -it week1_lab bash")
            return 0
        else:
            logger.warning("⚠ Unele servicii nu au pornit corect")
            return 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
