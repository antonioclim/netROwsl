#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest script oprește toate containerele Docker păstrând datele.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import socket
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului în path

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_laborator")

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

# Containere care NU trebuie oprite (rulează global)
CONTAINERE_EXCLUSE = ["portainer"]



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

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



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator Săptămâna 5",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Acest script oprește containerele păstrând volumele și datele.
Pentru curățare completă, utilizați: python3 scripts/curata.py --complet

NOTĂ: Portainer NU este oprit - rulează global pe portul 9000.
        """
    )
    parser.add_argument(
        "--fortat",
        action="store_true",
        help="Oprește forțat containerele (kill în loc de stop)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=10,
        help="Timeout în secunde pentru oprirea grațioasă (implicit: 10)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Afișează informații detaliate"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire mediu de laborator Săptămâna 5")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        # Verifică că nu oprim Portainer
        logger.info("Se opresc containerele de laborator...")
        logger.info("(Portainer va rămâne activ)")
        
        if args.fortat:
            logger.info("Oprire forțată a containerelor...")
            docker.compose_kill()
        else:
            logger.info(f"Oprire grațioasă (timeout: {args.timeout}s)...")
            docker.compose_stop(timeout=args.timeout)

        logger.info("=" * 60)
        logger.info("✓ Mediul de laborator a fost oprit.")
        logger.info("")
        
        # Verifică și afișează status Portainer
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
        
        logger.info("")
        logger.info("Datele au fost păstrate. Pentru a reporni:")
        logger.info("  python3 scripts/porneste_laborator.py")
        logger.info("")
        logger.info("Pentru curățare completă înainte de săptămâna următoare:")
        logger.info("  python3 scripts/curata.py --complet")
        logger.info("=" * 60)
        return 0

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
