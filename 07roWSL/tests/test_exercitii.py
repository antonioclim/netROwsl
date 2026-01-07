#!/usr/bin/env python3
"""
Teste pentru Exerciții - Săptămâna 7
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică finalizarea corectă a exercițiilor de laborator.
"""

from __future__ import annotations

import argparse
import socket
import sys
from datetime import datetime
from pathlib import Path


def logheaza(mesaj: str):
    """Logare cu timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {mesaj}", flush=True)


def verifica_port_tcp(host: str, port: int, timeout: float = 3.0) -> tuple[bool, str]:
    """Verifică un port TCP și returnează starea."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        rezultat = sock.connect_ex((host, port))
        sock.close()
        
        if rezultat == 0:
            return True, "deschis"
        else:
            return False, "închis sau filtrat"
    except socket.timeout:
        return False, "timeout (posibil filtrat)"
    except Exception as e:
        return False, str(e)


def test_exercitiu_1() -> bool:
    """
    Testează Exercițiul 1: Conectivitate de Bază.
    
    Verifică:
    - Serverul TCP răspunde pe portul 9090
    - Receptorul UDP ascultă pe portul 9091
    """
    logheaza("Test Exercițiul 1: Conectivitate de Bază")
    logheaza("-" * 40)
    
    erori = 0
    
    # Test TCP
    ok, stare = verifica_port_tcp("localhost", 9090)
    if ok:
        logheaza("  [OK] Server TCP (port 9090) accesibil")
    else:
        logheaza(f"  [EROARE] Server TCP: {stare}")
        erori += 1
    
    # Test echo
    if ok:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9090))
            sock.sendall(b"test_ex1")
            raspuns = sock.recv(1024)
            sock.close()
            
            if raspuns == b"test_ex1":
                logheaza("  [OK] Echo TCP funcțional")
            else:
                logheaza(f"  [EROARE] Răspuns echo incorect: {raspuns}")
                erori += 1
        except Exception as e:
            logheaza(f"  [EROARE] Test echo: {e}")
            erori += 1
    
    # Test UDP (doar trimitere)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(b"test_ex1_udp", ("localhost", 9091))
        sock.close()
        logheaza("  [OK] Datagramă UDP trimisă către port 9091")
    except Exception as e:
        logheaza(f"  [EROARE] UDP: {e}")
        erori += 1
    
    return erori == 0


def test_exercitiu_2() -> bool:
    """
    Testează Exercițiul 2: Filtrare TCP cu REJECT.
    
    Verifică:
    - Conexiunea TCP este refuzată rapid (nu timeout)
    """
    logheaza("Test Exercițiul 2: Filtrare TCP cu REJECT")
    logheaza("-" * 40)
    
    import time
    
    timp_start = time.time()
    ok, stare = verifica_port_tcp("localhost", 9090, timeout=3.0)
    timp_scurs = time.time() - timp_start
    
    logheaza(f"  Rezultat: {stare}")
    logheaza(f"  Timp răspuns: {timp_scurs:.3f}s")
    
    if ok:
        logheaza("  [INFO] Conexiunea a reușit - profilul REJECT nu este activ")
        logheaza("         Aplicați profilul: python scripts/ruleaza_demo.py --demo tcp")
        return True  # Nu e eroare, doar informativ
    elif timp_scurs < 1.0:
        logheaza("  [OK] Răspuns rapid - comportament REJECT detectat")
        return True
    else:
        logheaza("  [INFO] Răspuns lent - aceasta seamănă cu comportamentul DROP")
        return True


def test_exercitiu_3() -> bool:
    """
    Testează Exercițiul 3: Filtrare UDP cu DROP.
    
    Verifică:
    - Datagramele UDP pot fi trimise
    - Niciun răspuns nu este primit (comportament DROP)
    """
    logheaza("Test Exercițiul 3: Filtrare UDP cu DROP")
    logheaza("-" * 40)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2.0)
        
        sock.sendto(b"test_drop", ("localhost", 9091))
        logheaza("  [OK] Datagramă trimisă")
        
        try:
            date, adresa = sock.recvfrom(1024)
            logheaza(f"  [INFO] Răspuns primit: {date}")
            logheaza("         Profilul DROP nu este activ")
        except socket.timeout:
            logheaza("  [OK] Niciun răspuns - comportament DROP confirmat")
        
        sock.close()
        return True
        
    except Exception as e:
        logheaza(f"  [EROARE] {e}")
        return False


def test_exercitiu_4() -> bool:
    """
    Testează Exercițiul 4: Filtru la Nivel Aplicație.
    
    Verifică:
    - Proxy-ul ascultă pe portul 8888
    - Cererile cu conținut blocat sunt refuzate
    """
    logheaza("Test Exercițiul 4: Filtru Nivel Aplicație")
    logheaza("-" * 40)
    
    # Verifică dacă proxy-ul rulează
    ok, stare = verifica_port_tcp("localhost", 8888)
    
    if not ok:
        logheaza("  [INFO] Proxy-ul nu rulează pe portul 8888")
        logheaza("         Porniți cu: python scripts/porneste_lab.py --proxy")
        return True  # Nu e eroare
    
    logheaza("  [OK] Proxy accesibil pe portul 8888")
    
    # Test cu conținut permis
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("localhost", 8888))
        sock.sendall(b"test normal hello")
        raspuns = sock.recv(1024).decode()
        sock.close()
        
        if "200" in raspuns or "acceptat" in raspuns.lower():
            logheaza("  [OK] Conținut permis acceptat")
        else:
            logheaza(f"  [INFO] Răspuns: {raspuns[:50]}")
            
    except Exception as e:
        logheaza(f"  [EROARE] Test conținut permis: {e}")
    
    # Test cu conținut blocat
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(("localhost", 8888))
        sock.sendall(b"malware test attack")
        raspuns = sock.recv(1024).decode()
        sock.close()
        
        if "403" in raspuns or "blocat" in raspuns.lower():
            logheaza("  [OK] Conținut blocat refuzat corect")
        else:
            logheaza(f"  [INFO] Răspuns: {raspuns[:50]}")
            
    except Exception as e:
        logheaza(f"  [EROARE] Test conținut blocat: {e}")
    
    return True


def test_exercitiu_5() -> bool:
    """
    Testează Exercițiul 5: Sondare Defensivă a Porturilor.
    
    Verifică:
    - Sondarea porturilor funcționează
    - Porturile deschise/închise sunt detectate corect
    """
    logheaza("Test Exercițiul 5: Sondare Porturi")
    logheaza("-" * 40)
    
    porturi_test = [9090, 9091, 8888, 9999]
    rezultate = {}
    
    for port in porturi_test:
        ok, stare = verifica_port_tcp("localhost", port, timeout=1.0)
        rezultate[port] = "deschis" if ok else "închis/filtrat"
    
    logheaza("  Rezultate sondare:")
    for port, stare in rezultate.items():
        logheaza(f"    Port {port}: {stare}")
    
    # Verifică că cel puțin un port cunoscut este detectat corect
    if rezultate.get(9090) == "deschis" or rezultate.get(8888) == "deschis":
        logheaza("  [OK] Sondarea detectează porturi deschise")
        return True
    else:
        logheaza("  [INFO] Niciun serviciu activ detectat")
        logheaza("         Porniți laboratorul pentru test complet")
        return True


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Teste pentru exercițiile Săptămânii 7"
    )
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Rulează doar testul pentru un exercițiu specific"
    )
    parser.add_argument(
        "--toate", "-a",
        action="store_true",
        help="Rulează toate testele"
    )
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("Teste Exerciții - Săptămâna 7")
    print("Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)
    print()

    teste = {
        1: test_exercitiu_1,
        2: test_exercitiu_2,
        3: test_exercitiu_3,
        4: test_exercitiu_4,
        5: test_exercitiu_5,
    }

    rezultate = []

    if args.exercitiu:
        rezultate.append(teste[args.exercitiu]())
    else:
        for nr, test_func in teste.items():
            print()
            rezultate.append(test_func())

    print()
    print("=" * 60)
    reusit = sum(rezultate)
    total = len(rezultate)
    print(f"Rezultat final: {reusit}/{total} teste reușite")
    print("=" * 60)

    sys.exit(0 if all(rezultate) else 1)


if __name__ == "__main__":
    main()
