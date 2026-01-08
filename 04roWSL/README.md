# Săptămâna 4: Nivelul Fizic, Nivelul Legătură de Date și Protocoale Personalizate

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator
>
> realizat de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `04roWSL`

**Arhitectura Mediului:**
```
Windows 11 → WSL2 → Ubuntu 22.04 (implicit) → Docker Engine → Portainer CE
```

**Credențiale Standard:**
| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

---

## 📥 Clonarea Laboratorului Acestei Săptămâni

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 4
git clone https://github.com/antonioclim/netROwsl.git SAPT4
cd SAPT4
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 04roWSL/
cd 04roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT4\
    └── 04roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        ├── docs/            # Documentație suplimentară
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
        │   ├── apps/        # Servere și clienți protocol
        │   ├── exercises/   # Exerciții de laborator
        │   └── utils/       # Utilitare protocol
        ├── tests/           # Teste automatizate
        └── README.md        # Acest fișier
```

---

## 🔧 Configurarea Inițială a Mediului (Doar Prima Dată)

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows, ai mai multe opțiuni:
- Click pe "Ubuntu" în meniul Start, SAU
- În PowerShell tastează: `wsl`, SAU
- În Windows Terminal selectează tab-ul "Ubuntu"

Vei vedea promptul Ubuntu:
```
stud@CALCULATOR:~$
```

### Pasul 2: Pornește Serviciul Docker

```bash
# Pornește Docker (necesar după fiecare restart Windows)
sudo service docker start
# Parolă: stud

# Verifică că Docker rulează
docker ps
```

**Output așteptat:**
```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

Dacă vezi containerul `portainer` în listă, mediul este pregătit.

### Pasul 3: Verifică Accesul la Portainer

1. Deschide browser-ul web (Chrome, Firefox, Edge)
2. Navighează la: **http://localhost:9000**

**Credențiale de autentificare:**
- Utilizator: `stud`
- Parolă: `studstudstud`

**Ce să faci dacă Portainer nu răspunde:**
```bash
# Verifică dacă containerul Portainer există
docker ps -a | grep portainer

# Dacă e oprit, pornește-l
docker start portainer

# Dacă nu există, creează-l
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest
```

### Pasul 4: Navighează la Folderul Laboratorului în WSL

```bash
# Navighează la folderul laboratorului
cd /mnt/d/RETELE/SAPT4/04roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor

Navighează: **Home → local → Containers**

Vei vedea un tabel cu toate containerele care include:
- **Nume** - Identificatorul containerului (saptamana4-text, saptamana4-binar, saptamana4-senzor)
- **Stare** - Running/Stopped/Paused
- **Imagine** - Imaginea Docker folosită
- **Porturi** - Mapările de porturi host:container

### Acțiuni asupra Containerelor în Portainer

Pentru orice container, poți efectua următoarele operații:

| Acțiune | Descriere | Cum să o faci |
|---------|-----------|---------------|
| **Start** | Pornește containerul oprit | Butonul verde ▶ |
| **Stop** | Oprește containerul | Butonul roșu ■ |
| **Restart** | Repornește containerul | Butonul ↻ |
| **Logs** | Vezi jurnalele containerului | Click pe nume → tab "Logs" |
| **Console** | Accesează shell-ul containerului | Click pe nume → tab "Console" → "Connect" |
| **Inspect** | Vezi configurația JSON detaliată | Click pe nume → tab "Inspect" |
| **Stats** | Monitorizare CPU/Memorie/Rețea în timp real | Click pe nume → tab "Stats" |

### Vizualizarea Rețelei retea_saptamana4

1. Navighează: **Networks → retea_saptamana4**
2. Observă containerele conectate și configurația rețelei
3. Vezi adresele IP ale containerelor serviciilor protocol

### Modificarea Porturilor Containerului

1. În Portainer: selectează containerul → "Inspect" → derulează la "HostConfig.PortBindings"
2. Pentru a modifica permanent, editează `docker/docker-compose.yml`:
   ```yaml
   ports:
     - "5400:5400"   # Protocol TEXT
     - "5401:5401"   # Protocol BINAR
     - "5402:5402/udp"   # Senzor UDP
   ```
3. Recreează containerul:
   ```bash
   docker-compose -f docker/docker-compose.yml down
   docker-compose -f docker/docker-compose.yml up -d
   ```

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a examina structura mesajelor protocoalelor TEXT, BINAR și UDP
- Pentru a verifica validarea CRC32

### Pasul 1: Lansează Wireshark

Din Meniul Start Windows: Caută "Wireshark" → Click pentru a deschide

Alternativ, din PowerShell:
```powershell
& "C:\Program Files\Wireshark\Wireshark.exe"
```

### Pasul 2: Selectează Interfața de Captură

**CRITIC:** Selectează interfața corectă pentru traficul WSL:

| Numele Interfeței | Când să Folosești |
|-------------------|-------------------|
| **vEthernet (WSL)** | ✅ Cel mai frecvent - capturează traficul Docker WSL |
| **vEthernet (WSL) (Hyper-V firewall)** | Alternativă dacă prima nu funcționează |
| **Loopback Adapter** | Doar pentru trafic localhost (127.0.0.1) |
| **Ethernet/Wi-Fi** | Trafic rețea fizică (nu Docker) |

**Cum selectezi:** Dublu-click pe numele interfeței SAU selecteaz-o și click pe icoana aripioarei albastre de rechin.

### Pasul 3: Generează Trafic

Cu Wireshark capturând (vei vedea pachete apărând în timp real), rulează exercițiile:

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT4/04roWSL

# Testează protocolul TEXT
python3 src/apps/text_proto_client.py

# Testează protocolul BINAR
python3 src/apps/binary_proto_client.py

# Trimite date UDP de senzor
python3 src/apps/udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Lab"
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 4

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `tcp.port == 5400` | Protocol TEXT | Trafic server TEXT |
| `tcp.port == 5401` | Protocol BINAR | Trafic server BINAR |
| `udp.port == 5402` | Senzor UDP | Datagrame senzor |
| `tcp contains "PING"` | Comenzi TEXT specifice | Filtrare comenzi |
| `tcp contains "SET"` | Comenzi SET | Operații key-value |
| `tcp.flags.syn == 1` | Handshake TCP | Inițializări conexiuni |
| `tcp.len > 14` | Pachete cu payload | Exclud ACK-uri goale |
| `data.len == 23` | Datagrame senzor (23 octeți) | Structură fixă UDP |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 5400 && tcp.len > 0`
- SAU: `tcp.port == 5400 || tcp.port == 5401`
- NU: `!arp && !dns`

### Analiza Structurii Mesajelor în Wireshark

#### Protocol TEXT (Port 5400)
```
Wireshark: Click dreapta pe pachet → Follow → TCP Stream
```
Vei vedea conversația în format text:
```
4 PING
4 PONG
13 SET cheie val
2 OK
```

#### Protocol BINAR (Port 5401)
```
Wireshark: Selectează pachet → Expand "Data" în panoul de jos
```
Structura antetului de 14 octeți:
- Bytes 0-1: Magic ("NP" = 0x4E 0x50)
- Byte 2: Versiune
- Byte 3: Tip mesaj
- Bytes 4-5: Lungime payload
- Bytes 6-9: Număr secvență
- Bytes 10-13: CRC32

#### Protocol Senzor UDP (Port 5402)
```
Wireshark: Selectează datagrama UDP → Expand "Data"
```
Structura datagramei de 23 octeți:
- Byte 0: Versiune
- Bytes 1-2: ID Senzor
- Bytes 3-6: Temperatură (float)
- Bytes 7-16: Locație (10 caractere)
- Bytes 17-20: CRC32
- Bytes 21-22: Rezervat

### Verificarea CRC32 în Wireshark

1. Capturează un pachet cu protocol BINAR
2. În panoul de detalii, copiază bytes-urile antetului
3. În Python, verifică manual:
```python
import binascii
# header_fara_crc = bytes copiați din Wireshark (primii 10 bytes + payload)
# crc_din_pachet = ultimii 4 bytes din antet
crc_calculat = binascii.crc32(header_fara_crc) & 0xFFFFFFFF
print(f"CRC calculat: {crc_calculat:08X}")
```

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Text negru, fundal roșu | Erori, checksum-uri greșite |
| Text negru, fundal galben | Avertismente, retransmisii |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT4\04roWSL\pcap\`
3. Nume fișier sugestiv: `protocol_binar_crc.pcap` sau `senzor_udp.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

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
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau mai nou
- Git (opțional, pentru controlul versiunilor)

### Cerințe Hardware

- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Rulează O Singură Dată)

```bash
# Deschideți terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT4/04roWSL

# Verificați cerințele preliminare
python3 setup/verify_environment.py

# Dacă apar probleme, rulați asistentul de instalare
python3 setup/install_prerequisites.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT4/04roWSL

# Porniți toate serviciile
python3 scripts/start_lab.py

# Verificați că totul rulează
python3 scripts/start_lab.py --status

# Alternativ, rulați în mod nativ (fără Docker)
python3 scripts/start_lab.py --native
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Protocol TEXT | localhost:5400 | N/A |
| Protocol BINAR | localhost:5401 | N/A |
| Senzor UDP | localhost:5402 | N/A |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Protocol TEXT peste TCP

**Obiectiv:** Implementați și testați un protocol text simplu cu încadrare bazată pe lungime

**Durată:** 30-40 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` cu filtrul `tcp.port == 5400` ÎNAINTE de a începe exercițiul.

**Context:**
Protocolul TEXT folosește mesaje lizibile de către om în format `<LUNGIME> <CONTINUT>`. Serverul menține un magazin cheie-valoare și răspunde la comenzi precum PING, SET, GET, DEL, COUNT și KEYS.

**Pași:**

1. **Porniți serverul TEXT:**
   ```bash
   # În terminalul Ubuntu
   cd /mnt/d/RETELE/SAPT4/04roWSL
   
   # Mod Docker (automat cu start_lab.py)
   python3 scripts/start_lab.py --service text
   
   # Sau mod nativ
   python3 src/apps/text_proto_server.py
   ```

2. **Conectați-vă cu netcat sau clientul:**
   ```bash
   # Folosind clientul furnizat
   python3 src/apps/text_proto_client.py
   
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
```bash
python3 tests/test_exercises.py --exercise 1
```

**Ce să Observați:**
- Cum prefixul de lungime permite serverului să parseze mesajele
- Modul în care serverul gestionează multiple comenzi pe aceeași conexiune
- Diferența între tipurile de comenzi (cu date vs. fără date)

---

### Exercițiul 2: Protocol BINAR cu CRC32

**Obiectiv:** Implementați un protocol binar eficient cu verificare integritate

**Durată:** 40-50 minute

**Pregătire Wireshark:** Schimbă filtrul la `tcp.port == 5401` pentru a observa traficul protocolului binar.

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
   ```bash
   python3 scripts/start_lab.py --service binar
   
   # Sau mod nativ
   python3 src/apps/binary_proto_server.py
   ```

2. **Rulați clientul binar:**
   ```bash
   python3 src/apps/binary_proto_client.py
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
   ```bash
   python3 scripts/capture_traffic.py --port 5401 --output pcap/protocol_binar.pcap
   ```

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 2
```

**Ce să Observați:**
- Eficiența antetului fix față de încadrarea text
- Cum CRC32 detectează coruperea datelor
- Ordinea octeților în rețea (big-endian) pentru câmpuri numerice

---

### Exercițiul 3: Protocol Senzor UDP

**Obiectiv:** Implementați comunicație fără conexiune cu datagrame de dimensiune fixă

**Durată:** 30-40 minute

**Pregătire Wireshark:** Schimbă filtrul la `udp.port == 5402` pentru a observa datagramele.

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
   ```bash
   python3 scripts/start_lab.py --service udp
   
   # Sau mod nativ
   python3 src/apps/udp_sensor_server.py
   ```

2. **Trimiteți citiri de senzor:**
   ```bash
   python3 src/apps/udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Bucuresti"
   ```

3. **Simulați mai mulți senzori:**
   ```bash
   # Trimiteți citiri de la mai mulți senzori
   python3 src/apps/udp_sensor_client.py --sensor-id 1 --temp 22.0 --location "Laborator1"
   python3 src/apps/udp_sensor_client.py --sensor-id 2 --temp 24.5 --location "Laborator2"
   python3 src/apps/udp_sensor_client.py --sensor-id 3 --temp 21.0 --location "Hol"
   ```

4. **Observați caracteristicile UDP:**
   - Fără stabilire de conexiune
   - Fără confirmare de livrare
   - Datagramele pot fi pierdute sau reordonate
   - Overhead mai mic decât TCP

**Verificare:**
```bash
python3 tests/test_exercises.py --exercise 3
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
   ```bash
   python3 scripts/run_demo.py --demo 4
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
```bash
python3 tests/test_exercises.py --exercise 4
```

**Ce să Observați:**
- CRC32 detectează orice eroare de un singur bit
- Detectează majoritatea erorilor de biți multipli
- Nu este potrivit pentru verificări de securitate (nu este hash criptografic)

---

## Demonstrații

### Demo 1: Protocol TEXT

Demonstrație automată a operațiilor protocolului TEXT.

```bash
python3 scripts/run_demo.py --demo 1
```

**Ce să observați:**
- Secvența cerere-răspuns
- Formatul de încadrare cu prefixul de lungime
- Operațiile magazinului cheie-valoare

### Demo 2: Protocol BINAR

Demonstrație a protocolului binar eficient.

```bash
python3 scripts/run_demo.py --demo 2
```

**Ce să observați:**
- Antetul binar compact
- Numerele de secvență pentru urmărire
- Verificarea CRC32 la fiecare mesaj

### Demo 3: Simulare Senzori UDP

Simulare a mai multor senzori IoT care trimit date.

```bash
python3 scripts/run_demo.py --demo 3
```

**Ce să observați:**
- Natura fără conexiune a UDP
- Multiple surse de date
- Dimensiunea fixă a datagramelor

### Demo 4: Detectare Erori CRC32

Demonstrație a detectării coruperii datelor.

```bash
python3 scripts/run_demo.py --demo 4
```

**Ce să observați:**
- Pachete valide acceptate
- Pachete corupte respinse
- Sensibilitatea la schimbări de un singur bit

---

## Capturare și Analiză Pachete

### Capturare Trafic

```bash
# Pornire captură (în terminalul Ubuntu)
python3 scripts/capture_traffic.py --interface eth0 --output pcap/saptamana4_captura.pcap

# Sau folosiți Wireshark direct pe Windows
# Selectați interfața vEthernet (WSL)
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

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT4/04roWSL

# Oprire toate containerele de laborator (Portainer rămâne activ!)
python3 scripts/stop_lab.py

# Verificare oprire - ar trebui să vezi doar portainer
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Eliminare toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/cleanup.py --full

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
```bash
# În WSL/Ubuntu
# Găsiți procesul care folosește portul
sudo ss -tlnp | grep 5400

# Opriți procesul sau folosiți alt port
python3 scripts/stop_lab.py
```

#### Problema: Docker nu pornește
**Soluție:**
```bash
# Porniți serviciul Docker în WSL
sudo service docker start

# Verificați că Docker rulează
docker info
```

#### Problema: Conexiune refuzată la server
**Soluție:**
```bash
# Verificați starea serviciilor
python3 scripts/start_lab.py --status

# Verificați jurnalele containerului
docker logs saptamana4-text
docker logs saptamana4-binar
docker logs saptamana4-senzor
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
│          │     DOCKER ENGINE (WSL2)                                │
│          │                  │                                      │
│   ┌──────┴──────────────────┴───────────────────────────────┐     │
│   │              Containere Laborator                        │     │
│   │                                                          │     │
│   │   ┌───────────┐ ┌───────────┐ ┌───────────────┐        │     │
│   │   │  Server   │ │  Server   │ │    Server     │        │     │
│   │   │   TEXT    │ │   BINAR   │ │  Senzor UDP   │        │     │
│   │   │ TCP:5400  │ │ TCP:5401  │ │   UDP:5402    │        │     │
│   │   └───────────┘ └───────────┘ └───────────────┘        │     │
│   │                                                          │     │
│   │   Rețea: retea_saptamana4                               │     │
│   └──────────────────────────────────────────────────────────┘     │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────┐     │
│   │              Portainer (global)                          │     │
│   │              http://localhost:9000                       │     │
│   └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Depanare Extinsă

### Probleme Docker

**Problemă:** "Cannot connect to Docker daemon"
```bash
# Pornește serviciul Docker în WSL
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status

# Verifică că funcționează
docker ps
```

**Problemă:** Permisiune refuzată la rularea docker
```bash
# Adaugă utilizatorul la grupul docker
sudo usermod -aG docker $USER

# Aplică modificările
newgrp docker

# Sau deconectează-te și reconectează-te din WSL
exit
wsl
```

**Problemă:** Serviciul Docker nu pornește
```bash
# Verifică statusul detaliat
sudo service docker status

# Rulează daemon-ul manual pentru a vedea erorile
sudo dockerd

# Verifică log-urile
sudo cat /var/log/docker.log
```

### Probleme Portainer

**Problemă:** Nu pot accesa http://localhost:9000
```bash
# Verifică dacă containerul Portainer există și rulează
docker ps -a | grep portainer

# Dacă e oprit, pornește-l
docker start portainer

# Dacă nu există, creează-l
docker run -d -p 9000:9000 --name portainer --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data portainer/portainer-ce:latest

# Verifică log-urile
docker logs portainer
```

**Problemă:** Am uitat parola Portainer
```bash
# ATENȚIE: Aceasta resetează Portainer (pierde setările dar NU containerele)
docker stop portainer
docker rm portainer
docker volume rm portainer_data

# Recreează cu comanda de mai sus
# La prima accesare, setează parola nouă: studstudstud
```

### Probleme Wireshark

**Problemă:** Nu se capturează pachete
- ✅ Verifică interfața corectă selectată (vEthernet WSL)
- ✅ Asigură-te că traficul este generat ÎN TIMPUL capturii
- ✅ Verifică că filtrul de afișare nu ascunde pachetele (șterge filtrul)
- ✅ Încearcă "Capture → Options" și activează modul promiscuous

**Problemă:** "No interfaces found" sau eroare de permisiune
- Rulează Wireshark ca Administrator (click dreapta → Run as administrator)
- Reinstalează Npcap cu opțiunea "WinPcap API-compatible Mode" bifată

**Problemă:** Filtrul devine roșu (sintaxă invalidă)
- Verifică ghilimelele și parantezele
- `==` pentru egalitate, nu `=`
- Exemple corecte: `tcp.port == 5400`, `udp.port == 5402`

### Probleme Protocoale

**Problemă:** Protocol TEXT nu răspunde
```bash
# Verifică că serverul rulează
ps aux | grep text_proto_server

# Verifică portul
sudo ss -tlnp | grep 5400

# Verifică log-urile containerului
docker logs saptamana4-text
```

**Problemă:** CRC32 nu se validează corect
```python
# Verificare ordine bytes
# Folosește network byte order (big-endian)
import struct
struct.pack('!I', crc_value)  # '!' = network order
```

**Problemă:** Datagrame UDP nu ajung
```bash
# UDP nu oferă confirmare - trimiteți mai multe
for i in {1..5}; do
    python3 src/apps/udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Test"
done

# Verificați cu Wireshark pe portul 5402
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect retea_saptamana4
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 5400

# Oprește procesul sau folosește alt port
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT4/04roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
docker-compose -f docker/docker-compose.yml down

# Verifică - ar trebui să arate încă portainer
docker ps
# OUTPUT așteptat:
# CONTAINER ID   IMAGE                    NAMES
# abc123...      portainer/portainer-ce   portainer
```

### Sfârșit de Săptămână (Completă)

```bash
# Elimină containerele și rețelele acestei săptămâni
docker-compose -f docker/docker-compose.yml down --volumes

# Elimină imaginile nefolosite
docker image prune -f

# Elimină rețelele nefolosite
docker network prune -f

# Verifică utilizarea discului
docker system df
```

### Resetare Totală (Înainte de Semestru Nou)

```bash
# ATENȚIE: Aceasta elimină TOTUL în afară de Portainer

# Oprește toate containerele EXCEPTÂND Portainer
docker stop $(docker ps -q --filter "name=saptamana")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite  
docker network prune -f

# Verifică că Portainer încă rulează
docker ps
```

**⚠️ NU rula NICIODATĂ `docker system prune -a` fără să excluzi Portainer!**

### Verificare Post-Curățare

```bash
# Verifică ce a rămas
docker ps -a          # Containere
docker images         # Imagini
docker network ls     # Rețele
docker volume ls      # Volume

# Ar trebui să vezi doar:
# - Container: portainer
# - Volum: portainer_data
# - Rețele: bridge, host, none (implicite)
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
