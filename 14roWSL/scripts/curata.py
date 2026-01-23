#!/usr/bin/env python3
"""
Curățare Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Elimină containerele, rețelele și volumele pentru o curățare completă.
"""


# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import sys
import argparse
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE_CONFIGURARE
# ═══════════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent
PREFIX_SAPTAMANA = "week14"

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

def afiseaza_info(mesaj): print(f"{Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")
def afiseaza_succes(mesaj): print(f"{Culori.VERDE}[OK]{Culori.FINAL} {mesaj}")
def afiseaza_eroare(mesaj): print(f"{Culori.ROSU}[EROARE]{Culori.FINAL} {mesaj}")

def opreste_containere_compose(simulare=False):
    cale_compose = RADACINA_PROIECT / "docker" / "docker-compose.yml"
    if not cale_compose.exists():
        return False
    
    cmd = ["docker", "compose", "-f", str(cale_compose), "down"]
    if simulare:
        afiseaza_info(f"[SIMULARE] {' '.join(cmd)}")
        return True
    
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        return result.returncode == 0
    except:
        return False

def elimina_containere_dupa_eticheta(simulare=False):
    try:
        result = subprocess.run(
            ["docker", "ps", "-aq", "--filter", "label=week=14"],
            capture_output=True, text=True, timeout=10
        )
        containere = [c for c in result.stdout.strip().split('\n') if c]
        
        if not containere:
            return 0
        
        if simulare:
            afiseaza_info(f"[SIMULARE] S-ar elimina {len(containere)} containere")
            return len(containere)
        
        for container_id in containere:
            subprocess.run(["docker", "rm", "-f", container_id], capture_output=True)
        return len(containere)
    except:
        return 0

def elimina_retele_dupa_prefix(simulare=False):
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=10
        )
        retele = [r for r in result.stdout.strip().split('\n') 
                  if r.startswith(PREFIX_SAPTAMANA) or f"_{PREFIX_SAPTAMANA}" in r]
        
        if not retele:
            return 0
        
        if simulare:
            afiseaza_info(f"[SIMULARE] S-ar elimina {len(retele)} rețele")
            return len(retele)
        
        for retea in retele:
            subprocess.run(["docker", "network", "rm", retea], capture_output=True)
        return len(retele)
    except:
        return 0

def elimina_volume_dupa_prefix(simulare=False):
    try:
        result = subprocess.run(
            ["docker", "volume", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=10
        )
        volume = [v for v in result.stdout.strip().split('\n') 
                  if v.startswith(PREFIX_SAPTAMANA) or f"_{PREFIX_SAPTAMANA}" in v]
        
        if not volume:
            return 0
        
        if simulare:
            afiseaza_info(f"[SIMULARE] S-ar elimina {len(volume)} volume")
            return len(volume)
        
        for volum in volume:
            subprocess.run(["docker", "volume", "rm", volum], capture_output=True)
        return len(volume)
    except:
        return 0

def curata_directoare(simulare=False):
    directoare = [RADACINA_PROIECT / "artifacts", RADACINA_PROIECT / "pcap"]
    
    for director in directoare:
        if not director.exists():
            continue
        
        for fisier in director.iterdir():
            if fisier.name in ['.gitkeep', 'README.md']:
                continue
            
            if simulare:
                afiseaza_info(f"[SIMULARE] S-ar șterge: {fisier}")
            else:
                try:
                    fisier.unlink()
                    afiseaza_info(f"Șters: {fisier.name}")
                except Exception as e:
                    afiseaza_eroare(f"Nu s-a putut șterge {fisier.name}: {e}")

def afiseaza_utilizare_disc():
    try:
        result = subprocess.run(["docker", "system", "df"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"\n{Culori.BOLD}Utilizare Disc Docker:{Culori.FINAL}")
            print(result.stdout)
    except:
        pass


# ═══════════════════════════════════════════════════════════════════════════════
# LOGICA_PRINCIPALA
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Curățare Laborator Săptămâna 14",
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    parser.add_argument("--complet", "-c", action="store_true", help="Curățare completă (include volume)")
    parser.add_argument("--prune", "-p", action="store_true", help="Curăță resursele Docker neutilizate")
    parser.add_argument("--simulare", "-s", action="store_true", help="Mod simulare (fără modificări)")
    args = parser.parse_args()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Curățare Mediu Laborator Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    if args.simulare:
        print(f"{Culori.GALBEN}[MOD SIMULARE]{Culori.FINAL}\n")
    
    afiseaza_info("Se opresc containerele...")
    if opreste_containere_compose(args.simulare):
        afiseaza_succes("Containere oprite cu docker compose")
    
    afiseaza_info("Se elimină containerele după etichetă...")
    numar = elimina_containere_dupa_eticheta(args.simulare)
    if numar > 0:
        afiseaza_succes(f"Eliminate {numar} containere")
    
    afiseaza_info("Se elimină rețelele...")
    numar = elimina_retele_dupa_prefix(args.simulare)
    if numar > 0:
        afiseaza_succes(f"Eliminate {numar} rețele")
    
    if args.complet:
        afiseaza_info("Se elimină volumele...")
        numar = elimina_volume_dupa_prefix(args.simulare)
        if numar > 0:
            afiseaza_succes(f"Eliminate {numar} volume")
        
        afiseaza_info("Se curăță directoarele...")
        curata_directoare(args.simulare)
    
    if args.prune and not args.simulare:
        afiseaza_info("Se curăță resursele neutilizate...")
        subprocess.run(["docker", "system", "prune", "-f"], capture_output=True)
    
    if not args.simulare:
        afiseaza_utilizare_disc()
    
    print(f"\n{Culori.VERDE}Curățare completă!{Culori.FINAL}")
    return 0


# ═══════════════════════════════════════════════════════════════════════════════
# PUNCT_INTRARE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    sys.exit(main())
