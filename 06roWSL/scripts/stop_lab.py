#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 6
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script oprește grațios toate containerele Docker păstrând datele.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("stop_lab")


def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator Săptămâna 6"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout în secunde pentru oprire grațioasă (implicit: 30)"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Forțează oprirea imediată a containerelor"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișare detaliată"
    )
    args = parser.parse_args()
    
    if args.verbose:
        from scripts.utils.logger import set_verbose
        set_verbose(logger, True)
    
    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(f"Configurația Docker nu a fost găsită: {e}")
        return 1
    
    logger.info("=" * 60)
    logger.info("Oprirea mediului de laborator Săptămâna 6")
    logger.info("=" * 60)
    
    try:
        # Afișează starea curentă
        logger.info("Servicii care rulează în prezent:")
        stare = docker.compose_ps()
        for nume, info in stare.items():
            starea_serv = info.get("State", "necunoscută")
            logger.info(f"  {nume}: {starea_serv}")
        
        if not stare:
            logger.info("  Niciun serviciu nu rulează")
            return 0
        
        # Oprește serviciile
        logger.info("")
        if args.force:
            logger.info("Oprire forțată a tuturor containerelor...")
        else:
            logger.info(f"Oprire grațioasă a containerelor (timeout: {args.timeout}s)...")
        
        # docker compose stop păstrează volumele
        import subprocess
        fisier_compose = director_docker / "docker-compose.yml"
        
        cmd = ["docker", "compose", "-f", str(fisier_compose), "stop"]
        if args.timeout:
            cmd.extend(["-t", str(args.timeout)])
        
        rezultat = subprocess.run(cmd, cwd=director_docker)
        
        if rezultat.returncode == 0:
            logger.info("")
            logger.info("=" * 60)
            logger.info("✓ Toate serviciile au fost oprite cu succes")
            logger.info("")
            logger.info("Datele din volume au fost păstrate.")
            logger.info("Pentru a elimina complet containerele: python scripts/cleanup.py")
            logger.info("Pentru a reporni: python scripts/start_lab.py")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Eșec la oprirea unor servicii")
            return 1
    
    except KeyboardInterrupt:
        print("\nOprire întreruptă")
        return 130
    except Exception as e:
        logger.error(f"Eșec la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
