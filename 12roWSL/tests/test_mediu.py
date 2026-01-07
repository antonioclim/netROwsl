#!/usr/bin/env python3
"""
Teste pentru Verificarea Mediului
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Verifică dacă toate cerințele preliminare sunt îndeplinite.
"""

import sys
import subprocess
from pathlib import Path

import pytest


class TestVersiunePython:
    """Teste pentru versiunea Python."""
    
    def test_versiune_minima(self):
        """Verifică versiunea minimă Python 3.11."""
        assert sys.version_info >= (3, 11), \
            f"Python 3.11+ necesar, găsit {sys.version_info.major}.{sys.version_info.minor}"


class TestImporturi:
    """Teste pentru pachetele Python necesare."""
    
    def test_import_grpc(self):
        """Verifică dacă grpcio este instalat."""
        try:
            import grpc
            assert True
        except ImportError:
            pytest.fail("Pachetul 'grpcio' nu este instalat. Rulați: pip install grpcio")
    
    def test_import_protobuf(self):
        """Verifică dacă protobuf este instalat."""
        try:
            import google.protobuf
            assert True
        except ImportError:
            pytest.fail("Pachetul 'protobuf' nu este instalat. Rulați: pip install protobuf")
    
    def test_import_xmlrpc(self):
        """Verifică dacă xmlrpc.client este disponibil."""
        try:
            import xmlrpc.client
            assert True
        except ImportError:
            pytest.fail("Modulul xmlrpc.client nu este disponibil")
    
    def test_import_json(self):
        """Verifică dacă json este disponibil."""
        try:
            import json
            assert True
        except ImportError:
            pytest.fail("Modulul json nu este disponibil")
    
    def test_import_socket(self):
        """Verifică dacă socket este disponibil."""
        try:
            import socket
            assert True
        except ImportError:
            pytest.fail("Modulul socket nu este disponibil")
    
    def test_import_docker(self):
        """Verifică dacă pachetul docker este instalat."""
        try:
            import docker
            assert True
        except ImportError:
            pytest.skip("Pachetul 'docker' opțional nu este instalat")
    
    def test_import_requests(self):
        """Verifică dacă requests este instalat."""
        try:
            import requests
            assert True
        except ImportError:
            pytest.skip("Pachetul 'requests' opțional nu este instalat")


class TestStructuraProiect:
    """Teste pentru structura directorului proiectului."""
    
    @pytest.fixture
    def radacina_proiect(self):
        """Returnează calea către rădăcina proiectului."""
        return Path(__file__).parent.parent
    
    def test_director_docker(self, radacina_proiect):
        """Verifică existența directorului docker."""
        assert (radacina_proiect / "docker").is_dir(), \
            "Directorul 'docker' lipsește"
    
    def test_fisier_docker_compose(self, radacina_proiect):
        """Verifică existența fișierului docker-compose.yml."""
        assert (radacina_proiect / "docker" / "docker-compose.yml").is_file(), \
            "Fișierul 'docker/docker-compose.yml' lipsește"
    
    def test_director_src(self, radacina_proiect):
        """Verifică existența directorului src."""
        assert (radacina_proiect / "src").is_dir(), \
            "Directorul 'src' lipsește"
    
    def test_director_scripts(self, radacina_proiect):
        """Verifică existența directorului scripts."""
        assert (radacina_proiect / "scripts").is_dir(), \
            "Directorul 'scripts' lipsește"
    
    def test_director_tests(self, radacina_proiect):
        """Verifică existența directorului tests."""
        assert (radacina_proiect / "tests").is_dir(), \
            "Directorul 'tests' lipsește"


class TestDisponibilitatePorturi:
    """Teste pentru disponibilitatea porturilor."""
    
    def _verifica_port_disponibil(self, port: int) -> bool:
        """Verifică dacă un port este disponibil (neocupat)."""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                rezultat = s.connect_ex(('localhost', port))
                return rezultat != 0  # Disponibil dacă conexiunea eșuează
        except Exception:
            return True
    
    def test_port_smtp_disponibil(self):
        """Verifică dacă portul SMTP 1025 este disponibil."""
        # Acest test verifică dacă portul NU este ocupat de alt proces
        # Dacă serviciile de laborator rulează, testul va fi omis
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                rezultat = s.connect_ex(('localhost', 1025))
                if rezultat == 0:
                    pytest.skip("Portul 1025 este activ (serviciul de laborator rulează)")
        except Exception:
            pass
    
    def test_port_jsonrpc_disponibil(self):
        """Verifică portul JSON-RPC 6200."""
        import socket
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                rezultat = s.connect_ex(('localhost', 6200))
                if rezultat == 0:
                    pytest.skip("Portul 6200 este activ (serviciul de laborator rulează)")
        except Exception:
            pass


class TestDocker:
    """Teste pentru disponibilitatea Docker."""
    
    def test_docker_instalat(self):
        """Verifică dacă Docker este instalat."""
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=10
        )
        assert rezultat.returncode == 0, \
            "Docker nu este instalat sau nu este în PATH"
    
    def test_docker_compose_instalat(self):
        """Verifică dacă Docker Compose este disponibil."""
        rezultat = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True,
            timeout=10
        )
        assert rezultat.returncode == 0, \
            "Docker Compose nu este disponibil"
    
    def test_docker_daemon_activ(self):
        """Verifică dacă daemon-ul Docker rulează."""
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=15
        )
        if rezultat.returncode != 0:
            pytest.skip("Daemon-ul Docker nu rulează. Porniți Docker Desktop.")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
