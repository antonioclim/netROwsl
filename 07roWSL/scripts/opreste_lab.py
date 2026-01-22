#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest script oprește grațios toate containerele de laborator,
păstrând artefactele și datele colectate.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU — Importuri și configurare căi
# ═══════════════════════════════════════════════════════════════════════════════

from __future__ import annotations

import argparse
import subprocess
import sys
import socket
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

# ═══════════════════════════════════════════════════════════════════════════════
# DEFINIRE_CONFIGURATIE — Servicii excluse, credențiale
# ═══════════════════════════════════════════════════════════════════════════════

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

# Containere care NU trebuie oprite (rulează global)
CONTAINERE_EXCLUSE = ["portainer"]


# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICA_PREREQUISITE — Status Portainer
# ═══════════════════════════════════════════════════════════════════════════════

def verifica_portainer_status() -> bool:
    """
    Verifică dacă Portainer rulează pe portul 9000.
    
    Returns:
        True dacă Portainer este accesibil, False altfel
    """
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
# CONFIRMARE_UTILIZATOR — Cerere confirmare înainte de oprire
# ═══════════════════════════════════════════════════════════════════════════════

def cere_confirmare(args) -> bool:
    """
    Solicită confirmare de la utilizator pentru oprirea containerelor.
    
    Args:
        args: Argumente linie de comandă
        
    Returns:
        True dacă utilizatorul confirmă sau --force este activ, False altfel
    """
    if args.force:
        return True
        
    print()
    if args.volume:
        print("ATENȚIE: Această operațiune va elimina și volumele Docker!")
        print("         Toate datele salvate în volume vor fi pierdute.")
        print()
    
    raspuns = input("Doriți să continuați? (da/nu): ").strip().lower()
    return raspuns in ("da", "d", "yes", "y")


# ═══════════════════════════════════════════════════════════════════════════════
# OPRESTE_SERVICII — Compose down, cleanup
# ═══════════════════════════════════════════════════════════════════════════════

def opreste_containere(docker: ManagerDocker, elimina_volume: bool) -> bool:
    """
    Oprește containerele de laborator.
    
    Args:
        docker: Instanță ManagerDocker
        elimina_volume: True pentru a elimina și volumele
        
    Returns:
        True dacă oprirea a reușit, False altfel
    """
    logger.info("Oprire containere de laborator...")
    logger.info("(Portainer va rămâne activ)")
    return docker.compose_down(volumes=elimina_volume)


# ═══════════════════════════════════════════════════════════════════════════════
# AFISEAZA_REZULTATE — Status final
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_rezultat_oprire(succes: bool, volume_eliminate: bool) -> None:
    """
    Afișează rezultatul operațiunii de oprire.
    
    Args:
        succes: True dacă oprirea a reușit
        volume_eliminate: True dacă volumele au fost eliminate
    """
    if succes:
        logger.info("")
        logger.info("=" * 60)
        logger.info("✓ Containerele de laborator au fost oprite cu succes")
        
        # Verifică și afișează status Portainer
        if verifica_portainer_status():
            logger.info(f"✓ Portainer continuă să ruleze pe {PORTAINER_URL}")
        else:
            logger.warning(f"⚠ Portainer nu rulează pe {PORTAINER_URL}")
        
        if not volume_eliminate:
            logger.info("")
            logger.info("Notă: Volumele au fost păstrate")
            logger.info("      Pentru curățare completă: python3 scripts/curata.py --complet")
        logger.info("=" * 60)
    else:
        logger.error("Eroare la oprirea containerelor")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN — Punct de intrare, parsare argumente
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator pentru Săptămâna 7"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Oprire forțată fără confirmare"
    )
    parser.add_argument(
        "--volume", "-v",
        action="store_true",
        help="Elimină și volumele Docker (atenție: șterge datele)"
    )
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("Oprire Mediu Laborator Săptămâna 7")
    logger.info("(Portainer rămâne activ pe portul 9000)")
    logger.info("=" * 60)

    docker = ManagerDocker(RADACINA_PROIECT / "docker")

    # Confirmare dacă nu e forțată
    if not cere_confirmare(args):
        logger.info("Operațiune anulată de utilizator")
        return 0

    try:
        ok = opreste_containere(docker, args.volume)
        afiseaza_rezultat_oprire(ok, args.volume)
        return 0 if ok else 1

    except Exception as e:
        logger.error(f"Eroare la oprirea laboratorului: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
