#!/usr/bin/env python3
"""
Asistent de Configurare Docker Desktop
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică și ajută la configurarea Docker Desktop pentru mediul de laborator.
"""

import subprocess
import sys
import json
from pathlib import Path


def afiseaza_sectiune(titlu: str):
    """Afișează un titlu de secțiune."""
    print(f"\n{'─' * 60}")
    print(f"  {titlu}")
    print('─' * 60)


def verifica_backend_wsl2() -> bool:
    """Verifică dacă Docker folosește backend-ul WSL2."""
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{.OSType}}"],
            capture_output=True,
            text=True
        )
        return "linux" in rezultat.stdout.lower()
    except Exception:
        return False


def verifica_resurse_docker() -> dict:
    """Verifică resursele alocate Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True
        )
        info = json.loads(rezultat.stdout)
        return {
            "cpus": info.get("NCPU", "necunoscut"),
            "memorie_gb": round(info.get("MemTotal", 0) / (1024**3), 1),
            "driver_stocare": info.get("Driver", "necunoscut"),
            "versiune": info.get("ServerVersion", "necunoscută")
        }
    except Exception:
        return {}


def verifica_retele_docker() -> list:
    """Listează rețelele Docker existente."""
    try:
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        return rezultat.stdout.strip().split('\n')
    except Exception:
        return []


def verifica_containere_active() -> list:
    """Listează containerele active."""
    try:
        rezultat = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}: {{.Status}}"],
            capture_output=True,
            text=True
        )
        if rezultat.stdout.strip():
            return rezultat.stdout.strip().split('\n')
        return []
    except Exception:
        return []


def verifica_spatiu_disc() -> dict:
    """Verifică utilizarea discului de către Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "system", "df", "--format", "{{json .}}"],
            capture_output=True,
            text=True
        )
        linii = rezultat.stdout.strip().split('\n')
        utilizare = {}
        for linie in linii:
            try:
                data = json.loads(linie)
                tip = data.get("Type", "")
                utilizare[tip] = {
                    "dimensiune": data.get("Size", "0B"),
                    "recuperabil": data.get("Reclaimable", "0B")
                }
            except json.JSONDecodeError:
                continue
        return utilizare
    except Exception:
        return {}


def main():
    print("=" * 60)
    print("  Verificare Configurare Docker Desktop")
    print("  Rețele de Calculatoare – ASE, Informatică Economică")
    print("=" * 60)

    # Verifică dacă Docker rulează
    try:
        subprocess.run(
            ["docker", "info"],
            capture_output=True,
            check=True
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n✗ Docker Desktop nu rulează sau nu este instalat.")
        print("  Vă rugăm să porniți Docker Desktop și să rulați din nou acest script.")
        return 1

    # Backend WSL2
    afiseaza_sectiune("Backend Docker")
    if verifica_backend_wsl2():
        print("✓ Docker folosește backend-ul WSL2 (recomandat)")
    else:
        print("⚠ Docker nu pare să folosească WSL2")
        print("  Recomandare: Activați 'Use the WSL 2 based engine' în setările Docker Desktop")

    # Resurse
    afiseaza_sectiune("Resurse Alocate")
    resurse = verifica_resurse_docker()
    if resurse:
        print(f"  Versiune Docker: {resurse.get('versiune', 'necunoscută')}")
        print(f"  CPU-uri disponibile: {resurse.get('cpus', 'necunoscut')}")
        print(f"  Memorie totală: {resurse.get('memorie_gb', 'necunoscută')} GB")
        print(f"  Driver stocare: {resurse.get('driver_stocare', 'necunoscut')}")
        
        memorie = resurse.get('memorie_gb', 0)
        if memorie < 4:
            print("\n⚠ Memorie insuficientă pentru laboratorul de rețele")
            print("  Recomandare: Alocați cel puțin 4GB în Docker Desktop > Settings > Resources")
        elif memorie < 8:
            print("\nℹ Memorie adecvată, dar 8GB+ este recomandat pentru performanță optimă")
        else:
            print("\n✓ Resurse adecvate pentru laborator")

    # Rețele existente
    afiseaza_sectiune("Rețele Docker")
    retele = verifica_retele_docker()
    retele_week5 = [r for r in retele if 'week5' in r.lower()]
    
    print(f"  Rețele totale: {len(retele)}")
    if retele_week5:
        print(f"  Rețele week5_*: {', '.join(retele_week5)}")
    else:
        print("  Rețele week5_*: niciuna (se vor crea la pornirea laboratorului)")

    # Containere active
    afiseaza_sectiune("Containere Active")
    containere = verifica_containere_active()
    containere_week5 = [c for c in containere if 'week5' in c.lower()]
    
    if containere:
        print(f"  Containere totale active: {len(containere)}")
        if containere_week5:
            print("  Containere week5_*:")
            for c in containere_week5:
                print(f"    • {c}")
        else:
            print("  Containere week5_*: niciuna")
    else:
        print("  Nu există containere active")

    # Utilizare disc
    afiseaza_sectiune("Utilizare Disc Docker")
    spatiu = verifica_spatiu_disc()
    if spatiu:
        for tip, info in spatiu.items():
            print(f"  {tip}: {info['dimensiune']} (recuperabil: {info['recuperabil']})")
    else:
        print("  Nu s-a putut determina utilizarea discului")

    # Recomandări finale
    afiseaza_sectiune("Configurare Recomandată pentru Laborator")
    print("""
  Pentru performanță optimă în laboratorul de rețele:
  
  Docker Desktop > Settings > Resources:
    • Memory: minim 4GB, recomandat 8GB
    • CPUs: minim 2, recomandat 4
    • Swap: 1GB
    
  Docker Desktop > Settings > General:
    ✓ Use the WSL 2 based engine
    ✓ Start Docker Desktop when you log in (opțional)
    
  Docker Desktop > Settings > Resources > WSL Integration:
    ✓ Enable integration with your default WSL distro
    """)

    print("=" * 60)
    print("  Verificarea configurării este completă")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
