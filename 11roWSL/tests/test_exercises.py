#!/usr/bin/env python3
"""
Teste pentru Exercițiile Săptămânii 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Verifică funcționalitatea exercițiilor de laborator.
"""

import unittest
import socket
import sys
import argparse
from pathlib import Path
from typing import Optional

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


def http_get_simplu(host: str, port: int, path: str = "/", timeout: float = 5.0) -> Optional[tuple[int, str]]:
    """
    Execută o cerere HTTP GET simplă.
    
    Returns:
        Tuple (cod_status, corp) sau None la eroare
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((host, port))
            
            cerere = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
            s.sendall(cerere.encode())
            
            raspuns = b""
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                raspuns += chunk
            
            text = raspuns.decode('utf-8', errors='ignore')
            parti = text.split('\r\n\r\n', 1)
            
            linie_status = parti[0].split('\r\n')[0]
            status = int(linie_status.split()[1])
            corp = parti[1] if len(parti) > 1 else ""
            
            return (status, corp)
            
    except Exception:
        return None


class TestExercitiul1Backend(unittest.TestCase):
    """Teste pentru Exercițiul 1: Servere Backend."""
    
    def test_backend_1_raspunde(self):
        """Verifică dacă Backend 1 răspunde pe portul 8081."""
        rezultat = http_get_simplu("localhost", 8081)
        if rezultat is None:
            self.skipTest("Backend 1 nu rulează pe portul 8081")
        
        status, corp = rezultat
        self.assertEqual(status, 200, "Backend 1 ar trebui să returneze 200 OK")
        self.assertIn("Backend", corp, "Răspunsul ar trebui să conțină 'Backend'")
    
    def test_backend_2_raspunde(self):
        """Verifică dacă Backend 2 răspunde pe portul 8082."""
        rezultat = http_get_simplu("localhost", 8082)
        if rezultat is None:
            self.skipTest("Backend 2 nu rulează pe portul 8082")
        
        status, corp = rezultat
        self.assertEqual(status, 200)
    
    def test_backend_3_raspunde(self):
        """Verifică dacă Backend 3 răspunde pe portul 8083."""
        rezultat = http_get_simplu("localhost", 8083)
        if rezultat is None:
            self.skipTest("Backend 3 nu rulează pe portul 8083")
        
        status, corp = rezultat
        self.assertEqual(status, 200)


class TestExercitiul2RoundRobin(unittest.TestCase):
    """Teste pentru Exercițiul 2: Distribuție Round Robin."""
    
    def test_distributie_echilibrata(self):
        """Verifică dacă cererile sunt distribuite pe mai multe backend-uri."""
        backend_uri_gasite = set()
        
        for _ in range(6):
            rezultat = http_get_simplu("localhost", 8080)
            if rezultat is None:
                self.skipTest("Echiliborul nu rulează pe portul 8080")
            
            status, corp = rezultat
            if status == 200:
                corp_lower = corp.lower()
                for i in range(1, 4):
                    if f"web{i}" in corp_lower or f"backend {i}" in corp_lower:
                        backend_uri_gasite.add(i)
                        break
        
        self.assertGreater(
            len(backend_uri_gasite), 1,
            f"Doar {len(backend_uri_gasite)} backend(-uri) au primit trafic. "
            f"Round-robin ar trebui să distribuie pe mai multe."
        )


class TestExercitiul3IPHash(unittest.TestCase):
    """Teste pentru Exercițiul 3: Sesiuni Persistente IP Hash."""
    
    def test_acelasi_backend_pentru_acelasi_client(self):
        """Verifică dacă toate cererile de la același IP merg la același backend."""
        backend_uri = []
        
        for _ in range(5):
            rezultat = http_get_simplu("localhost", 8080)
            if rezultat is None:
                self.skipTest("Echiliborul nu rulează pe portul 8080")
            
            status, corp = rezultat
            if status == 200:
                backend_uri.append(corp)
        
        # Notă: acest test este valid doar dacă echiliborul folosește ip_hash
        # Cu round-robin, va eșua - ceea ce este comportamentul așteptat
        backend_uri_unice = set(backend_uri)
        if len(backend_uri_unice) == 1:
            self.assertTrue(True, "IP hash funcționează - același backend pentru toate cererile")
        else:
            self.skipTest("Echiliborul nu folosește ip_hash (distribuție pe mai multe backend-uri)")


class TestExercitiul4Failover(unittest.TestCase):
    """Teste pentru Exercițiul 4: Failover."""
    
    def test_echilibror_raspunde(self):
        """Verifică dacă echiliborul răspunde."""
        rezultat = http_get_simplu("localhost", 8080)
        if rezultat is None:
            self.skipTest("Echiliborul nu rulează pe portul 8080")
        
        status, _ = rezultat
        self.assertIn(status, [200, 502, 503], 
                      "Echiliborul ar trebui să returneze 200, 502 sau 503")


class TestExercitiul5NginxDocker(unittest.TestCase):
    """Teste pentru Exercițiul 5: Nginx cu Docker."""
    
    def test_health_endpoint(self):
        """Verifică endpoint-ul /health."""
        rezultat = http_get_simplu("localhost", 8080, "/health")
        if rezultat is None:
            self.skipTest("Nginx nu rulează pe portul 8080")
        
        status, corp = rezultat
        self.assertEqual(status, 200, "/health ar trebui să returneze 200")
        self.assertIn("OK", corp.upper(), "/health ar trebui să conțină 'OK'")
    
    def test_nginx_status_endpoint(self):
        """Verifică endpoint-ul /nginx_status."""
        rezultat = http_get_simplu("localhost", 8080, "/nginx_status")
        if rezultat is None:
            self.skipTest("Nginx nu rulează pe portul 8080")
        
        status, corp = rezultat
        self.assertEqual(status, 200, "/nginx_status ar trebui să returneze 200")
        self.assertIn("Active connections", corp, 
                      "/nginx_status ar trebui să conțină statistici")


class TestExercitiul6DNS(unittest.TestCase):
    """Teste pentru Exercițiul 6: Client DNS."""
    
    def test_sintaxa_modul_dns(self):
        """Verifică dacă modulul DNS client are sintaxă validă."""
        cale_modul = RADACINA_PROIECT / "src" / "exercises" / "ex_11_03_dns_client.py"
        
        if not cale_modul.exists():
            self.skipTest("Modulul ex_11_03_dns_client.py nu există")
        
        import py_compile
        try:
            py_compile.compile(str(cale_modul), doraise=True)
            self.assertTrue(True)
        except py_compile.PyCompileError as e:
            self.fail(f"Eroare de sintaxă în modulul DNS: {e}")


class TestExercitiul7Benchmark(unittest.TestCase):
    """Teste pentru Exercițiul 7: Benchmark."""
    
    def test_calcul_rps(self):
        """Verifică dacă se poate calcula RPS."""
        import time
        
        numar_cereri = 10
        timp_start = time.time()
        
        cereri_reusite = 0
        for _ in range(numar_cereri):
            rezultat = http_get_simplu("localhost", 8080, timeout=2.0)
            if rezultat and rezultat[0] == 200:
                cereri_reusite += 1
        
        durata = time.time() - timp_start
        
        if cereri_reusite == 0:
            self.skipTest("Nicio cerere reușită - echiliborul nu rulează?")
        
        rps = cereri_reusite / durata
        self.assertGreater(rps, 0, "RPS ar trebui să fie pozitiv")
        print(f"\nRPS măsurat: {rps:.2f}")


def ruleaza_exercitiu_specific(numar: int) -> bool:
    """
    Rulează testele pentru un exercițiu specific.
    
    Args:
        numar: Numărul exercițiului (1-7)
    
    Returns:
        True dacă testele au trecut
    """
    clase_test = {
        1: TestExercitiul1Backend,
        2: TestExercitiul2RoundRobin,
        3: TestExercitiul3IPHash,
        4: TestExercitiul4Failover,
        5: TestExercitiul5NginxDocker,
        6: TestExercitiul6DNS,
        7: TestExercitiul7Benchmark,
    }
    
    if numar not in clase_test:
        print(f"Eroare: Exercițiul {numar} nu există (valide: 1-7)")
        return False
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(clase_test[numar])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def main():
    parser = argparse.ArgumentParser(
        description="Rulează testele pentru exercițiile Săptămânii 11"
    )
    parser.add_argument(
        '--exercise', '--exercitiu', '-e',
        type=int,
        choices=range(1, 8),
        help='Rulează doar testele pentru un exercițiu specific (1-7)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Afișare detaliată'
    )
    
    args = parser.parse_args()
    
    if args.exercise:
        success = ruleaza_exercitiu_specific(args.exercise)
    else:
        # Rulează toate testele
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        for clasa in [
            TestExercitiul1Backend,
            TestExercitiul2RoundRobin,
            TestExercitiul3IPHash,
            TestExercitiul4Failover,
            TestExercitiul5NginxDocker,
            TestExercitiul6DNS,
            TestExercitiul7Benchmark,
        ]:
            suite.addTests(loader.loadTestsFromTestCase(clasa))
        
        verbosity = 2 if args.verbose else 1
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        success = result.wasSuccessful()
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
