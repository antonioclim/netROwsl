#!/usr/bin/env python3
"""
Teste pentru Mediul de Laborator
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Validează configurarea mediului pentru Săptămâna 9.
"""

import subprocess
import sys
import socket
import shutil
import unittest
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class TestMediuPython(unittest.TestCase):
    """Teste pentru mediul Python."""
    
    def test_versiune_python(self):
        """Verifică versiunea Python >= 3.8."""
        versiune = sys.version_info
        self.assertGreaterEqual(
            (versiune.major, versiune.minor),
            (3, 8),
            f"Se necesită Python 3.8+, găsit {versiune.major}.{versiune.minor}"
        )
    
    def test_modul_struct(self):
        """Verifică disponibilitatea modulului struct."""
        import struct
        self.assertIsNotNone(struct)
    
    def test_modul_socket(self):
        """Verifică disponibilitatea modulului socket."""
        import socket
        self.assertIsNotNone(socket)
    
    def test_modul_zlib(self):
        """Verifică disponibilitatea modulului zlib."""
        import zlib
        self.assertIsNotNone(zlib)
    
    def test_modul_ftplib(self):
        """Verifică disponibilitatea modulului ftplib."""
        from ftplib import FTP
        self.assertIsNotNone(FTP)


class TestMediuDocker(unittest.TestCase):
    """Teste pentru mediul Docker."""
    
    def test_docker_instalat(self):
        """Verifică dacă Docker este instalat."""
        docker_path = shutil.which("docker")
        self.assertIsNotNone(
            docker_path,
            "Docker nu este instalat sau nu este în PATH"
        )
    
    def test_docker_ruleaza(self):
        """Verifică dacă daemon-ul Docker rulează."""
        try:
            rezultat = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                timeout=10
            )
            self.assertEqual(
                rezultat.returncode, 0,
                "Daemon-ul Docker nu rulează. Porniți Docker Desktop."
            )
        except subprocess.TimeoutExpired:
            self.fail("Docker info a expirat - daemon-ul poate să nu răspundă")
        except FileNotFoundError:
            self.fail("Comanda docker nu a fost găsită")
    
    def test_docker_compose_disponibil(self):
        """Verifică disponibilitatea Docker Compose."""
        # Încearcă v2
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                return
        except Exception:
            pass
        
        # Încearcă v1
        try:
            rezultat = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                return
        except Exception:
            pass
        
        self.fail("Docker Compose nu este disponibil")


class TestStructuraProiect(unittest.TestCase):
    """Teste pentru structura proiectului."""
    
    def test_director_docker(self):
        """Verifică existența directorului docker."""
        director = RADACINA_PROIECT / "docker"
        self.assertTrue(
            director.exists(),
            f"Directorul docker lipsește: {director}"
        )
    
    def test_docker_compose_yml(self):
        """Verifică existența fișierului docker-compose.yml."""
        fisier = RADACINA_PROIECT / "docker" / "docker-compose.yml"
        self.assertTrue(
            fisier.exists(),
            f"Fișierul docker-compose.yml lipsește: {fisier}"
        )
    
    def test_director_scripturi(self):
        """Verifică existența directorului scripts."""
        director = RADACINA_PROIECT / "scripts"
        self.assertTrue(
            director.exists(),
            f"Directorul scripts lipsește: {director}"
        )
    
    def test_director_exercitii(self):
        """Verifică existența directorului exercises."""
        director = RADACINA_PROIECT / "src" / "exercises"
        self.assertTrue(
            director.exists(),
            f"Directorul exercises lipsește: {director}"
        )


class TestCapabilitatiRetea(unittest.TestCase):
    """Teste pentru capabilitățile de rețea."""
    
    def test_rezolvare_localhost(self):
        """Verifică rezolvarea localhost."""
        try:
            ip = socket.gethostbyname("localhost")
            self.assertIn(
                ip,
                ["127.0.0.1", "::1"],
                f"Rezolvare localhost neașteptată: {ip}"
            )
        except socket.gaierror:
            self.fail("Nu se poate rezolva localhost")
    
    def test_creare_socket_tcp(self):
        """Verifică posibilitatea creării unui socket TCP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                self.assertIsNotNone(s)
        except Exception as e:
            self.fail(f"Nu se poate crea socket TCP: {e}")
    
    def test_creare_socket_udp(self):
        """Verifică posibilitatea creării unui socket UDP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                self.assertIsNotNone(s)
        except Exception as e:
            self.fail(f"Nu se poate crea socket UDP: {e}")


def ruleaza_teste():
    """Rulează toate testele și returnează rezultatul."""
    print("=" * 60)
    print("Teste Validare Mediu - Săptămâna 9")
    print("=" * 60)
    print()
    
    # Creează suite de teste
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adaugă clasele de teste
    suite.addTests(loader.loadTestsFromTestCase(TestMediuPython))
    suite.addTests(loader.loadTestsFromTestCase(TestMediuDocker))
    suite.addTests(loader.loadTestsFromTestCase(TestStructuraProiect))
    suite.addTests(loader.loadTestsFromTestCase(TestCapabilitatiRetea))
    
    # Rulează testele
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    return len(rezultat.failures) == 0 and len(rezultat.errors) == 0


if __name__ == "__main__":
    succes = ruleaza_teste()
    sys.exit(0 if succes else 1)
