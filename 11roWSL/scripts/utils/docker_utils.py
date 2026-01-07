#!/usr/bin/env python3
"""
Utilitare Docker
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Oferă funcții pentru gestionarea containerelor și serviciilor Docker.
"""

import subprocess
import time
from pathlib import Path
from typing import Optional

from .logger import configureaza_logger

logger = configureaza_logger("docker_utils")


class ManagerDocker:
    """Manager pentru operațiuni Docker Compose."""
    
    def __init__(self, director_docker: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_docker: Calea către directorul cu docker-compose.yml
        """
        self.director_docker = Path(director_docker)
        self.fisier_compose = self.director_docker / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(
                f"Fișierul docker-compose.yml nu a fost găsit: {self.fisier_compose}"
            )
    
    def _ruleaza_compose(self, *args, **kwargs) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            *args: Argumente pentru docker compose
            **kwargs: Argumente pentru subprocess.run
        
        Returns:
            Rezultatul comenzii
        """
        cmd = ["docker", "compose", "-f", str(self.fisier_compose), *args]
        
        return subprocess.run(
            cmd,
            cwd=self.director_docker,
            capture_output=kwargs.get("capture_output", True),
            text=kwargs.get("text", True),
            timeout=kwargs.get("timeout", 120)
        )
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Pornește serviciile Docker Compose.
        
        Args:
            detach: Rulează în background
            build: Reconstruiește imaginile
        
        Returns:
            True dacă a reușit
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        result = self._ruleaza_compose(*args, capture_output=False)
        return result.returncode == 0
    
    def compose_down(self, volumes: bool = False) -> bool:
        """
        Oprește și elimină containerele.
        
        Args:
            volumes: Elimină și volumele
        
        Returns:
            True dacă a reușit
        """
        args = ["down"]
        if volumes:
            args.append("-v")
        
        result = self._ruleaza_compose(*args, capture_output=False)
        return result.returncode == 0
    
    def compose_build(self) -> bool:
        """
        Construiește imaginile Docker.
        
        Returns:
            True dacă a reușit
        """
        result = self._ruleaza_compose("build", capture_output=False)
        return result.returncode == 0
    
    def obtine_containere_rulare(self) -> list[str]:
        """
        Obține lista containerelor care rulează.
        
        Returns:
            Lista numelor containerelor
        """
        result = subprocess.run(
            ["docker", "ps", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            return []
        
        return [
            nume.strip() 
            for nume in result.stdout.strip().split('\n') 
            if nume.strip()
        ]
    
    def verifica_servicii(self, servicii: dict) -> bool:
        """
        Verifică starea serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        
        Returns:
            True dacă toate serviciile sunt sănătoase
        """
        import socket
        
        toate_sanatoase = True
        containere_active = self.obtine_containere_rulare()
        
        for nume, config in servicii.items():
            nume_container = config.get("container", "")
            port = config.get("port")
            
            # Verifică dacă containerul rulează
            if nume_container not in containere_active:
                logger.warning(f"  ✗ {nume}: containerul nu rulează")
                toate_sanatoase = False
                continue
            
            # Verifică portul dacă este specificat
            if port:
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(2)
                        s.connect(("localhost", port))
                        logger.info(f"  ✓ {nume}: activ pe portul {port}")
                except (socket.timeout, ConnectionRefusedError):
                    logger.warning(f"  ✗ {nume}: portul {port} nu răspunde")
                    toate_sanatoase = False
            else:
                logger.info(f"  ✓ {nume}: container activ")
        
        return toate_sanatoase
    
    def elimina_dupa_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Elimină resursele Docker cu un prefix specific.
        
        Args:
            prefix: Prefixul de căutat
            dry_run: Doar simulează (nu elimină efectiv)
        """
        # Elimină containere
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        containere = result.stdout.strip().split('\n')
        containere = [c for c in containere if c]
        
        if containere:
            if dry_run:
                logger.info(f"  [SIMULARE] Ar fi eliminate {len(containere)} containere")
            else:
                subprocess.run(["docker", "rm", "-f"] + containere, capture_output=True)
                logger.info(f"  ✓ {len(containere)} containere eliminate")
        
        # Elimină rețele
        result = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        retele = result.stdout.strip().split('\n')
        retele = [r for r in retele if r]
        
        if retele:
            if dry_run:
                logger.info(f"  [SIMULARE] Ar fi eliminate {len(retele)} rețele")
            else:
                for retea in retele:
                    subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                logger.info(f"  ✓ {len(retele)} rețele eliminate")
    
    def curata_sistem(self) -> None:
        """Curăță resursele Docker neutilizate."""
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )
