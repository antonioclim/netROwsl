#!/usr/bin/env python3
"""
Utilitare pentru Managementul Docker
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Oferă funcționalitate pentru gestionarea containerelor și serviciilor Docker.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

from .logger import configureaza_logger

logger = configureaza_logger("utilitare_docker")


class ManagerDocker:
    """
    Manager pentru operațiuni Docker Compose și container.
    
    Oferă o interfață simplificată pentru comenzile Docker comune
    utilizate în mediul de laborator.
    """
    
    def __init__(self, director_docker: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_docker: Calea către directorul cu fișierele Docker
        """
        self.director_docker = Path(director_docker)
        self.fisier_compose = self.director_docker / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            logger.warning(f"Fișierul docker-compose.yml nu a fost găsit în {self.director_docker}")
    
    def _executa_compose(self, *args, captura: bool = False) -> subprocess.CompletedProcess:
        """
        Execută o comandă docker compose.
        
        Args:
            *args: Argumentele pentru docker compose
            captura: Dacă să captureze output-ul
        
        Returns:
            Rezultatul procesului
        """
        cmd = ["docker", "compose", "-f", str(self.fisier_compose)] + list(args)
        
        if captura:
            return subprocess.run(cmd, capture_output=True, text=True)
        else:
            return subprocess.run(cmd)
    
    def _executa_docker(self, *args, captura: bool = False) -> subprocess.CompletedProcess:
        """
        Execută o comandă docker.
        
        Args:
            *args: Argumentele pentru docker
            captura: Dacă să captureze output-ul
        
        Returns:
            Rezultatul procesului
        """
        cmd = ["docker"] + list(args)
        
        if captura:
            return subprocess.run(cmd, capture_output=True, text=True)
        else:
            return subprocess.run(cmd)
    
    def compose_up(self, detasat: bool = True, construieste: bool = False) -> bool:
        """
        Pornește serviciile definite în docker-compose.yml.
        
        Args:
            detasat: Rulează în background (implicit: True)
            construieste: Construiește imaginile înainte de pornire
        
        Returns:
            True dacă pornirea a reușit
        """
        args = ["up"]
        
        if detasat:
            args.append("-d")
        
        if construieste:
            args.append("--build")
        
        rezultat = self._executa_compose(*args)
        return rezultat.returncode == 0
    
    def compose_down(self, volume: bool = False, simulare: bool = False) -> bool:
        """
        Oprește și elimină containerele.
        
        Args:
            volume: Elimină și volumele asociate
            simulare: Doar afișează ce s-ar face
        
        Returns:
            True dacă operațiunea a reușit
        """
        if simulare:
            args_afisare = ["down"]
            if volume:
                args_afisare.append("-v")
            logger.info(f"[SIMULARE] docker compose {' '.join(args_afisare)}")
            return True
        
        args = ["down"]
        if volume:
            args.append("-v")
        
        rezultat = self._executa_compose(*args)
        return rezultat.returncode == 0
    
    def compose_stop(self, timeout: int = 10) -> bool:
        """
        Oprește serviciile fără a le elimina.
        
        Args:
            timeout: Timpul de așteptare pentru oprire grațioasă (secunde)
        
        Returns:
            True dacă oprirea a reușit
        """
        rezultat = self._executa_compose("stop", "-t", str(timeout))
        return rezultat.returncode == 0
    
    def compose_kill(self) -> bool:
        """
        Oprește forțat serviciile (SIGKILL).
        
        Returns:
            True dacă operațiunea a reușit
        """
        rezultat = self._executa_compose("kill")
        return rezultat.returncode == 0
    
    def compose_build(self, fara_cache: bool = False) -> bool:
        """
        Construiește imaginile definite în docker-compose.yml.
        
        Args:
            fara_cache: Construiește fără a folosi cache-ul
        
        Returns:
            True dacă construirea a reușit
        """
        args = ["build"]
        
        if fara_cache:
            args.append("--no-cache")
        
        rezultat = self._executa_compose(*args)
        return rezultat.returncode == 0
    
    def compose_logs(self, serviciu: str = None, urmareste: bool = False, linii: int = 100) -> None:
        """
        Afișează jurnalele serviciilor.
        
        Args:
            serviciu: Numele serviciului specific (None pentru toate)
            urmareste: Urmărește jurnalele în timp real
            linii: Numărul de linii din istoric
        """
        args = ["logs", f"--tail={linii}"]
        
        if urmareste:
            args.append("-f")
        
        if serviciu:
            args.append(serviciu)
        
        self._executa_compose(*args)
    
    def verifica_servicii(self, servicii: Dict[str, Dict]) -> bool:
        """
        Verifică dacă toate serviciile sunt active și sănătoase.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        
        Returns:
            True dacă toate serviciile sunt active
        """
        toate_active = True
        
        rezultat = self._executa_docker("ps", "--format", "{{.Names}}\t{{.Status}}", captura=True)
        containere_active = {}
        
        for linie in rezultat.stdout.strip().split('\n'):
            if '\t' in linie:
                nume, status = linie.split('\t', 1)
                containere_active[nume] = status
        
        for nume, config in servicii.items():
            container = config.get("container", f"week5_{nume}")
            
            if container in containere_active:
                status = containere_active[container]
                if "Up" in status:
                    logger.info(f"  ✓ {container}: Activ ({status})")
                else:
                    logger.warning(f"  ⚠ {container}: {status}")
                    toate_active = False
            else:
                logger.error(f"  ✗ {container}: Nu rulează")
                toate_active = False
        
        return toate_active
    
    def afiseaza_status(self, servicii: Dict[str, Dict]) -> None:
        """
        Afișează starea detaliată a serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        """
        print()
        print("┌─ STARE SERVICII")
        print("│")
        
        self.verifica_servicii(servicii)
        
        print("│")
        print("└" + "─" * 50)
        print()
        
        # Afișează informații despre rețea
        print("┌─ REȚELE DOCKER")
        print("│")
        
        rezultat = self._executa_docker(
            "network", "ls", 
            "--format", "{{.Name}}\t{{.Driver}}\t{{.Scope}}",
            "--filter", "name=week5",
            captura=True
        )
        
        if rezultat.stdout.strip():
            for linie in rezultat.stdout.strip().split('\n'):
                parti = linie.split('\t')
                if len(parti) >= 3:
                    print(f"│  {parti[0]:25} Driver: {parti[1]:10} Scop: {parti[2]}")
        else:
            print("│  Nu există rețele week5_* active")
        
        print("│")
        print("└" + "─" * 50)
    
    def elimina_dupa_prefix(self, prefix: str, simulare: bool = False) -> None:
        """
        Elimină toate resursele Docker cu un anumit prefix.
        
        Args:
            prefix: Prefixul de căutat (ex: "week5")
            simulare: Doar afișează ce s-ar elimina
        """
        # Elimină containerele
        rezultat = self._executa_docker(
            "ps", "-aq", "--filter", f"name={prefix}",
            captura=True
        )
        
        containere = rezultat.stdout.strip().split('\n')
        containere = [c for c in containere if c]
        
        if containere:
            if simulare:
                logger.info(f"[SIMULARE] Ar elimina {len(containere)} containere")
            else:
                logger.info(f"Eliminare {len(containere)} containere...")
                self._executa_docker("rm", "-f", *containere)
        
        # Elimină rețelele
        rezultat = self._executa_docker(
            "network", "ls", "-q", "--filter", f"name={prefix}",
            captura=True
        )
        
        retele = rezultat.stdout.strip().split('\n')
        retele = [r for r in retele if r]
        
        if retele:
            if simulare:
                logger.info(f"[SIMULARE] Ar elimina {len(retele)} rețele")
            else:
                logger.info(f"Eliminare {len(retele)} rețele...")
                for retea in retele:
                    self._executa_docker("network", "rm", retea)
        
        # Elimină volumele
        rezultat = self._executa_docker(
            "volume", "ls", "-q", "--filter", f"name={prefix}",
            captura=True
        )
        
        volume = rezultat.stdout.strip().split('\n')
        volume = [v for v in volume if v]
        
        if volume:
            if simulare:
                logger.info(f"[SIMULARE] Ar elimina {len(volume)} volume")
            else:
                logger.info(f"Eliminare {len(volume)} volume...")
                for vol in volume:
                    self._executa_docker("volume", "rm", vol)
    
    def system_prune(self, toate: bool = False) -> bool:
        """
        Curăță resursele Docker neutilizate.
        
        Args:
            toate: Include și imaginile neutilizate
        
        Returns:
            True dacă curățarea a reușit
        """
        args = ["system", "prune", "-f"]
        
        if toate:
            args.append("-a")
        
        rezultat = self._executa_docker(*args)
        return rezultat.returncode == 0
    
    def exec_in_container(
        self, 
        container: str, 
        comanda: List[str],
        interactiv: bool = False
    ) -> subprocess.CompletedProcess:
        """
        Execută o comandă într-un container.
        
        Args:
            container: Numele containerului
            comanda: Comanda de executat
            interactiv: Mod interactiv (-it)
        
        Returns:
            Rezultatul execuției
        """
        args = ["exec"]
        
        if interactiv:
            args.extend(["-it"])
        
        args.append(container)
        args.extend(comanda)
        
        return self._executa_docker(*args, captura=not interactiv)


def verifica_docker_instalat() -> bool:
    """
    Verifică dacă Docker este instalat și accesibil.
    
    Returns:
        True dacă Docker este disponibil
    """
    try:
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=5
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def verifica_docker_activ() -> bool:
    """
    Verifică dacă daemonul Docker rulează.
    
    Returns:
        True dacă Docker daemon este activ
    """
    try:
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


# Alias pentru compatibilitate cu codul existent în limba engleză
DockerManager = ManagerDocker
