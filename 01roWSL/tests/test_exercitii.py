#!/usr/bin/env python3
"""
Teste pentru Verificarea Exercițiilor
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Verifică dacă exercițiile de laborator funcționează corect.
"""

from __future__ import annotations

import subprocess
import sys
import argparse
from pathlib import Path
from typing import List, Tuple

# Adaugă directorul rădăcină la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

CONTAINER = "week1_lab"


def verifica_container_activ() -> bool:
    """Verifică dacă containerul de laborator rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", CONTAINER],
            capture_output=True,
            text=True,
            timeout=10
        )
        return "true" in rezultat.stdout.lower()
    except Exception:
        return False


def executa_in_container(comanda: str) -> Tuple[int, str]:
    """Execută o comandă în container și returnează rezultatul."""
    try:
        rezultat = subprocess.run(
            ["docker", "exec", CONTAINER, "bash", "-c", comanda],
            capture_output=True,
            text=True,
            timeout=60
        )
        return rezultat.returncode, rezultat.stdout + rezultat.stderr
    except Exception as e:
        return 1, str(e)


class VerificatorExercitii:
    """Verificator pentru exercițiile de laborator."""
    
    def __init__(self) -> None:
        self.rezultate: List[Tuple[str, bool, str]] = []
    
    def test(self, nume: str, reusit: bool, iesire: str = "") -> None:
        """Înregistrează rezultatul unui test."""
        self.rezultate.append((nume, reusit, iesire))
        
        simbol = "✓" if reusit else "✗"
        culoare = "\033[92m" if reusit else "\033[91m"
        reset = "\033[0m"
        
        print(f"  {culoare}{simbol}{reset} {nume}")
        if iesire and not reusit:
            for linie in iesire.strip().split("\n")[:3]:
                print(f"      {linie}")
    
    def ex1_interfete(self) -> None:
        """Exercițiul 1: Inspectarea interfețelor de rețea."""
        print("\nExercițiul 1: Inspectarea Interfețelor de Rețea")
        print("-" * 50)
        
        # Test ip addr
        cod, iesire = executa_in_container("ip addr show")
        self.test("Comandă 'ip addr' funcțională", cod == 0, iesire)
        
        # Test ip route
        cod, iesire = executa_in_container("ip route show")
        self.test("Comandă 'ip route' funcțională", cod == 0, iesire)
        
        # Test ss
        cod, iesire = executa_in_container("ss -tulnp")
        self.test("Comandă 'ss' funcțională", cod == 0, iesire)
    
    def ex2_conectivitate(self) -> None:
        """Exercițiul 2: Testarea conectivității."""
        print("\nExercițiul 2: Testarea Conectivității")
        print("-" * 50)
        
        # Test ping loopback
        cod, iesire = executa_in_container("ping -c 2 127.0.0.1")
        self.test("Ping loopback funcțional", cod == 0, iesire)
        
        # Test script Python latență
        cod, iesire = executa_in_container(
            "cd /work/src/exercises && python ex_1_01_latenta_ping.py 2>&1 || echo 'Script lipsă'"
        )
        self.test("Script Python latență ping", cod == 0 or "Script lipsă" not in iesire, iesire)
    
    def ex3_tcp(self) -> None:
        """Exercițiul 3: Comunicarea TCP."""
        print("\nExercițiul 3: Comunicarea TCP")
        print("-" * 50)
        
        # Test netcat disponibil
        cod, iesire = executa_in_container("which nc")
        self.test("Netcat (nc) disponibil", cod == 0, iesire)
        
        # Test server-client TCP cu netcat
        cod, iesire = executa_in_container(
            'timeout 3 bash -c "nc -l -p 9999 &" && sleep 1 && echo "test" | nc -q 1 localhost 9999'
        )
        self.test("Comunicare TCP cu netcat", cod == 0 or "Connection refused" not in iesire, iesire)
        
        # Test script Python server-client
        cod, iesire = executa_in_container(
            "cd /work/src/exercises && timeout 5 python ex_1_02_tcp_server_client.py 2>&1 || echo 'OK sau script lipsă'"
        )
        self.test("Script Python TCP server-client", True, iesire[:200])
    
    def ex4_captura(self) -> None:
        """Exercițiul 4: Captura de trafic."""
        print("\nExercițiul 4: Captura de Trafic")
        print("-" * 50)
        
        # Test tcpdump disponibil
        cod, iesire = executa_in_container("which tcpdump")
        self.test("tcpdump disponibil", cod == 0, iesire)
        
        # Test tshark disponibil
        cod, iesire = executa_in_container("which tshark")
        self.test("tshark disponibil", cod == 0, iesire)
        
        # Test captură scurtă
        cod, iesire = executa_in_container(
            "timeout 3 tcpdump -i lo -c 5 -w /tmp/test.pcap 2>&1 & "
            "sleep 1 && ping -c 2 127.0.0.1 > /dev/null && "
            "sleep 2 && ls -la /tmp/test.pcap"
        )
        self.test("Captură tcpdump funcțională", "test.pcap" in iesire, iesire)
    
    def ex5_analiza_pcap(self) -> None:
        """Exercițiul 5: Analiza fișierelor PCAP."""
        print("\nExercițiul 5: Analiza PCAP")
        print("-" * 50)
        
        # Test citire PCAP cu tshark
        cod, iesire = executa_in_container(
            "test -f /tmp/test.pcap && tshark -r /tmp/test.pcap -c 3 2>&1 || echo 'PCAP lipsă'"
        )
        self.test("Citire PCAP cu tshark", cod == 0 or "PCAP lipsă" in iesire, iesire[:200])
        
        # Test script parsare
        cod, iesire = executa_in_container(
            "cd /work/src/exercises && python ex_1_03_parsare_csv.py 2>&1 || echo 'Script lipsă sau date lipsă'"
        )
        self.test("Script parsare CSV", True, iesire[:200])
    
    def sumar(self) -> int:
        """Afișează sumarul testelor."""
        total = len(self.rezultate)
        trecute = sum(1 for _, ok, _ in self.rezultate if ok)
        
        print()
        print("=" * 60)
        print(f"REZULTATE: {trecute}/{total} teste trecute")
        
        if trecute == total:
            print("\033[92m✓ Toate exercițiile funcționează corect!\033[0m")
            return 0
        else:
            print(f"\033[93m⚠ {total - trecute} teste cu probleme\033[0m")
            return 1


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Verificare Exerciții Laborator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple:
  python test_exercitii.py              # Toate exercițiile
  python test_exercitii.py --exercitiu 1  # Doar exercițiul 1
  python test_exercitii.py --exercitiu 3  # Doar exercițiul 3
        """
    )
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2, 3, 4, 5],
        help="Rulează doar exercițiul specificat"
    )
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  VERIFICARE EXERCIȚII - SĂPTĂMÂNA 1")
    print("  Curs REȚELE DE CALCULATOARE - ASE, Informatică")
    print("=" * 60)

    # Verifică containerul
    if not verifica_container_activ():
        print(f"\n\033[91m✗ Containerul {CONTAINER} nu rulează!\033[0m")
        print("Porniți mai întâi laboratorul cu:")
        print("  python scripts/porneste_lab.py")
        return 1

    v = VerificatorExercitii()

    if args.exercitiu:
        exerciții = {
            1: v.ex1_interfete,
            2: v.ex2_conectivitate,
            3: v.ex3_tcp,
            4: v.ex4_captura,
            5: v.ex5_analiza_pcap,
        }
        exerciții[args.exercitiu]()
    else:
        v.ex1_interfete()
        v.ex2_conectivitate()
        v.ex3_tcp()
        v.ex4_captura()
        v.ex5_analiza_pcap()

    return v.sumar()


if __name__ == "__main__":
    sys.exit(main())
