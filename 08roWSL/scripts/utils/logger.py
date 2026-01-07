#!/usr/bin/env python3
"""
Modul de Logare
Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Oferă funcționalitate de logare consistentă pentru toate scripturile.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

# Coduri ANSI pentru culori
CULORI = {
    'VERDE': "\033[92m",
    'ROSU': "\033[91m",
    'GALBEN': "\033[93m",
    'ALBASTRU': "\033[94m",
    'CYAN': "\033[96m",
    'MAGENTA': "\033[95m",
    'RESETARE': "\033[0m",
    'BOLD': "\033[1m",
}


class GestionarCulori(logging.StreamHandler):
    """Handler de logare cu suport pentru culori."""
    
    CULORI_NIVEL = {
        logging.DEBUG: CULORI['CYAN'],
        logging.INFO: CULORI['VERDE'],
        logging.WARNING: CULORI['GALBEN'],
        logging.ERROR: CULORI['ROSU'],
        logging.CRITICAL: CULORI['MAGENTA'],
    }
    
    def emit(self, record):
        try:
            culoare = self.CULORI_NIVEL.get(record.levelno, CULORI['RESETARE'])
            record.msg = f"{culoare}{record.msg}{CULORI['RESETARE']}"
            super().emit(record)
        except Exception:
            self.handleError(record)


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier_log: Optional[Path] = None
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul de logare (implicit INFO)
        fisier_log: Calea opțională către fișierul de log
    
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Elimină handlerii existenți
    logger.handlers.clear()
    
    # Handler pentru consolă cu culori
    handler_consola = GestionarCulori(sys.stdout)
    handler_consola.setLevel(nivel)
    
    format_consola = logging.Formatter(
        '[%(levelname)s] %(message)s'
    )
    handler_consola.setFormatter(format_consola)
    logger.addHandler(handler_consola)
    
    # Handler pentru fișier dacă este specificat
    if fisier_log:
        handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        
        format_fisier = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler_fisier.setFormatter(format_fisier)
        logger.addHandler(handler_fisier)
    
    return logger


def afiseaza_banner(titlu: str, subtitlu: str = ""):
    """Afișează un banner formatat."""
    latime = 60
    print()
    print(f"{CULORI['CYAN']}{'=' * latime}{CULORI['RESETARE']}")
    print(f"{CULORI['BOLD']}{CULORI['CYAN']}   {titlu}{CULORI['RESETARE']}")
    if subtitlu:
        print(f"{CULORI['CYAN']}   {subtitlu}{CULORI['RESETARE']}")
    print(f"{CULORI['CYAN']}{'=' * latime}{CULORI['RESETARE']}")
    print()


def afiseaza_sectiune(titlu: str):
    """Afișează un separator de secțiune."""
    print()
    print(f"{CULORI['ALBASTRU']}{titlu}{CULORI['RESETARE']}")
    print("-" * 50)


def afiseaza_succes(mesaj: str):
    """Afișează un mesaj de succes."""
    print(f"{CULORI['VERDE']}✓ {mesaj}{CULORI['RESETARE']}")


def afiseaza_eroare(mesaj: str):
    """Afișează un mesaj de eroare."""
    print(f"{CULORI['ROSU']}✗ {mesaj}{CULORI['RESETARE']}")


def afiseaza_avertisment(mesaj: str):
    """Afișează un mesaj de avertisment."""
    print(f"{CULORI['GALBEN']}! {mesaj}{CULORI['RESETARE']}")


def afiseaza_info(mesaj: str):
    """Afișează un mesaj informativ."""
    print(f"{CULORI['ALBASTRU']}ℹ {mesaj}{CULORI['RESETARE']}")
