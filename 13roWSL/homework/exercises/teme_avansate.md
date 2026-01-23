# Teme Avansate - Săptămâna 13

> Laborator IoT și Securitate în Rețelele de Calculatoare
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

---

## Prezentare Generală

Aceste teme vizează nivelurile superioare ale taxonomiei Bloom:
- **EVALUATE** — analiza critică, comparare, justificare decizii
- **CREATE** — proiectare sisteme noi, sinteză soluții originale

**Notare:** Fiecare temă valorează puncte bonus. Temele pot fi realizate individual sau în echipe de 2.

---

## Teme Nivel EVALUATE

### E1: Evaluare Arhitectură Securitate (15 puncte)

**Context:** Analizează topologia laboratorului (`week13net`) din perspectiva securității.

**Cerințe:**

1. **Evaluează riscurile** (5p) de a avea DVWA (aplicație web vulnerabilă) pe aceeași rețea Docker cu broker-ul MQTT:
   - Ce atacuri ar fi posibile dacă un atacator compromite DVWA?
   - Poate accesa broker-ul MQTT? Cum?
   - Ce date ar putea intercepta?

2. **Propune segmentare** (5p):
   - Desenează o arhitectură îmbunătățită cu rețele separate
   - Explică ce reguli de firewall ai implementa
   - Justifică fiecare decizie

3. **Compară trade-off-uri** (5p):
   - Complexitate vs. Securitate
   - Performanță vs. Izolare
   - Cost operațional vs. Risc acceptat

**Format livrabil:** Document PDF, 2-3 pagini, cu diagrame.

---

### E2: Comparație TLS vs. Text Clar (10 puncte)

**Context:** Ai capturat trafic MQTT pe ambele porturi (1883 și 8883).

**Cerințe:**

1. **Capturează și analizează** (4p):
   - 20 pachete pe portul 1883 (text clar)
   - 20 pachete pe portul 8883 (TLS)
   - Salvează ambele capturi în fișiere `.pcap`

2. **Documentează diferențele** (3p):
   - Ce informații sunt vizibile în fiecare caz?
   - Ce poate extrage un atacator din fiecare captură?
   - Include screenshots din Wireshark

3. **Evaluează scenarii** (3p):
   - Când este acceptabil să folosești portul 1883?
   - Ce riscuri rămân chiar cu TLS activat?
   - Cum ai convinge un manager să investească în TLS pentru IoT?

**Format livrabil:** Document PDF cu capturi de ecran și fișierele `.pcap` atașate.

---

### E3: Audit Vulnerabilități și Prioritizare (12 puncte)

**Context:** Rulează verificatorul de vulnerabilități pe toate serviciile laboratorului.

**Cerințe:**

1. **Execută audit complet** (3p):
   ```bash
   python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py --tinta localhost --toate --output audit.json
   ```

2. **Prioritizează vulnerabilitățile** (5p):
   - Creează o matrice risc/impact pentru fiecare vulnerabilitate găsită
   - Justifică prioritatea: Care rezolvi prima? De ce?
   - Estimează efortul de remediere (ore) pentru fiecare

3. **Critică metodologia** (4p):
   - Ce vulnerabilități ar putea fi RATATE de acest verificator?
   - Cum ai îmbunătăți instrumentul?
   - Compară cu un scanner comercial (ex: Nessus, OpenVAS) — ce lipsește?

**Format livrabil:** Spreadsheet Excel/Calc cu matricea + document explicativ.

---

### E4: Decizie Arhitecturală QoS (8 puncte)

**Context:** Proiectezi un sistem IoT pentru monitorizarea temperaturii într-un depozit de medicamente.

**Cerințe:**

1. **Analizează scenariul** (3p):
   - Temperatura trebuie monitorizată la fiecare 30 secunde
   - Alertele de temperatură critică (>8°C) trebuie livrate garantat
   - Sunt 50 de senzori, fiecare trimite ~100 bytes/mesaj

2. **Justifică alegerea QoS** (3p):
   - Ce QoS folosești pentru telemetria normală? De ce?
   - Ce QoS folosești pentru alerte? De ce?
   - Calculează overhead-ul în bytes pentru fiecare alegere

3. **Evaluează alternative** (2p):
   - Ce s-ar întâmpla dacă folosești QoS 2 pentru tot?
   - Când ar fi justificat acest overhead?

**Format livrabil:** Document 1-2 pagini cu calcule și justificări.

---

## Teme Nivel CREATE

### C1: Proiectare Sistem IoT Securizat (25 puncte)

**Context:** Proiectează o arhitectură Docker completă pentru un sistem IoT de tip "Smart Home".

**Cerințe funcționale:**
- 5 senzori de temperatură (simulați cu scripturi Python)
- 2 senzori de mișcare (simulați)
- 1 broker MQTT central
- 1 aplicație dashboard (poate fi un simplu script care loghează)
- 1 serviciu de alertare

**Cerințe de securitate:**
- TLS obligatoriu pentru toate conexiunile MQTT
- Autentificare cu username/parolă pentru fiecare senzor
- Rețele Docker separate pentru senzori vs. aplicații
- Logging centralizat al tuturor evenimentelor

**Livrabile:**

1. **`docker-compose.yml` funcțional** (10p):
   - Toate serviciile definite
   - Rețele configurate corect
   - Volume pentru persistență
   - Health checks

2. **Diagrama arhitectură** (5p):
   - Format ASCII sau draw.io/diagrams.net
   - Arată fluxul datelor
   - Evidențiază granițele de securitate

3. **Documentație** (5p):
   - README cu instrucțiuni de pornire
   - Explicația deciziilor de design
   - Credențiale și configurări

4. **Demonstrație** (5p):
   - Script care simulează un scenariu complet
   - Capturi Wireshark care demonstrează criptarea
   - Log-uri care arată alertele funcționând

**Termen:** 2 săptămâni de la data laboratorului.

---

### C2: Instrument de Detectare Anomalii MQTT (20 puncte)

**Context:** Creează un instrument Python care monitorizează traficul MQTT și detectează comportament anormal.

**Funcționalități cerute:**

1. **Monitorizare de bază** (6p):
   - Conectare la broker ca subscriber pe `#` (toate topicurile)
   - Logare: timestamp, topic, dimensiune payload, QoS
   - Statistici: mesaje/minut per topic

2. **Detectare anomalii** (8p):
   - Alertă dacă un topic primește >100 mesaje/minut (posibil flood)
   - Alertă dacă payload-ul depășește 10KB (neobișnuit pentru IoT)
   - Alertă dacă un client nou se conectează (topic $SYS)
   - Alertă dacă apar topicuri cu pattern suspect (ex: "../", "cmd/", "exec/")

3. **Raportare** (6p):
   - Output în timp real în terminal
   - Export periodic în JSON
   - Sumar la închidere: total mesaje, anomalii detectate, topicuri active

**Structura codului:**
```
src/apps/
└── detector_anomalii.py
```

**Utilizare:**
```bash
python3 src/apps/detector_anomalii.py --broker localhost --port 1883 --output anomalii.json
```

**Termen:** 2 săptămâni de la data laboratorului.

---

### C3: Extensie Scanner Porturi (15 puncte)

**Context:** Extinde scanner-ul de porturi din exercițiul 1 cu funcționalități avansate.

**Funcționalități noi:**

1. **Service fingerprinting** (5p):
   - După detectarea unui port deschis, trimite probe specifice
   - Identifică: HTTP (GET /), FTP (banner), MQTT (CONNECT), SSH (banner)
   - Raportează versiunea dacă e disponibilă

2. **Rate limiting inteligent** (5p):
   - Detectează dacă ținta începe să blocheze (multe timeout-uri)
   - Reduce automat viteza de scanare
   - Afișează avertisment utilizatorului

3. **Export în format Nmap XML** (5p):
   - Compatibilitate cu instrumente de analiză existente
   - Include toate informațiile: porturi, servicii, bannere

**Fișier de modificat:**
```
src/exercises/ex_13_01_scanner_porturi.py
```

**Teste:**
- Funcționează pe localhost cu toate serviciile laboratorului
- Export XML valid (verificabil cu `xmllint`)

---

### C4: Mini-Honeypot FTP (18 puncte)

**Context:** Creează un honeypot FTP simplu care simulează vulnerabilitatea vsftpd 2.3.4 și loghează încercările de exploatare.

**Funcționalități:**

1. **Server FTP minimal** (6p):
   - Ascultă pe un port configurabil
   - Acceptă comenzi: USER, PASS, QUIT
   - Răspunde cu banner-ul vsftpd 2.3.4

2. **Detectare exploatare** (6p):
   - Detectează username-uri care conțin `:)` (trigger-ul backdoor-ului)
   - Loghează: IP sursă, timestamp, payload complet
   - Deschide un port fals "backdoor" care doar loghează comenzile primite

3. **Raportare** (6p):
   - Log în format JSON pentru analiză
   - Statistici: încercări totale, IP-uri unice, comenzi primite
   - Alertă în timp real la detectare

**Structura:**
```
src/apps/
└── honeypot_ftp.py
```

**Considerații etice:**
- Documentează clar că este un honeypot educațional
- Nu implementa funcționalități reale de backdoor
- Include avertisment despre utilizarea legală

---

## Criterii de Evaluare Generale

### Pentru teme EVALUATE:

| Criteriu | Excelent (100%) | Bun (75%) | Satisfăcător (50%) | Insuficient (<50%) |
|----------|-----------------|-----------|--------------------|--------------------|
| Analiză | Profundă, cu nuanțe | Completă | Superficială | Lipsă |
| Justificare | Argumente solide | Argumente OK | Opinii fără suport | Afirmații goale |
| Comparație | Multi-dimensională | Corectă | Parțială | Incorectă |
| Documentare | Profesională | Clară | Acceptabilă | Dezordonată |

### Pentru teme CREATE:

| Criteriu | Excelent (100%) | Bun (75%) | Satisfăcător (50%) | Insuficient (<50%) |
|----------|-----------------|-----------|--------------------|--------------------|
| Funcționalitate | Completă + extra | Completă | Parțială | Nu funcționează |
| Cod | Curat, documentat | Clar | Funcțional | Dezordonat |
| Testare | Automată + manuală | Manuală OK | Minimală | Netestată |
| Documentare | Exemplară | Bună | Acceptabilă | Lipsă |

---

## Resurse Utile

- OWASP IoT Top 10: https://owasp.org/www-project-internet-of-things/
- MQTT Security Fundamentals: https://www.hivemq.com/mqtt-security-fundamentals/
- Docker Security Best Practices: https://docs.docker.com/develop/security-best-practices/
- Wireshark MQTT Dissector: https://wiki.wireshark.org/MQTT

---

## Predare

- **Unde:** Platforma e-learning a cursului sau GitHub repository personal
- **Format:** Arhivă ZIP cu toate fișierele
- **Naming:** `S13_Tema_[E1|C1|...]_NumePrenume.zip`
- **Deadline:** Vezi calendarul cursului

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
