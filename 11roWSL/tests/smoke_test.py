#!/usr/bin/env python3
"""
Test de Fum - Verificare Rapidă
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Verifică rapid dacă componentele principale funcționează.
Rulați acest script pentru o verificare rapidă înainte de laborator.
"""

import socket
import subprocess
import sys
from pathlib import Path


def print_status(mesaj: str, succes: bool):
    """Afișează starea unei verificări."""
    simbol = "✓" if succes else "✗"
    culoare = "\033[32m" if succes else "\033[31m"
    reset = "\033[0m"
    
    if sys.stdout.isatty():
        print(f"{culoare}{simbol}{reset} {mesaj}")
    else:
        print(f"[{'OK' if succes else 'EȘUAT'}] {mesaj}")


def verifica_port(host: str, port: int, timeout: float = 2.0) -> bool:
    """Verifică dacă un port răspunde."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            return True
    except Exception:
        return False


def verifica_http(host: str, port: int, path: str = "/") -> bool:
    """Verifică dacă un server HTTP răspunde cu 200."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((host, port))
            
            cerere = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.sendall(cerere.encode())
            
            raspuns = s.recv(1024).decode('utf-8', errors='ignore')
            return "200" in raspuns.split('\r\n')[0]
    except Exception:
        return False


def main():
    print("=" * 50)
    print("Test de Fum - Săptămâna 11")
    print("=" * 50)
    print()
    
    toate_ok = True
    
    # Verifică Docker
    print("Verificare Docker:")
    
    docker_ok = subprocess.run(
        ["docker", "info"],
        capture_output=True
    ).returncode == 0
    print_status("Docker rulează", docker_ok)
    toate_ok = toate_ok and docker_ok
    
    # Verifică containere
    result = subprocess.run(
        ["docker", "ps", "--filter", "name=s11_", "--format", "{{.Names}}"],
        capture_output=True,
        text=True
    )
    containere = [c for c in result.stdout.strip().split('\n') if c]
    containere_ok = len(containere) >= 3
    print_status(f"Containere s11_* active ({len(containere)})", containere_ok)
    
    # Verifică porturi
    print("\nVerificare porturi:")
    
    port_8080 = verifica_port("localhost", 8080)
    print_status("Port 8080 (echilibror)", port_8080)
    toate_ok = toate_ok and port_8080
    
    # Verifică HTTP
    print("\nVerificare HTTP:")
    
    http_ok = verifica_http("localhost", 8080)
    print_status("HTTP 200 de la echilibror", http_ok)
    toate_ok = toate_ok and http_ok
    
    health_ok = verifica_http("localhost", 8080, "/health")
    print_status("Endpoint /health", health_ok)
    
    # Verifică distribuție
    print("\nVerificare distribuție:")
    
    backend_uri = set()
    for _ in range(6):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(2.0)
                s.connect(("localhost", 8080))
                s.sendall(b"GET / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n")
                raspuns = s.recv(4096).decode('utf-8', errors='ignore').lower()
                for i in range(1, 4):
                    if f"web{i}" in raspuns:
                        backend_uri.add(i)
        except Exception:
            pass
    
    distributie_ok = len(backend_uri) >= 2
    print_status(f"Distribuție pe {len(backend_uri)} backend(-uri)", distributie_ok)
    
    # Sumar
    print()
    print("=" * 50)
    if toate_ok and distributie_ok:
        print("✓ Toate verificările principale au trecut!")
        print("  Mediul este pregătit pentru laborator.")
        return 0
    else:
        print("✗ Unele verificări au eșuat.")
        print("  Consultați documentația de depanare.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
