#!/usr/bin/env python3
"""
Modul de Logging
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Oferă funcționalități de logging consistente pentru toate scripturile.
"""

import logging
import sys
from datetime import datetime
from typing import Optional


class FormatatorColorat(logging.Formatter):
    """Formatator personalizat cu culori pentru terminal."""
    
    # Coduri de culoare ANSI
    CULORI = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Verde
        'WARNING': '\033[33m',   # Galben
        'ERROR': '\033[91m',     # Roșu deschis
        'CRITICAL': '\033[91m\033[1m',  # Roșu bold
    }
    RESET = '\033[0m'
    
    def format(self, record):
        """Formatează înregistrarea de log cu culori."""
        # Adaugă culoare la nivel
        nivel_original = record.levelname
        culoare = self.CULORI.get(record.levelname, '')
        record.levelname = f"{culoare}{record.levelname}{self.RESET}"
        
        # Formatează mesajul
        rezultat = super().format(record)
        
        # Restaurează nivelul original
        record.levelname = nivel_original
        
        return rezultat


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier: Optional[str] = None
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele loggerului
        nivel: Nivelul de logging (implicit INFO)
        fisier: Calea către fișierul de log (opțional)
    
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evită adăugarea multiplă de handlere
    if logger.handlers:
        return logger
    
    # Handler pentru consolă cu culori
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    
    # Verifică dacă terminalul suportă culori
    if hasattr(sys.stdout, 'isatty') and sys.stdout.isatty():
        format_consola = FormatatorColorat('%(levelname)s: %(message)s')
    else:
        format_consola = logging.Formatter('%(levelname)s: %(message)s')
    
    handler_consola.setFormatter(format_consola)
    logger.addHandler(handler_consola)
    
    # Handler pentru fișier (opțional)
    if fisier:
        handler_fisier = logging.FileHandler(fisier, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        format_fisier = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler_fisier.setFormatter(format_fisier)
        logger.addHandler(handler_fisier)
    
    return logger


def formateaza_timestamp(timestamp: Optional[datetime] = None) -> str:
    """
    Formatează un timestamp pentru afișare.
    
    Args:
        timestamp: Datetime de formatat (implicit: acum)
    
    Returns:
        String formatat
    """
    if timestamp is None:
        timestamp = datetime.now()
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")


def formateaza_octeti(octeti: bytes, max_lung: int = 32) -> str:
    """
    Formatează octeti pentru afișare.
    
    Args:
        octeti: Datele de formatat
        max_lung: Lungimea maximă de afișat
    
    Returns:
        String formatat (hex + ASCII)
    """
    if len(octeti) > max_lung:
        octeti_afisati = octeti[:max_lung]
        sufix = f"... ({len(octeti)} total)"
    else:
        octeti_afisati = octeti
        sufix = ""
    
    hex_str = octeti_afisati.hex()
    
    # Adaugă reprezentare ASCII
    ascii_str = ''.join(
        chr(b) if 32 <= b < 127 else '.'
        for b in octeti_afisati
    )
    
    return f"{hex_str} [{ascii_str}]{sufix}"


def formateaza_dimensiune(octeti: int) -> str:
    """
    Formatează o dimensiune în octeți pentru afișare.
    
    Args:
        octeti: Numărul de octeți
    
    Returns:
        String formatat (ex: "1.5 KB", "2.3 MB")
    """
    for unitate in ['B', 'KB', 'MB', 'GB']:
        if octeti < 1024:
            return f"{octeti:.1f} {unitate}" if octeti != int(octeti) else f"{int(octeti)} {unitate}"
        octeti /= 1024
    return f"{octeti:.1f} TB"


# Funcții de conveniență pentru logging rapid
def log_info(mesaj: str, logger_nume: str = "app"):
    """Logează un mesaj informativ."""
    logging.getLogger(logger_nume).info(mesaj)


def log_eroare(mesaj: str, logger_nume: str = "app"):
    """Logează un mesaj de eroare."""
    logging.getLogger(logger_nume).error(mesaj)


def log_avertisment(mesaj: str, logger_nume: str = "app"):
    """Logează un avertisment."""
    logging.getLogger(logger_nume).warning(mesaj)
