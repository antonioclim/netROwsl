# Întrebări Peer Instruction: Săptămâna 4

> Curs REȚELE DE CALCULATOARE - ASE București
> 
> **DOAR PENTRU INSTRUCTOR — Nu distribuiți studenților!**

---

## Ghid de Utilizare

### Secvența Standard

1. Afișați întrebarea (1 min)
2. Vot individual FĂRĂ discuție (1 min)
3. Discuție în perechi (2-3 min)
4. Revot (30 sec)
5. Explicație și debrief (2 min)

### Ținte

- Răspunsuri corecte la primul vot: 30-70%
- Îmbunătățire după discuție: +20-30%
- Dacă >80% corect la primul vot → întrebarea e prea ușoară
- Dacă <20% corect → întrebarea e prea grea sau ambiguă

---

## PI-1: Network Byte Order

### Scenariu
```python
import struct
valoare = 0x12345678

pachet_a = struct.pack('I', valoare)    # Opțiunea A
pachet_b = struct.pack('!I', valoare)   # Opțiunea B  
pachet_c = struct.pack('<I', valoare)   # Opțiunea C
```

### Întrebare
Care pachet este corect pentru transmisie în rețea?

### Opțiuni
- **A)** pachet_a — folosește ordinea nativă a sistemului
- **B)** pachet_b — network byte order (big-endian) ✓
- **C)** pachet_c — little-endian explicit
- **D)** Toate sunt echivalente pentru comunicare

### Analiza Distractorilor

| Opțiune | Misconceptie |
|---------|--------------|
| A | "Sistemul meu e standard, va funcționa oriunde" |
| C | Confuzie: little-endian = network order |
| D | "Bytes sunt bytes, nu contează ordinea" |

### După Discuție

Desenați pe tablă:
```
0x12345678 în memorie:

Little-endian (x86, majoritatea PC-urilor):
Adresă:   0    1    2    3
Valoare: [78] [56] [34] [12]

Big-endian (network order):
Adresă:   0    1    2    3
Valoare: [12] [34] [56] [78]
```

### Întrebare Follow-up
"De ce s-a ales big-endian ca standard de rețea și nu little-endian?"

---

## PI-2: CRC vs Hash Criptografic

### Scenariu
Descarci un fișier ISO de pe internet și vrei să verifici integritatea.

### Întrebare
Ce metodă de verificare alegi?

### Opțiuni
- **A)** CRC32 — rapid și simplu
- **B)** MD5 — standard pentru fișiere
- **C)** SHA-256 — securitate maximă
- **D)** Depinde de modelul de amenințare ✓

### Analiza Distractorilor

| Opțiune | Când e de fapt corectă |
|---------|------------------------|
| A | Verificare corupere accidentală (descărcare întreruptă) |
| B | Deprecated pentru securitate, dar OK pentru corupere |
| C | Când suspectezi manipulare intenționată (mirror compromis) |

### După Discuție

Întrebări de clarificare:
- "Cine ar vrea să modifice intenționat un fișier ISO?"
- "Ce atacuri sunt posibile cu un ISO modificat?"
- "De ce site-urile oferă atât MD5/SHA cât și semnături GPG?"

### Concept Cheie
CRC detectează erori accidentale. Hash-urile criptografice detectează modificări intenționate. Pentru ISO-uri oficiale, semnăturile digitale sunt și mai sigure.

---

## PI-3: TCP vs UDP pentru IoT

### Scenariu
Ai 100 de senzori de temperatură pe baterie (durată viață așteptată: 2 ani), care trimit date la fiecare 5 secunde.

### Întrebare
Ce protocol de transport alegi?

### Opțiuni
- **A)** TCP — garantează livrarea datelor
- **B)** UDP — overhead mic, economisește bateria ✓
- **C)** TCP cu keepalive dezactivat
- **D)** HTTP/REST — standard industrial

### Analiza

| Factor | TCP | UDP |
|--------|-----|-----|
| Overhead/mesaj | ~40 bytes | ~8 bytes |
| Handshake inițial | 3-way (6 pachete min) | 0 |
| Stare menținută | Da (memorie, CPU) | Nu |
| Consum baterie | Mai mare | Mai mic |
| O citire pierdută | Retransmisă (delay) | OK, vine alta în 5s |

### După Discuție

Calculați împreună:
- 100 senzori × 1 mesaj/5s × 86400s/zi = 1.7M mesaje/zi
- Overhead TCP: 1.7M × 40B = 68MB/zi extra
- Cu baterie de 2000mAh, fiecare byte transmis contează

### Întrebare Follow-up
"Ce facem dacă unele citiri SUNT critice? (ex: detector de fum)"

---

## PI-4: Detectare Erori în Protocol BINAR

### Scenariu
Serverul BINAR primește un mesaj cu CRC invalid.

### Întrebare
Ce ar trebui să facă serverul?

### Opțiuni
- **A)** Ignoră mesajul silențios
- **B)** Trimite ERROR și continuă ✓
- **C)** Închide conexiunea
- **D)** Încearcă să corecteze eroarea

### Analiza Distractorilor

| Opțiune | Problemă |
|---------|----------|
| A | Clientul așteaptă la infinit răspunsul |
| C | Prea agresiv — pierde starea, forțează reconectare |
| D | CRC detectează, NU corectează (nu are redundanță suficientă) |

### După Discuție

Demonstrați practic:
1. Trimiteți un mesaj valid → primiți PONG
2. Modificați manual un byte → primiți ERROR
3. Arătați că conexiunea rămâne deschisă

### Concept Cheie
Protocoalele trebuie să fie reziliente. Eroarea unui mesaj nu trebuie să afecteze celelalte.

---

## PI-5: Încadrare — Lungime Prefix vs Delimitatori

### Scenariu
Proiectezi un protocol pentru transmisie de JSON arbitrar.

### Întrebare
Ce metodă de încadrare (framing) alegi?

### Opțiuni
- **A)** Lungime prefix — eficient, parsing O(1) ✓
- **B)** Delimitator newline — JSON nu conține newline
- **C)** Delimitator NULL byte (\0)
- **D)** Câmpuri fixe — toate JSON-urile identice

### Capcana în Opțiunea B

JSON POATE conține newline în stringuri:
```json
{"mesaj": "Linia 1\nLinia 2"}
```

Și chiar formatat pe mai multe linii:
```json
{
  "nume": "Test",
  "valoare": 123
}
```

### După Discuție

| Metodă | Avantaj | Dezavantaj |
|--------|---------|------------|
| Lungime prefix | O(1) parsing, orice conținut | Eroare în lungime = pierdere sync |
| Delimitator | Recuperare ușoară din erori | Trebuie escaping, O(n) parsing |
| Fix | Foarte simplu | Risipă sau fragmentare |

### Întrebare Follow-up
"HTTP folosește ambele metode. Unde și de ce?"
- Headers: delimitator (CRLF CRLF)
- Body: Content-Length (prefix)

---

## Statistici de Urmărit

După fiecare întrebare, notați:

| Întrebare | % Corect V1 | % Corect V2 | Observații |
|-----------|-------------|-------------|------------|
| PI-1 | | | |
| PI-2 | | | |
| PI-3 | | | |
| PI-4 | | | |
| PI-5 | | | |

### Interpretare

- V1 < 30%: Explicați conceptul înainte de a re-vota
- V1 30-70%: Ideal, discuția în perechi va ajuta
- V1 > 70%: Treceți mai repede, întrebarea e prea ușoară
- V2 - V1 < 10%: Discuția nu a ajutat, reformulați

---

## Resurse Suplimentare

- Mazur, E. (1997). *Peer Instruction: A User's Manual*. Pearson.
- Porter, L. et al. (2011). "Peer Instruction: Do Students Really Learn from Peer Discussion in Computing?"

---

*Fișier pentru instructor — actualizați după fiecare semestru pe baza feedback-ului*

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
