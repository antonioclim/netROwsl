#!/usr/bin/env python3
"""
Utilități Docker pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă funcții helper pentru gestionarea containerelor Docker.
"""

import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

from .logger import configureaza_logger

logger = configureaza_logger("docker_utils")


class ManagerDocker:
    """Manager pentru operații Docker Compose."""
    
    def __init__(self, director_compose: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_compose: Directorul care conține docker-compose.yml
        """
        self.director = director_compose
        self.fisier_compose = director_compose / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(
                f"Nu s-a găsit docker-compose.yml în {director_compose}"
            )
    
    def _ruleaza_compose(
        self,
        *argumente: str,
        capturare: bool = True,
        timeout: int = 300
    ) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            *argumente: Argumentele pentru docker compose
            capturare: Dacă să captureze ieșirea
            timeout: Timeout în secunde
        
        Returns:
            Rezultatul comenzii
        """
        comanda = ["docker", "compose", "-f", str(self.fisier_compose)] + list(argumente)
        
        return subprocess.run(
            comanda,
            cwd=self.director,
            capture_output=capturare,
            text=True,
            timeout=timeout
        )
    
    def compose_up(self, detasare: bool = True, reconstruire: bool = False) -> bool:
        """
        Pornește serviciile cu docker compose up.
        
        Args:
            detasare: Rulează în fundal
            reconstruire: Reconstruiește imaginile
        
        Returns:
            True dacă a reușit
        """
        argumente = ["up"]
        if detasare:
            argumente.append("-d")
        if reconstruire:
            argumente.append("--build")
        
        logger.info("Pornire containere Docker...")
        rezultat = self._ruleaza_compose(*argumente)
        
        if rezultat.returncode == 0:
            logger.info("Containerele au fost pornite")
            return True
        else:
            logger.error(f"Eroare la pornire: {rezultat.stderr}")
            return False
    
    def compose_down(self, volume: bool = False, dry_run: bool = False) -> bool:
        """
        Oprește serviciile cu docker compose down.
        
        Args:
            volume: Șterge și volumele
            dry_run: Doar afișează ce ar face
        
        Returns:
            True dacă a reușit
        """
        if dry_run:
            logger.info("[SIMULARE] Ar opri containerele")
            if volume:
                logger.info("[SIMULARE] Ar șterge și volumele")
            return True
        
        argumente = ["down"]
        if volume:
            argumente.extend(["-v", "--remove-orphans"])
        
        logger.info("Oprire containere Docker...")
        rezultat = self._ruleaza_compose(*argumente)
        
        if rezultat.returncode == 0:
            logger.info("Containerele au fost oprite")
            return True
        else:
            logger.error(f"Eroare la oprire: {rezultat.stderr}")
            return False
    
    def compose_build(self) -> bool:
        """
        Construiește imaginile Docker.
        
        Returns:
            True dacă a reușit
        """
        logger.info("Construire imagini Docker...")
        rezultat = self._ruleaza_compose("build")
        
        if rezultat.returncode == 0:
            logger.info("Imaginile au fost construite")
            return True
        else:
            logger.error(f"Eroare la construire: {rezultat.stderr}")
            return False
    
    def obtine_stare_containere(self) -> Dict[str, Dict[str, Any]]:
        """
        Obține starea tuturor containerelor.
        
        Returns:
            Dicționar cu starea fiecărui container
        """
        rezultat = self._ruleaza_compose(
            "ps",
            "--format", "{{.Name}}|{{.State}}|{{.Status}}"
        )
        
        containere = {}
        if rezultat.returncode == 0:
            for linie in rezultat.stdout.strip().split('\n'):
                if linie and '|' in linie:
                    parti = linie.split('|')
                    if len(parti) >= 3:
                        containere[parti[0]] = {
                            "stare": parti[1],
                            "status": parti[2]
                        }
        
        return containere
    
    def verifica_servicii(self, servicii: Dict[str, dict]) -> bool:
        """
        Verifică starea de sănătate a serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        
        Returns:
            True dacă toate serviciile sunt sănătoase
        """
        toate_sanatoase = True
        
        for nume, config in servicii.items():
            container = config.get("container", f"week10_{nume}")
            
            # Verificare existență și stare
            rezultat = subprocess.run(
                ["docker", "inspect", "--format", "{{.State.Health.Status}}", container],
                capture_output=True,
                text=True
            )
            
            if rezultat.returncode == 0:
                stare = rezultat.stdout.strip()
                if stare == "healthy":
                    logger.info(f"  ✓ {nume}: sănătos")
                elif stare == "starting":
                    logger.warning(f"  ⏳ {nume}: pornește...")
                else:
                    logger.warning(f"  ⚠ {nume}: {stare}")
            else:
                # Container fără health check, verificăm dacă rulează
                rezultat = subprocess.run(
                    ["docker", "inspect", "--format", "{{.State.Running}}", container],
                    capture_output=True,
                    text=True
                )
                if rezultat.stdout.strip() == "true":
                    logger.info(f"  ✓ {nume}: rulează")
                else:
                    logger.error(f"  ✗ {nume}: nu rulează")
                    toate_sanatoase = False
        
        return toate_sanatoase
    
    def afiseaza_stare(self, servicii: Dict[str, dict]):
        """
        Afișează starea detaliată a serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        """
        print("\n" + "=" * 50)
        print("Stare Servicii Laborator")
        print("=" * 50)
        
        containere = self.obtine_stare_containere()
        
        for nume, config in servicii.items():
            container = config.get("container", f"week10_{nume}")
            port = config.get("port", "N/A")
            
            if container in containere:
                stare = containere[container]
                simbol = "✓" if stare["stare"] == "running" else "✗"
                print(f"  {simbol} {nume:15} Port: {port:5}  [{stare['status']}]")
            else:
                print(f"  ✗ {nume:15} Port: {port:5}  [nu există]")
        
        print("=" * 50)
    
    def elimina_dupa_prefix(self, prefix: str, dry_run: bool = False) -> bool:
        """
        Elimină toate resursele Docker cu un anumit prefix.
        
        Args:
            prefix: Prefixul de căutat
            dry_run: Doar afișează ce ar face
        
        Returns:
            True dacă a reușit
        """
        succes = True
        
        # Containere
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
            capture_output=True, text=True
        )
        containere = [c for c in rezultat.stdout.strip().split('\n') if c]
        
        for container in containere:
            if dry_run:
                logger.info(f"[SIMULARE] Ar șterge containerul: {container}")
            else:
                subprocess.run(["docker", "rm", "-f", container], capture_output=True)
                logger.info(f"Șters container: {container}")
        
        # Rețele
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True, text=True
        )
        retele = [r for r in rezultat.stdout.strip().split('\n') if r]
        
        for retea in retele:
            if dry_run:
                logger.info(f"[SIMULARE] Ar șterge rețeaua: {retea}")
            else:
                subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                logger.info(f"Ștersă rețea: {retea}")
        
        # Volume
        rezultat = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True, text=True
        )
        volume = [v for v in rezultat.stdout.strip().split('\n') if v]
        
        for volum in volume:
            if dry_run:
                logger.info(f"[SIMULARE] Ar șterge volumul: {volum}")
            else:
                subprocess.run(["docker", "volume", "rm", volum], capture_output=True)
                logger.info(f"Șters volum: {volum}")
        
        return succes
    
    def curata_sistem(self) -> bool:
        """
        Curăță resursele Docker neutilizate.
        
        Returns:
            True dacă a reușit
        """
        logger.info("Curățare resurse Docker neutilizate...")
        rezultat = subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True,
            text=True
        )
        
        if rezultat.returncode == 0:
            logger.info("Curățare completă")
            return True
        else:
            logger.warning(f"Avertisment la curățare: {rezultat.stderr}")
            return False
