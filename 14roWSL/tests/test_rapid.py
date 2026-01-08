#!/usr/bin/env python3
"""
Test Rapid (Smoke Test) - Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verificare rapidă a funcționalității mediului (<60 secunde).
"""

import sys
import socket
import subprocess
import time
import json
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import List

try:
    import requests
except ImportError:
    print("Eroare: Pachetul 'requests' nu este instalat.")
    sys.exit(1)

class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

@dataclass
class RezultatTest:
    nume: str
    trecut: bool
    durata_ms: float
    mesaj: str = ""

class RaportTestRapid:
    def __init__(self):
        self.rezultate: List[RezultatTest] = []
        self.timp_inceput = time.time()
    
    def adauga(self, rezultat: RezultatTest):
        self.rezultate.append(rezultat)
    
    @property
    def trecute(self) -> int:
        return sum(1 for r in self.rezultate if r.trecut)
    
    @property
    def esuate(self) -> int:
        return sum(1 for r in self.rezultate if not r.trecut)
    
    @property
    def durata_totala(self) -> float:
        return time.time() - self.timp_inceput
    
    def afiseaza(self):
        print(f"\n{Culori.BOLD}Rezultate Test Rapid:{Culori.FINAL}")
        print("-" * 50)
        
        for r in self.rezultate:
            if r.trecut:
                simbol = f"{Culori.VERDE}✓{Culori.FINAL}"
            else:
                simbol = f"{Culori.ROSU}✗{Culori.FINAL}"
            
            print(f"  {simbol} {r.nume} ({r.durata_ms:.0f}ms)")
            if r.mesaj and not r.trecut:
                print(f"      {r.mesaj}")
        
        print()
        print(f"Total: {self.trecute}/{len(self.rezultate)} trecute în {self.durata_totala*1000:.0f}ms")
    
    def exporta_json(self) -> dict:
        return {
            "trecute": self.trecute,
            "esuate": self.esuate,
            "durata_ms": self.durata_totala * 1000,
            "rezultate": [
                {
                    "nume": r.nume,
                    "trecut": r.trecut,
                    "durata_ms": r.durata_ms,
                    "mesaj": r.mesaj
                }
                for r in self.rezultate
            ]
        }

def masoara_timp(func):
    """Decorator pentru măsurarea timpului de execuție."""
    def wrapper(*args, **kwargs):
        start = time.time()
        rezultat = func(*args, **kwargs)
        durata = (time.time() - start) * 1000
        return rezultat, durata
    return wrapper

@masoara_timp
def test_docker_pornit():
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=5)
        return result.returncode == 0, ""
    except Exception as e:
        return False, str(e)

@masoara_timp
def test_containere_ruleaza():
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=week14", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=5
        )
        containere = result.stdout.strip().split('\n')
        numar = len([c for c in containere if c])
        return numar >= 4, f"{numar} containere"
    except Exception as e:
        return False, str(e)

@masoara_timp
def test_retea_configurata():
    try:
        result = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True, text=True, timeout=5
        )
        retele = result.stdout
        are_backend = "backend" in retele
        are_frontend = "frontend" in retele
        return are_backend and are_frontend, ""
    except Exception as e:
        return False, str(e)

@masoara_timp
def test_port_accesibil(port, nume):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        result = sock.connect_ex(('localhost', port))
        sock.close()
        return result == 0, ""
    except Exception as e:
        return False, str(e)

@masoara_timp
def test_raspuns_http():
    try:
        raspuns = requests.get("http://localhost:8080/", timeout=3)
        return raspuns.status_code == 200, f"Status: {raspuns.status_code}"
    except Exception as e:
        return False, str(e)

@masoara_timp
def test_echo_functional():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('localhost', 9090))
        sock.sendall(b"Test\n")
        raspuns = sock.recv(1024).decode()
        sock.close()
        return "Test" in raspuns, raspuns[:20]
    except Exception as e:
        return False, str(e)

@masoara_timp
def test_round_robin():
    try:
        backend_uri = set()
        for _ in range(6):
            raspuns = requests.get("http://localhost:8080/", timeout=2)
            if "app1" in raspuns.text.lower():
                backend_uri.add("app1")
            elif "app2" in raspuns.text.lower():
                backend_uri.add("app2")
        return len(backend_uri) >= 2, f"Backend-uri: {backend_uri}"
    except Exception as e:
        return False, str(e)

def ruleaza_test_rapid(output_json=False):
    """Rulează testele rapide."""
    raport = RaportTestRapid()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Test Rapid (Smoke Test) - Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print("\nSe rulează testele...")
    
    # Test 1: Docker
    (trecut, mesaj), durata = test_docker_pornit()
    raport.adauga(RezultatTest("Docker pornit", trecut, durata, mesaj))
    
    # Test 2: Containere
    (trecut, mesaj), durata = test_containere_ruleaza()
    raport.adauga(RezultatTest("Containere rulează", trecut, durata, mesaj))
    
    # Test 3: Rețele
    (trecut, mesaj), durata = test_retea_configurata()
    raport.adauga(RezultatTest("Rețele configurate", trecut, durata, mesaj))
    
    # Test 4-7: Porturi
    porturi = [(8080, "LB"), (8001, "App1"), (8002, "App2"), (9090, "Echo")]
    for port, nume in porturi:
        (trecut, mesaj), durata = test_port_accesibil(port, nume)
        raport.adauga(RezultatTest(f"Port {port} ({nume})", trecut, durata, mesaj))
    
    # Test 8: HTTP
    (trecut, mesaj), durata = test_raspuns_http()
    raport.adauga(RezultatTest("Răspuns HTTP", trecut, durata, mesaj))
    
    # Test 9: Echo
    (trecut, mesaj), durata = test_echo_functional()
    raport.adauga(RezultatTest("Echo funcțional", trecut, durata, mesaj))
    
    # Test 10: Round-robin
    (trecut, mesaj), durata = test_round_robin()
    raport.adauga(RezultatTest("Distribuție round-robin", trecut, durata, mesaj))
    
    raport.afiseaza()
    
    if output_json:
        print(f"\n{Culori.BOLD}JSON:{Culori.FINAL}")
        print(json.dumps(raport.exporta_json(), indent=2))
    
    return 0 if raport.esuate == 0 else 1

def main():
    parser = argparse.ArgumentParser(
        description="Test Rapid (Smoke Test) - Săptămâna 14",
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    parser.add_argument("--json", "-j", action="store_true", help="Afișează rezultate în format JSON")
    args = parser.parse_args()
    
    return ruleaza_test_rapid(args.json)

if __name__ == "__main__":
    sys.exit(main())
