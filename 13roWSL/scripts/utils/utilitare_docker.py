#!/usr/bin/env python3
"""
Utilitare Docker
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Furnizează funcții pentru gestionarea containerelor Docker.
"""

import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional


class ManagerDocker:
    """
    Manager pentru operațiuni Docker Compose.
    
    Attributes:
        director_docker: Calea către directorul cu docker-compose.yml
    """
    
    def __init__(self, director_docker: Path):
        """
        Inițializează manager-ul Docker.
        
        Args:
            director_docker: Calea către directorul cu fișierul docker-compose.yml
        """
        self.director_docker = Path(director_docker)
        self.fisier_compose = self.director_docker / "docker-compose.yml"
        
        if not self.fisier_compose.exists():
            raise FileNotFoundError(
                f"Fișierul docker-compose.yml nu a fost găsit în {self.director_docker}"
            )
    
    def _ruleaza_compose(self, *args, capture: bool = False) -> subprocess.CompletedProcess:
        """
        Rulează o comandă docker compose.
        
        Args:
            *args: Argumentele pentru docker compose
            capture: Dacă să captureze output-ul
        
        Returns:
            Rezultatul comenzii subprocess
        """
        comanda = ["docker", "compose", "-f", str(self.fisier_compose)] + list(args)
        
        return subprocess.run(
            comanda,
            capture_output=capture,
            text=True,
            cwd=str(self.director_docker)
        )
    
    def compose_up(self, detach: bool = True, build: bool = False):
        """
        Pornește serviciile definite în docker-compose.yml.
        
        Args:
            detach: Rulează în fundal (implicit True)
            build: Reconstruiește imaginile înainte de pornire
        """
        args = ["up"]
        if detach:
            args.append("-d")
        if build:
            args.append("--build")
        
        rezultat = self._ruleaza_compose(*args)
        if rezultat.returncode != 0:
            raise RuntimeError("Eroare la pornirea containerelor Docker")
    
    def compose_down(self, volumes: bool = False, timeout: int = 10):
        """
        Oprește și elimină containerele.
        
        Args:
            volumes: Elimină și volumele asociate
            timeout: Timpul de așteptare pentru oprire graceful
        """
        args = ["down", "-t", str(timeout)]
        if volumes:
            args.append("-v")
        
        self._ruleaza_compose(*args)
    
    def compose_build(self, no_cache: bool = False):
        """
        Construiește imaginile Docker.
        
        Args:
            no_cache: Nu folosește cache-ul (reconstruire completă)
        """
        args = ["build"]
        if no_cache:
            args.append("--no-cache")
        
        self._ruleaza_compose(*args)
    
    def compose_ps(self) -> str:
        """
        Returnează starea serviciilor.
        
        Returns:
            Output-ul comenzii docker compose ps
        """
        rezultat = self._ruleaza_compose("ps", capture=True)
        return rezultat.stdout
    
    def afiseaza_loguri(self, serviciu: Optional[str] = None, linii: int = 50):
        """
        Afișează log-urile containerelor.
        
        Args:
            serviciu: Numele serviciului (None pentru toate)
            linii: Numărul de linii de afișat
        """
        args = ["logs", "--tail", str(linii)]
        if serviciu:
            args.append(serviciu)
        
        self._ruleaza_compose(*args)
    
    def listeaza_containere(self) -> List[Dict]:
        """
        Returnează lista containerelor Docker.
        
        Returns:
            Listă de dicționare cu informații despre containere
        """
        try:
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "--format", "{{json .}}"],
                capture_output=True,
                text=True
            )
            
            containere = []
            for linie in rezultat.stdout.strip().split('\n'):
                if linie:
                    try:
                        containere.append(json.loads(linie))
                    except json.JSONDecodeError:
                        continue
            
            return containere
        except Exception:
            return []
    
    def verifica_serviciu(self, nume_container: str) -> bool:
        """
        Verifică dacă un container rulează.
        
        Args:
            nume_container: Numele containerului de verificat
        
        Returns:
            True dacă containerul rulează
        """
        try:
            rezultat = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", nume_container],
                capture_output=True,
                text=True
            )
            return rezultat.stdout.strip().lower() == "true"
        except Exception:
            return False
    
    def elimina_dupa_prefix(self, prefix: str, simulare: bool = False):
        """
        Elimină toate resursele Docker cu un anumit prefix.
        
        Args:
            prefix: Prefixul de căutat (ex: "week13")
            simulare: Doar afișează, nu șterge
        """
        # Containere
        try:
            rezultat = subprocess.run(
                ["docker", "ps", "-a", "-q", "--filter", f"name={prefix}"],
                capture_output=True,
                text=True
            )
            containere = rezultat.stdout.strip().split('\n')
            containere = [c for c in containere if c]
            
            if containere:
                if simulare:
                    print(f"  [SIMULARE] Ar șterge {len(containere)} containere")
                else:
                    subprocess.run(["docker", "rm", "-f"] + containere, capture_output=True)
                    print(f"  [ȘTERS] {len(containere)} containere")
        except Exception:
            pass
        
        # Rețele
        try:
            rezultat = subprocess.run(
                ["docker", "network", "ls", "-q", "--filter", f"name={prefix}"],
                capture_output=True,
                text=True
            )
            retele = rezultat.stdout.strip().split('\n')
            retele = [r for r in retele if r]
            
            if retele:
                if simulare:
                    print(f"  [SIMULARE] Ar șterge {len(retele)} rețele")
                else:
                    for retea in retele:
                        subprocess.run(["docker", "network", "rm", retea], capture_output=True)
                    print(f"  [ȘTERS] {len(retele)} rețele")
        except Exception:
            pass
        
        # Volume
        try:
            rezultat = subprocess.run(
                ["docker", "volume", "ls", "-q", "--filter", f"name={prefix}"],
                capture_output=True,
                text=True
            )
            volume = rezultat.stdout.strip().split('\n')
            volume = [v for v in volume if v]
            
            if volume:
                if simulare:
                    print(f"  [SIMULARE] Ar șterge {len(volume)} volume")
                else:
                    for vol in volume:
                        subprocess.run(["docker", "volume", "rm", vol], capture_output=True)
                    print(f"  [ȘTERS] {len(volume)} volume")
        except Exception:
            pass
    
    def curata_sistem(self):
        """Rulează docker system prune pentru curățare generală."""
        subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )
        print("  [OK] Curățare sistem Docker completă")


# Alias pentru compatibilitate
DockerManager = ManagerDocker
