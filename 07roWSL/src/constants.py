#!/usr/bin/env python3
"""
Constante globale pentru laboratorul Săptămâna 7.
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest modul centralizează toate valorile configurabile pentru a facilita
modificarea și a evita magic numbers în cod.

Utilizare:
    from src.constants import PORT_TCP_ECHO, PORTAINER_URL
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATIE_RETEA — Porturi și adrese IP
# ═══════════════════════════════════════════════════════════════════════════════

# Porturi servicii laborator
PORT_TCP_ECHO = 9090
PORT_UDP_RECEPTOR = 9091
PORT_FILTRU_APLICATIE = 8888
PORT_PORTAINER = 9000  # ⚠️ NU MODIFICA - rezervat global pentru Portainer

# Adrese IP în rețeaua Docker (week7net: 10.0.7.0/24)
IP_SERVER_TCP = "10.0.7.100"
IP_RECEPTOR_UDP = "10.0.7.200"
IP_FILTRU = "10.0.7.50"
IP_DEMO = "10.0.7.10"
IP_GATEWAY = "10.0.7.1"

# Configurare subnet
SUBNET_LABORATOR = "10.0.7.0/24"
NUME_RETEA = "week7net"

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATIE_CONTAINERE — Nume și imagini Docker
# ═══════════════════════════════════════════════════════════════════════════════

PREFIX_CONTAINER = "week7_"
IMAGINE_PYTHON = "python:3.11-slim"

# Nume complete containere
CONTAINER_SERVER_TCP = f"{PREFIX_CONTAINER}server_tcp"
CONTAINER_RECEPTOR_UDP = f"{PREFIX_CONTAINER}receptor_udp"
CONTAINER_FILTRU = f"{PREFIX_CONTAINER}filtru_pachete"
CONTAINER_DEMO = f"{PREFIX_CONTAINER}demo"

# ═══════════════════════════════════════════════════════════════════════════════
# CREDENTIALE_STANDARD — Autentificare servicii
# ═══════════════════════════════════════════════════════════════════════════════

# WSL Ubuntu
WSL_USER = "stud"
WSL_PASS = "stud"

# Portainer CE
PORTAINER_USER = "stud"
PORTAINER_PASS = "studstudstud"
PORTAINER_URL = f"http://localhost:{PORT_PORTAINER}"

# ═══════════════════════════════════════════════════════════════════════════════
# TIMEOUT_URI — Valori de timeout în secunde
# ═══════════════════════════════════════════════════════════════════════════════

TIMEOUT_CONEXIUNE_TCP = 5.0
TIMEOUT_CONEXIUNE_UDP = 3.0
TIMEOUT_HEALTH_CHECK = 30
TIMEOUT_DOCKER_INFO = 10
TIMP_ASTEPTARE_SERVICIU = 5  # după pornire container

# ═══════════════════════════════════════════════════════════════════════════════
# CUVINTE_CHEIE_FILTRU — Pentru filtrul la nivel aplicație
# ═══════════════════════════════════════════════════════════════════════════════

CUVINTE_BLOCATE_DEFAULT = [
    "malware",
    "virus",
    "hack",
    "exploit",
    "injection",
]

# ═══════════════════════════════════════════════════════════════════════════════
# PROFILE_FIREWALL — Nume profile predefinite
# ═══════════════════════════════════════════════════════════════════════════════

PROFIL_REFERINTA = "referinta"
PROFIL_BLOCARE_TCP = "blocare_tcp_9090"
PROFIL_BLOCARE_UDP = "blocare_udp_9091"
PROFIL_MIXT = "filtrare_mixta"
