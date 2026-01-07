#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oprește elegant toate containerele, păstrând datele și volumele.

Utilizare:
    python scripts/opreste_lab.py [--logs]
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

PREFIX_WEEK = "week3"


def afiseaza_loguri_containere():
    """Afișează ultimele log-uri de la fiecare container."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={PREFIX_WEEK}", "--format", "{{.Names}}"],
            capture_output=True
        )
        containere = rezultat.stdout.decode().strip().split('\n')
        containere = [c for c in containere if c]
        
        for container in containere:
            print(f"\n{'='*40}")
            print(f"Log-uri: {container}")
            print('='*40)
            subprocess.run(
                ["docker", "logs", "--tail", "20", container]
            )
    except Exception as e:
        logger.warning(f"Nu s-au putut afișa log-urile: {e}")


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Oprește Laboratorul Săptămânii 3"
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Afișează log-urile containerelor înainte de oprire"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire Laborator Săptămâna 3")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        # Afișează log-uri dacă este cerut
        if args.logs:
            logger.info("Afișare log-uri containere...")
            afiseaza_loguri_containere()

        # Oprește containerele
        logger.info("Oprire containere...")
        docker.compose_down(volume=False)

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Laboratorul a fost oprit cu succes!")
        logger.info("")
        logger.info("Datele și volumele au fost păstrate.")
        logger.info("Pentru curățare completă: python scripts/curata.py --complet")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
