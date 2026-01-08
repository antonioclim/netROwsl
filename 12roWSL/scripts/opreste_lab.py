#!/usr/bin/env python3
"""
Script de Oprire a Laboratorului Săptămânii 12
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Oprește grațios toate containerele de laborator.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

import subprocess
import sys
import argparse
import socket
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"


def verifica_portainer_status() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and "Up" in result.stdout:
            return True
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex(('localhost', PORTAINER_PORT))
            sock.close()
            return result == 0
        except Exception:
            return False
            
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 12"
    )
    parser.add_argument(
        "--volume", "-v",
        action="store_true",
        help="Elimină și volumele (datele persistente)"
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Forțează oprirea imediată"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Oprire Mediu de Laborator - Săptămâna 12")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    try:
        if args.fortat:
            logger.info("Oprire forțată a containerelor...")
            subprocess.run(
                ["docker", "compose", "kill"],
                cwd=RADACINA_PROIECT / "docker",
                capture_output=True
            )
        
        logger.info("Oprire grațioasă a containerelor de laborator...")
        docker.compune_down(volume=args.volume)

        # Verifică containerele week12 rămase
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=week12_", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        containere_ramase = [c for c in result.stdout.strip().split('\n') if c]
        
        if not containere_ramase:
            logger.info("✓ Toate containerele de laborator au fost oprite")
        else:
            logger.warning(f"⚠ Containere week12 încă prezente: {containere_ramase}")

        # Verifică și afișează status Portainer
        print()
        logger.info("=" * 60)
        logger.info("Oprire finalizată!")
        
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
        
        if args.volume:
            logger.info("  Volumele au fost de asemenea eliminate.")
        else:
            logger.info("  Volumele au fost păstrate.")
            logger.info("  Pentru curățare completă: python3 scripts/curata.py --complet")
        
        logger.info("")
        logger.info("Pentru a reporni: python3 scripts/porneste_lab.py")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
