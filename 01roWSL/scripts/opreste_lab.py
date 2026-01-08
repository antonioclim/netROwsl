#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script oprește toate containerele de laborator în mod controlat, păstrând datele.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

from __future__ import annotations

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

# Containere care NU trebuie oprite (rulează global)
CONTAINERE_EXCLUSE = ["portainer"]


def afiseaza_banner() -> None:
    """Afișează banner-ul de oprire."""
    print()
    print("╔" + "═" * 58 + "╗")
    print("║" + "  OPRIRE LABORATOR SĂPTĂMÂNA 1".center(58) + "║")
    print("║" + "  (Portainer rămâne activ pe portul 9000)".center(58) + "║")
    print("╚" + "═" * 58 + "╝")
    print()


def verifica_portainer_status() -> bool:
    """Verifică dacă Portainer rulează pe portul 9000."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--filter", "name=portainer", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if rezultat.returncode == 0 and "Up" in rezultat.stdout:
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


def este_container_exclus(nume_container: str) -> bool:
    """Verifică dacă un container este în lista de excluderi."""
    return any(exclus in nume_container.lower() for exclus in CONTAINERE_EXCLUSE)


def oprire_gratiosa(container: str, timeout: int = 30) -> bool:
    """Oprește un container în mod grațios.
    
    Args:
        container: Numele containerului
        timeout: Timpul de așteptare înainte de forțare
        
    Returns:
        True dacă oprirea a reușit
    """
    # Verifică dacă containerul este exclus
    if este_container_exclus(container):
        logger.info(f"  [SKIP] {container} - rulează global, nu se oprește")
        return True
    
    logger.info(f"Se oprește {container}...")
    
    try:
        # Mai întâi încearcă oprire grațioasă
        rezultat = subprocess.run(
            ["docker", "stop", "-t", str(timeout), container],
            capture_output=True,
            text=True,
            timeout=timeout + 10
        )
        
        if rezultat.returncode == 0:
            logger.info(f"✓ {container} oprit cu succes")
            return True
        else:
            logger.warning(f"Oprire grațioasă eșuată: {rezultat.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        logger.warning(f"Timeout la oprirea {container}")
        return False
    except Exception as e:
        logger.error(f"Eroare la oprirea {container}: {e}")
        return False


def oprire_fortata(container: str) -> bool:
    """Forțează oprirea unui container.
    
    Args:
        container: Numele containerului
        
    Returns:
        True dacă oprirea a reușit
    """
    # Verifică dacă containerul este exclus
    if este_container_exclus(container):
        logger.info(f"  [SKIP] {container} - rulează global, nu se oprește")
        return True
    
    logger.warning(f"Se forțează oprirea {container}...")
    
    try:
        rezultat = subprocess.run(
            ["docker", "kill", container],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if rezultat.returncode == 0:
            logger.info(f"✓ {container} oprit forțat")
            return True
        else:
            return False
            
    except Exception as e:
        logger.error(f"Eroare la oprirea forțată: {e}")
        return False


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprește Laboratorul Săptămânii 1",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python3 opreste_lab.py              # Oprire grațioasă
  python3 opreste_lab.py --fortat     # Oprire forțată
  python3 opreste_lab.py --timeout 60 # Timeout personalizat

NOTĂ: Portainer NU este oprit - rulează global pe portul 9000.
        """
    )
    parser.add_argument(
        "--fortat", "-f",
        action="store_true",
        help="Oprire forțată (kill) în loc de oprire grațioasă"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=30,
        help="Timeout pentru oprire grațioasă (implicit: 30 secunde)"
    )
    args = parser.parse_args()

    afiseaza_banner()

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    logger.info("=" * 60)
    logger.info("Oprirea Mediului de Laborator")
    logger.info("(Portainer rămâne activ)")
    logger.info("=" * 60)

    try:
        # Obține lista containerelor week1_* (exclude portainer)
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=week1_", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        containere = [
            c.strip() for c in rezultat.stdout.strip().split("\n") 
            if c.strip() and not este_container_exclus(c.strip())
        ]
        
        if not containere:
            logger.info("Nu există containere de laborator active.")
            
            # Verifică status Portainer
            if verifica_portainer_status():
                logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
            else:
                logger.warning(f"⚠ Portainer nu rulează")
            
            return 0
        
        logger.info(f"Se opresc {len(containere)} containere de laborator...")
        logger.info("(Portainer va rămâne activ)")
        logger.info("")
        
        succes_total = True
        for container in containere:
            if args.fortat:
                succes = oprire_fortata(container)
            else:
                succes = oprire_gratiosa(container, args.timeout)
                if not succes:
                    logger.warning(f"Se încearcă oprirea forțată pentru {container}")
                    succes = oprire_fortata(container)
            
            if not succes:
                succes_total = False

        # Oprește și cu docker compose (va ignora portainer care nu e definit)
        logger.info("")
        logger.info("Se finalizează oprirea cu Docker Compose...")
        docker.compose_down()

        logger.info("")
        logger.info("=" * 60)
        if succes_total:
            logger.info("✓ Toate containerele de laborator au fost oprite cu succes")
        else:
            logger.warning("⚠ Unele containere nu s-au oprit corect")
        
        logger.info("")
        
        # Verifică și afișează status Portainer
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează")
        
        logger.info("")
        logger.info("Datele au fost păstrate. Pentru a șterge totul:")
        logger.info("  python3 scripts/curatare.py --complet")
        logger.info("")
        logger.info("Pentru a reporni laboratorul:")
        logger.info("  python3 scripts/porneste_lab.py")
        logger.info("=" * 60)

        return 0 if succes_total else 1

    except KeyboardInterrupt:
        logger.warning("\nÎntrerupt de utilizator")
        return 130
    except Exception as e:
        logger.error(f"Eroare neașteptată: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
