#!/usr/bin/env python3
"""
Teste de Mediu pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică dacă mediul de laborator este configurat corect.
"""

import subprocess
import sys
import socket
from pathlib import Path


class TesterMediu:
    """Clasă pentru testarea mediului de laborator."""
    
    def __init__(self):
        self.rezultate = []
        self.radacina = Path(__file__).parent.parent
    
    def test(self, nume: str, conditie: bool, detalii: str = "") -> bool:
        """Înregistrează rezultatul unui test."""
        self.rezultate.append({
            "nume": nume,
            "trecut": conditie,
            "detalii": detalii
        })
        
        simbol = "✓" if conditie else "✗"
        print(f"  {simbol} {nume}")
        if detalii and not conditie:
            print(f"      {detalii}")
        
        return conditie
    
    def sumar(self) -> bool:
        """Afișează sumarul testelor."""
        trecute = sum(1 for r in self.rezultate if r["trecut"])
        total = len(self.rezultate)
        
        print()
        print("─" * 50)
        print(f"  Rezultat: {trecute}/{total} teste trecute")
        print("─" * 50)
        
        return trecute == total


def testeaza_docker() -> bool:
    """Testează disponibilitatea Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def testeaza_container(nume: str) -> bool:
    """Verifică dacă un container rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "inspect", "--format", "{{.State.Running}}", nume],
            capture_output=True,
            text=True,
            timeout=5
        )
        return rezultat.stdout.strip() == "true"
    except Exception:
        return False


def testeaza_port(port: int, gazda: str = "localhost") -> bool:
    """Verifică dacă un port răspunde."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            s.connect((gazda, port))
            return True
    except Exception:
        return False


def testeaza_pachet_python(nume: str) -> bool:
    """Verifică dacă un pachet Python este instalat."""
    try:
        __import__(nume)
        return True
    except ImportError:
        return False


def main():
    """Funcția principală de testare."""
    print()
    print("=" * 50)
    print("  TESTE DE MEDIU - LABORATOR SĂPTĂMÂNA 10")
    print("=" * 50)
    print()
    
    tester = TesterMediu()
    
    # Teste Docker
    print("  Docker:")
    tester.test("Docker disponibil", testeaza_docker())
    
    # Teste containere
    print("\n  Containere:")
    containere = [
        "week10_web",
        "week10_dns",
        "week10_ssh",
        "week10_ftp",
        "week10_debug",
    ]
    
    for container in containere:
        tester.test(
            f"Container {container}",
            testeaza_container(container),
            "Rulați: python scripts/porneste_lab.py"
        )
    
    # Teste porturi
    print("\n  Porturi:")
    porturi = [
        (8000, "HTTP"),
        (5353, "DNS"),
        (2222, "SSH"),
        (2121, "FTP"),
    ]
    
    for port, nume in porturi:
        tester.test(
            f"Port {port} ({nume})",
            testeaza_port(port)
        )
    
    # Teste pachete Python
    print("\n  Pachete Python:")
    pachete = ["docker", "requests", "flask", "paramiko", "dnslib"]
    
    for pachet in pachete:
        tester.test(
            f"Pachet {pachet}",
            testeaza_pachet_python(pachet),
            f"pip install {pachet}"
        )
    
    # Teste structură
    print("\n  Structură proiect:")
    directoare = ["docker", "scripts", "src", "tests", "docs"]
    
    for director in directoare:
        cale = tester.radacina / director
        tester.test(
            f"Director {director}/",
            cale.exists()
        )
    
    succes = tester.sumar()
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
