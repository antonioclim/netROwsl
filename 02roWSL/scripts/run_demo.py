#!/usr/bin/env python3
"""
Script de Demonstrație Automată - Săptămâna 2
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Demonstrații automate pentru prezentări la curs/laborator.
"""

import subprocess
import sys
import time
import argparse
import socket
import threading
from pathlib import Path
from typing import List, Tuple
from dataclasses import dataclass

# Adăugare rădăcină proiect la cale
RĂDĂCINĂ_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RĂDĂCINĂ_PROIECT))

from scripts.utils.logger import configurează_logger

logger = configurează_logger("demonstrație")


@dataclass
class RezultatTest:
    """Rezultatul unui test individual."""
    nume: str
    succes: bool
    durată_ms: float
    răspuns: str = ""
    eroare: str = ""


def afișează_antet(titlu: str) -> None:
    """Afișează un antet formatat pentru demonstrație."""
    print()
    print("╔" + "═" * 58 + "╗")
    print(f"║ {titlu:^56} ║")
    print("╚" + "═" * 58 + "╝")
    print()


def afișează_secțiune(titlu: str) -> None:
    """Afișează o secțiune în cadrul demonstrației."""
    print()
    print(f"┌─ {titlu} " + "─" * (55 - len(titlu)))
    print("│")


def afișează_rezultat(rezultat: RezultatTest) -> None:
    """Afișează rezultatul unui test."""
    simbol = "✓" if rezultat.succes else "✗"
    culoare_start = "\033[92m" if rezultat.succes else "\033[91m"
    culoare_sfârșit = "\033[0m"
    
    print(f"│  {culoare_start}{simbol}{culoare_sfârșit} {rezultat.nume}")
    print(f"│    Durată: {rezultat.durată_ms:.2f} ms")
    
    if rezultat.răspuns:
        print(f"│    Răspuns: {rezultat.răspuns[:50]}")
    if rezultat.eroare:
        print(f"│    Eroare: {rezultat.eroare}")


def test_tcp(host: str, port: int, mesaj: str, timeout: float = 5.0) -> RezultatTest:
    """
    Testează comunicarea TCP.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
        
    Returns:
        RezultatTest cu rezultatele testului
    """
    try:
        start = time.perf_counter()
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            sock.sendall(mesaj.encode())
            răspuns = sock.recv(1024).decode()
        
        durată = (time.perf_counter() - start) * 1000
        
        return RezultatTest(
            nume=f"TCP: '{mesaj}'",
            succes=True,
            durată_ms=durată,
            răspuns=răspuns.strip()
        )
    except Exception as e:
        return RezultatTest(
            nume=f"TCP: '{mesaj}'",
            succes=False,
            durată_ms=0,
            eroare=str(e)
        )


def test_udp(host: str, port: int, mesaj: str, timeout: float = 2.0) -> RezultatTest:
    """
    Testează comunicarea UDP.
    
    Args:
        host: Adresa serverului
        port: Portul serverului
        mesaj: Mesajul de trimis
        timeout: Timeout în secunde
        
    Returns:
        RezultatTest cu rezultatele testului
    """
    try:
        start = time.perf_counter()
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(timeout)
            sock.sendto(mesaj.encode(), (host, port))
            răspuns, _ = sock.recvfrom(1024)
        
        durată = (time.perf_counter() - start) * 1000
        
        return RezultatTest(
            nume=f"UDP: '{mesaj}'",
            succes=True,
            durată_ms=durată,
            răspuns=răspuns.decode().strip()
        )
    except socket.timeout:
        return RezultatTest(
            nume=f"UDP: '{mesaj}'",
            succes=False,
            durată_ms=0,
            eroare="Timeout - fără răspuns"
        )
    except Exception as e:
        return RezultatTest(
            nume=f"UDP: '{mesaj}'",
            succes=False,
            durată_ms=0,
            eroare=str(e)
        )


def demo_comparație_tcp_udp() -> None:
    """
    Demo 1: Comparație între TCP și UDP.
    
    Evidențiază diferențele de comportament între cele două protocoale.
    """
    afișează_antet("Demo 1: Comparație TCP vs UDP")
    
    host = "localhost"
    port_tcp = 9090
    port_udp = 9091
    
    print("Această demonstrație compară comportamentul TCP și UDP:")
    print("• TCP: Orientat pe conexiune, fiabil, cu confirmare")
    print("• UDP: Fără conexiune, best-effort, fără confirmare")
    print()
    
    # Verificare disponibilitate servere
    afișează_secțiune("Verificare Servere")
    
    tcp_disponibil = False
    udp_disponibil = False
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port_tcp))
            tcp_disponibil = True
            print(f"│  ✓ Server TCP pe portul {port_tcp}: ACTIV")
    except Exception:
        print(f"│  ✗ Server TCP pe portul {port_tcp}: INACTIV")
        print("│    Porniți: docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server")
    
    try:
        rezultat = test_udp(host, port_udp, "ping", timeout=1)
        if rezultat.succes:
            udp_disponibil = True
            print(f"│  ✓ Server UDP pe portul {port_udp}: ACTIV")
    except Exception:
        pass
    
    if not udp_disponibil:
        print(f"│  ✗ Server UDP pe portul {port_udp}: INACTIV")
        print("│    Porniți: docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py server")
    
    if not tcp_disponibil and not udp_disponibil:
        print("│")
        print("│  ⚠ Niciun server nu este activ. Demonstrația nu poate continua.")
        print("└" + "─" * 57)
        return
    
    # Test TCP (dacă disponibil)
    if tcp_disponibil:
        afișează_secțiune("Teste TCP")
        
        mesaje_tcp = ["salut", "rețele de calculatoare", "test123"]
        rezultate_tcp = []
        
        for mesaj in mesaje_tcp:
            rezultat = test_tcp(host, port_tcp, mesaj)
            rezultate_tcp.append(rezultat)
            afișează_rezultat(rezultat)
            time.sleep(0.3)  # Pauză pentru vizibilitate
        
        # Statistici TCP
        durate_tcp = [r.durată_ms for r in rezultate_tcp if r.succes]
        if durate_tcp:
            print("│")
            print(f"│  📊 Statistici TCP:")
            print(f"│     Media RTT: {sum(durate_tcp)/len(durate_tcp):.2f} ms")
            print(f"│     Min: {min(durate_tcp):.2f} ms, Max: {max(durate_tcp):.2f} ms")
    
    # Test UDP (dacă disponibil)
    if udp_disponibil:
        afișează_secțiune("Teste UDP")
        
        comenzi_udp = ["ping", "upper:test", "time", "reverse:demo"]
        rezultate_udp = []
        
        for comandă in comenzi_udp:
            rezultat = test_udp(host, port_udp, comandă)
            rezultate_udp.append(rezultat)
            afișează_rezultat(rezultat)
            time.sleep(0.3)
        
        # Statistici UDP
        durate_udp = [r.durată_ms for r in rezultate_udp if r.succes]
        if durate_udp:
            print("│")
            print(f"│  📊 Statistici UDP:")
            print(f"│     Media RTT: {sum(durate_udp)/len(durate_udp):.2f} ms")
            print(f"│     Min: {min(durate_udp):.2f} ms, Max: {max(durate_udp):.2f} ms")
    
    # Comparație finală
    afișează_secțiune("Concluzii")
    print("│  TCP:")
    print("│    • Stabilește conexiune (3-way handshake)")
    print("│    • Garantează livrarea și ordinea")
    print("│    • Overhead mai mare, latență inițială")
    print("│")
    print("│  UDP:")
    print("│    • Trimite direct, fără conexiune")
    print("│    • Nu garantează livrarea")
    print("│    • Overhead minim, răspuns rapid")
    print("└" + "─" * 57)


def demo_concurență_tcp() -> None:
    """
    Demo 2: Gestionarea clienților concurenți.
    
    Demonstrează cum un server threaded gestionează conexiuni multiple.
    """
    afișează_antet("Demo 2: Clienți TCP Concurenți")
    
    host = "localhost"
    port = 9090
    
    print("Această demonstrație arată cum serverul gestionează")
    print("mai mulți clienți simultan folosind thread-uri.")
    print()
    
    # Verificare server
    afișează_secțiune("Verificare Server TCP")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((host, port))
            print(f"│  ✓ Server TCP activ pe portul {port}")
    except Exception:
        print(f"│  ✗ Server TCP inactiv pe portul {port}")
        print("│")
        print("│  Porniți serverul în modul threaded:")
        print("│  docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --mode threaded")
        print("└" + "─" * 57)
        return
    
    # Simulare clienți concurenți
    afișează_secțiune("Lansare Clienți Concurenți")
    
    nr_clienți = 5
    rezultate: List[RezultatTest] = []
    lock = threading.Lock()
    
    def client_thread(id_client: int) -> None:
        """Thread pentru un client individual."""
        mesaj = f"Mesaj de la clientul {id_client}"
        rezultat = test_tcp(host, port, mesaj)
        rezultat.nume = f"Client #{id_client}"
        
        with lock:
            rezultate.append(rezultat)
            afișează_rezultat(rezultat)
    
    print(f"│  Lansare {nr_clienți} clienți simultan...")
    print("│")
    
    # Pornire thread-uri
    thread_uri = []
    start_total = time.perf_counter()
    
    for i in range(nr_clienți):
        t = threading.Thread(target=client_thread, args=(i + 1,))
        thread_uri.append(t)
        t.start()
    
    # Așteptare finalizare
    for t in thread_uri:
        t.join()
    
    durată_totală = (time.perf_counter() - start_total) * 1000
    
    # Statistici
    afișează_secțiune("Statistici Finale")
    
    reușite = sum(1 for r in rezultate if r.succes)
    durate = [r.durată_ms for r in rezultate if r.succes]
    
    print(f"│  Clienți: {nr_clienți}")
    print(f"│  Reușite: {reușite}/{nr_clienți}")
    print(f"│  Durată totală: {durată_totală:.2f} ms")
    
    if durate:
        durată_cumulată = sum(durate)
        print(f"│  Durată cumulată (secvențial ar fi fost): {durată_cumulată:.2f} ms")
        print(f"│  Factor de paralelizare: {durată_cumulată/durată_totală:.2f}x")
    
    print("│")
    print("│  💡 Observați că timpul total este mult mai mic decât")
    print("│     suma timpilor individuali - aceasta este puterea")
    print("│     procesării concurente!")
    print("└" + "─" * 57)


def listează_demonstrații() -> None:
    """Afișează lista demonstrațiilor disponibile."""
    print()
    print("Demonstrații disponibile:")
    print()
    print("  1. Comparație TCP vs UDP")
    print("     Evidențiază diferențele comportamentale dintre cele două protocoale")
    print()
    print("  2. Clienți TCP Concurenți")
    print("     Demonstrează gestionarea conexiunilor multiple cu thread-uri")
    print()
    print("Utilizare: python run_demo.py --demo <număr>")
    print()


def main() -> int:
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Demonstrații Automate - Săptămâna 2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  python run_demo.py --list       # Listează demonstrațiile disponibile
  python run_demo.py --demo 1     # Rulează demo-ul 1 (TCP vs UDP)
  python run_demo.py --demo 2     # Rulează demo-ul 2 (concurență)
  python run_demo.py --all        # Rulează toate demonstrațiile
        """
    )
    parser.add_argument(
        "--demo", "-d",
        type=int,
        choices=[1, 2],
        help="Numărul demonstrației de rulat (1 sau 2)"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="Listează demonstrațiile disponibile"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        help="Rulează toate demonstrațiile"
    )
    
    args = parser.parse_args()

    if args.list:
        listează_demonstrații()
        return 0
    
    if args.all:
        demo_comparație_tcp_udp()
        input("\nApăsați Enter pentru demonstrația următoare...")
        demo_concurență_tcp()
        return 0
    
    if args.demo == 1:
        demo_comparație_tcp_udp()
        return 0
    elif args.demo == 2:
        demo_concurență_tcp()
        return 0
    else:
        listează_demonstrații()
        return 0


if __name__ == "__main__":
    sys.exit(main())
