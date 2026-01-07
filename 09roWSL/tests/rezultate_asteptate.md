# Rezultate Așteptate pentru Exerciții

> Ghid de Verificare pentru Săptămâna 9
> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

---

## Exercițiul 1: Codificare Binară și Endianness

### Ieșire Așteptată

```
=== Demonstrație Endianness ===

Valoare originală: 0x12345678 (305419896)

Big-Endian (ordinea rețelei):
  Octeți: 12 34 56 78
  Hex: 12345678

Little-Endian (Intel/AMD):
  Octeți: 78 56 34 12
  Hex: 78563412

Concluzie: Protocoalele de rețea folosesc big-endian!
```

### Verificări Cheie

- [ ] Big-endian pune octetul cel mai semnificativ primul
- [ ] Little-endian pune octetul cel mai puțin semnificativ primul
- [ ] Valorile se decodifică corect înapoi la original

---

## Exercițiul 2: Server FTP Personalizat

### Ieșire Așteptată - Serverul

```
[INFO] Se pornește serverul pseudo-FTP pe portul 2121...
[INFO] Server pornit. Se așteaptă conexiuni...
[INFO] Conexiune nouă de la ('127.0.0.1', 54321)
[DEBUG] Primit: USER test
[DEBUG] Trimis: 331 Parola necesară pentru test
[DEBUG] Primit: PASS 12345
[DEBUG] Trimis: 230 Autentificat cu succes
[DEBUG] Primit: LIST
[DEBUG] Trimis: 150 Se deschide conexiunea de date
[DEBUG] Trimis: 226 Transfer complet
[DEBUG] Primit: QUIT
[DEBUG] Trimis: 221 La revedere
[INFO] Client deconectat
```

### Ieșire Așteptată - Clientul

```
Conectat la server
< 220 Bine ați venit la serverul FTP
> USER test
< 331 Parola necesară pentru test
> PASS 12345
< 230 Autentificat cu succes
> LIST
< 150 Se deschide conexiunea de date
< 226 Transfer complet
> QUIT
< 221 La revedere
Deconectat
```

### Verificări Cheie

- [ ] Serverul răspunde cu codul 220 la conectare
- [ ] Secvența USER → 331 → PASS → 230 funcționează
- [ ] QUIT închide sesiunea grațios

---

## Exercițiul 3: Testare Multi-Client

### Ieșire Așteptată

```
=== Test Multi-Client ===

[Client 1] Conectare...
[Client 2] Conectare...
[Client 1] Autentificare ca alice...
[Client 2] Autentificare ca bob...
[Client 1] LIST - succes
[Client 2] RETR test.txt - succes
[Client 1] Deconectare
[Client 2] Deconectare

Rezumat:
  - Client 1: 3 comenzi executate
  - Client 2: 3 comenzi executate
  - Erori: 0
```

### Verificări Cheie

- [ ] Ambii clienți se conectează simultan
- [ ] Sesiunile sunt independente
- [ ] Nu există interferențe între clienți

---

## Demo: Protocol Binar

### Ieșire Așteptată

```
=== Demonstrație Protocol Binar ===

Payload: "Salut, lume!"
Lungime payload: 12 octeți

CRC-32: 0xA1B2C3D4

Structura header-ului:
  Format: >4sBBII (14 octeți)
  • Magic:    FTPC (46545043)
  • Versiune: 1 (01)
  • Tip:      1 (01) - TEXT
  • Lungime:  12 (0000000c)
  • CRC-32:   0xA1B2C3D4 (a1b2c3d4)

Mesaj complet:
  Hex: 4654504301010000000ca1b2c3d453616c75742c206c756d6521
  Lungime totală: 26 octeți

Verificare CRC: REUȘITĂ
```

### Verificări Cheie

- [ ] Header-ul are exact 14 octeți
- [ ] Magic bytes sunt corecte
- [ ] CRC-32 se verifică cu succes
- [ ] Ordinea octeților este network byte order

---

## Teste Automate

### test_rapid.py

```
================================================
Test Rapid - Săptămâna 9
Verificare funcționalitate de bază
================================================

Verificări Python:
  ✓ Versiune Python >= 3.8
  ✓ Modul struct disponibil
  ✓ Modul zlib disponibil

Verificare Sintaxă:
  ✓ Sintaxă Python validă (XX fișiere)

Verificări Docker:
  ✓ Docker disponibil
  ✓ docker-compose.yml valid

Verificări Funcționale:
  ✓ Demo endianness funcționează
  ✓ CRC-32 funcționează

Structura Proiectului:
  ✓ Director docker/ există
  ✓ Director scripts/ există
  ✓ Director src/exercises/ există

================================================
Rezultate: X/X teste trecute
Toate testele au trecut! Mediul este pregătit.
================================================
```

---

## Coduri de Eroare

### Erori Frecvente și Semnificații

| Cod | Semnificație | Soluție |
|-----|--------------|---------|
| E001 | Docker nu rulează | Porniți Docker Desktop |
| E002 | Port ocupat | Opriți procesul care îl folosește |
| E003 | CRC invalid | Verificați integritatea datelor |
| E004 | Timeout | Verificați conexiunea de rețea |
| E005 | Autentificare eșuată | Verificați credențialele |

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
