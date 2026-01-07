#!/usr/bin/env python3
"""
Teste pentru Exerciții - Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică funcționalitatea exercițiilor de laborator.
"""

import subprocess
import sys
import socket
import time
import threading
import argparse
from pathlib import Path
from typing import List, Tuple, Optional
from dataclasses import dataclass

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))


@dataclass
class RezultatTest:
    """Rezultatul unui test individual."""
    nume: str
    succes: bool
    durată_ms: float
    mesaj: str = ""


class TesterExerciții:
    """Executor de teste pentru exercițiile de laborator."""
    
    def __init__(self, host: str = "localhost"):
        self.host = host
        self.rezultate: List[RezultatTest] = []
    
    def adaugă_rezultat(self, rezultat: RezultatTest) -> None:
        """Adaugă un rezultat de test."""
        self.rezultate.append(rezultat)
        
        simbol = "✓" if rezultat.succes else "✗"
        culoare = "\033[92m" if rezultat.succes else "\033[91m"
        resetare = "\033[0m"
        
        print(f"  {culoare}{simbol}{resetare} {rezultat.nume} ({rezultat.durată_ms:.1f}ms)")
        if rezultat.mesaj and not rezultat.succes:
            print(f"      {rezultat.mesaj}")
    
    # ========================================================================
    # Teste Exercițiul 1: TCP
    # ========================================================================
    
    def test_tcp_conexiune(self, port: int = 9090) -> RezultatTest:
        """Testează conexiunea TCP de bază."""
        start = time.perf_counter()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self.host, port))
                durată = (time.perf_counter() - start) * 1000
                
                return RezultatTest(
                    nume="TCP: Conexiune de bază",
                    succes=True,
                    durată_ms=durată,
                    mesaj="Conexiune stabilită cu succes"
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="TCP: Conexiune de bază",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_tcp_echo(self, port: int = 9090) -> RezultatTest:
        """Testează funcționalitatea echo TCP."""
        start = time.perf_counter()
        mesaj_test = "test mesaj"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self.host, port))
                sock.sendall(mesaj_test.encode())
                răspuns = sock.recv(1024).decode().strip()
                
                durată = (time.perf_counter() - start) * 1000
                
                # Verificăm că răspunsul conține mesajul în majuscule
                așteptat = mesaj_test.upper()
                succes = așteptat in răspuns
                
                return RezultatTest(
                    nume="TCP: Transformare majuscule",
                    succes=succes,
                    durată_ms=durată,
                    mesaj=f"Răspuns: {răspuns}" if not succes else ""
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="TCP: Transformare majuscule",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_tcp_mesaje_multiple(self, port: int = 9090) -> RezultatTest:
        """Testează trimiterea de mesaje multiple pe aceeași conexiune."""
        start = time.perf_counter()
        mesaje = ["primul", "al doilea", "al treilea"]
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect((self.host, port))
                
                for mesaj in mesaje:
                    sock.sendall(mesaj.encode())
                    răspuns = sock.recv(1024).decode()
                    if mesaj.upper() not in răspuns:
                        durată = (time.perf_counter() - start) * 1000
                        return RezultatTest(
                            nume="TCP: Mesaje multiple",
                            succes=False,
                            durată_ms=durată,
                            mesaj=f"Răspuns neașteptat pentru '{mesaj}': {răspuns}"
                        )
                
                durată = (time.perf_counter() - start) * 1000
                return RezultatTest(
                    nume="TCP: Mesaje multiple",
                    succes=True,
                    durată_ms=durată
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="TCP: Mesaje multiple",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_tcp_concurență(self, port: int = 9090, nr_clienți: int = 3) -> RezultatTest:
        """Testează gestionarea clienților concurenți."""
        start = time.perf_counter()
        rezultate_clienți = []
        lock = threading.Lock()
        
        def client_thread(id_client: int) -> None:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    sock.settimeout(5)
                    sock.connect((self.host, port))
                    mesaj = f"client{id_client}"
                    sock.sendall(mesaj.encode())
                    răspuns = sock.recv(1024).decode()
                    
                    with lock:
                        rezultate_clienți.append((id_client, mesaj.upper() in răspuns))
            except Exception:
                with lock:
                    rezultate_clienți.append((id_client, False))
        
        # Pornire clienți simultan
        thread_uri = []
        for i in range(nr_clienți):
            t = threading.Thread(target=client_thread, args=(i,))
            thread_uri.append(t)
            t.start()
        
        for t in thread_uri:
            t.join(timeout=10)
        
        durată = (time.perf_counter() - start) * 1000
        reușite = sum(1 for _, succes in rezultate_clienți if succes)
        
        return RezultatTest(
            nume=f"TCP: Concurență ({nr_clienți} clienți)",
            succes=reușite == nr_clienți,
            durată_ms=durată,
            mesaj=f"{reușite}/{nr_clienți} clienți reușiți"
        )
    
    # ========================================================================
    # Teste Exercițiul 2: UDP
    # ========================================================================
    
    def test_udp_ping(self, port: int = 9091) -> RezultatTest:
        """Testează comanda ping UDP."""
        start = time.perf_counter()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(b"ping", (self.host, port))
                răspuns, _ = sock.recvfrom(1024)
                
                durată = (time.perf_counter() - start) * 1000
                succes = răspuns.decode().strip() == "PONG"
                
                return RezultatTest(
                    nume="UDP: Comandă ping",
                    succes=succes,
                    durată_ms=durată,
                    mesaj=f"Răspuns: {răspuns.decode()}" if not succes else ""
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="UDP: Comandă ping",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_udp_upper(self, port: int = 9091) -> RezultatTest:
        """Testează comanda upper UDP."""
        start = time.perf_counter()
        text_test = "test"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(f"upper:{text_test}".encode(), (self.host, port))
                răspuns, _ = sock.recvfrom(1024)
                
                durată = (time.perf_counter() - start) * 1000
                succes = răspuns.decode().strip() == text_test.upper()
                
                return RezultatTest(
                    nume="UDP: Comandă upper",
                    succes=succes,
                    durată_ms=durată,
                    mesaj=f"Răspuns: {răspuns.decode()}" if not succes else ""
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="UDP: Comandă upper",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_udp_reverse(self, port: int = 9091) -> RezultatTest:
        """Testează comanda reverse UDP."""
        start = time.perf_counter()
        text_test = "abcdef"
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(f"reverse:{text_test}".encode(), (self.host, port))
                răspuns, _ = sock.recvfrom(1024)
                
                durată = (time.perf_counter() - start) * 1000
                succes = răspuns.decode().strip() == text_test[::-1]
                
                return RezultatTest(
                    nume="UDP: Comandă reverse",
                    succes=succes,
                    durată_ms=durată,
                    mesaj=f"Răspuns: {răspuns.decode()}" if not succes else ""
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="UDP: Comandă reverse",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_udp_time(self, port: int = 9091) -> RezultatTest:
        """Testează comanda time UDP."""
        start = time.perf_counter()
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                sock.sendto(b"time", (self.host, port))
                răspuns, _ = sock.recvfrom(1024)
                
                durată = (time.perf_counter() - start) * 1000
                
                # Verificăm că răspunsul arată ca o dată/oră
                răspuns_text = răspuns.decode().strip()
                succes = "-" in răspuns_text and ":" in răspuns_text
                
                return RezultatTest(
                    nume="UDP: Comandă time",
                    succes=succes,
                    durată_ms=durată,
                    mesaj=f"Răspuns: {răspuns_text}" if not succes else ""
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="UDP: Comandă time",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    def test_udp_comenzi_multiple(self, port: int = 9091) -> RezultatTest:
        """Testează mai multe comenzi UDP în secvență."""
        start = time.perf_counter()
        
        comenzi = [
            ("ping", "PONG"),
            ("upper:abc", "ABC"),
            ("lower:XYZ", "xyz"),
        ]
        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(2)
                
                for comandă, așteptat in comenzi:
                    sock.sendto(comandă.encode(), (self.host, port))
                    răspuns, _ = sock.recvfrom(1024)
                    
                    if răspuns.decode().strip() != așteptat:
                        durată = (time.perf_counter() - start) * 1000
                        return RezultatTest(
                            nume="UDP: Comenzi multiple",
                            succes=False,
                            durată_ms=durată,
                            mesaj=f"'{comandă}' → '{răspuns.decode()}' (așteptat: '{așteptat}')"
                        )
                
                durată = (time.perf_counter() - start) * 1000
                return RezultatTest(
                    nume="UDP: Comenzi multiple",
                    succes=True,
                    durată_ms=durată
                )
        except Exception as e:
            durată = (time.perf_counter() - start) * 1000
            return RezultatTest(
                nume="UDP: Comenzi multiple",
                succes=False,
                durată_ms=durată,
                mesaj=str(e)
            )
    
    # ========================================================================
    # Orchestrare teste
    # ========================================================================
    
    def rulează_teste_exercițiu1(self, port: int = 9090) -> None:
        """Rulează toate testele pentru Exercițiul 1 (TCP)."""
        print()
        print("=" * 60)
        print("Teste Exercițiul 1: Server TCP Concurent")
        print("=" * 60)
        print()
        
        self.adaugă_rezultat(self.test_tcp_conexiune(port))
        self.adaugă_rezultat(self.test_tcp_echo(port))
        self.adaugă_rezultat(self.test_tcp_mesaje_multiple(port))
        self.adaugă_rezultat(self.test_tcp_concurență(port))
    
    def rulează_teste_exercițiu2(self, port: int = 9091) -> None:
        """Rulează toate testele pentru Exercițiul 2 (UDP)."""
        print()
        print("=" * 60)
        print("Teste Exercițiul 2: Server UDP cu Protocol")
        print("=" * 60)
        print()
        
        self.adaugă_rezultat(self.test_udp_ping(port))
        self.adaugă_rezultat(self.test_udp_upper(port))
        self.adaugă_rezultat(self.test_udp_reverse(port))
        self.adaugă_rezultat(self.test_udp_time(port))
        self.adaugă_rezultat(self.test_udp_comenzi_multiple(port))
    
    def afișează_sumar(self) -> int:
        """
        Afișează sumarul testelor.
        
        Returns:
            0 dacă toate au trecut, 1 altfel
        """
        print()
        print("=" * 60)
        print("Sumar Teste")
        print("=" * 60)
        
        total = len(self.rezultate)
        reușite = sum(1 for r in self.rezultate if r.succes)
        eșuate = total - reușite
        
        if self.rezultate:
            durată_medie = sum(r.durată_ms for r in self.rezultate) / total
            print(f"Total: {total} teste")
            print(f"Reușite: {reușite}")
            print(f"Eșuate: {eșuate}")
            print(f"Durată medie: {durată_medie:.1f}ms")
        
        print()
        
        if eșuate == 0:
            print("✓ Toate testele au trecut!")
            return 0
        else:
            print(f"✗ {eșuate} teste au eșuat.")
            return 1


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Teste pentru Exerciții - Săptămâna 2"
    )
    parser.add_argument(
        "--exercise", "-e",
        type=int,
        choices=[1, 2],
        help="Numărul exercițiului de testat (1=TCP, 2=UDP)"
    )
    parser.add_argument(
        "--host", "-H",
        default="localhost",
        help="Adresa serverelor (implicit: localhost)"
    )
    parser.add_argument(
        "--tcp-port",
        type=int,
        default=9090,
        help="Portul serverului TCP (implicit: 9090)"
    )
    parser.add_argument(
        "--udp-port",
        type=int,
        default=9091,
        help="Portul serverului UDP (implicit: 9091)"
    )
    
    args = parser.parse_args()
    
    tester = TesterExerciții(host=args.host)
    
    if args.exercise == 1:
        tester.rulează_teste_exercițiu1(args.tcp_port)
    elif args.exercise == 2:
        tester.rulează_teste_exercițiu2(args.udp_port)
    else:
        # Rulează toate testele
        tester.rulează_teste_exercițiu1(args.tcp_port)
        tester.rulează_teste_exercițiu2(args.udp_port)
    
    return tester.afișează_sumar()


if __name__ == "__main__":
    sys.exit(main())
