#!/usr/bin/env python3
"""
Utilitare de gestionare Docker
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Furnizează funcții auxiliare pentru gestionarea containerelor și a compose-ului Docker.
"""

from __future__ import annotations

import subprocess
import time
from pathlib import Path
from typing import Optional

from .logger import setup_logger

logger = setup_logger("docker_utils")


class DockerManager:
    """
    Gestionează operațiunile Docker Compose pentru mediul de laborator.
    """
    
    def __init__(self, director_compose: Path):
        """
        Inițializează managerul Docker.
        
        Argumente:
            director_compose: Calea către directorul care conține docker-compose.yml
        """
        self.director_compose = Path(director_compose)
        self.fisier_compose = self.director_compose / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(f"docker-compose.yml nu a fost găsit în {director_compose}")
    
    def _ruleaza_compose(
        self,
        *argumente: str,
        capteaza_output: bool = False,
        verifica: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Argumente:
            *argumente: Argumentele comenzii
            capteaza_output: Dacă să captureze stdout/stderr
            verifica: Dacă să ridice excepție la ieșire non-zero
            
        Returnează:
            Rezultat CompletedProcess
        """
        cmd = ["docker", "compose", "-f", str(self.fisier_compose)] + list(argumente)
        logger.debug(f"Execut: {' '.join(cmd)}")
        
        return subprocess.run(
            cmd,
            cwd=self.director_compose,
            capture_output=capteaza_output,
            text=True,
            check=verifica
        )
    
    def compose_build(self, serviciu: Optional[str] = None, fara_cache: bool = False) -> bool:
        """
        Construiește imaginile Docker.
        
        Argumente:
            serviciu: Serviciul specific de construit (None pentru toate)
            fara_cache: Dacă să construiască fără cache
            
        Returnează:
            True dacă operația a reușit
        """
        argumente = ["build"]
        if fara_cache:
            argumente.append("--no-cache")
        if serviciu:
            argumente.append(serviciu)
        
        try:
            self._ruleaza_compose(*argumente)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Construirea a eșuat: {e}")
            return False
    
    def compose_up(
        self,
        servicii: Optional[list[str]] = None,
        detach: bool = True,
        profiles: Optional[list[str]] = None
    ) -> bool:
        """
        Pornește serviciile Docker Compose.
        
        Argumente:
            servicii: Lista de servicii de pornit (None pentru toate)
            detach: Rulează în mod detașat
            profiles: Lista de profile de activat
            
        Returnează:
            True dacă operația a reușit
        """
        argumente = []
        
        if profiles:
            for profil in profiles:
                argumente.extend(["--profile", profil])
        
        argumente.append("up")
        
        if detach:
            argumente.append("-d")
        
        if servicii:
            argumente.extend(servicii)
        
        try:
            self._ruleaza_compose(*argumente)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Eșec la pornirea serviciilor: {e}")
            return False
    
    def compose_down(
        self,
        volumes: bool = False,
        elimina_orfani: bool = True,
        dry_run: bool = False
    ) -> bool:
        """
        Oprește și elimină serviciile Docker Compose.
        
        Argumente:
            volumes: Elimină și volumele
            elimina_orfani: Elimină containerele orfane
            dry_run: Doar afișează ce s-ar face
            
        Returnează:
            True dacă operația a reușit
        """
        if dry_run:
            logger.info("[SIMULARE] Ar rula: docker compose down")
            return True
        
        argumente = ["down"]
        
        if volumes:
            argumente.append("-v")
        
        if elimina_orfani:
            argumente.append("--remove-orphans")
        
        try:
            self._ruleaza_compose(*argumente)
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Eșec la oprirea serviciilor: {e}")
            return False
    
    def compose_ps(self) -> dict[str, dict]:
        """
        Obține starea serviciilor compose.
        
        Returnează:
            Dicționar de nume serviciu la informații despre stare
        """
        try:
            rezultat = self._ruleaza_compose("ps", "--format", "json", capteaza_output=True)
            import json
            servicii = {}
            for linie in rezultat.stdout.strip().split('\n'):
                if linie:
                    try:
                        svc = json.loads(linie)
                        servicii[svc.get('Service', svc.get('Name', 'necunoscut'))] = svc
                    except json.JSONDecodeError:
                        pass
            return servicii
        except Exception as e:
            logger.error(f"Eșec la obținerea stării serviciilor: {e}")
            return {}
    
    def show_status(self, servicii_asteptate: dict) -> None:
        """
        Afișează starea serviciilor așteptate.
        
        Argumente:
            servicii_asteptate: Dicționar de configurații servicii
        """
        in_executie = self.compose_ps()
        
        print("\nStarea serviciilor:")
        print("-" * 60)
        
        for nume, config in servicii_asteptate.items():
            container = config.get("container", nume)
            port = config.get("port", "N/A")
            
            if container in in_executie:
                stare = in_executie[container].get("State", "necunoscută")
                if stare == "running":
                    print(f"  [✓] {nume:<20} Port: {port:<8} Stare: {stare}")
                else:
                    print(f"  [!] {nume:<20} Port: {port:<8} Stare: {stare}")
            else:
                print(f"  [✗] {nume:<20} Port: {port:<8} Stare: nu rulează")
        
        print("-" * 60)
    
    def verify_services(
        self,
        servicii: dict,
        timeout: int = 30
    ) -> bool:
        """
        Verifică dacă toate serviciile sunt sănătoase.
        
        Argumente:
            servicii: Dicționar de configurații servicii
            timeout: Timpul maxim de așteptare pentru servicii
            
        Returnează:
            True dacă toate serviciile sunt sănătoase
        """
        import requests
        
        timp_start = time.time()
        toate_sanatoase = True
        
        for nume, config in servicii.items():
            verificare_sanatate = config.get("health_check")
            timp_pornire = config.get("startup_time", 5)
            port = config.get("port")
            
            logger.info(f"Verific {nume}...")
            
            # Așteaptă timpul de pornire
            time.sleep(min(timp_pornire, timeout - (time.time() - timp_start)))
            
            if verificare_sanatate and port:
                url = f"http://localhost:{port}{verificare_sanatate}"
                try:
                    raspuns = requests.get(url, timeout=5)
                    if raspuns.status_code < 500:
                        logger.info(f"  ✓ {nume} este sănătos")
                    else:
                        logger.warning(f"  ! {nume} a returnat status {raspuns.status_code}")
                        toate_sanatoase = False
                except requests.RequestException as e:
                    logger.warning(f"  ! Verificarea sănătății {nume} a eșuat: {e}")
                    # Nu neapărat nesănătos, doar fără endpoint HTTP
            else:
                # Fără verificare de sănătate definită, presupunem OK dacă containerul rulează
                in_executie = self.compose_ps()
                container = config.get("container", nume)
                if container in in_executie and in_executie[container].get("State") == "running":
                    logger.info(f"  ✓ {nume} rulează")
                else:
                    logger.error(f"  ✗ {nume} nu rulează")
                    toate_sanatoase = False
        
        return toate_sanatoase
    
    def remove_by_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Elimină containerele, rețelele și volumele cu un prefix dat.
        
        Argumente:
            prefix: Prefixul de potrivit
            dry_run: Doar afișează ce s-ar face
        """
        # Elimină containerele
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--filter", f"name={prefix}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        containere = rezultat.stdout.strip().split('\n')
        containere = [c for c in containere if c]
        
        for container in containere:
            if dry_run:
                logger.info(f"[SIMULARE] Ar elimina containerul: {container}")
            else:
                logger.info(f"Elimin containerul: {container}")
                subprocess.run(["docker", "rm", "-f", container], capture_output=True)
        
        # Elimină rețelele
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        retele = rezultat.stdout.strip().split('\n')
        retele = [n for n in retele if n and n != "bridge" and n != "host" and n != "none"]
        
        for retea in retele:
            if dry_run:
                logger.info(f"[SIMULARE] Ar elimina rețeaua: {retea}")
            else:
                logger.info(f"Elimin rețeaua: {retea}")
                subprocess.run(["docker", "network", "rm", retea], capture_output=True)
        
        # Elimină volumele
        rezultat = subprocess.run(
            ["docker", "volume", "ls", "--filter", f"name={prefix}", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        volume = rezultat.stdout.strip().split('\n')
        volume = [v for v in volume if v]
        
        for volum in volume:
            if dry_run:
                logger.info(f"[SIMULARE] Ar elimina volumul: {volum}")
            else:
                logger.info(f"Elimin volumul: {volum}")
                subprocess.run(["docker", "volume", "rm", volum], capture_output=True)
    
    def system_prune(self, toate_neutilizate: bool = False) -> None:
        """
        Elimină resursele Docker neutilizate.
        
        Argumente:
            toate_neutilizate: Elimină toate imaginile neutilizate, nu doar cele dangling
        """
        argumente = ["docker", "system", "prune", "-f"]
        if toate_neutilizate:
            argumente.append("-a")
        
        subprocess.run(argumente)
