#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 13
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Acest script oprește toate containerele Docker păstrând datele.
"""

import sys
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.utilitare_docker import ManagerDocker

logger = configureaza_logger("opreste_lab")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 13"
    )
    parser.add_argument("--force", "-f", action="store_true",
                        help="Oprire forțată (timeout 0)")
    args = parser.parse_args()
    
    print("=" * 60)
    print("OPRIRE LABORATOR SĂPTĂMÂNA 13")
    print("=" * 60)
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    try:
        logger.info("Se opresc containerele Docker...")
        docker.compose_down(volumes=False, timeout=0 if args.force else 10)
        
        print("\n" + "=" * 60)
        print("✓ Containerele au fost oprite cu succes")
        print("  Datele au fost păstrate în volume.")
        print("\n  Pentru curățare completă, rulați:")
        print("  python scripts/curata.py --complet")
        print("=" * 60)
        return 0
        
    except Exception as e:
        logger.error(f"Eroare la oprire: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
