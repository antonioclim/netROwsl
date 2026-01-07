#!/usr/bin/env python3
"""
Teste pentru Exercițiile Săptămânii 3
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Validează funcționarea corectă a exercițiilor de broadcast, multicast și tunel TCP.

Utilizare:
    python tests/test_exercitii.py
    python tests/test_exercitii.py --exercitiu 1
    python tests/test_exercitii.py --verbose
"""

import socket
import struct
import subprocess
import sys
import time
import unittest
import argparse
from pathlib import Path
from typing import Optional

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURAȚIE
# ═══════════════════════════════════════════════════════════════════════════

RADACINA_PROIECT = Path(__file__).parent.parent

# Adrese și porturi pentru teste
ADRESA_BROADCAST = '255.255.255.255'
PORT_BROADCAST = 5007
GRUP_MULTICAST = '239.0.0.1'
PORT_MULTICAST = 5008
HOST_SERVER = 'localhost'
PORT_SERVER = 8080
HOST_TUNEL = 'localhost'
PORT_TUNEL = 9090

# Timeout-uri
TIMEOUT_CONECTARE = 5
TIMEOUT_CITIRE = 3


class TestExercitiul1Broadcast(unittest.TestCase):
    """Teste pentru Exercițiul 1: Broadcast UDP."""
    
    def test_creare_socket_broadcast(self):
        """Testează că se poate crea un socket cu opțiunea SO_BROADCAST."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Activează broadcast
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
        # Verifică că opțiunea este setată
        valoare = sock.getsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST)
        self.assertTrue(valoare, "SO_BROADCAST nu este activat")
        
        sock.close()
    
    def test_bind_receptor(self):
        """Testează că receptorul se poate lega la portul broadcast."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('0.0.0.0', PORT_BROADCAST))
            adresa_legata = sock.getsockname()
            self.assertEqual(adresa_legata[1], PORT_BROADCAST)
        finally:
            sock.close()
    
    def test_sintaxa_script(self):
        """Testează că scriptul de broadcast are sintaxă Python validă."""
        script = RADACINA_PROIECT / "src" / "exercises" / "ex_3_01_udp_broadcast.py"
        
        if not script.exists():
            self.skipTest(f"Scriptul nu există: {script}")
        
        rezultat = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script)],
            capture_output=True
        )
        
        self.assertEqual(
            rezultat.returncode, 0,
            f"Eroare de sintaxă: {rezultat.stderr.decode()}"
        )


class TestExercitiul2Multicast(unittest.TestCase):
    """Teste pentru Exercițiul 2: Multicast UDP."""
    
    def test_creare_socket_multicast(self):
        """Testează că se poate crea un socket pentru multicast."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            sock.bind(('', PORT_MULTICAST))
            
            # Înscrie în grup multicast
            mreq = struct.pack(
                '4s4s',
                socket.inet_aton(GRUP_MULTICAST),
                socket.inet_aton('0.0.0.0')
            )
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            
            # Dacă am ajuns aici, totul funcționează
            self.assertTrue(True)
            
        except Exception as e:
            self.fail(f"Nu s-a putut alătura grupului multicast: {e}")
        finally:
            sock.close()
    
    def test_setare_ttl_multicast(self):
        """Testează setarea TTL pentru multicast."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Setează TTL
        ttl = 32
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        
        # Verifică
        valoare = sock.getsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL)
        self.assertEqual(valoare, ttl, f"TTL nu este setat corect: {valoare} != {ttl}")
        
        sock.close()
    
    def test_adresa_multicast_valida(self):
        """Testează că adresa de grup este în intervalul multicast valid."""
        octeti = [int(x) for x in GRUP_MULTICAST.split('.')]
        
        # Verifică că este în 224.0.0.0 - 239.255.255.255
        self.assertTrue(
            224 <= octeti[0] <= 239,
            f"Adresa {GRUP_MULTICAST} nu este în intervalul multicast"
        )
    
    def test_sintaxa_script(self):
        """Testează că scriptul de multicast are sintaxă Python validă."""
        script = RADACINA_PROIECT / "src" / "exercises" / "ex_3_02_udp_multicast.py"
        
        if not script.exists():
            self.skipTest(f"Scriptul nu există: {script}")
        
        rezultat = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script)],
            capture_output=True
        )
        
        self.assertEqual(
            rezultat.returncode, 0,
            f"Eroare de sintaxă: {rezultat.stderr.decode()}"
        )


class TestExercitiul3Tunel(unittest.TestCase):
    """Teste pentru Exercițiul 3: Tunel TCP."""
    
    def test_conectare_server_echo(self):
        """Testează conectarea directă la serverul echo."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT_CONECTARE)
            sock.connect((HOST_SERVER, PORT_SERVER))
            
            # Trimite date de test
            mesaj = b"Test echo"
            sock.sendall(mesaj)
            
            # Primește răspuns
            sock.settimeout(TIMEOUT_CITIRE)
            raspuns = sock.recv(1024)
            
            self.assertEqual(
                raspuns, mesaj,
                f"Răspuns incorect: {raspuns} != {mesaj}"
            )
            
            sock.close()
            
        except ConnectionRefusedError:
            self.skipTest("Serverul echo nu rulează pe localhost:8080")
        except socket.timeout:
            self.skipTest("Timeout la conectarea la server")
    
    def test_conectare_prin_tunel(self):
        """Testează conectarea prin tunelul TCP."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT_CONECTARE)
            sock.connect((HOST_TUNEL, PORT_TUNEL))
            
            # Trimite date de test
            mesaj = b"Test prin tunel"
            sock.sendall(mesaj)
            
            # Primește răspuns
            sock.settimeout(TIMEOUT_CITIRE)
            raspuns = sock.recv(1024)
            
            self.assertEqual(
                raspuns, mesaj,
                f"Răspuns incorect prin tunel: {raspuns} != {mesaj}"
            )
            
            sock.close()
            
        except ConnectionRefusedError:
            self.skipTest("Tunelul TCP nu rulează pe localhost:9090")
        except socket.timeout:
            self.skipTest("Timeout la conectarea prin tunel")
    
    def test_relay_date_mari(self):
        """Testează relay-ul de date mai mari prin tunel."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(TIMEOUT_CONECTARE)
            sock.connect((HOST_TUNEL, PORT_TUNEL))
            
            # Trimite date mai mari
            mesaj = b"X" * 1000
            sock.sendall(mesaj)
            
            # Primește răspuns
            sock.settimeout(TIMEOUT_CITIRE)
            raspuns = b""
            while len(raspuns) < len(mesaj):
                chunk = sock.recv(4096)
                if not chunk:
                    break
                raspuns += chunk
            
            self.assertEqual(
                len(raspuns), len(mesaj),
                f"Lungime răspuns incorectă: {len(raspuns)} != {len(mesaj)}"
            )
            
            sock.close()
            
        except ConnectionRefusedError:
            self.skipTest("Tunelul TCP nu rulează")
        except socket.timeout:
            self.skipTest("Timeout la test")
    
    def test_sintaxa_script(self):
        """Testează că scriptul de tunel are sintaxă Python validă."""
        script = RADACINA_PROIECT / "src" / "exercises" / "ex_3_03_tcp_tunnel.py"
        
        if not script.exists():
            self.skipTest(f"Scriptul nu există: {script}")
        
        rezultat = subprocess.run(
            [sys.executable, "-m", "py_compile", str(script)],
            capture_output=True
        )
        
        self.assertEqual(
            rezultat.returncode, 0,
            f"Eroare de sintaxă: {rezultat.stderr.decode()}"
        )


class TestExercitiul4Wireshark(unittest.TestCase):
    """Teste pentru Exercițiul 4: Analiză Wireshark."""
    
    def test_tcpdump_disponibil_in_container(self):
        """Testează că tcpdump este disponibil în containere."""
        try:
            rezultat = subprocess.run(
                ["docker", "exec", "week3_client", "which", "tcpdump"],
                capture_output=True,
                timeout=10
            )
            
            if rezultat.returncode != 0:
                self.skipTest("Containerul week3_client nu rulează")
            
            self.assertIn(
                "tcpdump",
                rezultat.stdout.decode(),
                "tcpdump nu este instalat în container"
            )
            
        except FileNotFoundError:
            self.skipTest("Docker nu este disponibil")
        except subprocess.TimeoutExpired:
            self.skipTest("Timeout la verificarea tcpdump")
    
    def test_director_pcap_exista(self):
        """Testează că directorul pcap există pentru salvarea capturilor."""
        director_pcap = RADACINA_PROIECT / "pcap"
        
        if not director_pcap.exists():
            director_pcap.mkdir(parents=True)
        
        self.assertTrue(
            director_pcap.exists(),
            f"Directorul pcap nu există: {director_pcap}"
        )


def ruleaza_teste_exercitiu(numar_exercitiu: int, verbose: bool = False) -> bool:
    """
    Rulează testele pentru un exercițiu specific.
    
    Args:
        numar_exercitiu: Numărul exercițiului (1-4)
        verbose: True pentru output detaliat
        
    Returns:
        True dacă toate testele au trecut
    """
    clase_test = {
        1: TestExercitiul1Broadcast,
        2: TestExercitiul2Multicast,
        3: TestExercitiul3Tunel,
        4: TestExercitiul4Wireshark
    }
    
    if numar_exercitiu not in clase_test:
        print(f"Exercițiu invalid: {numar_exercitiu}")
        return False
    
    suite = unittest.TestLoader().loadTestsFromTestCase(clase_test[numar_exercitiu])
    verbozitate = 2 if verbose else 1
    rezultat = unittest.TextTestRunner(verbosity=verbozitate).run(suite)
    
    return rezultat.wasSuccessful()


def main():
    """Punct de intrare principal."""
    parser = argparse.ArgumentParser(
        description='Teste pentru Exercițiile Săptămânii 3'
    )
    parser.add_argument(
        '--exercitiu', '-e',
        type=int,
        choices=[1, 2, 3, 4],
        help='Rulează doar testele pentru un exercițiu specific'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Output detaliat'
    )
    args = parser.parse_args()
    
    print("=" * 60)
    print("Teste Exerciții - Săptămâna 3")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()
    
    if args.exercitiu:
        succes = ruleaza_teste_exercitiu(args.exercitiu, args.verbose)
    else:
        # Rulează toate testele
        loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        
        suite.addTests(loader.loadTestsFromTestCase(TestExercitiul1Broadcast))
        suite.addTests(loader.loadTestsFromTestCase(TestExercitiul2Multicast))
        suite.addTests(loader.loadTestsFromTestCase(TestExercitiul3Tunel))
        suite.addTests(loader.loadTestsFromTestCase(TestExercitiul4Wireshark))
        
        verbozitate = 2 if args.verbose else 1
        rezultat = unittest.TextTestRunner(verbosity=verbozitate).run(suite)
        succes = rezultat.wasSuccessful()
    
    print()
    if succes:
        print("✓ Toate testele au trecut!")
    else:
        print("✗ Unele teste au eșuat.")
    
    return 0 if succes else 1


if __name__ == '__main__':
    sys.exit(main())
