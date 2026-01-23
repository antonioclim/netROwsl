#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 13
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Acest script oprește toate containerele Docker păstrând datele.

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


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.utilitare_docker import ManagerDocker

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
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 13"
    )
    parser.add_argument("--force", "-f", action="store_true",
                        help="Oprire forțată (timeout 0)")
    args = parser.parse_args()
    
    print("=" * 60)
    print("OPRIRE LABORATOR SĂPTĂMÂNA 13")
    print("(Portainer rămâne activ pe portul 9000)")
    print("=" * 60)
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    try:
        logger.info("Se opresc containerele Docker de laborator...")
        docker.compose_down(volumes=False, timeout=0 if args.force else 10)
        
        # Verifică containerele week13 rămase
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=week13_", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        containere_ramase = [c for c in result.stdout.strip().split('\n') if c]
        
        if not containere_ramase:
            logger.info("✓ Toate containerele de laborator au fost oprite")
        else:
            logger.warning(f"⚠ Containere week13 încă prezente: {containere_ramase}")
        
        # Verifică și afișează status Portainer
        print()
        print("=" * 60)
        print("Oprire finalizată!")
        
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
        
        print("\n  Datele au fost păstrate în volume.")
        print("\n  Pentru curățare completă, rulați:")
        print("  python3 scripts/curata.py --complet")
        print("")
        print("Pentru a reporni: python3 scripts/porneste_lab.py")
        print("=" * 60)
        return 0
        
    except Exception as e:
        logger.error(f"Eroare la oprire: {e}")
        return 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
