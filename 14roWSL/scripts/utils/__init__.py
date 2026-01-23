"""
Utility modules for Week 14 Laboratory Scripts.

NETWORKING class - ASE, Informatics | by Revolvix

This package provides common utilities for Docker management,
network operations, logging, and console output across all laboratory scripts.
"""

from .docker_utils import DockerManager
from .network_utils import NetworkUtils
from .logger import setup_logger, get_logger
from .console import (
    Colors, C,
    info, success, warning, error,
    header, subheader, status_line, progress,
    afiseaza_info, afiseaza_succes, afiseaza_avertisment, afiseaza_eroare,
)

__all__ = [
    # Core utilities
    'DockerManager',
    'NetworkUtils',
    'setup_logger',
    'get_logger',
    
    # Console output
    'Colors', 'C',
    'info', 'success', 'warning', 'error',
    'header', 'subheader', 'status_line', 'progress',
    
    # Romanian aliases
    'afiseaza_info', 'afiseaza_succes', 'afiseaza_avertisment', 'afiseaza_eroare',
]
