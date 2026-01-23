#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
from pathlib import Path

# Adaugă directorul rădăcină la cale

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger, afiseaza_banner

logger = configureaza_logger("curata")

PREFIX_SAPTAMANA = "s9"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def curata_directoare(dry_run: bool = False) -> None:
    """
    Curăță directoarele de artefacte și capturi.
    
    Argumente:
        dry_run: Doar simulează acțiunile
    """
    directoare = [
        RADACINA_PROIECT / "artifacts",
        RADACINA_PROIECT / "pcap"
    ]
    
    for director in directoare:
        if not director.exists():
            continue
        
        for fisier in director.iterdir():
            if fisier.name == ".gitkeep" or fisier.name == "README.md":
                continue
            
            if dry_run:
                logger.info(f"[SIMULARE] S-ar șterge: {fisier}")
            else:
                try:
                    if fisier.is_file():
                        fisier.unlink()
                        logger.info(f"Șters: {fisier.name}")
                    elif fisier.is_dir():
                        import shutil
                        shutil.rmtree(fisier)
                        logger.info(f"Șters directorul: {fisier.name}")
                except Exception as e:
                    logger.warning(f"Nu s-a putut șterge {fisier}: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Curățare mediu de laborator pentru Săptămâna 9"
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
        help="Arată ce s-ar elimina fără a elimina efectiv"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    afiseaza_banner(
        "Curățare Mediu de Laborator",
        "Săptămâna 9 - Nivelul Sesiune și Prezentare"
    )

    if args.simulare:
        logger.info("[SIMULARE] Nu se vor face modificări efective")
        print()

    try:
        # Oprește containerele
        logger.info("Se opresc containerele...")
        docker.compose_down(volume=args.complet, dry_run=args.simulare)

        # Elimină resursele specifice săptămânii
        logger.info(f"Se elimină resursele {PREFIX_SAPTAMANA}_*...")
        docker.elimina_dupa_prefix(PREFIX_SAPTAMANA, dry_run=args.simulare)

        # Curăță directoarele de artefacte
        if args.complet:
            logger.info("Se curăță directoarele de artefacte...")
            curata_directoare(dry_run=args.simulare)

        # Curățare sistem opțională
        if args.curata_sistem and not args.simulare:
            logger.info("Se curăță resursele Docker neutilizate...")
            docker.curata_sistem()

        print()
        logger.info("=" * 50)
        logger.info("Curățare finalizată!")
        
        if args.complet:
            logger.info("Sistemul este pregătit pentru săptămâna următoare.")
            logger.info("")
            logger.info("Toate datele de laborator au fost eliminate:")
            logger.info("  - Containere")
            logger.info("  - Rețele")
            logger.info("  - Volume")
            logger.info("  - Artefacte")
            logger.info("  - Capturi de pachete")
        else:
            logger.info("Containerele au fost oprite.")
            logger.info("Volumele de date au fost păstrate.")
            logger.info("")
            logger.info("Pentru curățare completă:")
            logger.info("  python scripts/curata.py --complet")
        
        logger.info("=" * 50)
        return 0

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
