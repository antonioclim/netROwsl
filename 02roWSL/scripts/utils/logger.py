#!/usr/bin/env python3
"""
Modul de Logging
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă logging consistent cu culori și formatare.
"""

import logging
import sys
from datetime import datetime
from typing import Optional


class FormatatorColorat(logging.Formatter):
    """Formator cu suport pentru culori ANSI."""
    
    # Coduri de culoare ANSI
    CULORI = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Galben
        'ERROR': '\033[31m',      # Roșu
        'CRITICAL': '\033[35m',   # Magenta
    }
    RESETARE = '\033[0m'
    BOLD = '\033[1m'
    
    def __init__(self, fmt: str = None, datefmt: str = None, use_colors: bool = True):
        super().__init__(fmt, datefmt)
        self.folosește_culori = use_colors and sys.stdout.isatty()
    
    def format(self, record: logging.LogRecord) -> str:
        # Salvare valori originale
        original_levelname = record.levelname
        original_msg = record.msg
        
        if self.folosește_culori:
            culoare = self.CULORI.get(record.levelname, '')
            record.levelname = f"{culoare}{record.levelname}{self.RESETARE}"
            
            # Adăugare bold pentru erori și critice
            if original_levelname in ('ERROR', 'CRITICAL'):
                record.msg = f"{self.BOLD}{record.msg}{self.RESETARE}"
        
        rezultat = super().format(record)
        
        # Restaurare valori
        record.levelname = original_levelname
        record.msg = original_msg
        
        return rezultat


def configurează_logger(
    nume: str,
    nivel: int = logging.INFO,
    format_log: Optional[str] = None,
    fișier: Optional[str] = None
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele loggerului
        nivel: Nivelul de logging (implicit: INFO)
        format_log: Format personalizat (opțional)
        fișier: Cale către fișier de log (opțional)
        
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evitare duplicate handlers
    if logger.handlers:
        return logger
    
    # Format implicit
    if format_log is None:
        format_log = "%(asctime)s [%(levelname)s] %(message)s"
    
    format_dată = "%H:%M:%S"
    
    # Handler pentru consolă
    handler_consolă = logging.StreamHandler(sys.stdout)
    handler_consolă.setLevel(nivel)
    handler_consolă.setFormatter(FormatatorColorat(format_log, format_dată))
    logger.addHandler(handler_consolă)
    
    # Handler pentru fișier (opțional)
    if fișier:
        handler_fișier = logging.FileHandler(fișier, encoding='utf-8')
        handler_fișier.setLevel(nivel)
        handler_fișier.setFormatter(logging.Formatter(format_log, format_dată))
        logger.addHandler(handler_fișier)
    
    return logger


# Logger implicit pentru import simplu
logger = configurează_logger("week2_lab")


# Funcții de conveniență
def info(mesaj: str) -> None:
    """Afișează mesaj informativ."""
    logger.info(mesaj)


def warning(mesaj: str) -> None:
    """Afișează avertisment."""
    logger.warning(mesaj)


def error(mesaj: str) -> None:
    """Afișează eroare."""
    logger.error(mesaj)


def debug(mesaj: str) -> None:
    """Afișează mesaj de debug."""
    logger.debug(mesaj)


def succes(mesaj: str) -> None:
    """Afișează mesaj de succes (verde)."""
    if sys.stdout.isatty():
        print(f"\033[92m✓ {mesaj}\033[0m")
    else:
        print(f"✓ {mesaj}")


def eșec(mesaj: str) -> None:
    """Afișează mesaj de eșec (roșu)."""
    if sys.stdout.isatty():
        print(f"\033[91m✗ {mesaj}\033[0m")
    else:
        print(f"✗ {mesaj}")


if __name__ == "__main__":
    # Test logging
    test_logger = configurează_logger("test", nivel=logging.DEBUG)
    
    test_logger.debug("Mesaj de debug")
    test_logger.info("Mesaj informativ")
    test_logger.warning("Avertisment")
    test_logger.error("Eroare")
    test_logger.critical("Critic")
    
    print()
    succes("Operațiune reușită!")
    eșec("Operațiune eșuată!")
