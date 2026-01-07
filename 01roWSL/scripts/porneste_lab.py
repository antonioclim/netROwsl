#!/usr/bin/env python3
"""
Script de Pornire a Laboratorului Săptămânii 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Pornește toate containerele Docker și verifică mediul de laborator.

ADAPTAT PENTRU: WSL2 + Ubuntu 22.04 + Docker (în WSL) + Portainer Global
NOTĂ: Portainer NU este pornit de acest script - rulează global pe portul 9000
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("porneste_lab")

# Definiții servicii pentru Săptămâna 1
# NOTĂ: Portainer NU este inclus - rulează ca serviciu global
SERVICII = {
    "lab": {
        "container": "week1_lab",
        "port": 9090,
        "health_check": None,
        "startup_time": 5
    },
}

# Serviciu Portainer global (doar pentru verificări de status, NU este pornit de acest script)
PORTAINER_GLOBAL = {
    "portainer": {
        "container": "portainer",
        "port": 9000,
        "health_check": "http://localhost:9000",
        "startup_time": 0  # Deja rulează
    }
}


def verifica_docker_ruleaza() -> bool:
    """Verifică dacă daemon-ul Docker este disponibil."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def porneste_serviciu_docker() -> bool:
    """Încearcă să pornească serviciul Docker (mediu WSL)."""
    try:
        rezultat = subprocess.run(
            ["sudo", "service", "docker", "start"],
            capture_output=True,
            timeout=30
        )
        time.sleep(2)  # Așteaptă pornirea serviciului
        return verifica_docker_ruleaza()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def verifica_portainer_ruleaza() -> bool:
    """Verifică dacă Portainer global rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "portainer" in rezultat.stdout.lower()
    except:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Pornește Mediul de Laborator Săptămâna 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python scripts/porneste_lab.py              # Pornește containerele de laborator
  python scripts/porneste_lab.py --status     # Verifică doar statusul
  python scripts/porneste_lab.py --rebuild    # Forțează reconstruirea imaginilor
  python scripts/porneste_lab.py --shell      # Deschide shell după pornire

NOTĂ: Portainer rulează global pe portul 9000 și NU este gestionat de acest script.
      Accesați Portainer la: http://localhost:9000 (stud/studstudstud)
        """
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verifică statusul serviciilor fără a porni"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Forțează reconstruirea imaginilor container"
    )
    parser.add_argument(
        "--detach", "-d",
        action="store_true",
        default=True,
        help="Rulează în mod detașat (implicit: True)"
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Deschide shell interactiv în container după pornire"
    )
    args = parser.parse_args()

    # Verifică dacă Docker rulează
    if not verifica_docker_ruleaza():
        logger.warning("Docker nu rulează. Se încearcă pornirea...")
        if porneste_serviciu_docker():
            logger.info("Serviciul Docker pornit cu succes.")
        else:
            logger.error("Nu s-a putut porni Docker. Rulați: sudo service docker start")
            return 1

    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    # Doar verificare status
    if args.status:
        logger.info("Verificare status servicii...")
        docker.show_status(SERVICII)
        
        # Afișează și statusul Portainer
        logger.info("")
        logger.info("Status Portainer global:")
        if verifica_portainer_ruleaza():
            logger.info("  [\033[92mRULEAZĂ\033[0m] Portainer la http://localhost:9000")
        else:
            logger.warning("  [\033[91mOPRIT\033[0m] Portainer - porniți cu: docker start portainer")
        return 0

    logger.info("=" * 60)
    logger.info("Pornire Mediu Laborator Săptămâna 1")
    logger.info("Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix")
    logger.info("=" * 60)
    logger.info("")
    logger.info("Mediu: WSL2 + Ubuntu 22.04 + Docker + Portainer Global")
    logger.info("")

    # Verifică Portainer global
    if not verifica_portainer_ruleaza():
        logger.warning("Portainer global nu rulează!")
        logger.warning("Porniți-l cu: docker start portainer")
        logger.warning("Sau instalați fresh cu:")
        logger.warning("  docker run -d -p 9000:9000 --name portainer --restart=always \\")
        logger.warning("    -v /var/run/docker.sock:/var/run/docker.sock \\")
        logger.warning("    -v portainer_data:/data portainer/portainer-ce:latest")
        logger.info("")

    try:
        # Creează directoarele necesare
        (RADACINA_PROIECT / "artifacts").mkdir(exist_ok=True)
        (RADACINA_PROIECT / "pcap").mkdir(exist_ok=True)

        # Construiește imaginile dacă se solicită
        if args.rebuild:
            logger.info("Construire imagini container...")
            if not docker.compose_build(no_cache=True):
                logger.error("Construirea imaginilor a eșuat")
                return 1

        # Pornește containerele de laborator (NU Portainer)
        logger.info("Pornire containere de laborator...")
        if not docker.compose_up(detach=args.detach, services=["lab"]):
            logger.error("Pornirea containerelor a eșuat")
            return 1

        # Așteaptă inițializarea serviciilor
        logger.info("Așteptare inițializare servicii...")
        time.sleep(3)

        # Verifică serviciile
        logger.info("Verificare status servicii...")
        toate_ok = docker.verify_services(SERVICII)

        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("\033[92mMediul de laborator este pregătit!\033[0m")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info(f"  Container Lab: docker exec -it week1_lab bash")
            logger.info(f"  Port TCP Test: localhost:9090")
            logger.info(f"  Port UDP Test: localhost:9091")
            logger.info(f"  Portainer:     http://localhost:9000 (stud/studstudstud)")
            logger.info("")
            logger.info("Pornire rapidă:")
            logger.info("  docker exec -it week1_lab bash")
            logger.info("=" * 60)
            
            # Deschide shell dacă se solicită
            if args.shell:
                logger.info("\nDeschidere shell interactiv...")
                subprocess.run(["docker", "exec", "-it", "week1_lab", "bash"])
            
            return 0
        else:
            logger.error("Unele servicii nu au pornit. Verificați jurnalele de mai sus.")
            logger.info("\nDepanare:")
            logger.info("  docker-compose -f docker/docker-compose.yml logs")
            return 1

    except Exception as e:
        logger.error(f"Pornirea laboratorului a eșuat: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
