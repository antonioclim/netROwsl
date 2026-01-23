#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script oprește grațios toate containerele laboratorului.

IMPORTANT: Portainer NU este oprit - rulează global pe portul 9000!
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import time
import argparse
import socket
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
PREFIX_SAPTAMANA = "week14"

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_info(mesaj: str) -> None:
    print(f"{Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")

def afiseaza_succes(mesaj: str) -> None:
    print(f"{Culori.VERDE}[OK]{Culori.FINAL} {mesaj}")

def afiseaza_eroare(mesaj: str) -> None:
    print(f"{Culori.ROSU}[EROARE]{Culori.FINAL} {mesaj}")

def afiseaza_avertisment(mesaj: str) -> None:
    print(f"{Culori.GALBEN}[ATENȚIE]{Culori.FINAL} {mesaj}")


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


def opreste_cu_compose(timeout: int = 30) -> bool:
    """Oprește containerele folosind docker compose."""
    afiseaza_info(f"Se opresc containerele de laborator (timeout: {timeout}s)...")
    
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
    """Verifică dacă toate containerele week14 s-au oprit."""
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



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

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
    print(f"{Culori.CYAN}(Portainer rămâne activ pe portul 9000){Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    cale_compose = RADACINA_PROIECT / "docker" / "docker-compose.yml"
    if cale_compose.exists():
        succes = opreste_cu_compose(args.timeout)
    else:
        afiseaza_info("Fișierul compose nu a fost găsit, se opresc după etichetă...")
        succes = opreste_dupa_eticheta()
    
    time.sleep(2)
    
    # Verifică containerele week14 rămase
    result = subprocess.run(
        ["docker", "ps", "-a", "--filter", "name=week14_", "--format", "{{.Names}}"],
        capture_output=True,
        text=True,
        timeout=10
    )
    containere_ramase = [c for c in result.stdout.strip().split('\n') if c and "week14_" in c]
    
    if verifica_containere_oprite():
        afiseaza_succes("Toate containerele de laborator au fost oprite")
    else:
        afiseaza_avertisment(f"Containere week14 încă prezente: {containere_ramase}")
        afiseaza_stare_containere()
    
    # Verifică și afișează status Portainer
    print()
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.VERDE}Laboratorul a fost oprit cu succes!{Culori.FINAL}")
    
    if verifica_portainer_status():
        afiseaza_succes(f"Portainer continuă să ruleze pe {PORTAINER_URL}")
    else:
        afiseaza_avertisment(f"Portainer nu rulează pe {PORTAINER_URL}")
    
    print(f"\n{Culori.CYAN}Pentru curățare completă: python3 scripts/curata.py --complet{Culori.FINAL}")
    print(f"{Culori.CYAN}Pentru a reporni: python3 scripts/porneste_lab.py{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    return 0 if verifica_containere_oprite() else 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
