#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script oprește grațios toate containerele laboratorului.
"""

import subprocess
import sys
import time
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
PREFIX_SAPTAMANA = "week14"

class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

def afiseaza_info(mesaj: str) -> None:
    print(f"{Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")

def afiseaza_succes(mesaj: str) -> None:
    print(f"{Culori.VERDE}[OK]{Culori.FINAL} {mesaj}")

def afiseaza_eroare(mesaj: str) -> None:
    print(f"{Culori.ROSU}[EROARE]{Culori.FINAL} {mesaj}")

def opreste_cu_compose(timeout: int = 30) -> bool:
    """Oprește containerele folosind docker compose."""
    afiseaza_info(f"Se opresc containerele (timeout: {timeout}s)...")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "-f", "docker/docker-compose.yml", "stop", "-t", str(timeout)],
            cwd=str(RADACINA_PROIECT),
            timeout=timeout + 30
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        afiseaza_eroare("Oprirea a expirat")
        return False
    except Exception as e:
        afiseaza_eroare(f"Eroare la oprire: {e}")
        return False

def opreste_dupa_eticheta() -> bool:
    """Oprește containerele după eticheta week=14."""
    afiseaza_info("Se opresc containerele după etichetă...")
    
    try:
        result = subprocess.run(
            ["docker", "ps", "-q", "--filter", "label=week=14"],
            capture_output=True, text=True, timeout=10
        )
        
        if not result.stdout.strip():
            afiseaza_info("Nu s-au găsit containere cu eticheta week=14")
            return True
        
        containere = result.stdout.strip().split('\n')
        for container_id in containere:
            if container_id:
                subprocess.run(["docker", "stop", container_id], timeout=30)
        return True
    except Exception as e:
        afiseaza_eroare(f"Eroare: {e}")
        return False

def verifica_containere_oprite() -> bool:
    """Verifică dacă toate containerele s-au oprit."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-q", "--filter", f"name={PREFIX_SAPTAMANA}"],
            capture_output=True, text=True, timeout=10
        )
        return not result.stdout.strip()
    except Exception:
        return False

def afiseaza_stare_containere() -> None:
    """Afișează starea curentă a containerelor."""
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={PREFIX_SAPTAMANA}",
             "--format", "table {{.Names}}\t{{.Status}}"],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            print(f"\n{Culori.BOLD}Starea Containerelor:{Culori.FINAL}")
            print(result.stdout)
    except Exception:
        pass

def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 14",
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Timeout oprire (implicit: 30s)")
    parser.add_argument("--force", "-f", action="store_true", help="Forțează oprirea")
    
    args = parser.parse_args()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Oprire Mediu Laborator Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE, Informatică Economică{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    cale_compose = RADACINA_PROIECT / "docker" / "docker-compose.yml"
    if cale_compose.exists():
        succes = opreste_cu_compose(args.timeout)
    else:
        afiseaza_info("Fișierul compose nu a fost găsit, se opresc după etichetă...")
        succes = opreste_dupa_eticheta()
    
    time.sleep(2)
    
    if verifica_containere_oprite():
        afiseaza_succes("Toate containerele au fost oprite")
        print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
        print(f"{Culori.VERDE}Laboratorul a fost oprit cu succes!{Culori.FINAL}")
        print(f"{Culori.CYAN}Pentru curățare completă: python scripts/curata.py --complet{Culori.FINAL}")
        print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
        return 0
    else:
        afiseaza_eroare("Unele containere nu s-au oprit")
        afiseaza_stare_containere()
        return 1

if __name__ == "__main__":
    sys.exit(main())
