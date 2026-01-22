#!/usr/bin/env python3
"""
Constante pentru Modulul de Rețea
Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix

Centralizează valorile folosite în mai multe module pentru a evita magic numbers.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# Constante IPv4
# ═══════════════════════════════════════════════════════════════════════════════

BITI_IPV4 = 32
BITI_OCTET = 8
NUMAR_OCTETI_IPV4 = 4

PREFIX_MIN_IPV4 = 0
PREFIX_MAX_IPV4 = 32

# Adrese rezervate per rețea (adresa de rețea + broadcast)
ADRESE_REZERVATE_PER_RETEA = 2

# Valori octet
OCTET_MIN = 0
OCTET_MAX = 255

# ═══════════════════════════════════════════════════════════════════════════════
# Constante IPv6
# ═══════════════════════════════════════════════════════════════════════════════

BITI_IPV6 = 128
BITI_HEXTET = 16
NUMAR_HEXTETE_IPV6 = 8

PREFIX_MIN_IPV6 = 0
PREFIX_MAX_IPV6 = 128

# Lungimea adresei IPv6 expandate (cu toate zerourile și separatorii)
LUNGIME_IPV6_EXPANDAT = 39  # 8 grupuri * 4 caractere + 7 separatori

# ═══════════════════════════════════════════════════════════════════════════════
# Clase IP Tradiționale (pentru referință)
# ═══════════════════════════════════════════════════════════════════════════════

CLASE_IP = {
    'A': {
        'octet_start': 1,
        'octet_end': 126,
        'prefix_default': 8,
        'descriere': 'Rețele mari (16M gazde)'
    },
    'B': {
        'octet_start': 128,
        'octet_end': 191,
        'prefix_default': 16,
        'descriere': 'Rețele medii (65K gazde)'
    },
    'C': {
        'octet_start': 192,
        'octet_end': 223,
        'prefix_default': 24,
        'descriere': 'Rețele mici (254 gazde)'
    },
    'D': {
        'octet_start': 224,
        'octet_end': 239,
        'prefix_default': None,
        'descriere': 'Multicast'
    },
    'E': {
        'octet_start': 240,
        'octet_end': 255,
        'prefix_default': None,
        'descriere': 'Experimental/Rezervat'
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# Adrese Speciale IPv4
# ═══════════════════════════════════════════════════════════════════════════════

ADRESE_PRIVATE = [
    ('10.0.0.0', 8),      # Clasa A privată
    ('172.16.0.0', 12),   # Clasa B privată
    ('192.168.0.0', 16),  # Clasa C privată
]

ADRESE_SPECIALE = {
    'loopback': ('127.0.0.0', 8),
    'link_local': ('169.254.0.0', 16),
    'multicast': ('224.0.0.0', 4),
    'broadcast_limitat': ('255.255.255.255', 32),
    'retea_curenta': ('0.0.0.0', 8),
}

# ═══════════════════════════════════════════════════════════════════════════════
# Timeout-uri (secunde)
# ═══════════════════════════════════════════════════════════════════════════════

TIMEOUT_DOCKER_INFO = 10
TIMEOUT_DOCKER_COMPOSE = 60
TIMEOUT_HEALTH_CHECK = 30
TIMEOUT_PING = 5

# ═══════════════════════════════════════════════════════════════════════════════
# Configurație Laborator Săptămâna 5
# ═══════════════════════════════════════════════════════════════════════════════

LAB_NETWORK_NAME = "week5_labnet"
LAB_NETWORK_SUBNET = "10.5.0.0/24"
LAB_NETWORK_GATEWAY = "10.5.0.1"

LAB_CONTAINERS = {
    'python': {
        'name': 'week5_python',
        'ip': '10.5.0.10',
        'descriere': 'Container principal pentru exerciții Python'
    },
    'udp_server': {
        'name': 'week5_udp-server',
        'ip': '10.5.0.20',
        'port': 9999,
        'descriere': 'Server UDP Echo pentru demonstrații'
    },
    'udp_client': {
        'name': 'week5_udp-client',
        'ip': '10.5.0.30',
        'descriere': 'Client UDP pentru testare'
    },
}

# ═══════════════════════════════════════════════════════════════════════════════
# Portainer
# ═══════════════════════════════════════════════════════════════════════════════

PORTAINER_PORT = 9000
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"
PORTAINER_URL = f"http://localhost:{PORTAINER_PORT}"

# ═══════════════════════════════════════════════════════════════════════════════
# Credențiale WSL
# ═══════════════════════════════════════════════════════════════════════════════

WSL_USER = "stud"
WSL_PASS = "stud"

# ═══════════════════════════════════════════════════════════════════════════════
# Formatare Output
# ═══════════════════════════════════════════════════════════════════════════════

SEPARATOR_LINIE = "═" * 55
SEPARATOR_SECTIUNE = "─" * 55

# Coduri ANSI pentru culori (pentru terminale care le suportă)
class Culori:
    """Coduri ANSI pentru colorarea output-ului în terminal."""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Culori text
    ROSU = "\033[91m"
    VERDE = "\033[92m"
    GALBEN = "\033[93m"
    ALBASTRU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    
    # Fundal
    BG_ROSU = "\033[41m"
    BG_VERDE = "\033[42m"
    BG_GALBEN = "\033[43m"


def coloreaza(text: str, culoare: str) -> str:
    """
    Aplică culoare unui text pentru afișare în terminal.
    
    Args:
        text: Textul de colorat
        culoare: Codul de culoare din clasa Culori
    
    Returns:
        Textul cu coduri ANSI pentru culoare
    """
    return f"{culoare}{text}{Culori.RESET}"


# ═══════════════════════════════════════════════════════════════════════════════
# Validare Pattern-uri Regex
# ═══════════════════════════════════════════════════════════════════════════════

import re

# Pattern pentru adresă IPv4 simplă
PATTERN_IPV4 = re.compile(
    r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
)

# Pattern pentru notație CIDR IPv4
PATTERN_CIDR_IPV4 = re.compile(
    r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/(\d{1,2})$'
)

# Pattern pentru adresă IPv6 (simplificat)
PATTERN_IPV6 = re.compile(
    r'^([0-9a-fA-F]{0,4}:){2,7}[0-9a-fA-F]{0,4}$|'
    r'^::$|'
    r'^::1$|'
    r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
)


# ═══════════════════════════════════════════════════════════════════════════════
# Versiune Modul
# ═══════════════════════════════════════════════════════════════════════════════

__version__ = "1.0.0"
__author__ = "Laborator Rețele ASE"
