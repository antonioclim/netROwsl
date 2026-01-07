#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script oprește toate containerele în mod controlat, păstrând datele.
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
from pathlib import Path

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")


def afiseaza_banner() -> None:
    """Afișează banner-ul de oprire."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  OPRIRE LABORATOR SĂPTĂMÂNA 1".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def oprire_gratiosa(container: str, timeout: int = 30) -> bool:
    """Oprește un container în mod grațios.
    
    Args:
        container: Numele containerului
        timeout: Timpul de așteptare înainte de forțare
        
    Returns:
        True dacă oprirea a reușit
    """
    logger.info(f"Se oprește {container}...")
    
    try:
        # Mai întâi încearcă oprire grațioasă
        rezultat = subprocess.run(
            ["docker", "stop", "-t", str(timeout), container],
            capture_output=True,
            text=True,
            timeout=timeout + 10
        )
        
        if rezultat.returncode == 0:
            logger.info(f"✓ {container} oprit cu succes")
            return True
        else:
            logger.warning(f"Oprire grațioasă eșuată: {rezultat.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout la oprirea {container}")
        return False
    except Exception as e:
        logger.error(f"Eroare la oprirea {container}: {e}")
        return False


def oprire_fortata(container: str) -> bool:
    """Forțează oprirea unui container.
    
    Args:
        container: Numele containerului
        
    Returns:
        True dacă oprirea a reușit
    """
    logger.warning(f"Se forțează oprirea {container}...")
    
    try:
        rezultat = subprocess.run(
            ["docker", "kill", container],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if rezultat.returncode == 0:
            logger.info(f"✓ {container} oprit forțat")
            return True
        else:
            return False
            
    except Exception as e:
        logger.error(f"Eroare la oprirea forțată: {e}")
        return False


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprește Laboratorul Săptămânii 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python opreste_lab.py              # Oprire grațioasă
  python opreste_lab.py --fortat     # Oprire forțată
  python opreste_lab.py --timeout 60 # Timeout personalizat
        """
    )
    parser.add_argument(
        "--fortat", "-f",
        action="store_true",
        help="Oprire forțată (kill) în loc de oprire grațioasă"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout pentru oprire grațioasă (implicit: 30 secunde)"
    )
    args = parser.parse_args()

    afiseaza_banner()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Oprirea Mediului de Laborator")
    logger.info("=" * 60)

    try:
        # Obține lista containerelor week1_*
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=week1_", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        containere = [c.strip() for c in rezultat.stdout.strip().split("\n") if c.strip()]
        
        if not containere:
            logger.info("Nu există containere de laborator active.")
            return 0
        
        logger.info(f"Se opresc {len(containere)} containere...")
        
        succes_total = True
        for container in containere:
            if args.fortat:
                succes = oprire_fortata(container)
            else:
                succes = oprire_gratiosa(container, args.timeout)
                if not succes:
                    logger.warning(f"Se încearcă oprirea forțată pentru {container}")
                    succes = oprire_fortata(container)
            
            if not succes:
                succes_total = False

        # Oprește și cu docker compose
        logger.info("Se finalizează oprirea cu Docker Compose...")
        docker.compose_down()

        logger.info("")
        logger.info("=" * 60)
        if succes_total:
            logger.info("✓ Toate containerele au fost oprite cu succes")
            logger.info("")
            logger.info("Datele au fost păstrate. Pentru a șterge totul:")
            logger.info("  python scripts/curatare.py --complet")
        else:
            logger.warning("⚠ Unele containere nu s-au oprit corect")
        logger.info("=" * 60)

        return 0 if succes_total else 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
