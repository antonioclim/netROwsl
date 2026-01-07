#!/usr/bin/env python3
"""
Script de Oprire a Laboratorului Săptămânii 12
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Oprește grațios toate containerele de laborator.
"""

import subprocess
import sys
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")


def main():
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 12"
    )
    parser.add_argument(
        "--volume", "-v",
        action="store_true",
        help="Elimină și volumele (datele persistente)"
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Forțează oprirea imediată"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Oprire Mediu de Laborator - Săptămâna 12")
    logger.info("=" * 60)

    try:
        if args.fortat:
            logger.info("Oprire forțată a containerelor...")
            subprocess.run(
                ["docker", "compose", "kill"],
                cwd=RADACINA_PROIECT / "docker",
                capture_output=True
            )
        
        logger.info("Oprire grațioasă a containerelor...")
        docker.compune_down(volume=args.volume)

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Toate containerele au fost oprite.")
        
        if args.volume:
            logger.info("  Volumele au fost de asemenea eliminate.")
        else:
            logger.info("  Volumele au fost păstrate.")
            logger.info("  Pentru curățare completă: python scripts/curata.py --complet")
        
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
