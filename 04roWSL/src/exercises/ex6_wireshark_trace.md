# Exercițiu 6: Analiză Protocol în Wireshark — Fără Cod!

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

---

## Obiectiv

Analizezi o captură Wireshark și răspunzi la întrebări PE HÂRTIE sau într-un document.
Acest exercițiu NU implică scrierea de cod.

**Timp alocat:** 50 minute  
**Punctaj:** 50 puncte

---

## Pregătire

### Pasul 1: Pornește laboratorul

```bash
cd /mnt/d/RETELE/SAPT4/04roWSL
python3 scripts/start_lab.py
```

### Pasul 2: Pornește captura Wireshark

1. Deschide Wireshark
2. Selectează interfața "vEthernet (WSL)"
3. Click pe butonul albastru (Start capture)

### Pasul 3: Generează trafic

```bash
# Rulează clientul BINAR
python3 src/apps/binary_proto_client.py
```

### Pasul 4: Oprește și salvează captura

1. Click pe butonul roșu (Stop)
2. File → Save As → `pcap/exercitiu6.pcapng`

---

## Partea A: Handshake TCP (15 puncte)

Aplică filtrul în Wireshark: `tcp.port == 5401`

Găsește cele 3 pachete ale TCP 3-way handshake (cele care stabilesc conexiunea).

### Întrebarea A1 (3 puncte)
Completează tabelul pentru handshake:

| Pachet | Nr. în captură | Flag-uri TCP | Direcție |
|--------|----------------|--------------|----------|
| SYN | _____ | _____ | Client → Server |
| SYN-ACK | _____ | _____ | Server → Client |
| ACK | _____ | _____ | Client → Server |

### Întrebarea A2 (3 puncte)
Care e ISN (Initial Sequence Number) al clientului?

**Răspuns:** _______________

*Hint: Găsești în pachetul SYN, câmpul "Sequence Number (raw)"*

### Întrebarea A3 (3 puncte)
Care e ISN al serverului?

**Răspuns:** _______________

*Hint: Găsești în pachetul SYN-ACK*

### Întrebarea A4 (3 puncte)
După handshake, care e "Acknowledgment Number" în pachetul ACK al clientului?

**Răspuns:** _______________

*Hint: Ar trebui să fie ISN_server + 1*

### Întrebarea A5 (3 puncte)
Cât timp a durat handshake-ul complet (de la SYN la ultimul ACK)?

**Răspuns:** _______________ ms

*Hint: Wireshark arată timestamp-ul relativ în coloana "Time"*

---

## Partea B: Protocol BINAR (25 puncte)

Găsește primul pachet cu date aplicație (după handshake). Acesta conține primul mesaj BINAR.

### Întrebarea B1 (2 puncte)
Care e numărul pachetului în captură?

**Răspuns:** _______________

### Întrebarea B2 (3 puncte)
Câți bytes de date TCP (payload) conține acest pachet?

**Răspuns:** _______________ bytes

*Hint: Uită-te la "TCP Segment Len" sau la lungimea payload-ului*

### Întrebarea B3 (10 puncte)
Decodează antetul BINAR manual. Completează tabelul:

| Câmp | Offset (bytes) | Valoare HEX | Valoare DEC/ASCII |
|------|----------------|-------------|-------------------|
| Magic | 0-1 | _____ | _____ |
| Versiune | 2 | _____ | _____ |
| Tip | 3 | _____ | _____ (nume: _____) |
| Lungime | 4-5 | _____ | _____ |
| Secvență | 6-9 | _____ | _____ |
| CRC32 | 10-13 | _____ | _____ |

*Hint: În Wireshark, expandează "Data" și vezi bytes-ii în hex. 
Atenție la Network Byte Order (big-endian)!*

### Întrebarea B4 (5 puncte)
Verifică CRC-ul manual:

1. Extrage bytes 0-9 (antet fără CRC) + payload:
   
   **Date hex:** _________________________________

2. Calculează CRC32 (folosește Python sau un calculator online):
   ```python
   import binascii
   date = bytes.fromhex("...")  # pune hex-ul de mai sus
   print(f"0x{binascii.crc32(date) & 0xFFFFFFFF:08X}")
   ```
   
   **CRC calculat:** 0x_______________

3. Se potrivește cu cel din pachet?
   
   **Răspuns:** DA / NU

### Întrebarea B5 (5 puncte)
Ce tip de mesaj este (conform tabelului din documentație)?

| Cod | Nume |
|-----|------|
| 0x01 | PING |
| 0x02 | PONG |
| 0x03 | SET |
| 0x04 | GET |
| 0x05 | DELETE |
| 0x06 | RESPONSE |
| 0xFF | ERROR |

**Tip mesaj:** _______________

**E o cerere (request) sau un răspuns (response)?** _______________

---

## Partea C: Conversație Completă (10 puncte)

Analizează întreaga conversație TCP pentru protocolul BINAR.

### Întrebarea C1 (3 puncte)
Câte mesaje PING trimite clientul în total?

**Răspuns:** _______________

### Întrebarea C2 (3 puncte)
Câte răspunsuri PONG primește clientul?

**Răspuns:** _______________

### Întrebarea C3 (2 puncte)
Care e latența medie (timpul) între un PING și PONG-ul corespunzător?

**Răspuns:** _______________ ms

*Hint: Calculează diferența de timestamp între pachetele pereche*

### Întrebarea C4 (2 puncte)
Câte bytes în total a trimis clientul (sumă TCP payload)?

**Răspuns:** _______________ bytes

*Hint: Statistics → Conversations → TCP → selectează conversația*

---

## Bonus: TCP Teardown (5 puncte extra)

Găsește închiderea conexiunii TCP.

### Întrebarea D1 (2 puncte)
Câte pachete sunt implicate în închiderea conexiunii?

**Răspuns:** _______________

*Hint: Poate fi 4-way (FIN, ACK, FIN, ACK) sau 3-way (FIN-ACK combinat)*

### Întrebarea D2 (3 puncte)
Listează flag-urile TCP pentru fiecare pachet de închidere:

| Pachet | Flag-uri | Direcție |
|--------|----------|----------|
| 1 | _____ | _____ |
| 2 | _____ | _____ |
| 3 | _____ | _____ |
| 4 | _____ | _____ |

---

## Predare

### Format
- Răspunsurile pot fi pe hârtie (fotografiate) sau într-un document
- Include capturi de ecran relevante din Wireshark pentru B3

### Fișiere de încărcat în Moodle
1. Răspunsurile (PDF, DOCX, sau poze)
2. Fișierul de captură: `exercitiu6.pcapng`

### Criterii de evaluare
- Corectitudinea răspunsurilor (40%)
- Demonstrarea înțelegerii conceptelor (30%)
- Calitatea capturilor de ecran și explicațiilor (20%)
- Verificarea manuală a CRC-ului (10%)

---

## Referințe Utile

- [Rezumat Teoretic - Structura Protocol BINAR](../docs/theory_summary.md)
- [Fișa de Comenzi Wireshark](../docs/commands_cheatsheet.md)
- [Ghid Debugging](../docs/debugging_guide.md)

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
