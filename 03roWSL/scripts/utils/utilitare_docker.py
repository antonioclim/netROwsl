#!/usr/bin/env python3
"""
Utilitare Docker
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă funcții helper pentru gestionarea containerelor și serviciilor Docker.
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict
from .logger import configureaza_logger

logger = configureaza_logger("utilitare_docker")


class ManagerDocker:
    """Manager pentru operațiuni Docker Compose."""
    
    def __init__(self, director_compose: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_compose: Directorul care conține docker-compose.yml
        """
        self.director_compose = Path(director_compose)
        self.fisier_compose = self.director_compose / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(f"Nu s-a găsit: {self.fisier_compose}")
    
    def _ruleaza_compose(self, argumente: List[str], capture: bool = False) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            argumente: Lista de argumente pentru docker compose
            capture: True pentru a captura output-ul
            
        Returns:
            Rezultatul procesului
        """
        cmd = ["docker", "compose", "-f", str(self.fisier_compose)] + argumente
        
        return subprocess.run(
            cmd,
            capture_output=capture,
            cwd=str(self.director_compose)
        )
    
    def compose_up(self, detach: bool = True, profiluri: List[str] = None) -> bool:
        """
        Pornește serviciile Docker Compose.
        
        Args:
            detach: True pentru a rula în fundal
            profiluri: Lista de profiluri de activat
            
        Returns:
            True dacă a reușit
        """
        argumente = []
        
        if profiluri:
            for profil in profiluri:
                argumente.extend(["--profile", profil])
        
        argumente.append("up")
        
        if detach:
            argumente.append("-d")
        
        rezultat = self._ruleaza_compose(argumente)
        return rezultat.returncode == 0
    
    def compose_down(self, volume: bool = False) -> bool:
        """
        Oprește serviciile Docker Compose.
        
        Args:
            volume: True pentru a elimina și volumele
            
        Returns:
            True dacă a reușit
        """
        argumente = ["down"]
        
        if volume:
            argumente.append("-v")
        
        rezultat = self._ruleaza_compose(argumente)
        return rezultat.returncode == 0
    
    def compose_build(self, fara_cache: bool = False) -> bool:
        """
        Construiește imaginile Docker.
        
        Args:
            fara_cache: True pentru a ignora cache-ul
            
        Returns:
            True dacă a reușit
        """
        argumente = ["build"]
        
        if fara_cache:
            argumente.append("--no-cache")
        
        rezultat = self._ruleaza_compose(argumente)
        return rezultat.returncode == 0
    
    def obtine_containere(self) -> List[Dict]:
        """
        Obține lista containerelor.
        
        Returns:
            Lista de dicționare cu informații despre containere
        """
        try:
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{json .}}"],
                capture_output=True,
                timeout=30
            )
            
            containere = []
            for linie in rezultat.stdout.decode().strip().split('\n'):
                if linie:
                    containere.append(json.loads(linie))
            
            return containere
        except Exception as e:
            logger.error(f"Eroare la obținerea containerelor: {e}")
            return []
    
    def verifica_sanatate(self, container: str) -> bool:
        """
        Verifică starea de sănătate a unui container.
        
        Args:
            container: Numele containerului
            
        Returns:
            True dacă containerul este sănătos
        """
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Health.Status}}", container],
                capture_output=True,
                timeout=10
            )
            
            stare = rezultat.stdout.decode().strip()
            return stare == "healthy"
        except Exception:
            # Dacă nu are health check, verificăm dacă rulează
            try:
                rezultat = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Running}}", container],
                    capture_output=True,
                    timeout=10
                )
                return "true" in rezultat.stdout.decode().lower()
            except Exception:
                return False
    
    def obtine_loguri(self, container: str, linii: int = 50) -> str:
        """
        Obține ultimele log-uri ale unui container.
        
        Args:
            container: Numele containerului
            linii: Numărul de linii de returnat
            
        Returns:
            Log-urile containerului
        """
        try:
            rezultat = subprocess.run(
                ["docker", "logs", "--tail", str(linii), container],
                capture_output=True,
                timeout=30
            )
            return rezultat.stdout.decode() + rezultat.stderr.decode()
        except Exception as e:
            return f"Eroare la obținerea log-urilor: {e}"
    
    def executa_in_container(self, container: str, comanda: str, timeout: int = 30) -> tuple:
        """
        Execută o comandă într-un container.
        
        Args:
            container: Numele containerului
            comanda: Comanda de executat
            timeout: Timeout în secunde
            
        Returns:
            Tuple (success, output)
        """
        try:
            rezultat = subprocess.run(
                ["docker", "exec", container, "bash", "-c", comanda],
                capture_output=True,
                timeout=timeout
            )
            output = rezultat.stdout.decode() + rezultat.stderr.decode()
            return rezultat.returncode == 0, output
        except subprocess.TimeoutExpired:
            return False, "Timeout expirat"
        except Exception as e:
            return False, str(e)


def verifica_docker_disponibil() -> bool:
    """Verifică dacă Docker este disponibil și rulează."""
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def obtine_versiune_docker() -> Optional[str]:
    """Obține versiunea Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "version", "--format", "{{.Server.Version}}"],
            capture_output=True,
            timeout=10
        )
        return rezultat.stdout.decode().strip()
    except Exception:
        return None
