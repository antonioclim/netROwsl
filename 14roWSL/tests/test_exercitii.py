#!/usr/bin/env python3
"""
Verificare Exerciții Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest script verifică implementarea corectă a exercițiilor de laborator.
"""

import sys
import socket
import argparse
from pathlib import Path
from typing import List, Tuple, Dict, Any

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Coduri de culoare
class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

def afiseaza_trecut(mesaj: str) -> None:
    print(f"  {Culori.VERDE}[TRECUT]{Culori.FINAL} {mesaj}")

def afiseaza_esuat(mesaj: str) -> None:
    print(f"  {Culori.ROSU}[EȘUAT]{Culori.FINAL} {mesaj}")

def afiseaza_info(mesaj: str) -> None:
    print(f"  {Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")

class RezultatTest:
    """Rezultatul unui test."""
    def __init__(self, nume: str, trecut: bool, mesaj: str = ""):
        self.nume = nume
        self.trecut = trecut
        self.mesaj = mesaj

def test_exercitiu_1() -> List[RezultatTest]:
    """
    Exercițiul 1: Verificarea Mediului
    Testează accesibilitatea serviciilor.
    """
    rezultate = []
    
    # Test: Load balancer accesibil
    try:
        import requests
        raspuns = requests.get("http://localhost:8080/", timeout=5)
        trecut = raspuns.status_code == 200
        rezultate.append(RezultatTest(
            "Load balancer accesibil",
            trecut,
            f"Status: {raspuns.status_code}"
        ))
    except Exception as e:
        rezultate.append(RezultatTest("Load balancer accesibil", False, str(e)))
    
    # Test: Backend app1 accesibil
    try:
        raspuns = requests.get("http://localhost:8001/", timeout=5)
        trecut = raspuns.status_code == 200
        rezultate.append(RezultatTest(
            "Backend app1 accesibil",
            trecut
        ))
    except Exception as e:
        rezultate.append(RezultatTest("Backend app1 accesibil", False, str(e)))
    
    # Test: Backend app2 accesibil
    try:
        raspuns = requests.get("http://localhost:8002/", timeout=5)
        trecut = raspuns.status_code == 200
        rezultate.append(RezultatTest(
            "Backend app2 accesibil",
            trecut
        ))
    except Exception as e:
        rezultate.append(RezultatTest("Backend app2 accesibil", False, str(e)))
    
    # Test: Endpoint status LB returnează JSON valid
    try:
        raspuns = requests.get("http://localhost:8080/status", timeout=5)
        date = raspuns.json()
        trecut = "status" in date or "backends" in date
        rezultate.append(RezultatTest(
            "Endpoint status LB returnează JSON valid",
            trecut
        ))
    except Exception as e:
        rezultate.append(RezultatTest(
            "Endpoint status LB returnează JSON valid", False, str(e)
        ))
    
    return rezultate

def test_exercitiu_2() -> List[RezultatTest]:
    """
    Exercițiul 2: Analiza Comportamentului Load Balancer-ului
    Testează distribuția round-robin.
    """
    rezultate = []
    
    try:
        import requests
        
        afiseaza_info("Se trimit 10 cereri HTTP către load balancer...")
        
        backend_uri = {"app1": 0, "app2": 0}
        raspunsuri = []
        
        for _ in range(10):
            raspuns = requests.get("http://localhost:8080/", timeout=5)
            corp = raspuns.text.lower()
            
            if "app1" in corp:
                backend_uri["app1"] += 1
                raspunsuri.append("app1")
            elif "app2" in corp:
                backend_uri["app2"] += 1
                raspunsuri.append("app2")
        
        # Test: Ambele backend-uri au primit cereri
        ambele_folosite = backend_uri["app1"] > 0 and backend_uri["app2"] > 0
        rezultate.append(RezultatTest(
            "Ambele backend-uri au primit cereri",
            ambele_folosite,
            f"app1={backend_uri['app1']}, app2={backend_uri['app2']}"
        ))
        
        # Test: Distribuție aproximativ egală
        distributie_ok = abs(backend_uri["app1"] - backend_uri["app2"]) <= 4
        rezultate.append(RezultatTest(
            f"Distribuție: app1={backend_uri['app1']}, app2={backend_uri['app2']}",
            distributie_ok
        ))
        
        # Test: Detectare pattern round-robin
        alternari = 0
        for i in range(1, len(raspunsuri)):
            if raspunsuri[i] != raspunsuri[i-1]:
                alternari += 1
        
        pattern_rr = alternari >= 5  # Cel puțin 5 alternări din 9 posibile
        rezultate.append(RezultatTest(
            "Pattern round-robin detectat",
            pattern_rr,
            f"{alternari} alternări"
        ))
        
    except Exception as e:
        rezultate.append(RezultatTest("Eroare la testare", False, str(e)))
    
    return rezultate

def test_exercitiu_3() -> List[RezultatTest]:
    """
    Exercițiul 3: Testarea Serviciului Echo TCP
    Testează funcționalitatea serverului echo.
    """
    rezultate = []
    
    mesaje_test = [
        "Salut",
        "Test123Rețele",
        "",
        "A" * 50  # Mesaj lung
    ]
    
    afiseaza_info("Se testează serverul echo cu 4 mesaje...")
    
    for mesaj in mesaje_test:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(('localhost', 9090))
            
            sock.sendall(f"{mesaj}\n".encode())
            raspuns = sock.recv(1024).decode().strip()
            sock.close()
            
            # Verifică că răspunsul conține mesajul original
            if mesaj:
                trecut = mesaj in raspuns
                rezultate.append(RezultatTest(
                    f'"{mesaj[:20]}..." ecou corect',
                    trecut,
                    raspuns[:50]
                ))
            else:
                # Mesaj gol - doar verifică că primim răspuns
                rezultate.append(RezultatTest(
                    "Mesaj gol gestionat",
                    True
                ))
                
        except Exception as e:
            rezultate.append(RezultatTest(
                f'"{mesaj[:20]}..." ecou',
                False,
                str(e)
            ))
    
    return rezultate

def test_exercitiu_4() -> List[RezultatTest]:
    """
    Exercițiul 4: Captură și Analiză de Pachete
    Verifică prezența fișierelor PCAP.
    """
    rezultate = []
    
    director_pcap = RADACINA_PROIECT / "pcap"
    
    afiseaza_info("Se verifică directorul pcap/...")
    
    if not director_pcap.exists():
        rezultate.append(RezultatTest(
            "Directorul pcap/ există",
            False
        ))
        return rezultate
    
    fisiere_pcap = list(director_pcap.glob("*.pcap"))
    
    if fisiere_pcap:
        rezultate.append(RezultatTest(
            "Fișiere PCAP găsite",
            True,
            f"Fișiere: {', '.join(f.name for f in fisiere_pcap[:3])}"
        ))
    else:
        rezultate.append(RezultatTest(
            "Fișiere PCAP găsite",
            False,
            "Rulați: python scripts/captura_trafic.py --durata 30"
        ))
    
    return rezultate

def ruleaza_teste(numar_exercitiu: int = None) -> Tuple[int, int]:
    """
    Rulează testele pentru exercițiile specificate.
    
    Returnează:
        Tuplu (trecut, total)
    """
    exercitii = {
        1: ("Verificarea Mediului", test_exercitiu_1),
        2: ("Analiza Comportamentului Load Balancer-ului", test_exercitiu_2),
        3: ("Testarea Serviciului Echo TCP", test_exercitiu_3),
        4: ("Captură și Analiză de Pachete", test_exercitiu_4),
    }
    
    total_trecut = 0
    total_teste = 0
    
    for nr, (titlu, functie_test) in exercitii.items():
        if numar_exercitiu and nr != numar_exercitiu:
            continue
        
        print()
        print(f"{Culori.BOLD}Exercițiul {nr}: {titlu}{Culori.FINAL}")
        print("=" * 50)
        
        rezultate = functie_test()
        
        for rez in rezultate:
            if rez.trecut:
                afiseaza_trecut(rez.nume)
                total_trecut += 1
            else:
                afiseaza_esuat(f"{rez.nume}: {rez.mesaj}")
            total_teste += 1
        
        ex_trecut = sum(1 for r in rezultate if r.trecut)
        print(f"\nRezultate: {ex_trecut}/{len(rezultate)} teste trecute")
    
    return total_trecut, total_teste

def main() -> int:
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description="Verificare Exerciții Laborator Săptămâna 14",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2, 3, 4],
        help="Rulează doar exercițiul specificat (1-4)"
    )
    parser.add_argument(
        "--toate", "-t",
        action="store_true",
        help="Rulează toate exercițiile"
    )
    
    args = parser.parse_args()
    
    print()
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Verificare Exerciții Laborator Săptămâna 14{Culori.FINAL}")
    print(f"{Culori.CYAN}Laborator Rețele de Calculatoare - ASE{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    try:
        import requests
    except ImportError:
        print(f"\n{Culori.ROSU}Eroare: Pachetul 'requests' nu este instalat.{Culori.FINAL}")
        print("Rulați: pip install requests")
        return 1
    
    if args.exercitiu:
        trecut, total = ruleaza_teste(args.exercitiu)
    else:
        trecut, total = ruleaza_teste()
    
    print()
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}Sumar Final{Culori.FINAL}")
    print(f"Teste trecute: {trecut}/{total}")
    
    if trecut == total:
        print(f"{Culori.VERDE}✓ Toate testele au trecut!{Culori.FINAL}")
    else:
        print(f"{Culori.GALBEN}! Unele teste au eșuat.{Culori.FINAL}")
    
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    
    return 0 if trecut == total else 1

if __name__ == "__main__":
    sys.exit(main())
