#!/usr/bin/env python3
"""
Script de Oprire Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Oprește mediul de laborator într-un mod curat.

Utilizare:
    python3 scripts/stop_lab.py [--remove-volumes]

Opțiuni:
    --remove-volumes    Șterge și volumele Docker (date persistente)
"""

import subprocess
import sys
import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# IMPORTS_AND_CONFIGURATION
# Scop: Încarcă dependențele și setează constantele
# Transferabil la: Orice script Python care folosește module externe
# ═══════════════════════════════════════════════════════════════════════════════

SCRIPT_DIR = Path(__file__).parent.absolute()
BASE_DIR = SCRIPT_DIR.parent
DOCKER_DIR = BASE_DIR / "docker"
COMPOSE_FILE = DOCKER_DIR / "docker-compose.yml"


# ═══════════════════════════════════════════════════════════════════════════════
# SERVICE_SHUTDOWN
# Scop: Oprește containerele în mod controlat
# Transferabil la: Orice orchestrare de servicii
# ═══════════════════════════════════════════════════════════════════════════════

def opreste_containere(remove_volumes: bool = False) -> bool:
    """
    Oprește containerele folosind docker-compose down.
    
    Args:
        remove_volumes: Dacă True, șterge și volumele
    
    Returns:
        True dacă oprirea a reușit, False altfel
    """
    print("Oprire containere...")
    
    cmd = ["docker", "compose", "-f", str(COMPOSE_FILE), "down"]
    
    if remove_volumes:
        cmd.append("--volumes")
        print("  (inclusiv volumele)")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(BASE_DIR)
        )
        
        if result.returncode != 0:
            print(f"EROARE la oprire containere:")
            print(result.stderr)
            return False
        
        return True
        
    except subprocess.TimeoutExpired:
        print("EROARE: Timeout la oprirea containerelor")
        print("Încercați: docker compose -f docker/docker-compose.yml down")
        return False
    except FileNotFoundError:
        print("EROARE: Docker nu este instalat")
        return False


def verifica_containere_oprite() -> bool:
    """
    Verifică că nu mai rulează containere din acest laborator.
    
    Returns:
        True dacă nu mai sunt containere active, False altfel
    """
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=saptamana4", "-q"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        # Dacă output-ul e gol, nu mai sunt containere
        return len(result.stdout.strip()) == 0
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def afiseaza_containere_ramase():
    """Afișează containerele care încă rulează."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=saptamana4", 
             "--format", "{{.Names}}: {{.Status}}"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.stdout.strip():
            print("Containere încă active:")
            for line in result.stdout.strip().split('\n'):
                print(f"  - {line}")
        
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# CLEANUP_OPERATIONS
# Scop: Curăță resursele rămase
# Transferabil la: Orice script de cleanup
# ═══════════════════════════════════════════════════════════════════════════════

def curata_retele_orfane():
    """Curăță rețelele Docker neutilizate."""
    try:
        subprocess.run(
            ["docker", "network", "prune", "-f"],
            capture_output=True,
            timeout=30
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_ORCHESTRATION
# Scop: Coordonează întregul proces de oprire
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_banner():
    """Afișează banner-ul de oprire."""
    print("=" * 60)
    print("Oprire Mediu Laborator Săptămâna 4")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică")
    print("=" * 60)


def main():
    """Funcția principală de oprire."""
    # Parsare argumente
    parser = argparse.ArgumentParser(
        description="Oprește mediul de laborator pentru Săptămâna 4"
    )
    parser.add_argument(
        "--remove-volumes",
        action="store_true",
        help="Șterge și volumele Docker (date persistente)"
    )
    
    args = parser.parse_args()
    
    # Banner
    afiseaza_banner()
    
    # Verifică dacă fișierul compose există
    if not COMPOSE_FILE.exists():
        print(f"EROARE: Fișierul {COMPOSE_FILE} nu există")
        print("Încercați să opriți manual: docker stop $(docker ps -q --filter name=saptamana4)")
        return 1
    
    # Oprire containere
    if not opreste_containere(remove_volumes=args.remove_volumes):
        return 1
    
    # Verificare
    if verifica_containere_oprite():
        print()
        print("✓ Toate containerele au fost oprite cu succes!")
    else:
        print()
        print("AVERTISMENT: Unele containere încă rulează:")
        afiseaza_containere_ramase()
        print()
        print("Pentru a forța oprirea:")
        print("  docker stop $(docker ps -q --filter name=saptamana4)")
    
    # Curățare rețele
    curata_retele_orfane()
    
    print()
    print("=" * 60)
    print("Mediul de laborator a fost oprit.")
    print()
    print("Notă: Portainer rămâne activ pentru utilizare viitoare.")
    print("Pentru a opri și Portainer: docker stop portainer")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
