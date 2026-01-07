# Sumar Teoretic

> Laborator Săptămâna 13 - IoT și Securitate în Rețelele de Calculatoare
>
> Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

---

## Cuprins

1. [Arhitectura IoT](#arhitectura-iot)
2. [Protocolul MQTT](#protocolul-mqtt)
3. [Securitatea TLS](#securitatea-tls)
4. [Scanarea Porturilor](#scanarea-porturilor)
5. [OWASP IoT Top 10](#owasp-iot-top-10)
6. [Măsuri Defensive](#măsuri-defensive)

---

## Arhitectura IoT

### Straturile Sistemelor IoT

Sistemele Internet of Things se structurează tipic în patru straturi funcționale:

**1. Stratul de Percepție (Edge Layer)**
- Senzori: temperatură, umiditate, presiune, mișcare
- Actuatoare: motoare, valve, LED-uri
- Caracteristici: consum redus, resurse limitate, comunicație intermitentă

**2. Stratul de Rețea (Network Layer)**
- Protocoale de comunicație: MQTT, CoAP, AMQP, HTTP/REST
- Tehnologii wireless: WiFi, Bluetooth, Zigbee, LoRa, NB-IoT
- Gateway-uri pentru traducere între protocoale

**3. Stratul de Procesare (Processing Layer)**
- Agregare și filtrare date
- Analiză în timp real (streaming analytics)
- Stocare în cloud sau edge computing
- Machine learning pentru predicții

**4. Stratul Aplicație (Application Layer)**
- Dashboard-uri și vizualizări
- Sisteme de alertare și notificare
- Automatizări și reguli de business
- API-uri pentru integrare

### Provocări de Securitate în IoT

- **Resurse limitate:** Dispozitivele au CPU, memorie și energie limitate pentru criptografie
- **Heterogenitate:** Varietate mare de protocoale și standarde
- **Scalabilitate:** Milioane de dispozitive de gestionat
- **Acces fizic:** Dispozitivele pot fi compromise fizic
- **Actualizări:** Dificultate în aplicarea patch-urilor de securitate

---

## Protocolul MQTT

### Prezentare Generală

MQTT (Message Queuing Telemetry Transport) este un protocol de mesagerie lightweight, proiectat inițial de IBM pentru monitorizarea conductelor de petrol prin satelit.

**Caracteristici principale:**
- Protocol publish/subscribe
- Header minimal de 2 bytes
- Suport pentru conexiuni nesigure și lentețe mare
- Ideal pentru dispozitive cu resurse limitate

### Modelul Publish/Subscribe

```
┌──────────────┐          ┌──────────────┐          ┌──────────────┐
│   Publisher  │──────────│    Broker    │──────────│  Subscriber  │
│   (Senzor)   │ PUBLISH  │   (MQTT)     │ DELIVER  │  (Aplicație) │
└──────────────┘          └──────────────┘          └──────────────┘
                                │
                          Gestionează
                          Topicuri
```

**Avantaje față de client/server:**
- Decuplare spațială: publisherii nu cunosc subscriberii
- Decuplare temporală: mesajele pot fi reținute
- Scalabilitate: broker-ul gestionează distribuția

### Structura Topicurilor

Topicurile MQTT sunt organizate ierarhic, folosind "/" ca separator:

```
senzori/
├── temperatura/
│   ├── camera1
│   ├── camera2
│   └── exterior
├── umiditate/
│   └── sera
└── miscare/
    └── intrare
```

**Wildcards:**
- `+` (plus): înlocuiește un singur nivel
  - `senzori/+/camera1` → se potrivește cu `senzori/temperatura/camera1`
- `#` (hash): înlocuiește oricâte niveluri (doar la final)
  - `senzori/#` → se potrivește cu toate topicurile sub `senzori/`

### Niveluri QoS (Quality of Service)

| QoS | Nume | Garanție | Utilizare |
|-----|------|----------|-----------|
| 0 | At most once | Fără confirmare, posibilă pierdere | Telemetrie frecventă, pierderi acceptabile |
| 1 | At least once | Confirmare ACK, posibile duplicate | Alertări, date importante |
| 2 | Exactly once | Protocol în 4 pași, garantat o dată | Comenzi critice, tranzacții |

**Fluxul QoS 2:**
```
Publisher          Broker          Subscriber
    │                │                │
    │──PUBLISH──────>│                │
    │<──PUBREC───────│                │
    │──PUBREL──────>│──PUBLISH──────>│
    │<──PUBCOMP──────│<──PUBACK───────│
```

### Mesaje Reținute și Last Will

**Mesaje Reținute:**
- Broker-ul păstrează ultimul mesaj pentru un topic
- Noii subscriberi primesc imediat ultima valoare

**Last Will and Testament (LWT):**
- Mesaj configurat la conectare
- Publicat automat de broker dacă clientul se deconectează neașteptat
- Util pentru detectarea dispozitivelor offline

---

## Securitatea TLS

### Transport Layer Security

TLS protejează comunicațiile prin trei mecanisme:

**1. Confidențialitate (Criptare)**
- Algoritmi simetrici: AES-256-GCM, ChaCha20
- Datele sunt criptate în tranzit
- Doar părțile autorizate pot decripta

**2. Integritate (HMAC)**
- Hash-uri criptografice pentru detectarea modificărilor
- Orice alterare a datelor este detectată
- Protecție împotriva atacurilor man-in-the-middle

**3. Autenticitate (Certificate)**
- Certificate X.509 pentru verificarea identității
- Lanț de încredere către CA (Certificate Authority)
- Previne impersonarea serverului

### Handshake TLS 1.3

```
Client                                    Server
   │                                        │
   │────── Client Hello ──────────────────>│
   │       (versiuni suportate,            │
   │        cipher suites, random)          │
   │                                        │
   │<───── Server Hello ───────────────────│
   │       (versiune selectată,            │
   │        certificat, parametri DH)       │
   │                                        │
   │────── Client Finished ───────────────>│
   │       (verificare, cheie partajată)   │
   │                                        │
   │<───── Server Finished ────────────────│
   │                                        │
   │<═══════ Date Criptate ═══════════════>│
```

### Ce Protejează TLS și Ce Nu

**Protejează:**
- Conținutul mesajelor
- Credențialele de autentificare
- Integritatea datelor

**NU Protejează:**
- Metadate (dimensiuni pachete, timing)
- Adrese IP sursă/destinație
- Faptul că are loc o comunicație

---

## Scanarea Porturilor

### Tehnici de Scanare TCP

**1. TCP Connect Scan**
```
Atacator          Țintă
    │──SYN──────>│
    │<─SYN/ACK──│  (Port DESCHIS)
    │──ACK──────>│
    │──RST──────>│  (Închide conexiunea)
```
- Conexiune completă three-way handshake
- Detectabilă în loguri
- Nu necesită privilegii speciale

**2. TCP SYN Scan (Half-Open)**
```
Atacator          Țintă
    │──SYN──────>│
    │<─SYN/ACK──│  (Port DESCHIS)
    │──RST──────>│  (Nu finalizează)
```
- Nu completează handshake-ul
- Mai greu de detectat
- Necesită drepturi root/administrator

**3. TCP FIN/NULL/XMAS Scans**
- Exploatează comportamentul RFC 793
- Porturile închise răspund cu RST
- Porturile deschise nu răspund
- Utile pentru evaziune firewall

### Identificarea Serviciilor (Banner Grabbing)

După ce un port este identificat ca deschis, se poate obține banner-ul serviciului:

```python
# Exemplu banner grabbing
sock.connect((host, port))
banner = sock.recv(1024)  # "220 (vsFTPd 2.3.4)"
```

**Informații obținute:**
- Tipul serviciului
- Versiunea software
- Configurația (uneori)
- Vulnerabilități potențiale

---

## OWASP IoT Top 10

OWASP (Open Web Application Security Project) menține o listă cu cele mai frecvente vulnerabilități IoT:

| # | Vulnerabilitate | Descriere |
|---|----------------|-----------|
| 1 | Parole slabe | Credențiale implicite sau ușor de ghicit |
| 2 | Servicii de rețea nesecure | Porturi deschise inutil, protocoale nesigure |
| 3 | Interfețe ecosistem nesecure | API-uri, cloud, aplicații mobile vulnerabile |
| 4 | Lipsa mecanismului de actualizare | Nu există mod de a aplica patch-uri |
| 5 | Componente nesigure sau învechite | Software cu vulnerabilități cunoscute |
| 6 | Protecție insuficientă a intimității | Date personale expuse sau colectate inutil |
| 7 | Transfer și stocare nesecure | Date necriptate în tranzit sau în repaus |
| 8 | Lipsa managementului dispozitivelor | Nu se știe ce dispozitive există în rețea |
| 9 | Setări implicite nesecure | Configurații care sacrifică securitatea |
| 10 | Lipsa hardening-ului fizic | Acces fizic la porturi de debug, memorie |

---

## Măsuri Defensive

### Segmentarea Rețelei

```
┌─────────────────────────────────────────────────────────┐
│                    Rețea Corporativă                    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │ VLAN IoT    │  │ VLAN Intern │  │ VLAN DMZ    │     │
│  │ (izolat)    │  │ (birou)     │  │ (servere)   │     │
│  │             │  │             │  │             │     │
│  │ ○ Senzori   │  │ ○ Laptopuri │  │ ○ Web       │     │
│  │ ○ Camere    │  │ ○ Telefoane │  │ ○ Mail      │     │
│  │             │  │             │  │             │     │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘     │
│         │                │                │             │
│         └────────────────┼────────────────┘             │
│                          │                              │
│                    ┌─────┴─────┐                        │
│                    │ Firewall  │                        │
│                    └───────────┘                        │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Cele Mai Bune Practici

**Autentificare și Autorizare:**
- Schimbați credențialele implicite
- Implementați autentificare puternică
- Aplicați principiul privilegiului minim

**Criptare:**
- TLS pentru toate comunicațiile
- Criptare date în repaus
- Gestionare corectă a cheilor

**Monitorizare:**
- Logging centralizat
- Detectare anomalii
- Alertare în timp real

**Actualizări:**
- Proces de patch management
- Actualizări firmware over-the-air (OTA)
- Verificare integritate update-uri

---

## Referințe

1. MQTT Version 5.0 Specification - https://mqtt.org/mqtt-specification/
2. OWASP IoT Top 10 - https://owasp.org/www-project-internet-of-things/
3. NIST Special Publication 800-183: Networks of 'Things'
4. RFC 793 - Transmission Control Protocol

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix*
