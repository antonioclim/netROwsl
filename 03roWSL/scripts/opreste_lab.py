#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oprește elegant toate containerele de laborator, păstrând datele și volumele.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!

Utilizare:
    python3 scripts/opreste_lab.py [--logs]
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în PATH

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.utilitare_docker import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

PREFIX_WEEK = "week3"

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


def este_container_exclus(nume_container: str) -> bool:
    """Verifică dacă un container este în lista de excluderi."""
    return any(exclus in nume_container.lower() for exclus in CONTAINERE_EXCLUSE)


def afiseaza_loguri_containere():
    """Afișează ultimele log-uri de la fiecare container de laborator."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={PREFIX_WEEK}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        containere = rezultat.stdout.strip().split('\n')
        containere = [c for c in containere if c and not este_container_exclus(c)]
        
        for container in containere:
            print(f"\n{'='*40}")
            print(f"Log-uri: {container}")
            print('='*40)
            subprocess.run(
                ["docker", "logs", "--tail", "20", container]
            )
    except Exception as e:
        logger.warning(f"Nu s-au putut afișa log-urile: {e}")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Oprește Laboratorul Săptămânii 3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python3 opreste_lab.py           # Oprire normală
  python3 opreste_lab.py --logs    # Afișează log-uri înainte de oprire

NOTĂ: Portainer NU este oprit - rulează global pe portul 9000.
        """
    )
    parser.add_argument(
        "--logs",
        action="store_true",
        help="Afișează log-urile containerelor înainte de oprire"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Afișează informații detaliate"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire Laborator Săptămâna 3")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    try:
        # Afișează log-uri dacă este cerut
        if args.logs:
            logger.info("Afișare log-uri containere...")
            afiseaza_loguri_containere()

        # Obține lista containerelor week3_* (exclude portainer)
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={PREFIX_WEEK}", "--format", "{{.Names}}"],
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

        # Oprește containerele
        logger.info("")
        logger.info("Oprire containere...")
        docker.compose_down(volume=False)

        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Laboratorul a fost oprit cu succes!")
        logger.info("")
        
        # Verifică și afișează status Portainer
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează")
        
        logger.info("")
        logger.info("Datele și volumele au fost păstrate.")
        logger.info("Pentru a relua laboratorul:")
        logger.info("  python3 scripts/porneste_lab.py")
        logger.info("")
        logger.info("Pentru curățare completă:")
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
