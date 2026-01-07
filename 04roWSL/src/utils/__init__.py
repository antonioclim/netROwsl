"""
Utilitare Protocol
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Funcții utilitare pentru protocoalele de laborator.
"""

from .protocol_utils import (
    calculeaza_crc32,
    verifica_crc32,
    formateaza_hex,
    parseaza_hex,
    impacheteaza_text,
    despacheteaza_text,
    impacheteaza_binar,
    despacheteaza_binar,
    impacheteaza_senzor,
    despacheteaza_senzor,
    TipMesajBinar,
    BINAR_MAGIC,
    BINAR_VERSIUNE,
    BINAR_DIMENSIUNE_ANTET,
    UDP_DIMENSIUNE_DATAGRAMA
)

__all__ = [
    'calculeaza_crc32',
    'verifica_crc32',
    'formateaza_hex',
    'parseaza_hex',
    'impacheteaza_text',
    'despacheteaza_text',
    'impacheteaza_binar',
    'despacheteaza_binar',
    'impacheteaza_senzor',
    'despacheteaza_senzor',
    'TipMesajBinar',
    'BINAR_MAGIC',
    'BINAR_VERSIUNE',
    'BINAR_DIMENSIUNE_ANTET',
    'UDP_DIMENSIUNE_DATAGRAMA'
]
