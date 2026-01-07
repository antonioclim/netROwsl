#!/usr/bin/env python3
"""
Pornire Laborator Săptămâna 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script pornește toate containerele Docker și verifică mediul de laborator.
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.network_utils import TesterRetea
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("porneste_lab")

# Configurația serviciilor
SERVICII = {
    "lab": {
        "container": "week1_lab",
        "port": 9090,
        "descriere": "Container principal de laborator",
        "timp_pornire": 5
    }
}


def afiseaza_banner() -> None:
    """Afișează banner-ul de pornire."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LABORATOR SĂPTĂMÂNA 1 - FUNDAMENTELE REȚELELOR".center(58) + "║")
    print("║" + "  Curs REȚELE DE CALCULATOARE - ASE, Informatică".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def verifica_docker_activ() -> bool:
    """Verifică dacă Docker este activ și funcțional."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Pornește Laboratorul Săptămânii 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python porneste_lab.py              # Pornire normală
  python porneste_lab.py --status     # Verifică doar starea
  python porneste_lab.py --rebuild    # Reconstruiește imaginile
  python porneste_lab.py --shell      # Pornește și deschide shell-ul
  python porneste_lab.py --portainer  # Include Portainer
        """
    )
    parser.add_argument(
        "--status",
        action="store_true",
        help="Verifică doar starea serviciilor"
    )
    parser.add_argument(
        "--rebuild",
        action="store_true",
        help="Reconstruiește imaginile Docker"
    )
    parser.add_argument(
        "--shell",
        action="store_true",
        help="Deschide un shell în container după pornire"
    )
    parser.add_argument(
        "--portainer",
        action="store_true",
        help="Include Portainer pentru management vizual"
    )
    parser.add_argument(
        "-d", "--detasat",
        action="store_true",
        default=True,
        help="Rulează în background (implicit)"
    )
    args = parser.parse_args()

    afiseaza_banner()

    # Verifică Docker
    if not verifica_docker_activ():
        logger.error("Docker nu este activ!")
        logger.error("Asigurați-vă că Docker Desktop rulează.")
        return 1

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Doar verificare stare
    if args.status:
        docker.afiseaza_stare(SERVICII)
        return 0

    logger.info("=" * 60)
    logger.info("Pornirea Mediului de Laborator - Săptămâna 1")
    logger.info("=" * 60)

    try:
        # Reconstruiește dacă este cerut
        if args.rebuild:
            logger.info("Se reconstruiesc imaginile Docker...")
            if not docker.compose_build(fara_cache=True):
                logger.error("Eroare la construirea imaginilor")
                return 1

        # Pornește containerele
        profiluri = ["management"] if args.portainer else None
        if not docker.compose_up(detasat=args.detasat, profiluri=profiluri):
            logger.error("Eroare la pornirea containerelor")
            return 1

        # Așteaptă să fie gata
        logger.info("Se așteaptă inițializarea serviciilor...")
        time.sleep(3)

        # Verifică serviciile
        toate_ok = True
        for nume, config in SERVICII.items():
            if docker.asteapta_container(config["container"], timeout=30):
                logger.info(f"✓ {config['descriere']} este gata")
            else:
                logger.error(f"✗ {config['descriere']} nu a pornit")
                toate_ok = False

        if toate_ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Mediul de laborator este pregătit!")
            logger.info("")
            logger.info("Puncte de acces:")
            logger.info(f"  • Container Lab: docker exec -it week1_lab bash")
            logger.info(f"  • Port TCP:      localhost:9090")
            logger.info(f"  • Port UDP:      localhost:9091")
            if args.portainer:
                logger.info(f"  • Portainer:     https://localhost:9443")
            logger.info("")
            logger.info("Pentru a opri laboratorul:")
            logger.info("  python scripts/opreste_lab.py")
            logger.info("=" * 60)

            # Deschide shell dacă este cerut
            if args.shell:
                logger.info("")
                logger.info("Se deschide shell-ul în container...")
                subprocess.run(["docker", "exec", "-it", "week1_lab", "bash"])

            return 0
        else:
            logger.error("Unele servicii nu au pornit. Verificați log-urile.")
            logger.error("  docker compose logs")
            return 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
