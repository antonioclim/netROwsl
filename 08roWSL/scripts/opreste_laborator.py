#!/usr/bin/env python3
"""
Oprire Laborator Săptămâna 8
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script oprește toate containerele Docker fără a șterge datele.
"""

import subprocess
import sys
import argparse
from pathlib import Path

# Adaugă rădăcina proiectului la calea Python
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


def afiseaza_banner():
    """Afișează banner-ul de oprire."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{CYAN}   Oprire Laborator Săptămâna 8{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()


def opreste_containere(cale_docker: Path) -> bool:
    """Oprește toate containerele folosind docker compose."""
    print(f"{ALBASTRU}[INFO]{RESETARE} Oprire containere...")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "stop"],
            cwd=str(cale_docker),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"{VERDE}[OK]{RESETARE} Toate containerele au fost oprite")
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


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Oprire Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Note:
  Această comandă oprește containerele dar păstrează datele.
  Pentru curățare completă, folosiți: python curatare.py --complet
        """
    )
    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Afișează doar starea containerelor"
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
    
    succes = opreste_containere(cale_docker)
    
    if succes:
        print()
        print(f"{CYAN}{'=' * 60}{RESETARE}")
        print(f"{VERDE}Laboratorul a fost oprit cu succes!{RESETARE}")
        print()
        print("Datele au fost păstrate. Pentru a reporni:")
        print(f"  python scripts/porneste_laborator.py")
        print()
        print("Pentru curățare completă:")
        print(f"  python scripts/curatare.py --complet")
        print(f"{CYAN}{'=' * 60}{RESETARE}")
    
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
