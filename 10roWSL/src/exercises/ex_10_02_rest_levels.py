#!/usr/bin/env python3
"""
Exercițiul 10.02: Nivelurile de Maturitate REST (Richardson)
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest exercițiu demonstrează cele 4 niveluri ale modelului Richardson:
- Nivelul 0: HTTP ca tunel pentru RPC
- Nivelul 1: Resurse individuale
- Nivelul 2: Verbe HTTP
- Nivelul 3: HATEOAS (Hypermedia as the Engine of Application State)

Utilizare:
    python ex_10_02_rest_levels.py              # Pornește serverul
    python ex_10_02_rest_levels.py --selftest   # Rulează auto-testare
    python ex_10_02_rest_levels.py --port 5001  # Folosește alt port
"""

import argparse
import json
import sys
import threading
import time
from typing import Dict, Any, List

try:
    from flask import Flask, request, jsonify, url_for
except ImportError:
    print("Eroare: Flask nu este instalat")
    print("Rulați: pip install flask")
    sys.exit(1)


# Configurație
PORT_IMPLICIT = 5000
GAZDA_IMPLICITA = "0.0.0.0"

# Aplicația Flask
app = Flask(__name__)

# Depozit de date simplu
class DepozitProduse:
    """Depozit în memorie pentru produse."""
    
    def __init__(self):
        self._produse: Dict[int, Dict[str, Any]] = {}
        self._urmatorul_id = 1
    
    def reseteaza(self):
        """Resetează depozitul."""
        self._produse.clear()
        self._urmatorul_id = 1
    
    def creeaza(self, date: Dict[str, Any]) -> Dict[str, Any]:
        """Creează un produs nou."""
        id_produs = self._urmatorul_id
        self._urmatorul_id += 1
        
        produs = {
            "id": id_produs,
            **date,
            "creat_la": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self._produse[id_produs] = produs
        return produs
    
    def citeste(self, id_produs: int) -> Dict[str, Any] | None:
        """Citește un produs."""
        return self._produse.get(id_produs)
    
    def citeste_toate(self) -> List[Dict[str, Any]]:
        """Returnează toate produsele."""
        return list(self._produse.values())
    
    def actualizeaza(self, id_produs: int, date: Dict[str, Any]) -> Dict[str, Any] | None:
        """Actualizează un produs."""
        if id_produs not in self._produse:
            return None
        self._produse[id_produs].update(date)
        return self._produse[id_produs]
    
    def sterge(self, id_produs: int) -> bool:
        """Șterge un produs."""
        if id_produs in self._produse:
            del self._produse[id_produs]
            return True
        return False


depozit = DepozitProduse()


# ============================================================================
# NIVELUL 0: RPC peste HTTP
# Un singur endpoint, toate operațiile prin POST cu un câmp "actiune"
# ============================================================================

@app.route('/api/nivel0', methods=['POST'])
def nivel0_rpc():
    """
    Nivelul 0: HTTP ca tunel pentru RPC.
    
    Toate operațiile sunt făcute prin POST către un singur endpoint.
    Acțiunea este specificată în corpul cererii.
    
    Exemplu cerere:
        {"actiune": "listeaza"}
        {"actiune": "creeaza", "date": {"nume": "Produs"}}
        {"actiune": "citeste", "id": 1}
        {"actiune": "actualizeaza", "id": 1, "date": {"nume": "Nou"}}
        {"actiune": "sterge", "id": 1}
    """
    date = request.get_json() or {}
    actiune = date.get('actiune', '')
    
    if actiune == 'listeaza':
        return jsonify({
            "succes": True,
            "rezultat": depozit.citeste_toate()
        })
    
    elif actiune == 'creeaza':
        produs = depozit.creeaza(date.get('date', {}))
        return jsonify({
            "succes": True,
            "rezultat": produs
        })
    
    elif actiune == 'citeste':
        id_produs = date.get('id')
        produs = depozit.citeste(id_produs)
        if produs:
            return jsonify({"succes": True, "rezultat": produs})
        return jsonify({"succes": False, "eroare": "Produs negăsit"})
    
    elif actiune == 'actualizeaza':
        id_produs = date.get('id')
        produs = depozit.actualizeaza(id_produs, date.get('date', {}))
        if produs:
            return jsonify({"succes": True, "rezultat": produs})
        return jsonify({"succes": False, "eroare": "Produs negăsit"})
    
    elif actiune == 'sterge':
        id_produs = date.get('id')
        if depozit.sterge(id_produs):
            return jsonify({"succes": True, "mesaj": "Produs șters"})
        return jsonify({"succes": False, "eroare": "Produs negăsit"})
    
    else:
        return jsonify({
            "succes": False,
            "eroare": f"Acțiune necunoscută: {actiune}",
            "actiuni_disponibile": ["listeaza", "creeaza", "citeste", "actualizeaza", "sterge"]
        })


# ============================================================================
# NIVELUL 1: Resurse
# Endpoint-uri separate pentru fiecare resursă, dar încă folosește doar POST
# ============================================================================

@app.route('/api/nivel1/produse', methods=['POST'])
def nivel1_produse():
    """
    Nivelul 1: Resurse individuale.
    
    Fiecare resursă are propriul endpoint, dar toate operațiile
    sunt încă făcute prin POST.
    """
    date = request.get_json() or {}
    actiune = date.get('actiune', 'creeaza')
    
    if actiune == 'listeaza' or not date.get('actiune'):
        # Listare sau creare
        if 'nume' in date:
            produs = depozit.creeaza(date)
            return jsonify({"produs": produs})
        return jsonify({"produse": depozit.citeste_toate()})
    
    return jsonify({"eroare": "Operație invalidă"})


@app.route('/api/nivel1/produse/<int:id_produs>', methods=['POST'])
def nivel1_produs(id_produs: int):
    """Operații pe un produs specific (Nivelul 1)."""
    date = request.get_json() or {}
    actiune = date.get('actiune', 'citeste')
    
    if actiune == 'citeste':
        produs = depozit.citeste(id_produs)
        if produs:
            return jsonify({"produs": produs})
        return jsonify({"eroare": "Produs negăsit"}), 404
    
    elif actiune == 'actualizeaza':
        produs = depozit.actualizeaza(id_produs, date.get('date', {}))
        if produs:
            return jsonify({"produs": produs})
        return jsonify({"eroare": "Produs negăsit"}), 404
    
    elif actiune == 'sterge':
        if depozit.sterge(id_produs):
            return jsonify({"mesaj": "Produs șters"})
        return jsonify({"eroare": "Produs negăsit"}), 404
    
    return jsonify({"eroare": "Acțiune necunoscută"})


# ============================================================================
# NIVELUL 2: Verbe HTTP
# Folosește metodele HTTP corecte (GET, POST, PUT, DELETE)
# ============================================================================

@app.route('/api/nivel2/produse', methods=['GET'])
def nivel2_listeaza():
    """GET - Listează toate produsele."""
    return jsonify({"produse": depozit.citeste_toate()})


@app.route('/api/nivel2/produse', methods=['POST'])
def nivel2_creeaza():
    """POST - Creează un produs nou."""
    date = request.get_json() or {}
    produs = depozit.creeaza(date)
    return jsonify({"produs": produs}), 201


@app.route('/api/nivel2/produse/<int:id_produs>', methods=['GET'])
def nivel2_citeste(id_produs: int):
    """GET - Citește un produs specific."""
    produs = depozit.citeste(id_produs)
    if produs:
        return jsonify({"produs": produs})
    return jsonify({"eroare": "Produs negăsit"}), 404


@app.route('/api/nivel2/produse/<int:id_produs>', methods=['PUT'])
def nivel2_actualizeaza(id_produs: int):
    """PUT - Actualizează un produs."""
    date = request.get_json() or {}
    produs = depozit.actualizeaza(id_produs, date)
    if produs:
        return jsonify({"produs": produs})
    return jsonify({"eroare": "Produs negăsit"}), 404


@app.route('/api/nivel2/produse/<int:id_produs>', methods=['DELETE'])
def nivel2_sterge(id_produs: int):
    """DELETE - Șterge un produs."""
    if depozit.sterge(id_produs):
        return jsonify({"mesaj": "Produs șters"})
    return jsonify({"eroare": "Produs negăsit"}), 404


# ============================================================================
# NIVELUL 3: HATEOAS
# Răspunsurile includ linkuri către acțiunile disponibile
# ============================================================================

def adauga_linkuri_produs(produs: Dict[str, Any]) -> Dict[str, Any]:
    """Adaugă linkuri HATEOAS la un produs."""
    id_produs = produs['id']
    produs['_linkuri'] = {
        "self": f"/api/nivel3/produse/{id_produs}",
        "actualizeaza": {
            "href": f"/api/nivel3/produse/{id_produs}",
            "metoda": "PUT"
        },
        "sterge": {
            "href": f"/api/nivel3/produse/{id_produs}",
            "metoda": "DELETE"
        },
        "colectie": "/api/nivel3/produse"
    }
    return produs


@app.route('/api/nivel3/produse', methods=['GET'])
def nivel3_listeaza():
    """GET - Listează produsele cu linkuri HATEOAS."""
    produse = [adauga_linkuri_produs(p.copy()) for p in depozit.citeste_toate()]
    return jsonify({
        "produse": produse,
        "_linkuri": {
            "self": "/api/nivel3/produse",
            "creeaza": {
                "href": "/api/nivel3/produse",
                "metoda": "POST",
                "corpNecesar": {"nume": "string", "pret": "number"}
            }
        }
    })


@app.route('/api/nivel3/produse', methods=['POST'])
def nivel3_creeaza():
    """POST - Creează un produs cu răspuns HATEOAS."""
    date = request.get_json() or {}
    produs = depozit.creeaza(date)
    produs_cu_linkuri = adauga_linkuri_produs(produs.copy())
    
    return jsonify({
        "mesaj": "Produs creat cu succes",
        "produs": produs_cu_linkuri
    }), 201


@app.route('/api/nivel3/produse/<int:id_produs>', methods=['GET'])
def nivel3_citeste(id_produs: int):
    """GET - Citește un produs cu linkuri HATEOAS."""
    produs = depozit.citeste(id_produs)
    if produs:
        return jsonify({"produs": adauga_linkuri_produs(produs.copy())})
    return jsonify({
        "eroare": "Produs negăsit",
        "_linkuri": {"colectie": "/api/nivel3/produse"}
    }), 404


@app.route('/api/nivel3/produse/<int:id_produs>', methods=['PUT'])
def nivel3_actualizeaza(id_produs: int):
    """PUT - Actualizează un produs cu răspuns HATEOAS."""
    date = request.get_json() or {}
    produs = depozit.actualizeaza(id_produs, date)
    if produs:
        return jsonify({"produs": adauga_linkuri_produs(produs.copy())})
    return jsonify({
        "eroare": "Produs negăsit",
        "_linkuri": {"colectie": "/api/nivel3/produse"}
    }), 404


@app.route('/api/nivel3/produse/<int:id_produs>', methods=['DELETE'])
def nivel3_sterge(id_produs: int):
    """DELETE - Șterge un produs cu răspuns HATEOAS."""
    if depozit.sterge(id_produs):
        return jsonify({
            "mesaj": "Produs șters",
            "_linkuri": {"colectie": "/api/nivel3/produse"}
        })
    return jsonify({
        "eroare": "Produs negăsit",
        "_linkuri": {"colectie": "/api/nivel3/produse"}
    }), 404


# ============================================================================
# Pagina principală
# ============================================================================

@app.route('/')
def pagina_principala():
    """Pagina principală cu documentația API-ului."""
    return jsonify({
        "titlu": "Demonstrație Niveluri REST (Richardson)",
        "descriere": "Acest server demonstrează cele 4 niveluri ale modelului de maturitate Richardson",
        "niveluri": {
            "nivel0": {
                "descriere": "RPC peste HTTP - un singur endpoint",
                "endpoint": "/api/nivel0",
                "metoda": "POST",
                "exemplu": {"actiune": "listeaza"}
            },
            "nivel1": {
                "descriere": "Resurse individuale",
                "endpoints": ["/api/nivel1/produse", "/api/nivel1/produse/{id}"],
                "metoda": "POST"
            },
            "nivel2": {
                "descriere": "Verbe HTTP corecte",
                "endpoints": ["/api/nivel2/produse", "/api/nivel2/produse/{id}"],
                "metode": ["GET", "POST", "PUT", "DELETE"]
            },
            "nivel3": {
                "descriere": "HATEOAS - Hypermedia",
                "endpoints": ["/api/nivel3/produse", "/api/nivel3/produse/{id}"],
                "metode": ["GET", "POST", "PUT", "DELETE"],
                "nota": "Răspunsurile includ linkuri către acțiuni disponibile"
            }
        }
    })


def ruleaza_auto_testare(port: int = PORT_IMPLICIT):
    """Rulează o suită de teste pentru toate nivelurile."""
    import requests
    
    print()
    print("=" * 60)
    print("  AUTO-TESTARE NIVELURI REST")
    print("=" * 60)
    print()
    
    url_baza = f"http://localhost:{port}"
    teste_trecute = 0
    teste_esuate = 0
    
    def test(nume: str, metoda: str, cale: str, date: dict = None, cod_asteptat: int = 200):
        nonlocal teste_trecute, teste_esuate
        
        url = f"{url_baza}{cale}"
        
        try:
            if metoda == 'GET':
                raspuns = requests.get(url, timeout=5)
            elif metoda == 'POST':
                raspuns = requests.post(url, json=date, timeout=5)
            elif metoda == 'PUT':
                raspuns = requests.put(url, json=date, timeout=5)
            elif metoda == 'DELETE':
                raspuns = requests.delete(url, timeout=5)
            else:
                print(f"  ✗ {nume} (metodă necunoscută)")
                teste_esuate += 1
                return
            
            if raspuns.status_code == cod_asteptat:
                print(f"  ✓ {nume}")
                teste_trecute += 1
            else:
                print(f"  ✗ {nume} (cod: {raspuns.status_code}, așteptat: {cod_asteptat})")
                teste_esuate += 1
                
        except Exception as e:
            print(f"  ✗ {nume} (eroare: {e})")
            teste_esuate += 1
    
    # Pornește server într-un thread
    depozit.reseteaza()
    fir_server = threading.Thread(
        target=lambda: app.run(host='localhost', port=port, debug=False, use_reloader=False),
        daemon=True
    )
    fir_server.start()
    time.sleep(1)
    
    # Teste Nivelul 0
    print("  NIVELUL 0 (RPC):")
    test("L0: Listare", "POST", "/api/nivel0", {"actiune": "listeaza"})
    test("L0: Creare", "POST", "/api/nivel0", {"actiune": "creeaza", "date": {"nume": "Test L0"}})
    test("L0: Citire", "POST", "/api/nivel0", {"actiune": "citeste", "id": 1})
    test("L0: Actualizare", "POST", "/api/nivel0", {"actiune": "actualizeaza", "id": 1, "date": {"nume": "Actualizat"}})
    test("L0: Ștergere", "POST", "/api/nivel0", {"actiune": "sterge", "id": 1})
    print()
    
    # Teste Nivelul 2
    print("  NIVELUL 2 (Verbe HTTP):")
    test("L2: GET listare", "GET", "/api/nivel2/produse")
    test("L2: POST creare", "POST", "/api/nivel2/produse", {"nume": "Test L2"}, 201)
    test("L2: GET citire", "GET", "/api/nivel2/produse/2")
    test("L2: PUT actualizare", "PUT", "/api/nivel2/produse/2", {"nume": "Actualizat L2"})
    test("L2: DELETE ștergere", "DELETE", "/api/nivel2/produse/2")
    print()
    
    # Teste Nivelul 3
    print("  NIVELUL 3 (HATEOAS):")
    test("L3: GET listare cu linkuri", "GET", "/api/nivel3/produse")
    test("L3: POST creare cu linkuri", "POST", "/api/nivel3/produse", {"nume": "Test L3", "pret": 99.99}, 201)
    test("L3: GET citire cu linkuri", "GET", "/api/nivel3/produse/3")
    print()
    
    # Sumar
    print("─" * 60)
    print(f"  Rezultat: {teste_trecute} trecute, {teste_esuate} eșuate")
    
    return 0 if teste_esuate == 0 else 1


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Exercițiul 10.02: Nivelurile de Maturitate REST"
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=PORT_IMPLICIT,
        help=f"Portul serverului (implicit: {PORT_IMPLICIT})"
    )
    parser.add_argument(
        "--selftest",
        action="store_true",
        help="Rulează auto-testare"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Mod debug Flask"
    )
    args = parser.parse_args()
    
    if args.selftest:
        return ruleaza_auto_testare(args.port)
    
    print()
    print("=" * 60)
    print("  NIVELURI DE MATURITATE REST (Richardson)")
    print("  Laborator Rețele de Calculatoare")
    print("=" * 60)
    print()
    print(f"  Server pornit pe http://localhost:{args.port}")
    print()
    print("  Niveluri disponibile:")
    print("    • Nivelul 0: /api/nivel0 (RPC)")
    print("    • Nivelul 1: /api/nivel1/produse (Resurse)")
    print("    • Nivelul 2: /api/nivel2/produse (Verbe HTTP)")
    print("    • Nivelul 3: /api/nivel3/produse (HATEOAS)")
    print()
    print("  Apăsați Ctrl+C pentru oprire")
    print("─" * 60)
    
    app.run(host=GAZDA_IMPLICITA, port=args.port, debug=args.debug)
    return 0


if __name__ == "__main__":
    sys.exit(main())
