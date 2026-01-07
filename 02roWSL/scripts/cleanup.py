#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configurează_logger

logger = configurează_logger("cleanup")

PREFIX_SĂPTĂMÂNĂ = "week2"


def curăță_fișiere_locale(dry_run: bool = False) -> None:
    """
    Curăță fișierele locale generate (pcap, artifacts).
    
    Args:
        dry_run: Dacă True, doar afișează ce ar fi șters
    """
    directoare_de_curățat = [
        ("pcap", "*.pcap"),
        ("artifacts", "*"),
    ]
    
    for director, pattern in directoare_de_curățat:
        cale = RĂDĂCINĂ_PROIECT / director
        if not cale.exists():
            continue
        
        fișiere = list(cale.glob(pattern))
        fișiere = [f for f in fișiere if f.is_file() and f.name != ".gitkeep"]
        
        if not fișiere:
            logger.info(f"  Directorul '{director}' este deja curat")
            continue
        
        for fișier in fișiere:
            if dry_run:
                logger.info(f"  [SIMULARE] Ar fi șters: {fișier.name}")
            else:
                try:
                    fișier.unlink()
                    logger.info(f"  Șters: {fișier.name}")
                except Exception as e:
                    logger.warning(f"  Nu s-a putut șterge {fișier.name}: {e}")


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python cleanup.py              # Curățare de bază (oprește containerele)
  python cleanup.py --full       # Curățare completă (șterge și volumele)
  python cleanup.py --dry-run    # Simulare (arată ce ar fi șters)
  python cleanup.py --prune      # Curăță și resursele Docker neutilizate
        """
    )
    parser.add_argument(
        "--full", "-f",
        action="store_true",
        help="Curățare completă: elimină volume și toate datele (pentru săptămâna următoare)"
    )
    parser.add_argument(
        "--prune", "-p",
        action="store_true",
        help="Curăță și resursele Docker neutilizate din sistem"
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Simulare: arată ce ar fi șters fără a șterge efectiv"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Curățare Mediu de Laborator - Săptămâna 2")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[SIMULARE] Nu se vor face modificări reale")
        logger.info("")

    if args.full:
        logger.warning("ATENȚIE: Curățare completă selectată!")
        logger.warning("Toate datele din volume vor fi șterse.")
        
        if not args.dry_run:
            try:
                confirmare = input("Continuați? (da/nu): ").strip().lower()
                if confirmare not in ['da', 'yes', 'd', 'y']:
                    logger.info("Curățare anulată.")
                    return 0
            except (KeyboardInterrupt, EOFError):
                logger.info("\nCurățare anulată.")
                return 0

    try:
        cale_docker = RĂDĂCINĂ_PROIECT / "docker"
        manager = ManagerDocker(cale_docker)

        # Oprire containere
        logger.info("Oprire containere...")
        if not args.dry_run:
            manager.compose_down(volumes=args.full)
        else:
            logger.info("  [SIMULARE] Ar fi oprit containerele")

        # Eliminare resurse cu prefix specific
        logger.info(f"Eliminare resurse {PREFIX_SĂPTĂMÂNĂ}_*...")
        if not args.dry_run:
            manager.elimină_după_prefix(PREFIX_SĂPTĂMÂNĂ)
        else:
            logger.info(f"  [SIMULARE] Ar fi eliminat resursele cu prefix '{PREFIX_SĂPTĂMÂNĂ}'")

        # Curățare fișiere locale
        if args.full:
            logger.info("Curățare fișiere locale...")
            curăță_fișiere_locale(dry_run=args.dry_run)

        # Curățare sistem Docker
        if args.prune:
            logger.info("Curățare resurse Docker neutilizate...")
            if not args.dry_run:
                try:
                    subprocess.run(
                        ["docker", "system", "prune", "-f"],
                        capture_output=True,
                        check=True
                    )
                    logger.info("  Resurse neutilizate eliminate")
                except subprocess.CalledProcessError as e:
                    logger.warning(f"  Avertisment la curățare sistem: {e}")
            else:
                logger.info("  [SIMULARE] Ar fi rulat 'docker system prune -f'")

        logger.info("")
        logger.info("=" * 60)
        
        if args.dry_run:
            logger.info("✓ Simulare completă (nu s-au făcut modificări)")
        else:
            logger.info("✓ Curățare completă!")
            if args.full:
                logger.info("")
                logger.info("Sistemul este pregătit pentru săptămâna următoare.")
        
        logger.info("=" * 60)
        return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
