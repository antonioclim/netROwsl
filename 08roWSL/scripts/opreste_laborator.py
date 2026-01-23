#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 8
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script oprește toate containerele Docker fără a șterge datele.

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

# Adaugă rădăcina proiectului la calea Python

# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Coduri ANSI pentru culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
CYAN = "\033[96m"
RESETARE = "\033[0m"
BOLD = "\033[1m"

# Credențiale standard
PORTAINER_PORT = 9000
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_banner():
    """Afișează banner-ul de oprire."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{CYAN}   Oprire Laborator Săptămâna 8{RESETARE}")
    print(f"{CYAN}   (Portainer rămâne activ pe portul 9000){RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()


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


def opreste_containere(cale_docker: Path) -> bool:
    """Oprește toate containerele folosind docker compose."""
    print(f"{ALBASTRU}[INFO]{RESETARE} Oprire containere de laborator...")
    print(f"{ALBASTRU}[INFO]{RESETARE} (Portainer va rămâne activ)")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "stop"],
            cwd=str(cale_docker),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"{VERDE}[OK]{RESETARE} Toate containerele de laborator au fost oprite")
            return True
        else:
            print(f"{ROSU}[EROARE]{RESETARE} Oprirea a eșuat")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"{ROSU}[EROARE]{RESETARE} Timeout la oprirea containerelor")
        return False
    except Exception as e:
        print(f"{ROSU}[EROARE]{RESETARE} Excepție: {e}")
        return False


def afiseaza_containere_active():
    """Afișează containerele Docker active."""
    print(f"\n{ALBASTRU}[INFO]{RESETARE} Containere Docker active:")
    print("-" * 50)
    
    result = subprocess.run(
        ["docker", "ps", "--format", "table {{.Names}}\t{{.Status}}\t{{.Ports}}"],
        capture_output=True,
        text=True
    )
    
    if result.stdout.strip():
        print(result.stdout)
    else:
        print("  Niciun container activ")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Note:
  Această comandă oprește containerele de laborator dar păstrează datele.
  Portainer NU va fi oprit - continuă să ruleze pe portul 9000.
  Pentru curățare completă: python3 scripts/curatare.py --complet
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Afișează doar starea containerelor"
    )
    parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="Oprire forțată fără confirmare"
    )
    
    args = parser.parse_args()
    
    afiseaza_banner()
    
    if args.status:
        afiseaza_containere_active()
        return 0
    
    cale_docker = RADACINA_PROIECT / "docker"
    
    if not cale_docker.exists():
        print(f"{ROSU}[EROARE]{RESETARE} Directorul docker/ nu a fost găsit!")
        return 1
    
    # Confirmare dacă nu e forțată
    if not args.force:
        raspuns = input("Doriți să opriți containerele de laborator? (da/nu): ").strip().lower()
        if raspuns not in ("da", "d", "yes", "y"):
            print(f"{ALBASTRU}[INFO]{RESETARE} Operațiune anulată de utilizator")
            return 0
    
    succes = opreste_containere(cale_docker)
    
    if succes:
        print()
        print(f"{CYAN}{'=' * 60}{RESETARE}")
        print(f"{VERDE}✓ Laboratorul a fost oprit cu succes!{RESETARE}")
        
        # Verifică și afișează status Portainer
        if verifica_portainer_status():
            print(f"{VERDE}✓ Portainer continuă să ruleze pe {PORTAINER_URL}{RESETARE}")
        else:
            print(f"{GALBEN}⚠ Portainer nu rulează pe {PORTAINER_URL}{RESETARE}")
        
        print()
        print("Datele au fost păstrate. Pentru a reporni:")
        print(f"  python3 scripts/porneste_laborator.py")
        print()
        print("Pentru curățare completă:")
        print(f"  python3 scripts/curatare.py --complet")
        print(f"{CYAN}{'=' * 60}{RESETARE}")
    
    return 0 if succes else 1



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
