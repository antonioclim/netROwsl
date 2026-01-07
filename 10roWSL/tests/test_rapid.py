#!/usr/bin/env python3
"""
Test Rapid de Verificare (Smoke Test)
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verificare rapidă (60 secunde) a mediului de laborator.
"""

import subprocess
import sys
import socket
import time


def verifica_docker() -> bool:
    """Verifică dacă Docker rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=5
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def verifica_port(port: int, gazda: str = "localhost") -> bool:
    """Verifică dacă un port răspunde."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((gazda, port))
            return True
    except Exception:
        return False


def verifica_http(url: str) -> bool:
    """Verifică dacă un endpoint HTTP răspunde."""
    try:
        from urllib.request import urlopen
        with urlopen(url, timeout=5) as raspuns:
            return raspuns.getcode() == 200
    except Exception:
        return False


def main():
    """Rulează testul rapid."""
    print()
    print("=" * 50)
    print("  TEST RAPID (SMOKE TEST)")
    print("  Laborator Săptămâna 10")
    print("=" * 50)
    print()
    
    timp_start = time.time()
    toate_ok = True
    
    # 1. Docker
    print("  [1/5] Verificare Docker...", end=" ", flush=True)
    if verifica_docker():
        print("✓")
    else:
        print("✗")
        print("        → Porniți Docker Desktop")
        toate_ok = False
    
    # 2. Port HTTP
    print("  [2/5] Verificare HTTP (port 8000)...", end=" ", flush=True)
    if verifica_port(8000):
        print("✓")
    else:
        print("✗")
        print("        → Rulați: python scripts/porneste_lab.py")
        toate_ok = False
    
    # 3. Port DNS
    print("  [3/5] Verificare DNS (port 5353)...", end=" ", flush=True)
    if verifica_port(5353):
        print("✓")
    else:
        print("✗")
        toate_ok = False
    
    # 4. Port SSH
    print("  [4/5] Verificare SSH (port 2222)...", end=" ", flush=True)
    if verifica_port(2222):
        print("✓")
    else:
        print("✗")
        toate_ok = False
    
    # 5. Port FTP
    print("  [5/5] Verificare FTP (port 2121)...", end=" ", flush=True)
    if verifica_port(2121):
        print("✓")
    else:
        print("✗")
        toate_ok = False
    
    # Sumar
    durata = time.time() - timp_start
    print()
    print("─" * 50)
    
    if toate_ok:
        print(f"  ✓ Toate verificările trecute ({durata:.1f}s)")
        print("  Mediul de laborator este pregătit!")
    else:
        print(f"  ✗ Unele verificări au eșuat ({durata:.1f}s)")
        print("  Rulați: python scripts/porneste_lab.py")
    
    print("─" * 50)
    
    return 0 if toate_ok else 1


if __name__ == "__main__":
    sys.exit(main())
