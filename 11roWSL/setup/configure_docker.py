#!/usr/bin/env python3
"""
Script de Configurare Docker
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Ajută la configurarea Docker Desktop pentru laboratorul săptămânii 11.
"""

import subprocess
import sys
import json
import platform
from pathlib import Path


def afiseaza_banner():
    """Afișează bannerul de configurare."""
    print("=" * 60)
    print("Configurare Docker - Săptămâna 11")
    print("Laborator Rețele de Calculatoare — ASE")
    print("=" * 60)
    print()


def verifica_docker_instalat() -> bool:
    """Verifică dacă Docker este instalat."""
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def verifica_docker_ruleaza() -> bool:
    """Verifică dacă daemon-ul Docker rulează."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return result.returncode == 0
    except Exception:
        return False


def obtine_informatii_docker() -> dict:
    """Obține informații despre configurația Docker."""
    try:
        result = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            return json.loads(result.stdout.decode())
    except Exception:
        pass
    return {}


def afiseaza_configuratie_curenta():
    """Afișează configurația Docker curentă."""
    print("Configurație Docker curentă:")
    print("-" * 40)
    
    info = obtine_informatii_docker()
    
    if not info:
        print("  Nu se pot obține informații Docker")
        return
    
    # Afișează informații relevante
    print(f"  Versiune Server: {info.get('ServerVersion', 'N/A')}")
    print(f"  Sistem de Operare: {info.get('OperatingSystem', 'N/A')}")
    print(f"  Arhitectură: {info.get('Architecture', 'N/A')}")
    print(f"  CPU-uri: {info.get('NCPU', 'N/A')}")
    print(f"  Memorie Totală: {info.get('MemTotal', 0) // (1024**3)} GB")
    print(f"  Driver Stocare: {info.get('Driver', 'N/A')}")
    print(f"  Containere: {info.get('Containers', 0)} (Rulează: {info.get('ContainersRunning', 0)})")
    print(f"  Imagini: {info.get('Images', 0)}")


def verifica_retele_docker():
    """Verifică rețelele Docker existente."""
    print("\nRețele Docker:")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}\t{{.Driver}}"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            retele = result.stdout.decode().strip().split('\n')
            for retea in retele:
                if retea:
                    print(f"  {retea}")
    except Exception as e:
        print(f"  Eroare: {e}")


def verifica_containere_sapt11():
    """Verifică containerele din săptămâna 11."""
    print("\nContainere Săptămâna 11:")
    print("-" * 40)
    
    try:
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", "name=s11_", "--format", 
             "{{.Names}}\t{{.Status}}\t{{.Ports}}"],
            capture_output=True,
            timeout=10
        )
        if result.returncode == 0:
            containere = result.stdout.decode().strip()
            if containere:
                for container in containere.split('\n'):
                    print(f"  {container}")
            else:
                print("  Nu există containere pentru Săptămâna 11")
    except Exception as e:
        print(f"  Eroare: {e}")


def verifica_imagini_necesare():
    """Verifică dacă imaginile Docker necesare sunt disponibile."""
    print("\nImagini Docker necesare:")
    print("-" * 40)
    
    imagini = [
        "nginx:alpine",
        "python:3.11-slim",
    ]
    
    for imagine in imagini:
        try:
            result = subprocess.run(
                ["docker", "image", "inspect", imagine],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"  ✓ {imagine} - disponibilă local")
            else:
                print(f"  ○ {imagine} - va fi descărcată la prima utilizare")
        except Exception:
            print(f"  ? {imagine} - nu se poate verifica")


def descarca_imagini():
    """Descarcă imaginile Docker necesare."""
    print("\nDescărcare imagini Docker...")
    
    imagini = [
        "nginx:alpine",
        "python:3.11-slim",
    ]
    
    for imagine in imagini:
        print(f"  Descărcare {imagine}...")
        try:
            result = subprocess.run(
                ["docker", "pull", imagine],
                timeout=300
            )
            if result.returncode == 0:
                print(f"  ✓ {imagine} descărcată cu succes")
            else:
                print(f"  ✗ Eroare la descărcarea {imagine}")
        except subprocess.TimeoutExpired:
            print(f"  ✗ Timeout la descărcarea {imagine}")
        except Exception as e:
            print(f"  ✗ Eroare: {e}")


def afiseaza_recomandari():
    """Afișează recomandări pentru configurarea Docker Desktop."""
    print("\nRecomandări pentru Docker Desktop:")
    print("-" * 40)
    print("""
  1. Resurse alocate (Settings → Resources):
     - CPU-uri: minim 2 (recomandat 4)
     - Memorie: minim 4GB (recomandat 8GB)
     - Swap: 1GB
     - Spațiu disc: minim 20GB

  2. Configurare rețea (Settings → Resources → Network):
     - Activați 'Enable host networking' (opțional)

  3. Integrare WSL (Settings → Resources → WSL Integration):
     - Activați integrarea cu distribuția Ubuntu

  4. General (Settings → General):
     - Activați 'Start Docker Desktop when you log in'
     - Activați 'Use the WSL 2 based engine'
""")


def main():
    """Funcția principală de configurare."""
    afiseaza_banner()
    
    # Verifică dacă Docker este instalat
    if not verifica_docker_instalat():
        print("✗ Docker nu este instalat!")
        print("  Rulați mai întâi: python setup/install_prerequisites.py")
        return 1
    
    # Verifică dacă Docker rulează
    if not verifica_docker_ruleaza():
        print("✗ Docker nu rulează!")
        print("  Porniți Docker Desktop și așteptați inițializarea.")
        return 1
    
    print("✓ Docker este instalat și rulează\n")
    
    # Afișează informații
    afiseaza_configuratie_curenta()
    verifica_retele_docker()
    verifica_containere_sapt11()
    verifica_imagini_necesare()
    
    # Întreabă dacă să descarce imaginile
    print()
    raspuns = input("Doriți să descărcați imaginile Docker acum? (d/n): ").strip().lower()
    if raspuns in ['d', 'da', 'y', 'yes']:
        descarca_imagini()
    
    # Afișează recomandări
    afiseaza_recomandari()
    
    print("\n" + "=" * 60)
    print("Configurare finalizată!")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
