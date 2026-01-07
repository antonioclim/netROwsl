"""
Pachet Utilitare pentru Scripturi
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Acest pachet conține module helper pentru:
- Jurnalizare colorată (logger)
- Gestionare Docker (docker_utils)
- Diagnosticare rețea (network_utils)
"""

from .logger import (
    configureaza_logger,
    afiseaza_banner,
    afiseaza_succes,
    afiseaza_eroare,
    afiseaza_avertisment,
    afiseaza_info,
    # Alias-uri pentru compatibilitate
    setup_logger,
    print_banner,
)

from .docker_utils import (
    ManagerDocker,
    DockerManager,  # Alias
)

from .network_utils import (
    verifica_port,
    asteapta_port,
    ping_gazda,
    testeaza_conexiune_ftp,
    obtine_ip_local,
    rezolva_hostname,
    scaneaza_porturi,
    formateaza_dimensiune,
    # Alias-uri pentru compatibilitate
    check_port,
    wait_for_port,
    ping_host,
    test_ftp_connection,
    get_local_ip,
)

__all__ = [
    # Logger
    'configureaza_logger',
    'afiseaza_banner',
    'afiseaza_succes',
    'afiseaza_eroare',
    'afiseaza_avertisment',
    'afiseaza_info',
    'setup_logger',
    'print_banner',
    
    # Docker
    'ManagerDocker',
    'DockerManager',
    
    # Network
    'verifica_port',
    'asteapta_port',
    'ping_gazda',
    'testeaza_conexiune_ftp',
    'obtine_ip_local',
    'rezolva_hostname',
    'scaneaza_porturi',
    'formateaza_dimensiune',
    'check_port',
    'wait_for_port',
    'ping_host',
    'test_ftp_connection',
    'get_local_ip',
]
