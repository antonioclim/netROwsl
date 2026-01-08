# Săptămâna 9: Nivelul Sesiune și Nivelul Prezentare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică
> 
> de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `09roWSL`

**Arhitectura Mediului:**
```
Windows 11 → WSL2 → Ubuntu 22.04 (implicit) → Docker Engine → Portainer CE
```

**Credențiale Standard:**
| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |
| Server FTP | `test` | `12345` |

---

## 📥 Clonarea Laboratorului Acestei Săptămâni

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 9
git clone https://github.com/antonioclim/netROwsl.git SAPT9
cd SAPT9
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 09roWSL/
cd 09roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT9\
    └── 09roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker
        │   ├── configs/     # Fișiere de configurare
        │   └── volumes/     # Date persistente
        ├── docs/            # Documentație suplimentară
        │   ├── depanare.md
        │   ├── fisa_comenzi.md
        │   ├── lecturi_suplimentare.md
        │   └── sumar_teorie.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/   # tema_9_01, tema_9_02
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # Aplicații suport
        │   ├── exercises/   # ex_9_01, ex_9_02, ftp_demo
        │   └── utils/       # Utilitare rețea
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
cd /mnt/d/RETELE/SAPT9/09roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 9

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **s9_ftp-server** - Server FTP Python (172.29.9.x:2121)
- **s9_client1** - Client de test pentru comanda LIST
- **s9_client2** - Client de test pentru mod pasiv

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

### Vizualizarea Rețelei week9_ftp_network

1. Navighează: **Networks**
2. Click pe **week9_ftp_network**
3. Vezi configurația IPAM: 172.29.9.0/24, gateway 172.29.9.1
4. Vezi toate containerele conectate și IP-urile lor

### Observarea Sesiunilor FTP

În Portainer poți observa sesiunile FTP active:
1. **Containers** → Click pe **s9_ftp-server** → **Logs**
2. Observă conexiunile de la client1 și client2
3. Vezi mesajele de autentificare și comenzile FTP

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a observa fluxul de autentificare FTP
- Pentru analiza conexiunilor de control și date în FTP

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
cd /mnt/d/RETELE/SAPT9/09roWSL

# Pornește mediul de laborator
python3 scripts/porneste_lab.py

# Testează conexiunea FTP
python3 src/exercises/ftp_demo_client.py
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 9

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Trafic FTP:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `ftp` | Tot traficul FTP de control | Analiză generală FTP |
| `ftp.request` | Doar comenzile FTP | Vezi ce trimite clientul |
| `ftp.response` | Doar răspunsurile FTP | Vezi ce returnează serverul |
| `ftp.request.command == "USER"` | Comandă USER | Autentificare - username |
| `ftp.request.command == "PASS"` | Comandă PASS | Autentificare - parolă |
| `ftp.request.command == "LIST"` | Comandă LIST | Listare director |
| `ftp.request.command == "PASV"` | Comandă PASV | Activare mod pasiv |
| `ftp.request.command == "RETR"` | Comandă RETR | Descărcare fișier |
| `ftp.request.command == "STOR"` | Comandă STOR | Încărcare fișier |
| `ftp-data` | Transferuri de date FTP | Date transferate |

**Filtre pentru Coduri de Răspuns FTP:**

| Filtru | Scop | Cod |
|--------|------|-----|
| `ftp.response.code == 220` | Mesaj bun venit | Server ready |
| `ftp.response.code == 331` | Parolă necesară | User OK, need password |
| `ftp.response.code == 230` | Autentificare reușită | Login successful |
| `ftp.response.code == 227` | Mod pasiv | Entering passive mode |
| `ftp.response.code == 226` | Transfer complet | Transfer complete |
| `ftp.response.code == 530` | Autentificare eșuată | Login incorrect |

**Filtre pentru Porturi:**

| Filtru | Scop | Serviciu |
|--------|------|----------|
| `tcp.port == 2121` | Port de control FTP | Comenzi și răspunsuri |
| `tcp.port >= 60000 && tcp.port <= 60010` | Porturi passive | Transfer date |

**Filtre pentru Analiza TCP:**

| Filtru | Scop | Ce să observi |
|--------|------|---------------|
| `tcp.flags.syn == 1` | Pachete SYN | Inițieri conexiuni |
| `tcp.flags.fin == 1` | Pachete FIN | Închidere conexiuni |
| `tcp.stream eq 0` | Primul stream TCP | Conexiune de control |
| `tcp.stream eq 1` | Al doilea stream TCP | Prima conexiune de date |

**Combinarea filtrelor:**
- Autentificare completă: `ftp.request.command == "USER" || ftp.request.command == "PASS" || ftp.response.code == 230`
- Tot traficul FTP: `ftp || ftp-data`
- Doar transfer date: `ftp-data && !ftp`

### Analiza Sesiunii FTP în Wireshark

**Fluxul Tipic de Autentificare FTP:**
1. **220** - Server ready (bun venit)
2. **USER test** - Client trimite username
3. **331** - User OK, need password
4. **PASS 12345** - Client trimite parola
5. **230** - Login successful

**Observarea Modului Pasiv:**
1. **PASV** - Client cere mod pasiv
2. **227 Entering Passive Mode (...)** - Server indică portul
3. Nouă conexiune TCP pe portul indicat
4. Transfer de date pe noua conexiune

### Analiza Protocolului Binar (Exercițiul 1)

Pentru captura conversiei endianness:
1. Aplică filtrul: `tcp.port == 9095` (sau portul folosit)
2. Observă diferențele în reprezentarea binară
3. Compară big-endian vs little-endian în panoul Hex

### Urmărirea unei Conversații FTP Complete

1. Găsește un pachet FTP din conversația pe care vrei să o examinezi
2. Click dreapta → **Follow → TCP Stream**
3. Vei vedea:
   - **Roșu**: Comenzi FTP de la client (USER, PASS, LIST, etc.)
   - **Albastru**: Răspunsuri de la server (220, 331, 230, etc.)
4. Observă fluxul complet al sesiunii

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT9\09roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s9_ftp_auth.pcap` - Autentificare FTP
   - `captura_s9_ftp_pasv.pcap` - Mod pasiv
   - `captura_s9_endianness.pcap` - Conversie binară
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

## Prezentare Generală

Săptămâna 9 explorează nivelurile intermediare ale modelului OSI care fac legătura între nivelul transport (L4) și protocoalele specifice aplicațiilor (L7). Aceste niveluri gestionează **managementul dialogului** (sesiune) și **reprezentarea datelor** (prezentare).

Nivelul Sesiune (L5) asigură stabilirea, menținerea și terminarea conexiunilor logice între aplicații, oferind mecanisme de autentificare, puncte de sincronizare și control al dialogului. Nivelul Prezentare (L6) se ocupă de transformările sintactice ale datelor: serializare, codificare, compresie și criptare.

În cadrul laboratorului, veți implementa un server FTP personalizat, veți analiza protocoale binare cu atenție la ordinea octeților (endianness) și veți testa scenarii multi-client folosind Docker.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** diferențele conceptuale între conexiune TCP și sesiune aplicație
2. **Explicați** rolul nivelurilor L5 și L6 în stiva de protocoale OSI
3. **Implementați** serializare binară utilizând modulul `struct` din Python
4. **Demonstrați** conversii între ordinea octeților (big-endian vs little-endian)
5. **Analizați** fluxul de autentificare și transfer în protocolul FTP
6. **Construiți** un protocol binar personalizat cu header, checksum și payload
7. **Evaluați** diferențele între modurile activ și pasiv în FTP

## Cerințe Preliminare

### Cunoștințe Necesare
- Concepte de bază despre modelul OSI și TCP/IP
- Programare Python (socket-uri, module standard)
- Comenzi Docker de bază
- Familiaritate cu Wireshark

### Cerințe Software
- Windows 10/11 cu WSL2 activat (Ubuntu 22.04)
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git

### Cerințe Hardware
- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT9/09roWSL

# Verifică prerequisitele
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulează instalatorul
python3 setup/instaleaza_prerequisite.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT9/09roWSL

# Pornește toate serviciile
python3 scripts/porneste_lab.py

# Verifică starea serviciilor
python3 scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Server FTP | localhost:2121 | test / 12345 |
| Porturi Passive | 60000-60010 | - |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Codificare Binară și Endianness

**Obiectiv:** Înțelegerea ordinii octeților în transmisia de date în rețea

**Durată estimată:** 30 minute

**Pași:**

1. Deschideți fișierul `src/exercises/ex_9_01_endianness.py`
2. Studiați funcțiile `pack_data()` și `unpack_data()`
3. Rulați scriptul și observați diferențele dintre big-endian și little-endian
4. Modificați valorile și observați efectele asupra reprezentării binare

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

**Ce trebuie observat:**
- Ordinea octeților diferă între arhitecturi
- Protocolele de rețea folosesc întotdeauna big-endian (network byte order)
- Modulul `struct` oferă specificatori pentru ambele ordini

### Exercițiul 2: Implementare Server FTP Personalizat

**Obiectiv:** Implementarea unui protocol de tip FTP cu gestiunea sesiunii

**Durată estimată:** 45 minute

**Pași:**

1. Studiați codul din `src/exercises/ex_9_02_pseudo_ftp.py`
2. Porniți serverul FTP din container
3. Conectați-vă cu clientul și observați fluxul de autentificare
4. Analizați traficul cu Wireshark

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

### Exercițiul 3: Testare Multi-Client

**Obiectiv:** Observarea comportamentului serverului cu clienți concurenți

**Durată estimată:** 30 minute

**Pași:**

1. Porniți mediul Docker complet
2. Observați în Portainer cele două containere client
3. Analizați log-urile pentru a vedea ordinea operațiilor
4. Capturați traficul și identificați sesiunile separate

**Verificare:**
```bash
python3 scripts/ruleaza_demo.py --demo multi_client
```

## Demonstrații

### Demo 1: Conversie Endianness

Demonstrație automată a diferențelor de codificare binară.

```bash
python3 scripts/ruleaza_demo.py --demo endianness
```

**Ce se observă:**
- Aceeași valoare numerică produce secvențe de octeți diferite
- Importanța standardizării pentru interoperabilitate

### Demo 2: Sesiune FTP Completă

Simulare a unui flux complet de autentificare și transfer.

```bash
python3 scripts/ruleaza_demo.py --demo ftp_sesiune
```

**Ce se observă:**
- Schimbul de mesaje USER/PASS
- Răspunsurile serverului (coduri 220, 331, 230)
- Separarea canalelor de control și date

### Demo 3: Protocol Binar Personalizat

Demonstrație a construirii unui protocol cu header, lungime și CRC.

```bash
python3 scripts/ruleaza_demo.py --demo protocol_binar
```

## Capturarea și Analiza Traficului

### Pornirea Capturii

```bash
# Folosind scriptul helper (din WSL)
python3 scripts/captureaza_trafic.py --interfata eth0 --output pcap/saptamana9_captura.pcap

# Sau cu Wireshark direct
# Deschide Wireshark > Selectează interfața vEthernet (WSL) > Pornește captura
```

### Filtre Wireshark Recomandate

```
# Tot traficul FTP de control
ftp

# Doar comenzile FTP
ftp.request

# Doar răspunsurile FTP
ftp.response

# Autentificare
ftp.request.command == "USER" || ftp.request.command == "PASS"

# Transfer de date FTP
ftp-data

# Trafic pe portul de control
tcp.port == 2121
```

## Oprire și Curățare

### La Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT9/09roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verifică oprirea
docker ps
# Ar trebui să vezi doar: portainer
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Elimină toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/curata.py --complet

# Verifică curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Protocol Multi-Format
Implementați un protocol binar care suportă mai multe tipuri de mesaje (TEXT, INTEGER, BLOB) cu header și checksum.

### Tema 2: Mașină de Stări pentru Sesiuni
Implementați o mașină de stări finite pentru gestionarea sesiunilor de tip FTP.

## Depanare

### Probleme Frecvente

#### Problema: Portul 2121 este deja utilizat
**Soluție:** Verificați procesele care folosesc portul și opriți-le:
```bash
# În WSL
ss -tlnp | grep 2121

# Opriți procesul sau modificați portul
```

#### Problema: Containerele nu pornesc
**Soluție:** Verificați log-urile și reconstruiți imaginile:
```bash
docker logs s9_ftp-server
docker compose up -d --build
```

#### Problema: Conexiunea FTP eșuează
**Soluție:** Verificați că serverul este pornit și credențialele sunt corecte:
- Utilizator: `test`
- Parolă: `12345`

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundamente Teoretice

### Nivelul Sesiune (L5)

Nivelul Sesiune gestionează **dialogul logic** între aplicații:

- **Stabilirea sesiunii**: Inițierea comunicării cu autentificare
- **Sincronizare**: Puncte de control pentru reluare după erori
- **Control dialog**: Gestionarea alternării în comunicarea half-duplex
- **Terminare**: Închidere grațioasă cu păstrarea stării

### Nivelul Prezentare (L6)

Nivelul Prezentare se ocupă de **sintaxa datelor**:

- **Serializare**: Convertirea structurilor de date în secvențe de octeți
- **Codificare**: Conversii între seturi de caractere (ASCII, UTF-8)
- **Compresie**: Reducerea dimensiunii datelor
- **Criptare**: Protejarea confidențialității

### Protocolul FTP

FTP folosește **două conexiuni separate**:

1. **Conexiunea de Control** (port 21): Comenzi text, gestiunea sesiunii
2. **Conexiunea de Date** (port 20 sau dinamic): Transferuri de fișiere

```
┌─────────────┐                    ┌─────────────┐
│   Client    │──── Control ───────│   Server    │
│             │     (port 21)      │             │
│             │                    │             │
│             │──── Date ──────────│             │
│             │  (port 20/dinamic) │             │
└─────────────┘                    └─────────────┘
```

### Big-Endian vs Little-Endian

Ordinea octeților (endianness) determină cum sunt stocați octeții unui număr multi-octet:

| Ordine | Descriere | Utilizare |
|--------|-----------|-----------|
| **Big-Endian** | Octetul cel mai semnificativ primul | Protocoale de rețea (Network Byte Order) |
| **Little-Endian** | Octetul cel mai puțin semnificativ primul | Arhitecturi Intel x86/x64 |

Exemplu pentru valoarea `0x12345678`:
- Big-Endian: `12 34 56 78`
- Little-Endian: `78 56 34 12`

## Diagrama Arhitecturii

```
┌────────────────────────────────────────────────────────────────┐
│                    Rețea Docker: week9_ftp_network             │
│                         172.29.9.0/24                          │
│                                                                │
│  ┌──────────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   s9_ftp-server  │  │  s9_client1  │  │  s9_client2  │     │
│  │                  │  │              │  │              │     │
│  │  Port 2121 (FTP) │  │  Test LIST   │  │  Test GET    │     │
│  │  60000-60010     │  │              │  │  Mod Pasiv   │     │
│  │  (passive)       │  │              │  │              │     │
│  └──────────────────┘  └──────────────┘  └──────────────┘     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                              │
                              │ Expunere porturi
                              ▼
┌────────────────────────────────────────────────────────────────┐
│                      Gazdă Windows                             │
│                                                                │
│   localhost:9000 ──► Portainer (administrare globală)          │
│   localhost:2121 ──► Server FTP (control)                      │
│   localhost:60000-60010 ──► Porturi passive FTP                │
│                                                                │
│   Wireshark ──► Captură trafic pe interfața vEthernet (WSL)    │
└────────────────────────────────────────────────────────────────┘
```

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 959: File Transfer Protocol (FTP)
- RFC 4217: Securing FTP with TLS
- Documentația Python struct: https://docs.python.org/3/library/struct.html

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

### Probleme Specifice Săptămânii 9

**Problemă:** Server FTP nu pornește
```bash
# Verifică log-urile serverului FTP
docker logs s9_ftp-server

# Verifică starea de sănătate
docker inspect s9_ftp-server | grep -A 10 Health

# Repornește serverul
docker restart s9_ftp-server
```

**Problemă:** Conexiunea FTP timeout
```bash
# Verifică că portul 2121 este accesibil
nc -zv localhost 2121

# Verifică porturile passive
for i in $(seq 60000 60010); do nc -zv localhost $i 2>&1 | grep succeeded; done

# Verifică configurația de rețea
docker network inspect week9_ftp_network
```

**Problemă:** Client FTP nu se poate conecta
```bash
# Testează manual conexiunea FTP
python3 -c "
from ftplib import FTP
ftp = FTP()
ftp.connect('localhost', 2121)
print(ftp.getwelcome())
ftp.login('test', '12345')
print('Autentificare reușită!')
ftp.quit()
"
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week9_ftp_network

# Verifică DNS în container
docker exec s9_ftp-server cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 2121

# Oprește procesul sau folosește alt port
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT9/09roWSL

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
docker stop $(docker ps -q --filter "name=s9_")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite
docker network prune -f

# Elimină volumele acestei săptămâni
docker volume rm week9_server_files week9_client1_files week9_client2_files

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

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
