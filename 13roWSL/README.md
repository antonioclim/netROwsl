# Săptămâna 13: IoT și Securitate în Rețelele de Calculatoare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator Rețele de Calculatoare
>
> de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `13roWSL`

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

# Clonează Săptămâna 13
git clone https://github.com/antonioclim/netROwsl.git SAPT13
cd SAPT13
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 13roWSL/
cd 13roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT13\
    └── 13roWSL\
        ├── artifacts/       # Rezultate generate (capturi, rapoarte)
        ├── docker/          # Configurație Docker
        │   ├── configs/     # Configurații servicii
        │   │   ├── certs/   # Certificate TLS pentru MQTT
        │   │   └── mosquitto/  # Configurație broker MQTT
        │   └── volumes/     # Date persistente
        ├── docs/            # Documentație suplimentară
        │   ├── cheatsheet_comenzi.md
        │   ├── depanare.md
        │   └── sumar_teorie.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # Aplicații demonstrative IoT
        │   │   ├── controler_iot.py
        │   │   ├── senzor_iot.py
        │   │   └── verificare_backdoor_ftp.py
        │   └── exercises/   # Exerciții laborator
        │       ├── ex_13_01_scanner_porturi.py
        │       ├── ex_13_02_client_mqtt.py
        │       ├── ex_13_03_sniffer_pachete.py
        │       └── ex_13_04_verificator_vulnerabilitati.py
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
cd /mnt/d/RETELE/SAPT13/13roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 13

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **week13_mosquitto** - Broker MQTT (10.0.13.100)
- **week13_dvwa** - Aplicație Web Vulnerabilă (10.0.13.11)
- **week13_vsftpd** - Server FTP cu backdoor simulat (10.0.13.12)

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

### Vizualizarea Rețelei week13net

1. Navighează: **Networks**
2. Click pe **week13net**
3. Vezi configurația IPAM: 10.0.13.0/24, gateway 10.0.13.1
4. Vezi containerele conectate cu IP-urile lor:
   - mosquitto: 10.0.13.100
   - dvwa: 10.0.13.11
   - vsftpd: 10.0.13.12

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a compara traficul MQTT în clar vs. criptat TLS
- Pentru analiza traficului FTP și detectarea backdoor-ului

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
cd /mnt/d/RETELE/SAPT13/13roWSL

# Pornește mediul de laborator
python3 scripts/porneste_lab.py

# Testează MQTT
python3 src/exercises/ex_13_02_client_mqtt.py --mode publish --topic "test" --message "hello"
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 13

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Trafic MQTT:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 1883` | MQTT text clar | Vezi mesajele necriptate |
| `tcp.port == 8883` | MQTT TLS | Vezi traficul criptat |
| `mqtt` | Protocol MQTT | Doar pachete MQTT |
| `mqtt.msgtype == 3` | MQTT PUBLISH | Mesaje publicate |
| `mqtt.msgtype == 8` | MQTT SUBSCRIBE | Abonamente la topicuri |
| `mqtt.topic contains "senzor"` | Topic specific | Filtrează după topic |

**Filtre pentru Trafic HTTP/Web (DVWA):**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 8080` | Trafic DVWA | Tot traficul web |
| `tcp.port == 8080 && http` | HTTP DVWA | Doar HTTP |
| `http.request.method == "POST"` | Cereri POST | Autentificare, formulare |
| `http.request.uri contains "login"` | Pagini login | Analiză autentificare |
| `http.response.code >= 400` | Erori HTTP | Probleme acces |

**Filtre pentru Trafic FTP:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 2121` | Trafic FTP | Conexiuni FTP |
| `ftp` | Protocol FTP | Comenzi și răspunsuri FTP |
| `ftp.request.command == "USER"` | Autentificare | Vezi utilizatori |
| `ftp.request.command == "PASS"` | Parole | ⚠️ Parole în clar! |
| `tcp.port == 6200` | Backdoor simulat | Conexiuni backdoor |

**Filtre pentru Scanare Porturi:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN | Scanări noi |
| `tcp.flags.rst == 1` | RST (port închis) | Porturi închise |
| `tcp.analysis.flags` | Anomalii TCP | Probleme rețea |

**Filtre pentru Rețeaua Laboratorului:**

| Filtru | Scop | Container |
|--------|------|-----------|
| `ip.addr == 10.0.13.100` | Broker MQTT | week13_mosquitto |
| `ip.addr == 10.0.13.11` | DVWA | week13_dvwa |
| `ip.addr == 10.0.13.12` | FTP/Backdoor | week13_vsftpd |
| `ip.addr == 10.0.13.0/24` | Toată rețeaua | Toate containerele |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 1883 && mqtt.msgtype == 3`
- SAU: `tcp.port == 1883 || tcp.port == 8883`
- NU: `!arp && !icmp`

### Analiza Comparativă: MQTT Text Clar vs. TLS

1. **Captură pe portul 1883** (text clar):
   - Poți vedea conținutul mesajelor MQTT
   - Topic-urile sunt vizibile
   - Payload-ul este în clar

2. **Captură pe portul 8883** (TLS):
   - Traficul apare ca "TLS Application Data"
   - Conținutul este complet criptat
   - Doar metadatele TLS sunt vizibile

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP, RST |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT13\13roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s13_mqtt_clar.pcap` - MQTT necriptat
   - `captura_s13_mqtt_tls.pcap` - MQTT criptat
   - `captura_s13_scanare.pcap` - Scanare porturi
   - `captura_s13_ftp.pcap` - Trafic FTP
4. Format: Wireshark/pcap sau pcapng (implicit)

---

## ⚠️ Avertisment de Securitate

> **ATENȚIE:** Acest laborator conține servicii **INTENȚIONAT VULNERABILE** pentru scopuri educaționale.
>
> - **NU** expuneți aceste servicii la internet
> - **NU** utilizați tehnicile învățate pe sisteme fără autorizare explicită
> - **Scanarea porturilor și testarea vulnerabilităților pe sisteme neautorizate este ILEGALĂ**
>
> Utilizați doar în mediul de laborator izolat!

---

## Prezentare Generală

Această sesiune de laborator explorează intersecția critică dintre tehnologiile **Internet of Things (IoT)** și **securitatea rețelelor**. Veți examina protocoalele de comunicație specifice IoT, în special MQTT (Message Queuing Telemetry Transport), și veți înțelege atât capabilitățile cât și vulnerabilitățile inerente dispozitivelor conectate.

Componenta practică vă introduce în tehnicile fundamentale de evaluare a securității: scanarea porturilor pentru descoperirea serviciilor, analiza traficului pentru identificarea protocoalelor și verificarea vulnerabilităților pentru evaluarea posturii de securitate. Aceste competențe formează baza auditului profesional de securitate și a testării de penetrare.

Mediul de laborator include servicii intenționat vulnerabile (DVWA, vsftpd cu simulare de backdoor) într-un mediu Docker izolat. Această configurație controlată permite explorarea în siguranță a conceptelor de securitate fără a afecta sistemele de producție.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele arhitecturii IoT și protocoalele de comunicație asociate
2. **Explicați** mecanismele de funcționare ale protocolului MQTT, inclusiv nivelurile QoS și structura topicurilor
3. **Implementați** un scanner de porturi TCP folosind programare concurentă în Python
4. **Demonstrați** comunicația MQTT securizată folosind criptare TLS
5. **Analizați** traficul de rețea pentru a distinge între comunicații în text clar și cele criptate
6. **Evaluați** postura de securitate a serviciilor de rețea folosind tehnici de verificare a vulnerabilităților

## Cerințe Preliminare

### Cunoștințe Necesare
- Fundamentele programării socket în Python (TCP/UDP)
- Înțelegerea modelului de referință OSI și stiva TCP/IP
- Cunoașterea de bază a containerizării Docker
- Familiaritate cu analiza pachetelor în Wireshark

### Cerințe Software

| Software | Versiune | Scop |
|----------|---------|------|
| Windows 10/11 | 21H2+ | Sistem de operare gazdă |
| WSL2 | Ubuntu 22.04+ | Mediu de execuție Linux |
| Docker Engine | 24.0+ | Rulare containere (în WSL) |
| Portainer CE | 2.19+ | Management vizual Docker (port 9000) |
| Python | 3.11+ | Execuție scripturi |
| Wireshark | 4.0+ | Analiză pachete |
| Git | 2.40+ | Control versiuni (opțional) |

### Cerințe Hardware
- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT13/13roWSL

# Verifică cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulează asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT13/13roWSL

# Pornește toate serviciile
python3 scripts/porneste_lab.py

# Verifică starea
python3 scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale/Descriere |
|----------|----------|----------------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Mosquitto MQTT (text clar) | localhost:1883 | Fără autentificare |
| Mosquitto MQTT (TLS) | localhost:8883 | Fără autentificare |
| DVWA | http://localhost:8080 | admin / password |
| vsftpd FTP | localhost:2121 | acces anonim |
| Backdoor simulat | localhost:6200 | doar pentru exerciții |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Scanner de Porturi TCP

**Obiectiv:** Implementați și utilizați un scanner de porturi pentru a descoperi serviciile active din rețea

**Durată:** 25-30 minute

**Context Teoretic:**
Scanarea porturilor reprezintă tehnica fundamentală de recunoaștere în securitatea rețelelor. Prin trimiterea de pachete SYN către porturi țintă și analizarea răspunsurilor, putem determina:
- **Port deschis:** Serviciu activ, acceptă conexiuni (primește SYN-ACK)
- **Port închis:** Niciun serviciu, dar host-ul răspunde (primește RST)
- **Port filtrat:** Firewall blochează pachetele (timeout sau ICMP unreachable)

**Pași:**

1. **Examinați codul scannerului:**
   ```bash
   # În terminalul Ubuntu
   cat src/exercises/ex_13_01_scanner_porturi.py
   ```

2. **Rulați o scanare de bază:**
   ```bash
   # Scanați serviciile laboratorului
   python3 src/exercises/ex_13_01_scanner_porturi.py --target localhost --ports 1883,8883,8080,2121,6200
   ```

3. **Scanați un interval de porturi:**
   ```bash
   # Scanați porturile comune
   python3 src/exercises/ex_13_01_scanner_porturi.py --target localhost --ports 1-1024 --threads 50
   ```

4. **Exportați rezultatele în JSON:**
   ```bash
   python3 src/exercises/ex_13_01_scanner_porturi.py --target localhost --ports 1883,8883,8080,2121,6200 --output artifacts/scanare_lab.json
   ```

**Rezultate Așteptate:**
```
[SCANARE] Țintă: localhost
[DESCHIS] Port 1883 - Banner: (mosquitto)
[DESCHIS] Port 2121 - Banner: 220 (vsFTPd 2.3.4)
[DESCHIS] Port 6200 - Conectat (niciun banner)
[DESCHIS] Port 8080 - Banner: HTTP/1.1 200 OK
[DESCHIS] Port 8883 - Conectat (TLS)
[INFO] Scanare completă: 5 porturi deschise găsite
```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

---

### Exercițiul 2: Client MQTT cu Suport TLS

**Obiectiv:** Demonstrați comunicația IoT folosind protocolul MQTT, comparând traficul în text clar cu cel criptat

**Durată:** 30-35 minute

**Context Teoretic:**
MQTT (Message Queuing Telemetry Transport) este protocolul dominant în domeniul IoT datorită:
- **Amprentă minimă:** Header de doar 2 bytes, ideal pentru dispozitive constrânse
- **Model publish/subscribe:** Decuplare completă între producători și consumatori
- **Niveluri QoS:** Garanții de livrare configurabile (0=cel mult o dată, 1=cel puțin o dată, 2=exact o dată)
- **Topicuri ierarhice:** Organizare logică cu wildcard-uri (+ pentru un nivel, # pentru mai multe)

**Pași:**

1. **Porniți un subscriber în terminal separat:**
   ```bash
   # Terminal 1: Subscriber pe topic senzor
   python3 src/exercises/ex_13_02_client_mqtt.py --mode subscribe --topic "senzori/temperatura/#" --broker localhost --port 1883
   ```

2. **Publicați mesaje de la un alt terminal:**
   ```bash
   # Terminal 2: Publisher
   python3 src/exercises/ex_13_02_client_mqtt.py --mode publish --topic "senzori/temperatura/camera1" --message "23.5" --broker localhost --port 1883
   ```

3. **Observați mesajele în terminal-ul subscriber**

4. **Repetați cu conexiune TLS:**
   ```bash
   # Terminal 1: Subscriber TLS
   python3 src/exercises/ex_13_02_client_mqtt.py --mode subscribe --topic "senzori/#" --broker localhost --port 8883 --tls --ca-cert docker/configs/certs/ca.crt

   # Terminal 2: Publisher TLS
   python3 src/exercises/ex_13_02_client_mqtt.py --mode publish --topic "senzori/umiditate/living" --message "65" --broker localhost --port 8883 --tls --ca-cert docker/configs/certs/ca.crt
   ```

5. **Capturați și comparați traficul:**
   ```bash
   # Într-un terminal separat, porniți captura
   python3 scripts/capteaza_trafic.py --durata 60 --output pcap/mqtt_comparatie.pcap
   ```

**Rezultate Așteptate:**
- Subscriber-ul primește mesajele publicate în timp real
- În Wireshark, traficul pe portul 1883 arată conținutul mesajelor în text clar
- Traficul pe portul 8883 apare complet criptat (TLS Application Data)

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

---

### Exercițiul 3: Analizor de Pachete (Packet Sniffer)

**Obiectiv:** Capturați și analizați traficul de rețea pentru identificarea protocoalelor și extragerea informațiilor

**Durată:** 20-25 minute

**Context Teoretic:**
Analiza pachetelor (packet sniffing) permite inspectarea datagramelor la nivel de octeți. Folosind biblioteca Scapy, putem:
- Captura pachete în timp real de pe interfețe de rețea
- Diseca straturile protocolare (Ethernet → IP → TCP/UDP → Application)
- Filtra după criterii specifice (port sursă/destinație, adrese IP, flags TCP)
- Reconstrui fluxuri de comunicație

**Pași:**

1. **Rulați sniffer-ul de bază:**
   ```bash
   # Capturați 20 de pachete pe toate interfețele
   sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --count 20
   ```

2. **Filtrați după port:**
   ```bash
   # Capturați doar trafic MQTT
   sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --port 1883 --count 10
   ```

3. **Afișați detalii despre pachete:**
   ```bash
   # Mod verbose
   sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --port 1883 --verbose --count 5
   ```

4. **Salvați captura:**
   ```bash
   sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --count 50 --output pcap/sniffer_captura.pcap
   ```

**Notă:** Scapy necesită privilegii de administrator (sudo) pentru captură.

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Verificator de Vulnerabilități

**Obiectiv:** Evaluați postura de securitate a serviciilor folosind verificări automate

**Durată:** 30-35 minute

**Context Teoretic:**
Verificarea vulnerabilităților implică testarea sistematică a serviciilor pentru:
- Configurări nesigure (porturi expuse, autentificare dezactivată)
- Versiuni software vulnerabile (CVE-uri cunoscute)
- Protocoale nesigure (text clar vs. criptat)

**Pași:**

1. **Rulați verificarea completă:**
   ```bash
   python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost
   ```

2. **Verificați servicii specifice:**
   ```bash
   # Doar MQTT
   python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --service mqtt
   
   # Doar FTP
   python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --service ftp
   ```

3. **Generați raport JSON:**
   ```bash
   python3 src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --output artifacts/raport_vulnerabilitati.json
   ```

4. **Testați backdoor-ul FTP simulat:**
   ```bash
   python3 src/apps/verificare_backdoor_ftp.py --host localhost --port 2121
   ```

**Rezultate Așteptate:**
```
[VERIFICARE] Țintă: localhost
[AVERTISMENT] MQTT pe 1883: Autentificare DEZACTIVATĂ
[OK] MQTT pe 8883: TLS activ
[CRITICAL] FTP pe 2121: Banner indică versiune vulnerabilă (vsftpd 2.3.4)
[CRITICAL] Port 6200: Backdoor detectat!
[OK] DVWA pe 8080: Aplicație funcțională (vulnerabilă by design)
```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

---

## Demonstrații

### Demo 1: Comunicație IoT End-to-End

```bash
python3 scripts/ruleaza_demo.py --demo 1
```

**Ce să observați:**
- Senzorul virtual publică date periodic
- Controlerul primește și procesează datele
- Traficul este vizibil în Wireshark (port 1883)

### Demo 2: Comparație Securitate MQTT

```bash
python3 scripts/ruleaza_demo.py --demo 2
```

**Ce să observați:**
- Același mesaj trimis pe ambele porturi (1883 și 8883)
- Diferența vizibilă în Wireshark
- Importanța criptării pentru date sensibile

### Demo 3: Exploatare Backdoor FTP

```bash
python3 scripts/ruleaza_demo.py --demo 3
```

**Ce să observați:**
- Cum funcționează vulnerabilitatea CVE-2011-2523
- De ce versiunile software trebuie actualizate
- Importanța auditului de securitate

---

## Capturarea și Analiza Traficului

### Capturarea Traficului

```bash
# Pornire captură cu durată specificată
python3 scripts/capteaza_trafic.py --durata 120 --output pcap/sesiune_laborator.pcap

# Sau folosiți Wireshark direct
# Deschideți Wireshark > Selectați interfața vEthernet (WSL)
```

### Filtre Wireshark Recomandate

```
# Trafic MQTT text clar
tcp.port == 1883

# Trafic MQTT criptat
tcp.port == 8883

# Trafic HTTP către DVWA
tcp.port == 8080 and http

# Trafic FTP
tcp.port == 2121

# Conexiuni TCP noi (doar SYN)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Toate serviciile laboratorului
tcp.port in {1883, 8883, 8080, 2121, 6200}

# Mesaje MQTT PUBLISH
mqtt.msgtype == 3

# Erori TCP (retransmisiuni, RST)
tcp.analysis.flags
```

---

## Oprirea și Curățarea

### La Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT13/13roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verifică oprire - ar trebui să vezi doar portainer
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Elimină toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/curata.py --complet

# Verifică curățarea
docker system df
```

---

## Teme pentru Acasă

Consultați directorul `homework/` pentru exerciții suplimentare.

### Tema 1: Scanner de Porturi Extins
Extindeți scanner-ul cu detecție a sistemului de operare și fingerprinting al serviciilor.
**Termen:** Înainte de următoarea sesiune de laborator

### Tema 2: Raport de Securitate MQTT
Redactați un raport de 2 pagini despre cele mai bune practici de securitate pentru implementările MQTT în medii IoT industriale.
**Termen:** Două săptămâni

---

## Context Teoretic

### Arhitectura IoT

Sistemele IoT se structurează tipic în patru straturi:

1. **Stratul de Percepție:** Senzori și actuatoare care colectează date din mediul fizic
2. **Stratul de Rețea:** Protocoale de comunicație (MQTT, CoAP, AMQP, HTTP)
3. **Stratul de Procesare:** Agregare date, analiză, stocare în cloud
4. **Stratul Aplicație:** Interfețe utilizator, dashboard-uri, sisteme de alertare

### Protocolul MQTT

MQTT folosește un model **publish/subscribe** mediat de un **broker**:

```
[Senzor] --publish--> [Broker MQTT] --deliver--> [Aplicație]
    |                      |                          |
    +-- topic: temp/sala1  +-- înregistrare topic    +-- subscribe: temp/#
```

**Niveluri Quality of Service (QoS):**
- **QoS 0:** "Fire and forget" - nicio confirmare, posibilă pierdere
- **QoS 1:** "At least once" - confirmare ACK, posibile duplicate
- **QoS 2:** "Exactly once" - protocol în 4 pași, garantat fără duplicate

### TLS în IoT

Transport Layer Security protejează comunicațiile prin:
- **Confidențialitate:** Criptare simetrică (AES-256-GCM)
- **Integritate:** HMAC pentru detectarea modificărilor
- **Autenticitate:** Certificate X.509 pentru verificarea identității

**Atenție:** TLS protejează conținutul, dar metadatele (dimensiune pachete, timing, adrese IP) rămân vizibile!

### Scanarea Porturilor

Tehnici de scanare TCP:
- **TCP Connect:** Conexiune completă three-way handshake (detectabilă)
- **TCP SYN:** Half-open scan, trimite doar SYN (necesită privilegii root)
- **TCP FIN/NULL/XMAS:** Stealth scans, exploatează comportamentul RFC

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- OWASP. (2018). *OWASP IoT Top 10*. https://owasp.org/www-project-internet-of-things/
- MQTT.org. (2019). *MQTT Version 5.0 Specification*. https://mqtt.org/mqtt-specification/

---

## Diagramă Arhitectură

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEEK13_WSLkit - Topologie Rețea                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                    Rețea Docker: week13net                       │   │
│   │                    Subnet: 10.0.13.0/24                          │   │
│   │                                                                  │   │
│   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │   │
│   │   │   Mosquitto     │  │     DVWA        │  │    vsftpd       │ │   │
│   │   │   (MQTT Broker) │  │  (Web Vulnerabil)│  │  (FTP Server)   │ │   │
│   │   │                 │  │                 │  │                 │ │   │
│   │   │  10.0.13.100    │  │   10.0.13.11    │  │   10.0.13.12    │ │   │
│   │   │                 │  │                 │  │                 │ │   │
│   │   │  Port 1883 ─────┼──┼─ Port 8080 ─────┼──┼─ Port 2121 ─────┼─┼───┼─► Host
│   │   │  (text clar)    │  │  (HTTP)         │  │  (FTP)          │ │   │
│   │   │                 │  │                 │  │                 │ │   │
│   │   │  Port 8883 ─────┼──┼─────────────────┼──┼─ Port 6200 ─────┼─┼───┼─► Host
│   │   │  (TLS)          │  │                 │  │  (backdoor)     │ │   │
│   │   └─────────────────┘  └─────────────────┘  └─────────────────┘ │   │
│   │                                                                  │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                      │                                   │
│                                      ▼                                   │
│   ┌─────────────────────────────────────────────────────────────────┐   │
│   │                     Host Windows (WSL2)                          │   │
│   │                                                                  │   │
│   │   Python Scripts    │    Wireshark    │    Docker Engine         │   │
│   │   (src/exercises/)  │    (Analiză)    │    (Container Runtime)   │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
│   Portainer (Management Vizual): http://localhost:9000                  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
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

**Problemă:** Nu văd traficul containerelor Docker
- Selectează interfața `vEthernet (WSL)`, nu `Ethernet` sau `Wi-Fi`
- Asigură-te că containerele sunt pe rețea bridge, nu host

### Probleme Specifice Săptămânii 13

**Problemă:** Containerele Docker nu pornesc
```bash
# Verifică log-urile pentru fiecare container
docker logs week13_mosquitto
docker logs week13_dvwa
docker logs week13_vsftpd

# Verifică dacă porturile sunt ocupate
sudo ss -tlnp | grep -E "1883|8883|8080|2121|6200"
```

**Problemă:** Erori de certificat TLS pentru MQTT
```bash
# Regenerați certificatele
python3 setup/configureaza_docker.py --regen-certs

# Verificați că folosiți calea corectă către ca.crt
ls -la docker/configs/certs/

# Verificați permisiunile fișierelor de certificat
chmod 644 docker/configs/certs/*.crt
chmod 600 docker/configs/certs/*.key
```

**Problemă:** Scapy nu capturează pachete
```bash
# Scapy necesită privilegii root
sudo python3 src/exercises/ex_13_03_sniffer_pachete.py --count 10

# Verifică interfețele disponibile
python3 -c "from scapy.all import *; print(get_if_list())"

# În WSL, interfața corectă este de obicei "eth0"
```

**Problemă:** DVWA afișează eroare la autentificare
```bash
# Repornește containerul DVWA
docker restart week13_dvwa

# Așteaptă inițializarea
sleep 10

# Verifică jurnalele
docker logs week13_dvwa

# Accesează http://localhost:8080/setup.php pentru a reinițializa baza de date
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week13net

# Verifică DNS în container
docker exec week13_mosquitto cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul
sudo ss -tlnp | grep 1883

# Oprește procesul sau modificați porturile în fișierul .env
cat .env
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT13/13roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verifică - ar trebui să vezi doar portainer
docker ps
```

### Sfârșit de Săptămână (Completă)

```bash
# Curățare completă laborator
python3 scripts/curata.py --complet

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
docker stop $(docker ps -q --filter "name=week13_")

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

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
