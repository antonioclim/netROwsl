#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 10
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script oprește toate containerele Docker păstrând volumele de date.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import socket
from pathlib import Path

# Adaugă rădăcina proiectului la calea Python

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

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



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală de oprire."""
    parser = argparse.ArgumentParser(
        description="Oprește Laboratorul Săptămânii 10"
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Oprire forțată (kill în loc de stop)"
    )
    args = parser.parse_args()

    print()
    logger.info("=" * 60)
    logger.info("Oprire Laborator Săptămâna 10")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    try:
        docker = ManagerDocker(RADACINA_PROIECT / "docker")
    except FileNotFoundError as e:
        logger.error(f"Eroare: {e}")
        return 1

    try:
        logger.info("Oprire containere de laborator (datele vor fi păstrate)...")
        
        succes = docker.compose_down(volume=False)
        
        if succes:
            print()
            logger.info("=" * 60)
            logger.info("✓ Toate containerele de laborator au fost oprite!")
            
            # Verifică și afișează status Portainer
            if verifica_portainer_status():
                logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
            else:
                logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
            
            logger.info("")
            logger.info("Volumele de date au fost păstrate.")
            logger.info("Pentru a reporni: python3 scripts/porneste_lab.py")
            logger.info("")
            logger.info("Pentru curățare completă (șterge și datele):")
            logger.info("  python3 scripts/curata.py --complet")
            logger.info("=" * 60)
            return 0
        else:
            logger.error("Oprirea containerelor a eșuat")
            return 1

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare la oprire: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
