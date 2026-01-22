#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("curatare")

PREFIX_SAPTAMANA = "week1"


def afiseaza_banner() -> None:
    """Afișează banner-ul de curățare."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  CURĂȚARE LABORATOR SĂPTĂMÂNA 1".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# CURATARE_DIRECTOARE
# ═══════════════════════════════════════════════════════════════════════════════

def curata_directoare_locale(complet: bool, dry_run: bool) -> None:
    """Curăță directoarele locale de artefacte.
    
    Șterge fișierele generate (pcap, artifacts) dar păstrează .gitkeep
    
    Args:
        complet: Curățare completă
        dry_run: Doar simulare
    """
    if not complet:
        return
    
    directoare_de_curatat = [
        RADACINA_PROIECT / "artifacts",
        RADACINA_PROIECT / "pcap",
    ]
    
    for director in directoare_de_curatat:
        if director.exists():
            logger.info(f"Se curăță directorul: {director}")
            for fisier in director.iterdir():
                # Păstrează .gitkeep și README.md
                if fisier.name != ".gitkeep" and fisier.name != "README.md":
                    if dry_run:
                        logger.info(f"  [SIMULARE] S-ar șterge: {fisier}")
                    else:
                        if fisier.is_file():
                            fisier.unlink()
                            logger.info(f"  Șters: {fisier.name}")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIRMARE_UTILIZATOR
# ═══════════════════════════════════════════════════════════════════════════════

def confirma_actiune(mesaj: str) -> bool:
    """Solicită confirmarea utilizatorului.
    
    Args:
        mesaj: Mesajul de confirmare
        
    Returns:
        True dacă utilizatorul confirmă cu 'd' sau 'da'
    """
    raspuns = input(f"\n{mesaj} (d/n): ").strip().lower()
    return raspuns == "d" or raspuns == "da"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_SI_ARGUMENTE
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python curatare.py                 # Curățare de bază
  python curatare.py --complet       # Curățare completă (inclusiv volume)
  python curatare.py --prune         # Curăță și resursele Docker neutilizate
  python curatare.py --dry-run       # Arată ce s-ar șterge fără a șterge
  python curatare.py --da            # Fără confirmare
        """
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
        "--dry-run",
        action="store_true",
        help="Arată ce s-ar elimina fără a elimina efectiv"
    )
    parser.add_argument(
        "--da", "-y",
        action="store_true",
        help="Confirmă automat (fără prompturi)"
    )
    args = parser.parse_args()

    afiseaza_banner()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Curățarea Mediului de Laborator - Săptămâna 1")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[SIMULARE] Nu se vor face modificări reale")

    # ═══════════════════════════════════════════════════════════════════════════
    # CONFIRMARE_CURATARE_COMPLETA
    # ═══════════════════════════════════════════════════════════════════════════

    # Avertisment pentru curățare completă
    if args.complet and not args.dry_run and not args.da:
        logger.warning("")
        logger.warning("⚠ ATENȚIE: Curățarea completă va șterge:")
        logger.warning("  • Toate containerele week1_*")
        logger.warning("  • Toate rețelele week1_*")
        logger.warning("  • Toate volumele week1_*")
        logger.warning("  • Toate fișierele din artifacts/ și pcap/")
        
        if not confirma_actiune("Sigur doriți să continuați?"):
            logger.info("Curățare anulată.")
            return 0

    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTA_CURATARE
    # ═══════════════════════════════════════════════════════════════════════════

    try:
        # Pas 1: Oprește containerele
        logger.info("")
        logger.info("Pas 1: Oprirea containerelor...")
        docker.compose_down(volume=args.complet, dry_run=args.dry_run)

        # Pas 2: Elimină resursele cu prefix
        logger.info("")
        logger.info(f"Pas 2: Eliminarea resurselor {PREFIX_SAPTAMANA}_*...")
        docker.elimina_dupa_prefix(PREFIX_SAPTAMANA, dry_run=args.dry_run)

        # Pas 3: Curăță directoarele locale
        if args.complet:
            logger.info("")
            logger.info("Pas 3: Curățarea directoarelor locale...")
            curata_directoare_locale(args.complet, args.dry_run)

        # Pas 4: Curățare sistem Docker (opțional)
        if args.prune and not args.dry_run:
            logger.info("")
            logger.info("Pas 4: Curățarea resurselor Docker neutilizate...")
            docker.curatare_sistem()

        # ═══════════════════════════════════════════════════════════════════════
        # AFISEAZA_REZULTATE
        # ═══════════════════════════════════════════════════════════════════════

        logger.info("")
        logger.info("=" * 60)
        if args.dry_run:
            logger.info("[SIMULARE] Curățare simulată completă!")
            logger.info("Rulați fără --dry-run pentru a efectua curățarea.")
        else:
            logger.info("✓ Curățare completă!")
            if args.complet:
                logger.info("Sistemul este pregătit pentru următoarea sesiune de laborator.")
        logger.info("=" * 60)
        
        return 0

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
