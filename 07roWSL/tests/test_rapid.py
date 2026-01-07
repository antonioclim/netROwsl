#!/usr/bin/env python3
"""
Test Rapid (Smoke Test) - Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verificare rapidă că mediul de laborator este funcțional.
Rulați acest test înainte de a începe exercițiile.
"""

from __future__ import annotations

import socket
import subprocess
import sys
from datetime import datetime


def logheaza(mesaj: str, nivel: str = "INFO"):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{nivel}] {mesaj}", flush=True)


def verifica_docker() -> bool:
    """Verifică că Docker rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def verifica_container(nume: str) -> bool:
    """Verifică că un container Docker rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", nume],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "true" in rezultat.stdout.lower()
    except Exception:
        return False


def verifica_port(port: int, protocol: str = "tcp") -> bool:
    """Verifică accesibilitatea unui port."""
    try:
        if protocol == "tcp":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            rezultat = sock.connect_ex(("localhost", port))
            sock.close()
            return rezultat == 0
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(b"test", ("localhost", port))
            sock.close()
            return True
    except Exception:
        return False


def main():
    """Funcția principală - test rapid."""
    print()
    print("╔══════════════════════════════════════════════════════════╗")
    print("║   TEST RAPID - Săptămâna 7                               ║")
    print("║   Curs REȚELE DE CALCULATOARE - ASE, Informatică         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print()

    toate_ok = True

    # Test 1: Docker
    logheaza("Verificare Docker...")
    if verifica_docker():
        logheaza("Docker rulează", "OK")
    else:
        logheaza("Docker NU rulează - porniți Docker Desktop", "EROARE")
        toate_ok = False

    # Test 2: Containere
    containere = [
        ("week7_server_tcp", "Server TCP"),
        ("week7_receptor_udp", "Receptor UDP"),
    ]
    
    logheaza("Verificare containere...")
    for nume_container, descriere in containere:
        if verifica_container(nume_container):
            logheaza(f"  {descriere} rulează", "OK")
        else:
            logheaza(f"  {descriere} NU rulează", "ATENȚIE")
            # Nu setăm toate_ok = False, containerele pot fi oprite

    # Test 3: Porturi
    porturi = [
        (9090, "tcp", "Server TCP Echo"),
        (9091, "udp", "Receptor UDP"),
    ]
    
    logheaza("Verificare porturi...")
    for port, protocol, descriere in porturi:
        if verifica_port(port, protocol):
            logheaza(f"  Port {port}/{protocol} ({descriere}) accesibil", "OK")
        else:
            logheaza(f"  Port {port}/{protocol} ({descriere}) inaccesibil", "ATENȚIE")

    # Test 4: Python
    logheaza("Verificare Python...")
    versiune = sys.version_info
    if versiune >= (3, 11):
        logheaza(f"  Python {versiune.major}.{versiune.minor}", "OK")
    else:
        logheaza(f"  Python {versiune.major}.{versiune.minor} (recomandat 3.11+)", "ATENȚIE")

    # Rezultat final
    print()
    print("═" * 60)
    if toate_ok:
        print("  REZULTAT: Mediul este pregătit pentru laborator!")
        print("  Rulați: python scripts/porneste_lab.py")
    else:
        print("  REZULTAT: Unele componente necesită atenție")
        print("  Consultați documentația pentru rezolvare")
    print("═" * 60)
    print()

    return 0 if toate_ok else 1


if __name__ == "__main__":
    sys.exit(main())
