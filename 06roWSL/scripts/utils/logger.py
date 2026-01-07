#!/usr/bin/env python3
"""
Utilitare de logging
Disciplina REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Furnizează configurare consistentă de logging pentru toate scripturile.
"""

from __future__ import annotations

import logging
import sys
from typing import Optional


def setup_logger(
    nume: str,
    nivel: int = logging.INFO,
    fmt: str = "[%(asctime)s] %(levelname)s: %(message)s",
    format_data: str = "%H:%M:%S"
) -> logging.Logger:
    """
    Configurează și returnează un logger cu formatare consistentă.
    
    Argumente:
        nume: Numele logger-ului (de obicei numele modulului)
        nivel: Nivelul de logging (implicit: INFO)
        fmt: Formatul mesajului de log
        format_data: Formatul datei/timpului
        
    Returnează:
        Instanță Logger configurată
    """
    logger = logging.getLogger(nume)
    logger.setLevel(nivel)
    
    # Evită adăugarea de handler-e duplicate
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(nivel)
        formatator = logging.Formatter(fmt, datefmt=format_data)
        handler.setFormatter(formatator)
        logger.addHandler(handler)
    
    return logger


def set_verbose(logger: logging.Logger, detaliat: bool = True) -> None:
    """
    Activează sau dezactivează logging-ul detaliat (DEBUG).
    
    Argumente:
        logger: Logger-ul de modificat
        detaliat: Dacă să activeze nivelul DEBUG
    """
    if detaliat:
        logger.setLevel(logging.DEBUG)
        for handler in logger.handlers:
            handler.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        for handler in logger.handlers:
            handler.setLevel(logging.INFO)


class ProgressLogger:
    """
    Manager de context pentru logging-ul progresului operațiunilor cu mai mulți pași.
    """
    
    def __init__(self, logger: logging.Logger, operatiune: str, total_pasi: int = 0):
        """
        Inițializează logger-ul de progres.
        
        Argumente:
            logger: Logger-ul de utilizat
            operatiune: Numele operațiunii
            total_pasi: Numărul total de pași (0 pentru necunoscut)
        """
        self.logger = logger
        self.operatiune = operatiune
        self.total_pasi = total_pasi
        self.pas_curent = 0
    
    def __enter__(self):
        self.logger.info(f"Pornire: {self.operatiune}")
        return self
    
    def __exit__(self, tip_exc, val_exc, tb):
        if tip_exc is None:
            self.logger.info(f"Finalizat: {self.operatiune}")
        else:
            self.logger.error(f"Eșuat: {self.operatiune} - {val_exc}")
        return False
    
    def step(self, mesaj: str) -> None:
        """Înregistrează un pas de progres."""
        self.pas_curent += 1
        if self.total_pasi > 0:
            self.logger.info(f"  [{self.pas_curent}/{self.total_pasi}] {mesaj}")
        else:
            self.logger.info(f"  [{self.pas_curent}] {mesaj}")
