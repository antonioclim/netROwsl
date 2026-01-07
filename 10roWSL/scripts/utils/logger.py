#!/usr/bin/env python3
"""
Modul de Logging pentru Scripturi
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă logging consistent pentru toate scripturile de laborator.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


class FormatatorColor(logging.Formatter):
    """Formatator cu suport pentru culori în terminal."""
    
    # Coduri ANSI pentru culori
    CULORI = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Galben
        'ERROR': '\033[31m',      # Roșu
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m',       # Reset
    }
    
    def format(self, record):
        # Adaugă culoare pentru nivel
        nivel_culoare = self.CULORI.get(record.levelname, self.CULORI['RESET'])
        reset = self.CULORI['RESET']
        
        # Format: [NIVEL] mesaj
        record.levelname = f"{nivel_culoare}{record.levelname:8}{reset}"
        return super().format(record)


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier_log: Path = None,
    cu_culori: bool = True
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul minim de logging (default: INFO)
        fisier_log: Calea opțională către fișierul de log
        cu_culori: Dacă să folosească culori în terminal
    
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evită duplicarea handler-elor
    if logger.handlers:
        return logger
    
    # Handler pentru consolă
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    
    if cu_culori and sys.stdout.isatty():
        formatator = FormatatorColor("%(levelname)s %(message)s")
    else:
        formatator = logging.Formatter("%(levelname)-8s %(message)s")
    
    handler_consola.setFormatter(formatator)
    logger.addHandler(handler_consola)
    
    # Handler opțional pentru fișier
    if fisier_log:
        fisier_log.parent.mkdir(parents=True, exist_ok=True)
        handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        formatator_fisier = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler_fisier.setFormatter(formatator_fisier)
        logger.addHandler(handler_fisier)
    
    return logger


def creeaza_fisier_log(nume_script: str) -> Path:
    """
    Creează calea pentru un fișier de log cu timestamp.
    
    Args:
        nume_script: Numele scriptului care creează log-ul
    
    Returns:
        Calea către fișierul de log
    """
    radacina = Path(__file__).parent.parent.parent
    dir_artifacts = radacina / "artifacts" / "logs"
    dir_artifacts.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return dir_artifacts / f"{nume_script}_{timestamp}.log"


# Logger pre-configurat pentru import rapid
logger_implicit = configureaza_logger("week10")
