"""
Modul de Utilitare pentru Săptămâna 5
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix
"""

from .net_utils import (
    analizeaza_interfata_ipv4,
    imparte_flsm,
    aloca_vlsm,
    comprima_ipv6,
    expandeaza_ipv6,
    subretele_ipv6_din_prefix,
    prefix_pentru_gazde,
    interval_gazde_ipv4,
    ip_la_binar,
    ip_la_binar_punctat,
    prefix_la_masca,
    masca_la_prefix,
)

__all__ = [
    'analizeaza_interfata_ipv4',
    'imparte_flsm',
    'aloca_vlsm',
    'comprima_ipv6',
    'expandeaza_ipv6',
    'subretele_ipv6_din_prefix',
    'prefix_pentru_gazde',
    'interval_gazde_ipv4',
    'ip_la_binar',
    'ip_la_binar_punctat',
    'prefix_la_masca',
    'masca_la_prefix',
]
