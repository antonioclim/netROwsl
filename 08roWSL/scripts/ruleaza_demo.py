#!/usr/bin/env python3
"""
Executor Demonstrații
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Rulează demonstrații interactive pentru conceptele de laborator.

Utilizare:
    python scripts/ruleaza_demo.py --demo docker-nginx
    python scripts/ruleaza_demo.py --demo echilibrare
    python scripts/ruleaza_demo.py --lista
"""

import argparse
import sys
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

# Coduri culori
VERDE = "\033[92m"
ROSU = "\033[91m"
GALBEN = "\033[93m"
ALBASTRU = "\033[94m"
CYAN = "\033[96m"
RESETARE = "\033[0m"
BOLD = "\033[1m"


DEMONSTRATII = {
    "docker-nginx": {
        "nume": "Proxy nginx cu Docker",
        "descriere": "Demonstrează echilibrarea round-robin cu nginx"
    },
    "echilibrare": {
        "nume": "Algoritmi de Echilibrare",
        "descriere": "Compară diferiți algoritmi de echilibrare a încărcării"
    },
    "handshake": {
        "nume": "Handshake TCP",
        "descriere": "Explică stabilirea conexiunii TCP în trei pași"
    },
    "antete": {
        "nume": "Antete HTTP",
        "descriere": "Afișează antetele HTTP din răspunsuri"
    }
}


def afiseaza_titlu(titlu: str):
    """Afișează un titlu formatat."""
    print()
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print(f"{BOLD}{titlu}{RESETARE}")
    print(f"{CYAN}{'=' * 60}{RESETARE}")
    print()


def demo_docker_nginx():
    """Demonstrație nginx cu echilibrare round-robin."""
    afiseaza_titlu("Demo: Proxy nginx cu Echilibrare Round-Robin")
    
    print("Această demonstrație arată cum nginx distribuie cererile")
    print("între cele 3 backend-uri folosind algoritmul round-robin.")
    print()
    
    print(f"{ALBASTRU}Trimit 6 cereri către http://localhost:8080/{RESETARE}")
    print("-" * 50)
    
    rezultate = []
    
    for i in range(6):
        try:
            with urlopen("http://localhost:8080/", timeout=5) as response:
                backend_id = response.headers.get('X-Backend-ID', '?')
                backend_name = response.headers.get('X-Backend-Name', '?')
                
                rezultate.append({
                    'id': backend_id,
                    'nume': backend_name
                })
                
                print(f"  Cererea {i+1}: Backend {backend_id} ({backend_name})")
                time.sleep(0.3)
                
        except URLError as e:
            print(f"  {ROSU}Cererea {i+1}: Eroare - {e}{RESETARE}")
    
    print()
    print(f"{VERDE}Rezultate:{RESETARE}")
    
    # Numără distribuția
    distributie = {}
    for r in rezultate:
        cheie = f"Backend {r['id']} ({r['nume']})"
        distributie[cheie] = distributie.get(cheie, 0) + 1
    
    for backend, numar in sorted(distributie.items()):
        bara = "█" * numar
        print(f"  {backend}: {bara} ({numar} cereri)")
    
    print()
    print(f"{CYAN}Observație:{RESETARE} Round-robin distribuie cererile secvențial 1→2→3→1→2→3")


def demo_echilibrare():
    """Demonstrație algoritmi de echilibrare."""
    afiseaza_titlu("Demo: Algoritmi de Echilibrare a Încărcării")
    
    algoritmi = [
        ("Round-Robin", "/", "Distribuție egală, ciclic"),
        ("Weighted", "/weighted/", "Proporțional cu ponderile (5:3:1)"),
        ("Least-Conn", "/least-conn/", "Către serverul cu cele mai puține conexiuni"),
        ("IP-Hash", "/sticky/", "Același client → același server")
    ]
    
    for nume, cale, descriere in algoritmi:
        print(f"{BOLD}{nume}{RESETARE}: {descriere}")
        print(f"  Cale: http://localhost:8080{cale}")
        
        try:
            rezultate = []
            for _ in range(6):
                url = f"http://localhost:8080{cale}"
                with urlopen(url, timeout=5) as response:
                    backend_id = response.headers.get('X-Backend-ID', '?')
                    rezultate.append(backend_id)
            
            print(f"  Distribuție (6 cereri): {' → '.join(rezultate)}")
        except Exception as e:
            print(f"  {GALBEN}Nu este disponibil: {e}{RESETARE}")
        
        print()


def demo_handshake():
    """Demonstrație handshake TCP."""
    afiseaza_titlu("Demo: Handshake TCP (Three-Way Handshake)")
    
    print("""
Stabilirea unei conexiuni TCP urmează trei pași:

    Client                                Server
       │                                     │
       │  ─────── SYN (seq=x) ─────────►    │
       │          Cerere conectare           │
       │                                     │
       │  ◄─── SYN-ACK (seq=y, ack=x+1) ─── │
       │       Confirmare + Propunere        │
       │                                     │
       │  ─────── ACK (ack=y+1) ────────►   │
       │          Confirmare finală          │
       │                                     │
       │  ═══════ CONEXIUNE ACTIVĂ ════════ │
       │                                     │

Fiecare pas are un rol specific:

1. {BOLD}SYN{RESETARE} (Synchronize)
   - Clientul inițiază conexiunea
   - Trimite numărul de secvență inițial (ISN)
   - Flags: SYN=1

2. {BOLD}SYN-ACK{RESETARE} (Synchronize-Acknowledge)  
   - Serverul confirmă recepția SYN
   - Trimite propriul număr de secvență
   - Flags: SYN=1, ACK=1

3. {BOLD}ACK{RESETARE} (Acknowledge)
   - Clientul confirmă recepția SYN-ACK
   - Conexiunea este stabilită
   - Flags: ACK=1

Pentru a observa acest proces în Wireshark:
  Filtru: tcp.flags.syn == 1

""".format(BOLD=BOLD, RESETARE=RESETARE))


def demo_antete():
    """Demonstrație antete HTTP."""
    afiseaza_titlu("Demo: Antete HTTP din Răspunsuri")
    
    print("Trimit o cerere și afișez toate antetele răspunsului:")
    print()
    
    try:
        cerere = Request("http://localhost:8080/")
        cerere.add_header("User-Agent", "Demo-Laborator/1.0")
        
        with urlopen(cerere, timeout=5) as response:
            print(f"{VERDE}Cod stare: {response.status} {response.reason}{RESETARE}")
            print()
            print(f"{ALBASTRU}Antete răspuns:{RESETARE}")
            
            for antet, valoare in response.headers.items():
                # Evidențiază antetele custom
                if antet.startswith('X-'):
                    print(f"  {GALBEN}{antet}{RESETARE}: {valoare}")
                else:
                    print(f"  {antet}: {valoare}")
                    
    except URLError as e:
        print(f"{ROSU}Eroare: {e}{RESETARE}")
        print("Asigurați-vă că laboratorul rulează.")


def listeaza_demonstratii():
    """Listează toate demonstrațiile disponibile."""
    afiseaza_titlu("Demonstrații Disponibile")
    
    for cheie, info in DEMONSTRATII.items():
        print(f"  {BOLD}{cheie}{RESETARE}")
        print(f"    {info['nume']}")
        print(f"    {info['descriere']}")
        print()
    
    print(f"Utilizare: python scripts/ruleaza_demo.py --demo <nume>")


def main():
    """Punctul principal de intrare."""
    parser = argparse.ArgumentParser(
        description="Executor Demonstrații - Laborator Săptămâna 8",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMONSTRATII.keys()),
        help="Demonstrația de rulat"
    )
    parser.add_argument(
        "--lista", "-l",
        action="store_true",
        help="Listează toate demonstrațiile disponibile"
    )
    
    args = parser.parse_args()
    
    if args.lista:
        listeaza_demonstratii()
        return 0
    
    if not args.demo:
        listeaza_demonstratii()
        return 0
    
    # Rulează demonstrația selectată
    if args.demo == "docker-nginx":
        demo_docker_nginx()
    elif args.demo == "echilibrare":
        demo_echilibrare()
    elif args.demo == "handshake":
        demo_handshake()
    elif args.demo == "antete":
        demo_antete()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
