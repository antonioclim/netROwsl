#!/usr/bin/env python3
"""
Utilitare Docker pentru Management
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Oferă o interfață Python pentru gestionarea Docker Compose și containerelor.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

from .logger import configureaza_logger


class ManagerDocker:
    """Manager pentru operațiuni Docker și Docker Compose."""
    
    def __init__(self, director_docker: Path) -> None:
        """Inițializează managerul Docker.
        
        Args:
            director_docker: Calea către directorul cu docker-compose.yml
        """
        self.director_docker = director_docker
        self.fisier_compose = director_docker / "docker-compose.yml"
        self.logger = configureaza_logger("docker")
        
        if not self.fisier_compose.exists():
            self.logger.warning(f"Fișierul compose nu există: {self.fisier_compose}")

    def _ruleaza_compose(
        self,
        comanda: List[str],
        capteaza_iesire: bool = False
    ) -> subprocess.CompletedProcess:
        """Rulează o comandă Docker Compose.
        
        Args:
            comanda: Lista de argumente pentru docker compose
            capteaza_iesire: Capturează stdout/stderr
            
        Returns:
            Rezultatul procesului
        """
        cmd_completa = ["docker", "compose", "-f", str(self.fisier_compose)] + comanda
        
        self.logger.debug(f"Se execută: {' '.join(cmd_completa)}")
        
        return subprocess.run(
            cmd_completa,
            capture_output=capteaza_iesire,
            text=True,
            cwd=self.director_docker
        )

    def compose_up(self, detasat: bool = True, profiluri: Optional[List[str]] = None) -> bool:
        """Pornește serviciile definite în docker-compose.yml.
        
        Args:
            detasat: Rulează în background
            profiluri: Lista de profiluri de activat
            
        Returns:
            True dacă a reușit
        """
        self.logger.info("Se pornesc containerele...")
        
        cmd = ["up"]
        if detasat:
            cmd.append("-d")
        
        if profiluri:
            for profil in profiluri:
                cmd.extend(["--profile", profil])
        
        rezultat = self._ruleaza_compose(cmd)
        
        if rezultat.returncode == 0:
            self.logger.info("Containerele au fost pornite cu succes")
            return True
        else:
            self.logger.error("Eroare la pornirea containerelor")
            return False

    def compose_down(self, volume: bool = False, dry_run: bool = False) -> bool:
        """Oprește și elimină containerele.
        
        Args:
            volume: Elimină și volumele
            dry_run: Doar afișează ce ar face
            
        Returns:
            True dacă a reușit
        """
        if dry_run:
            self.logger.info("[SIMULARE] S-ar opri containerele")
            return True
        
        self.logger.info("Se opresc containerele...")
        
        cmd = ["down"]
        if volume:
            cmd.append("-v")
        
        rezultat = self._ruleaza_compose(cmd)
        
        if rezultat.returncode == 0:
            self.logger.info("Containerele au fost oprite cu succes")
            return True
        else:
            self.logger.error("Eroare la oprirea containerelor")
            return False

    def compose_build(self, fara_cache: bool = False) -> bool:
        """Construiește imaginile Docker.
        
        Args:
            fara_cache: Construiește fără cache
            
        Returns:
            True dacă a reușit
        """
        self.logger.info("Se construiesc imaginile Docker...")
        
        cmd = ["build"]
        if fara_cache:
            cmd.append("--no-cache")
        
        rezultat = self._ruleaza_compose(cmd)
        
        if rezultat.returncode == 0:
            self.logger.info("Imaginile au fost construite cu succes")
            return True
        else:
            self.logger.error("Eroare la construirea imaginilor")
            return False

    def obtine_stare_container(self, nume_container: str) -> Optional[str]:
        """Obține starea unui container specific.
        
        Args:
            nume_container: Numele containerului
            
        Returns:
            Starea containerului sau None
        """
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Status}}", nume_container],
                capture_output=True,
                text=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                return rezultat.stdout.strip()
        except Exception:
            pass
        return None

    def asteapta_container(
        self,
        nume_container: str,
        timeout: int = 60,
        interval: float = 2.0
    ) -> bool:
        """Așteaptă ca un container să fie gata.
        
        Args:
            nume_container: Numele containerului
            timeout: Timeout în secunde
            interval: Interval între verificări
            
        Returns:
            True dacă containerul este gata
        """
        self.logger.info(f"Se așteaptă containerul {nume_container}...")
        
        timp_start = time.time()
        while time.time() - timp_start < timeout:
            stare = self.obtine_stare_container(nume_container)
            if stare == "running":
                self.logger.info(f"Containerul {nume_container} este gata")
                return True
            time.sleep(interval)
        
        self.logger.error(f"Timeout în așteptarea containerului {nume_container}")
        return False

    def verifica_servicii(self, servicii: Dict[str, Dict[str, Any]]) -> bool:
        """Verifică starea serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
            
        Returns:
            True dacă toate serviciile sunt funcționale
        """
        toate_ok = True
        
        for nume, config in servicii.items():
            container = config.get("container", nume)
            stare = self.obtine_stare_container(container)
            
            if stare == "running":
                self.logger.info(f"✓ {nume}: rulează")
            else:
                self.logger.error(f"✗ {nume}: {stare or 'nu există'}")
                toate_ok = False
        
        return toate_ok

    def elimina_dupa_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """Elimină resursele Docker care încep cu un prefix.
        
        Args:
            prefix: Prefixul de căutat
            dry_run: Doar afișează ce ar face
        """
        # Elimină containerele
        self.logger.info(f"Se caută containerele cu prefix '{prefix}'...")
        
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        
        containere = rezultat.stdout.strip().split()
        if containere and containere[0]:
            for container in containere:
                if dry_run:
                    self.logger.info(f"[SIMULARE] S-ar elimina containerul: {container}")
                else:
                    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
                    self.logger.info(f"Eliminat containerul: {container}")
        
        # Elimină rețelele
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "-q"],
            capture_output=True,
            text=True
        )
        
        retele = rezultat.stdout.strip().split()
        if retele and retele[0]:
            for retea in retele:
                if dry_run:
                    self.logger.info(f"[SIMULARE] S-ar elimina rețeaua: {retea}")
                else:
                    subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                    self.logger.info(f"Eliminată rețeaua: {retea}")

    def executa_in_container(
        self,
        container: str,
        comanda: List[str],
        interactiv: bool = False
    ) -> subprocess.CompletedProcess:
        """Execută o comandă într-un container.
        
        Args:
            container: Numele containerului
            comanda: Comanda de executat
            interactiv: Mod interactiv
            
        Returns:
            Rezultatul execuției
        """
        cmd = ["docker", "exec"]
        if interactiv:
            cmd.extend(["-it"])
        cmd.append(container)
        cmd.extend(comanda)
        
        return subprocess.run(cmd, capture_output=not interactiv, text=True)

    def curatare_sistem(self) -> None:
        """Curăță resursele Docker neutilizate."""
        self.logger.info("Se curăță resursele Docker neutilizate...")
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )
        self.logger.info("Curățare completă")

    def afiseaza_stare(self, servicii: Dict[str, Dict[str, Any]]) -> None:
        """Afișează starea detaliată a serviciilor.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        """
        print("\n" + "=" * 60)
        print("  STARE SERVICII LABORATOR")
        print("=" * 60 + "\n")
        
        for nume, config in servicii.items():
            container = config.get("container", nume)
            port = config.get("port", "N/A")
            stare = self.obtine_stare_container(container)
            
            if stare == "running":
                simbol = "✓"
                culoare = "\033[92m"  # Verde
            else:
                simbol = "✗"
                culoare = "\033[91m"  # Roșu
            
            reset = "\033[0m"
            print(f"  {culoare}{simbol}{reset} {nume:20} Port: {port:10} Stare: {stare or 'oprit'}")
        
        print("\n" + "=" * 60 + "\n")
