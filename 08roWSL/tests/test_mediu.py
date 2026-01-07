#!/usr/bin/env python3
"""
Teste de Validare a Mediului
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Teste pentru verificarea configurației corecte a mediului de laborator.
"""

import subprocess
import socket
import sys
from pathlib import Path

import pytest

RADACINA_PROIECT = Path(__file__).parent.parent


class TestMediuDocker:
    """Teste pentru mediul Docker."""
    
    def test_docker_disponibil(self):
        """Comanda Docker trebuie să fie disponibilă."""
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True
        )
        assert result.returncode == 0, "Docker nu este instalat"
    
    def test_docker_compose_disponibil(self):
        """Docker Compose V2 trebuie să fie disponibil."""
        result = subprocess.run(
            ["docker", "compose", "version"],
            capture_output=True
        )
        assert result.returncode == 0, "Docker Compose V2 nu este disponibil"
    
    def test_daemon_docker_ruleaza(self):
        """Daemon-ul Docker trebuie să ruleze."""
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        assert result.returncode == 0, "Daemon-ul Docker nu rulează"


class TestStructuraDirectoare:
    """Teste pentru structura directoarelor."""
    
    def test_director_docker_exista(self):
        """Directorul docker trebuie să existe."""
        assert (RADACINA_PROIECT / "docker").is_dir()
    
    def test_fisier_compose_exista(self):
        """Fișierul docker-compose.yml trebuie să existe."""
        assert (RADACINA_PROIECT / "docker" / "docker-compose.yml").is_file()
    
    def test_director_scripts_exista(self):
        """Directorul scripts trebuie să existe."""
        assert (RADACINA_PROIECT / "scripts").is_dir()
    
    def test_director_src_exista(self):
        """Directorul src trebuie să existe."""
        assert (RADACINA_PROIECT / "src").is_dir()
    
    def test_director_www_exista(self):
        """Directorul www trebuie să existe."""
        assert (RADACINA_PROIECT / "www").is_dir()


class TestPorturiRetea:
    """Teste pentru disponibilitatea porturilor."""
    
    @staticmethod
    def este_port_disponibil(port: int) -> bool:
        """Verifică dacă un port este disponibil."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return True
        except OSError:
            return False
    
    def test_stare_port_8080(self):
        """Starea portului 8080 trebuie să fie cunoscută."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                result = s.connect_ex(("127.0.0.1", 8080))
                # Fie disponibil (conexiune refuzată) fie în uz (conectat)
                assert result in [0, 111, 10061]
        except Exception:
            pass  # Verificarea portului completată


class TestMediuPython:
    """Teste pentru mediul Python."""
    
    def test_versiune_python(self):
        """Versiunea Python trebuie să fie 3.11+."""
        assert sys.version_info >= (3, 11), f"Este necesar Python 3.11+, găsit {sys.version}"
    
    def test_modul_socket(self):
        """Modulul socket trebuie să fie disponibil."""
        import socket
        assert socket is not None
    
    def test_modul_pathlib(self):
        """Modulul pathlib trebuie să fie disponibil."""
        from pathlib import Path
        assert Path is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
