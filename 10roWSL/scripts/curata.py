#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 10
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
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

logger = configureaza_logger("curata")

PREFIX_SAPTAMANA = "week10"


def curata_artefacte(dry_run: bool = False):
    """Curăță directoarele de artefacte și capturi."""
    dir_artefacte = RADACINA_PROIECT / "artifacts"
    dir_capturi = RADACINA_PROIECT / "pcap"
    
    for director in [dir_artefacte, dir_capturi]:
        if not director.exists():
            continue
        
        for fisier in director.iterdir():
            if fisier.name == ".gitkeep":
                continue
            
            if dry_run:
                logger.info(f"[SIMULARE] Ar șterge: {fisier}")
            else:
                if fisier.is_file():
                    fisier.unlink()
                    logger.info(f"Șters: {fisier.name}")
                elif fisier.is_dir():
                    import shutil
                    shutil.rmtree(fisier)
                    logger.info(f"Șters director: {fisier.name}")


def main():
    """Funcția principală de curățare."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 10"
    )
    parser.add_argument(
        "--complet",
        action="store_true",
        help="Elimină volumele și toate datele (folosiți înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--curata-sistem",
        action="store_true",
        help="Curăță și resursele Docker neutilizate"
    )
    parser.add_argument(
        "--simulare",
        action="store_true",
        help="Arată ce ar fi eliminat fără să elimine efectiv"
    )
    args = parser.parse_args()

    print()
    logger.info("=" * 60)
    logger.info("Curățare Laborator Săptămâna 10")
    logger.info("=" * 60)

    if args.simulare:
        logger.info("[SIMULARE] Nu se vor face modificări reale")
        print()

    try:
        docker = ManagerDocker(RADACINA_PROIECT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Eroare: {e}")
        return 1

    try:
        # Oprire containere
        logger.info("Oprire containere...")
        docker.compose_down(volume=args.complet, dry_run=args.simulare)

        # Eliminare resurse cu prefixul săptămânii
        logger.info(f"Eliminare resurse {PREFIX_SAPTAMANA}_*...")
        docker.elimina_dupa_prefix(PREFIX_SAPTAMANA, dry_run=args.simulare)

        # Curățare artefacte și capturi
        if args.complet:
            logger.info("Curățare directoare artefacte...")
            curata_artefacte(dry_run=args.simulare)

        # Curățare sistem opțională
        if args.curata_sistem and not args.simulare:
            logger.info("Curățare resurse Docker neutilizate...")
            docker.curata_sistem()

        logger.info("=" * 60)
        if args.simulare:
            logger.info("[SIMULARE] Curățare completă (nu s-au făcut modificări)")
        else:
            logger.info("✓ Curățare completă!")
            if args.complet:
                logger.info("Sistemul este pregătit pentru următoarea sesiune.")
        logger.info("=" * 60)
        return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
