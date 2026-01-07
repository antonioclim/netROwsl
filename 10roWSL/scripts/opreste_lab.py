#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 10
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script oprește toate containerele Docker păstrând volumele de date.
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului la calea Python
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")


def main():
    """Funcția principală de oprire."""
    parser = argparse.ArgumentParser(
        description="Oprește Laboratorul Săptămânii 10"
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Oprire forțată (kill în loc de stop)"
    )
    args = parser.parse_args()

    print()
    logger.info("=" * 60)
    logger.info("Oprire Laborator Săptămâna 10")
    logger.info("=" * 60)

    try:
        docker = ManagerDocker(RADACINA_PROIECT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Eroare: {e}")
        return 1

    try:
        logger.info("Oprire containere (datele vor fi păstrate)...")
        
        succes = docker.compose_down(volume=False)
        
        if succes:
            logger.info("=" * 60)
            logger.info("✓ Toate containerele au fost oprite")
            logger.info("")
            logger.info("Volumele de date au fost păstrate.")
            logger.info("Pentru curățare completă, rulați:")
            logger.info("  python scripts/curata.py --complet")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Oprirea containerelor a eșuat")
            return 1

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare la oprire: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
