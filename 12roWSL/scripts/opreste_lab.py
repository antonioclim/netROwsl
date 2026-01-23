#!/usr/bin/env python3
"""
Script de Oprire a Laboratorului Săptămânii 12
==============================================
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("opreste_lab")

# ═══════════════════════════════════════════════════════════════════════════════
# VERIFICARE_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════
def verifica_docker_disponibil() -> bool:
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        return result.returncode == 0
    except Exception:
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# OPRIRE_CONTAINERE
# ═══════════════════════════════════════════════════════════════════════════════
def opreste_containere(docker: ManagerDocker, forta: bool = False) -> bool:
    logger.info("Se opresc containerele laboratorului...")
    try:
        if forta:
            docker.compune_down(volumes=False)
        else:
            docker.compune_stop()
        logger.info("✓ Containerele au fost oprite")
        return True
    except Exception as e:
        logger.error(f"Eroare: {e}")
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# AFISARE_STATUS
# ═══════════════════════════════════════════════════════════════════════════════
def afiseaza_status_final() -> None:
    print("\n" + "=" * 60)
    print("Starea Finală")
    print("=" * 60)
    try:
        result = subprocess.run(
            ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}"],
            capture_output=True, text=True, timeout=10)
        print(result.stdout)
    except Exception:
        pass
    print("\nNOTĂ: Portainer rămâne activ la http://localhost:9000")
    print("=" * 60)

# ═══════════════════════════════════════════════════════════════════════════════
# PARSEAZA_ARGUMENTE
# ═══════════════════════════════════════════════════════════════════════════════
def parseaza_argumente() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Oprire Laborator Săptămâna 12")
    parser.add_argument("--forta", action="store_true", help="Forțează oprirea")
    parser.add_argument("--status", action="store_true", help="Doar status")
    return parser.parse_args()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parseaza_argumente()
    logger.info("Oprire Laborator - Săptămâna 12")
    
    if not verifica_docker_disponibil():
        logger.error("Docker nu este disponibil!")
        return 1
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    
    if args.status:
        afiseaza_status_final()
        return 0
    
    if not opreste_containere(docker, forta=args.forta):
        return 1
    
    afiseaza_status_final()
    logger.info("Pentru curățare completă: python3 scripts/curata.py --complet")
    return 0

if __name__ == "__main__":
    sys.exit(main())
