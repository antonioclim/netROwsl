#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""

import subprocess
import sys
import argparse
from pathlib import Path
import shutil

# Adaugă rădăcina proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("cleanup")

PREFIX_SAPTAMANA = "week4"


def curata_cache_python():
    """Șterge fișierele cache Python."""
    fisiere_sterse = 0
    directoare_sterse = 0
    
    # Șterge directoare __pycache__
    for cale in RADACINA_PROIECT.rglob("__pycache__"):
        try:
            shutil.rmtree(cale)
            directoare_sterse += 1
        except Exception:
            pass
    
    # Șterge fișiere .pyc
    for cale in RADACINA_PROIECT.rglob("*.pyc"):
        try:
            cale.unlink()
            fisiere_sterse += 1
        except Exception:
            pass
    
    return fisiere_sterse, directoare_sterse


def curata_directoare_temporare(complet: bool = False):
    """Curăță directoarele artifacts și pcap."""
    fisiere_sterse = 0
    
    # Curăță artifacts/
    dir_artifacts = RADACINA_PROIECT / "artifacts"
    if dir_artifacts.exists():
        for fisier in dir_artifacts.iterdir():
            if fisier.name != ".gitkeep":
                try:
                    if fisier.is_dir():
                        shutil.rmtree(fisier)
                    else:
                        fisier.unlink()
                    fisiere_sterse += 1
                except Exception as e:
                    logger.warning(f"Nu s-a putut șterge {fisier}: {e}")
    
    # Curăță pcap/ (doar la curățare completă)
    if complet:
        dir_pcap = RADACINA_PROIECT / "pcap"
        if dir_pcap.exists():
            for fisier in dir_pcap.glob("*.pcap"):
                try:
                    fisier.unlink()
                    fisiere_sterse += 1
                except Exception as e:
                    logger.warning(f"Nu s-a putut șterge {fisier}: {e}")
    
    return fisiere_sterse


def curata_docker(complet: bool = False, dry_run: bool = False):
    """Curăță resursele Docker."""
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    # Oprește containerele
    logger.info("Oprire containere...")
    if not dry_run:
        docker.compose_down(volumes=complet)
    else:
        logger.info("  [SIMULARE] ar opri containerele")
    
    # Elimină resurse cu prefix week4
    logger.info(f"Eliminare resurse {PREFIX_SAPTAMANA}_*...")
    if not dry_run:
        docker.elimina_dupa_prefix(PREFIX_SAPTAMANA)
    else:
        # Listează ce ar fi eliminat
        try:
            # Containere
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "--filter", f"name={PREFIX_SAPTAMANA}", "-q"],
                capture_output=True
            )
            if rezultat.stdout:
                logger.info(f"  [SIMULARE] ar elimina containere: {rezultat.stdout.decode().strip()}")
            
            # Rețele
            rezultat = subprocess.run(
                ["docker", "network", "ls", "--filter", f"name={PREFIX_SAPTAMANA}", "-q"],
                capture_output=True
            )
            if rezultat.stdout:
                logger.info(f"  [SIMULARE] ar elimina rețele")
            
            # Volume (doar la complet)
            if complet:
                rezultat = subprocess.run(
                    ["docker", "volume", "ls", "--filter", f"name={PREFIX_SAPTAMANA}", "-q"],
                    capture_output=True
                )
                if rezultat.stdout:
                    logger.info(f"  [SIMULARE] ar elimina volume")
        except Exception:
            pass


def prune_docker(dry_run: bool = False):
    """Curăță resursele Docker nefolosite."""
    logger.info("Curățare resurse Docker nefolosite...")
    
    if dry_run:
        logger.info("  [SIMULARE] ar executa 'docker system prune'")
        return
    
    try:
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True,
            timeout=60
        )
        logger.info("  ✓ Curățare Docker completă")
    except Exception as e:
        logger.warning(f"  Eroare la curățare Docker: {e}")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 4",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python scripts/cleanup.py             # Curățare de bază
  python scripts/cleanup.py --full      # Curățare completă (inclusiv volume)
  python scripts/cleanup.py --dry-run   # Simulare (fără modificări)
  python scripts/cleanup.py --prune     # Include și 'docker system prune'
        """
    )
    parser.add_argument("--full", action="store_true",
                        help="Eliminare volume și toate datele (folosiți înainte de săptămâna următoare)")
    parser.add_argument("--prune", action="store_true",
                        help="Curăță și resursele Docker nefolosite")
    parser.add_argument("--dry-run", action="store_true",
                        help="Afișează ce ar fi eliminat fără a face modificări")
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("Curățare Mediu Laborator Săptămâna 4")
    logger.info("=" * 60)
    
    if args.dry_run:
        logger.info("[MOD SIMULARE] Nicio modificare nu va fi efectuată")
    
    # Curăță Docker
    curata_docker(args.full, args.dry_run)
    
    # Curăță cache Python
    if not args.dry_run:
        logger.info("\nCurățare cache Python...")
        fisiere, directoare = curata_cache_python()
        logger.info(f"  {fisiere} fișiere, {directoare} directoare șterse")
    
    # Curăță directoare temporare
    if args.full and not args.dry_run:
        logger.info("\nCurățare directoare temporare...")
        fisiere = curata_directoare_temporare(complet=True)
        logger.info(f"  {fisiere} fișiere șterse")
    
    # Prune Docker (opțional)
    if args.prune:
        prune_docker(args.dry_run)
    
    logger.info("\n" + "=" * 60)
    logger.info("Curățare completă!")
    if args.full:
        logger.info("Sistemul este pregătit pentru următoarea sesiune de laborator.")
    logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
