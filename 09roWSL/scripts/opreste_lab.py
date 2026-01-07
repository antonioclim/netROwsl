#!/usr/bin/env python3
"""
Opritor Laborator Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script oprește grațios toate containerele Docker,
păstrând datele și volumele pentru utilizare ulterioară.
"""

import sys
import argparse
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger, afiseaza_banner

logger = configureaza_logger("opreste_lab")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator pentru Săptămâna 9"
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Forțează oprirea containerelor"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timpul de așteptare pentru oprire grațioasă (secunde)"
    )
    args = parser.parse_args()

    afiseaza_banner(
        "Oprire Mediu de Laborator",
        "Săptămâna 9 - Nivelul Sesiune și Prezentare"
    )

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        logger.info("Se opresc containerele...")
        logger.info("(Datele și volumele vor fi păstrate)")
        
        # Oprește serviciile fără a elimina volumele
        succes = docker.compose_down(volume=False)

        if succes:
            logger.info("")
            logger.info("=" * 50)
            logger.info("Toate containerele au fost oprite cu succes!")
            logger.info("")
            logger.info("Volumele de date au fost păstrate.")
            logger.info("Pentru a reporni: python scripts/porneste_lab.py")
            logger.info("")
            logger.info("Pentru curățare completă (șterge și datele):")
            logger.info("  python scripts/curata.py --complet")
            logger.info("=" * 50)
            return 0
        else:
            logger.error("Eroare la oprirea containerelor.")
            logger.error("Încercați cu --fortat sau verificați manual.")
            return 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
