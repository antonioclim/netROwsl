#!/usr/bin/env python3
"""
Test de Funcționare (Smoke Test)
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verificare rapidă că mediul de laborator funcționează corect.

Utilizare:
    python tests/test_rapid.py
"""

import socket
import sys
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

# Coduri culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
RESETARE = "\033[0m"


def afiseaza_rezultat(nume: str, trecut: bool, detalii: str = ""):
    """Afișează rezultatul unui test."""
    status = f"{VERDE}TRECUT{RESETARE}" if trecut else f"{ROSU}EȘUAT{RESETARE}"
    print(f"  [{status}] {nume}")
    if detalii and not trecut:
        print(f"          {detalii}")


def test_port_deschis(port: int) -> bool:
    """Verifică dacă un port este deschis."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex(("127.0.0.1", port))
            return result == 0
    except Exception:
        return False


def test_raspuns_http(url: str) -> tuple:
    """Verifică dacă un URL răspunde."""
    try:
        with urlopen(url, timeout=5) as response:
            return True, response.status
    except URLError as e:
        return False, str(e)
    except Exception as e:
        return False, str(e)


def test_echilibrare_round_robin() -> tuple:
    """Testează distribuția round-robin."""
    try:
        backend_uri = []
        for _ in range(6):
            with urlopen("http://localhost:8080/", timeout=5) as response:
                for antet in ['X-Backend-ID', 'X-Backend-Name']:
                    valoare = response.headers.get(antet)
                    if valoare:
                        backend_uri.append(valoare)
                        break
        
        # Verifică dacă avem rotație
        unice = set(backend_uri)
        if len(unice) >= 2:
            return True, f"Găsite {len(unice)} backend-uri: {unice}"
        else:
            return False, f"Doar {len(unice)} backend găsit"
    except Exception as e:
        return False, str(e)


def main():
    """Rulează toate testele."""
    print()
    print("=" * 60)
    print("Test Rapid - Laborator Săptămâna 8")
    print("=" * 60)
    print()
    
    teste_trecute = 0
    teste_totale = 0
    
    # Test 1: Port 8080
    print("Conectivitate:")
    teste_totale += 1
    trecut = test_port_deschis(8080)
    afiseaza_rezultat("Portul 8080 deschis", trecut, "Porniți laboratorul cu: python scripts/porneste_laborator.py")
    if trecut:
        teste_trecute += 1
    
    if not trecut:
        print()
        print(f"{GALBEN}Laboratorul nu pare să ruleze.{RESETARE}")
        print("Porniți-l cu: python scripts/porneste_laborator.py")
        return 1
    
    # Test 2: Răspuns HTTP
    print()
    print("Răspunsuri HTTP:")
    teste_totale += 1
    trecut, detalii = test_raspuns_http("http://localhost:8080/")
    afiseaza_rezultat("GET / returnează 200", trecut and detalii == 200, str(detalii))
    if trecut and detalii == 200:
        teste_trecute += 1
    
    # Test 3: Endpoint sănătate
    teste_totale += 1
    trecut, detalii = test_raspuns_http("http://localhost:8080/nginx-health")
    afiseaza_rezultat("Endpoint sănătate răspunde", trecut, str(detalii))
    if trecut:
        teste_trecute += 1
    
    # Test 4: Echilibrare round-robin
    print()
    print("Echilibrare încărcare:")
    teste_totale += 1
    trecut, detalii = test_echilibrare_round_robin()
    afiseaza_rezultat("Distribuție round-robin", trecut, detalii)
    if trecut:
        teste_trecute += 1
    
    # Test 5: Structura fișierelor
    print()
    print("Structura fișierelor:")
    radacina = Path(__file__).parent.parent
    fisiere_necesare = [
        "docker/docker-compose.yml",
        "scripts/porneste_laborator.py",
        "src/exercises/ex_8_01_server_http.py",
        "www/index.html"
    ]
    
    toate_exista = True
    for fisier in fisiere_necesare:
        cale = radacina / fisier
        if not cale.exists():
            toate_exista = False
            afiseaza_rezultat(f"Fișier: {fisier}", False)
    
    teste_totale += 1
    if toate_exista:
        afiseaza_rezultat("Toate fișierele necesare prezente", True)
        teste_trecute += 1
    
    # Sumar
    print()
    print("=" * 60)
    rata = (teste_trecute / teste_totale) * 100
    
    if teste_trecute == teste_totale:
        print(f"{VERDE}Toate testele au trecut! ({teste_trecute}/{teste_totale}){RESETARE}")
        print()
        print("Pași următori:")
        print("  1. Deschideți Portainer: https://localhost:9443")
        print("  2. Începeți exercițiile: src/exercises/")
        print("  3. Capturați trafic cu Wireshark")
    else:
        print(f"{GALBEN}Rezultat: {teste_trecute}/{teste_totale} teste trecute ({rata:.0f}%){RESETARE}")
        print()
        print("Verificați problemele de mai sus și încercați din nou.")
    
    print("=" * 60)
    
    return 0 if teste_trecute == teste_totale else 1


if __name__ == "__main__":
    sys.exit(main())
