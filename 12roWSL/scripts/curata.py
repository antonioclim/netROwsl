#!/usr/bin/env python3
"""
Script de Curățare a Laboratorului Săptămânii 12
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""

import subprocess
import sys
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("curata")

PREFIX_SAPTAMANA = "week12"


def curata_director(cale: Path, extensii: list = None, pastreaza_gitkeep: bool = True):
    """Curăță un director de fișiere specifice."""
    if not cale.exists():
        return 0
    
    numar_sters = 0
    for fisier in cale.iterdir():
        if fisier.name == ".gitkeep" and pastreaza_gitkeep:
            continue
        
        if extensii:
            if fisier.suffix in extensii:
                fisier.unlink()
                numar_sters += 1
        else:
            if fisier.is_file():
                fisier.unlink()
                numar_sters += 1
    
    return numar_sters


def main():
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 12"
    )
    parser.add_argument(
        "--complet",
        action="store_true",
        help="Elimină volumele și toate datele (folosiți înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Curăță și resursele Docker neutilizate"
    )
    parser.add_argument(
        "--simulare",
        action="store_true",
        help="Afișează ce ar fi șters fără a șterge efectiv"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Curățare Mediu de Laborator - Săptămâna 12")
    logger.info("=" * 60)

    if args.simulare:
        logger.info("[SIMULARE] Nu se vor face modificări efective")

    try:
        # Oprire containere
        logger.info("Oprire containere...")
        if not args.simulare:
            docker.compune_down(volume=args.complet)
        else:
            logger.info("  [SIMULARE] docker compose down" + 
                       (" --volumes" if args.complet else ""))

        # Eliminare resurse specifice săptămânii
        logger.info(f"Eliminare resurse {PREFIX_SAPTAMANA}_*...")
        if not args.simulare:
            docker.elimina_dupa_prefix(PREFIX_SAPTAMANA)
        else:
            logger.info(f"  [SIMULARE] Eliminare containere/rețele/volume cu prefix '{PREFIX_SAPTAMANA}'")

        # Curățare artefacte
        if args.complet:
            logger.info("Curățare directoare de lucru...")
            
            # Curățare pcap
            dir_pcap = RADACINA_PROIECT / "pcap"
            if not args.simulare:
                nr = curata_director(dir_pcap, extensii=[".pcap", ".pcapng"])
                logger.info(f"  Șterse {nr} fișiere de captură")
            else:
                logger.info(f"  [SIMULARE] Ștergere fișiere din {dir_pcap}")
            
            # Curățare artefacte
            dir_artefacte = RADACINA_PROIECT / "artifacts"
            if not args.simulare:
                nr = curata_director(dir_artefacte)
                logger.info(f"  Șterse {nr} artefacte")
            else:
                logger.info(f"  [SIMULARE] Ștergere fișiere din {dir_artefacte}")
            
            # Curățare spool
            dir_spool = RADACINA_PROIECT / "docker" / "volumes" / "spool"
            if not args.simulare:
                nr = curata_director(dir_spool, extensii=[".eml", ".json"])
                logger.info(f"  Șterse {nr} mesaje email")
            else:
                logger.info(f"  [SIMULARE] Ștergere mesaje din {dir_spool}")

        # Prune opțional
        if args.prune and not args.simulare:
            logger.info("Curățare resurse Docker neutilizate...")
            docker.prune_sistem()

        # Mesaj final
        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Curățare completă!")
        
        if args.complet:
            logger.info("  Sistemul este pregătit pentru următoarea sesiune.")
        else:
            logger.info("  Pentru curățare completă: python scripts/curata.py --complet")
        
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
