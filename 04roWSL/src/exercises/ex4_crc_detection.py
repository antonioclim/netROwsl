#!/usr/bin/env python3
"""
Exercițiu 4: Detectarea Erorilor cu CRC32
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

OBIECTIV:
    Experimentați cu detectarea erorilor folosind CRC32 și
    înțelegeți limitările acestei tehnici.

ÎNAINTE DE A ÎNCEPE — Răspunde mental:
======================================
1. CRC32("123456789") = 0x_________ (hint: e o valoare standard de verificare)
2. Dacă inversezi UN SINGUR BIT din date, CRC-ul se schimbă? DA / NU
3. CRC poate CORECTA erori sau doar le DETECTEAZĂ?
4. CRC32 oferă protecție împotriva modificărilor INTENȚIONATE? DA / NU (și de ce?)

Notează răspunsurile și verifică-le după ce termini exercițiul.

INSTRUCȚIUNI:
    1. Rulați experimentele pentru a înțelege CRC32
    2. Observați ce tipuri de erori detectează
    3. Înțelegeți diferența față de hash-uri criptografice

TEORIE CRC:
    - CRC = Cyclic Redundancy Check
    - Detectează 100% din erorile de 1-2 biți
    - Detectează 100% din erorile de rafală până la 32 biți
    - NU oferă securitate (nu e hash criptografic!)

PUNCTAJ: 10 puncte
"""

import binascii
import random
from typing import List, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# FUNCȚII_CRC
# Scop: Experimentare cu calculul și verificarea CRC32
# ═══════════════════════════════════════════════════════════════════════════════

def calculeaza_crc32(date: bytes) -> int:
    """Calculează CRC32 pentru date."""
    return binascii.crc32(date) & 0xFFFFFFFF


def verifica_valoare_cunoscuta() -> bool:
    """
    Verifică CRC32 cu valoarea standard de test.
    
    "123456789" este string-ul standard de verificare pentru CRC32.
    Rezultatul trebuie să fie 0xCBF43926.
    """
    date = b"123456789"
    crc = calculeaza_crc32(date)
    asteptat = 0xCBF43926
    
    print("Experiment 1: Verificare valoare standard")
    print("-" * 50)
    print(f"  Date: {date}")
    print(f"  CRC32 calculat: 0x{crc:08X}")
    print(f"  CRC32 așteptat: 0x{asteptat:08X}")
    
    if crc == asteptat:
        print("  ✓ CORECT!")
        return True
    else:
        print("  ✗ INCORECT!")
        return False


# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENTE_DETECTARE
# Scop: Demonstrează capacitățile de detectare a erorilor
# ═══════════════════════════════════════════════════════════════════════════════

def experiment_eroare_1_bit():
    """
    Experimentează detectarea erorilor de un singur bit.
    
    PREDICȚIE: CRC32 va detecta TOATE erorile de 1 bit? DA / NU
    """
    print("\nExperiment 2: Erori de un singur bit")
    print("-" * 50)
    
    date_originale = b"Mesaj de test pentru CRC32"
    crc_original = calculeaza_crc32(date_originale)
    
    print(f"  Date originale: {date_originale}")
    print(f"  CRC original: 0x{crc_original:08X}")
    print()
    
    # Testează inversarea fiecărui bit
    erori_detectate = 0
    erori_nedetectate = 0
    
    # Convertim la bytearray pentru modificare
    for byte_idx in range(len(date_originale)):
        for bit_idx in range(8):
            # Copiază și modifică
            date_modificate = bytearray(date_originale)
            date_modificate[byte_idx] ^= (1 << bit_idx)
            date_modificate = bytes(date_modificate)
            
            # Calculează CRC nou
            crc_nou = calculeaza_crc32(date_modificate)
            
            if crc_nou != crc_original:
                erori_detectate += 1
            else:
                erori_nedetectate += 1
                print(f"  ⚠ Eroare NEDETECTATĂ la byte {byte_idx}, bit {bit_idx}!")
    
    total_teste = len(date_originale) * 8
    print(f"  Rezultat: {erori_detectate}/{total_teste} erori detectate")
    
    if erori_nedetectate == 0:
        print("  ✓ TOATE erorile de 1 bit detectate!")
    else:
        print(f"  ✗ {erori_nedetectate} erori nedetectate!")


def experiment_eroare_2_biti():
    """
    Experimentează detectarea erorilor de doi biți.
    
    PREDICȚIE: CRC32 va detecta TOATE erorile de 2 biți? DA / NU
    """
    print("\nExperiment 3: Erori de doi biți (eșantion)")
    print("-" * 50)
    
    date_originale = b"Test CRC"
    crc_original = calculeaza_crc32(date_originale)
    
    print(f"  Date originale: {date_originale}")
    print(f"  CRC original: 0x{crc_original:08X}")
    print()
    
    # Testează un eșantion de erori de 2 biți (testarea completă ar dura prea mult)
    erori_detectate = 0
    erori_nedetectate = 0
    teste_rulate = 0
    
    for i in range(min(100, len(date_originale) * 8)):
        for j in range(i + 1, min(100, len(date_originale) * 8)):
            date_modificate = bytearray(date_originale)
            
            byte_i, bit_i = divmod(i, 8)
            byte_j, bit_j = divmod(j, 8)
            
            if byte_i < len(date_modificate) and byte_j < len(date_modificate):
                date_modificate[byte_i] ^= (1 << bit_i)
                date_modificate[byte_j] ^= (1 << bit_j)
                
                crc_nou = calculeaza_crc32(bytes(date_modificate))
                teste_rulate += 1
                
                if crc_nou != crc_original:
                    erori_detectate += 1
                else:
                    erori_nedetectate += 1
    
    print(f"  Teste rulate: {teste_rulate}")
    print(f"  Rezultat: {erori_detectate}/{teste_rulate} erori detectate")
    
    if erori_nedetectate == 0:
        print("  ✓ Toate erorile de 2 biți testate au fost detectate!")


def experiment_eroare_rafala():
    """
    Experimentează detectarea erorilor de rafală (burst errors).
    
    PREDICȚIE: Cât de lungă poate fi o rafală pentru a fi detectată 100%?
    """
    print("\nExperiment 4: Erori de rafală")
    print("-" * 50)
    
    date_originale = b"Date pentru test rafala de erori CRC32"
    crc_original = calculeaza_crc32(date_originale)
    
    print(f"  Date originale: {date_originale}")
    print(f"  CRC original: 0x{crc_original:08X}")
    print()
    
    # Testează rafale de diferite lungimi
    for lungime_rafala in [8, 16, 24, 32, 40, 48]:
        erori_detectate = 0
        teste = 100  # Teste aleatorii pentru fiecare lungime
        
        for _ in range(teste):
            date_modificate = bytearray(date_originale)
            
            # Generează o rafală de erori
            start_bit = random.randint(0, len(date_modificate) * 8 - lungime_rafala)
            
            for bit in range(lungime_rafala):
                bit_pozitie = start_bit + bit
                byte_idx, bit_idx = divmod(bit_pozitie, 8)
                if byte_idx < len(date_modificate):
                    date_modificate[byte_idx] ^= (1 << bit_idx)
            
            crc_nou = calculeaza_crc32(bytes(date_modificate))
            
            if crc_nou != crc_original:
                erori_detectate += 1
        
        procent = erori_detectate / teste * 100
        print(f"  Rafală {lungime_rafala:2d} biți: {procent:.1f}% detectate ({erori_detectate}/{teste})")


def experiment_securitate():
    """
    Demonstrează de ce CRC32 NU oferă securitate.
    
    PREDICȚIE: Poți modifica datele păstrând CRC-ul valid? DA / NU
    """
    print("\nExperiment 5: CRC32 vs Securitate")
    print("-" * 50)
    
    date_originale = b"Suma: 100 lei"
    crc_original = calculeaza_crc32(date_originale)
    
    print(f"  Date originale: {date_originale}")
    print(f"  CRC original: 0x{crc_original:08X}")
    print()
    
    # Demonstrează că CRC nu e sigur - putem găsi coliziuni
    print("  CRC32 NU oferă securitate deoarece:")
    print("  1. Nu e rezistent la coliziuni (intenționat)")
    print("  2. Algoritmul e public și reversibil")
    print("  3. Un atacator poate modifica datele și recalcula CRC")
    print()
    
    # Exemplu: modificăm suma și recalculăm CRC
    date_modificate = b"Suma: 999 lei"
    crc_nou = calculeaza_crc32(date_modificate)
    
    print(f"  Date modificate: {date_modificate}")
    print(f"  CRC nou: 0x{crc_nou:08X}")
    print()
    print("  ⚠ Un atacator poate:")
    print("    1. Modifica datele cum dorește")
    print("    2. Recalcula CRC-ul pentru datele noi")
    print("    3. Trimite datele modificate cu CRC valid")
    print()
    print("  Pentru securitate, folosiți:")
    print("    - HMAC (Hash-based Message Authentication Code)")
    print("    - Semnături digitale (RSA, ECDSA)")
    print("    - Hash-uri criptografice (SHA-256) + secret partajat")


def experiment_determinism():
    """
    Verifică că CRC32 e determinist.
    
    PREDICȚIE: Același input produce ÎNTOTDEAUNA același output? DA / NU
    """
    print("\nExperiment 6: Determinism CRC32")
    print("-" * 50)
    
    date = b"Test determinism"
    
    # Calculează de 1000 de ori
    rezultate = set()
    for _ in range(1000):
        crc = calculeaza_crc32(date)
        rezultate.add(crc)
    
    print(f"  Date: {date}")
    print(f"  Calcule: 1000")
    print(f"  Rezultate distincte: {len(rezultate)}")
    
    if len(rezultate) == 1:
        print(f"  ✓ CRC32 e determinist: 0x{list(rezultate)[0]:08X}")
    else:
        print("  ✗ EROARE: CRC32 nu e determinist?!")


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRAM_PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Rulează toate experimentele CRC32."""
    print("=" * 60)
    print("Detectarea Erorilor cu CRC32")
    print("=" * 60)
    
    # Experiment 1: Verificare valoare standard
    verifica_valoare_cunoscuta()
    
    # Experiment 2: Erori de 1 bit
    experiment_eroare_1_bit()
    
    # Experiment 3: Erori de 2 biți
    experiment_eroare_2_biti()
    
    # Experiment 4: Erori de rafală
    experiment_eroare_rafala()
    
    # Experiment 5: Securitate
    experiment_securitate()
    
    # Experiment 6: Determinism
    experiment_determinism()
    
    print("\n" + "=" * 60)
    print("Experimente complete!")
    print("=" * 60)
    
    # Verificare răspunsuri predicție
    print("\n" + "-" * 60)
    print("VERIFICARE PREDICȚII:")
    print("-" * 60)
    print("1. CRC32('123456789') = 0xCBF43926")
    print("2. DA, inversarea unui bit schimbă CRC-ul (100% detectare)")
    print("3. CRC doar DETECTEAZĂ erori, NU le corectează")
    print("4. NU, CRC nu oferă securitate (atacatorul poate recalcula)")
    
    print("\n" + "-" * 60)
    print("CONCLUZII:")
    print("-" * 60)
    print("• CRC32 e EXCELENT pentru detectarea erorilor ACCIDENTALE")
    print("• CRC32 e INUTIL pentru securitate (modificări intenționate)")
    print("• Pentru securitate: HMAC, semnături digitale, hash+secret")


if __name__ == "__main__":
    main()
