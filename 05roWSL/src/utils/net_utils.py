#!/usr/bin/env python3
"""
Utilitare de Rețea pentru Adresare IP
=====================================
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Acest modul oferă funcții pentru:
- Analiza adreselor IPv4 și CIDR
- Subnetare FLSM și VLSM
- Operații cu adrese IPv6
- Conversii binare și calcule de mască

Funcții principale:
    analizeaza_interfata_ipv4() - Analizează o adresă IPv4/CIDR
    imparte_flsm() - Împarte o rețea în subrețele egale
    aloca_vlsm() - Alocă subrețele cu mască variabilă
    comprima_ipv6() - Comprimă o adresă IPv6
    expandeaza_ipv6() - Expandează o adresă IPv6
"""

from __future__ import annotations

import ipaddress
import math
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

# Tipuri pentru adrese IP
AdresaIPv4 = Union[str, ipaddress.IPv4Address]
AdresaIPv6 = Union[str, ipaddress.IPv6Address]
ReteaCIDR = Union[str, ipaddress.IPv4Network, ipaddress.IPv6Network]


# =============================================================================
# Clase de date
# =============================================================================

@dataclass
class InfoRetea:
    """Informații complete despre o adresă IPv4 și rețeaua sa."""
    adresa: ipaddress.IPv4Address
    retea: ipaddress.IPv4Network
    masca: ipaddress.IPv4Address
    wildcard: ipaddress.IPv4Address
    broadcast: ipaddress.IPv4Address
    total_adrese: int
    gazde_utilizabile: int
    prima_gazda: Optional[ipaddress.IPv4Address]
    ultima_gazda: Optional[ipaddress.IPv4Address]
    este_privata: bool
    tip_adresa: str


# Alias pentru compatibilitate cu versiunea engleză
IPv4NetworkInfo = InfoRetea


# =============================================================================
# Funcții de analiză IPv4
# =============================================================================

def analizeaza_interfata_ipv4(cidr: str) -> InfoRetea:
    """
    Analizează o adresă IPv4 cu prefix CIDR și returnează informații complete.
    
    Args:
        cidr: Adresă în format CIDR (ex: "192.168.10.14/26")
    
    Returns:
        InfoRetea cu toate detaliile despre rețea
    
    Raises:
        ValueError: Dacă formatul CIDR este invalid
    
    Exemplu:
        >>> info = analizeaza_interfata_ipv4("192.168.10.14/26")
        >>> print(info.gazde_utilizabile)
        62
    """
    try:
        # Parsează interfața (adresă cu prefix)
        interfata = ipaddress.ip_interface(cidr)
        adresa = interfata.ip
        retea = interfata.network
        
        # Calculează masca și wildcard
        masca = retea.netmask
        wildcard = retea.hostmask
        broadcast = retea.broadcast_address
        
        # Calculează gazdele
        total = retea.num_addresses
        utilizabile = max(0, total - 2)  # Minus rețea și broadcast
        
        # Prima și ultima gazdă
        gazde = list(retea.hosts())
        prima = gazde[0] if gazde else None
        ultima = gazde[-1] if gazde else None
        
        # Determină tipul adresei
        if adresa.is_private:
            tip = "privată"
        elif adresa.is_loopback:
            tip = "loopback"
        elif adresa.is_multicast:
            tip = "multicast"
        elif adresa.is_reserved:
            tip = "rezervată"
        else:
            tip = "publică"
        
        return InfoRetea(
            adresa=adresa,
            retea=retea,
            masca=masca,
            wildcard=wildcard,
            broadcast=broadcast,
            total_adrese=total,
            gazde_utilizabile=utilizabile,
            prima_gazda=prima,
            ultima_gazda=ultima,
            este_privata=adresa.is_private,
            tip_adresa=tip
        )
    
    except ValueError as e:
        raise ValueError(f"Format CIDR invalid '{cidr}': {e}")


# Alias pentru compatibilitate
analyze_ipv4_interface = analizeaza_interfata_ipv4


def interval_gazde_ipv4(retea: ipaddress.IPv4Network) -> Tuple[Optional[ipaddress.IPv4Address], Optional[ipaddress.IPv4Address], int]:
    """
    Returnează intervalul de gazde utilizabile pentru o rețea.
    
    Args:
        retea: Obiect IPv4Network
    
    Returns:
        Tuple (prima_gazda, ultima_gazda, numar_gazde)
    """
    gazde = list(retea.hosts())
    if not gazde:
        return None, None, 0
    return gazde[0], gazde[-1], len(gazde)


# Alias pentru compatibilitate
ipv4_host_range = interval_gazde_ipv4


# =============================================================================
# Funcții de conversie binară
# =============================================================================

def ip_la_binar(ip: str) -> str:
    """
    Convertește o adresă IPv4 la reprezentare binară (32 de biți).
    
    Args:
        ip: Adresă IPv4 în format zecimal punctat
    
    Returns:
        Șir de 32 de caractere binare (0 și 1)
    
    Exemplu:
        >>> ip_la_binar("192.168.1.1")
        '11000000101010000000000100000001'
    """
    octeti = ip.split('.')
    return ''.join(format(int(octet), '08b') for octet in octeti)


# Alias pentru compatibilitate
ip_to_binary = ip_la_binar


def ip_la_binar_punctat(ip: str) -> str:
    """
    Convertește o adresă IPv4 la reprezentare binară cu puncte.
    
    Args:
        ip: Adresă IPv4 în format zecimal punctat
    
    Returns:
        Șir binar cu puncte între octeți
    
    Exemplu:
        >>> ip_la_binar_punctat("192.168.1.1")
        '11000000.10101000.00000001.00000001'
    """
    octeti = ip.split('.')
    return '.'.join(format(int(octet), '08b') for octet in octeti)


# Alias pentru compatibilitate
ip_to_dotted_binary = ip_la_binar_punctat


def binar_la_ip(binar: str) -> str:
    """
    Convertește un șir binar de 32 de biți la adresă IPv4.
    
    Args:
        binar: Șir de 32 de caractere binare
    
    Returns:
        Adresă IPv4 în format zecimal punctat
    """
    # Elimină punctele dacă există
    binar = binar.replace('.', '')
    
    if len(binar) != 32:
        raise ValueError(f"Lungimea trebuie să fie 32 de biți, nu {len(binar)}")
    
    octeti = [str(int(binar[i:i+8], 2)) for i in range(0, 32, 8)]
    return '.'.join(octeti)


# Alias pentru compatibilitate
binary_to_ip = binar_la_ip


# =============================================================================
# Funcții de conversie prefix/mască
# =============================================================================

def prefix_la_masca(prefix: int) -> str:
    """
    Convertește o lungime de prefix CIDR la mască de rețea.
    
    Args:
        prefix: Lungimea prefixului (0-32)
    
    Returns:
        Masca de rețea în format zecimal punctat
    
    Exemplu:
        >>> prefix_la_masca(24)
        '255.255.255.0'
    """
    if not 0 <= prefix <= 32:
        raise ValueError(f"Prefixul trebuie să fie între 0 și 32, nu {prefix}")
    
    masca_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    return str(ipaddress.IPv4Address(masca_int))


# Alias pentru compatibilitate
prefix_to_netmask = prefix_la_masca


def masca_la_prefix(masca: str) -> int:
    """
    Convertește o mască de rețea la lungimea prefixului CIDR.
    
    Args:
        masca: Masca de rețea în format zecimal punctat
    
    Returns:
        Lungimea prefixului
    
    Exemplu:
        >>> masca_la_prefix("255.255.255.0")
        24
    """
    binar = ip_la_binar(masca)
    # Numără biții de 1 consecutivi de la început
    return len(binar) - len(binar.lstrip('1'))


# Alias pentru compatibilitate
netmask_to_prefix = masca_la_prefix


def prefix_pentru_gazde(numar_gazde: int) -> int:
    """
    Calculează prefixul CIDR minim pentru a acomoda un număr de gazde.
    
    Args:
        numar_gazde: Numărul de gazde necesare
    
    Returns:
        Lungimea prefixului CIDR
    
    Exemplu:
        >>> prefix_pentru_gazde(100)
        25  # 126 gazde disponibile
    """
    if numar_gazde <= 0:
        return 32
    
    # Adaugă 2 pentru adresa de rețea și broadcast
    adrese_necesare = numar_gazde + 2
    
    # Calculează puterea de 2 necesară
    biti_gazda = math.ceil(math.log2(adrese_necesare))
    
    return 32 - biti_gazda


# Alias pentru compatibilitate
prefix_for_hosts = prefix_pentru_gazde


# =============================================================================
# Funcții de subnetare FLSM
# =============================================================================

def imparte_flsm(baza: str, numar_subretele: int) -> List[ipaddress.IPv4Network]:
    """
    Împarte o rețea în subrețele egale folosind FLSM.
    
    FLSM (Fixed Length Subnet Mask) creează subrețele de dimensiuni egale.
    Numărul de subrețele trebuie să fie o putere de 2.
    
    Args:
        baza: Rețea de bază în format CIDR
        numar_subretele: Numărul de subrețele dorite (putere de 2)
    
    Returns:
        Lista de subrețele IPv4Network
    
    Raises:
        ValueError: Dacă numărul nu este putere de 2 sau rețeaua este invalidă
    
    Exemplu:
        >>> subretele = imparte_flsm("192.168.100.0/24", 4)
        >>> for s in subretele:
        ...     print(s)
        192.168.100.0/26
        192.168.100.64/26
        192.168.100.128/26
        192.168.100.192/26
    """
    # Validare: numărul trebuie să fie putere de 2
    if numar_subretele <= 0 or (numar_subretele & (numar_subretele - 1)) != 0:
        raise ValueError(f"Numărul de subrețele ({numar_subretele}) trebuie să fie o putere de 2")
    
    try:
        retea = ipaddress.ip_network(baza, strict=True)
    except ValueError:
        # Încearcă cu strict=False pentru adrese care nu sunt pe granița de rețea
        retea = ipaddress.ip_network(baza, strict=False)
    
    # Calculează noul prefix
    biti_adaugati = int(math.log2(numar_subretele))
    prefix_nou = retea.prefixlen + biti_adaugati
    
    if prefix_nou > 32:
        raise ValueError(
            f"Nu se pot crea {numar_subretele} subrețele din /{retea.prefixlen}. "
            f"Ar necesita prefix /{prefix_nou} (maxim /32)"
        )
    
    return list(retea.subnets(prefixlen_diff=biti_adaugati))


# Alias pentru compatibilitate
flsm_split = imparte_flsm


# =============================================================================
# Funcții de subnetare VLSM
# =============================================================================

def aloca_vlsm(baza: str, cerinte: List[int]) -> List[dict]:
    """
    Alocă subrețele folosind VLSM pentru cerințele date.
    
    VLSM (Variable Length Subnet Mask) alocă subrețele de dimensiuni
    diferite bazate pe cerințele specifice de gazde.
    
    Args:
        baza: Rețea de bază în format CIDR
        cerinte: Lista de cerințe de gazde pentru fiecare subrețea
    
    Returns:
        Lista de dicționare cu 'cerinta' și 'subretea'
    
    Raises:
        ValueError: Dacă spațiul de adrese este insuficient
    
    Exemplu:
        >>> alocari = aloca_vlsm("172.16.0.0/16", [500, 120, 60, 30, 2])
        >>> for a in alocari:
        ...     print(f"{a['cerinta']} gazde -> {a['subretea']}")
    """
    try:
        retea = ipaddress.ip_network(baza, strict=True)
    except ValueError:
        retea = ipaddress.ip_network(baza, strict=False)
    
    # Sortează cerințele descrescător (cele mai mari primele)
    cerinte_sortate = sorted(enumerate(cerinte), key=lambda x: x[1], reverse=True)
    
    alocari = []
    adresa_curenta = retea.network_address
    sfarsit_retea = retea.broadcast_address
    
    for idx_original, cerinta in cerinte_sortate:
        # Calculează prefixul necesar
        prefix = prefix_pentru_gazde(cerinta)
        
        # Verifică dacă mai avem spațiu
        dimensiune_bloc = 2 ** (32 - prefix)
        
        # Aliniază la granița de bloc
        adresa_int = int(adresa_curenta)
        rest = adresa_int % dimensiune_bloc
        if rest != 0:
            adresa_int += dimensiune_bloc - rest
        
        adresa_aliniat = ipaddress.IPv4Address(adresa_int)
        
        # Verifică dacă încape
        adresa_sfarsit = ipaddress.IPv4Address(int(adresa_aliniat) + dimensiune_bloc - 1)
        
        if adresa_sfarsit > sfarsit_retea:
            raise ValueError(
                f"Spațiu insuficient pentru {cerinta} gazde. "
                f"Ar fi necesar de la {adresa_aliniat}, dar rețeaua se termină la {sfarsit_retea}"
            )
        
        subretea = ipaddress.ip_network(f"{adresa_aliniat}/{prefix}", strict=True)
        
        alocari.append({
            'cerinta': cerinta,
            'subretea': subretea,
            'index_original': idx_original
        })
        
        # Avansează la următoarea adresă disponibilă
        adresa_curenta = ipaddress.IPv4Address(int(adresa_sfarsit) + 1)
    
    # Sortează înapoi după indexul original pentru consistență
    alocari.sort(key=lambda x: x['index_original'])
    
    return alocari


# Alias pentru compatibilitate
vlsm_allocate = aloca_vlsm


# =============================================================================
# Funcții IPv6
# =============================================================================

def comprima_ipv6(adresa: str) -> str:
    """
    Comprimă o adresă IPv6 la forma scurtă.
    
    Aplică regulile standard de comprimare IPv6:
    1. Elimină zerourile de început din fiecare grup
    2. Înlocuiește cel mai lung șir de grupuri consecutive de zerouri cu ::
    
    Args:
        adresa: Adresă IPv6 în orice format
    
    Returns:
        Adresa IPv6 comprimată
    
    Exemplu:
        >>> comprima_ipv6("2001:0db8:0000:0000:0000:0000:0000:0001")
        '2001:db8::1'
    """
    try:
        # Folosește biblioteca standard pentru validare și comprimare
        addr = ipaddress.IPv6Address(adresa)
        return str(addr)
    except ValueError as e:
        raise ValueError(f"Adresă IPv6 invalidă '{adresa}': {e}")


# Alias pentru compatibilitate
ipv6_compress = comprima_ipv6


def expandeaza_ipv6(adresa: str) -> str:
    """
    Expandează o adresă IPv6 comprimată la forma completă.
    
    Args:
        adresa: Adresă IPv6 în orice format
    
    Returns:
        Adresa IPv6 în format complet (8 grupuri de 4 cifre hexazecimale)
    
    Exemplu:
        >>> expandeaza_ipv6("2001:db8::1")
        '2001:0db8:0000:0000:0000:0000:0000:0001'
    """
    try:
        addr = ipaddress.IPv6Address(adresa)
        # Folosește exploded care returnează forma completă
        return addr.exploded
    except ValueError as e:
        raise ValueError(f"Adresă IPv6 invalidă '{adresa}': {e}")


# Alias pentru compatibilitate
ipv6_expand = expandeaza_ipv6


def subretele_ipv6_din_prefix(prefix_baza: str, numar: int, prefix_tinta: int = 64) -> List[ipaddress.IPv6Network]:
    """
    Generează subrețele IPv6 dintr-un prefix de bază.
    
    Args:
        prefix_baza: Prefix IPv6 de bază (ex: "2001:db8:abcd::/48")
        numar: Numărul de subrețele de generat
        prefix_tinta: Lungimea prefixului pentru subrețele (implicit: 64)
    
    Returns:
        Lista de subrețele IPv6Network
    
    Exemplu:
        >>> subretele = subretele_ipv6_din_prefix("2001:db8:abcd::/48", 4)
        >>> for s in subretele:
        ...     print(s)
    """
    try:
        retea = ipaddress.ip_network(prefix_baza, strict=False)
    except ValueError as e:
        raise ValueError(f"Prefix IPv6 invalid '{prefix_baza}': {e}")
    
    if prefix_tinta <= retea.prefixlen:
        raise ValueError(
            f"Prefixul țintă (/{prefix_tinta}) trebuie să fie mai mare decât "
            f"prefixul de bază (/{retea.prefixlen})"
        )
    
    # Generează subrețelele
    toate_subrețelele = list(retea.subnets(new_prefix=prefix_tinta))
    
    if numar > len(toate_subrețelele):
        raise ValueError(
            f"Pot fi generate maxim {len(toate_subrețelele)} subrețele /{prefix_tinta} "
            f"din prefixul /{retea.prefixlen}"
        )
    
    return toate_subrețelele[:numar]


# Alias pentru compatibilitate
ipv6_subnets_from_prefix = subretele_ipv6_din_prefix


def valideaza_ipv6(adresa: str) -> bool:
    """
    Validează o adresă IPv6.
    
    Args:
        adresa: Șirul de validat
    
    Returns:
        True dacă adresa este validă
    """
    try:
        ipaddress.IPv6Address(adresa)
        return True
    except ValueError:
        return False


# =============================================================================
# Funcții de validare și utilitate
# =============================================================================

def valideaza_cidr(cidr: str) -> bool:
    """
    Validează o notație CIDR (IPv4 sau IPv6).
    
    Args:
        cidr: Șirul de validat
    
    Returns:
        True dacă notația este validă
    """
    try:
        ipaddress.ip_network(cidr, strict=False)
        return True
    except ValueError:
        return False


def este_in_retea(ip: str, retea: str) -> bool:
    """
    Verifică dacă o adresă IP este în rețeaua specificată.
    
    Args:
        ip: Adresa IP de verificat
        retea: Rețeaua în format CIDR
    
    Returns:
        True dacă IP-ul este în rețea
    """
    try:
        adresa = ipaddress.ip_address(ip)
        net = ipaddress.ip_network(retea, strict=False)
        return adresa in net
    except ValueError:
        return False


def distanta_intre_ip(ip1: str, ip2: str) -> int:
    """
    Calculează distanța (numărul de adrese) între două IP-uri.
    
    Args:
        ip1: Prima adresă IP
        ip2: A doua adresă IP
    
    Returns:
        Numărul de adrese între cele două IP-uri
    """
    addr1 = ipaddress.ip_address(ip1)
    addr2 = ipaddress.ip_address(ip2)
    return abs(int(addr1) - int(addr2))


# =============================================================================
# Exporturi pentru compatibilitate cu versiunea engleză
# =============================================================================

__all__ = [
    # Clase
    'InfoRetea',
    'IPv4NetworkInfo',
    
    # Funcții principale - română
    'analizeaza_interfata_ipv4',
    'interval_gazde_ipv4',
    'ip_la_binar',
    'ip_la_binar_punctat',
    'binar_la_ip',
    'prefix_la_masca',
    'masca_la_prefix',
    'prefix_pentru_gazde',
    'imparte_flsm',
    'aloca_vlsm',
    'comprima_ipv6',
    'expandeaza_ipv6',
    'subretele_ipv6_din_prefix',
    'valideaza_ipv6',
    'valideaza_cidr',
    'este_in_retea',
    'distanta_intre_ip',
    
    # Alias-uri engleză
    'analyze_ipv4_interface',
    'ipv4_host_range',
    'ip_to_binary',
    'ip_to_dotted_binary',
    'binary_to_ip',
    'prefix_to_netmask',
    'netmask_to_prefix',
    'prefix_for_hosts',
    'flsm_split',
    'vlsm_allocate',
    'ipv6_compress',
    'ipv6_expand',
    'ipv6_subnets_from_prefix',
]
