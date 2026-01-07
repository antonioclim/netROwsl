#!/usr/bin/env python3
"""
Utilitare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Oferă funcționalități pentru gestionarea containerelor Docker.
"""

import subprocess
import sys
from pathlib import Path
from typing import Optional, List, Dict

from .logger import configureaza_logger

logger = configureaza_logger("docker_utils")


class ManagerDocker:
    """Clasă pentru gestionarea operațiunilor Docker."""
    
    def __init__(self, director_compose: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_compose: Directorul care conține docker-compose.yml
        """
        self.director_compose = Path(director_compose)
        self.fisier_compose = self.director_compose / "docker-compose.yml"
    
    def _ruleaza_compose(self, *args, capture: bool = False, timeout: int = 120) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            *args: Argumentele comenzii compose
            capture: Captează output-ul
            timeout: Timeout în secunde
        
        Returns:
            Rezultatul comenzii
        """
        cmd = ["docker", "compose", "-f", str(self.fisier_compose)] + list(args)
        
        return subprocess.run(
            cmd,
            capture_output=capture,
            timeout=timeout,
            cwd=str(self.director_compose)
        )
    
    def compose_build(self, serviciu: Optional[str] = None, no_cache: bool = False):
        """
        Construiește imaginile Docker.
        
        Args:
            serviciu: Serviciul specific de construit (opțional)
            no_cache: Construiește fără cache
        """
        logger.info("Construire imagini Docker...")
        
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        if serviciu:
            args.append(serviciu)
        
        rezultat = self._ruleaza_compose(*args)
        
        if rezultat.returncode != 0:
            raise RuntimeError("Construirea imaginilor Docker a eșuat")
        
        logger.info("Imagini Docker construite cu succes")
    
    def compose_up(self, detach: bool = True, serviciu: Optional[str] = None):
        """
        Pornește containerele.
        
        Args:
            detach: Rulează în background
            serviciu: Serviciul specific de pornit (opțional)
        """
        logger.info("Pornire containere...")
        
        args = ["up"]
        if detach:
            args.append("-d")
        if serviciu:
            args.append(serviciu)
        
        rezultat = self._ruleaza_compose(*args)
        
        if rezultat.returncode != 0:
            raise RuntimeError("Pornirea containerelor a eșuat")
        
        logger.info("Containere pornite")
    
    def compose_down(self, volumes: bool = False, timeout: int = 30):
        """
        Oprește și elimină containerele.
        
        Args:
            volumes: Elimină și volumele
            timeout: Timeout pentru oprire grațioasă
        """
        logger.info("Oprire containere...")
        
        args = ["down", "-t", str(timeout)]
        if volumes:
            args.append("-v")
        
        rezultat = self._ruleaza_compose(*args)
        
        if rezultat.returncode != 0:
            logger.warning("Oprirea containerelor a întâmpinat probleme")
        else:
            logger.info("Containere oprite")
    
    def compose_logs(self, serviciu: Optional[str] = None, urmarire: bool = False, linii: int = 100):
        """
        Afișează jurnalele containerelor.
        
        Args:
            serviciu: Serviciul specific (opțional)
            urmarire: Urmărește jurnalele în timp real
            linii: Numărul de linii de afișat
        """
        args = ["logs", "--tail", str(linii)]
        if urmarire:
            args.append("-f")
        if serviciu:
            args.append(serviciu)
        
        self._ruleaza_compose(*args)
    
    def compose_ps(self) -> str:
        """
        Returnează starea containerelor.
        
        Returns:
            Output-ul comenzii docker compose ps
        """
        rezultat = self._ruleaza_compose("ps", capture=True)
        return rezultat.stdout.decode() if rezultat.returncode == 0 else ""
    
    def obtine_stare_container(self, nume_container: str) -> Optional[str]:
        """
        Obține starea unui container specific.
        
        Args:
            nume_container: Numele containerului
        
        Returns:
            Starea containerului sau None
        """
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Status}}", nume_container],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                return rezultat.stdout.decode().strip()
        except Exception:
            pass
        return None
    
    def elimina_dupa_prefix(self, prefix: str, dry_run: bool = False):
        """
        Elimină resursele Docker cu un anumit prefix.
        
        Args:
            prefix: Prefixul de căutat
            dry_run: Doar afișează ce ar fi eliminat
        """
        # Elimină containere
        try:
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "--filter", f"name={prefix}", "-q"],
                capture_output=True,
                timeout=10
            )
            containere = rezultat.stdout.decode().strip().split('\n')
            containere = [c for c in containere if c]
            
            if containere:
                if dry_run:
                    logger.info(f"  [SIMULARE] Ar elimina containere: {', '.join(containere)}")
                else:
                    subprocess.run(["docker", "rm", "-f"] + containere, capture_output=True)
                    logger.info(f"  Containere eliminate: {len(containere)}")
        except Exception as e:
            logger.debug(f"Eroare la eliminarea containerelor: {e}")
        
        # Elimină rețele
        try:
            rezultat = subprocess.run(
                ["docker", "network", "ls", "--filter", f"name={prefix}", "-q"],
                capture_output=True,
                timeout=10
            )
            retele = rezultat.stdout.decode().strip().split('\n')
            retele = [r for r in retele if r]
            
            if retele:
                if dry_run:
                    logger.info(f"  [SIMULARE] Ar elimina rețele: {len(retele)}")
                else:
                    for retea in retele:
                        subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                    logger.info(f"  Rețele eliminate: {len(retele)}")
        except Exception as e:
            logger.debug(f"Eroare la eliminarea rețelelor: {e}")
        
        # Elimină volume
        try:
            rezultat = subprocess.run(
                ["docker", "volume", "ls", "--filter", f"name={prefix}", "-q"],
                capture_output=True,
                timeout=10
            )
            volume = rezultat.stdout.decode().strip().split('\n')
            volume = [v for v in volume if v]
            
            if volume:
                if dry_run:
                    logger.info(f"  [SIMULARE] Ar elimina volume: {len(volume)}")
                else:
                    for volum in volume:
                        subprocess.run(["docker", "volume", "rm", volum], capture_output=True)
                    logger.info(f"  Volume eliminate: {len(volume)}")
        except Exception as e:
            logger.debug(f"Eroare la eliminarea volumelor: {e}")
    
    def system_prune(self, toate: bool = False):
        """
        Curăță resursele Docker nefolosite.
        
        Args:
            toate: Include și imagini nefolosite
        """
        logger.info("Curățare resurse Docker nefolosite...")
        
        args = ["docker", "system", "prune", "-f"]
        if toate:
            args.append("-a")
        
        try:
            subprocess.run(args, capture_output=True, timeout=60)
            logger.info("Curățare completă")
        except Exception as e:
            logger.warning(f"Eroare la curățare: {e}")
    
    def verifica_serviciu(self, port: int, timeout: int = 30) -> bool:
        """
        Verifică dacă un serviciu răspunde pe un port.
        
        Args:
            port: Portul de verificat
            timeout: Timeout total în secunde
        
        Returns:
            True dacă serviciul răspunde
        """
        import socket
        import time
        
        timp_start = time.time()
        while time.time() - timp_start < timeout:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    rezultat = s.connect_ex(('localhost', port))
                    if rezultat == 0:
                        return True
            except Exception:
                pass
            time.sleep(1)
        
        return False
