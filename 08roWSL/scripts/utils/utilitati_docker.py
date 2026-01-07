#!/usr/bin/env python3
"""
Utilități Docker
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Oferă funcții helper pentru gestionarea Docker.
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, List, Dict, Tuple


class GestionarDocker:
    """Clasă pentru gestionarea operațiunilor Docker."""
    
    def __init__(self, director_compose: Path):
        """
        Inițializează gestionarul Docker.
        
        Args:
            director_compose: Directorul care conține docker-compose.yml
        """
        self.director_compose = director_compose
    
    def compose_up(self, detasat: bool = True, construieste: bool = False) -> Tuple[bool, str]:
        """
        Pornește serviciile folosind docker compose up.
        
        Args:
            detasat: Rulează în background
            construieste: Construiește imaginile înainte de pornire
        
        Returns:
            Tuplu (succes, mesaj)
        """
        cmd = ["docker", "compose", "up"]
        if detasat:
            cmd.append("-d")
        if construieste:
            cmd.append("--build")
        
        return self._ruleaza_compose(cmd)
    
    def compose_down(self, volume: bool = False) -> Tuple[bool, str]:
        """
        Oprește și elimină serviciile.
        
        Args:
            volume: Elimină și volumele
        
        Returns:
            Tuplu (succes, mesaj)
        """
        cmd = ["docker", "compose", "down"]
        if volume:
            cmd.append("-v")
        
        return self._ruleaza_compose(cmd)
    
    def compose_build(self, fara_cache: bool = False) -> Tuple[bool, str]:
        """
        Construiește imaginile Docker.
        
        Args:
            fara_cache: Ignoră cache-ul
        
        Returns:
            Tuplu (succes, mesaj)
        """
        cmd = ["docker", "compose", "build"]
        if fara_cache:
            cmd.append("--no-cache")
        
        return self._ruleaza_compose(cmd)
    
    def _ruleaza_compose(self, cmd: List[str], timeout: int = 300) -> Tuple[bool, str]:
        """Rulează o comandă docker compose."""
        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.director_compose),
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode == 0:
                return True, result.stdout
            else:
                return False, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, "Timeout la executarea comenzii"
        except Exception as e:
            return False, str(e)
    
    def obtine_stare_containere(self) -> List[Dict]:
        """
        Obține starea containerelor din compose.
        
        Returns:
            Lista de dicționare cu informații despre containere
        """
        try:
            result = subprocess.run(
                ["docker", "compose", "ps", "--format", "json"],
                cwd=str(self.director_compose),
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                # Poate returna mai multe obiecte JSON, câte unul pe linie
                containere = []
                for linie in result.stdout.strip().split('\n'):
                    if linie:
                        containere.append(json.loads(linie))
                return containere
        except Exception:
            pass
        
        return []
    
    def verifica_servicii(self, servicii: Dict) -> bool:
        """
        Verifică dacă toate serviciile sunt sănătoase.
        
        Args:
            servicii: Dicționar cu configurația serviciilor
        
        Returns:
            True dacă toate serviciile sunt sănătoase
        """
        stare = self.obtine_stare_containere()
        
        if not stare:
            return False
        
        for container in stare:
            stare_container = container.get('State', '').lower()
            if stare_container not in ['running', 'healthy']:
                return False
        
        return True
    
    def elimina_dupa_prefix(self, prefix: str) -> Dict[str, int]:
        """
        Elimină resursele Docker care au un anumit prefix.
        
        Args:
            prefix: Prefixul pentru filtrare
        
        Returns:
            Dicționar cu numărul de resurse eliminate per tip
        """
        rezultat = {
            'containere': 0,
            'retele': 0,
            'volume': 0
        }
        
        # Elimină containere
        proc = subprocess.run(
            ["docker", "ps", "-aq", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        containere = [c for c in proc.stdout.strip().split('\n') if c]
        if containere:
            subprocess.run(["docker", "rm", "-f"] + containere, capture_output=True)
            rezultat['containere'] = len(containere)
        
        # Elimină rețele
        proc = subprocess.run(
            ["docker", "network", "ls", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        retele = [r for r in proc.stdout.strip().split('\n') if r]
        for retea in retele:
            subprocess.run(["docker", "network", "rm", retea], capture_output=True)
        rezultat['retele'] = len(retele)
        
        # Elimină volume
        proc = subprocess.run(
            ["docker", "volume", "ls", "-q", "--filter", f"name={prefix}"],
            capture_output=True,
            text=True
        )
        volume = [v for v in proc.stdout.strip().split('\n') if v]
        for vol in volume:
            subprocess.run(["docker", "volume", "rm", vol], capture_output=True)
        rezultat['volume'] = len(volume)
        
        return rezultat
    
    def curata_sistem(self) -> bool:
        """
        Curăță resursele Docker nefolosite.
        
        Returns:
            True dacă curățarea a reușit
        """
        result = subprocess.run(
            ["docker", "system", "prune", "-f"],
            capture_output=True
        )
        return result.returncode == 0
