#!/usr/bin/env python3
"""
Utilitare Docker
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Oferă funcții pentru gestionarea containerelor și serviciilor Docker.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import subprocess
import socket
import time
from pathlib import Path
from typing import Any, Optional

from .logger import configureaza_logger

logger = configureaza_logger("docker_utils")


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE
# ═══════════════════════════════════════════════════════════════════════════════

DEFAULT_TIMEOUT = 120
SOCKET_TIMEOUT = 2


# ═══════════════════════════════════════════════════════════════════════════════
# CLASA_MANAGER_DOCKER
# ═══════════════════════════════════════════════════════════════════════════════

class ManagerDocker:
    """
    Manager pentru operațiuni Docker Compose.
    
    Attributes:
        director_docker: Calea către directorul cu docker-compose.yml
        fisier_compose: Calea completă către fișierul compose
    
    Example:
        >>> manager = ManagerDocker(Path("/home/claude/11roWSL/docker"))
        >>> manager.compose_up(detach=True)
        True
    """
    
    def __init__(self, director_docker: Path) -> None:
        """
        Inițializează managerul Docker.
        
        Args:
            director_docker: Calea către directorul cu docker-compose.yml
        
        Raises:
            FileNotFoundError: Dacă docker-compose.yml nu există
        """
        self.director_docker = Path(director_docker)
        self.fisier_compose = self.director_docker / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(
                f"Fișierul docker-compose.yml nu a fost găsit: {self.fisier_compose}"
            )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # EXECUTARE_COMENZI
    # ═══════════════════════════════════════════════════════════════════════════
    
    def _ruleaza_compose(
        self, 
        *args: str, 
        capture_output: bool = True,
        text: bool = True,
        timeout: int = DEFAULT_TIMEOUT
    ) -> subprocess.CompletedProcess[str]:
        """
        Rulează o comandă docker compose.
        
        Args:
            *args: Argumente pentru docker compose
            capture_output: Capturează stdout/stderr
            text: Returnează output ca string
            timeout: Timeout în secunde
        
        Returns:
            Rezultatul comenzii subprocess.CompletedProcess
        """
        cmd = ["docker", "compose", "-f", str(self.fisier_compose), *args]
        
        return subprocess.run(
            cmd,
            cwd=self.director_docker,
            capture_output=capture_output,
            text=text,
            timeout=timeout
        )
    
    # ═══════════════════════════════════════════════════════════════════════════
    # OPERATII_LIFECYCLE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Pornește serviciile Docker Compose.
        
        Args:
            detach: Rulează în background (implicit True)
            build: Reconstruiește imaginile înainte de pornire
        
        Returns:
            True dacă comanda a reușit, False altfel
        
        Example:
            >>> manager.compose_up(detach=True, build=False)
            True
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
            volumes: Elimină și volumele asociate (implicit False)
        
        Returns:
            True dacă comanda a reușit, False altfel
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
            True dacă build-ul a reușit, False altfel
        """
        result = self._ruleaza_compose("build", capture_output=False)
        return result.returncode == 0
    
    def compose_restart(self, serviciu: Optional[str] = None) -> bool:
        """
        Repornește serviciile.
        
        Args:
            serviciu: Numele serviciului de repornit (None pentru toate)
        
        Returns:
            True dacă repornirea a reușit, False altfel
        """
        args = ["restart"]
        if serviciu:
            args.append(serviciu)
        
        result = self._ruleaza_compose(*args, capture_output=False)
        return result.returncode == 0
    
    # ═══════════════════════════════════════════════════════════════════════════
    # INTEROGARE_STARE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def obtine_containere_rulare(self) -> list[str]:
        """
        Obține lista containerelor care rulează.
        
        Returns:
            Lista numelor containerelor active
        
        Example:
            >>> manager.obtine_containere_rulare()
            ['s11_nginx_lb', 's11_backend_1', 's11_backend_2', 's11_backend_3']
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
    
    def verifica_servicii(self, servicii: dict[str, dict[str, Any]]) -> bool:
        """
        Verifică starea serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
                      Format: {nume: {container, port, descriere, ...}}
        
        Returns:
            True dacă toate serviciile sunt sănătoase, False altfel
        """
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
                        s.settimeout(SOCKET_TIMEOUT)
                        s.connect(("localhost", port))
                        logger.info(f"  ✓ {nume}: activ pe portul {port}")
                except (socket.timeout, ConnectionRefusedError):
                    logger.warning(f"  ✗ {nume}: portul {port} nu răspunde")
                    toate_sanatoase = False
            else:
                logger.info(f"  ✓ {nume}: container activ")
        
        return toate_sanatoase
    
    def obtine_log_uri(
        self, 
        serviciu: Optional[str] = None, 
        linii: int = 100
    ) -> str:
        """
        Obține log-urile serviciilor.
        
        Args:
            serviciu: Numele serviciului (None pentru toate)
            linii: Numărul de linii de returnat
        
        Returns:
            Log-urile ca string
        """
        args = ["logs", f"--tail={linii}"]
        if serviciu:
            args.append(serviciu)
        
        result = self._ruleaza_compose(*args)
        return result.stdout if result.returncode == 0 else result.stderr
    
    # ═══════════════════════════════════════════════════════════════════════════
    # CURATARE_RESURSE
    # ═══════════════════════════════════════════════════════════════════════════
    
    def elimina_dupa_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Elimină resursele Docker cu un prefix specific.
        
        Args:
            prefix: Prefixul de căutat (ex: 's11_')
            dry_run: Doar simulează operația (implicit False)
        """
        # Elimină containere
        result = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        containere = [c for c in result.stdout.strip().split('\n') if c]
        
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
        retele = [r for r in result.stdout.strip().split('\n') if r]
        
        if retele:
            if dry_run:
                logger.info(f"  [SIMULARE] Ar fi eliminate {len(retele)} rețele")
            else:
                for retea in retele:
                    subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                logger.info(f"  ✓ {len(retele)} rețele eliminate")
    
    def curata_sistem(self, force: bool = True) -> None:
        """
        Curăță resursele Docker neutilizate.
        
        Args:
            force: Nu cere confirmare (implicit True)
        """
        args = ["docker", "system", "prune"]
        if force:
            args.append("-f")
        
        subprocess.run(args, capture_output=True)
