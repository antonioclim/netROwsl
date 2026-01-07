#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest script oprește toate containerele Docker păstrând datele.
"""

import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_laborator")


def main():
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator Săptămâna 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Acest script oprește containerele păstrând volumele și datele.
Pentru curățare completă, utilizați: python scripts/curata.py --complet
        """
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Oprește forțat containerele (kill în loc de stop)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Timeout în secunde pentru oprirea grațioasă (implicit: 10)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire mediu de laborator Săptămâna 5")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        if args.fortat:
            logger.info("Oprire forțată a containerelor...")
            docker.compose_kill()
        else:
            logger.info(f"Oprire grațioasă (timeout: {args.timeout}s)...")
            docker.compose_stop(timeout=args.timeout)

        logger.info("=" * 60)
        logger.info("✓ Mediul de laborator a fost oprit.")
        logger.info("")
        logger.info("Datele au fost păstrate. Pentru a reporni:")
        logger.info("  python scripts/porneste_laborator.py")
        logger.info("")
        logger.info("Pentru curățare completă înainte de săptămâna următoare:")
        logger.info("  python scripts/curata.py --complet")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
