#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.

Utilizare:
    python scripts/curata.py [--complet] [--prune] [--dry-run]
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

logger = configureaza_logger("curata")

PREFIX_WEEK = "week3"


def curata_artefacte(dry_run: bool = False) -> None:
    """Curăță fișierele generate din directoarele artifacts și pcap."""
    directoare = [
        RADACINA_PROIECT / "artifacts",
        RADACINA_PROIECT / "pcap"
    ]
    
    for director in directoare:
        if not director.exists():
            continue
            
        for fisier in director.iterdir():
            if fisier.name.startswith('.'):  # Păstrează .gitkeep
                continue
            
            if dry_run:
                logger.info(f"  [DRY-RUN] Ar șterge: {fisier}")
            else:
                try:
                    if fisier.is_file():
                        fisier.unlink()
                        logger.info(f"  Șters: {fisier.name}")
                    elif fisier.is_dir():
                        import shutil
                        shutil.rmtree(fisier)
                        logger.info(f"  Șters director: {fisier.name}")
                except Exception as e:
                    logger.warning(f"  Nu s-a putut șterge {fisier}: {e}")


def curata_resurse_docker(prefix: str, dry_run: bool = False) -> None:
    """Curăță resursele Docker cu prefixul specificat."""
    
    # Curăță containerele
    logger.info("Căutare containere...")
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
            capture_output=True
        )
        containere = [c for c in rezultat.stdout.decode().strip().split('\n') if c]
        
        for container in containere:
            if dry_run:
                logger.info(f"  [DRY-RUN] Ar elimina containerul: {container}")
            else:
                subprocess.run(["docker", "rm", "-f", container], capture_output=True)
                logger.info(f"  Eliminat container: {container}")
    except Exception as e:
        logger.warning(f"Eroare la curățarea containerelor: {e}")
    
    # Curăță rețelele
    logger.info("Căutare rețele...")
    try:
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True
        )
        retele = [r for r in rezultat.stdout.decode().strip().split('\n') if r]
        
        for retea in retele:
            if dry_run:
                logger.info(f"  [DRY-RUN] Ar elimina rețeaua: {retea}")
            else:
                subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                logger.info(f"  Eliminată rețea: {retea}")
    except Exception as e:
        logger.warning(f"Eroare la curățarea rețelelor: {e}")
    
    # Curăță volumele
    logger.info("Căutare volume...")
    try:
        rezultat = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True
        )
        volume = [v for v in rezultat.stdout.decode().strip().split('\n') if v]
        
        for volum in volume:
            if dry_run:
                logger.info(f"  [DRY-RUN] Ar elimina volumul: {volum}")
            else:
                subprocess.run(["docker", "volume", "rm", volum], capture_output=True)
                logger.info(f"  Eliminat volum: {volum}")
    except Exception as e:
        logger.warning(f"Eroare la curățarea volumelor: {e}")


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 3"
    )
    parser.add_argument(
        "--complet",
        action="store_true",
        help="Elimină și volumele și toate datele (folosiți înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Curăță și resursele Docker neutilizate din sistem"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Afișează ce ar fi eliminat fără a efectua modificări"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Curățare Laborator Săptămâna 3")
    logger.info("=" * 60)

    if args.dry_run:
        logger.info("[DRY-RUN] Nu se vor efectua modificări reale")
        logger.info("")

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        # Oprește containerele prin compose
        logger.info("Oprire containere prin Docker Compose...")
        if not args.dry_run:
            docker.compose_down(volume=args.complet)
        else:
            logger.info("  [DRY-RUN] Ar opri containerele")

        # Curăță resursele cu prefixul week3
        logger.info(f"\nCurățare resurse {PREFIX_WEEK}_*...")
        curata_resurse_docker(PREFIX_WEEK, dry_run=args.dry_run)

        # Curăță artefactele dacă este curățare completă
        if args.complet:
            logger.info("\nCurățare artefacte și capturi...")
            curata_artefacte(dry_run=args.dry_run)

        # Prune sistem dacă este cerut
        if args.prune and not args.dry_run:
            logger.info("\nCurățare resurse Docker neutilizate...")
            subprocess.run(["docker", "system", "prune", "-f"], capture_output=True)
            logger.info("  Curățare completată")

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Curățare finalizată!")
        if args.complet:
            logger.info("  Sistemul este pregătit pentru următoarea sesiune de laborator.")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la curățare: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
