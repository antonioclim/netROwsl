#!/usr/bin/env python3
"""
Script de Configurare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Configurează rețeaua Docker și verifică fișierele de configurare
pentru mediul de laborator al săptămânii 7.
"""

from __future__ import annotations

import subprocess
import sys
import json
from pathlib import Path

# Calea către rădăcina proiectului
RADACINA_PROIECT = Path(__file__).parent.parent


def ruleaza_comanda(comanda: list[str], descriere: str) -> tuple[bool, str]:
    """Rulează o comandă și returnează rezultatul."""
    try:
        rezultat = subprocess.run(
            comanda,
            capture_output=True,
            text=True,
            timeout=60
        )
        if rezultat.returncode == 0:
            return True, rezultat.stdout
        else:
            return False, rezultat.stderr
    except subprocess.TimeoutExpired:
        return False, f"Timeout la: {descriere}"
    except Exception as e:
        return False, str(e)


def verifica_retea_docker(nume_retea: str = "week7net") -> bool:
    """Verifică dacă rețeaua Docker există."""
    ok, iesire = ruleaza_comanda(
        ["docker", "network", "ls", "--format", "{{.Name}}"],
        "listare rețele Docker"
    )
    if ok:
        return nume_retea in iesire.split('\n')
    return False


def creeaza_retea_docker(
    nume_retea: str = "week7net",
    subnet: str = "10.0.7.0/24",
    gateway: str = "10.0.7.1"
) -> bool:
    """Creează rețeaua Docker pentru laborator."""
    print(f"  Creare rețea Docker: {nume_retea}")
    print(f"    Subnet: {subnet}")
    print(f"    Gateway: {gateway}")
    
    ok, mesaj = ruleaza_comanda(
        [
            "docker", "network", "create",
            "--driver", "bridge",
            "--subnet", subnet,
            "--gateway", gateway,
            nume_retea
        ],
        f"creare rețea {nume_retea}"
    )
    
    if ok:
        print(f"  [OK] Rețea {nume_retea} creată cu succes")
        return True
    else:
        if "already exists" in mesaj:
            print(f"  [OK] Rețea {nume_retea} există deja")
            return True
        print(f"  [EROARE] Nu s-a putut crea rețeaua: {mesaj}")
        return False


def verifica_imagine_docker(imagine: str) -> bool:
    """Verifică dacă o imagine Docker există local."""
    ok, iesire = ruleaza_comanda(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
        "listare imagini Docker"
    )
    if ok:
        return imagine in iesire
    return False


def descarca_imagine_docker(imagine: str) -> bool:
    """Descarcă o imagine Docker."""
    print(f"  Descărcare imagine: {imagine}")
    
    ok, mesaj = ruleaza_comanda(
        ["docker", "pull", imagine],
        f"descărcare {imagine}"
    )
    
    if ok:
        print(f"  [OK] Imagine {imagine} descărcată")
        return True
    else:
        print(f"  [EROARE] Nu s-a putut descărca: {mesaj}")
        return False


def verifica_fisier_compose() -> bool:
    """Verifică că fișierul docker-compose.yml este valid."""
    cale_compose = RADACINA_PROIECT / "docker" / "docker-compose.yml"
    
    if not cale_compose.exists():
        print("  [EROARE] Fișierul docker-compose.yml nu există")
        return False
    
    # Verificare sintaxă YAML
    try:
        import yaml
        with open(cale_compose, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Verificări de bază
        if 'services' not in config:
            print("  [EROARE] Fișierul compose nu conține secțiunea 'services'")
            return False
        
        servicii = config['services']
        print(f"  [OK] Fișier compose valid cu {len(servicii)} servicii:")
        for nume_serviciu in servicii:
            print(f"       - {nume_serviciu}")
        
        return True
        
    except yaml.YAMLError as e:
        print(f"  [EROARE] Eroare de sintaxă YAML: {e}")
        return False
    except Exception as e:
        print(f"  [EROARE] Nu s-a putut verifica fișierul: {e}")
        return False


def verifica_profile_firewall() -> bool:
    """Verifică fișierul de profile firewall."""
    cale_profile = RADACINA_PROIECT / "docker" / "configs" / "firewall_profiles.json"
    
    if not cale_profile.exists():
        print("  [EROARE] Fișierul firewall_profiles.json nu există")
        return False
    
    try:
        with open(cale_profile, 'r', encoding='utf-8') as f:
            profile = json.load(f)
        
        if 'profiles' not in profile:
            print("  [EROARE] Fișierul nu conține secțiunea 'profiles'")
            return False
        
        lista_profile = profile['profiles']
        print(f"  [OK] Fișier profile valid cu {len(lista_profile)} profile:")
        for profil in lista_profile:
            nume = profil.get('name', 'fără nume')
            nr_reguli = len(profil.get('rules', []))
            print(f"       - {nume} ({nr_reguli} reguli)")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"  [EROARE] Eroare de sintaxă JSON: {e}")
        return False
    except Exception as e:
        print(f"  [EROARE] Nu s-a putut verifica fișierul: {e}")
        return False


def main():
    """Funcția principală de configurare Docker."""
    print("=" * 60)
    print("Configurare Docker pentru Laboratorul Săptămânii 7")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()

    erori = 0

    # Verificare că Docker rulează
    print("[1/5] Verificare daemon Docker...")
    ok, _ = ruleaza_comanda(["docker", "info"], "verificare Docker")
    if ok:
        print("  [OK] Daemon-ul Docker rulează")
    else:
        print("  [EROARE] Docker nu rulează. Porniți Docker Desktop.")
        return 1

    # Verificare/Creare rețea
    print("\n[2/5] Configurare rețea Docker...")
    if verifica_retea_docker("week7net"):
        print("  [OK] Rețea week7net există")
    else:
        if not creeaza_retea_docker():
            erori += 1

    # Verificare imagine de bază
    print("\n[3/5] Verificare imagine Python...")
    imagine_python = "python:3.11-slim"
    if verifica_imagine_docker(imagine_python):
        print(f"  [OK] Imagine {imagine_python} disponibilă local")
    else:
        if not descarca_imagine_docker(imagine_python):
            erori += 1

    # Verificare fișier compose
    print("\n[4/5] Verificare fișier docker-compose.yml...")
    if not verifica_fisier_compose():
        erori += 1

    # Verificare profile firewall
    print("\n[5/5] Verificare profile firewall...")
    if not verifica_profile_firewall():
        erori += 1

    # Sumar
    print()
    print("=" * 60)
    if erori == 0:
        print("Configurare completă! Toate componentele sunt pregătite.")
        print()
        print("Pași următori:")
        print("  1. Porniți laboratorul: python scripts/porneste_lab.py")
        print("  2. Verificați serviciile: python scripts/porneste_lab.py --status")
    else:
        print(f"Configurare incompletă. {erori} eroare(i) detectată(e).")
        print("Verificați mesajele de mai sus și rezolvați problemele.")
    print("=" * 60)

    return 0 if erori == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
