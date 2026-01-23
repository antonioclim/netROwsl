#!/usr/bin/env python3
"""
Script de Curățare a Laboratorului Săptămânii 12
================================================
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix
"""

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTURI_SI_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Tuple

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.docker_utils import ManagerDocker
from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("curata")

PREFIX_LABORATOR = "week12_"
RESURSE_PROTEJATE = ["portainer", "portainer_data"]

# ═══════════════════════════════════════════════════════════════════════════════
# LISTARE_RESURSE
# ═══════════════════════════════════════════════════════════════════════════════
def listeaza_containere_laborator() -> List[str]:
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={PREFIX_LABORATOR}", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=10)
        containere = result.stdout.strip().split('\n')
        return [c for c in containere if c and c not in RESURSE_PROTEJATE]
    except Exception:
        return []

def listeaza_volume_laborator() -> List[str]:
    try:
        result = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={PREFIX_LABORATOR}", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=10)
        volume = result.stdout.strip().split('\n')
        return [v for v in volume if v and v not in RESURSE_PROTEJATE]
    except Exception:
        return []

# ═══════════════════════════════════════════════════════════════════════════════
# STERGERE_RESURSE
# ═══════════════════════════════════════════════════════════════════════════════
def sterge_containere(containere: List[str]) -> Tuple[int, int]:
    succes, esec = 0, 0
    for container in containere:
        try:
            result = subprocess.run(["docker", "rm", "-f", container], capture_output=True, timeout=30)
            if result.returncode == 0:
                logger.info(f"  ✓ Șters container: {container}")
                succes += 1
            else:
                esec += 1
        except Exception:
            esec += 1
    return succes, esec

# ═══════════════════════════════════════════════════════════════════════════════
# CURATARE_COMPLETA
# ═══════════════════════════════════════════════════════════════════════════════
def curata_complet(docker: ManagerDocker) -> bool:
    logger.info("Curățare completă...")
    try:
        docker.compune_down(volumes=True)
    except Exception as e:
        logger.warning(f"Eroare la compose down: {e}")
    
    containere = listeaza_containere_laborator()
    if containere:
        sterge_containere(containere)
    
    logger.info("Curățare finalizată")
    return True

# ═══════════════════════════════════════════════════════════════════════════════
# PARSEAZA_ARGUMENTE
# ═══════════════════════════════════════════════════════════════════════════════
def parseaza_argumente() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Curățare Laborator Săptămâna 12")
    parser.add_argument("--complet", action="store_true", help="Curățare completă")
    parser.add_argument("--lista", action="store_true", help="Doar listează resursele")
    parser.add_argument("--forta", action="store_true", help="Nu cere confirmare")
    return parser.parse_args()

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════
def main() -> int:
    args = parseaza_argumente()
    logger.info("Curățare Laborator - Săptămâna 12")
    
    if args.lista:
        containere = listeaza_containere_laborator()
        print(f"Containere: {containere}")
        return 0
    
    if not args.forta and args.complet:
        print("\n⚠️  ATENȚIE: Aceasta va șterge toate resursele laboratorului!")
        confirmare = input("Continuați? [y/N]: ").strip().lower()
        if confirmare != 'y':
            logger.info("Anulat.")
            return 0
    
    docker = ManagerDocker(RADACINA_PROIECT / "docker")
    curata_complet(docker)
    
    print("\nNOTĂ: Portainer NU a fost afectat.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
