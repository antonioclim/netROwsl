#!/usr/bin/env python3
"""
Teste pentru Exercițiile de Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică rezultatele exercițiilor din laborator.
"""

import subprocess
import sys
import socket
import argparse
from urllib.request import urlopen
from urllib.error import URLError


class TesterExercitii:
    """Clasă pentru testarea exercițiilor."""
    
    def __init__(self):
        self.trecute = 0
        self.esuate = 0
    
    def test(self, nume: str, conditie: bool, detalii: str = ""):
        """Înregistrează un test."""
        if conditie:
            print(f"  ✓ {nume}")
            self.trecute += 1
        else:
            print(f"  ✗ {nume}")
            if detalii:
                print(f"      {detalii}")
            self.esuate += 1
    
    def sumar(self) -> bool:
        """Afișează sumarul."""
        print()
        print("─" * 50)
        print(f"  Rezultat: {self.trecute} trecute, {self.esuate} eșuate")
        return self.esuate == 0


def testeaza_exercitiu_1():
    """Testează Exercițiul 1: HTTP Service."""
    print("\n  Exercițiul 1: Explorare Serviciu HTTP")
    print("  " + "-" * 40)
    
    tester = TesterExercitii()
    
    # Test 1: Pagina principală
    try:
        with urlopen("http://localhost:8000/", timeout=5) as raspuns:
            tester.test("GET /", raspuns.getcode() == 200)
    except Exception as e:
        tester.test("GET /", False, str(e))
    
    # Test 2: Fișier hello.txt
    try:
        with urlopen("http://localhost:8000/hello.txt", timeout=5) as raspuns:
            tester.test("GET /hello.txt", raspuns.getcode() == 200)
    except Exception as e:
        tester.test("GET /hello.txt", False, str(e))
    
    # Test 3: 404 pentru fișier inexistent
    try:
        urlopen("http://localhost:8000/inexistent.html", timeout=5)
        tester.test("GET /inexistent.html (404)", False)
    except URLError as e:
        tester.test("GET /inexistent.html (404)", hasattr(e, 'code') and e.code == 404)
    
    return tester.sumar()


def testeaza_exercitiu_2():
    """Testează Exercițiul 2: DNS Resolution."""
    print("\n  Exercițiul 2: Rezoluție DNS")
    print("  " + "-" * 40)
    
    tester = TesterExercitii()
    
    domenii_asteptate = {
        "web.lab.local": "172.20.0.10",
        "ssh.lab.local": "172.20.0.22",
        "ftp.lab.local": "172.20.0.21",
    }
    
    for domeniu, ip_asteptat in domenii_asteptate.items():
        try:
            rezultat = subprocess.run(
                ["dig", "@localhost", "-p", "5353", domeniu, "+short"],
                capture_output=True,
                text=True,
                timeout=5
            )
            ip_obtinut = rezultat.stdout.strip()
            tester.test(
                f"DNS {domeniu}",
                ip_obtinut == ip_asteptat,
                f"Obținut: {ip_obtinut}, Așteptat: {ip_asteptat}"
            )
        except Exception as e:
            tester.test(f"DNS {domeniu}", False, str(e))
    
    # Test NXDOMAIN
    try:
        rezultat = subprocess.run(
            ["dig", "@localhost", "-p", "5353", "inexistent.lab.local"],
            capture_output=True,
            text=True,
            timeout=5
        )
        tester.test(
            "NXDOMAIN pentru domeniu inexistent",
            "NXDOMAIN" in rezultat.stdout
        )
    except Exception as e:
        tester.test("NXDOMAIN", False, str(e))
    
    return tester.sumar()


def testeaza_exercitiu_3():
    """Testează Exercițiul 3: SSH Communication."""
    print("\n  Exercițiul 3: Comunicație SSH")
    print("  " + "-" * 40)
    
    tester = TesterExercitii()
    
    # Test conectivitate port SSH
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(("localhost", 2222))
            banner = s.recv(1024).decode('utf-8', errors='ignore')
            tester.test("Port SSH 2222 deschis", True)
            tester.test("Banner SSH prezent", banner.startswith("SSH-"))
    except Exception as e:
        tester.test("Port SSH 2222", False, str(e))
    
    # Test cu Paramiko din container
    try:
        rezultat = subprocess.run(
            ["docker", "exec", "week10_ssh_client", "python", "/app/paramiko_client.py"],
            capture_output=True,
            text=True,
            timeout=30
        )
        tester.test(
            "Conexiune Paramiko din container",
            "Conectat cu succes" in rezultat.stdout or rezultat.returncode == 0
        )
    except Exception as e:
        tester.test("Conexiune Paramiko", False, str(e))
    
    return tester.sumar()


def testeaza_exercitiu_4():
    """Testează Exercițiul 4: FTP Protocol."""
    print("\n  Exercițiul 4: Protocol FTP")
    print("  " + "-" * 40)
    
    tester = TesterExercitii()
    
    # Test conectivitate port FTP
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(("localhost", 2121))
            banner = s.recv(1024).decode('utf-8', errors='ignore')
            tester.test("Port FTP 2121 deschis", True)
            tester.test("Banner FTP (220)", "220" in banner)
    except Exception as e:
        tester.test("Port FTP 2121", False, str(e))
    
    return tester.sumar()


def testeaza_exercitiu_5():
    """Testează Exercițiul 5: HTTPS with TLS."""
    print("\n  Exercițiul 5: HTTPS cu TLS")
    print("  " + "-" * 40)
    
    tester = TesterExercitii()
    
    # Test cu curl -k
    try:
        rezultat = subprocess.run(
            ["curl", "-k", "-s", "-o", "/dev/null", "-w", "%{http_code}",
             "https://localhost:4443/"],
            capture_output=True,
            text=True,
            timeout=10
        )
        cod = rezultat.stdout.strip()
        tester.test("HTTPS GET /", cod == "200", f"Cod: {cod}")
    except Exception as e:
        tester.test("HTTPS GET /", False, f"Porniți serverul: python src/exercises/ex_10_01_https.py")
    
    return tester.sumar()


def testeaza_exercitiu_6():
    """Testează Exercițiul 6: REST Maturity Levels."""
    print("\n  Exercițiul 6: Niveluri REST")
    print("  " + "-" * 40)
    
    tester = TesterExercitii()
    
    # Test niveluri REST
    niveluri = [
        ("Nivelul 0 (RPC)", "http://localhost:5000/api/nivel0", "POST"),
        ("Nivelul 2 (Verbe)", "http://localhost:5000/api/nivel2/produse", "GET"),
        ("Nivelul 3 (HATEOAS)", "http://localhost:5000/api/nivel3/produse", "GET"),
    ]
    
    for nume, url, metoda in niveluri:
        try:
            if metoda == "GET":
                with urlopen(url, timeout=5) as raspuns:
                    tester.test(nume, raspuns.getcode() == 200)
            else:
                import urllib.request
                import json
                cerere = urllib.request.Request(
                    url,
                    data=json.dumps({"actiune": "listeaza"}).encode(),
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urlopen(cerere, timeout=5) as raspuns:
                    tester.test(nume, raspuns.getcode() == 200)
        except Exception as e:
            tester.test(nume, False, f"Porniți serverul: python src/exercises/ex_10_02_rest_levels.py")
    
    return tester.sumar()


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Testează Exercițiile de Laborator"
    )
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help="Testează un exercițiu specific"
    )
    args = parser.parse_args()
    
    print()
    print("=" * 50)
    print("  TESTE EXERCIȚII - LABORATOR SĂPTĂMÂNA 10")
    print("=" * 50)
    
    if args.exercitiu:
        functii = {
            1: testeaza_exercitiu_1,
            2: testeaza_exercitiu_2,
            3: testeaza_exercitiu_3,
            4: testeaza_exercitiu_4,
            5: testeaza_exercitiu_5,
            6: testeaza_exercitiu_6,
        }
        succes = functii[args.exercitiu]()
    else:
        rezultate = []
        for i, func in enumerate([
            testeaza_exercitiu_1,
            testeaza_exercitiu_2,
            testeaza_exercitiu_3,
            testeaza_exercitiu_4,
            testeaza_exercitiu_5,
            testeaza_exercitiu_6,
        ], 1):
            try:
                rezultate.append(func())
            except Exception as e:
                print(f"  Eroare la exercițiul {i}: {e}")
                rezultate.append(False)
        
        succes = all(rezultate)
    
    print()
    print("=" * 50)
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
