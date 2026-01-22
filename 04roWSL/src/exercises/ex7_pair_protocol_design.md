# Exercițiu 7: Design Protocol în Perechi (Pair Programming)

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

---

## Obiectiv

Proiectați și implementați un protocol simplu de chat în perechi, aplicând conceptele învățate despre structura mesajelor, CRC și încadrare.

**Timp alocat:** 45 minute  
**Punctaj:** 20 puncte  
**Mod de lucru:** Perechi (Driver + Navigator)

---

## Roluri Pair Programming

**Driver:** Scrie codul, tastează, controlează editorul.

**Navigator:** Revizuiește în timp real, gândește strategic, identifică erori.

Schimbați rolurile la fiecare rundă (15 minute).

---

## Cerințe Protocol

Proiectați un protocol de chat cu următoarele caracteristici:

### Specificații

| Cerință | Detaliu |
|---------|---------|
| Transport | TCP |
| Mesaj maxim | 256 caractere |
| Username | Maxim 16 caractere |
| Verificare | CRC32 |
| Byte order | Network (big-endian) |

### Funcționalități Obligatorii

1. Trimitere mesaj text cu username
2. Primire și afișare mesaj cu username
3. Detectarea mesajelor corupte (CRC invalid)

---

## Runda 1: Design Antet (15 minute)

**Sarcină:** Proiectați structura antetului protocolului.

### Câmpuri Necesare

Decideți împreună ce câmpuri includeți în antet. Considerați:

- Cum identifici începutul unui mesaj? (magic number)
- Cum știi lungimea mesajului? (length prefix)
- Cum identifici expeditorul? (username)
- Cum verifici integritatea? (CRC)

### Template de Completat

```
Structura Antet Propusă:
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Câmp 1    │   Câmp 2    │   Câmp 3    │   Câmp 4    │   Câmp 5    │
│   __ bytes  │   __ bytes  │   __ bytes  │   __ bytes  │   __ bytes  │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘

Dimensiune totală antet: ___ bytes

Format struct.pack: '!_______________'

Note de design:
- De ce ați ales această ordine a câmpurilor?
- Ce compromisuri ați făcut?
```

### Livrabil Runda 1

Desenați structura pe hârtie sau într-un document. Explicați alegerea fiecărui câmp.

---

## Runda 2: Funcție Împachetare (15 minute)

**Schimbați rolurile!** Cine a fost Navigator devine Driver.

**Sarcină:** Implementați funcția de împachetare a mesajelor.

### Template Cod

```python
#!/usr/bin/env python3
"""
Protocol Chat - Funcții de împachetare/despachetare
Echipa: [Nume1] + [Nume2]
"""

import struct
import binascii
from typing import Tuple

# Constante protocol (completați conform designului vostru)
MAGIC = b'??'  # 2 bytes
VERSIUNE = 1
MAX_USERNAME = 16
MAX_MESAJ = 256


def impacheteaza_mesaj(username: str, text: str) -> bytes:
    """
    Împachetează un mesaj de chat.
    
    Args:
        username: Numele expeditorului (max 16 caractere)
        text: Textul mesajului (max 256 caractere)
    
    Returns:
        Mesajul împachetat ca bytes
    
    Raises:
        ValueError: Dacă username sau text depășesc limitele
    
    ---
    PREDICȚIE înainte de implementare:
    1. Câți bytes va avea un mesaj cu username "Ana" și text "Salut"?
    2. Ce faci dacă username are mai puțin de 16 caractere?
    3. CRC se calculează peste ce date exact?
    ---
    """
    # TODO: Implementați conform designului din Runda 1
    # 
    # Pași sugerați:
    # 1. Validare input (lungimi)
    # 2. Pregătire username (padding la 16 bytes)
    # 3. Codificare text
    # 4. Construire antet parțial (fără CRC)
    # 5. Calculare CRC
    # 6. Asamblare mesaj final
    pass


# Test rapid
if __name__ == "__main__":
    mesaj = impacheteaza_mesaj("Ana", "Salut!")
    print(f"Lungime: {len(mesaj)} bytes")
    print(f"Hex: {mesaj.hex()}")
```

### Criterii de Verificare

- [ ] Funcția acceptă username și text
- [ ] Validează lungimile maxime
- [ ] Username e padding-uit corect
- [ ] CRC e calculat și inclus
- [ ] Returnează bytes

---

## Runda 3: Funcție Despachetare (15 minute)

**Schimbați rolurile din nou!**

**Sarcină:** Implementați funcția de despachetare și verificare.

### Template Cod

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class MesajChat:
    """Mesaj de chat parsat."""
    username: str
    text: str
    crc_valid: bool


def despacheteaza_mesaj(date: bytes) -> Optional[MesajChat]:
    """
    Despachetează un mesaj de chat.
    
    Args:
        date: Mesajul brut
    
    Returns:
        MesajChat parsat sau None dacă invalid
    
    ---
    PREDICȚIE:
    1. Ce verifici primul: magic sau lungime?
    2. Cum extragi username-ul fără trailing nulls?
    3. Ce returnezi dacă CRC e invalid?
    ---
    """
    # TODO: Implementați inversul funcției impacheteaza_mesaj
    #
    # Pași sugerați:
    # 1. Verificare lungime minimă
    # 2. Verificare magic
    # 3. Extragere câmpuri din antet
    # 4. Extragere username (eliminare padding)
    # 5. Extragere text
    # 6. Verificare CRC
    # 7. Returnare MesajChat
    pass


# Test round-trip
if __name__ == "__main__":
    # Test 1: Mesaj valid
    original = impacheteaza_mesaj("Bob", "Test mesaj")
    parsat = despacheteaza_mesaj(original)
    
    if parsat:
        print(f"Username: {parsat.username}")
        print(f"Text: {parsat.text}")
        print(f"CRC valid: {parsat.crc_valid}")
    
    # Test 2: Mesaj corupt
    corupt = bytearray(original)
    corupt[10] ^= 0xFF  # Flip un byte
    parsat_corupt = despacheteaza_mesaj(bytes(corupt))
    
    if parsat_corupt:
        print(f"\nMesaj corupt - CRC valid: {parsat_corupt.crc_valid}")
```

---

## Verificare Finală (Test Încrucișat)

După ce ambele perechi au terminat, faceți schimb de cod:

1. Perechea A trimite un mesaj împachetat perechii B
2. Perechea B încearcă să-l despacheteze
3. Dacă funcționează, protocoalele sunt compatibile!

### Script de Test

```python
# Copiați și rulați acest test cu implementările voastre

def test_compatibilitate():
    """Test compatibilitate între implementări."""
    # Mesaje de test
    teste = [
        ("Alice", "Hello!"),
        ("Bob", "Salut, cum ești?"),
        ("X" * 16, "A" * 256),  # Maxime
        ("Jo", "Hi"),  # Minime
    ]
    
    for username, text in teste:
        try:
            pachet = impacheteaza_mesaj(username, text)
            rezultat = despacheteaza_mesaj(pachet)
            
            assert rezultat is not None, "Despachetare a returnat None"
            assert rezultat.crc_valid, "CRC invalid"
            assert rezultat.username == username[:MAX_USERNAME], f"Username: {rezultat.username}"
            assert rezultat.text == text[:MAX_MESAJ], f"Text: {rezultat.text}"
            
            print(f"✓ Test passed: {username[:8]}... -> {text[:20]}...")
        except Exception as e:
            print(f"✗ Test failed: {username} -> {text}: {e}")


if __name__ == "__main__":
    test_compatibilitate()
```

---

## Predare

### Fișiere de Încărcat

1. `protocol_chat.py` — Codul complet cu ambele funcții
2. `design_protocol.pdf` — Schema antetului cu explicații
3. (Opțional) Captură Wireshark dacă ați testat real

### Criterii de Evaluare

| Criteriu | Puncte |
|----------|--------|
| Design antet clar și documentat | 5 |
| Funcție împachetare corectă | 5 |
| Funcție despachetare corectă | 5 |
| Test round-trip funcționează | 3 |
| Cod curat, comentarii | 2 |
| **Total** | **20** |

---

## Reflecție (Completați Individual)

După exercițiu, răspundeți:

1. Ce a fost mai dificil: designul sau implementarea?
2. Ce ați face diferit data viitoare la structura antetului?
3. Cum v-a ajutat pair programming?
4. Ce ați învățat de la partener?

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
