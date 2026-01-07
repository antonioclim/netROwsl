#!/usr/bin/env python3
"""
Modul de Logging Colorat
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Oferă funcționalitate de logging cu culori pentru consolă și fișier.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


# Coduri de culoare ANSI
class Culori:
    """Coduri de escape ANSI pentru culori în terminal."""
    HEADER = '\033[95m'
    ALBASTRU = '\033[94m'
    CYAN = '\033[96m'
    VERDE = '\033[92m'
    GALBEN = '\033[93m'
    ROSU = '\033[91m'
    SFARSIT = '\033[0m'
    BOLD = '\033[1m'
    SUBLINIAT = '\033[4m'


class FormatorColorat(logging.Formatter):
    """Formator de logging cu culori pentru consolă."""
    
    FORMATE = {
        logging.DEBUG: Culori.CYAN + "%(asctime)s [DEBUG] %(message)s" + Culori.SFARSIT,
        logging.INFO: Culori.VERDE + "%(asctime)s [INFO] %(message)s" + Culori.SFARSIT,
        logging.WARNING: Culori.GALBEN + "%(asctime)s [ATENȚIE] %(message)s" + Culori.SFARSIT,
        logging.ERROR: Culori.ROSU + "%(asctime)s [EROARE] %(message)s" + Culori.SFARSIT,
        logging.CRITICAL: Culori.BOLD + Culori.ROSU + "%(asctime)s [CRITIC] %(message)s" + Culori.SFARSIT,
    }

    def __init__(self):
        super().__init__(datefmt="%H:%M:%S")

    def format(self, record):
        format_log = self.FORMATE.get(record.levelno)
        formatter = logging.Formatter(format_log, datefmt="%H:%M:%S")
        return formatter.format(record)


class FormatorFisier(logging.Formatter):
    """Formator simplu pentru logging în fișier."""
    
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier_log: str = None
) -> logging.Logger:
    """
    Configurează și returnează un logger cu output colorat în consolă.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul minim de logging (implicit: INFO)
        fisier_log: Calea opțională către fișierul de log
    
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evită adăugarea handler-elor duplicate
    if logger.handlers:
        return logger
    
    # Handler pentru consolă cu culori
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    handler_consola.setFormatter(FormatorColorat())
    logger.addHandler(handler_consola)
    
    # Handler opțional pentru fișier
    if fisier_log:
        cale_fisier = Path(fisier_log)
        cale_fisier.parent.mkdir(parents=True, exist_ok=True)
        
        handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        handler_fisier.setFormatter(FormatorFisier())
        logger.addHandler(handler_fisier)
    
    return logger


def afiseaza_succes(mesaj: str):
    """Afișează un mesaj de succes cu culoare verde."""
    print(f"{Culori.VERDE}✓ {mesaj}{Culori.SFARSIT}")


def afiseaza_eroare(mesaj: str):
    """Afișează un mesaj de eroare cu culoare roșie."""
    print(f"{Culori.ROSU}✗ {mesaj}{Culori.SFARSIT}")


def afiseaza_avertisment(mesaj: str):
    """Afișează un avertisment cu culoare galbenă."""
    print(f"{Culori.GALBEN}⚠ {mesaj}{Culori.SFARSIT}")


def afiseaza_info(mesaj: str):
    """Afișează o informație cu culoare albastră."""
    print(f"{Culori.ALBASTRU}ℹ {mesaj}{Culori.SFARSIT}")


# Pentru compatibilitate cu codul existent în limba engleză
setup_logger = configureaza_logger
