#!/usr/bin/env python3
"""
Teste Mediu Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică conectivitatea și funcționalitatea serviciilor.
"""

import sys
import socket
import subprocess
from typing import List, Tuple

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

class RezultatTest:
    def __init__(self, nume: str, trecut: bool, mesaj: str = ""):
        self.nume = nume
        self.trecut = trecut
        self.mesaj = mesaj

def test_docker_pornit() -> RezultatTest:
    """Verifică dacă Docker rulează."""
    try:
        result = subprocess.run(["docker", "info"], capture_output=True, timeout=10)
        return RezultatTest("Docker pornit", result.returncode == 0)
    except Exception as e:
        return RezultatTest("Docker pornit", False, str(e))

def test_containere_ruleaza() -> List[RezultatTest]:
    """Verifică containerele laboratorului."""
    rezultate = []
    containere = ["week14_app1", "week14_app2", "week14_lb", "week14_echo"]
    
    for container in containere:
        try:
            result = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Running}}", container],
                capture_output=True, text=True, timeout=5
            )
            ruleaza = result.stdout.strip() == "true"
            rezultate.append(RezultatTest(f"Container {container}", ruleaza))
        except Exception as e:
            rezultate.append(RezultatTest(f"Container {container}", False, str(e)))
    
    return rezultate

def test_conectivitate_http() -> List[RezultatTest]:
    """Verifică endpoint-urile HTTP."""
    rezultate = []
    endpoint_uri = [
        ("http://localhost:8080/", "Load Balancer"),
        ("http://localhost:8001/", "Backend App 1"),
        ("http://localhost:8002/", "Backend App 2"),
    ]
    
    for url, nume in endpoint_uri:
        try:
            raspuns = requests.get(url, timeout=5)
            trecut = raspuns.status_code == 200
            rezultate.append(RezultatTest(
                f"HTTP {nume}", trecut, f"Status: {raspuns.status_code}"
            ))
        except Exception as e:
            rezultate.append(RezultatTest(f"HTTP {nume}", False, str(e)))
    
    return rezultate

def test_echo_tcp() -> RezultatTest:
    """Verifică serverul echo TCP."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 9000))
        
        mesaj_test = "Test123\n"
        sock.sendall(mesaj_test.encode())
        raspuns = sock.recv(1024).decode()
        sock.close()
        
        trecut = "Test123" in raspuns
        return RezultatTest("Server Echo TCP", trecut, raspuns[:30])
    except Exception as e:
        return RezultatTest("Server Echo TCP", False, str(e))

def ruleaza_toate_testele() -> Tuple[int, int]:
    """Rulează toate testele și afișează rezultatele."""
    total_trecut = 0
    total_teste = 0
    
    # Docker
    print(f"\n{Culori.BOLD}Teste Docker:{Culori.FINAL}")
    rezultat = test_docker_pornit()
    if rezultat.trecut:
        print(f"  {Culori.VERDE}[TRECUT]{Culori.FINAL} {rezultat.nume}")
        total_trecut += 1
    else:
        print(f"  {Culori.ROSU}[EȘUAT]{Culori.FINAL} {rezultat.nume}: {rezultat.mesaj}")
    total_teste += 1
    
    # Containere
    print(f"\n{Culori.BOLD}Teste Containere:{Culori.FINAL}")
    for rezultat in test_containere_ruleaza():
        if rezultat.trecut:
            print(f"  {Culori.VERDE}[TRECUT]{Culori.FINAL} {rezultat.nume}")
            total_trecut += 1
        else:
            print(f"  {Culori.ROSU}[EȘUAT]{Culori.FINAL} {rezultat.nume}: {rezultat.mesaj}")
        total_teste += 1
    
    # HTTP
    print(f"\n{Culori.BOLD}Teste HTTP:{Culori.FINAL}")
    for rezultat in test_conectivitate_http():
        if rezultat.trecut:
            print(f"  {Culori.VERDE}[TRECUT]{Culori.FINAL} {rezultat.nume}")
            total_trecut += 1
        else:
            print(f"  {Culori.ROSU}[EȘUAT]{Culori.FINAL} {rezultat.nume}: {rezultat.mesaj}")
        total_teste += 1
    
    # Echo TCP
    print(f"\n{Culori.BOLD}Teste TCP:{Culori.FINAL}")
    rezultat = test_echo_tcp()
    if rezultat.trecut:
        print(f"  {Culori.VERDE}[TRECUT]{Culori.FINAL} {rezultat.nume}")
        total_trecut += 1
    else:
        print(f"  {Culori.ROSU}[EȘUAT]{Culori.FINAL} {rezultat.nume}: {rezultat.mesaj}")
    total_teste += 1
    
    return total_trecut, total_teste

def main():
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Teste Mediu Laborator Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    trecut, total = ruleaza_toate_testele()
    
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"Rezultate: {trecut}/{total} teste trecute")
    
    if trecut == total:
        print(f"{Culori.VERDE}✓ Toate testele au trecut!{Culori.FINAL}")
    else:
        print(f"{Culori.GALBEN}! Unele teste au eșuat.{Culori.FINAL}")
    
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    return 0 if trecut == total else 1

if __name__ == "__main__":
    sys.exit(main())
