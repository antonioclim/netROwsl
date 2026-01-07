#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script oprește grațios toate containerele de laborator,
păstrând artefactele și datele colectate.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator pentru Săptămâna 7"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Oprire forțată fără confirmare"
    )
    parser.add_argument(
        "--volume", "-v",
        action="store_true",
        help="Elimină și volumele Docker (atenție: șterge datele)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire Mediu Laborator Săptămâna 7")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Confirmare dacă nu e forțată
    if not args.force:
        print()
        if args.volume:
            print("ATENȚIE: Această operațiune va elimina și volumele Docker!")
            print("         Toate datele salvate în volume vor fi pierdute.")
            print()
        
        raspuns = input("Doriți să continuați? (da/nu): ").strip().lower()
        if raspuns not in ("da", "d", "yes", "y"):
            logger.info("Operațiune anulată de utilizator")
            return 0

    try:
        logger.info("Oprire containere...")
        ok = docker.compose_down(volumes=args.volume)

        if ok:
            logger.info("")
            logger.info("=" * 60)
            logger.info("Containerele au fost oprite cu succes")
            if not args.volume:
                logger.info("Notă: Volumele au fost păstrate")
                logger.info("      Pentru curățare completă: python scripts/curata.py --complet")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Eroare la oprirea containerelor")
            return 1

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
