#!/usr/bin/env python3
"""
Modul de Logging
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă funcționalitate de logging consistentă cu suport pentru culori.
"""

import logging
import sys
from typing import Optional


class FormatorCulori(logging.Formatter):
    """Formator de logging cu suport pentru culori în terminal."""
    
    # Coduri ANSI pentru culori
    CULORI = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Galben
        'ERROR': '\033[31m',      # Roșu
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def __init__(self, foloseste_culori: bool = True):
        """
        Inițializează formatorul.
        
        Args:
            foloseste_culori: True pentru a activa culorile
        """
        super().__init__(
            fmt='%(asctime)s %(levelname)-8s %(message)s',
            datefmt='%H:%M:%S'
        )
        self.foloseste_culori = foloseste_culori
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatează înregistrarea de log cu culori."""
        mesaj = super().format(record)
        
        if self.foloseste_culori:
            culoare = self.CULORI.get(record.levelname, '')
            reset = self.CULORI['RESET']
            return f"{culoare}{mesaj}{reset}"
        
        return mesaj


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier_log: Optional[str] = None,
    foloseste_culori: bool = True
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul de logging (implicit INFO)
        fisier_log: Calea către fișierul de log (opțional)
        foloseste_culori: True pentru culori în consolă
        
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(logging.DEBUG)
    
    # Elimină handler-ii existenți
    logger.handlers.clear()
    
    # Handler pentru consolă
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    handler_consola.setFormatter(FormatorCulori(foloseste_culori=foloseste_culori))
    logger.addHandler(handler_consola)
    
    # Handler pentru fișier (dacă este specificat)
    if fisier_log:
        handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
        handler_fisier.setLevel(logging.DEBUG)
        handler_fisier.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)-8s [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        ))
        logger.addHandler(handler_fisier)
    
    return logger


# Logger implicit pentru import direct
logger_implicit = configureaza_logger('week3')
