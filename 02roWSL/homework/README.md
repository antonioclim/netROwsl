# Teme pentru Acasă - Săptămâna 2

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Prezentare Generală

Această săptămână aveți de completat **două exerciții** care vă vor ajuta să consolidați cunoștințele despre programarea socket-urilor TCP și UDP.

## Cerințe Generale

- **Termen limită:** Conform indicațiilor profesorului
- **Formatul predării:** Fișierele Python completate + un scurt README cu explicații
- **Denumire:** `Nume_Prenume_HW2.zip`

## Exerciții

### Tema 2.01: Server TCP cu Autentificare

**Fișier:** `exercises/hw_2_01.py`

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

**Punctaj:** 50 puncte

---

### Tema 2.02: Client UDP Robust cu Retry

**Fișier:** `exercises/hw_2_02.py`

**Cerință:**
Implementați un client UDP care gestionează pierderea pachetelor prin retry automat.

**Specificații:**
1. Dacă nu primește răspuns în 2 secunde, clientul retrimite cererea
2. Maximum 3 încercări înainte de a raporta eșec
3. Afișați statistici: încercări necesare, timp total
4. Implementați un mod de test care simulează pierdere de pachete

**Interfață:**
```python
class ClientUDPRobust:
    def __init__(self, host: str, port: int, timeout: float = 2.0, max_retry: int = 3):
        ...
    
    def trimite_cu_retry(self, mesaj: str) -> Tuple[Optional[str], int]:
        """
        Trimite mesaj cu retry automat.
        
        Returns:
            Tuple de (răspuns sau None, număr de încercări)
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

**Punctaj:** 50 puncte

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

## Resurse Utile

- Codul din laborator (`src/exercises/`)
- Documentația Python pentru modulul `socket`
- Prezentarea teoretică din `docs/theory_summary.md`

## Întrebări Frecvente

**Î: Pot folosi biblioteci externe?**
R: Da, atât timp cât sunt în biblioteca standard Python. Evitați dependențe externe.

**Î: Cum testez codul?**
R: Folosiți scripturile din laborator ca referință. Porniți serverul și testați cu clientul.

**Î: Unde pun soluțiile?**
R: Completați fișierele din `exercises/` și păstrați structura existentă.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
