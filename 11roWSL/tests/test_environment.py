#!/usr/bin/env python3
"""
Teste pentru Mediul de Laborator
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Verifică dacă mediul este configurat corect pentru laborator.
"""

import unittest
import subprocess
import shutil
import socket
import sys
from pathlib import Path


class TestMediuPython(unittest.TestCase):
    """Teste pentru mediul Python."""
    
    def test_versiune_python(self):
        """Verifică versiunea Python >= 3.11."""
        versiune = sys.version_info
        self.assertGreaterEqual(
            (versiune.major, versiune.minor),
            (3, 11),
            f"Se necesită Python 3.11+, găsit {versiune.major}.{versiune.minor}"
        )
    
    def test_pachet_requests(self):
        """Verifică dacă requests este instalat."""
        try:
            import requests
            self.assertTrue(True)
        except ImportError:
            self.fail("Pachetul 'requests' nu este instalat")
    
    def test_pachet_yaml(self):
        """Verifică dacă PyYAML este instalat."""
        try:
            import yaml
            self.assertTrue(True)
        except ImportError:
            self.fail("Pachetul 'pyyaml' nu este instalat")


class TestMediuDocker(unittest.TestCase):
    """Teste pentru mediul Docker."""
    
    def test_docker_instalat(self):
        """Verifică dacă Docker este instalat."""
        docker = shutil.which("docker")
        self.assertIsNotNone(docker, "Docker nu este instalat sau nu este în PATH")
    
    def test_docker_ruleaza(self):
        """Verifică dacă daemon-ul Docker rulează."""
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        self.assertEqual(
            result.returncode, 0,
            "Daemon-ul Docker nu rulează. Porniți Docker Desktop."
        )
    
    def test_docker_compose_disponibil(self):
        """Verifică dacă Docker Compose este disponibil."""
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        self.assertEqual(
            result.returncode, 0,
            "Docker Compose nu este disponibil"
        )


class TestDisponibilitatePorturi(unittest.TestCase):
    """Teste pentru disponibilitatea porturilor."""
    
    def _verifica_port_disponibil(self, port: int) -> bool:
        """Verifică dacă un port este disponibil."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return True
        except OSError:
            return False
    
    def test_port_8080_disponibil(self):
        """Verifică dacă portul 8080 este disponibil."""
        if not self._verifica_port_disponibil(8080):
            self.skipTest("Portul 8080 este în uz (poate fi echiliborul în funcțiune)")
    
    def test_porturi_backend_disponibile(self):
        """Verifică dacă porturile backend sunt disponibile."""
        porturi_ocupate = []
        for port in [8081, 8082, 8083]:
            if not self._verifica_port_disponibil(port):
                porturi_ocupate.append(port)
        
        if porturi_ocupate:
            self.skipTest(f"Porturi ocupate: {porturi_ocupate} (poate sunt backend-urile)")


class TestStructuraDirectoare(unittest.TestCase):
    """Teste pentru structura directoarelor."""
    
    @classmethod
    def setUpClass(cls):
        cls.radacina = Path(__file__).parent.parent
    
    def test_director_docker_exista(self):
        """Verifică dacă directorul docker/ există."""
        self.assertTrue(
            (self.radacina / "docker").exists(),
            "Directorul 'docker/' lipsește"
        )
    
    def test_docker_compose_exista(self):
        """Verifică dacă docker-compose.yml există."""
        self.assertTrue(
            (self.radacina / "docker" / "docker-compose.yml").exists(),
            "Fișierul 'docker/docker-compose.yml' lipsește"
        )
    
    def test_director_scripts_exista(self):
        """Verifică dacă directorul scripts/ există."""
        self.assertTrue(
            (self.radacina / "scripts").exists(),
            "Directorul 'scripts/' lipsește"
        )
    
    def test_director_src_exista(self):
        """Verifică dacă directorul src/ există."""
        self.assertTrue(
            (self.radacina / "src").exists(),
            "Directorul 'src/' lipsește"
        )


def ruleaza_toate_testele():
    """Rulează toate testele și returnează rezultatul."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adaugă toate clasele de test
    suite.addTests(loader.loadTestsFromTestCase(TestMediuPython))
    suite.addTests(loader.loadTestsFromTestCase(TestMediuDocker))
    suite.addTests(loader.loadTestsFromTestCase(TestDisponibilitatePorturi))
    suite.addTests(loader.loadTestsFromTestCase(TestStructuraDirectoare))
    
    # Rulează testele
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = ruleaza_toate_testele()
    sys.exit(0 if success else 1)
