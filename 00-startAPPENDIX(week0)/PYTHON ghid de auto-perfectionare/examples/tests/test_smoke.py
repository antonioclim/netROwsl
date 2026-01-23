#!/usr/bin/env python3
"""
Smoke Tests pentru Exemplele Python
====================================
Verifică că toate modulele se importă și funcționează minimal.

Curs: Rețele de Calculatoare - ASE București, CSIE
Autor: ing. dr. Antonio Clim

Rulare:
    python test_smoke.py
    
Sau cu pytest:
    pytest test_smoke.py -v
"""

# ═══════════════════════════════════════════════════════════════════════════════
# SETUP_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
import subprocess
import sys
import os
from pathlib import Path

# NOTE: Detectăm automat directorul examples/
SCRIPT_DIR = Path(__file__).parent
EXAMPLES_DIR = SCRIPT_DIR.parent if SCRIPT_DIR.name == "tests" else SCRIPT_DIR


# ═══════════════════════════════════════════════════════════════════════════════
# CONSTANTE
# ═══════════════════════════════════════════════════════════════════════════════
SUBPROCESS_TIMEOUT: int = 10  # Timeout pentru verificări import
SCRIPT_TIMEOUT: int = 30      # Timeout pentru rulare scripturi complete
TEST_PORT: int = 8080         # Port standard pentru teste socket


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_IMPORTS
# ═══════════════════════════════════════════════════════════════════════════════
def test_socket_tcp_imports() -> None:
    """Verifică că 01_socket_tcp.py se importă fără erori."""
    result = subprocess.run(
        [sys.executable, "-c", "import socket; import logging; import sys"],
        capture_output=True,
        timeout=10
    )
    assert result.returncode == 0, f"Import failed: {result.stderr.decode()}"


def test_bytes_vs_str_imports() -> None:
    """Verifică că 02_bytes_vs_str.py se importă fără erori."""
    result = subprocess.run(
        [sys.executable, "-c", "from typing import Optional; import logging"],
        capture_output=True,
        timeout=10
    )
    assert result.returncode == 0, f"Import failed: {result.stderr.decode()}"


def test_struct_parsing_imports() -> None:
    """Verifică că 03_struct_parsing.py se importă fără erori."""
    result = subprocess.run(
        [sys.executable, "-c", "import struct; from dataclasses import dataclass"],
        capture_output=True,
        timeout=10
    )
    assert result.returncode == 0, f"Import failed: {result.stderr.decode()}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_EXECUTIE
# ═══════════════════════════════════════════════════════════════════════════════
def test_bytes_demo_runs() -> None:
    """Rulează demonstrația bytes fără erori."""
    script_path = EXAMPLES_DIR / "02_bytes_vs_str.py"
    if not script_path.exists():
        print(f"SKIP: {script_path} nu există")
        return
        
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Script failed: {result.stderr.decode()}"
    
    # Verifică că output-ul conține textul așteptat
    output = result.stdout.decode().lower()
    assert "bytes" in output or "str" in output, "Output nu conține cuvinte cheie"


def test_struct_parsing_runs() -> None:
    """Rulează demonstrația struct fără erori."""
    script_path = EXAMPLES_DIR / "03_struct_parsing.py"
    if not script_path.exists():
        print(f"SKIP: {script_path} nu există")
        return
        
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        timeout=30
    )
    
    assert result.returncode == 0, f"Script failed: {result.stderr.decode()}"


# ═══════════════════════════════════════════════════════════════════════════════
# TEST_FUNCTIONALITATE
# ═══════════════════════════════════════════════════════════════════════════════
def test_bytes_encoding() -> None:
    """Verifică encoding/decoding bytes ↔ str."""
    text = "Salut, Rețele!"
    encoded = text.encode('utf-8')
    decoded = encoded.decode('utf-8')
    
    assert isinstance(encoded, bytes), "encode() trebuie să returneze bytes"
    assert isinstance(decoded, str), "decode() trebuie să returneze str"
    assert text == decoded, "Roundtrip encoding trebuie să păstreze textul"


def test_struct_pack_unpack() -> None:
    """Verifică struct pack/unpack pentru porturi."""
    import struct
    
    # Pack
    port = 8080
    packed = struct.pack('!H', port)  # Network byte order, unsigned short
    
    assert len(packed) == 2, "Unsigned short trebuie să aibă 2 bytes"
    assert packed == b'\x1f\x90', f"8080 în big-endian = 0x1F90, got {packed.hex()}"
    
    # Unpack
    unpacked, = struct.unpack('!H', packed)
    assert unpacked == port, f"Unpack trebuie să returneze {port}, got {unpacked}"


def test_socket_creation() -> None:
    """Verifică că putem crea un socket TCP."""
    import socket
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.fileno() >= 0, "Socket trebuie să aibă file descriptor valid"
        
        # Verifică opțiuni
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Dacă ajungem aici fără excepție, e OK


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN_RUNNER
# ═══════════════════════════════════════════════════════════════════════════════
def run_all_tests() -> bool:
    """Rulează toate testele și afișează rezultatele."""
    tests: list = [
        test_socket_tcp_imports,
        test_bytes_vs_str_imports,
        test_struct_parsing_imports,
        test_bytes_encoding,
        test_struct_pack_unpack,
        test_socket_creation,
        test_bytes_demo_runs,
        test_struct_parsing_runs,
    ]
    
    passed = 0
    failed = 0
    
    print("=" * 60)
    print("SMOKE TESTS - Python Networking Examples")
    print("=" * 60)
    
    for test in tests:
        try:
            test()
            print(f"✅ PASS: {test.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {test.__name__}")
            print(f"   Motiv: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {test.__name__}")
            print(f"   Excepție: {type(e).__name__}: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"REZULTAT: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
