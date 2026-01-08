#!/usr/bin/env python3
"""
Demonstrații Laborator Săptămâna 14
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Rulează demonstrații pentru prezentarea funcționalităților laboratorului.
"""

import subprocess
import sys
import socket
import json
import time
import argparse
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("Eroare: Pachetul 'requests' nu este instalat.")
    print("Rulați: pip install requests")
    sys.exit(1)

RADACINA_PROIECT = Path(__file__).parent.parent

class Culori:
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    FINAL = '\033[0m'

def afiseaza_info(mesaj): print(f"{Culori.CYAN}[INFO]{Culori.FINAL} {mesaj}")
def afiseaza_succes(mesaj): print(f"{Culori.VERDE}[OK]{Culori.FINAL} {mesaj}")
def afiseaza_eroare(mesaj): print(f"{Culori.ROSU}[EROARE]{Culori.FINAL} {mesaj}")

def demo_complet():
    """Demonstrație completă a sistemului."""
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}DEMONSTRAȚIE COMPLETĂ A SISTEMULUI{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    raport = {
        "timestamp": datetime.now().isoformat(),
        "rezultate": {}
    }
    
    # Partea 1: Verificare servicii
    print(f"\n{Culori.BOLD}Partea 1: Verificare Servicii{Culori.FINAL}")
    print("-" * 40)
    
    servicii = [
        ("Load Balancer", "http://localhost:8080/"),
        ("Backend App 1", "http://localhost:8001/"),
        ("Backend App 2", "http://localhost:8002/"),
    ]
    
    for nume, url in servicii:
        try:
            raspuns = requests.get(url, timeout=5)
            if raspuns.status_code == 200:
                afiseaza_succes(f"{nume}: OK ({raspuns.status_code})")
            else:
                afiseaza_eroare(f"{nume}: {raspuns.status_code}")
        except Exception as e:
            afiseaza_eroare(f"{nume}: {e}")
    
    # Partea 2: Test Round-Robin
    print(f"\n{Culori.BOLD}Partea 2: Test Distribuție Round-Robin{Culori.FINAL}")
    print("-" * 40)
    
    backend_uri = {"app1": 0, "app2": 0}
    
    afiseaza_info("Se trimit 20 cereri HTTP...")
    for i in range(20):
        try:
            raspuns = requests.get("http://localhost:8080/", timeout=5)
            corp = raspuns.text.lower()
            
            if "app1" in corp:
                backend_uri["app1"] += 1
                print(f"  Cerere {i+1:2d}: {Culori.CYAN}app1{Culori.FINAL}")
            elif "app2" in corp:
                backend_uri["app2"] += 1
                print(f"  Cerere {i+1:2d}: {Culori.GALBEN}app2{Culori.FINAL}")
        except Exception as e:
            print(f"  Cerere {i+1:2d}: {Culori.ROSU}eroare{Culori.FINAL}")
    
    print(f"\n  Sumar: app1={backend_uri['app1']}, app2={backend_uri['app2']}")
    raport["rezultate"]["round_robin"] = backend_uri
    
    # Partea 3: Test Server Echo
    print(f"\n{Culori.BOLD}Partea 3: Test Server Echo TCP{Culori.FINAL}")
    print("-" * 40)
    
    mesaje_test = ["Salut Lume", "Test123", "Laborator Rețele"]
    
    for mesaj in mesaje_test:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(('localhost', 9090))
            sock.sendall(f"{mesaj}\n".encode())
            raspuns = sock.recv(1024).decode().strip()
            sock.close()
            
            if mesaj in raspuns:
                afiseaza_succes(f'"{mesaj}" → "{raspuns[:40]}"')
            else:
                afiseaza_eroare(f'"{mesaj}" → răspuns neașteptat')
        except Exception as e:
            afiseaza_eroare(f'"{mesaj}" → eroare: {e}')
    
    # Salvare raport
    director_artefacte = RADACINA_PROIECT / "artifacts"
    director_artefacte.mkdir(exist_ok=True)
    fisier_raport = director_artefacte / "raport_demo.json"
    
    with open(fisier_raport, 'w', encoding='utf-8') as f:
        json.dump(raport, f, indent=2, ensure_ascii=False)
    
    print(f"\n{Culori.VERDE}Demonstrație completă!{Culori.FINAL}")
    print(f"Raport salvat: {fisier_raport}")

def demo_failover():
    """Demonstrație comportament failover."""
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}DEMONSTRAȚIE FAILOVER{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    # Stare inițială
    print(f"{Culori.BOLD}Stare Inițială:{Culori.FINAL}")
    for i in range(5):
        try:
            raspuns = requests.get("http://localhost:8080/", timeout=5)
            backend = "app1" if "app1" in raspuns.text.lower() else "app2"
            print(f"  Cerere {i+1}: {backend}")
        except:
            print(f"  Cerere {i+1}: eroare")
    
    # Oprește app1
    print(f"\n{Culori.GALBEN}Se oprește app1...{Culori.FINAL}")
    subprocess.run(["docker", "stop", "week14_app1"], capture_output=True)
    time.sleep(3)
    
    # Teste cu app1 oprit
    print(f"\n{Culori.BOLD}Stare cu app1 oprit:{Culori.FINAL}")
    for i in range(5):
        try:
            raspuns = requests.get("http://localhost:8080/", timeout=5)
            backend = "app1" if "app1" in raspuns.text.lower() else "app2"
            print(f"  Cerere {i+1}: {backend}")
        except:
            print(f"  Cerere {i+1}: eroare")
    
    # Repornește app1
    print(f"\n{Culori.VERDE}Se repornește app1...{Culori.FINAL}")
    subprocess.run(["docker", "start", "week14_app1"], capture_output=True)
    time.sleep(5)
    
    # Teste după repornire
    print(f"\n{Culori.BOLD}Stare după repornire:{Culori.FINAL}")
    for i in range(5):
        try:
            raspuns = requests.get("http://localhost:8080/", timeout=5)
            backend = "app1" if "app1" in raspuns.text.lower() else "app2"
            print(f"  Cerere {i+1}: {backend}")
        except:
            print(f"  Cerere {i+1}: eroare")
    
    print(f"\n{Culori.VERDE}Demonstrație failover completă!{Culori.FINAL}")

def demo_trafic():
    """Generează trafic pentru captură."""
    print(f"\n{Culori.BOLD}{'=' * 60}{Culori.FINAL}")
    print(f"{Culori.BOLD}GENERARE TRAFIC{Culori.FINAL}")
    print(f"{Culori.BOLD}{'=' * 60}{Culori.FINAL}\n")
    
    afiseaza_info("Se generează trafic HTTP...")
    
    for i in range(10):
        try:
            requests.get("http://localhost:8080/", timeout=5)
            print(f"  Cerere HTTP {i+1}")
        except:
            pass
        time.sleep(0.5)
    
    afiseaza_info("Se generează trafic TCP echo...")
    
    for i in range(5):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(('localhost', 9090))
            sock.sendall(f"Test trafic {i+1}\n".encode())
            sock.recv(1024)
            sock.close()
            print(f"  Cerere Echo {i+1}")
        except:
            pass
        time.sleep(0.3)
    
    print(f"\n{Culori.VERDE}Generare trafic completă!{Culori.FINAL}")

def main():
    parser = argparse.ArgumentParser(
        description="Demonstrații Laborator Săptămâna 14",
        epilog="Laborator Rețele de Calculatoare - ASE | by Revolvix"
    )
    
    parser.add_argument(
        "--demo", "-d",
        choices=["complet", "failover", "trafic"],
        default="complet",
        help="Tipul demonstrației (implicit: complet)"
    )
    
    args = parser.parse_args()
    
    if args.demo == "complet":
        demo_complet()
    elif args.demo == "failover":
        demo_failover()
    elif args.demo == "trafic":
        demo_trafic()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
