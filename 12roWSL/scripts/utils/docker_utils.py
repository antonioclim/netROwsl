#!/usr/bin/env python3
"""
Utilitare pentru Gestionarea Docker
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Funcții helper pentru operații Docker Compose.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, List

from .logger import configureaza_logger

logger = configureaza_logger("docker_utils")


class ManagerDocker:
    """Manager pentru operații Docker Compose."""
    
    def __init__(self, director_docker: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_docker: Calea către directorul cu docker-compose.yml
        """
        self.director_docker = Path(director_docker)
        self.fisier_compose = self.director_docker / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            logger.warning(f"docker-compose.yml nu a fost găsit în {self.director_docker}")
    
    def _ruleaza_compose(self, argumente: List[str], capteaza: bool = False) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            argumente: Lista de argumente pentru docker compose
            capteaza: Dacă se captează output-ul
        
        Returns:
            Rezultatul comenzii
        """
        comanda = ["docker", "compose"] + argumente
        logger.debug(f"Execuție: {' '.join(comanda)}")
        
        return subprocess.run(
            comanda,
            cwd=self.director_docker,
            capture_output=capteaza,
            text=True
        )
    
    def compune_build(self, fara_cache: bool = False) -> bool:
        """
        Construiește imaginile Docker.
        
        Args:
            fara_cache: Dacă se ignoră cache-ul
        
        Returns:
            True dacă a reușit
        """
        argumente = ["build"]
        if fara_cache:
            argumente.append("--no-cache")
        
        logger.info("Construire imagini Docker...")
        rezultat = self._ruleaza_compose(argumente)
        
        if rezultat.returncode == 0:
            logger.info("✓ Imaginile au fost construite cu succes")
            return True
        else:
            logger.error("✗ Construirea imaginilor a eșuat")
            return False
    
    def compune_up(self, detasat: bool = True, servicii: List[str] = None) -> bool:
        """
        Pornește containerele.
        
        Args:
            detasat: Dacă se rulează în fundal
            servicii: Lista de servicii de pornit (implicit: toate)
        
        Returns:
            True dacă a reușit
        """
        argumente = ["up"]
        if detasat:
            argumente.append("-d")
        if servicii:
            argumente.extend(servicii)
        
        logger.info("Pornire containere Docker...")
        rezultat = self._ruleaza_compose(argumente)
        
        if rezultat.returncode == 0:
            logger.info("✓ Containerele au fost pornite")
            return True
        else:
            logger.error("✗ Pornirea containerelor a eșuat")
            return False
    
    def compune_down(self, volume: bool = False, orfani: bool = True) -> bool:
        """
        Oprește și elimină containerele.
        
        Args:
            volume: Dacă se elimină și volumele
            orfani: Dacă se elimină containerele orfane
        
        Returns:
            True dacă a reușit
        """
        argumente = ["down"]
        if volume:
            argumente.append("--volumes")
        if orfani:
            argumente.append("--remove-orphans")
        
        logger.info("Oprire containere Docker...")
        rezultat = self._ruleaza_compose(argumente)
        
        if rezultat.returncode == 0:
            logger.info("✓ Containerele au fost oprite")
            return True
        else:
            logger.error("✗ Oprirea containerelor a eșuat")
            return False
    
    def compune_jurnale(self, serviciu: str = None, urmareste: bool = False, linii: int = 100):
        """
        Afișează jurnalele containerelor.
        
        Args:
            serviciu: Serviciul specific (implicit: toate)
            urmareste: Dacă se urmăresc în timp real
            linii: Numărul de linii de afișat
        """
        argumente = ["logs", f"--tail={linii}"]
        if urmareste:
            argumente.append("-f")
        if serviciu:
            argumente.append(serviciu)
        
        self._ruleaza_compose(argumente)
    
    def verifica_servicii(self, servicii: Dict) -> bool:
        """
        Verifică dacă toate serviciile sunt active.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        
        Returns:
            True dacă toate serviciile sunt active
        """
        import socket
        
        toate_active = True
        
        for nume, config in servicii.items():
            port = config.get("port")
            if not port:
                continue
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    rezultat = s.connect_ex(('localhost', port))
                    
                    if rezultat == 0:
                        logger.info(f"  ✓ {config.get('descriere', nume)}: ACTIV (port {port})")
                    else:
                        logger.warning(f"  ✗ {config.get('descriere', nume)}: INACTIV (port {port})")
                        toate_active = False
            except Exception as e:
                logger.error(f"  ✗ {nume}: Eroare la verificare - {e}")
                toate_active = False
        
        return toate_active
    
    def elimina_dupa_prefix(self, prefix: str, simulare: bool = False):
        """
        Elimină resursele Docker cu un anumit prefix.
        
        Args:
            prefix: Prefixul de căutat
            simulare: Dacă doar se afișează ce ar fi șters
        """
        # Eliminare containere
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "-q"],
            capture_output=True, text=True
        )
        containere = rezultat.stdout.strip().split('\n')
        containere = [c for c in containere if c]
        
        if containere:
            if simulare:
                logger.info(f"  [SIMULARE] Ar fi șterse {len(containere)} containere")
            else:
                subprocess.run(["docker", "rm", "-f"] + containere, capture_output=True)
                logger.info(f"  Șterse {len(containere)} containere")
        
        # Eliminare rețele
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "-q"],
            capture_output=True, text=True
        )
        retele = rezultat.stdout.strip().split('\n')
        retele = [r for r in retele if r]
        
        if retele:
            if simulare:
                logger.info(f"  [SIMULARE] Ar fi șterse {len(retele)} rețele")
            else:
                for retea in retele:
                    subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                logger.info(f"  Șterse {len(retele)} rețele")
        
        # Eliminare volume
        rezultat = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "-q"],
            capture_output=True, text=True
        )
        volume = rezultat.stdout.strip().split('\n')
        volume = [v for v in volume if v]
        
        if volume:
            if simulare:
                logger.info(f"  [SIMULARE] Ar fi șterse {len(volume)} volume")
            else:
                subprocess.run(["docker", "volume", "rm"] + volume, capture_output=True)
                logger.info(f"  Șterse {len(volume)} volume")
    
    def prune_sistem(self):
        """Curăță resursele Docker neutilizate."""
        logger.info("Curățare resurse Docker neutilizate...")
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )
        logger.info("✓ Curățare completă")
