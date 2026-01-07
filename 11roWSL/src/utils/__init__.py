"""
Utilitare pentru cod sursă Săptămâna 11
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix
"""

from .net_utils import (
    creeaza_socket_tcp,
    creeaza_socket_udp,
    verifica_port,
    obtine_ip_local,
    rezolva_hostname,
)

__all__ = [
    'creeaza_socket_tcp',
    'creeaza_socket_udp',
    'verifica_port',
    'obtine_ip_local',
    'rezolva_hostname',
]
