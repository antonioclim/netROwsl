#!/usr/bin/env python3
"""
Utilitare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Funcții pentru gestionarea containerelor Docker în laboratorul Săptămânii 7.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Any

from .logger import configureaza_logger

logger = configureaza_logger('docker_utils')


class ManagerDocker:
    """Clasă pentru gestionarea operațiunilor Docker Compose."""
    
    def __init__(self, director_docker: Path):
        """
        Inițializează managerul Docker.
        
        Args:
            director_docker: Calea către directorul cu docker-compose.yml
        """
        self.director_docker = director_docker
        self.fisier_compose = director_docker / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(
                f"Fișierul docker-compose.yml nu a fost găsit în {director_docker}"
            )
    
    def _ruleaza_compose(
        self,
        argumente: list[str],
        timeout: int = 120
    ) -> tuple[bool, str]:
        """
        Rulează o comandă docker compose.
        
        Args:
            argumente: Lista de argumente pentru docker compose
            timeout: Timeout în secunde
        
        Returns:
            Tuplu (succes, mesaj)
        """
        comanda = ["docker", "compose", "-f", str(self.fisier_compose)] + argumente
        
        try:
            rezultat = subprocess.run(
                comanda,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=self.director_docker
            )
            
            if rezultat.returncode == 0:
                return True, rezultat.stdout
            else:
                return False, rezultat.stderr
                
        except subprocess.TimeoutExpired:
            return False, f"Timeout după {timeout} secunde"
        except Exception as e:
            return False, str(e)
    
    def compose_up(
        self,
        detach: bool = True,
        profile: str | None = None,
        rebuild: bool = False
    ) -> bool:
        """
        Pornește serviciile definite în docker-compose.yml.
        
        Args:
            detach: Rulează în fundal
            profile: Profilul Docker Compose de activat
            rebuild: Reconstruiește imaginile
        
        Returns:
            True dacă pornirea a reușit
        """
        argumente = []
        
        if profile:
            argumente.extend(["--profile", profile])
        
        argumente.append("up")
        
        if detach:
            argumente.append("-d")
        
        if rebuild:
            argumente.append("--build")
        
        logger.info("Pornire containere Docker...")
        ok, mesaj = self._ruleaza_compose(argumente)
        
        if ok:
            logger.info("Containerele au fost pornite")
        else:
            logger.error(f"Eroare la pornirea containerelor: {mesaj}")
        
        return ok
    
    def compose_down(
        self,
        volumes: bool = False,
        dry_run: bool = False
    ) -> bool:
        """
        Oprește și elimină containerele.
        
        Args:
            volumes: Elimină și volumele asociate
            dry_run: Doar afișează ce s-ar face
        
        Returns:
            True dacă oprirea a reușit
        """
        if dry_run:
            logger.info("[SIMULARE] S-ar opri containerele")
            if volumes:
                logger.info("[SIMULARE] S-ar elimina și volumele")
            return True
        
        argumente = ["down"]
        
        if volumes:
            argumente.append("-v")
        
        logger.info("Oprire containere Docker...")
        ok, mesaj = self._ruleaza_compose(argumente)
        
        if ok:
            logger.info("Containerele au fost oprite")
        else:
            logger.error(f"Eroare la oprirea containerelor: {mesaj}")
        
        return ok
    
    def compose_build(self) -> bool:
        """
        Reconstruiește imaginile Docker.
        
        Returns:
            True dacă build-ul a reușit
        """
        logger.info("Reconstruire imagini Docker...")
        ok, mesaj = self._ruleaza_compose(["build"])
        
        if ok:
            logger.info("Imaginile au fost reconstruite")
        else:
            logger.error(f"Eroare la reconstruire: {mesaj}")
        
        return ok
    
    def verifica_servicii(self, servicii: dict[str, dict[str, Any]]) -> bool:
        """
        Verifică că toate serviciile rulează și sunt sănătoase.
        
        Args:
            servicii: Dicționar cu informații despre servicii
        
        Returns:
            True dacă toate serviciile sunt funcționale
        """
        toate_ok = True
        
        for nume, info in servicii.items():
            container = info.get("container", f"week7_{nume}")
            port = info.get("port")
            
            # Verifică că containerul rulează
            try:
                rezultat = subprocess.run(
                    ["docker", "inspect", "-f", "{{.State.Running}}", container],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if rezultat.returncode == 0 and "true" in rezultat.stdout.lower():
                    logger.info(f"  [OK] {nume} ({container}) rulează")
                else:
                    logger.error(f"  [EROARE] {nume} ({container}) nu rulează")
                    toate_ok = False
                    
            except Exception as e:
                logger.error(f"  [EROARE] Nu s-a putut verifica {nume}: {e}")
                toate_ok = False
        
        return toate_ok
    
    def afiseaza_status(self, servicii: dict[str, dict[str, Any]]):
        """
        Afișează statusul curent al serviciilor.
        
        Args:
            servicii: Dicționar cu informații despre servicii
        """
        logger.info("Status containere:")
        logger.info("-" * 50)
        
        ok, iesire = self._ruleaza_compose(["ps", "--format", "table"])
        
        if ok:
            print(iesire)
        else:
            logger.warning("Nu s-a putut obține statusul")
    
    def elimina_dupa_prefix(
        self,
        prefix: str,
        dry_run: bool = False
    ) -> bool:
        """
        Elimină containerele cu un anumit prefix în nume.
        
        Args:
            prefix: Prefixul de căutat
            dry_run: Doar afișează ce s-ar face
        
        Returns:
            True dacă eliminarea a reușit
        """
        try:
            # Găsește containerele
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{.Names}}"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            containere = [
                c for c in rezultat.stdout.strip().split('\n')
                if c and c.startswith(prefix)
            ]
            
            if not containere:
                logger.info(f"Niciun container cu prefixul '{prefix}' găsit")
                return True
            
            for container in containere:
                if dry_run:
                    logger.info(f"[SIMULARE] S-ar elimina: {container}")
                else:
                    logger.info(f"Eliminare container: {container}")
                    subprocess.run(
                        ["docker", "rm", "-f", container],
                        capture_output=True,
                        timeout=30
                    )
            
            return True
            
        except Exception as e:
            logger.error(f"Eroare la eliminarea containerelor: {e}")
            return False
    
    def system_prune(self) -> bool:
        """
        Curăță resursele Docker neutilizate.
        
        Returns:
            True dacă curățarea a reușit
        """
        logger.info("Curățare resurse Docker neutilizate...")
        
        try:
            rezultat = subprocess.run(
                ["docker", "system", "prune", "-f"],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if rezultat.returncode == 0:
                logger.info("Resursele au fost curățate")
                return True
            else:
                logger.error(f"Eroare la curățare: {rezultat.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Eroare la curățare: {e}")
            return False
