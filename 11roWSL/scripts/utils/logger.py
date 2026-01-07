#!/usr/bin/env python3
"""
Configurare Logging
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Oferă logging consistent cu output colorat.
"""

import logging
import sys


class FormatorColorat(logging.Formatter):
    """Formator de logging cu culori pentru terminal."""
    
    # Coduri de culoare ANSI
    CULORI = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Galben
        'ERROR': '\033[31m',     # Roșu
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m',      # Reset
    }
    
    def format(self, record):
        # Adaugă culoare pentru nivel
        culoare = self.CULORI.get(record.levelname, self.CULORI['RESET'])
        reset = self.CULORI['RESET']
        
        # Formatează mesajul
        record.levelname = f"{culoare}{record.levelname:8}{reset}"
        
        return super().format(record)


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier: str | None = None
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul de logging (implicit: INFO)
        fisier: Calea fișierului de log opțional
    
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
    
    # Folosește formator colorat dacă stdout este terminal
    if sys.stdout.isatty():
        formator = FormatorColorat('%(levelname)s %(message)s')
    else:
        formator = logging.Formatter('%(levelname)s %(message)s')
    
    handler_consola.setFormatter(formator)
    logger.addHandler(handler_consola)
    
    # Handler opțional pentru fișier
    if fisier:
        handler_fisier = logging.FileHandler(fisier, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        formator_fisier = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        )
        handler_fisier.setFormatter(formator_fisier)
        logger.addHandler(handler_fisier)
    
    return logger
