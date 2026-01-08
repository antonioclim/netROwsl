#!/usr/bin/env python3
"""
Opritor Laborator Săptămâna 9
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script oprește grațios toate containerele Docker,
păstrând datele și volumele pentru utilizare ulterioară.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

import sys
import argparse
import socket
import subprocess
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger, afiseaza_banner

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
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator pentru Săptămâna 9"
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Forțează oprirea containerelor"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Timpul de așteptare pentru oprire grațioasă (secunde)"
    )
    args = parser.parse_args()

    afiseaza_banner(
        "Oprire Mediu de Laborator",
        "Săptămâna 9 - Nivelul Sesiune și Prezentare",
        "(Portainer rămâne activ pe portul 9000)"
    )

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        logger.info("Se opresc containerele de laborator...")
        logger.info("(Portainer va rămâne activ, datele și volumele vor fi păstrate)")
        
        # Oprește serviciile fără a elimina volumele
        succes = docker.compose_down(volume=False)

        if succes:
            print()
            logger.info("=" * 60)
            logger.info("✓ Toate containerele de laborator au fost oprite cu succes!")
            
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
            logger.error("Eroare la oprirea containerelor.")
            logger.error("Încercați cu --fortat sau verificați manual.")
            return 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
