#!/usr/bin/env python3
"""
Utilități de Rețea pentru Exerciții
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Funcții helper pentru exercițiile de laborator.
"""

import socket
from typing import Tuple, Optional


def obtine_adresa_locala() -> str:
    """
    Obține adresa IP locală a mașinii.
    
    Returns:
        Adresa IP ca string
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"


def verifica_port_disponibil(port: int, gazda: str = "localhost") -> bool:
    """
    Verifică dacă un port este disponibil.
    
    Args:
        port: Numărul portului
        gazda: Adresa gazdei
    
    Returns:
        True dacă portul este disponibil
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.bind((gazda, port))
            return True
    except OSError:
        return False


def asteapta_serviciu(
    gazda: str,
    port: int,
    timeout: int = 30,
    interval: float = 0.5
) -> bool:
    """
    Așteaptă până când un serviciu devine disponibil.
    
    Args:
        gazda: Adresa gazdei
        port: Numărul portului
        timeout: Timeout total în secunde
        interval: Interval între încercări
    
    Returns:
        True dacă serviciul a devenit disponibil
    """
    import time
    
    timp_start = time.time()
    
    while time.time() - timp_start < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((gazda, port))
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(interval)
    
    return False


def formateaza_bytes(numar_bytes: int) -> str:
    """
    Formatează un număr de bytes într-un format citibil.
    
    Args:
        numar_bytes: Numărul de bytes
    
    Returns:
        String formatat (ex: "1.5 KB")
    """
    for unitate in ['B', 'KB', 'MB', 'GB', 'TB']:
        if abs(numar_bytes) < 1024.0:
            return f"{numar_bytes:.1f} {unitate}"
        numar_bytes /= 1024.0
    return f"{numar_bytes:.1f} PB"
