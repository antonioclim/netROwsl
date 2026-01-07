# Săptămâna 13: IoT și Securitate în Rețelele de Calculatoare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator Rețele de Calculatoare
>
> de Revolvix

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
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git (opțional, pentru controlul versiunilor)

### Cerințe Hardware
- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK13_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/porneste_lab.py

# Verificați că totul rulează
python scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Mosquitto MQTT (text clar) | localhost:1883 | Fără autentificare |
| Mosquitto MQTT (TLS) | localhost:8883 | Fără autentificare |
| DVWA | http://localhost:8080 | admin / password |
| vsftpd FTP | localhost:2121 | acces anonim |

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
   ```powershell
   # Deschideți fișierul pentru analiză
   code src/exercises/ex_13_01_scanner_porturi.py
   ```

2. **Rulați o scanare de bază:**
   ```powershell
   # Scanați serviciile laboratorului
   python src/exercises/ex_13_01_scanner_porturi.py --target localhost --ports 1883,8883,8080,2121,6200
   ```

3. **Scanați un interval de porturi:**
   ```powershell
   # Scanați porturile comune
   python src/exercises/ex_13_01_scanner_porturi.py --target localhost --ports 1-1024 --threads 50
   ```

4. **Exportați rezultatele în JSON:**
   ```powershell
   python src/exercises/ex_13_01_scanner_porturi.py --target localhost --ports 1883,8883,8080,2121,6200 --output artifacts/scanare_lab.json
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
```powershell
python tests/test_exercitii.py --exercitiu 1
```

---

### Exercițiul 2: Client MQTT cu Suport TLS

**Obiectiv:** Demonstrați comunicația IoT folosind protocolul MQTT, comparând traficul în text clar cu cel criptat

**Durată:** 30-35 minute

**Context Teoretic:**
MQTT (Message Queuing Telemetry Transport) este protocolul dominant în ecosistemul IoT datorită:
- **Amprentă minimă:** Header de doar 2 bytes, ideal pentru dispozitive constrânse
- **Model publish/subscribe:** Decuplare completă între producători și consumatori
- **Niveluri QoS:** Garanții de livrare configurabile (0=cel mult o dată, 1=cel puțin o dată, 2=exact o dată)
- **Topicuri ierarhice:** Organizare logică cu wildcard-uri (+ pentru un nivel, # pentru mai multe)

**Pași:**

1. **Porniți un subscriber în terminal separat:**
   ```powershell
   # Terminal 1: Subscriber pe topic senzor
   python src/exercises/ex_13_02_client_mqtt.py --mode subscribe --topic "senzori/temperatura/#" --broker localhost --port 1883
   ```

2. **Publicați mesaje de la un alt terminal:**
   ```powershell
   # Terminal 2: Publisher
   python src/exercises/ex_13_02_client_mqtt.py --mode publish --topic "senzori/temperatura/camera1" --message "23.5" --broker localhost --port 1883
   ```

3. **Observați mesajele în terminal-ul subscriber**

4. **Repetați cu conexiune TLS:**
   ```powershell
   # Terminal 1: Subscriber TLS
   python src/exercises/ex_13_02_client_mqtt.py --mode subscribe --topic "senzori/#" --broker localhost --port 8883 --tls --ca-cert docker/configs/certs/ca.crt

   # Terminal 2: Publisher TLS
   python src/exercises/ex_13_02_client_mqtt.py --mode publish --topic "senzori/umiditate/living" --message "65" --broker localhost --port 8883 --tls --ca-cert docker/configs/certs/ca.crt
   ```

5. **Capturați și comparați traficul:**
   ```powershell
   # Într-un terminal separat, porniți captura
   python scripts/capteaza_trafic.py --durata 60 --output pcap/mqtt_comparatie.pcap
   ```

**Rezultate Așteptate:**
- Subscriber-ul primește mesajele publicate în timp real
- În Wireshark, traficul pe portul 1883 arată conținutul mesajelor în text clar
- Traficul pe portul 8883 apare complet criptat (TLS Application Data)

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 2
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
   ```powershell
   # Capturați 20 de pachete pe toate interfețele
   python src/exercises/ex_13_03_sniffer_pachete.py --count 20
   ```

2. **Filtrați după port:**
   ```powershell
   # Capturați doar trafic MQTT
   python src/exercises/ex_13_03_sniffer_pachete.py --filter "tcp port 1883" --count 50
   ```

3. **În paralel, generați trafic MQTT** (din alt terminal):
   ```powershell
   python src/exercises/ex_13_02_client_mqtt.py --mode publish --topic "test/sniffer" --message "Mesaj de test pentru captură" --broker localhost --port 1883
   ```

4. **Salvați captura pentru analiză ulterioară:**
   ```powershell
   python src/exercises/ex_13_03_sniffer_pachete.py --filter "tcp port 1883 or tcp port 8080" --output pcap/analiza_protocoale.pcap --count 100
   ```

**Rezultate Așteptate:**
```
[CAPTURĂ] Interfață: eth0 | Filtru: tcp port 1883
[PKT 001] TCP 172.20.0.1:54321 -> 172.20.0.100:1883 [SYN] Seq=0
[PKT 002] TCP 172.20.0.100:1883 -> 172.20.0.1:54321 [SYN,ACK] Seq=0 Ack=1
[PKT 003] TCP 172.20.0.1:54321 -> 172.20.0.100:1883 [ACK] Seq=1 Ack=1
[PKT 004] MQTT CONNECT ClientId='python-mqtt-client'
[PKT 005] MQTT CONNACK Return=0 (Accepted)
[PKT 006] MQTT PUBLISH Topic='test/sniffer' QoS=0
```

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Verificator de Vulnerabilități

**Obiectiv:** Evaluați postura de securitate a serviciilor de rețea folosind verificări automate

**Durată:** 25-30 minute

**Context Teoretic:**
Evaluarea vulnerabilităților implică verificarea sistematică a serviciilor pentru:
- **Configurații nesigure:** Porturi deschise inutil, servicii expuse
- **Versiuni vulnerabile:** Software cu CVE-uri cunoscute
- **Acces neautentificat:** Servicii fără protecție prin parolă
- **Transmisie în text clar:** Date sensibile necriptate

**Pași:**

1. **Rulați verificarea completă:**
   ```powershell
   python src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --all
   ```

2. **Verificați doar serviciul FTP:**
   ```powershell
   python src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --ftp --port 2121
   ```

3. **Verificați DVWA:**
   ```powershell
   python src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --http --port 8080
   ```

4. **Verificați broker-ul MQTT:**
   ```powershell
   python src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --mqtt --port 1883
   ```

5. **Generați raport detaliat:**
   ```powershell
   python src/exercises/ex_13_04_verificator_vulnerabilitati.py --target localhost --all --output artifacts/raport_vulnerabilitati.json
   ```

**Rezultate Așteptate:**
```
╔══════════════════════════════════════════════════════════════╗
║           RAPORT VERIFICARE VULNERABILITĂȚI                  ║
╠══════════════════════════════════════════════════════════════╣
║ Țintă: localhost                                             ║
║ Data: 2026-01-07 12:00:00                                    ║
╠══════════════════════════════════════════════════════════════╣
║ [CRITIC] FTP (2121): vsftpd 2.3.4 - versiune vulnerabilă     ║
║          CVE-2011-2523: Backdoor în codul sursă              ║
║ [RIDICAT] FTP: Acces anonim activat                          ║
║ [CRITIC] MQTT (1883): Broker fără autentificare              ║
║ [MEDIU]  MQTT: Trafic în text clar (lipsă TLS)               ║
║ [CRITIC] HTTP (8080): DVWA - aplicație vulnerabilă           ║
║          Detectat: SQL Injection, XSS, CSRF posibile         ║
╠══════════════════════════════════════════════════════════════╣
║ Sumar: 3 CRITICE | 1 RIDICAT | 1 MEDIU | 0 SCĂZUT            ║
╚══════════════════════════════════════════════════════════════╝
```

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 4
```

---

## Demonstrații

### Demo 1: Pipeline Complet de Recunoaștere

Demonstrație automată care prezintă fluxul complet de evaluare a securității.

```powershell
python scripts/ruleaza_demo.py --demo 1
```

**Ce să observați:**
- Descoperirea serviciilor prin scanare de porturi
- Identificarea versiunilor prin banner grabbing
- Detectarea configurațiilor vulnerabile
- Generarea raportului final

### Demo 2: Comparație Trafic Text Clar vs TLS

Demonstrație side-by-side a diferenței dintre comunicația necriptată și cea securizată.

```powershell
python scripts/ruleaza_demo.py --demo 2
```

**Ce să observați:**
- Mesajele MQTT vizibile în captura pe portul 1883
- Trafic complet opac pe portul 8883 (TLS)
- Metadata expusă chiar și cu TLS (dimensiuni pachete, timing)

### Demo 3: Recunoaștere și Detecție Backdoor

Demonstrație a tehnicilor de fingerprinting și detecție a amenințărilor.

```powershell
python scripts/ruleaza_demo.py --demo 3
```

**Ce să observați:**
- Identificarea serviciilor prin răspunsurile banner
- Detectarea portului 6200 (simulare backdoor vsftpd)
- Raportare structurată a descoperirilor

---

## Capturarea și Analiza Traficului

### Capturarea Traficului

```powershell
# Pornire captură cu durată specificată
python scripts/capteaza_trafic.py --durata 120 --output pcap/sesiune_laborator.pcap

# Sau folosiți Wireshark direct
# Deschideți Wireshark > Selectați interfața Docker
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

### Sfârșitul Sesiunii

```powershell
# Opriți toate containerele (păstrează datele)
python scripts/opreste_lab.py

# Verificați oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python scripts/curata.py --complet

# Verificați curățarea
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

## Depanare

### Probleme Frecvente

#### Problema: Containerele Docker nu pornesc
**Simptome:** Eroare "Cannot connect to Docker daemon"
**Soluție:**
1. Verificați că Docker Desktop rulează
2. Verificați că backend-ul WSL2 este activat în setările Docker Desktop
3. Reporniți Docker Desktop
4. Rulați `wsl --shutdown` și reporniți

#### Problema: Erori de certificat TLS pentru MQTT
**Simptome:** "SSL: CERTIFICATE_VERIFY_FAILED"
**Soluție:**
1. Regenerați certificatele: `python setup/configureaza_docker.py --regen-certs`
2. Verificați că folosiți calea corectă către `ca.crt`
3. Verificați permisiunile fișierelor de certificat

#### Problema: Porturile sunt deja ocupate
**Simptome:** "Address already in use"
**Soluție:**
1. Identificați procesul: `netstat -ano | findstr :PORT`
2. Opriți procesul sau modificați porturile în fișierul `.env`
3. Verificați că nu există containere din sesiuni anterioare: `docker ps -a`

#### Problema: Scapy nu capturează pachete
**Simptome:** "Permission denied" sau listă goală de pachete
**Soluție:**
1. Rulați ca Administrator în Windows
2. În WSL, folosiți `sudo`
3. Verificați interfața de rețea corectă cu `--list-interfaces`

Consultați `docs/depanare.md` pentru mai multe soluții.

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
│   │   Python Scripts    │    Wireshark    │    Docker Desktop        │   │
│   │   (src/exercises/)  │    (Analiză)    │    (Container Runtime)   │   │
│   └─────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

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

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
