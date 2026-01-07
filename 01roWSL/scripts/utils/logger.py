#!/usr/bin/env python3
"""
Modul de Logging cu Culori
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Oferă logare consistentă cu formatare colorată pentru terminal.
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


# Coduri de culoare ANSI pentru terminal
class CuloriANSI:
    """Coduri de culoare ANSI pentru formatarea terminalului."""
    RESET = "\033[0m"
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    ALBASTRU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    ALB = "\033[97m"
    BOLD = "\033[1m"


class FormatatorColorat(logging.Formatter):
    """Formatator de log-uri cu suport pentru culori."""
    
    # Mapare nivel -> culoare
    CULORI_NIVEL = {
        logging.DEBUG: CuloriANSI.CYAN,
        logging.INFO: CuloriANSI.VERDE,
        logging.WARNING: CuloriANSI.GALBEN,
        logging.ERROR: CuloriANSI.ROSU,
        logging.CRITICAL: CuloriANSI.BOLD + CuloriANSI.ROSU,
    }
    
    # Mapare nivel -> prefix în română
    PREFIXE_NIVEL = {
        logging.DEBUG: "[DEBUG]  ",
        logging.INFO: "[INFO]   ",
        logging.WARNING: "[ATENȚIE]",
        logging.ERROR: "[EROARE] ",
        logging.CRITICAL: "[CRITIC] ",
    }

    def __init__(self, foloseste_culori: bool = True) -> None:
        """Inițializează formatatorul.
        
        Args:
            foloseste_culori: Activează/dezactivează culorile
        """
        super().__init__()
        self.foloseste_culori = foloseste_culori

    def format(self, record: logging.LogRecord) -> str:
        """Formatează înregistrarea de log.
        
        Args:
            record: Înregistrarea de log
            
        Returns:
            Șirul formatat
        """
        prefix = self.PREFIXE_NIVEL.get(record.levelno, "[???]    ")
        mesaj = record.getMessage()
        
        if self.foloseste_culori:
            culoare = self.CULORI_NIVEL.get(record.levelno, "")
            return f"{culoare}{prefix}{CuloriANSI.RESET} {mesaj}"
        else:
            return f"{prefix} {mesaj}"


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    director_loguri: Optional[Path] = None
) -> logging.Logger:
    """Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul de logare (implicit INFO)
        director_loguri: Directorul pentru fișierele de log (opțional)
        
    Returns:
        Logger-ul configurat
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Previne adăugarea multiplă de handlers
    if logger.handlers:
        return logger
    
    # Handler pentru consolă cu culori
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    handler_consola.setFormatter(FormatatorColorat(foloseste_culori=True))
    logger.addHandler(handler_consola)
    
    # Handler pentru fișier (opțional)
    if director_loguri:
        director_loguri.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cale_fisier = director_loguri / f"{nume}_{timestamp}.log"
        
        handler_fisier = logging.FileHandler(cale_fisier, encoding="utf-8")
        handler_fisier.setLevel(logging.DEBUG)
        handler_fisier.setFormatter(FormatatorColorat(foloseste_culori=False))
        logger.addHandler(handler_fisier)
        
        logger.debug(f"Logare în fișier: {cale_fisier}")
    
    return logger


def creeaza_log_sesiune(director_artefacte: Path) -> Path:
    """Creează un fișier de log pentru sesiunea curentă.
    
    Args:
        director_artefacte: Directorul pentru artefacte
        
    Returns:
        Calea către fișierul de log
    """
    director_artefacte.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    cale_log = director_artefacte / f"sesiune_{timestamp}.log"
    
    # Creează fișierul cu antet
    with open(cale_log, "w", encoding="utf-8") as f:
        f.write(f"# Log Sesiune Laborator\n")
        f.write(f"# Început: {datetime.now().isoformat()}\n")
        f.write(f"# Curs REȚELE DE CALCULATOARE - ASE, Informatică\n")
        f.write("=" * 60 + "\n\n")
    
    return cale_log


# Exemplu de utilizare
if __name__ == "__main__":
    # Demonstrație a logger-ului
    logger = configureaza_logger("demo", nivel=logging.DEBUG)
    
    logger.debug("Acesta este un mesaj de debug")
    logger.info("Acesta este un mesaj informativ")
    logger.warning("Acesta este un avertisment")
    logger.error("Acesta este un mesaj de eroare")
    logger.critical("Acesta este un mesaj critic")
