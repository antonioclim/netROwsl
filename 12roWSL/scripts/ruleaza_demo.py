#!/usr/bin/env python3
"""
Script de Demonstrații pentru Laboratorul Săptămânii 12
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Demonstrații automate pentru protocoalele SMTP și RPC.
"""

import subprocess
import sys
import time
import json
import argparse
from pathlib import Path

RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger
from scripts.utils.network_utils import TesterSMTP, TesterJSONRPC, TesterXMLRPC

logger = configureaza_logger("ruleaza_demo")


def pauza_interactiva(mesaj: str = "Apăsați Enter pentru a continua..."):
    """Pauză cu mesaj pentru demonstrații."""
    print(f"\n  ⏸  {mesaj}")
    input()


def afiseaza_sectiune(titlu: str):
    """Afișează un antet de secțiune."""
    print("\n" + "=" * 60)
    print(f"  {titlu}")
    print("=" * 60 + "\n")


def demo_smtp():
    """Demonstrație dialog SMTP."""
    afiseaza_sectiune("DEMONSTRAȚIE: Dialog SMTP")
    
    print("Această demonstrație prezintă un dialog SMTP complet.")
    print("Vom trimite un email de test folosind protocolul SMTP.\n")
    
    tester = TesterSMTP("localhost", 1025)
    
    try:
        # Conectare
        print("[1] Conectare la serverul SMTP...")
        raspuns = tester.conecteaza()
        print(f"    ← {raspuns}")
        pauza_interactiva()
        
        # HELO
        print("[2] Trimitere comandă HELO...")
        print("    → HELO demo.local")
        raspuns = tester.trimite_comanda("HELO demo.local")
        print(f"    ← {raspuns}")
        pauza_interactiva()
        
        # MAIL FROM
        print("[3] Specificare expeditor (MAIL FROM)...")
        print("    → MAIL FROM:<demo@laborator.ro>")
        raspuns = tester.trimite_comanda("MAIL FROM:<demo@laborator.ro>")
        print(f"    ← {raspuns}")
        pauza_interactiva()
        
        # RCPT TO
        print("[4] Specificare destinatar (RCPT TO)...")
        print("    → RCPT TO:<student@ase.ro>")
        raspuns = tester.trimite_comanda("RCPT TO:<student@ase.ro>")
        print(f"    ← {raspuns}")
        pauza_interactiva()
        
        # DATA
        print("[5] Trimitere conținut mesaj (DATA)...")
        print("    → DATA")
        raspuns = tester.trimite_comanda("DATA")
        print(f"    ← {raspuns}")
        
        mesaj = """Subject: Demonstratie SMTP din Laborator
From: demo@laborator.ro
To: student@ase.ro
Date: {date}

Acesta este un mesaj de demonstratie trimis prin
dialogul SMTP din Laboratorul Saptamanii 12.

Protocoalele aplicate: SMTP (RFC 5321)

Cu stima,
Sistemul de Laborator
.
""".format(date=time.strftime("%a, %d %b %Y %H:%M:%S +0000"))
        
        print("    → [Conținut mesaj...]")
        raspuns = tester.trimite_date(mesaj)
        print(f"    ← {raspuns}")
        pauza_interactiva()
        
        # LIST (comandă nestandardă)
        print("[6] Listare mesaje stocate (LIST - comandă educațională)...")
        print("    → LIST")
        raspuns = tester.trimite_comanda("LIST")
        print(f"    ← {raspuns}")
        pauza_interactiva()
        
        # QUIT
        print("[7] Închidere conexiune (QUIT)...")
        print("    → QUIT")
        raspuns = tester.trimite_comanda("QUIT")
        print(f"    ← {raspuns}")
        
        tester.deconecteaza()
        
        print("\n✓ Demonstrație SMTP completă!")
        
    except Exception as e:
        logger.error(f"Eroare în demonstrația SMTP: {e}")
        return False
    
    return True


def demo_jsonrpc():
    """Demonstrație apeluri JSON-RPC."""
    afiseaza_sectiune("DEMONSTRAȚIE: JSON-RPC 2.0")
    
    print("Această demonstrație prezintă apeluri JSON-RPC 2.0.")
    print("Vom efectua apeluri singulare și în lot (batch).\n")
    
    tester = TesterJSONRPC("localhost", 6200)
    
    try:
        # Apel simplu
        print("[1] Apel simplu: add(15, 27)")
        cerere = {"jsonrpc": "2.0", "method": "add", "params": [15, 27], "id": 1}
        print(f"    → {json.dumps(cerere)}")
        rezultat = tester.apeleaza("add", [15, 27])
        print(f"    ← Rezultat: {rezultat}")
        pauza_interactiva()
        
        # Apel cu parametri numiți
        print("[2] Apel cu parametri numiți: subtract(a=100, b=37)")
        cerere = {"jsonrpc": "2.0", "method": "subtract", "params": {"a": 100, "b": 37}, "id": 2}
        print(f"    → {json.dumps(cerere)}")
        rezultat = tester.apeleaza("subtract", {"a": 100, "b": 37})
        print(f"    ← Rezultat: {rezultat}")
        pauza_interactiva()
        
        # Apel în lot (batch)
        print("[3] Apel în lot (batch): 3 operații simultane")
        cereri = [
            {"method": "add", "params": [1, 2]},
            {"method": "multiply", "params": [3, 4]},
            {"method": "get_time", "params": []}
        ]
        print(f"    → [3 cereri în lot]")
        rezultate = tester.apel_lot(cereri)
        for i, r in enumerate(rezultate, 1):
            print(f"    ← [{i}] {r}")
        pauza_interactiva()
        
        # Demonstrare eroare
        print("[4] Demonstrare eroare: metodă inexistentă")
        cerere = {"jsonrpc": "2.0", "method": "metoda_falsa", "id": 4}
        print(f"    → {json.dumps(cerere)}")
        try:
            rezultat = tester.apeleaza("metoda_falsa", [])
        except Exception as e:
            print(f"    ← Eroare (așteptată): {e}")
        pauza_interactiva()
        
        # Statistici server
        print("[5] Obținere statistici server")
        rezultat = tester.apeleaza("get_stats", [])
        print(f"    ← {json.dumps(rezultat, indent=6)}")
        
        print("\n✓ Demonstrație JSON-RPC completă!")
        
    except Exception as e:
        logger.error(f"Eroare în demonstrația JSON-RPC: {e}")
        return False
    
    return True


def demo_xmlrpc():
    """Demonstrație apeluri XML-RPC."""
    afiseaza_sectiune("DEMONSTRAȚIE: XML-RPC")
    
    print("Această demonstrație prezintă apeluri XML-RPC cu introspecție.")
    print("XML-RPC folosește XML pentru codificarea datelor.\n")
    
    tester = TesterXMLRPC("localhost", 6201)
    
    try:
        # Listare metode (introspecție)
        print("[1] Introspecție: listare metode disponibile")
        print("    → system.listMethods()")
        metode = tester.proxy.system.listMethods()
        print(f"    ← Metode: {', '.join(metode[:5])}...")
        pauza_interactiva()
        
        # Ajutor metodă
        print("[2] Introspecție: ajutor pentru metoda 'add'")
        print("    → system.methodHelp('add')")
        ajutor = tester.proxy.system.methodHelp("add")
        print(f"    ← {ajutor}")
        pauza_interactiva()
        
        # Apel calcul
        print("[3] Apel calcul: multiply(7, 8)")
        print("    → multiply(7, 8)")
        rezultat = tester.proxy.multiply(7, 8)
        print(f"    ← Rezultat: {rezultat}")
        pauza_interactiva()
        
        # Comparare dimensiune cerere
        print("[4] Observație: Dimensiunea cererii XML-RPC")
        cerere_xml = """<?xml version="1.0"?>
<methodCall>
  <methodName>multiply</methodName>
  <params>
    <param><value><int>7</int></value></param>
    <param><value><int>8</int></value></param>
  </params>
</methodCall>"""
        print(f"    Dimensiune cerere XML: {len(cerere_xml)} bytes")
        cerere_json = '{"jsonrpc":"2.0","method":"multiply","params":[7,8],"id":1}'
        print(f"    Dimensiune cerere JSON: {len(cerere_json)} bytes")
        print(f"    Raport: XML/JSON = {len(cerere_xml)/len(cerere_json):.1f}x")
        
        print("\n✓ Demonstrație XML-RPC completă!")
        
    except Exception as e:
        logger.error(f"Eroare în demonstrația XML-RPC: {e}")
        return False
    
    return True


def demo_rpc_comparatie():
    """Comparație între protocoalele RPC."""
    afiseaza_sectiune("DEMONSTRAȚIE: Comparație Protocoale RPC")
    
    print("Comparăm JSON-RPC, XML-RPC și gRPC pentru aceeași operație.\n")
    
    operatie = "add(100, 200)"
    print(f"Operație de test: {operatie}\n")
    
    # JSON-RPC
    print("[JSON-RPC 2.0]")
    print("  Format: JSON peste HTTP/1.1")
    try:
        tester_json = TesterJSONRPC("localhost", 6200)
        start = time.perf_counter()
        rezultat = tester_json.apeleaza("add", [100, 200])
        durata = (time.perf_counter() - start) * 1000
        print(f"  Rezultat: {rezultat}")
        print(f"  Timp: {durata:.2f} ms")
    except Exception as e:
        print(f"  Eroare: {e}")
    
    pauza_interactiva()
    
    # XML-RPC
    print("[XML-RPC]")
    print("  Format: XML peste HTTP/1.1")
    try:
        tester_xml = TesterXMLRPC("localhost", 6201)
        start = time.perf_counter()
        rezultat = tester_xml.proxy.add(100, 200)
        durata = (time.perf_counter() - start) * 1000
        print(f"  Rezultat: {rezultat}")
        print(f"  Timp: {durata:.2f} ms")
    except Exception as e:
        print(f"  Eroare: {e}")
    
    pauza_interactiva()
    
    # gRPC
    print("[gRPC]")
    print("  Format: Protocol Buffers peste HTTP/2")
    try:
        sys.path.insert(0, str(RADACINA_PROIECT / "src" / "apps" / "rpc" / "grpc"))
        import grpc
        import calculator_pb2
        import calculator_pb2_grpc
        
        canal = grpc.insecure_channel("localhost:6251")
        stub = calculator_pb2_grpc.CalculatorServiceStub(canal)
        
        start = time.perf_counter()
        cerere = calculator_pb2.BinaryOpRequest(a=100, b=200)
        raspuns = stub.Add(cerere)
        durata = (time.perf_counter() - start) * 1000
        print(f"  Rezultat: {raspuns.result}")
        print(f"  Timp: {durata:.2f} ms")
        canal.close()
    except Exception as e:
        print(f"  Eroare: {e}")
    
    print("\n✓ Comparație completă!")
    return True


def demo_benchmark():
    """Benchmark performanță RPC."""
    afiseaza_sectiune("DEMONSTRAȚIE: Benchmark RPC")
    
    print("Rulăm un benchmark pentru a compara performanța protocoalelor.\n")
    
    script_benchmark = RADACINA_PROIECT / "src" / "apps" / "rpc" / "benchmark_rpc.py"
    
    if script_benchmark.exists():
        print("Se execută scriptul de benchmark...\n")
        subprocess.run([sys.executable, str(script_benchmark)])
    else:
        print("Scriptul de benchmark nu a fost găsit.")
        print(f"Calea așteptată: {script_benchmark}")
    
    return True


DEMONSTRATII = {
    "smtp": ("Dialog SMTP", demo_smtp),
    "jsonrpc": ("Apeluri JSON-RPC", demo_jsonrpc),
    "xmlrpc": ("Apeluri XML-RPC", demo_xmlrpc),
    "rpc-compara": ("Comparație RPC", demo_rpc_comparatie),
    "benchmark": ("Benchmark RPC", demo_benchmark),
    "all": ("Toate demonstrațiile", None)
}


def main():
    parser = argparse.ArgumentParser(
        description="Demonstrații pentru Laboratorul Săptămânii 12"
    )
    parser.add_argument(
        "--demo", "-d",
        choices=list(DEMONSTRATII.keys()),
        default="all",
        help="Demonstrația de rulat (implicit: all)"
    )
    parser.add_argument(
        "--fara-pauze",
        action="store_true",
        help="Rulează fără pauze interactive"
    )
    args = parser.parse_args()

    if args.fara_pauze:
        global pauza_interactiva
        pauza_interactiva = lambda msg="": time.sleep(0.5)

    logger.info("=" * 60)
    logger.info("Demonstrații - Laboratorul Săptămânii 12")
    logger.info("SMTP, JSON-RPC, XML-RPC, gRPC")
    logger.info("=" * 60)

    if args.demo == "all":
        demo_list = ["smtp", "jsonrpc", "xmlrpc", "rpc-compara"]
    else:
        demo_list = [args.demo]

    for demo_key in demo_list:
        nume, functie = DEMONSTRATII[demo_key]
        if functie:
            try:
                functie()
            except KeyboardInterrupt:
                print("\n\nDemonstrație întreruptă de utilizator.")
                return 130
            except Exception as e:
                logger.error(f"Eroare în demonstrația '{nume}': {e}")
                continue

    print("\n" + "=" * 60)
    print("Toate demonstrațiile au fost finalizate!")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
