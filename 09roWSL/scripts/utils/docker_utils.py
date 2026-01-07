#!/usr/bin/env python3
"""
Utilitare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Funcții helper pentru gestionarea containerelor Docker.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

from scripts.utils.logger import configureaza_logger

logger = configureaza_logger("docker_utils")


class ManagerDocker:
    """
    Manager pentru operațiuni Docker Compose.
    
    Oferă metode pentru pornirea, oprirea și gestionarea
    containerelor de laborator.
    
    Atribute:
        director_docker: Calea către directorul cu docker-compose.yml
        comanda_compose: Comanda Docker Compose (v2 sau v1)
        
    Exemplu:
        >>> manager = ManagerDocker(Path("./docker"))
        >>> manager.compose_up()
        >>> manager.verifica_servicii(SERVICII)
    """
    
    def __init__(self, director_docker: Path):
        """
        Inițializează managerul Docker.
        
        Argumente:
            director_docker: Calea către directorul Docker
        """
        self.director_docker = director_docker
        self.comanda_compose = self._detecteaza_compose()
    
    def _detecteaza_compose(self) -> List[str]:
        """
        Detectează versiunea Docker Compose disponibilă.
        
        Returnează:
            Lista de argumente pentru comanda compose
        """
        # Încearcă mai întâi Docker Compose V2
        try:
            rezultat = subprocess.run(
                ["docker", "compose", "version"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                logger.debug("Se folosește Docker Compose V2")
                return ["docker", "compose"]
        except Exception:
            pass
        
        # Fallback la Docker Compose V1
        try:
            rezultat = subprocess.run(
                ["docker-compose", "--version"],
                capture_output=True,
                timeout=10
            )
            if rezultat.returncode == 0:
                logger.debug("Se folosește Docker Compose V1")
                return ["docker-compose"]
        except Exception:
            pass
        
        logger.warning("Docker Compose nu a fost detectat")
        return ["docker", "compose"]  # Implicit
    
    def _ruleaza_compose(
        self,
        argumente: List[str],
        capteaza: bool = True
    ) -> subprocess.CompletedProcess:
        """
        Rulează o comandă Docker Compose.
        
        Argumente:
            argumente: Argumentele pentru comanda compose
            capteaza: Dacă să capteze output-ul
            
        Returnează:
            Rezultatul procesului
        """
        comanda = self.comanda_compose + argumente
        
        return subprocess.run(
            comanda,
            cwd=self.director_docker,
            capture_output=capteaza,
            text=True
        )
    
    def compose_up(self, detasat: bool = True, rebuild: bool = False) -> bool:
        """
        Pornește serviciile cu Docker Compose.
        
        Argumente:
            detasat: Rulare în fundal (implicit True)
            rebuild: Reconstruiește imaginile (implicit False)
            
        Returnează:
            True dacă a reușit, False altfel
        """
        argumente = ["up"]
        
        if detasat:
            argumente.append("-d")
        if rebuild:
            argumente.append("--build")
        
        logger.info("Se pornesc serviciile Docker...")
        rezultat = self._ruleaza_compose(argumente, capteaza=False)
        
        return rezultat.returncode == 0
    
    def compose_down(self, volume: bool = False, dry_run: bool = False) -> bool:
        """
        Oprește și elimină containerele.
        
        Argumente:
            volume: Elimină și volumele (implicit False)
            dry_run: Doar afișează ce ar face (implicit False)
            
        Returnează:
            True dacă a reușit, False altfel
        """
        argumente = ["down"]
        
        if volume:
            argumente.append("-v")
        
        if dry_run:
            logger.info(f"[SIMULARE] S-ar executa: {' '.join(self.comanda_compose + argumente)}")
            return True
        
        logger.info("Se opresc serviciile Docker...")
        rezultat = self._ruleaza_compose(argumente)
        
        return rezultat.returncode == 0
    
    def compose_build(self) -> bool:
        """
        Construiește imaginile Docker.
        
        Returnează:
            True dacă a reușit, False altfel
        """
        logger.info("Se construiesc imaginile Docker...")
        rezultat = self._ruleaza_compose(["build"], capteaza=False)
        
        return rezultat.returncode == 0
    
    def obtine_containere_active(self) -> List[str]:
        """
        Obține lista containerelor active.
        
        Returnează:
            Lista numelor containerelor active
        """
        rezultat = self._ruleaza_compose(["ps", "-q"])
        
        if rezultat.returncode != 0:
            return []
        
        return [c.strip() for c in rezultat.stdout.split('\n') if c.strip()]
    
    def verifica_servicii(self, servicii: Dict[str, Any]) -> bool:
        """
        Verifică dacă toate serviciile sunt sănătoase.
        
        Argumente:
            servicii: Dicționar cu definițiile serviciilor
            
        Returnează:
            True dacă toate serviciile sunt OK, False altfel
        """
        import socket
        
        toate_ok = True
        
        for nume, config in servicii.items():
            port = config.get("port")
            if not port:
                continue
            
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    rezultat = s.connect_ex(("localhost", port))
                    
                    if rezultat == 0:
                        logger.info(f"  ✓ {nume}: activ pe portul {port}")
                    else:
                        logger.error(f"  ✗ {nume}: nu răspunde pe portul {port}")
                        toate_ok = False
            except Exception as e:
                logger.error(f"  ✗ {nume}: eroare la verificare - {e}")
                toate_ok = False
        
        return toate_ok
    
    def afiseaza_stare(self, servicii: Dict[str, Any]) -> None:
        """
        Afișează starea curentă a serviciilor.
        
        Argumente:
            servicii: Dicționar cu definițiile serviciilor
        """
        logger.info("Starea serviciilor:")
        logger.info("-" * 40)
        
        # Afișează containerele active
        rezultat = self._ruleaza_compose(["ps"])
        if rezultat.returncode == 0:
            print(rezultat.stdout)
        
        # Verifică porturile
        logger.info("\nVerificare porturi:")
        self.verifica_servicii(servicii)
    
    def obtine_log_uri(self, serviciu: Optional[str] = None, linii: int = 50) -> str:
        """
        Obține log-urile containerelor.
        
        Argumente:
            serviciu: Numele serviciului (sau toate dacă None)
            linii: Numărul de linii de afișat
            
        Returnează:
            Log-urile ca string
        """
        argumente = ["logs", "--tail", str(linii)]
        
        if serviciu:
            argumente.append(serviciu)
        
        rezultat = self._ruleaza_compose(argumente)
        
        return rezultat.stdout if rezultat.returncode == 0 else ""
    
    def elimina_dupa_prefix(self, prefix: str, dry_run: bool = False) -> None:
        """
        Elimină resursele Docker cu un prefix specific.
        
        Argumente:
            prefix: Prefixul de căutat
            dry_run: Doar afișează ce ar face
        """
        # Elimină containerele
        rezultat = subprocess.run(
            ["docker", "ps", "-a", "--format", "{{.Names}}"],
            capture_output=True,
            text=True
        )
        
        for container in rezultat.stdout.split('\n'):
            if container.startswith(prefix):
                if dry_run:
                    logger.info(f"[SIMULARE] S-ar elimina containerul: {container}")
                else:
                    subprocess.run(
                        ["docker", "rm", "-f", container],
                        capture_output=True
                    )
                    logger.info(f"Eliminat containerul: {container}")
        
        # Elimină rețelele
        rezultat = subprocess.run(
            ["docker", "network", "ls", "--format", "{{.Name}}"],
            capture_output=True,
            text=True
        )
        
        for retea in rezultat.stdout.split('\n'):
            if retea.startswith(prefix) or f"_{prefix}" in retea:
                if dry_run:
                    logger.info(f"[SIMULARE] S-ar elimina rețeaua: {retea}")
                else:
                    subprocess.run(
                        ["docker", "network", "rm", retea],
                        capture_output=True
                    )
                    logger.info(f"Eliminată rețeaua: {retea}")
    
    def curata_sistem(self) -> None:
        """Curăță resursele Docker neutilizate."""
        logger.info("Se curăță resursele Docker neutilizate...")
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )


# Alias-uri pentru compatibilitate cu versiunea engleză
DockerManager = ManagerDocker


if __name__ == "__main__":
    # Test
    from pathlib import Path
    
    director_test = Path(__file__).parent.parent.parent / "docker"
    manager = ManagerDocker(director_test)
    
    print(f"Comandă Compose: {' '.join(manager.comanda_compose)}")
    print(f"Director Docker: {manager.director_docker}")
