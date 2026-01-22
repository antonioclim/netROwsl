#!/usr/bin/env python3
"""
Teste pentru Exercițiile Săptămânii 1
Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

Acest fișier conține teste automatizate pentru verificarea corectitudinii
exercițiilor. Rulează cu: python3 -m pytest tests/test_exercitii.py -v
"""

from __future__ import annotations

import sys
import socket
import subprocess
from pathlib import Path
from typing import Optional
from unittest.mock import patch, MagicMock

import pytest

# Adaugă directorul rădăcină al proiectului la path
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))

# Import module de testat
try:
    from src.exercises.ex_1_01_latenta_ping import (
        executa_ping,
        RezultatPing,
        interpreteaza_latenta,
        interpreteaza_jitter,
        interpreteaza_pierdere,
        MIN_PACHETE,
        MAX_PACHETE,
        LATENTA_EXCELENTA_MS,
        JITTER_EXCELENT_MS,
    )
    IMPORT_PING_OK = True
except ImportError:
    IMPORT_PING_OK = False


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_REZULTAT_PING
# ═══════════════════════════════════════════════════════════════════════════════

class TestRezultatPing:
    """Teste pentru clasa RezultatPing."""
    
    def test_creare_rezultat_gol(self) -> None:
        """Un rezultat nou are valori implicite corecte."""
        r = RezultatPing(destinatie="test")
        assert r.destinatie == "test"
        assert r.pachete_trimise == 0
        assert r.pachete_primite == 0
        assert r.rtt_values == []
        assert r.pierdere_procent == 0.0
    
    def test_pierdere_procent_zero(self) -> None:
        """Dacă toate pachetele sunt primite, pierderea e 0%."""
        r = RezultatPing(destinatie="test", pachete_trimise=4, pachete_primite=4)
        assert r.pierdere_procent == 0.0
    
    def test_pierdere_procent_partial(self) -> None:
        """Calculează corect pierderea parțială."""
        r = RezultatPing(destinatie="test", pachete_trimise=4, pachete_primite=2)
        assert r.pierdere_procent == 50.0
    
    def test_pierdere_procent_total(self) -> None:
        """Dacă niciun pachet nu e primit, pierderea e 100%."""
        r = RezultatPing(destinatie="test", pachete_trimise=4, pachete_primite=0)
        assert r.pierdere_procent == 100.0
    
    def test_pierdere_procent_fara_trimise(self) -> None:
        """Dacă nu s-a trimis nimic, pierderea e 0% (nu eroare)."""
        r = RezultatPing(destinatie="test", pachete_trimise=0, pachete_primite=0)
        assert r.pierdere_procent == 0.0


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_EXECUTA_PING
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not IMPORT_PING_OK, reason="Modulul ping nu a putut fi importat")
class TestExecutaPing:
    """Teste pentru funcția executa_ping."""
    
    def test_numar_pachete_invalid_zero(self) -> None:
        """Număr de pachete 0 aruncă ValueError."""
        with pytest.raises(ValueError) as exc_info:
            executa_ping("127.0.0.1", numar_pachete=0)
        assert "numar_pachete" in str(exc_info.value)
    
    def test_numar_pachete_invalid_negativ(self) -> None:
        """Număr de pachete negativ aruncă ValueError."""
        with pytest.raises(ValueError):
            executa_ping("127.0.0.1", numar_pachete=-1)
    
    def test_numar_pachete_invalid_prea_mare(self) -> None:
        """Număr de pachete peste limită aruncă ValueError."""
        with pytest.raises(ValueError) as exc_info:
            executa_ping("127.0.0.1", numar_pachete=MAX_PACHETE + 1)
        assert str(MAX_PACHETE) in str(exc_info.value)
    
    def test_numar_pachete_valid_limita_jos(self) -> None:
        """Număr de pachete egal cu MIN_PACHETE e valid."""
        # Nu ar trebui să arunce excepție
        rezultat = executa_ping("127.0.0.1", numar_pachete=MIN_PACHETE)
        assert isinstance(rezultat, RezultatPing)
    
    @pytest.mark.slow
    def test_loopback_succes(self) -> None:
        """Ping către loopback trebuie să aibă 0% pierdere."""
        rezultat = executa_ping("127.0.0.1", numar_pachete=2)
        assert rezultat.pachete_primite == rezultat.pachete_trimise
        assert rezultat.pierdere_procent == 0.0
    
    @pytest.mark.slow
    def test_loopback_rtt_rapid(self) -> None:
        """RTT pentru loopback trebuie să fie sub 1ms."""
        rezultat = executa_ping("127.0.0.1", numar_pachete=2)
        if rezultat.rtt_avg > 0:
            assert rezultat.rtt_avg < LATENTA_EXCELENTA_MS * 10  # 10ms margine
    
    @pytest.mark.slow
    def test_destinatie_inexistenta(self) -> None:
        """Ping către IP inexistent returnează rezultat valid (nu excepție)."""
        # 192.0.2.1 e din TEST-NET, nu ar trebui să răspundă
        rezultat = executa_ping("192.0.2.1", numar_pachete=1, timeout=1)
        assert isinstance(rezultat, RezultatPing)
        # Fie timeout, fie packet loss
        assert rezultat.pachete_primite <= rezultat.pachete_trimise
    
    def test_rtt_values_lista(self) -> None:
        """RTT values trebuie să fie listă, nu None."""
        rezultat = RezultatPing(destinatie="test")
        assert isinstance(rezultat.rtt_values, list)


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_INTERPRETARE
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.skipif(not IMPORT_PING_OK, reason="Modulul ping nu a putut fi importat")
class TestInterpretareLatenta:
    """Teste pentru funcția interpreteaza_latenta."""
    
    def test_latenta_excelenta(self) -> None:
        """Latență sub pragul de excelență."""
        culoare, mesaj = interpreteaza_latenta(0.5)
        assert "excelent" in mesaj.lower()
    
    def test_latenta_buna(self) -> None:
        """Latență în intervalul bun."""
        culoare, mesaj = interpreteaza_latenta(50.0)
        assert "bună" in mesaj.lower() or "bun" in mesaj.lower()
    
    def test_latenta_ridicata(self) -> None:
        """Latență peste pragul acceptabil."""
        culoare, mesaj = interpreteaza_latenta(200.0)
        assert "ridicat" in mesaj.lower() or "distanță" in mesaj.lower()


@pytest.mark.skipif(not IMPORT_PING_OK, reason="Modulul ping nu a putut fi importat")
class TestInterpretareJitter:
    """Teste pentru funcția interpreteaza_jitter."""
    
    def test_jitter_excelent(self) -> None:
        """Jitter sub pragul de excelență."""
        culoare, mesaj = interpreteaza_jitter(0.5)
        assert "excelent" in mesaj.lower()
    
    def test_jitter_ridicat(self) -> None:
        """Jitter peste pragul acceptabil."""
        culoare, mesaj = interpreteaza_jitter(50.0)
        assert "ridicat" in mesaj.lower() or "instabil" in mesaj.lower()


@pytest.mark.skipif(not IMPORT_PING_OK, reason="Modulul ping nu a putut fi importat")
class TestInterpretarePierdere:
    """Teste pentru funcția interpreteaza_pierdere."""
    
    def test_pierdere_zero(self) -> None:
        """Zero pierdere e excelentă."""
        culoare, mesaj = interpreteaza_pierdere(0.0)
        assert "Excelent" in mesaj
    
    def test_pierdere_mare(self) -> None:
        """Pierdere mare e problematică."""
        culoare, mesaj = interpreteaza_pierdere(15.0)
        assert "Problem" in mesaj


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_SOCKET_BASIC
# ═══════════════════════════════════════════════════════════════════════════════

class TestSocketBasic:
    """Teste de bază pentru operații socket."""
    
    def test_socket_tcp_creation(self) -> None:
        """Crearea unui socket TCP funcționează."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            assert sock.fileno() >= 0
        finally:
            sock.close()
    
    def test_socket_udp_creation(self) -> None:
        """Crearea unui socket UDP funcționează."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            assert sock.fileno() >= 0
        finally:
            sock.close()
    
    def test_socket_bind_localhost(self) -> None:
        """Bind pe localhost funcționează."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Port 0 = kernel alege un port liber
            sock.bind(('127.0.0.1', 0))
            addr = sock.getsockname()
            assert addr[0] == '127.0.0.1'
            assert addr[1] > 0
        finally:
            sock.close()
    
    def test_socket_listen(self) -> None:
        """Listen pe un socket bound funcționează."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('127.0.0.1', 0))
            sock.listen(1)
            # Dacă am ajuns aici fără excepție, e OK
        finally:
            sock.close()


# ═══════════════════════════════════════════════════════════════════════════════
# TESTE_INTEGRARE
# ═══════════════════════════════════════════════════════════════════════════════

class TestIntegrare:
    """Teste de integrare — verifică că componentele funcționează împreună."""
    
    @pytest.mark.slow
    def test_ping_si_interpretare(self) -> None:
        """Execută ping și interpretează rezultatul."""
        if not IMPORT_PING_OK:
            pytest.skip("Modulul ping nu a putut fi importat")
        
        rezultat = executa_ping("127.0.0.1", numar_pachete=2)
        
        # Verifică că avem date
        assert rezultat.pachete_trimise > 0
        
        # Dacă avem RTT, verifică interpretarea
        if rezultat.rtt_avg > 0:
            culoare, mesaj = interpreteaza_latenta(rezultat.rtt_avg)
            assert len(mesaj) > 0
    
    def test_comenzi_disponibile(self) -> None:
        """Verifică că comenzile de bază sunt disponibile."""
        comenzi = [
            (["ip", "--version"], "iproute2"),
            (["ping", "-V"], "ping"),  # ping nu are --version
        ]
        
        for cmd, nume in comenzi:
            try:
                result = subprocess.run(
                    cmd, 
                    capture_output=True, 
                    text=True, 
                    timeout=5
                )
                # Unele comenzi returnează 0, altele non-zero pentru --version
                # Important e că nu au dat FileNotFoundError
            except FileNotFoundError:
                pytest.skip(f"Comanda '{nume}' nu e disponibilă")
            except subprocess.TimeoutExpired:
                pytest.skip(f"Comanda '{nume}' a expirat")


# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURARE_PYTEST
# ═══════════════════════════════════════════════════════════════════════════════

def pytest_configure(config):
    """Configurare pytest — adaugă markeri custom."""
    config.addinivalue_line(
        "markers", "slow: marchează testele care durează mult"
    )


if __name__ == "__main__":
    # Rulare directă pentru debugging
    pytest.main([__file__, "-v", "--tb=short"])
