#!/usr/bin/env python3
"""
Test Rapid de Funcționalitate
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verificare rapidă că mediul de laborator este funcțional.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    """Rulează un test rapid de funcționalitate."""
    print()
    print("=" * 50)
    print("  TEST RAPID - SĂPTĂMÂNA 1")
    print("=" * 50)
    print()

    erori = 0

    # Test 1: Docker disponibil
    print("1. Verificare Docker...", end=" ")
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        if rezultat.returncode == 0:
            print("\033[92m✓\033[0m")
        else:
            print("\033[91m✗ Docker nu răspunde\033[0m")
            erori += 1
    except Exception as e:
        print(f"\033[91m✗ {e}\033[0m")
        erori += 1

    # Test 2: Container activ
    print("2. Verificare container week1_lab...", end=" ")
    try:
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week1_lab"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "true" in rezultat.stdout.lower():
            print("\033[92m✓\033[0m")
        else:
            print("\033[93m⚠ Nu rulează (porniți cu porneste_lab.py)\033[0m")
    except Exception:
        print("\033[93m⚠ Container inexistent\033[0m")

    # Test 3: Structură fișiere
    print("3. Verificare structură proiect...", end=" ")
    radacina = Path(__file__).parent.parent
    fisiere_critice = [
        "docker/docker-compose.yml",
        "scripts/porneste_lab.py",
        "README.md",
    ]
    lipsa = [f for f in fisiere_critice if not (radacina / f).exists()]
    if not lipsa:
        print("\033[92m✓\033[0m")
    else:
        print(f"\033[91m✗ Lipsă: {', '.join(lipsa)}\033[0m")
        erori += 1

    # Sumar
    print()
    print("=" * 50)
    if erori == 0:
        print("\033[92m✓ Mediul este pregătit!\033[0m")
        return 0
    else:
        print(f"\033[91m✗ {erori} probleme detectate\033[0m")
        return 1


if __name__ == "__main__":
    sys.exit(main())
