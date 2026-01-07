#!/usr/bin/env python3
"""
Modul de Jurnalizare (Logging)
Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix

Configurare consistentă a jurnalizării pentru toate scripturile.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_DISPONIBIL = True
except ImportError:
    COLORAMA_DISPONIBIL = False


class FormatatorCuCulori(logging.Formatter):
    """Formatator de jurnale cu suport pentru culori în terminal."""
    
    CULORI = {
        logging.DEBUG: Fore.CYAN if COLORAMA_DISPONIBIL else "",
        logging.INFO: Fore.GREEN if COLORAMA_DISPONIBIL else "",
        logging.WARNING: Fore.YELLOW if COLORAMA_DISPONIBIL else "",
        logging.ERROR: Fore.RED if COLORAMA_DISPONIBIL else "",
        logging.CRITICAL: Fore.RED + Style.BRIGHT if COLORAMA_DISPONIBIL else ""
    }
    
    RESET = Style.RESET_ALL if COLORAMA_DISPONIBIL else ""
    
    def format(self, record):
        culoare = self.CULORI.get(record.levelno, "")
        
        # Format simplu pentru INFO, detaliat pentru altele
        if record.levelno == logging.INFO:
            mesaj = record.getMessage()
        else:
            mesaj = f"[{record.levelname}] {record.getMessage()}"
        
        return f"{culoare}{mesaj}{self.RESET}"


class FormatatorFisier(logging.Formatter):
    """Formatator pentru fișierele de jurnal."""
    
    def __init__(self):
        super().__init__(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    cu_fisier: bool = False,
    director_jurnale: Path = None
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul de jurnalizare (implicit: INFO)
        cu_fisier: Dacă se creează și un fișier de jurnal
        director_jurnale: Directorul pentru fișierele de jurnal
    
    Returns:
        Logger configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evităm duplicarea handler-elor
    if logger.handlers:
        return logger
    
    # Handler pentru consolă
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    handler_consola.setFormatter(FormatatorCuCulori())
    logger.addHandler(handler_consola)
    
    # Handler opțional pentru fișier
    if cu_fisier:
        if director_jurnale is None:
            director_jurnale = Path(__file__).parent.parent.parent / "artifacts"
        
        director_jurnale.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d")
        cale_fisier = director_jurnale / f"{nume}_{timestamp}.log"
        
        handler_fisier = logging.FileHandler(cale_fisier, encoding="utf-8")
        handler_fisier.setLevel(logging.DEBUG)
        handler_fisier.setFormatter(FormatatorFisier())
        logger.addHandler(handler_fisier)
    
    return logger


# Logger implicit pentru import rapid
logger_implicit = configureaza_logger("week12")
