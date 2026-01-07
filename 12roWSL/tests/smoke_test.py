#!/usr/bin/env python3
"""
Test Rapid de Verificare (Smoke Test)
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Verifică rapid dacă toate serviciile de laborator sunt funcționale.
"""

import sys
import socket


def verifica_port(host: str, port: int, timeout: float = 3.0) -> bool:
    """Verifică dacă un port răspunde."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            rezultat = s.connect_ex((host, port))
            return rezultat == 0
    except Exception:
        return False


def main():
    """Funcția principală de verificare."""
    print("=" * 60)
    print("Test Rapid de Verificare - Laboratorul Săptămânii 12")
    print("=" * 60)
    print()
    
    servicii = [
        ("Server SMTP", "localhost", 1025),
        ("Server JSON-RPC", "localhost", 6200),
        ("Server XML-RPC", "localhost", 6201),
        ("Server gRPC", "localhost", 6251),
        ("Portainer", "localhost", 9443)
    ]
    
    toate_ok = True
    
    for nume, host, port in servicii:
        activ = verifica_port(host, port)
        
        if activ:
            status = "\033[92m✓ ACTIV\033[0m"
        else:
            status = "\033[91m✗ INACTIV\033[0m"
            toate_ok = False
        
        print(f"  {status}  {nume:20} ({host}:{port})")
    
    print()
    print("=" * 60)
    
    if toate_ok:
        print("\033[92m✓ Toate serviciile sunt active!\033[0m")
        print("  Mediul de laborator este pregătit pentru lucru.")
        return 0
    else:
        print("\033[91m✗ Unele servicii nu sunt active.\033[0m")
        print("  Rulați: python scripts/porneste_lab.py")
        return 1


if __name__ == "__main__":
    sys.exit(main())
