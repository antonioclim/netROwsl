#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script oprește toate containerele Docker păstrând datele.
"""

import sys
import argparse
from pathlib import Path

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configurează_logger

logger = configurează_logger("stop_lab")


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python stop_lab.py           # Oprire normală (păstrează datele)
  python stop_lab.py --timeout 30  # Așteptare 30 secunde înainte de forțare
        """
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Secunde de așteptat pentru oprire grațioasă (implicit: 10)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire Mediu de Laborator - Săptămâna 2")
    logger.info("=" * 60)

    try:
        cale_docker = RĂDĂCINĂ_PROIECT / "docker"
        manager = ManagerDocker(cale_docker)

        logger.info("Oprire containere...")
        logger.info(f"  (timeout: {args.timeout} secunde)")
        
        manager.compose_down(timeout=args.timeout)

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Toate containerele au fost oprite.")
        logger.info("")
        logger.info("Datele au fost păstrate. Pentru a relua laboratorul:")
        logger.info("  python scripts/start_lab.py")
        logger.info("")
        logger.info("Pentru curățare completă (înainte de săptămâna următoare):")
        logger.info("  python scripts/cleanup.py --full")
        logger.info("=" * 60)
        
        return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
