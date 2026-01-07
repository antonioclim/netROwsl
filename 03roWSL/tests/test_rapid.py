#!/usr/bin/env python3
"""
Test Rapid de Verificare
Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Verificare rapidă (<60s) că mediul de laborator este pregătit.
Rulează verificări de bază pentru Docker, containere și conectivitate.

Utilizare:
    python tests/test_rapid.py
"""

import socket
import struct
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime


class TestRapid:
    """Suite de teste rapide pentru verificarea mediului."""
    
    def __init__(self):
        self.rezultate = []
        self.timp_start = time.time()
    
    def log(self, mesaj: str) -> None:
        """Afișează un mesaj cu timestamp."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] {mesaj}")
    
    def verifica(self, nume: str, test_func) -> bool:
        """
        Rulează o verificare și înregistrează rezultatul.
        
        Args:
            nume: Numele testului
            test_func: Funcția de test (returnează bool)
            
        Returns:
            Rezultatul testului
        """
        try:
            start = time.time()
            rezultat = test_func()
            durata = time.time() - start
            
            stare = "✓ TRECUT" if rezultat else "✗ EȘUAT"
            culoare = "\033[32m" if rezultat else "\033[31m"
            reset = "\033[0m"
            
            self.log(f"{culoare}{stare}{reset} {nume} ({durata:.2f}s)")
            self.rezultate.append((nume, rezultat))
            return rezultat
            
        except Exception as e:
            self.log(f"\033[33m⊘ SĂRIT\033[0m {nume}: {e}")
            self.rezultate.append((nume, None))
            return False
    
    # ═══════════════════════════════════════════════════════════════════════
    # VERIFICĂRI DOCKER
    # ═══════════════════════════════════════════════════════════════════════
    
    def test_docker_disponibil(self) -> bool:
        """Verifică că Docker este instalat și rulează."""
        rezultat = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    
    def test_compose_valid(self) -> bool:
        """Verifică că docker-compose.yml este valid."""
        cale = Path(__file__).parent.parent / "docker" / "docker-compose.yml"
        
        rezultat = subprocess.run(
            ["docker", "compose", "-f", str(cale), "config", "-q"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    
    def test_container_server(self) -> bool:
        """Verifică că containerul server rulează."""
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week3_server"],
            capture_output=True,
            timeout=10
        )
        return "true" in rezultat.stdout.decode().lower()
    
    def test_container_router(self) -> bool:
        """Verifică că containerul router rulează."""
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week3_router"],
            capture_output=True,
            timeout=10
        )
        return "true" in rezultat.stdout.decode().lower()
    
    def test_container_client(self) -> bool:
        """Verifică că containerul client rulează."""
        rezultat = subprocess.run(
            ["docker", "inspect", "-f", "{{.State.Running}}", "week3_client"],
            capture_output=True,
            timeout=10
        )
        return "true" in rezultat.stdout.decode().lower()
    
    def test_retea_docker(self) -> bool:
        """Verifică că rețeaua Docker există."""
        rezultat = subprocess.run(
            ["docker", "network", "inspect", "week3_network"],
            capture_output=True,
            timeout=10
        )
        return rezultat.returncode == 0
    
    # ═══════════════════════════════════════════════════════════════════════
    # VERIFICĂRI CONECTIVITATE
    # ═══════════════════════════════════════════════════════════════════════
    
    def test_server_echo_raspunde(self) -> bool:
        """Verifică că serverul echo răspunde."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 8080))
            
            sock.sendall(b"test")
            raspuns = sock.recv(1024)
            sock.close()
            
            return raspuns == b"test"
        except Exception:
            return False
    
    def test_tunel_redirecționeaza(self) -> bool:
        """Verifică că tunelul redirecționează corect."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("localhost", 9090))
            
            sock.sendall(b"test tunel")
            raspuns = sock.recv(1024)
            sock.close()
            
            return raspuns == b"test tunel"
        except Exception:
            return False
    
    # ═══════════════════════════════════════════════════════════════════════
    # VERIFICĂRI SOCKET-URI
    # ═══════════════════════════════════════════════════════════════════════
    
    def test_socket_broadcast(self) -> bool:
        """Verifică că se poate crea un socket broadcast."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            valoare = sock.getsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST)
            sock.close()
            return valoare != 0
        except Exception:
            return False
    
    def test_join_multicast(self) -> bool:
        """Verifică că se poate alătura unui grup multicast."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            mreq = struct.pack(
                '4s4s',
                socket.inet_aton('239.0.0.1'),
                socket.inet_aton('0.0.0.0')
            )
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            sock.close()
            return True
        except Exception:
            return False
    
    # ═══════════════════════════════════════════════════════════════════════
    # VERIFICĂRI INSTRUMENTE
    # ═══════════════════════════════════════════════════════════════════════
    
    def test_tcpdump_in_container(self) -> bool:
        """Verifică că tcpdump este disponibil în containere."""
        rezultat = subprocess.run(
            ["docker", "exec", "week3_client", "which", "tcpdump"],
            capture_output=True,
            timeout=10
        )
        return "tcpdump" in rezultat.stdout.decode()
    
    def test_sintaxa_scripturi(self) -> bool:
        """Verifică sintaxa Python a scripturilor principale."""
        radacina = Path(__file__).parent.parent
        scripturi = list(radacina.rglob("*.py"))
        
        for script in scripturi[:20]:  # Limitează pentru rapiditate
            rezultat = subprocess.run(
                [sys.executable, "-m", "py_compile", str(script)],
                capture_output=True,
                timeout=5
            )
            if rezultat.returncode != 0:
                return False
        
        return True
    
    # ═══════════════════════════════════════════════════════════════════════
    # RULARE TESTE
    # ═══════════════════════════════════════════════════════════════════════
    
    def ruleaza(self) -> int:
        """
        Rulează toate testele rapide.
        
        Returns:
            0 dacă totul a trecut, 1 altfel
        """
        print("=" * 60)
        print("TEST RAPID DE VERIFICARE - Săptămâna 3")
        print("Rețele de Calculatoare - ASE, Informatică Economică")
        print("=" * 60)
        print()
        
        # Verificări Docker
        print("Verificări Docker:")
        print("-" * 40)
        self.verifica("Docker disponibil", self.test_docker_disponibil)
        self.verifica("Compose valid", self.test_compose_valid)
        self.verifica("Container server", self.test_container_server)
        self.verifica("Container router", self.test_container_router)
        self.verifica("Container client", self.test_container_client)
        self.verifica("Rețea Docker", self.test_retea_docker)
        print()
        
        # Verificări conectivitate
        print("Verificări Conectivitate:")
        print("-" * 40)
        self.verifica("Server echo răspunde", self.test_server_echo_raspunde)
        self.verifica("Tunel redirecționează", self.test_tunel_redirecționeaza)
        print()
        
        # Verificări socket-uri
        print("Verificări Socket-uri:")
        print("-" * 40)
        self.verifica("Socket broadcast", self.test_socket_broadcast)
        self.verifica("Join multicast", self.test_join_multicast)
        print()
        
        # Verificări instrumente
        print("Verificări Instrumente:")
        print("-" * 40)
        self.verifica("tcpdump în container", self.test_tcpdump_in_container)
        self.verifica("Sintaxă scripturi", self.test_sintaxa_scripturi)
        print()
        
        # Sumar
        durata_totala = time.time() - self.timp_start
        trecute = sum(1 for _, r in self.rezultate if r is True)
        esuate = sum(1 for _, r in self.rezultate if r is False)
        sarite = sum(1 for _, r in self.rezultate if r is None)
        
        print("=" * 60)
        print(f"REZULTAT: {trecute} trecute, {esuate} eșuate, {sarite} sărite")
        print(f"Timp total: {durata_totala:.2f}s")
        print("=" * 60)
        
        if esuate == 0:
            print("\n\033[32m✓ PREGĂTIT PENTRU LABORATOR\033[0m")
            print("\nPuteți începe exercițiile!")
            return 0
        else:
            print("\n\033[31m✗ PROBLEME DETECTATE\033[0m")
            print("\nVerificați:")
            print("  1. Docker Desktop este pornit")
            print("  2. Laboratorul este pornit: python scripts/porneste_lab.py")
            print("  3. Consultați docs/depanare.md pentru soluții")
            return 1


def main():
    """Punct de intrare principal."""
    tester = TestRapid()
    return tester.ruleaza()


if __name__ == "__main__":
    sys.exit(main())
