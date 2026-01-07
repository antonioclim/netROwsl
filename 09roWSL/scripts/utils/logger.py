#!/usr/bin/env python3
"""
Modul de Jurnalizare
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Oferă funcționalități de jurnalizare colorată pentru scripturi.
"""

import logging
import sys
from typing import Optional


class FormatatorColorat(logging.Formatter):
    """
    Formatator personalizat care adaugă culori la mesajele de log.
    
    Culori ANSI:
        - ROȘU: Erori
        - GALBEN: Avertismente
        - VERDE: Informații
        - ALBASTRU: Debug
        - CYAN: Mesaje speciale
    """
    
    # Coduri de culoare ANSI
    GRI = "\033[90m"
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    ALBASTRU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    ALB = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Formaturi pentru fiecare nivel
    FORMATE = {
        logging.DEBUG: f"{ALBASTRU}[DEBUG]{RESET} %(message)s",
        logging.INFO: f"{VERDE}[INFO]{RESET} %(message)s",
        logging.WARNING: f"{GALBEN}[ATENȚIE]{RESET} %(message)s",
        logging.ERROR: f"{ROSU}[EROARE]{RESET} %(message)s",
        logging.CRITICAL: f"{BOLD}{ROSU}[CRITIC]{RESET} %(message)s",
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Formatează înregistrarea de log cu culori."""
        format_log = self.FORMATE.get(record.levelno, "%(message)s")
        formatter = logging.Formatter(format_log)
        return formatter.format(record)


def configureaza_logger(
    nume: str,
    nivel: int = logging.INFO,
    fisier: Optional[str] = None
) -> logging.Logger:
    """
    Configurează și returnează un logger cu ieșire colorată.
    
    Argumente:
        nume: Numele logger-ului
        nivel: Nivelul de jurnalizare (implicit INFO)
        fisier: Calea opțională pentru jurnalizare în fișier
        
    Returnează:
        Logger configurat
        
    Exemplu:
        >>> logger = configureaza_logger("scriptul_meu")
        >>> logger.info("Mesaj de informare")
        [INFO] Mesaj de informare
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Elimină handler-ele existente pentru a evita duplicarea
    logger.handlers.clear()
    
    # Handler pentru consolă cu culori
    handler_consola = logging.StreamHandler(sys.stdout)
    handler_consola.setLevel(nivel)
    handler_consola.setFormatter(FormatatorColorat())
    logger.addHandler(handler_consola)
    
    # Handler opțional pentru fișier (fără culori)
    if fisier:
        handler_fisier = logging.FileHandler(fisier, encoding='utf-8')
        handler_fisier.setLevel(nivel)
        format_fisier = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler_fisier.setFormatter(format_fisier)
        logger.addHandler(handler_fisier)
    
    return logger


def afiseaza_banner(titlu: str, subtitlu: str = "") -> None:
    """
    Afișează un banner decorativ în terminal.
    
    Argumente:
        titlu: Textul principal al banner-ului
        subtitlu: Text opțional sub titlu
        
    Exemplu:
        >>> afiseaza_banner("Săptămâna 9", "Nivelul Sesiune și Prezentare")
    """
    latime = 60
    linie = "=" * latime
    
    print()
    print(f"\033[96m{linie}\033[0m")
    print(f"\033[1m\033[97m{titlu.center(latime)}\033[0m")
    if subtitlu:
        print(f"\033[90m{subtitlu.center(latime)}\033[0m")
    print(f"\033[96m{linie}\033[0m")
    print()


def afiseaza_succes(mesaj: str) -> None:
    """Afișează un mesaj de succes în verde."""
    print(f"\033[92m✓ {mesaj}\033[0m")


def afiseaza_eroare(mesaj: str) -> None:
    """Afișează un mesaj de eroare în roșu."""
    print(f"\033[91m✗ {mesaj}\033[0m")


def afiseaza_avertisment(mesaj: str) -> None:
    """Afișează un avertisment în galben."""
    print(f"\033[93m⚠ {mesaj}\033[0m")


def afiseaza_info(mesaj: str) -> None:
    """Afișează informație în cyan."""
    print(f"\033[96mℹ {mesaj}\033[0m")


# Alias-uri pentru compatibilitate
setup_logger = configureaza_logger
print_banner = afiseaza_banner


if __name__ == "__main__":
    # Demonstrație
    afiseaza_banner("Test Logger", "Demonstrație funcționalități")
    
    logger = configureaza_logger("test")
    logger.debug("Acesta este un mesaj de debug")
    logger.info("Acesta este un mesaj informativ")
    logger.warning("Acesta este un avertisment")
    logger.error("Acesta este o eroare")
    logger.critical("Acesta este un mesaj critic")
    
    print()
    afiseaza_succes("Operațiune reușită!")
    afiseaza_eroare("Ceva nu a funcționat!")
    afiseaza_avertisment("Atenție la această situație!")
    afiseaza_info("Informație utilă")
