#!/usr/bin/env python3
"""
Modul de Logging
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Oferă funcționalitate de logging consistentă pentru toate scripturile.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path

# Încearcă să importe colorama pentru output colorat
try:
    from colorama import Fore, Style, init as colorama_init
    colorama_init()
    CULORI_DISPONIBILE = True
except ImportError:
    CULORI_DISPONIBILE = False


class FormatorColorat(logging.Formatter):
    """Formator personalizat cu suport pentru culori în consolă."""
    
    # Mapare nivel -> culoare
    CULORI_NIVEL = {
        logging.DEBUG: 'CYAN',
        logging.INFO: 'GREEN',
        logging.WARNING: 'YELLOW',
        logging.ERROR: 'RED',
        logging.CRITICAL: 'MAGENTA',
    }
    
    # Mapare nivel -> text în română
    NUME_NIVEL = {
        logging.DEBUG: 'DEBUG',
        logging.INFO: 'INFO',
        logging.WARNING: 'ATENȚIE',
        logging.ERROR: 'EROARE',
        logging.CRITICAL: 'CRITIC',
    }
    
    def __init__(self, foloseste_culori: bool = True):
        super().__init__()
        self.foloseste_culori = foloseste_culori and CULORI_DISPONIBILE
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatează înregistrarea de log."""
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        nume_nivel = self.NUME_NIVEL.get(record.levelno, record.levelname)
        
        if self.foloseste_culori:
            culoare = self.CULORI_NIVEL.get(record.levelno, 'WHITE')
            cod_culoare = getattr(Fore, culoare, Fore.WHITE)
            reset = Style.RESET_ALL
            return f"[{timestamp}] {cod_culoare}{nume_nivel:8}{reset}: {record.getMessage()}"
        else:
            return f"[{timestamp}] {nume_nivel:8}: {record.getMessage()}"


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier_log: Path | None = None,
    foloseste_culori: bool = True
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul minim de logging
        fisier_log: Calea către fișierul de log (opțional)
        foloseste_culori: Dacă să folosească culori în consolă
    
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
    handler_consola.setFormatter(FormatorColorat(foloseste_culori))
    logger.addHandler(handler_consola)
    
    # Handler pentru fișier (dacă este specificat)
    if fisier_log:
        fisier_log.parent.mkdir(parents=True, exist_ok=True)
        handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        # Fișierul nu folosește culori
        handler_fisier.setFormatter(FormatorColorat(foloseste_culori=False))
        logger.addHandler(handler_fisier)
    
    return logger


# Logger implicit pentru utilizare rapidă
logger_implicit = configureaza_logger('week7')


def info(mesaj: str):
    """Logare nivel INFO."""
    logger_implicit.info(mesaj)


def warning(mesaj: str):
    """Logare nivel WARNING (ATENȚIE)."""
    logger_implicit.warning(mesaj)


def error(mesaj: str):
    """Logare nivel ERROR (EROARE)."""
    logger_implicit.error(mesaj)


def debug(mesaj: str):
    """Logare nivel DEBUG."""
    logger_implicit.debug(mesaj)
