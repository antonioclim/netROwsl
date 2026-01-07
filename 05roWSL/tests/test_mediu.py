#!/usr/bin/env python3
"""
Teste pentru Verificarea Mediului
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică dacă mediul de laborator este corect configurat.
"""

import subprocess
import sys
import unittest
from pathlib import Path

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class TesteMediu(unittest.TestCase):
    """Teste pentru verificarea mediului de laborator."""
    
    def test_versiune_python(self):
        """Verifică versiunea Python (minim 3.11)."""
        self.assertGreaterEqual(
            sys.version_info[:2], 
            (3, 11),
            f"Se necesită Python 3.11+, găsit {sys.version_info.major}.{sys.version_info.minor}"
        )
    
    def test_import_ipaddress(self):
        """Verifică disponibilitatea modulului ipaddress."""
        try:
            import ipaddress
            self.assertTrue(True)
        except ImportError:
            self.fail("Modulul 'ipaddress' nu este disponibil")
    
    def test_import_socket(self):
        """Verifică disponibilitatea modulului socket."""
        try:
            import socket
            self.assertTrue(True)
        except ImportError:
            self.fail("Modulul 'socket' nu este disponibil")
    
    def test_structura_proiect(self):
        """Verifică structura de directoare a proiectului."""
        directoare_necesare = [
            "src",
            "src/exercises",
            "src/utils",
            "scripts",
            "docker",
            "tests",
            "docs",
        ]
        
        for director in directoare_necesare:
            cale = RADACINA_PROIECT / director
            self.assertTrue(
                cale.exists(),
                f"Directorul '{director}' lipsește"
            )
    
    def test_fisiere_exercitii(self):
        """Verifică existența fișierelor de exerciții."""
        exercitii = [
            "src/exercises/ex_5_01_cidr_flsm.py",
            "src/exercises/ex_5_02_vlsm_ipv6.py",
            "src/exercises/ex_5_03_generator_quiz.py",
        ]
        
        for exercitiu in exercitii:
            cale = RADACINA_PROIECT / exercitiu
            self.assertTrue(
                cale.exists(),
                f"Fișierul de exercițiu '{exercitiu}' lipsește"
            )
    
    def test_fisier_docker_compose(self):
        """Verifică existența fișierului docker-compose.yml."""
        cale = RADACINA_PROIECT / "docker" / "docker-compose.yml"
        self.assertTrue(
            cale.exists(),
            "Fișierul docker-compose.yml lipsește"
        )
    
    def test_import_net_utils(self):
        """Verifică importul modulului net_utils."""
        try:
            from src.utils.net_utils import (
                analizeaza_interfata_ipv4,
                imparte_flsm,
                aloca_vlsm,
            )
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Nu s-a putut importa net_utils: {e}")


class TesteDocker(unittest.TestCase):
    """Teste pentru verificarea Docker (opționale)."""
    
    @unittest.skipIf(
        subprocess.run(["docker", "--version"], capture_output=True).returncode != 0,
        "Docker nu este disponibil"
    )
    def test_docker_instalat(self):
        """Verifică dacă Docker este instalat."""
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True
        )
        self.assertEqual(rezultat.returncode, 0)
        self.assertIn("Docker", rezultat.stdout)
    
    @unittest.skipIf(
        subprocess.run(["docker", "info"], capture_output=True).returncode != 0,
        "Daemonul Docker nu rulează"
    )
    def test_docker_activ(self):
        """Verifică dacă daemonul Docker rulează."""
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True
        )
        self.assertEqual(rezultat.returncode, 0)


def ruleaza_teste():
    """Rulează toate testele și returnează rezultatul."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Adaugă testele de mediu
    suite.addTests(loader.loadTestsFromTestCase(TesteMediu))
    suite.addTests(loader.loadTestsFromTestCase(TesteDocker))
    
    # Rulează testele
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    return len(rezultat.failures) == 0 and len(rezultat.errors) == 0


if __name__ == "__main__":
    succes = ruleaza_teste()
    sys.exit(0 if succes else 1)
