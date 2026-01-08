#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest script oprește toate containerele Docker pentru laborator.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

import subprocess
import sys
import argparse
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("stop_lab")

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
        description="Oprește mediul de laborator pentru Săptămâna 11"
    )
    parser.add_argument(
        "--force", "--forta", "-f",
        action="store_true",
        help="Forțează oprirea (kill în loc de stop)"
    )
    parser.add_argument(
        "--volumes", "--volume", "-v",
        action="store_true",
        help="Elimină și volumele (datele persistente)"
    )
    args = parser.parse_args()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Oprire Mediu Laborator Săptămâna 11")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    try:
        # Oprește containerele
        logger.info("Oprire containere de laborator...")
        docker.compose_down(volumes=args.volumes)

        # Verifică oprirea
        containere_ramase = docker.obtine_containere_rulare()
        containere_s11 = [c for c in containere_ramase if c.startswith("s11_")]
        
        if not containere_s11:
            logger.info("✓ Toate containerele de laborator au fost oprite")
        else:
            logger.warning(f"⚠ Containere încă active: {containere_s11}")
            
            if args.force:
                logger.info("Forțare oprire containere rămase...")
                for container in containere_s11:
                    subprocess.run(
                        ["docker", "kill", container],
                        capture_output=True
                    )
                logger.info("✓ Containere oprite forțat")

        # Verifică și afișează status Portainer
        print()
        logger.info("=" * 60)
        logger.info("Oprire finalizată!")
        
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
        
        if args.volumes:
            logger.info("Volumele au fost eliminate.")
        else:
            logger.info("Volumele au fost păstrate. Folosiți --volumes pentru eliminare.")
        
        logger.info("")
        logger.info("Pentru a reporni: python3 scripts/start_lab.py")
        logger.info("=" * 60)
        return 0

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
