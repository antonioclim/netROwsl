#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script oprește toate containerele Docker de laborator păstrând datele.

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

# Adăugare rădăcină proiect la cale

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configurează_logger

logger = configurează_logger("stop_lab")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

# Containere care NU trebuie oprite (rulează global)
CONTAINERE_EXCLUSE = ["portainer"]



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def verifică_portainer_status() -> bool:
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



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python3 stop_lab.py           # Oprire normală (păstrează datele)
  python3 stop_lab.py --timeout 30  # Așteptare 30 secunde înainte de forțare

NOTĂ: Portainer NU este oprit - rulează global pe portul 9000.
        """
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Secunde de așteptat pentru oprire grațioasă (implicit: 10)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire Mediu de Laborator - Săptămâna 2")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    try:
        cale_docker = RĂDĂCINĂ_PROIECT / "docker"
        manager = ManagerDocker(cale_docker)

        # Obține lista containerelor week2_* (exclude portainer)
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=week2_", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        containere = [
            c.strip() for c in rezultat.stdout.strip().split("\n") 
            if c.strip() and not este_container_exclus(c.strip())
        ]
        
        if not containere:
            logger.info("Nu există containere de laborator active.")
        else:
            logger.info(f"Se opresc {len(containere)} containere de laborator...")
            logger.info("(Portainer va rămâne activ)")
            logger.info(f"  (timeout: {args.timeout} secunde)")

        # Oprire cu docker compose
        logger.info("")
        logger.info("Oprire containere...")
        manager.compose_down(timeout=args.timeout)

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Toate containerele de laborator au fost oprite.")
        logger.info("")
        
        # Verifică și afișează status Portainer
        if verifică_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează")
        
        logger.info("")
        logger.info("Datele au fost păstrate. Pentru a relua laboratorul:")
        logger.info("  python3 scripts/start_lab.py")
        logger.info("")
        logger.info("Pentru curățare completă (înainte de săptămâna următoare):")
        logger.info("  python3 scripts/cleanup.py --full")
        logger.info("=" * 60)
        
        return 0

    except KeyboardInterrupt:
        logger.info("\nÎntrerupt de utilizator.")
        return 130
    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
