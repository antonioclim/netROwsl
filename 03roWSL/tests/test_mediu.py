#!/usr/bin/env python3
"""
Teste pentru Verificarea Mediului
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verifică că mediul Docker este configurat corect și toate serviciile funcționează.

Utilizare:
    python tests/test_mediu.py
"""

import subprocess
import socket
import sys
import unittest
from pathlib import Path


class TestMediuDocker(unittest.TestCase):
    """Teste pentru verificarea mediului Docker."""
    
    def test_docker_disponibil(self):
        """Verifică că Docker este instalat și rulează."""
        try:
            rezultat = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=30
            )
            self.assertEqual(rezultat.returncode, 0, "Docker nu este disponibil")
        except FileNotFoundError:
            self.fail("Docker nu este instalat")
        except subprocess.TimeoutExpired:
            self.fail("Docker nu răspunde (timeout)")
    
    def test_docker_compose_disponibil(self):
        """Verifică că Docker Compose este disponibil."""
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            self.assertEqual(rezultat.returncode, 0, "Docker Compose nu este disponibil")
        except Exception as e:
            self.fail(f"Eroare la verificarea Docker Compose: {e}")
    
    def test_retea_week3_exista(self):
        """Verifică că rețeaua week3_network există."""
        try:
            rezultat = subprocess.run(
                ["docker", "network", "inspect", "week3_network"],
                capture_output=True,
                timeout=10
            )
            # Rețeaua poate să nu existe încă, nu e o eroare critică
            if rezultat.returncode != 0:
                self.skipTest("Rețeaua week3_network nu există încă (se creează la pornire)")
        except Exception as e:
            self.skipTest(f"Nu s-a putut verifica rețeaua: {e}")


class TestServicii(unittest.TestCase):
    """Teste pentru verificarea serviciilor."""
    
    def test_container_server_ruleaza(self):
        """Verifică că containerul server rulează."""
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", "week3_server"],
                capture_output=True,
                timeout=10
            )
            if "true" not in rezultat.stdout.decode().lower():
                self.skipTest("Containerul week3_server nu rulează")
        except Exception:
            self.skipTest("Nu s-a putut verifica containerul server")
    
    def test_container_router_ruleaza(self):
        """Verifică că containerul router rulează."""
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", "week3_router"],
                capture_output=True,
                timeout=10
            )
            if "true" not in rezultat.stdout.decode().lower():
                self.skipTest("Containerul week3_router nu rulează")
        except Exception:
            self.skipTest("Nu s-a putut verifica containerul router")
    
    def test_container_client_ruleaza(self):
        """Verifică că containerul client rulează."""
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", "week3_client"],
                capture_output=True,
                timeout=10
            )
            if "true" not in rezultat.stdout.decode().lower():
                self.skipTest("Containerul week3_client nu rulează")
        except Exception:
            self.skipTest("Nu s-a putut verifica containerul client")


class TestConectivitate(unittest.TestCase):
    """Teste pentru verificarea conectivității."""
    
    def _verifica_port(self, host: str, port: int) -> bool:
        """Verifică dacă un port este deschis."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            rezultat = sock.connect_ex((host, port))
            sock.close()
            return rezultat == 0
        except Exception:
            return False
    
    def test_server_echo_raspunde(self):
        """Verifică că serverul echo răspunde pe portul 8080."""
        if not self._verifica_port("localhost", 8080):
            self.skipTest("Serverul echo nu răspunde (laboratorul nu este pornit?)")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 8080))
            sock.sendall(b"test")
            raspuns = sock.recv(1024)
            sock.close()
            self.assertEqual(raspuns, b"test", "Serverul echo nu a returnat datele corect")
        except Exception as e:
            self.fail(f"Eroare la testarea serverului echo: {e}")
    
    def test_tunel_tcp_raspunde(self):
        """Verifică că tunelul TCP răspunde pe portul 9090."""
        if not self._verifica_port("localhost", 9090):
            self.skipTest("Tunelul TCP nu răspunde (laboratorul nu este pornit?)")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9090))
            sock.sendall(b"test prin tunel")
            raspuns = sock.recv(1024)
            sock.close()
            self.assertEqual(raspuns, b"test prin tunel", "Tunelul nu a redirecționat corect")
        except Exception as e:
            self.fail(f"Eroare la testarea tunelului: {e}")


class TestCapabilitatiRetea(unittest.TestCase):
    """Teste pentru capabilitățile de rețea."""
    
    def test_socket_broadcast(self):
        """Verifică că se pot crea socket-uri broadcast."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.close()
        except Exception as e:
            self.fail(f"Nu se pot crea socket-uri broadcast: {e}")
    
    def test_socket_multicast(self):
        """Verifică că se pot crea socket-uri multicast."""
        try:
            import struct
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            mreq = struct.pack(
                '4s4s',
                socket.inet_aton('239.0.0.1'),
                socket.inet_aton('0.0.0.0')
            )
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.close()
        except Exception as e:
            self.skipTest(f"Multicast nu este suportat: {e}")


def main():
    """Punct de intrare principal."""
    print("=" * 60)
    print("Teste Mediu - Săptămâna 3")
    print("Rețele de Calculatoare - ASE, Informatică Economică")
    print("=" * 60)
    print()
    
    # Configurează unittest pentru output detaliat
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adaugă toate clasele de test
    suite.addTests(loader.loadTestsFromTestCase(TestMediuDocker))
    suite.addTests(loader.loadTestsFromTestCase(TestServicii))
    suite.addTests(loader.loadTestsFromTestCase(TestConectivitate))
    suite.addTests(loader.loadTestsFromTestCase(TestCapabilitatiRetea))
    
    # Rulează testele
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    # Returnează codul de ieșire
    return 0 if rezultat.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())
