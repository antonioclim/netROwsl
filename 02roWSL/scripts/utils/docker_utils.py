#!/usr/bin/env python3
"""
Utilitare Docker
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Funcții helper pentru managementul containerelor Docker.
"""

import subprocess
import socket
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from scripts.utils.logger import configurează_logger

logger = configurează_logger("docker_utils")


@dataclass
class InfoContainer:
    """Informații despre un container Docker."""
    nume: str
    id: str
    stare: str
    porturi: List[str]
    imagine: str


class ManagerDocker:
    """Manager pentru operațiuni Docker Compose."""
    
    def __init__(self, cale_docker: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            cale_docker: Calea către directorul cu docker-compose.yml
        """
        self.cale_docker = Path(cale_docker)
        self.fișier_compose = self.cale_docker / "docker-compose.yml"
        
        if not self.fișier_compose.exists():
            logger.warning(f"Fișierul docker-compose.yml nu există: {self.fișier_compose}")
    
    def _rulează_compose(self, *args: str, capture: bool = False) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            *args: Argumente pentru docker compose
            capture: Dacă să captureze output-ul
            
        Returns:
            Rezultatul comenzii
        """
        cmd = ["docker", "compose", "-f", str(self.fișier_compose)] + list(args)
        
        logger.debug(f"Rulare: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            cwd=self.cale_docker
        )
    
    def compose_up(self, detach: bool = True, build: bool = False) -> bool:
        """
        Pornește serviciile din docker-compose.
        
        Args:
            detach: Rulare în fundal
            build: Reconstruire imagini înainte de pornire
            
        Returns:
            True dacă a reușit
        """
        args = ["up"]
        
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        rezultat = self._rulează_compose(*args)
        return rezultat.returncode == 0
    
    def compose_down(self, volumes: bool = False, timeout: int = 10) -> bool:
        """
        Oprește și elimină serviciile.
        
        Args:
            volumes: Elimină și volumele
            timeout: Timeout pentru oprire grațioasă
            
        Returns:
            True dacă a reușit
        """
        args = ["down", "-t", str(timeout)]
        
        if volumes:
            args.append("-v")
        
        rezultat = self._rulează_compose(*args)
        return rezultat.returncode == 0
    
    def compose_build(self, no_cache: bool = False) -> bool:
        """
        Construiește imaginile.
        
        Args:
            no_cache: Construire fără cache
            
        Returns:
            True dacă a reușit
        """
        args = ["build"]
        
        if no_cache:
            args.append("--no-cache")
        
        rezultat = self._rulează_compose(*args)
        return rezultat.returncode == 0
    
    def compose_logs(self, serviciu: Optional[str] = None, follow: bool = False, tail: int = 100) -> str:
        """
        Obține logurile serviciilor.
        
        Args:
            serviciu: Numele serviciului (None pentru toate)
            follow: Urmărire în timp real
            tail: Număr de linii de afișat
            
        Returns:
            Conținutul logurilor
        """
        args = ["logs", f"--tail={tail}"]
        
        if follow:
            args.append("-f")
        
        if serviciu:
            args.append(serviciu)
        
        rezultat = self._rulează_compose(*args, capture=True)
        return rezultat.stdout
    
    def container_rulează(self, nume_container: str) -> bool:
        """
        Verifică dacă un container rulează.
        
        Args:
            nume_container: Numele containerului
            
        Returns:
            True dacă rulează
        """
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", nume_container],
                capture_output=True,
                text=True,
                timeout=5
            )
            return rezultat.stdout.strip().lower() == "true"
        except Exception:
            return False
    
    def obține_info_container(self, nume_container: str) -> Optional[InfoContainer]:
        """
        Obține informații detaliate despre un container.
        
        Args:
            nume_container: Numele containerului
            
        Returns:
            InfoContainer sau None dacă nu există
        """
        try:
            # Obține ID-ul și starea
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", 
                 "{{.Id}}|{{.State.Status}}|{{.Config.Image}}", 
                 nume_container],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if rezultat.returncode != 0:
                return None
            
            părți = rezultat.stdout.strip().split("|")
            if len(părți) != 3:
                return None
            
            # Obține porturile
            rezultat_porturi = subprocess.run(
                ["docker", "port", nume_container],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            porturi = rezultat_porturi.stdout.strip().split("\n") if rezultat_porturi.stdout.strip() else []
            
            return InfoContainer(
                nume=nume_container,
                id=părți[0][:12],
                stare=părți[1],
                porturi=porturi,
                imagine=părți[2]
            )
        except Exception as e:
            logger.debug(f"Eroare la obținerea info container: {e}")
            return None
    
    def verifică_port(self, host: str, port: int, timeout: float = 1.0) -> bool:
        """
        Verifică dacă un port TCP este accesibil.
        
        Args:
            host: Adresa host
            port: Numărul portului
            timeout: Timeout în secunde
            
        Returns:
            True dacă portul răspunde
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((host, port))
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
    
    def elimină_după_prefix(self, prefix: str) -> None:
        """
        Elimină resursele Docker cu un anumit prefix.
        
        Args:
            prefix: Prefixul de căutat
        """
        # Eliminare containere
        try:
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "-q", "-f", f"name={prefix}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            containere = rezultat.stdout.strip().split("\n")
            containere = [c for c in containere if c]
            
            if containere:
                subprocess.run(
                    ["docker", "rm", "-f"] + containere,
                    capture_output=True,
                    timeout=30
                )
                logger.info(f"  Eliminate {len(containere)} containere")
        except Exception as e:
            logger.debug(f"Eroare la eliminare containere: {e}")
        
        # Eliminare rețele
        try:
            rezultat = subprocess.run(
                ["docker", "network", "ls", "-q", "-f", f"name={prefix}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            rețele = rezultat.stdout.strip().split("\n")
            rețele = [r for r in rețele if r]
            
            for rețea in rețele:
                subprocess.run(
                    ["docker", "network", "rm", rețea],
                    capture_output=True,
                    timeout=10
                )
            
            if rețele:
                logger.info(f"  Eliminate {len(rețele)} rețele")
        except Exception as e:
            logger.debug(f"Eroare la eliminare rețele: {e}")
        
        # Eliminare volume
        try:
            rezultat = subprocess.run(
                ["docker", "volume", "ls", "-q", "-f", f"name={prefix}"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            volume = rezultat.stdout.strip().split("\n")
            volume = [v for v in volume if v]
            
            for volum in volume:
                subprocess.run(
                    ["docker", "volume", "rm", volum],
                    capture_output=True,
                    timeout=10
                )
            
            if volume:
                logger.info(f"  Eliminate {len(volume)} volume")
        except Exception as e:
            logger.debug(f"Eroare la eliminare volume: {e}")


def docker_disponibil() -> bool:
    """
    Verifică dacă Docker este instalat și rulează.
    
    Returns:
        True dacă Docker este disponibil
    """
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


if __name__ == "__main__":
    # Test rapid
    print("Test Utilitare Docker")
    print("=" * 40)
    
    print(f"Docker disponibil: {docker_disponibil()}")
    
    if docker_disponibil():
        manager = ManagerDocker(Path("."))
        print(f"Container week2_lab rulează: {manager.container_rulează('week2_lab')}")
