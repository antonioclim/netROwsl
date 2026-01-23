#!/usr/bin/env python3
"""
Configurare Logger
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Oferă funcții pentru configurarea logger-ului în mod consistent.
"""

import logging
import sys
from typing import Optional


def configureaza_logger(
    nume: str, 
    nivel: int = logging.INFO,
    format_mesaj: Optional[str] = None
) -> logging.Logger:
    """
    Configurează și returnează un logger.
    
    Args:
        nume: Numele logger-ului
        nivel: Nivelul de logging (implicit INFO)
        format_mesaj: Format personalizat (opțional)
    
    Returns:
        Logger configurat
    
    Example:
        >>> logger = configureaza_logger("start_lab")
        >>> logger.info("Mesaj informativ")
    """
    logger = logging.getLogger(nume)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        
        if format_mesaj is None:
            format_mesaj = "[%(asctime)s] %(levelname)s: %(message)s"
        
        formatter = logging.Formatter(format_mesaj, datefmt="%H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    logger.setLevel(nivel)
    return logger
