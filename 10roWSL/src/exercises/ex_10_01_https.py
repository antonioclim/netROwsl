#!/usr/bin/env python3
"""
Exercițiul 10.01: Server HTTPS cu REST API
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Acest exercițiu demonstrează:
- Crearea unui server HTTPS cu certificat auto-semnat
- Implementarea unui API REST simplu cu operații CRUD
- Înțelegerea handshake-ului TLS și a securității transportului

Utilizare:
    python ex_10_01_https.py              # Pornește serverul
    python ex_10_01_https.py --selftest   # Rulează auto-testare
    python ex_10_01_https.py --port 8443  # Folosește alt port
"""

import argparse
import json
import ssl
import sys
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Dict, Any, Optional
from urllib.request import Request, urlopen
from urllib.error import URLError
import tempfile
import subprocess


# Configurație implicită
PORT_IMPLICIT = 4443
GAZDA_IMPLICITA = "0.0.0.0"


class DepozitResurse:
    """
    Depozit simplu în memorie pentru resurse.
    Demonstrează un model de date pentru API REST.
    """
    
    def __init__(self):
        self._resurse: Dict[int, Dict[str, Any]] = {}
        self._urmatorul_id = 1
        self._blocare = threading.Lock()
    
    def creeaza(self, date: Dict[str, Any]) -> Dict[str, Any]:
        """Creează o resursă nouă."""
        with self._blocare:
            id_resursa = self._urmatorul_id
            self._urmatorul_id += 1
            
            resursa = {
                "id": id_resursa,
                **date,
                "creat_la": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            self._resurse[id_resursa] = resursa
            return resursa
    
    def citeste(self, id_resursa: int) -> Optional[Dict[str, Any]]:
        """Citește o resursă după ID."""
        return self._resurse.get(id_resursa)
    
    def citeste_toate(self) -> list:
        """Returnează toate resursele."""
        return list(self._resurse.values())
    
    def actualizeaza(self, id_resursa: int, date: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Actualizează o resursă existentă."""
        with self._blocare:
            if id_resursa not in self._resurse:
                return None
            
            self._resurse[id_resursa].update(date)
            self._resurse[id_resursa]["actualizat_la"] = time.strftime("%Y-%m-%d %H:%M:%S")
            return self._resurse[id_resursa]
    
    def sterge(self, id_resursa: int) -> bool:
        """Șterge o resursă."""
        with self._blocare:
            if id_resursa in self._resurse:
                del self._resurse[id_resursa]
                return True
            return False


# Instanță globală a depozitului
depozit = DepozitResurse()


class HandlerHTTPS(BaseHTTPRequestHandler):
    """
    Handler pentru cereri HTTPS.
    Implementează un API REST simplu pentru gestionarea resurselor.
    """
    
    # Suprimă mesajele de log standard
    def log_message(self, format, *args):
        print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")
    
    def _trimite_raspuns_json(self, cod_stare: int, date: Any):
        """Trimite un răspuns JSON."""
        corp = json.dumps(date, ensure_ascii=False, indent=2).encode('utf-8')
        
        self.send_response(cod_stare)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(corp))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(corp)
    
    def _citeste_corp_json(self) -> Optional[Dict]:
        """Citește și parsează corpul cererii ca JSON."""
        try:
            lungime_continut = int(self.headers.get('Content-Length', 0))
            if lungime_continut == 0:
                return {}
            
            corp = self.rfile.read(lungime_continut)
            return json.loads(corp.decode('utf-8'))
        except (json.JSONDecodeError, ValueError) as e:
            return None
    
    def _extrage_id_resursa(self) -> Optional[int]:
        """Extrage ID-ul resursei din cale."""
        parti = self.path.strip('/').split('/')
        if len(parti) >= 3:
            try:
                return int(parti[2])
            except ValueError:
                return None
        return None
    
    def do_GET(self):
        """Gestionează cererile GET."""
        if self.path == '/':
            # Pagina principală
            self._trimite_raspuns_json(200, {
                "mesaj": "Bine ați venit la serverul HTTPS!",
                "versiune": "1.0",
                "endpoints": [
                    "GET /api/resurse - Listează toate resursele",
                    "GET /api/resurse/{id} - Obține o resursă",
                    "POST /api/resurse - Creează o resursă",
                    "PUT /api/resurse/{id} - Actualizează o resursă",
                    "DELETE /api/resurse/{id} - Șterge o resursă"
                ]
            })
        
        elif self.path == '/api/resurse':
            # Listează toate resursele
            resurse = depozit.citeste_toate()
            self._trimite_raspuns_json(200, {
                "total": len(resurse),
                "resurse": resurse
            })
        
        elif self.path.startswith('/api/resurse/'):
            # Obține o resursă specifică
            id_resursa = self._extrage_id_resursa()
            if id_resursa is None:
                self._trimite_raspuns_json(400, {"eroare": "ID invalid"})
                return
            
            resursa = depozit.citeste(id_resursa)
            if resursa:
                self._trimite_raspuns_json(200, resursa)
            else:
                self._trimite_raspuns_json(404, {"eroare": "Resursa nu a fost găsită"})
        
        else:
            self._trimite_raspuns_json(404, {"eroare": "Endpoint necunoscut"})
    
    def do_POST(self):
        """Gestionează cererile POST."""
        if self.path == '/api/resurse':
            date = self._citeste_corp_json()
            if date is None:
                self._trimite_raspuns_json(400, {"eroare": "JSON invalid"})
                return
            
            resursa = depozit.creeaza(date)
            self._trimite_raspuns_json(201, {
                "mesaj": "Resursă creată cu succes",
                "resursa": resursa
            })
        else:
            self._trimite_raspuns_json(404, {"eroare": "Endpoint necunoscut"})
    
    def do_PUT(self):
        """Gestionează cererile PUT."""
        if self.path.startswith('/api/resurse/'):
            id_resursa = self._extrage_id_resursa()
            if id_resursa is None:
                self._trimite_raspuns_json(400, {"eroare": "ID invalid"})
                return
            
            date = self._citeste_corp_json()
            if date is None:
                self._trimite_raspuns_json(400, {"eroare": "JSON invalid"})
                return
            
            resursa = depozit.actualizeaza(id_resursa, date)
            if resursa:
                self._trimite_raspuns_json(200, {
                    "mesaj": "Resursă actualizată",
                    "resursa": resursa
                })
            else:
                self._trimite_raspuns_json(404, {"eroare": "Resursa nu a fost găsită"})
        else:
            self._trimite_raspuns_json(404, {"eroare": "Endpoint necunoscut"})
    
    def do_DELETE(self):
        """Gestionează cererile DELETE."""
        if self.path.startswith('/api/resurse/'):
            id_resursa = self._extrage_id_resursa()
            if id_resursa is None:
                self._trimite_raspuns_json(400, {"eroare": "ID invalid"})
                return
            
            if depozit.sterge(id_resursa):
                self._trimite_raspuns_json(200, {"mesaj": "Resursă ștearsă"})
            else:
                self._trimite_raspuns_json(404, {"eroare": "Resursa nu a fost găsită"})
        else:
            self._trimite_raspuns_json(404, {"eroare": "Endpoint necunoscut"})
    
    def do_OPTIONS(self):
        """Gestionează cererile OPTIONS pentru CORS."""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def genereaza_certificat_autosemnat(dir_iesire: Path) -> tuple:
    """
    Generează un certificat TLS auto-semnat.
    
    Args:
        dir_iesire: Directorul pentru fișierele de certificat
    
    Returns:
        Tuple (cale_certificat, cale_cheie)
    """
    dir_iesire.mkdir(parents=True, exist_ok=True)
    
    cale_cheie = dir_iesire / "server.key"
    cale_cert = dir_iesire / "server.crt"
    
    # Verifică dacă există deja
    if cale_cheie.exists() and cale_cert.exists():
        print(f"  Folosesc certificatele existente din {dir_iesire}")
        return str(cale_cert), str(cale_cheie)
    
    print("  Generez certificat TLS auto-semnat...")
    
    try:
        # Încearcă cu OpenSSL
        rezultat = subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(cale_cheie),
            "-out", str(cale_cert),
            "-days", "365",
            "-nodes",
            "-subj", "/C=RO/ST=Bucharest/L=Bucharest/O=ASE/OU=Informatica/CN=localhost"
        ], capture_output=True, timeout=30)
        
        if rezultat.returncode == 0:
            print(f"  ✓ Certificat generat: {cale_cert}")
            return str(cale_cert), str(cale_cheie)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    # Fallback: generare cu Python (cryptography)
    try:
        from cryptography import x509
        from cryptography.x509.oid import NameOID
        from cryptography.hazmat.primitives import hashes
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
        from datetime import datetime, timedelta
        
        # Generează cheie privată
        cheie = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        
        # Generează certificat
        subiect = emitent = x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, "RO"),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Bucharest"),
            x509.NameAttribute(NameOID.LOCALITY_NAME, "Bucharest"),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, "ASE"),
            x509.NameAttribute(NameOID.COMMON_NAME, "localhost"),
        ])
        
        cert = x509.CertificateBuilder().subject_name(
            subiect
        ).issuer_name(
            emitent
        ).public_key(
            cheie.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=365)
        ).add_extension(
            x509.SubjectAlternativeName([x509.DNSName("localhost")]),
            critical=False,
        ).sign(cheie, hashes.SHA256())
        
        # Salvează fișierele
        with open(cale_cheie, "wb") as f:
            f.write(cheie.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(cale_cert, "wb") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM))
        
        print(f"  ✓ Certificat generat (Python): {cale_cert}")
        return str(cale_cert), str(cale_cheie)
        
    except ImportError:
        print("  ✗ Biblioteca 'cryptography' nu este instalată")
        print("    Rulați: pip install cryptography")
        sys.exit(1)


def porneste_server(port: int = PORT_IMPLICIT, gazda: str = GAZDA_IMPLICITA):
    """Pornește serverul HTTPS."""
    print()
    print("=" * 60)
    print("  SERVER HTTPS - Exercițiul 10.01")
    print("  Laborator Rețele de Calculatoare")
    print("=" * 60)
    print()
    
    # Generează sau folosește certificat existent
    dir_certs = Path(__file__).parent.parent.parent / "artifacts" / "certs"
    cale_cert, cale_cheie = genereaza_certificat_autosemnat(dir_certs)
    
    # Creează context SSL
    context_ssl = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context_ssl.load_cert_chain(cale_cert, cale_cheie)
    
    # Pornește serverul
    server = HTTPServer((gazda, port), HandlerHTTPS)
    server.socket = context_ssl.wrap_socket(server.socket, server_side=True)
    
    print()
    print(f"  ✓ Server HTTPS pornit pe https://{gazda}:{port}")
    print()
    print("  Testare cu curl:")
    print(f"    curl -k https://localhost:{port}/")
    print(f"    curl -k https://localhost:{port}/api/resurse")
    print()
    print("  Apăsați Ctrl+C pentru oprire")
    print("─" * 60)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server oprit.")
        server.shutdown()


def ruleaza_auto_testare(port: int = PORT_IMPLICIT):
    """Rulează o suită de teste pentru verificarea funcționalității."""
    print()
    print("=" * 60)
    print("  AUTO-TESTARE SERVER HTTPS")
    print("=" * 60)
    print()
    
    url_baza = f"https://localhost:{port}"
    teste_trecute = 0
    teste_esuate = 0
    
    # Creează context SSL care ignoră verificarea certificatului
    context_ssl = ssl.create_default_context()
    context_ssl.check_hostname = False
    context_ssl.verify_mode = ssl.CERT_NONE
    
    def test(nume: str, metoda: str, cale: str, date: dict = None, cod_asteptat: int = 200):
        nonlocal teste_trecute, teste_esuate
        
        url = f"{url_baza}{cale}"
        
        try:
            if date:
                corp = json.dumps(date).encode('utf-8')
                cerere = Request(url, data=corp, method=metoda)
                cerere.add_header("Content-Type", "application/json")
            else:
                cerere = Request(url, method=metoda)
            
            with urlopen(cerere, context=context_ssl, timeout=5) as raspuns:
                cod = raspuns.getcode()
                if cod == cod_asteptat:
                    print(f"  ✓ {nume}")
                    teste_trecute += 1
                else:
                    print(f"  ✗ {nume} (cod: {cod}, așteptat: {cod_asteptat})")
                    teste_esuate += 1
                
        except URLError as e:
            if hasattr(e, 'code') and e.code == cod_asteptat:
                print(f"  ✓ {nume}")
                teste_trecute += 1
            else:
                print(f"  ✗ {nume} (eroare: {e})")
                teste_esuate += 1
    
    # Pornește server într-un thread separat
    from socketserver import ThreadingMixIn
    
    class ServerThreaded(ThreadingMixIn, HTTPServer):
        pass
    
    dir_certs = Path(__file__).parent.parent.parent / "artifacts" / "certs"
    cale_cert, cale_cheie = genereaza_certificat_autosemnat(dir_certs)
    
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(cale_cert, cale_cheie)
    
    server = ServerThreaded(("localhost", port), HandlerHTTPS)
    server.socket = ctx.wrap_socket(server.socket, server_side=True)
    
    fir_server = threading.Thread(target=server.serve_forever)
    fir_server.daemon = True
    fir_server.start()
    
    time.sleep(1)  # Așteaptă pornirea
    
    # Rulează teste
    print("  Teste CRUD:")
    print()
    
    test("GET /", "GET", "/")
    test("GET /api/resurse (gol)", "GET", "/api/resurse")
    test("POST /api/resurse", "POST", "/api/resurse", {"nume": "Test", "valoare": 42}, 201)
    test("GET /api/resurse (cu date)", "GET", "/api/resurse")
    test("GET /api/resurse/1", "GET", "/api/resurse/1")
    test("PUT /api/resurse/1", "PUT", "/api/resurse/1", {"nume": "Actualizat", "valoare": 100})
    test("DELETE /api/resurse/1", "DELETE", "/api/resurse/1")
    test("GET /api/resurse/1 (șters)", "GET", "/api/resurse/1", None, 404)
    
    # Sumar
    print()
    print("─" * 60)
    print(f"  Rezultat: {teste_trecute} trecute, {teste_esuate} eșuate")
    
    server.shutdown()
    
    return 0 if teste_esuate == 0 else 1


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Exercițiul 10.01: Server HTTPS cu REST API"
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
    args = parser.parse_args()
    
    if args.selftest:
        return ruleaza_auto_testare(args.port)
    else:
        porneste_server(args.port)
        return 0


if __name__ == "__main__":
    sys.exit(main())
