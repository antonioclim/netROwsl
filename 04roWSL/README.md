# Săptămâna 4: Nivelul Fizic, Nivelul Legătură de Date și Protocoale Personalizate

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator
>
> realizat de Revolvix

## Prezentare Generală

Această săptămână explorează fundamentele transmisiei datelor prin **Nivelul Fizic** și **Nivelul Legătură de Date** din modelul OSI. Veți înțelege cum sunt transformate datele în semnale pentru transmisie și cum sunt detectate și corectate erorile la nivelul cadrelor.

Componenta practică se concentrează pe **proiectarea și implementarea protocoalelor personalizate** folosind TCP și UDP. Veți construi trei tipuri de protocoale:
- **Protocol TEXT**: Format lizibil de către om, cu încadrare bazată pe lungime
- **Protocol BINAR**: Format eficient cu anteturi fixe și verificare CRC32
- **Protocol Senzor UDP**: Datagrame fără conexiune cu validare integritate

Aceste exerciții demonstrează principiile fundamentale ale comunicării în rețea: încadrarea mesajelor, serializarea datelor, detectarea erorilor și diferențele dintre protocoalele orientate pe conexiune (TCP) versus cele fără conexiune (UDP).

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele și funcțiile Nivelului Fizic și Nivelului Legătură de Date
2. **Explicați** tehnicile de încadrare (delimitare bazată pe lungime vs. delimitatori) și mecanismele de detectare a erorilor
3. **Implementați** protocoale personalizate text și binare folosind programarea cu socket-uri în Python
4. **Analizați** traficul de rețea pentru a verifica comportamentul protocolului și structura mesajelor
5. **Proiectați** formate de mesaje cu câmpuri de antet și sarcină utilă (payload) corespunzătoare
6. **Evaluați** compromisurile dintre protocoalele text și cele binare în diferite scenarii

## Cerințe Preliminare

### Cunoștințe Necesare
- Înțelegerea de bază a modelului OSI și straturilor TCP/IP
- Familiaritate cu programarea socket-urilor Python (Săptămâna 2-3)
- Cunoașterea reprezentării datelor binare și a codificării caracterelor
- Experiență cu analiza traficului folosind Wireshark (Săptămâna 1)

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau mai nou
- Git (opțional, pentru controlul versiunilor)

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Rulează O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK4_WSLkit_RO

# Verificați cerințele preliminare
python setup/verify_environment.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/install_prerequisites.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/start_lab.py

# Verificați că totul rulează
python scripts/start_lab.py --status

# Alternativ, rulați în mod nativ (fără Docker)
python scripts/start_lab.py --native
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Protocol TEXT | localhost:5400 | N/A |
| Protocol BINAR | localhost:5401 | N/A |
| Senzor UDP | localhost:5402 | N/A |

## Exerciții de Laborator

### Exercițiul 1: Protocol TEXT peste TCP

**Obiectiv:** Implementați și testați un protocol text simplu cu încadrare bazată pe lungime

**Durată:** 30-40 minute

**Context:**
Protocolul TEXT folosește mesaje lizibile de către om în format `<LUNGIME> <CONTINUT>`. Serverul menține un magazin cheie-valoare și răspunde la comenzi precum PING, SET, GET, DEL, COUNT și KEYS.

**Pași:**

1. **Porniți serverul TEXT:**
   ```powershell
   # Mod Docker (automat cu start_lab.py)
   python scripts/start_lab.py --service text
   
   # Sau mod nativ
   cd src/apps
   python text_proto_server.py
   ```

2. **Conectați-vă cu netcat sau clientul:**
   ```powershell
   # Folosind clientul furnizat
   python src/apps/text_proto_client.py
   
   # Sau folosind netcat
   nc localhost 5400
   ```

3. **Testați comenzile protocolului:**
   ```
   4 PING           -> Răspuns: 4 PONG
   13 SET cheie val -> Răspuns: 2 OK
   9 GET cheie      -> Răspuns: 3 val
   5 COUNT          -> Răspuns: 1 1
   4 KEYS           -> Răspuns: 5 cheie
   9 DEL cheie      -> Răspuns: 2 OK
   4 QUIT           -> Conexiune închisă
   ```

4. **Observați formatul de încadrare:**
   - Fiecare mesaj începe cu un număr indicând lungimea
   - Urmat de un spațiu și conținutul propriu-zis
   - Acest lucru permite serverului să știe exact câți octeți să citească

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 1
```

**Ce să Observați:**
- Cum prefixul de lungime permite serverului să parseze mesajele
- Modul în care serverul gestionează multiple comenzi pe aceeași conexiune
- Diferența între tipurile de comenzi (cu date vs. fără date)

---

### Exercițiul 2: Protocol BINAR cu CRC32

**Obiectiv:** Implementați un protocol binar eficient cu verificare integritate

**Durată:** 40-50 minute

**Context:**
Protocolul BINAR folosește un antet fix de 14 octeți pentru eficiență. Include verificare CRC32 pentru detectarea erorilor de transmisie.

**Structura Antetului (14 octeți):**
```
+--------+--------+--------+--------+--------+--------+--------+
| Offset |   0    |   1    |   2    |   3    |   4    |   5    |
+--------+--------+--------+--------+--------+--------+--------+
| Câmp   | Magic ('N')| Magic ('P')| Versiune | Tip    | Lung. (MSB)|Lung. (LSB)|
+--------+--------+--------+--------+--------+--------+--------+

+--------+--------+--------+--------+--------+--------+--------+--------+
| Offset |   6    |   7    |   8    |   9    |   10   |   11   |  12   |  13   |
+--------+--------+--------+--------+--------+--------+--------+--------+
| Câmp   |     Secvență (4 octeți)          |      CRC32 (4 octeți)          |
+--------+--------+--------+--------+--------+--------+--------+--------+
```

**Pași:**

1. **Porniți serverul BINAR:**
   ```powershell
   python scripts/start_lab.py --service binary
   
   # Sau mod nativ
   cd src/apps
   python binary_proto_server.py
   ```

2. **Rulați clientul binar:**
   ```powershell
   python src/apps/binary_proto_client.py
   ```

3. **Analizați structura mesajelor:**
   ```python
   import struct
   
   # Construirea unui antet binar
   magic = b'NP'
   versiune = 1
   tip_mesaj = 0x01  # PING
   payload = b''
   lungime = len(payload)
   secventa = 1
   
   # Împachetare fără CRC (pentru calcul)
   antet_fara_crc = struct.pack('!2sBBHI', magic, versiune, tip_mesaj, lungime, secventa)
   
   # Calculare CRC32
   import binascii
   crc = binascii.crc32(antet_fara_crc + payload) & 0xFFFFFFFF
   
   # Antet complet cu CRC
   antet = struct.pack('!2sBBHII', magic, versiune, tip_mesaj, lungime, secventa, crc)
   ```

4. **Capturați și analizați traficul:**
   ```powershell
   python scripts/capture_traffic.py --port 5401 --output pcap/protocol_binar.pcap
   ```

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 2
```

**Ce să Observați:**
- Eficiența antetului fix față de încadrarea text
- Cum CRC32 detectează coruperea datelor
- Ordinea octeților în rețea (big-endian) pentru câmpuri numerice

---

### Exercițiul 3: Protocol Senzor UDP

**Obiectiv:** Implementați comunicație fără conexiune cu datagrame de dimensiune fixă

**Durată:** 30-40 minute

**Context:**
Protocolul senzor UDP simulează dispozitive IoT care trimit citiri periodice de temperatură. Fiecare datagramă are exact 23 de octeți.

**Structura Datagramei (23 octeți):**
```
+--------+------------+----------------+-----------+--------+----------+
| Câmp   | Versiune   | ID Senzor      | Temp      | Locație| CRC32    | Rezervat |
+--------+------------+----------------+-----------+--------+----------+
| Octeți | 1          | 2              | 4 (float) | 10     | 4        | 2        |
+--------+------------+----------------+-----------+--------+----------+
```

**Pași:**

1. **Porniți serverul senzor UDP:**
   ```powershell
   python scripts/start_lab.py --service udp
   
   # Sau mod nativ
   python src/apps/udp_sensor_server.py
   ```

2. **Trimiteți citiri de senzor:**
   ```powershell
   python src/apps/udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Bucuresti"
   ```

3. **Simulați mai mulți senzori:**
   ```powershell
   # Trimiteți citiri de la mai mulți senzori
   python src/apps/udp_sensor_client.py --sensor-id 1 --temp 22.0 --location "Laborator1"
   python src/apps/udp_sensor_client.py --sensor-id 2 --temp 24.5 --location "Laborator2"
   python src/apps/udp_sensor_client.py --sensor-id 3 --temp 21.0 --location "Hol"
   ```

4. **Observați caracteristicile UDP:**
   - Fără stabilire de conexiune
   - Fără confirmare de livrare
   - Datagramele pot fi pierdute sau reordonate
   - Overhead mai mic decât TCP

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 3
```

**Ce să Observați:**
- Diferența de comportament între TCP și UDP
- De ce dimensiunea fixă simplifică parsarea
- Cum validarea CRC32 funcționează pentru datagrame

---

### Exercițiul 4: Detectarea Erorilor cu CRC32

**Obiectiv:** Demonstrați detectarea coruperii datelor folosind CRC32

**Durată:** 20-30 minute

**Context:**
CRC32 (Cyclic Redundancy Check pe 32 de biți) este folosit pentru a detecta erorile accidentale în datele transmise. Acest exercițiu demonstrează eficacitatea sa.

**Pași:**

1. **Rulați demonstrația de erori:**
   ```powershell
   python scripts/run_demo.py --demo 4
   ```

2. **Experimentați manual cu coruperea:**
   ```python
   import binascii
   
   # Date originale
   date_originale = b"Mesaj de test pentru CRC"
   crc_original = binascii.crc32(date_originale) & 0xFFFFFFFF
   print(f"CRC original: {crc_original:08X}")
   
   # Corupere un singur bit
   date_corupte = bytearray(date_originale)
   date_corupte[5] ^= 0x01  # Inversare un bit
   crc_corupt = binascii.crc32(bytes(date_corupte)) & 0xFFFFFFFF
   print(f"CRC corupt: {crc_corupt:08X}")
   
   # Verificare detecție
   if crc_original != crc_corupt:
       print("Corupere detectată cu succes!")
   ```

3. **Testați diferite tipuri de erori:**
   - Inversare bit unic
   - Inversare biți multipli
   - Inserare/ștergere octeți
   - Reordonare secțiuni

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 4
```

**Ce să Observați:**
- CRC32 detectează orice eroare de un singur bit
- Detectează majoritatea erorilor de biți multipli
- Nu este potrivit pentru verificări de securitate (nu este hash criptografic)

---

## Demonstrații

### Demo 1: Protocol TEXT

Demonstrație automată a operațiilor protocolului TEXT.

```powershell
python scripts/run_demo.py --demo 1
```

**Ce să observați:**
- Secvența cerere-răspuns
- Formatul de încadrare cu prefixul de lungime
- Operațiile magazinului cheie-valoare

### Demo 2: Protocol BINAR

Demonstrație a protocolului binar eficient.

```powershell
python scripts/run_demo.py --demo 2
```

**Ce să observați:**
- Antetul binar compact
- Numerele de secvență pentru urmărire
- Verificarea CRC32 la fiecare mesaj

### Demo 3: Simulare Senzori UDP

Simulare a mai multor senzori IoT care trimit date.

```powershell
python scripts/run_demo.py --demo 3
```

**Ce să observați:**
- Natura fără conexiune a UDP
- Multiple surse de date
- Dimensiunea fixă a datagramelor

### Demo 4: Detectare Erori CRC32

Demonstrație a detectării coruperii datelor.

```powershell
python scripts/run_demo.py --demo 4
```

**Ce să observați:**
- Pachete valide acceptate
- Pachete corupte respinse
- Sensibilitatea la schimbări de un singur bit

---

## Capturare și Analiză Pachete

### Capturare Trafic

```powershell
# Pornire captură
python scripts/capture_traffic.py --interface eth0 --output pcap/saptamana4_captura.pcap

# Sau folosiți Wireshark direct
# Deschideți Wireshark > Selectați interfața corespunzătoare
```

### Filtre Wireshark Sugerate

```
# Protocol TEXT (TCP port 5400)
tcp.port == 5400

# Protocol BINAR (TCP port 5401)
tcp.port == 5401

# Protocol Senzor UDP (port 5402)
udp.port == 5402

# Filtrare după conținut
tcp contains "PING"
tcp contains "SET"

# Urmărire flux TCP
# Click dreapta pe pachet -> Follow -> TCP Stream
```

### Analiză cu tshark

```bash
# Afișare conversații TCP
tshark -r captura.pcap -q -z conv,tcp

# Extragere date payload
tshark -r captura.pcap -T fields -e data

# Filtrare și afișare pachete specifice
tshark -r captura.pcap -Y "tcp.port == 5400" -V
```

---

## Oprire și Curățare

### Sfârșitul Sesiunii

```powershell
# Oprire toate containerele (păstrează datele)
python scripts/stop_lab.py

# Verificare oprire
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminare toate containerele, rețelele și volumele pentru această săptămână
python scripts/cleanup.py --full

# Verificare curățare
docker system df
```

---

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Protocol Binar Extins
Extindeți protocolul BINAR cu tipuri noi de mesaje și funcționalități avansate.

### Tema 2: Protocol UDP Fiabil
Proiectați și implementați un protocol de transfer fiabil peste UDP.

---

## Depanare

### Probleme Frecvente

#### Problema: Portul este deja în uz
**Soluție:**
```powershell
# Găsiți procesul care folosește portul
netstat -ano | findstr :5400

# Opriți procesul sau folosiți alt port
python scripts/stop_lab.py
```

#### Problema: Docker nu pornește
**Soluție:**
```powershell
# Verificați că Docker Desktop rulează
docker info

# Reporniți Docker Desktop dacă este necesar
```

#### Problema: Conexiune refuzată la server
**Soluție:**
```powershell
# Verificați starea serviciilor
python scripts/start_lab.py --status

# Verificați jurnalele containerului
docker logs week4-lab
```

#### Problema: CRC32 nu se potrivește
**Soluție:**
- Verificați ordinea octeților (big-endian pentru rețea)
- Asigurați-vă că toate câmpurile sunt incluse în calcul
- Verificați că CRC este calculat înainte de a fi adăugat la mesaj

Consultați `docs/troubleshooting.md` pentru mai multe soluții.

---

## Fundament Teoretic

### Nivelul Fizic

Nivelul Fizic se ocupă cu transmisia biților bruti prin mediul de comunicare:
- **Semnalizare**: Convertirea biților în semnale electrice, optice sau radio
- **Sincronizare**: Acordul asupra ratei de transfer
- **Specificații fizice**: Conectori, cabluri, tensiuni

### Nivelul Legătură de Date

Nivelul Legătură de Date oferă transfer fiabil între noduri adiacente:
- **Încadrare**: Gruparea biților în cadre
- **Detectarea erorilor**: CRC, checksum, paritate
- **Controlul accesului la mediu**: CSMA/CD, CSMA/CA
- **Adresare**: Adrese MAC

### Tehnici de Încadrare

1. **Prefix de lungime**: Lungimea mesajului specificată la început
   - Avantaje: Simplu, eficient
   - Dezavantaje: Coruperea lungimii pierde sincronizarea

2. **Delimitatori**: Caractere sau secvențe speciale marchează limitele
   - Avantaje: Rezistent la corupere parțială
   - Dezavantaje: Necesită escaping, overhead

3. **Câmpuri de dimensiune fixă**: Toate mesajele au aceeași lungime
   - Avantaje: Parsare foarte simplă
   - Dezavantaje: Risipă pentru mesaje scurte

### CRC32 (Cyclic Redundancy Check)

CRC32 este un algoritm de detectare a erorilor care calculează o „amprentă" de 32 de biți pentru un bloc de date:
- Detectează toate erorile de un singur bit
- Detectează majoritatea erorilor de biți multipli
- Detectează toate erorile de rafală până la 32 de biți
- Nu oferă securitate (nu este hash criptografic)

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 768 - User Datagram Protocol
- RFC 793 - Transmission Control Protocol
- Documentația Python: modulele `socket` și `struct`

---

## Diagramă Arhitectură

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GAZDĂ WINDOWS (WSL2)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐           │
│   │  Wireshark  │    │  PowerShell │    │   VS Code   │           │
│   │  (Analiză)  │    │  (Comenzi)  │    │  (Editor)   │           │
│   └──────┬──────┘    └──────┬──────┘    └─────────────┘           │
│          │                  │                                      │
│          │    localhost:5400/5401/5402                            │
│          │                  │                                      │
├──────────┼──────────────────┼──────────────────────────────────────┤
│          │     DOCKER DESKTOP (Backend WSL2)                       │
│          │                  │                                      │
│   ┌──────┴──────────────────┴───────────────────────────────┐     │
│   │              Container: week4-lab                        │     │
│   │              Imagine: python:3.11-slim                   │     │
│   │                                                          │     │
│   │   ┌─────────────────────────────────────────────────┐   │     │
│   │   │  ┌───────────┐ ┌───────────┐ ┌───────────────┐  │   │     │
│   │   │  │  Server   │ │  Server   │ │    Server     │  │   │     │
│   │   │  │   TEXT    │ │   BINAR   │ │  Senzor UDP   │  │   │     │
│   │   │  │ TCP:5400  │ │ TCP:5401  │ │   UDP:5402    │  │   │     │
│   │   │  └───────────┘ └───────────┘ └───────────────┘  │   │     │
│   │   │                                                  │   │     │
│   │   │  ┌─────────────────────────────────────────┐    │   │     │
│   │   │  │  Utilitare: tcpdump, tshark, netcat     │    │   │     │
│   │   │  └─────────────────────────────────────────┘    │   │     │
│   │   └─────────────────────────────────────────────────┘   │     │
│   │                                                          │     │
│   │   Rețea: week4_network (172.28.0.0/16)                  │     │
│   │   IP Container: 172.28.1.10                              │     │
│   └──────────────────────────────────────────────────────────┘     │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────┐     │
│   │              Container: portainer                        │     │
│   │              https://localhost:9443                      │     │
│   └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
