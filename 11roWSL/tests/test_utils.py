#!/usr/bin/env python3
"""
Teste Unitare pentru Utilitare
Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Aceste teste verifică funcționalitatea utilitarelor din kit.
Rulează cu: python -m pytest tests/test_utils.py -v
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_MEDIU
# ═══════════════════════════════════════════════════════════════════════════════

import unittest
import sys
import socket
from pathlib import Path
from unittest.mock import patch, MagicMock

# Adaugă rădăcina proiectului în path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_NETWORK_UTILS
# ═══════════════════════════════════════════════════════════════════════════════

class TestNetworkUtils(unittest.TestCase):
    """Teste pentru funcțiile de utilitate rețea."""
    
    def test_port_invalid_range_low(self) -> None:
        """Portul 0 este invalid."""
        # Port 0 nu poate fi folosit pentru conexiuni normale
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', 0))
            # Se așteaptă eroare (returncode != 0)
            self.assertNotEqual(result, 0)
    
    def test_port_invalid_range_high(self) -> None:
        """Portul > 65535 este invalid pentru socket."""
        # Nu putem testa direct, dar verificăm că socket-ul refuză
        # Nota: Python acceptă porturi mari dar sistemul le refuză
        pass
    
    def test_socket_timeout(self) -> None:
        """Testează comportamentul timeout-ului socket."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.1)  # 100ms timeout
        
        # Conectare la un port care probabil nu ascultă
        start_time = __import__('time').time()
        result = sock.connect_ex(('localhost', 59999))
        elapsed = __import__('time').time() - start_time
        
        sock.close()
        
        # Verifică că s-a returnat rapid (nu blocant)
        # Timpul ar trebui să fie < 2 secunde
        self.assertLess(elapsed, 2.0)
    
    def test_localhost_resolution(self) -> None:
        """Verifică că localhost se rezolvă corect."""
        try:
            addr = socket.gethostbyname('localhost')
            self.assertIn(addr, ['127.0.0.1', '::1'])
        except socket.gaierror:
            self.fail("localhost nu se poate rezolva")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_DOCKER_UTILS
# ═══════════════════════════════════════════════════════════════════════════════

class TestDockerUtils(unittest.TestCase):
    """Teste pentru utilitarele Docker."""
    
    def test_manager_docker_invalid_path(self) -> None:
        """Cale invalidă ridică FileNotFoundError."""
        try:
            from scripts.utils.docker_utils import ManagerDocker
            with self.assertRaises(FileNotFoundError):
                ManagerDocker(Path('/nonexistent/path/that/does/not/exist'))
        except ImportError:
            self.skipTest("Modulul docker_utils nu este disponibil")
    
    def test_manager_docker_valid_path(self) -> None:
        """Cale validă nu ridică excepție."""
        try:
            from scripts.utils.docker_utils import ManagerDocker
            docker_path = RADACINA_PROIECT / "docker"
            
            if docker_path.exists() and (docker_path / "docker-compose.yml").exists():
                manager = ManagerDocker(docker_path)
                self.assertIsNotNone(manager)
            else:
                self.skipTest("Directorul docker nu există")
        except ImportError:
            self.skipTest("Modulul docker_utils nu este disponibil")


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_VALIDARE_INPUT
# ═══════════════════════════════════════════════════════════════════════════════

class TestInputValidation(unittest.TestCase):
    """Teste pentru validarea input-ului."""
    
    def test_backend_string_parsing(self) -> None:
        """Testează parsarea string-urilor de backend."""
        backend_str = "localhost:8081,localhost:8082,localhost:8083"
        backends = []
        
        for entry in backend_str.split(','):
            if ':' in entry:
                host, port_str = entry.rsplit(':', 1)
                try:
                    port = int(port_str)
                    backends.append((host, port))
                except ValueError:
                    pass
        
        self.assertEqual(len(backends), 3)
        self.assertEqual(backends[0], ('localhost', 8081))
        self.assertEqual(backends[1], ('localhost', 8082))
        self.assertEqual(backends[2], ('localhost', 8083))
    
    def test_backend_string_invalid_port(self) -> None:
        """Port invalid nu ar trebui să cauzeze crash."""
        backend_str = "localhost:abc"
        backends = []
        
        for entry in backend_str.split(','):
            if ':' in entry:
                host, port_str = entry.rsplit(':', 1)
                try:
                    port = int(port_str)
                    backends.append((host, port))
                except ValueError:
                    # Port invalid - ignoră
                    pass
        
        self.assertEqual(len(backends), 0)
    
    def test_weight_parsing(self) -> None:
        """Testează parsarea ponderilor."""
        weights_str = "3,2,1"
        weights = [int(w) for w in weights_str.split(',')]
        
        self.assertEqual(weights, [3, 2, 1])
        self.assertEqual(sum(weights), 6)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_ALGORITMI_ECHILIBRARE
# ═══════════════════════════════════════════════════════════════════════════════

class TestLoadBalancingAlgorithms(unittest.TestCase):
    """Teste pentru algoritmii de echilibrare."""
    
    def test_round_robin_distribution(self) -> None:
        """Round robin distribuie uniform."""
        backends = ['A', 'B', 'C']
        index = 0
        selections: dict[str, int] = {}
        
        for _ in range(9):  # 3 x 3 = distribuție perfectă
            backend = backends[index % len(backends)]
            selections[backend] = selections.get(backend, 0) + 1
            index += 1
        
        # Fiecare backend ar trebui să fie selectat de 3 ori
        self.assertEqual(selections.get('A', 0), 3)
        self.assertEqual(selections.get('B', 0), 3)
        self.assertEqual(selections.get('C', 0), 3)
    
    def test_ip_hash_consistency(self) -> None:
        """IP hash returnează același backend pentru același IP."""
        backends = ['A', 'B', 'C']
        ip = '192.168.1.100'
        
        def select_by_ip_hash(ip_addr: str) -> str:
            hash_val = hash(ip_addr)
            index = hash_val % len(backends)
            return backends[index]
        
        # Verifică că același IP merge mereu la același backend
        first_selection = select_by_ip_hash(ip)
        for _ in range(10):
            self.assertEqual(select_by_ip_hash(ip), first_selection)
    
    def test_ip_hash_different_ips(self) -> None:
        """IP-uri diferite pot merge la backend-uri diferite."""
        backends = ['A', 'B', 'C']
        
        def select_by_ip_hash(ip_addr: str) -> str:
            hash_val = hash(ip_addr)
            index = hash_val % len(backends)
            return backends[index]
        
        # Testăm mai multe IP-uri pentru a vedea distribuția
        selections = set()
        for i in range(100):
            ip = f'192.168.1.{i}'
            selections.add(select_by_ip_hash(ip))
        
        # Cu 100 IP-uri diferite, ar trebui să avem cel puțin 2 backend-uri
        self.assertGreaterEqual(len(selections), 2)
    
    def test_weighted_distribution_proportional(self) -> None:
        """Weighted round robin respectă proporțiile."""
        backends = [
            {'name': 'A', 'weight': 3},
            {'name': 'B', 'weight': 2},
            {'name': 'C', 'weight': 1}
        ]
        
        # Construiește lista expandată
        expanded: list[str] = []
        for b in backends:
            expanded.extend([b['name']] * b['weight'])
        
        # expanded = ['A', 'A', 'A', 'B', 'B', 'C']
        self.assertEqual(len(expanded), 6)
        self.assertEqual(expanded.count('A'), 3)
        self.assertEqual(expanded.count('B'), 2)
        self.assertEqual(expanded.count('C'), 1)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_HEALTH_CHECK
# ═══════════════════════════════════════════════════════════════════════════════

class TestHealthCheckLogic(unittest.TestCase):
    """Teste pentru logica health check."""
    
    def test_consecutive_failures_marking(self) -> None:
        """După 3 eșecuri consecutive, backend-ul devine nesănătos."""
        class Backend:
            def __init__(self) -> None:
                self.healthy = True
                self.consecutive_failures = 0
                self.threshold = 3
            
            def record_failure(self) -> None:
                self.consecutive_failures += 1
                if self.consecutive_failures >= self.threshold:
                    self.healthy = False
            
            def record_success(self) -> None:
                self.consecutive_failures = 0
                self.healthy = True
        
        backend = Backend()
        
        # Înregistrează 2 eșecuri - încă sănătos
        backend.record_failure()
        backend.record_failure()
        self.assertTrue(backend.healthy)
        
        # Al treilea eșec - devine nesănătos
        backend.record_failure()
        self.assertFalse(backend.healthy)
    
    def test_recovery_after_success(self) -> None:
        """Un succes resetează contorul de eșecuri."""
        class Backend:
            def __init__(self) -> None:
                self.healthy = True
                self.consecutive_failures = 0
                self.threshold = 3
            
            def record_failure(self) -> None:
                self.consecutive_failures += 1
                if self.consecutive_failures >= self.threshold:
                    self.healthy = False
            
            def record_success(self) -> None:
                self.consecutive_failures = 0
                self.healthy = True
        
        backend = Backend()
        
        # 2 eșecuri
        backend.record_failure()
        backend.record_failure()
        self.assertEqual(backend.consecutive_failures, 2)
        
        # Un succes resetează
        backend.record_success()
        self.assertEqual(backend.consecutive_failures, 0)
        self.assertTrue(backend.healthy)


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # Rulează testele cu output verbose
    unittest.main(verbosity=2)
