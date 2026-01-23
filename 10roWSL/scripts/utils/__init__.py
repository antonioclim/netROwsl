#!/usr/bin/env python3
"""
Pachet de Utilitare pentru Laborator
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Exportă modulele de utilitare pentru uz în scripturi.

Utilizare:
    from scripts.utils import ManagerDocker, configureaza_logger, config
    
    # Sau importuri individuale
    from scripts.utils.docker_utils import ManagerDocker
    from scripts.utils.logger import configureaza_logger
    from scripts.utils.config import config
"""

from .docker_utils import ManagerDocker
from .logger import configureaza_logger
from .config import config, ConfigLab
from .network_utils import (
    verifica_port_disponibil,
    asteapta_serviciu,
    obtine_ip_local,
)

__all__ = [
    # Docker
    "ManagerDocker",
    
    # Logging
    "configureaza_logger",
    
    # Configurație
    "config",
    "ConfigLab",
    
    # Rețea
    "verifica_port_disponibil",
    "asteapta_serviciu",
    "obtine_ip_local",
]

__version__ = "1.1.0"
__author__ = "Laborator Rețele ASE"
