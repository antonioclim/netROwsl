#!/usr/bin/env python3
"""
Asistent de Configurare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică și ajută la configurarea optimă a Docker Desktop pentru laborator.
"""

from __future__ import annotations

import subprocess
import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional


def afiseaza_sectiune(titlu: str) -> None:
    """Afișează un titlu de secțiune formatat."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60 + "\n")


def obtine_info_docker() -> Optional[Dict[str, Any]]:
    """Obține informații despre configurația Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "info", "--format", "{{json .}}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            return json.loads(rezultat.stdout)
    except Exception:
        pass
    return None


def verifica_resurse(info: Dict[str, Any]) -> None:
    """Verifică resursele alocate Docker."""
    afiseaza_sectiune("Resurse Alocate")
    
    # Memorie
    memorie_totala = info.get("MemTotal", 0)
    memorie_gb = memorie_totala / (1024 ** 3)
    
    print(f"Memorie RAM: {memorie_gb:.1f} GB")
    if memorie_gb < 4:
        print("  ⚠ AVERTISMENT: Memorie insuficientă!")
        print("  → Recomandare: Minim 4 GB, optim 8 GB")
    elif memorie_gb < 8:
        print("  ⚠ Memorie acceptabilă, dar 8 GB ar fi mai bine")
    else:
        print("  ✓ Memorie suficientă")
    
    # CPU-uri
    cpus = info.get("NCPU", 0)
    print(f"\nProcesoare (CPU-uri): {cpus}")
    if cpus < 2:
        print("  ⚠ AVERTISMENT: Procesoare insuficiente!")
        print("  → Recomandare: Minim 2 CPU-uri")
    elif cpus < 4:
        print("  ✓ Acceptabil pentru laborator")
    else:
        print("  ✓ Resurse excelente")


def verifica_backend(info: Dict[str, Any]) -> None:
    """Verifică backend-ul Docker (WSL2 vs Hyper-V)."""
    afiseaza_sectiune("Backend Docker")
    
    # Verifică dacă rulează pe WSL2
    isolation = info.get("Isolation", "")
    os_type = info.get("OSType", "")
    kernel = info.get("KernelVersion", "")
    
    print(f"Sistem de operare: {os_type}")
    print(f"Kernel: {kernel}")
    print(f"Izolare: {isolation}")
    
    if "microsoft" in kernel.lower() or "wsl" in kernel.lower():
        print("\n✓ Docker rulează cu backend WSL2 (recomandat)")
    elif "hyperv" in isolation.lower():
        print("\n⚠ Docker rulează cu Hyper-V")
        print("  → Recomandare: Comutați la backend WSL2 pentru performanță mai bună")
    else:
        print("\n? Backend necunoscut - verificați setările Docker Desktop")


def verifica_retele() -> None:
    """Verifică rețelele Docker existente."""
    afiseaza_sectiune("Rețele Docker")
    
    try:
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}\t{{.Driver}}"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            print("Rețele disponibile:")
            for linie in rezultat.stdout.strip().split("\n"):
                if linie:
                    print(f"  • {linie}")
            
            # Verifică dacă există rețeaua de laborator
            if "week1_network" in rezultat.stdout:
                print("\n✓ Rețeaua de laborator (week1_network) există deja")
            else:
                print("\n→ Rețeaua de laborator va fi creată la pornirea laboratorului")
    except Exception as e:
        print(f"Eroare la verificarea rețelelor: {e}")


def verifica_spatiu_disc() -> None:
    """Verifică spațiul pe disc pentru Docker."""
    afiseaza_sectiune("Spațiu pe Disc")
    
    try:
        rezultat = subprocess.run(
            ["docker", "system", "df"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if rezultat.returncode == 0:
            print("Utilizare spațiu Docker:")
            print(rezultat.stdout)
    except Exception as e:
        print(f"Eroare la verificarea spațiului: {e}")


def afiseaza_recomandari() -> None:
    """Afișează recomandările de configurare."""
    afiseaza_sectiune("Recomandări de Configurare")
    
    print("""
Pentru o experiență optimă în laborator, configurați Docker Desktop astfel:

SETĂRI GENERALE (Settings > General):
  ☑ Start Docker Desktop when you sign in to Windows
  ☑ Use WSL 2 based engine

RESURSE (Settings > Resources > Advanced):
  • CPU-uri: minim 2, recomandat 4
  • Memorie: minim 4 GB, recomandat 8 GB
  • Spațiu disc: minim 20 GB pentru imaginile Docker

INTEGRARE WSL (Settings > Resources > WSL Integration):
  ☑ Enable integration with my default WSL distro
  ☑ Selectați distribuția WSL pe care o folosiți

REȚEA (Settings > Resources > Network):
  • Lăsați setările implicite în majoritatea cazurilor
  • Pentru probleme cu proxy, configurați în această secțiune

NOTĂ: Modificările necesită repornirea Docker Desktop.
""")


def main() -> int:
    """Funcția principală."""
    print("=" * 60)
    print("  Asistent de Configurare Docker")
    print("  Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    
    info = obtine_info_docker()
    
    if info is None:
        print("\n✗ Nu s-a putut conecta la Docker!")
        print("\nVerificați că:")
        print("  1. Docker Desktop este instalat")
        print("  2. Docker Desktop rulează (pictograma verde în system tray)")
        print("  3. Așteptați câteva secunde dacă tocmai a pornit")
        return 1
    
    print("\n✓ Conectat la Docker cu succes!")
    
    verifica_resurse(info)
    verifica_backend(info)
    verifica_retele()
    verifica_spatiu_disc()
    afiseaza_recomandari()
    
    print("\n" + "=" * 60)
    print("  Verificare completă!")
    print("=" * 60 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
