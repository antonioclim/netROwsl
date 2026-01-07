#!/usr/bin/env python3
"""
Script de Oprire a Laboratorului Săptămânii 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Oprește toate containerele de laborator păstrând volumele de date.

ADAPTAT PENTRU: WSL2 + Ubuntu 22.04 + Docker (în WSL) + Portainer Global
NOTĂ: Portainer NU este oprit de acest script - rulează global pe portul 9000
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import DockerManager
from scripts.utils.logger import setup_logger

logger = setup_logger("opreste_lab")


def verifica_portainer_ruleaza() -> bool:
    """Verifică dacă Portainer global rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "portainer" in rezultat.stdout.lower()
    except:
        return False


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Oprește Mediul de Laborator Săptămâna 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python scripts/opreste_lab.py              # Oprește containerele de laborator
  python scripts/opreste_lab.py --elimina    # Oprește și elimină containerele
  python scripts/opreste_lab.py --volume     # Elimină și volumele (pierdere date!)

NOTĂ: Portainer rulează global și NU este oprit de acest script.
      Rămâne accesibil la http://localhost:9000
        """
    )
    parser.add_argument(
        "--elimina",
        action="store_true",
        help="Elimină containerele după oprire"
    )
    parser.add_argument(
        "--volume",
        action="store_true",
        help="Elimină și volumele (ATENȚIE: pierdere date!)"
    )
    parser.add_argument(
        "--forta", "-f",
        action="store_true",
        help="Forțează oprirea fără confirmare"
    )
    args = parser.parse_args()

    director_docker = RADACINA_PROIECT / "docker"
    
    try:
        docker = DockerManager(director_docker)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    logger.info("=" * 60)
    logger.info("Oprire Mediu Laborator Săptămâna 1")
    logger.info("Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix")
    logger.info("=" * 60)

    try:
        # Confirmare eliminare volume dacă se solicită
        if args.volume and not args.forta:
            raspuns = input("\n⚠️  ATENȚIE: Aceasta va șterge toate datele laboratorului! Continuați? [d/N]: ")
            if raspuns.lower() != 'd':
                logger.info("Anulat.")
                return 0

        # Oprește containerele
        logger.info("Oprire containere de laborator...")
        
        if args.elimina or args.volume:
            # Folosește docker-compose down
            cmd = ["docker-compose", "-f", str(docker.compose_file), "down"]
            if args.volume:
                cmd.append("-v")
            
            rezultat = subprocess.run(
                cmd,
                cwd=director_docker.parent,
                capture_output=True,
                text=True
            )
            
            if rezultat.returncode != 0:
                logger.error(f"Oprirea containerelor a eșuat: {rezultat.stderr}")
                return 1
        else:
            # Doar oprește containerele (păstrează volumele)
            if not docker.compose_stop():
                logger.error("Oprirea containerelor a eșuat")
                return 1

        logger.info("")
        logger.info("\033[92mContainerele de laborator au fost oprite cu succes.\033[0m")
        
        # Reamintire despre Portainer
        logger.info("")
        logger.info("=" * 60)
        logger.info("NOTĂ: Portainer rulează în continuare (serviciu global)")
        if verifica_portainer_ruleaza():
            logger.info("  Status: \033[92mRULEAZĂ\033[0m la http://localhost:9000")
        else:
            logger.warning("  Status: \033[91mNU RULEAZĂ\033[0m")
        logger.info("")
        logger.info("Portainer este intenționat NEOPRIT pentru a rămâne")
        logger.info("disponibil pentru alte sesiuni de laborator.")
        logger.info("=" * 60)
        
        return 0

    except Exception as e:
        logger.error(f"Oprirea laboratorului a eșuat: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
