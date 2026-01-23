#!/usr/bin/env python3
"""
Modul de Logging pentru Scripturi
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Oferă logging consistent pentru toate scripturile de laborator.

Caracteristici:
- Culori în terminal pentru diferențiere rapidă a nivelurilor
- Suport opțional pentru fișiere de log cu timestamp
- Format consistent în întregul proiect

Utilizare:
    from scripts.utils.logger import configureaza_logger
    
    logger = configureaza_logger("numele_scriptului")
    logger.info("Mesaj informativ")
    logger.warning("Avertisment")
    logger.error("Eroare")
    
    # Cu fișier de log
    from scripts.utils.logger import configureaza_logger, creeaza_fisier_log
    logger = configureaza_logger("script", fisier_log=creeaza_fisier_log("script"))

Niveluri de logging (în ordine crescătoare a severității):
- DEBUG: Informații detaliate pentru diagnosticare
- INFO: Confirmări că lucrurile funcționează
- WARNING: Indicație că ceva neașteptat s-a întâmplat
- ERROR: Eroare care împiedică o funcționalitate
- CRITICAL: Eroare gravă care poate opri programul
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional


class FormatatorColor(logging.Formatter):
    """
    Formatator cu suport pentru culori în terminal.
    
    Codifică fiecare nivel de logging cu o culoare distinctă
    pentru identificare rapidă în output-ul terminal-ului.
    
    Attributes:
        CULORI: Dicționar cu codurile ANSI pentru fiecare nivel
    """
    
    # Coduri ANSI pentru culori
    CULORI = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Galben
        'ERROR': '\033[31m',      # Roșu
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m',       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Formatează înregistrarea de log cu culori.
        
        Args:
            record: Înregistrarea de log de formatat
        
        Returns:
            String formatat cu coduri de culoare ANSI
        """
        # Adaugă culoare pentru nivel
        nivel_culoare = self.CULORI.get(record.levelname, self.CULORI['RESET'])
        reset = self.CULORI['RESET']
        
        # Format: [NIVEL] mesaj
        record.levelname = f"{nivel_culoare}{record.levelname:8}{reset}"
        return super().format(record)


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier_log: Optional[Path] = None,
    cu_culori: bool = True
) -> logging.Logger:
    """
    Configurează și returnează un logger pentru scripturi de laborator.
    
    Creează un logger cu handler pentru consolă (cu sau fără culori)
    și opțional un handler pentru fișier de log.
    
    Args:
        nume: Numele logger-ului (de obicei numele scriptului/modulului)
        nivel: Nivelul minim de logging (default: INFO)
        fisier_log: Calea opțională către fișierul de log
        cu_culori: Dacă să folosească culori în terminal (default: True)
    
    Returns:
        Logger configurat și gata de utilizare
    
    Examples:
        >>> logger = configureaza_logger("porneste_lab")
        >>> logger.info("Pornire containere...")
        INFO     Pornire containere...
        
        >>> logger = configureaza_logger("test", nivel=logging.DEBUG)
        >>> logger.debug("Detalii diagnosticare")
        DEBUG    Detalii diagnosticare
    
    Note:
        Dacă logger-ul a fost deja configurat (are handlere),
        funcția returnează logger-ul existent pentru a evita duplicarea.
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evită duplicarea handler-elor
    if logger.handlers:
        return logger
    
    # Handler pentru consolă
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    
    if cu_culori and sys.stdout.isatty():
        formatator = FormatatorColor("%(levelname)s %(message)s")
    else:
        formatator = logging.Formatter("%(levelname)-8s %(message)s")
    
    handler_consola.setFormatter(formatator)
    logger.addHandler(handler_consola)
    
    # Handler opțional pentru fișier
    if fisier_log:
        fisier_log.parent.mkdir(parents=True, exist_ok=True)
        handler_fisier = logging.FileHandler(fisier_log, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        formatator_fisier = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler_fisier.setFormatter(formatator_fisier)
        logger.addHandler(handler_fisier)
    
    return logger


def creeaza_fisier_log(nume_script: str) -> Path:
    """
    Creează calea pentru un fișier de log cu timestamp.
    
    Generează o cale unică în directorul artifacts/logs/
    cu formatul: {nume_script}_{YYYYMMDD_HHMMSS}.log
    
    Args:
        nume_script: Numele scriptului care creează log-ul
    
    Returns:
        Calea absolută către fișierul de log
    
    Examples:
        >>> cale = creeaza_fisier_log("porneste_lab")
        >>> print(cale)
        /path/to/10roWSL/artifacts/logs/porneste_lab_20250115_143022.log
    """
    radacina = Path(__file__).parent.parent.parent
    dir_artifacts = radacina / "artifacts" / "logs"
    dir_artifacts.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return dir_artifacts / f"{nume_script}_{timestamp}.log"


def log_separator(logger: logging.Logger, caracter: str = "═", lungime: int = 60):
    """
    Loghează o linie separatoare pentru vizibilitate în output.
    
    Args:
        logger: Logger-ul de utilizat
        caracter: Caracterul pentru separator (default: ═)
        lungime: Lungimea liniei (default: 60)
    
    Examples:
        >>> log_separator(logger)
        INFO     ════════════════════════════════════════════════════════════
    """
    logger.info(caracter * lungime)


def log_sectiune(logger: logging.Logger, titlu: str, caracter: str = "─"):
    """
    Loghează un titlu de secțiune formatat.
    
    Args:
        logger: Logger-ul de utilizat
        titlu: Textul titlului
        caracter: Caracterul pentru subliniere (default: ─)
    
    Examples:
        >>> log_sectiune(logger, "Verificare servicii")
        INFO     Verificare servicii
        INFO     ──────────────────────────────────────────────────
    """
    logger.info(titlu)
    logger.info(caracter * len(titlu))


# ═══════════════════════════════════════════════════════════════════════════════
# LOGGER IMPLICIT
# ═══════════════════════════════════════════════════════════════════════════════

# Logger pre-configurat pentru import rapid
# Utilizare: from scripts.utils.logger import logger_implicit as logger
logger_implicit = configureaza_logger("week10")


# Permite rularea directă pentru testare
if __name__ == "__main__":
    print("Test modul logging:")
    print()
    
    test_logger = configureaza_logger("test_logger", nivel=logging.DEBUG)
    
    log_separator(test_logger)
    log_sectiune(test_logger, "Testare niveluri de logging")
    
    test_logger.debug("Mesaj DEBUG - pentru diagnosticare")
    test_logger.info("Mesaj INFO - operație normală")
    test_logger.warning("Mesaj WARNING - atenție necesară")
    test_logger.error("Mesaj ERROR - ceva nu a mers")
    test_logger.critical("Mesaj CRITICAL - eroare gravă")
    
    log_separator(test_logger)
    print()
    print("Test încheiat cu succes!")
