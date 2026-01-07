#!/usr/bin/env python3
"""
Test Rapid (Smoke Test)
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

Verificare rapidă a funcționalității de bază (< 60 secunde).
"""

import subprocess
import sys
import struct
import zlib
from pathlib import Path

# Adaugă directorul rădăcină la cale
RADACINA_PROIECT = Path(__file__).parent.parent
sys.path.insert(0, str(RADACINA_PROIECT))


class TestareRapida:
    """Executor pentru teste rapide."""
    
    def __init__(self):
        self.reușite = 0
        self.eșuate = 0
    
    def test(self, nume: str, conditie: bool, mesaj_eroare: str = "") -> bool:
        """Rulează un test și raportează rezultatul."""
        if conditie:
            print(f"  \033[92m✓\033[0m {nume}")
            self.reușite += 1
            return True
        else:
            print(f"  \033[91m✗\033[0m {nume}")
            if mesaj_eroare:
                print(f"      {mesaj_eroare}")
            self.eșuate += 1
            return False
    
    def sumar(self) -> bool:
        """Afișează sumarul și returnează True dacă toate testele au trecut."""
        print()
        print(f"Rezultate: {self.reușite} reușite, {self.eșuate} eșuate")
        return self.eșuate == 0


def verifica_docker() -> bool:
    """Verifică disponibilitatea Docker."""
    try:
        rezultat = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            timeout=5
        )
        return rezultat.returncode == 0
    except Exception:
        return False


def verifica_sintaxa_python() -> tuple:
    """Verifică sintaxa tuturor fișierelor Python."""
    fisiere_ok = 0
    fisiere_eroare = []
    
    for fisier in RADACINA_PROIECT.rglob("*.py"):
        try:
            with open(fisier, 'r', encoding='utf-8') as f:
                compile(f.read(), fisier, 'exec')
            fisiere_ok += 1
        except SyntaxError as e:
            fisiere_eroare.append(f"{fisier.name}: {e}")
    
    return fisiere_ok, fisiere_eroare


def verifica_compose() -> bool:
    """Verifică validitatea docker-compose.yml."""
    fisier_compose = RADACINA_PROIECT / "docker" / "docker-compose.yml"
    
    if not fisier_compose.exists():
        return False
    
    try:
        # Încearcă parsarea YAML
        import yaml
        with open(fisier_compose, 'r', encoding='utf-8') as f:
            yaml.safe_load(f)
        return True
    except ImportError:
        # Dacă yaml nu e disponibil, verifică doar existența
        return True
    except Exception:
        return False


def test_endianness_demo() -> bool:
    """Testează rapid funcționalitatea endianness."""
    try:
        valoare = 0x12345678
        big = struct.pack(">I", valoare)
        little = struct.pack("<I", valoare)
        
        # Verifică că sunt diferite
        if big == little:
            return False
        
        # Verifică ordinea octeților
        if big != b'\x12\x34\x56\x78':
            return False
        
        return True
    except Exception:
        return False


def test_crc() -> bool:
    """Testează rapid funcționalitatea CRC-32."""
    try:
        date = b"Date de test"
        crc1 = zlib.crc32(date) & 0xFFFFFFFF
        crc2 = zlib.crc32(date) & 0xFFFFFFFF
        
        # CRC trebuie să fie deterministic
        return crc1 == crc2 and isinstance(crc1, int)
    except Exception:
        return False


def main():
    """Funcția principală."""
    print("=" * 50)
    print("Test Rapid - Săptămâna 9")
    print("Verificare funcționalitate de bază")
    print("=" * 50)
    print()
    
    t = TestareRapida()
    
    # Verificări de bază Python
    print("Verificări Python:")
    t.test("Versiune Python >= 3.8", sys.version_info >= (3, 8))
    t.test("Modul struct disponibil", struct is not None)
    t.test("Modul zlib disponibil", zlib is not None)
    
    # Verificare sintaxă
    print("\nVerificare Sintaxă:")
    fisiere_ok, erori = verifica_sintaxa_python()
    t.test(
        f"Sintaxă Python validă ({fisiere_ok} fișiere)",
        len(erori) == 0,
        "; ".join(erori[:3]) if erori else ""
    )
    
    # Verificări Docker
    print("\nVerificări Docker:")
    t.test("Docker disponibil", verifica_docker())
    t.test("docker-compose.yml valid", verifica_compose())
    
    # Verificări funcționale
    print("\nVerificări Funcționale:")
    t.test("Demo endianness funcționează", test_endianness_demo())
    t.test("CRC-32 funcționează", test_crc())
    
    # Verificare structură
    print("\nStructura Proiectului:")
    t.test(
        "Director docker/ există",
        (RADACINA_PROIECT / "docker").exists()
    )
    t.test(
        "Director scripts/ există",
        (RADACINA_PROIECT / "scripts").exists()
    )
    t.test(
        "Director src/exercises/ există",
        (RADACINA_PROIECT / "src" / "exercises").exists()
    )
    
    # Sumar
    print()
    print("=" * 50)
    succes = t.sumar()
    
    if succes:
        print("\033[92mToate testele au trecut! Mediul este pregătit.\033[0m")
    else:
        print("\033[91mUnele teste au eșuat. Verificați problemele de mai sus.\033[0m")
    
    print("=" * 50)
    
    return 0 if succes else 1


if __name__ == "__main__":
    sys.exit(main())
