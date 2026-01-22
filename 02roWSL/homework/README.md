# Teme pentru Acasă - Săptămâna 2

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Prezentare Generală

Această săptămână aveți de completat **trei exerciții** care vă vor ajuta să consolidați cunoștințele despre programarea socket-urilor TCP și UDP, precum și despre proiectarea protocoalelor binare.

## Cerințe Generale

- **Termen limită:** Conform indicațiilor profesorului
- **Formatul predării:** Fișierele Python completate + un scurt README cu explicații
- **Denumire:** `Nume_Prenume_HW2.zip`

## Exerciții

### Tema 2.01: Server TCP cu Autentificare

**Fișier:** `exercises/hw_2_01.py`  
**Nivel:** Intermediar (Bloom: APPLY)  
**Punctaj:** 35 puncte

**Cerință:**
Extindeți serverul TCP din laborator pentru a implementa un sistem de autentificare simplu.

**Specificații:**
1. La conectare, serverul cere utilizatorului să se autentifice
2. Formatul comenzii de autentificare: `LOGIN:utilizator:parolă`
3. Utilizatori valizi (hardcoded): `admin:admin123`, `student:parola`
4. După autentificare reușită, serverul procesează comenzile normal
5. Fără autentificare, singura comandă acceptată este `LOGIN`
6. După 3 încercări eșuate, conexiunea este închisă

**Exemple de interacțiune:**
```
Client: upper:test
Server: EROARE: Trebuie să vă autentificați. Folosiți LOGIN:user:pass

Client: LOGIN:admin:gresit
Server: EROARE: Credențiale invalide. Încercări rămase: 2

Client: LOGIN:admin:admin123
Server: OK: Autentificare reușită. Bine ați venit, admin!

Client: upper:test
Server: OK: TEST
```

---

### Tema 2.02: Client UDP cu Retry Automat

**Fișier:** `exercises/hw_2_02.py`  
**Nivel:** Intermediar (Bloom: APPLY)  
**Punctaj:** 35 puncte

**Cerință:**
Implementați un client UDP care gestionează pierderea pachetelor prin retry automat.

**Specificații:**
1. Dacă nu primește răspuns în 2 secunde, clientul retrimite cererea
2. Maximum 3 încercări înainte de a raporta eșec
3. Afișați statistici: încercări necesare, timp total
4. Implementați un mod de test care simulează pierdere de pachete

**Interfață:**
```python
class ClientUDPRetryer:
    def __init__(self, host: str, port: int, timeout: float = 2.0, max_retry: int = 3):
        ...
    
    def trimite_cu_retry(self, mesaj: str) -> StatisticiTrimitere:
        """
        Trimite mesaj cu retry automat.
        
        Returns:
            StatisticiTrimitere cu rezultatul operațiunii
        """
        ...
```

**Exemple de output:**
```
Trimitere: ping
  Încercarea 1... timeout
  Încercarea 2... succes!
Răspuns: PONG (2 încercări, 2.15s total)

Trimitere: upper:test
  Încercarea 1... succes!
Răspuns: TEST (1 încercare, 0.05s total)
```

---

### Tema 2.03: Protocol Binar pentru Mesaje

**Fișier:** `exercises/hw_2_03.py`  
**Nivel:** Avansat (Bloom: CREATE)  
**Punctaj:** 30 puncte

**Cerință:**
Proiectați și implementați un protocol binar simplu pentru schimb de mesaje.

**Specificații Protocol:**

Header fix de 8 bytes:
- Bytes 0-1: Magic number (0xCAFE) — identifică protocolul
- Byte 2: Versiune protocol (0x01)
- Byte 3: Tip mesaj (0x01=TEXT, 0x02=PING, 0x03=PONG, 0xFF=ERROR)
- Bytes 4-5: Lungime payload (big-endian, max 65535)
- Bytes 6-7: Checksum XOR (peste payload)

```
┌─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┬─────────┐
│  0xCA   │  0xFE   │ Version │ MsgType │ Len Hi  │ Len Lo  │ Chk Hi  │ Chk Lo  │
├─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┴─────────┤
│                              Payload (variabil)                               │
└───────────────────────────────────────────────────────────────────────────────┘
```

**Funcții de implementat:**
```python
def calculeaza_checksum(payload: bytes) -> int:
    """Calculează checksum XOR pe 16 biți."""
    ...

def encode_message(tip: TipMesaj, payload: bytes = b"") -> bytes:
    """Codifică un mesaj în format binar."""
    ...

def decode_message(data: bytes) -> Tuple[TipMesaj, bytes]:
    """Decodifică un mesaj, validând integritatea."""
    ...
```

**Exemple:**
```python
>>> encoded = encode_message(TipMesaj.TEXT, b"Salut!")
>>> print(encoded.hex())
cafe0101000653616c757421xxxx  # xxxx = checksum

>>> tip, payload = decode_message(encoded)
>>> print(tip, payload)
TipMesaj.TEXT b'Salut!'
```

---

## Criterii de Evaluare

| Criteriu | Punctaj |
|----------|---------|
| Funcționalitate corectă | 60% |
| Calitatea codului (lizibilitate, comentarii) | 20% |
| Gestionarea erorilor | 15% |
| Documentație/README | 5% |

## Bonusuri (opțional)

- **+10 puncte:** Implementați logging în fișier pentru debugging
- **+10 puncte:** Adăugați teste unitare pentru funcționalitățile noi
- **+5 puncte:** Suportați configurare din variabile de mediu sau fișier
- **+5 puncte:** Pentru tema 2.03, implementați și un server/client funcțional care folosește protocolul

## Resurse Utile

- Codul din laborator (`src/exercises/`)
- Documentația Python pentru modulul `socket`
- Documentația Python pentru modulul `struct` (pentru tema 2.03)
- Prezentarea teoretică din `docs/theory_summary.md`

## Întrebări Frecvente

**Î: Pot folosi biblioteci externe?**
R: Da, atât timp cât sunt în biblioteca standard Python. Evitați dependențe externe.

**Î: Cum testez codul?**
R: Folosiți scripturile din laborator ca referință. Porniți serverul și testați cu clientul. Pentru tema 2.03, rulați `python hw_2_03.py test`.

**Î: Unde pun soluțiile?**
R: Completați fișierele din `exercises/` și păstrați structura existentă.

**Î: Care e diferența între temele 2.01/2.02 și 2.03?**
R: Primele două vă cer să extindeți cod existent (APPLY), ultima vă cere să proiectați de la zero (CREATE).

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
