#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 8
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest script elimină toate containerele, rețelele și opțional volumele
pentru a pregăti sistemul pentru următoarea sesiune de laborator.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
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

PREFIX_SAPTAMANA = "week8"



# ═══════════════════════════════════════════════════════════════════════════════
# FUNCTII_AJUTATOARE
# ═══════════════════════════════════════════════════════════════════════════════

def afiseaza_banner():
    """Afișează banner-ul de curățare."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{CYAN}   Curățare Laborator Săptămâna 8{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()


def ruleaza_compose_down(cale_docker: Path, volume: bool = False, simulare: bool = False) -> bool:
    """Oprește și elimină containerele folosind docker compose."""
    print(f"{ALBASTRU}[INFO]{RESETARE} Oprire și eliminare containere...")
    
    if simulare:
        print(f"  {GALBEN}[SIMULARE]{RESETARE} docker compose down" + (" -v" if volume else ""))
        return True
    
    cmd = ["docker", "compose", "down"]
    if volume:
        cmd.append("-v")
    
    try:
        result = subprocess.run(
            cmd,
            cwd=str(cale_docker),
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if result.returncode == 0:
            print(f"{VERDE}[OK]{RESETARE} Containere eliminate")
            return True
        else:
            print(f"{ROSU}[EROARE]{RESETARE} Eliminarea a eșuat")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"{ROSU}[EROARE]{RESETARE} Excepție: {e}")
        return False


def elimina_resurse_cu_prefix(prefix: str, simulare: bool = False):
    """Elimină resursele Docker care au prefixul specificat."""
    
    # Elimină containere
    print(f"{ALBASTRU}[INFO]{RESETARE} Eliminare containere {prefix}_*...")
    result = subprocess.run(
        ["docker", "ps", "-aq", "--filter", f"name={prefix}"],
        capture_output=True,
        text=True
    )
    containere = result.stdout.strip().split('\n')
    containere = [c for c in containere if c]
    
    if containere:
        if simulare:
            print(f"  {GALBEN}[SIMULARE]{RESETARE} Ar elimina {len(containere)} container(e)")
        else:
            subprocess.run(["docker", "rm", "-f"] + containere, capture_output=True)
            print(f"{VERDE}[OK]{RESETARE} {len(containere)} container(e) eliminate")
    else:
        print(f"  Niciun container de eliminat")
    
    # Elimină rețele
    print(f"{ALBASTRU}[INFO]{RESETARE} Eliminare rețele {prefix}-*...")
    result = subprocess.run(
        ["docker", "network", "ls", "-q", "--filter", f"name={prefix}"],
        capture_output=True,
        text=True
    )
    retele = result.stdout.strip().split('\n')
    retele = [r for r in retele if r]
    
    if retele:
        if simulare:
            print(f"  {GALBEN}[SIMULARE]{RESETARE} Ar elimina {len(retele)} rețea(rețele)")
        else:
            for retea in retele:
                subprocess.run(["docker", "network", "rm", retea], capture_output=True)
            print(f"{VERDE}[OK]{RESETARE} {len(retele)} rețea(rețele) eliminate")
    else:
        print(f"  Nicio rețea de eliminat")
    
    # Elimină volume
    print(f"{ALBASTRU}[INFO]{RESETARE} Eliminare volume {prefix}_*...")
    result = subprocess.run(
        ["docker", "volume", "ls", "-q", "--filter", f"name={prefix}"],
        capture_output=True,
        text=True
    )
    volume = result.stdout.strip().split('\n')
    volume = [v for v in volume if v]
    
    if volume:
        if simulare:
            print(f"  {GALBEN}[SIMULARE]{RESETARE} Ar elimina {len(volume)} volum(e)")
        else:
            for vol in volume:
                subprocess.run(["docker", "volume", "rm", vol], capture_output=True)
            print(f"{VERDE}[OK]{RESETARE} {len(volume)} volum(e) eliminate")
    else:
        print(f"  Niciun volum de eliminat")


def curata_directoare(simulare: bool = False):
    """Curăță directoarele de artefacte și capturi."""
    
    # Curăță directorul artifacts
    print(f"{ALBASTRU}[INFO]{RESETARE} Curățare director artifacts/...")
    director_artefacte = RADACINA_PROIECT / "artifacts"
    if director_artefacte.exists():
        count = 0
        for fisier in director_artefacte.glob("*"):
            if fisier.name != ".gitkeep":
                if simulare:
                    print(f"  {GALBEN}[SIMULARE]{RESETARE} Ar șterge {fisier.name}")
                else:
                    fisier.unlink()
                count += 1
        if count > 0:
            print(f"{VERDE}[OK]{RESETARE} {count} fișier(e) eliminate din artifacts/")
        else:
            print(f"  Directorul este deja gol")
    
    # Curăță directorul pcap
    print(f"{ALBASTRU}[INFO]{RESETARE} Curățare director pcap/...")
    director_pcap = RADACINA_PROIECT / "pcap"
    if director_pcap.exists():
        count = 0
        for fisier in director_pcap.glob("*.pcap"):
            if simulare:
                print(f"  {GALBEN}[SIMULARE]{RESETARE} Ar șterge {fisier.name}")
            else:
                fisier.unlink()
            count += 1
        if count > 0:
            print(f"{VERDE}[OK]{RESETARE} {count} fișier(e) .pcap eliminate")
        else:
            print(f"  Niciun fișier .pcap de eliminat")


def curata_sistem(simulare: bool = False):
    """Curăță resursele Docker nefolosite în întregul sistem."""
    print(f"{ALBASTRU}[INFO]{RESETARE} Curățare resurse Docker nefolosite...")
    
    if simulare:
        print(f"  {GALBEN}[SIMULARE]{RESETARE} Ar rula docker system prune -f")
        return
    
    result = subprocess.run(
        ["docker", "system", "prune", "-f"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print(f"{VERDE}[OK]{RESETARE} Resursele nefolosite au fost curățate")
        # Afișează spațiul recuperat
        for linie in result.stdout.split('\n'):
            if 'reclaimed' in linie.lower() or 'recuperat' in linie.lower():
                print(f"  {linie}")
    else:
        print(f"{GALBEN}[ATENȚIE]{RESETARE} Curățarea sistemului a eșuat parțial")



# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python curatare.py              # Oprire containere, păstrare volume
  python curatare.py --complet    # Eliminare totală inclusiv volume
  python curatare.py --simulare   # Afișează ce ar fi eliminat
  python curatare.py --curata-sistem  # Include și curățarea sistemului
        """
    )
    parser.add_argument(
        "--complet", "-c",
        action="store_true",
        help="Elimină volumele și toate datele (folosiți înainte de săptămâna următoare)"
    )
    parser.add_argument(
        "--curata-sistem", "-p",
        action="store_true",
        help="Curăță și resursele Docker nefolosite"
    )
    parser.add_argument(
        "--simulare", "-s",
        action="store_true",
        help="Afișează ce ar fi eliminat fără a elimina efectiv"
    )
    
    args = parser.parse_args()
    
    afiseaza_banner()
    
    if args.simulare:
        print(f"{GALBEN}[SIMULARE] Nicio modificare nu va fi efectuată{RESETARE}")
        print()
    
    cale_docker = RADACINA_PROIECT / "docker"
    
    if not cale_docker.exists():
        print(f"{ROSU}[EROARE]{RESETARE} Directorul docker/ nu a fost găsit!")
        return 1
    
    # Oprește și elimină containerele
    ruleaza_compose_down(cale_docker, volume=args.complet, simulare=args.simulare)
    
    # Elimină resursele cu prefix
    print()
    elimina_resurse_cu_prefix(PREFIX_SAPTAMANA, simulare=args.simulare)
    
    # Curăță directoarele dacă este curățare completă
    if args.complet:
        print()
        curata_directoare(simulare=args.simulare)
    
    # Curăță sistemul dacă este solicitat
    if args.curata_sistem:
        print()
        curata_sistem(simulare=args.simulare)
    
    # Afișează sumarul
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    if args.simulare:
        print(f"{GALBEN}Simulare completă - nicio modificare efectuată{RESETARE}")
    else:
        print(f"{VERDE}Curățare completă!{RESETARE}")
        if args.complet:
            print("Sistemul este pregătit pentru următoarea sesiune de laborator.")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    
    return 0



# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
