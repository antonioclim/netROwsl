#!/usr/bin/env python3
"""
Teste pentru Verificarea Exercițiilor
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Verifică dacă exercițiile de laborator au fost completate corect.
"""

import sys
import json
import socket
import argparse
from pathlib import Path

import pytest

# Adăugare rădăcină proiect în PATH
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


def verifica_port(port: int, timeout: float = 2.0) -> bool:
    """Verifică dacă un serviciu rulează pe un port."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            rezultat = s.connect_ex(('localhost', port))
            return rezultat == 0
    except Exception:
        return False


# Markere pentru a sări testele dacă serviciile nu rulează
necesita_smtp = pytest.mark.skipif(
    not verifica_port(1025),
    reason="Serverul SMTP nu rulează pe portul 1025"
)

necesita_jsonrpc = pytest.mark.skipif(
    not verifica_port(6200),
    reason="Serverul JSON-RPC nu rulează pe portul 6200"
)

necesita_xmlrpc = pytest.mark.skipif(
    not verifica_port(6201),
    reason="Serverul XML-RPC nu rulează pe portul 6201"
)

necesita_grpc = pytest.mark.skipif(
    not verifica_port(6251),
    reason="Serverul gRPC nu rulează pe portul 6251"
)


class TestExercitiuSMTP:
    """Teste pentru Exercițiul 1: Dialog SMTP."""
    
    @necesita_smtp
    def test_conectare_smtp(self):
        """Testează conectarea la serverul SMTP."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('localhost', 1025))
            raspuns = s.recv(1024).decode()
            assert raspuns.startswith('220'), \
                f"Banner SMTP invalid: {raspuns}"
    
    @necesita_smtp
    def test_helo(self):
        """Testează comanda HELO."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect(('localhost', 1025))
            s.recv(1024)  # Ignorăm banner-ul
            
            s.send(b"HELO test.local\r\n")
            raspuns = s.recv(1024).decode()
            assert raspuns.startswith('250'), \
                f"Răspuns HELO invalid: {raspuns}"
    
    @necesita_smtp
    def test_tranzactie_completa(self):
        """Testează o tranzacție SMTP completă."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)
            s.connect(('localhost', 1025))
            
            # Banner
            raspuns = s.recv(1024).decode()
            assert '220' in raspuns
            
            # HELO
            s.send(b"HELO test.local\r\n")
            raspuns = s.recv(1024).decode()
            assert '250' in raspuns
            
            # MAIL FROM
            s.send(b"MAIL FROM:<test@pytest.local>\r\n")
            raspuns = s.recv(1024).decode()
            assert '250' in raspuns
            
            # RCPT TO
            s.send(b"RCPT TO:<destinatar@pytest.local>\r\n")
            raspuns = s.recv(1024).decode()
            assert '250' in raspuns
            
            # DATA
            s.send(b"DATA\r\n")
            raspuns = s.recv(1024).decode()
            assert '354' in raspuns
            
            # Conținut mesaj
            mesaj = b"Subject: Test Pytest\r\n\r\nAcesta este un test.\r\n.\r\n"
            s.send(mesaj)
            raspuns = s.recv(1024).decode()
            assert '250' in raspuns
            
            # QUIT
            s.send(b"QUIT\r\n")
            raspuns = s.recv(1024).decode()
            assert '221' in raspuns


class TestExercitiuJSONRPC:
    """Teste pentru Exercițiul 2: Apeluri JSON-RPC."""
    
    def _apel_jsonrpc(self, metoda: str, parametri=None, id: int = 1):
        """Helper pentru apeluri JSON-RPC."""
        import urllib.request
        
        cerere = {
            "jsonrpc": "2.0",
            "method": metoda,
            "id": id
        }
        if parametri is not None:
            cerere["params"] = parametri
        
        req = urllib.request.Request(
            "http://localhost:6200",
            data=json.dumps(cerere).encode(),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as raspuns:
            return json.loads(raspuns.read())
    
    @necesita_jsonrpc
    def test_adunare(self):
        """Testează metoda add."""
        rezultat = self._apel_jsonrpc("add", [10, 20])
        assert "result" in rezultat
        assert rezultat["result"] == 30
    
    @necesita_jsonrpc
    def test_scadere(self):
        """Testează metoda subtract."""
        rezultat = self._apel_jsonrpc("subtract", [100, 42])
        assert "result" in rezultat
        assert rezultat["result"] == 58
    
    @necesita_jsonrpc
    def test_inmultire(self):
        """Testează metoda multiply."""
        rezultat = self._apel_jsonrpc("multiply", [7, 8])
        assert "result" in rezultat
        assert rezultat["result"] == 56
    
    @necesita_jsonrpc
    def test_impartire(self):
        """Testează metoda divide."""
        rezultat = self._apel_jsonrpc("divide", [100, 4])
        assert "result" in rezultat
        assert rezultat["result"] == 25
    
    @necesita_jsonrpc
    def test_parametri_numiti(self):
        """Testează apel cu parametri numiți."""
        rezultat = self._apel_jsonrpc("subtract", {"a": 50, "b": 10})
        assert "result" in rezultat
        assert rezultat["result"] == 40
    
    @necesita_jsonrpc
    def test_apel_batch(self):
        """Testează apeluri în lot (batch)."""
        import urllib.request
        
        cereri = [
            {"jsonrpc": "2.0", "method": "add", "params": [1, 2], "id": 1},
            {"jsonrpc": "2.0", "method": "multiply", "params": [3, 4], "id": 2}
        ]
        
        req = urllib.request.Request(
            "http://localhost:6200",
            data=json.dumps(cereri).encode(),
            headers={"Content-Type": "application/json"}
        )
        
        with urllib.request.urlopen(req, timeout=10) as raspuns:
            rezultate = json.loads(raspuns.read())
        
        assert len(rezultate) == 2
        assert rezultate[0]["result"] == 3
        assert rezultate[1]["result"] == 12
    
    @necesita_jsonrpc
    def test_eroare_metoda_inexistenta(self):
        """Testează eroare pentru metodă inexistentă."""
        import urllib.request
        
        try:
            rezultat = self._apel_jsonrpc("metoda_care_nu_exista", [])
            if "error" in rezultat:
                assert rezultat["error"]["code"] == -32601
        except urllib.error.HTTPError:
            pass  # Unele servere returnează HTTP 500


class TestExercitiuXMLRPC:
    """Teste pentru Exercițiul 3: Apeluri XML-RPC."""
    
    @necesita_xmlrpc
    def test_adunare(self):
        """Testează metoda add prin XML-RPC."""
        import xmlrpc.client
        proxy = xmlrpc.client.ServerProxy("http://localhost:6201")
        rezultat = proxy.add(10, 20)
        assert rezultat == 30
    
    @necesita_xmlrpc
    def test_inmultire(self):
        """Testează metoda multiply prin XML-RPC."""
        import xmlrpc.client
        proxy = xmlrpc.client.ServerProxy("http://localhost:6201")
        rezultat = proxy.multiply(7, 8)
        assert rezultat == 56
    
    @necesita_xmlrpc
    def test_introspectie_list_methods(self):
        """Testează introspecția system.listMethods."""
        import xmlrpc.client
        proxy = xmlrpc.client.ServerProxy("http://localhost:6201")
        metode = proxy.system.listMethods()
        assert isinstance(metode, list)
        assert len(metode) > 0
    
    @necesita_xmlrpc
    def test_introspectie_method_help(self):
        """Testează introspecția system.methodHelp."""
        import xmlrpc.client
        proxy = xmlrpc.client.ServerProxy("http://localhost:6201")
        try:
            ajutor = proxy.system.methodHelp("add")
            assert isinstance(ajutor, str)
        except xmlrpc.client.Fault:
            pytest.skip("system.methodHelp nu este implementat")


class TestExercitiuGRPC:
    """Teste pentru Exercițiul 4: Apeluri gRPC."""
    
    @necesita_grpc
    def test_import_stub_grpc(self):
        """Testează dacă stub-urile gRPC pot fi importate."""
        try:
            sys.path.insert(0, str(RADACINA_PROIECT / "src" / "apps" / "rpc" / "grpc"))
            import calculator_pb2
            import calculator_pb2_grpc
            assert True
        except ImportError as e:
            pytest.fail(f"Nu s-au putut importa stub-urile gRPC: {e}")
    
    @necesita_grpc
    def test_conectare_grpc(self):
        """Testează conectarea la serverul gRPC."""
        import grpc
        sys.path.insert(0, str(RADACINA_PROIECT / "src" / "apps" / "rpc" / "grpc"))
        import calculator_pb2
        import calculator_pb2_grpc
        
        canal = grpc.insecure_channel("localhost:6251")
        stub = calculator_pb2_grpc.CalculatorServiceStub(canal)
        
        # Test simplu de adunare
        cerere = calculator_pb2.BinaryOpRequest(a=10, b=20)
        raspuns = stub.Add(cerere)
        
        assert raspuns.result == 30
        canal.close()


def ruleaza_exercitiu(numar: int):
    """Rulează testele pentru un exercițiu specific."""
    clase_exercitii = {
        1: "TestExercitiuSMTP",
        2: "TestExercitiuJSONRPC",
        3: "TestExercitiuXMLRPC",
        4: "TestExercitiuGRPC"
    }
    
    if numar not in clase_exercitii:
        print(f"Exercițiu invalid: {numar}. Alegeți între 1-4.")
        return 1
    
    clasa = clase_exercitii[numar]
    return pytest.main([__file__, "-v", "-k", clasa])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verificare exerciții Săptămâna 12"
    )
    parser.add_argument(
        "--exercitiu", "-e",
        type=int,
        choices=[1, 2, 3, 4],
        help="Numărul exercițiului de verificat (1-4)"
    )
    args = parser.parse_args()
    
    if args.exercitiu:
        sys.exit(ruleaza_exercitiu(args.exercitiu))
    else:
        sys.exit(pytest.main([__file__, "-v"]))
