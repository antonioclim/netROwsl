#!/usr/bin/env python3
"""
Teste pentru Modulele Utilitare
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Verifică funcționalitatea modulelor din scripts/utils/.
"""

import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

RADACINA = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA))

from scripts.utils.utilitare_docker import (
    ManagerDocker,
    verifica_docker_instalat,
    verifica_docker_activ,
)
from scripts.utils.logger import configureaza_logger


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Logger
# ═══════════════════════════════════════════════════════════════════════════════

class TesteLogger(unittest.TestCase):
    """Teste pentru modulul logger."""
    
    def test_configureaza_logger_returneaza_logger(self):
        """Verifică că funcția returnează un logger valid."""
        logger = configureaza_logger("test")
        self.assertIsNotNone(logger)
        self.assertEqual(logger.name, "test")
    
    def test_logger_nivele(self):
        """Verifică că logger-ul suportă toate nivelele."""
        logger = configureaza_logger("test_nivele")
        # Nu ar trebui să ridice excepții
        logger.debug("debug message")
        logger.info("info message")
        logger.warning("warning message")
        logger.error("error message")
    
    def test_logger_nume_diferite(self):
        """Verifică că logger-uri cu nume diferite sunt diferite."""
        logger1 = configureaza_logger("modul1")
        logger2 = configureaza_logger("modul2")
        self.assertNotEqual(logger1.name, logger2.name)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Docker Manager
# ═══════════════════════════════════════════════════════════════════════════════

class TesteDockerManager(unittest.TestCase):
    """Teste pentru ManagerDocker."""
    
    def setUp(self):
        """Configurare pentru teste."""
        self.director_test = Path("/tmp/test_docker")
        self.director_test.mkdir(exist_ok=True)
        
        # Creează fișier compose mock
        self.compose_file = self.director_test / "docker-compose.yml"
        self.compose_file.write_text("version: '3'\nservices: {}")
    
    def tearDown(self):
        """Curățare după teste."""
        if self.compose_file.exists():
            self.compose_file.unlink()
        if self.director_test.exists():
            self.director_test.rmdir()
    
    @patch('subprocess.run')
    def test_compose_up_succes(self, mock_run):
        """Testează compose_up cu rezultat de succes."""
        mock_run.return_value = MagicMock(returncode=0)
        
        manager = ManagerDocker(self.director_test)
        rezultat = manager.compose_up(detasat=True)
        
        self.assertTrue(rezultat)
        mock_run.assert_called()
    
    @patch('subprocess.run')
    def test_compose_up_esec(self, mock_run):
        """Testează compose_up cu rezultat de eșec."""
        mock_run.return_value = MagicMock(returncode=1)
        
        manager = ManagerDocker(self.director_test)
        rezultat = manager.compose_up(detasat=True)
        
        self.assertFalse(rezultat)
    
    @patch('subprocess.run')
    def test_compose_down_cu_volume(self, mock_run):
        """Testează compose_down cu ștergere volume."""
        mock_run.return_value = MagicMock(returncode=0)
        
        manager = ManagerDocker(self.director_test)
        rezultat = manager.compose_down(volume=True)
        
        self.assertTrue(rezultat)
        call_args = mock_run.call_args[0][0]
        self.assertIn("-v", call_args)
    
    @patch('subprocess.run')
    def test_compose_down_simulare(self, mock_run):
        """Testează compose_down în mod simulare."""
        manager = ManagerDocker(self.director_test)
        rezultat = manager.compose_down(volume=True, simulare=True)
        
        self.assertTrue(rezultat)
        mock_run.assert_not_called()
    
    @patch('subprocess.run')
    def test_compose_build_fara_cache(self, mock_run):
        """Testează compose_build fără cache."""
        mock_run.return_value = MagicMock(returncode=0)
        
        manager = ManagerDocker(self.director_test)
        rezultat = manager.compose_build(fara_cache=True)
        
        self.assertTrue(rezultat)
        call_args = mock_run.call_args[0][0]
        self.assertIn("--no-cache", call_args)


# ═══════════════════════════════════════════════════════════════════════════════
# Teste Verificări Docker
# ═══════════════════════════════════════════════════════════════════════════════

class TesteVerificariDocker(unittest.TestCase):
    """Teste pentru funcțiile de verificare Docker."""
    
    @patch('subprocess.run')
    def test_verifica_docker_instalat_true(self, mock_run):
        """Testează când Docker este instalat."""
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(verifica_docker_instalat())
    
    @patch('subprocess.run')
    def test_verifica_docker_instalat_false(self, mock_run):
        """Testează când Docker nu este instalat."""
        mock_run.side_effect = FileNotFoundError()
        self.assertFalse(verifica_docker_instalat())
    
    @patch('subprocess.run')
    def test_verifica_docker_activ_true(self, mock_run):
        """Testează când Docker daemon este activ."""
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(verifica_docker_activ())
    
    @patch('subprocess.run')
    def test_verifica_docker_activ_false(self, mock_run):
        """Testează când Docker daemon nu răspunde."""
        mock_run.return_value = MagicMock(returncode=1)
        self.assertFalse(verifica_docker_activ())
    
    @patch('subprocess.run')
    def test_verifica_docker_activ_timeout(self, mock_run):
        """Testează când Docker nu răspunde (timeout)."""
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="docker", timeout=10)
        self.assertFalse(verifica_docker_activ())


# ═══════════════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  Teste Module Utilitare")
    print("  Rețele de Calculatoare – ASE")
    print("=" * 60)
    print()
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TesteLogger))
    suite.addTests(loader.loadTestsFromTestCase(TesteDockerManager))
    suite.addTests(loader.loadTestsFromTestCase(TesteVerificariDocker))
    
    runner = unittest.TextTestRunner(verbosity=2)
    rezultat = runner.run(suite)
    
    print()
    if rezultat.wasSuccessful():
        print("✓ Toate testele au trecut!")
        return 0
    else:
        print("✗ Unele teste au eșuat.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
