#!/usr/bin/env python3
"""
Modul de Logging
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Furnizează funcții de logging consistente pentru toate scripturile.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path


class FormatatorColor:
    """Formatator de log-uri cu suport pentru culori în terminal."""
    
    CULORI = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Galben
        'ERROR': '\033[31m',     # Roșu
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def __init__(self, foloseste_culori: bool = True):
        self.foloseste_culori = foloseste_culori
    
    def format(self, record):
        ora = datetime.now().strftime("%H:%M:%S")
        nivel = record.levelname
        mesaj = record.getMessage()
        
        if self.foloseste_culori and sys.stdout.isatty():
            culoare = self.CULORI.get(nivel, '')
            reset = self.CULORI['RESET']
            return f"[{ora}] {culoare}[{nivel}]{reset} {mesaj}"
        else:
            return f"[{ora}] [{nivel}] {mesaj}"


class LoggerLaborator:
    """
    Logger personalizat pentru scripturile de laborator.
    
    Utilizare:
        logger = LoggerLaborator("nume_script")
        logger.info("Mesaj informativ")
        logger.succes("Operație reușită")
        logger.eroare("Ceva a eșuat")
    """
    
    def __init__(self, nume: str, nivel: int = logging.INFO):
        self.logger = logging.getLogger(nume)
        self.logger.setLevel(nivel)
        
        # Evită duplicarea handler-elor
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(nivel)
            
            formatator = FormatatorColor()
            handler.setFormatter(type('', (), {'format': formatator.format})())
            
            self.logger.addHandler(handler)
    
    def debug(self, mesaj: str):
        """Mesaj de debug."""
        self.logger.debug(mesaj)
    
    def info(self, mesaj: str):
        """Mesaj informativ."""
        self.logger.info(mesaj)
    
    def warning(self, mesaj: str):
        """Mesaj de avertisment."""
        self.logger.warning(mesaj)
    
    def error(self, mesaj: str):
        """Mesaj de eroare."""
        self.logger.error(mesaj)
    
    def critical(self, mesaj: str):
        """Mesaj critic."""
        self.logger.critical(mesaj)
    
    def succes(self, mesaj: str):
        """Mesaj de succes (afișat ca INFO cu prefix special)."""
        self.logger.info(f"✓ {mesaj}")
    
    def esec(self, mesaj: str):
        """Mesaj de eșec (afișat ca ERROR cu prefix special)."""
        self.logger.error(f"✗ {mesaj}")


def configureaza_logger(nume: str, nivel: int = logging.INFO) -> LoggerLaborator:
    """
    Creează și configurează un logger pentru scriptul specificat.
    
    Args:
        nume: Numele logger-ului (de obicei numele scriptului)
        nivel: Nivelul minim de logging (implicit INFO)
    
    Returns:
        Instanță LoggerLaborator configurată
    """
    return LoggerLaborator(nume, nivel)


# Alias pentru compatibilitate
setup_logger = configureaza_logger
