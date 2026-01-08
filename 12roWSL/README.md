# Săptămâna 12: Protocoale de Email (SMTP) și Apel de Procedură la Distanță (RPC)

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică
>
> de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `12roWSL`

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

# Clonează Săptămâna 12
git clone https://github.com/antonioclim/netROwsl.git SAPT12
cd SAPT12
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 12roWSL/
cd 12roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT12\
    └── 12roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker
        │   └── volumes/     # Volume pentru email spool
        ├── docs/            # Documentație suplimentară
        │   ├── depanare.md
        │   ├── fisa_comenzi.md
        │   ├── lecturi_suplimentare.md
        │   └── rezumat_teorie.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # Aplicații demonstrative
        │   │   ├── email/   # smtp_client.py, smtp_server.py
        │   │   └── rpc/     # jsonrpc/, xmlrpc/, grpc/
        │   ├── exercises/   # ex_01_smtp, ex_02_rpc
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
cd /mnt/d/RETELE/SAPT12/12roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 12

Navighează: **Home → local → Containers**

Vei vedea containerul specific laboratorului:
- **week12_lab** - Container principal (172.28.12.10) cu toate serverele:
  - SMTP pe portul 1025
  - JSON-RPC pe portul 6200
  - XML-RPC pe portul 6201
  - gRPC pe portul 6251

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

### Vizualizarea Rețelei week12_net

1. Navighează: **Networks**
2. Click pe **week12_net**
3. Vezi configurația IPAM: 172.28.12.0/24, gateway 172.28.12.1
4. Vezi containerul week12_lab conectat cu IP-ul său

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a compara dimensiunile payload-urilor între JSON-RPC, XML-RPC și gRPC
- Pentru a observa dialogul SMTP în clar

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
cd /mnt/d/RETELE/SAPT12/12roWSL

# Pornește mediul de laborator
python3 scripts/porneste_lab.py

# Testează SMTP
nc localhost 1025
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 12

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Trafic SMTP:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 1025` | Tot traficul SMTP | Analiză generală SMTP |
| `smtp` | Protocol SMTP | Vezi comenzi și răspunsuri |
| `smtp.req.command` | Comenzi SMTP | Vezi HELO, MAIL FROM, etc. |
| `smtp.req.command == "MAIL"` | Comanda MAIL FROM | Inițiere tranzacție |
| `smtp.req.command == "DATA"` | Comanda DATA | Conținut mesaj |
| `smtp.response.code` | Coduri răspuns | Toate răspunsurile |
| `smtp.response.code >= 400` | Erori SMTP | Probleme (4xx, 5xx) |
| `smtp.response.code == 250` | Succes SMTP | Comenzi reușite |

**Filtre pentru Trafic RPC:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 6200` | JSON-RPC | Trafic JSON-RPC |
| `tcp.port == 6201` | XML-RPC | Trafic XML-RPC |
| `tcp.port == 6251` | gRPC | Trafic gRPC (HTTP/2) |
| `http` | Tot HTTP | JSON-RPC și XML-RPC |
| `http.request.method == "POST"` | Cereri RPC | Apeluri către servere |
| `http contains "jsonrpc"` | Conținut JSON-RPC | Filtrează JSON-RPC |
| `http contains "methodCall"` | Conținut XML-RPC | Filtrează XML-RPC |
| `http2` | HTTP/2 | gRPC (protocol binar) |
| `http2.header.name == ":path"` | Căi gRPC | Metodele apelate |

**Filtre pentru Rețeaua Laboratorului:**

| Filtru | Scop | Container |
|--------|------|-----------|
| `ip.addr == 172.28.12.10` | Container lab | week12_lab |
| `ip.addr == 172.28.12.0/24` | Toată rețeaua | Toate containerele |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 6200 && http`
- SAU: `tcp.port == 1025 || tcp.port == 6200`
- NU: `!arp && !icmp`

### Analiza Comparativă a Protocoalelor RPC

1. Capturează trafic pentru JSON-RPC, XML-RPC și gRPC
2. Compară dimensiunile pachetelor:
   - JSON-RPC: compact, text lizibil
   - XML-RPC: mai mare, text verbose
   - gRPC: foarte compact, binar (Protocol Buffers)
3. Observă overhead-ul HTTP vs HTTP/2

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT12\12roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s12_smtp.pcap` - Dialog SMTP
   - `captura_s12_jsonrpc.pcap` - Trafic JSON-RPC
   - `captura_s12_xmlrpc.pcap` - Trafic XML-RPC
   - `captura_s12_grpc.pcap` - Trafic gRPC
4. Format: Wireshark/pcap sau pcapng (implicit)

---

## Prezentare Generală

Această sesiune de laborator explorează două paradigme fundamentale ale comunicației la nivelul aplicației: protocoalele de poștă electronică și mecanismele de apel de procedură la distanță (RPC). Protocolul SMTP (Simple Mail Transfer Protocol) stă la baza infrastructurii globale de email, permițând transferul fiabil de mesaje între servere de poștă electronică prin intermediul unor dialoguri bazate pe text, ușor de înțeles de către om.

Apelul de procedură la distanță reprezintă o abstracție puternică care permite programelor să invoce funcții pe sisteme aflate la distanță ca și cum acestea ar fi apeluri locale. Vom examina trei implementări distincte ale RPC: JSON-RPC 2.0 (ușor și bazat pe text), XML-RPC (predecesorul SOAP cu tipare de date bogate) și gRPC (framework modern de înaltă performanță ce utilizează Protocol Buffers pentru serializare binară).

Prin exerciții practice cu aceste protocoale, veți dobândi experiență directă atât cu formatele de mesaje citibile de om, cât și cu cele binare eficiente, înțelegând compromisurile între simplitate, performanță și siguranța tipurilor în sistemele distribuite.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele unei tranzacții SMTP și să recunoașteți comenzile și răspunsurile standard ale protocolului
2. **Explicați** diferențele arhitecturale dintre JSON-RPC, XML-RPC și gRPC, inclusiv metodele de serializare și protocoalele de transport
3. **Implementați** dialoguri SMTP folosind netcat și să verificați livrarea mesajelor prin examinarea cutiilor poștale
4. **Demonstrați** apeluri RPC folosind toate cele trei framework-uri, inclusiv tratarea erorilor și invocări în lot (batch)
5. **Analizați** traficul de rețea în Wireshark pentru a compara dimensiunile payload-urilor și overhead-ul protocoalelor
6. **Evaluați** adecvarea diferitelor protocoale RPC pentru diverse scenarii de aplicații pe baza cerințelor de performanță

## Cerințe Preliminare

### Cunoștințe Necesare
- Modelul client-server și comunicarea bazată pe socket-uri (Săptămânile 2-3)
- Concepte HTTP și structura cerere/răspuns (Săptămânile 8, 10)
- Bazele Docker și Docker Compose (Săptămânile 10-11)
- Fundamentele analizei de pachete cu Wireshark (Săptămâna 1)

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
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT12/12roWSL

# Verifică cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulează asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT12/12roWSL

# Pornește toate serviciile
python3 scripts/porneste_lab.py

# Verifică starea
python3 scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Descriere |
|----------|----------|-----------|
| Portainer | http://localhost:9000 | Management Docker |
| Server SMTP | localhost:1025 | Server SMTP educațional |
| Server JSON-RPC | http://localhost:6200 | JSON-RPC 2.0 |
| Server XML-RPC | http://localhost:6201 | XML-RPC cu introspecție |
| Server gRPC | localhost:6251 | gRPC (HTTP/2 + Protocol Buffers) |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Dialog SMTP Manual

**Obiectiv:** Realizarea unui dialog SMTP complet folosind netcat pentru a înțelege mecanismul protocolului

**Durată:** 30-40 minute

**Fundament Teoretic:**

SMTP utilizează un model cerere-răspuns bazat pe text, unde clientul trimite comenzi, iar serverul răspunde cu coduri de stare pe trei cifre. Fazele principale sunt:
- **Stabilirea conexiunii:** Serverul trimite banner-ul de salut (cod 220)
- **Identificare:** Clientul se prezintă cu HELO sau EHLO
- **Tranzacția mail:** MAIL FROM, RCPT TO, DATA
- **Terminare:** QUIT închide conexiunea

**Pași:**

1. Deschideți un terminal și conectați-vă la serverul SMTP:
   ```bash
   # Din terminalul Ubuntu WSL
   nc localhost 1025
   ```

2. Observați banner-ul de salut al serverului (răspuns 220)

3. Trimiteți comanda HELO:
   ```
   HELO client.local
   ```
   Așteptați răspunsul 250

4. Inițiați o tranzacție de email:
   ```
   MAIL FROM:<expeditor@exemplu.ro>
   RCPT TO:<destinatar@exemplu.ro>
   DATA
   ```

5. Introduceți conținutul mesajului (terminat cu o linie conținând doar un punct):
   ```
   Subject: Test SMTP din Laborator
   From: expeditor@exemplu.ro
   To: destinatar@exemplu.ro

   Acesta este corpul mesajului de test.
   Trimis manual prin dialog SMTP.
   .
   ```

6. Verificați mesajele stocate folosind comanda nestandardă LIST:
   ```
   LIST
   ```

7. Încheiați sesiunea:
   ```
   QUIT
   ```

**Captură de Trafic:**

```bash
# Într-un terminal separat, înainte de a începe dialogul
python3 scripts/captura_trafic.py --port 1025 --output pcap/smtp_dialog.pcap --durata 120
```

**Filtre Wireshark Sugerate:**
```
tcp.port == 1025
smtp
smtp.req.command == "MAIL"
smtp.response.code >= 500
```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

---

### Exercițiul 2: Apeluri JSON-RPC 2.0

**Obiectiv:** Efectuarea de apeluri JSON-RPC singulare și în lot, cu tratare de erori

**Durată:** 25-30 minute

**Fundament Teoretic:**

JSON-RPC 2.0 definește un protocol ușor pentru apeluri de procedură la distanță folosind JSON ca format de date. Fiecare cerere conține:
- `jsonrpc`: Versiunea protocolului ("2.0")
- `method`: Numele metodei de apelat
- `params`: Parametrii (array sau obiect)
- `id`: Identificator unic pentru corelarea răspunsurilor

**Pași:**

1. Testați un apel simplu folosind curl:
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"add","params":[10,20],"id":1}'
   ```

2. Testați apeluri cu parametri numiți:
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"subtract","params":{"a":100,"b":42},"id":2}'
   ```

3. Executați un apel în lot (batch):
   ```bash
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '[
       {"jsonrpc":"2.0","method":"add","params":[1,2],"id":1},
       {"jsonrpc":"2.0","method":"multiply","params":[3,4],"id":2},
       {"jsonrpc":"2.0","method":"get_time","id":3}
     ]'
   ```

4. Provocați și observați erori:
   ```bash
   # Metodă inexistentă (cod eroare -32601)
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"metoda_inexistenta","id":4}'
   
   # Parametri invalizi (cod eroare -32602)
   curl -X POST http://localhost:6200 \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"divide","params":[10,0],"id":5}'
   ```

5. Utilizați clientul Python pentru teste suplimentare:
   ```bash
   python3 src/apps/rpc/jsonrpc/jsonrpc_client.py
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

---

### Exercițiul 3: Apeluri XML-RPC cu Introspecție

**Obiectiv:** Utilizarea XML-RPC și explorarea capacităților de introspecție

**Durată:** 20-25 minute

**Fundament Teoretic:**

XML-RPC folosește XML pentru codificarea apelurilor și HTTP ca transport. Oferă tipuri de date bogate (int, double, string, array, struct, base64, datetime) și suportă introspecția — capacitatea de a descoperi metodele disponibile la runtime.

**Pași:**

1. Listați metodele disponibile:
   ```bash
   curl -X POST http://localhost:6201 \
     -H "Content-Type: text/xml" \
     -d '<?xml version="1.0"?>
     <methodCall>
       <methodName>system.listMethods</methodName>
     </methodCall>'
   ```

2. Obțineți ajutor pentru o metodă:
   ```bash
   curl -X POST http://localhost:6201 \
     -H "Content-Type: text/xml" \
     -d '<?xml version="1.0"?>
     <methodCall>
       <methodName>system.methodHelp</methodName>
       <params><param><value><string>add</string></value></param></params>
     </methodCall>'
   ```

3. Efectuați un apel de calcul:
   ```bash
   curl -X POST http://localhost:6201 \
     -H "Content-Type: text/xml" \
     -d '<?xml version="1.0"?>
     <methodCall>
       <methodName>add</methodName>
       <params>
         <param><value><int>15</int></value></param>
         <param><value><int>27</int></value></param>
       </params>
     </methodCall>'
   ```

4. Utilizați clientul Python pentru teste suplimentare:
   ```bash
   python3 src/apps/rpc/xmlrpc/xmlrpc_client.py
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Apeluri gRPC cu Protocol Buffers

**Obiectiv:** Utilizarea gRPC și înțelegerea serializării binare cu Protocol Buffers

**Durată:** 25-30 minute

**Fundament Teoretic:**

gRPC utilizează Protocol Buffers (protobuf) pentru serializarea datelor, oferind:
- Serializare binară compactă
- Definirea strictă a schemei (.proto)
- Generare automată de cod client/server
- Transport eficient peste HTTP/2

**Pași:**

1. Examinați definiția serviciului:
   ```bash
   cat src/apps/rpc/grpc/calculator.proto
   ```

2. Rulați clientul gRPC:
   ```bash
   python3 src/apps/rpc/grpc/grpc_client.py
   ```

3. Observați în Wireshark diferența de dimensiune a payload-ului comparativ cu JSON/XML:
   ```
   tcp.port == 6251
   http2
   ```

4. Testați metodele disponibile:
   - `Add(a, b)` — Adunare
   - `Subtract(a, b)` — Scădere
   - `Multiply(a, b)` — Înmulțire
   - `Divide(a, b)` — Împărțire
   - `Echo(message)` — Ecou
   - `Sha256Hash(data)` — Hash SHA-256
   - `GetStats()` — Statistici server

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

---

### Exercițiul 5: Benchmark Comparativ RPC

**Obiectiv:** Măsurarea și compararea performanței celor trei framework-uri RPC

**Durată:** 20-25 minute

**Pași:**

1. Rulați scriptul de benchmark:
   ```bash
   python3 src/apps/rpc/benchmark_rpc.py
   ```

2. Analizați rezultatele:
   - Latența medie per apel
   - Throughput (cereri/secundă)
   - Dimensiunea medie a mesajelor

3. Documentați observațiile:
   - Care protocol are cel mai mic overhead?
   - Care este cel mai rapid pentru apeluri simple?
   - Cum se comportă fiecare la apeluri în lot?

**Rezultate Așteptate (orientative):**
| Protocol | Cereri/secundă | Latență medie |
|----------|----------------|---------------|
| JSON-RPC | 500-2000 | 0.5-2ms |
| XML-RPC | 300-1500 | 0.7-3ms |
| gRPC | 1000-5000 | 0.2-1ms |

*Valorile pot varia în funcție de hardware și configurație.*

---

## Demonstrații

### Demo 1: Dialog SMTP Complet

```bash
python3 scripts/ruleaza_demo.py --demo smtp
```

**Ce să observați:**
- Secvența de comenzi și răspunsuri
- Codurile de stare SMTP
- Stocarea mesajului în directorul spool

### Demo 2: Comparație RPC

```bash
python3 scripts/ruleaza_demo.py --demo rpc-compara
```

**Ce să observați:**
- Diferențele de sintaxă între protocoale
- Dimensiunile relative ale mesajelor
- Timpii de răspuns

### Demo 3: Benchmark Complet

```bash
python3 scripts/ruleaza_demo.py --demo benchmark
```

**Ce să observați:**
- Graficele de performanță
- Statisticile comparative
- Analiza overhead-ului

---

## Capturarea și Analiza Traficului

### Capturarea Traficului

```bash
# Capturați tot traficul Week 12 pentru 60 de secunde
python3 scripts/captura_trafic.py --durata 60 --output pcap/week12_sesiune.pcap

# Sau pentru un protocol specific
python3 scripts/captura_trafic.py --port 1025 --output pcap/smtp.pcap
python3 scripts/captura_trafic.py --port 6200 --output pcap/jsonrpc.pcap
```

### Filtre Wireshark Sugerate

```
# SMTP
tcp.port == 1025
smtp.req.command
smtp.response.code >= 400

# JSON-RPC și XML-RPC (HTTP)
tcp.port == 6200 or tcp.port == 6201
http.request.method == "POST"
http contains "jsonrpc"
http contains "methodCall"

# gRPC (HTTP/2)
tcp.port == 6251
http2
http2.header.name == ":path"
```

---

## Oprire și Curățare

### La Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT12/12roWSL

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

Consultați directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Client SMTP cu Atașamente MIME
Implementați un client SMTP în Python capabil să trimită emailuri cu atașamente binare folosind codificarea MIME.

### Tema 2: Metodă JSON-RPC Personalizată
Extindeți serverul JSON-RPC cu o metodă `statistici_text` care analizează un șir de caractere.

### Tema 3: Raport de Analiză a Protocoalelor
Realizați o analiză comparativă detaliată a celor patru protocoale folosind capturi Wireshark.

---

## Fundament Teoretic

### Protocolul SMTP

SMTP (Simple Mail Transfer Protocol, RFC 5321) este protocolul standard pentru transmisia poștei electronice pe Internet. Funcționează pe portul 25 (sau 587 pentru submission, 465 pentru SMTPS), folosind un dialog bazat pe text în care clientul trimite comenzi iar serverul răspunde cu coduri numerice pe trei cifre:
- 2xx: Succes
- 3xx: Mai sunt necesare date
- 4xx: Eroare temporară
- 5xx: Eroare permanentă

### Remote Procedure Call (RPC)

RPC este o paradigmă de comunicare în sistemele distribuite care permite unui program să execute o procedură pe un alt sistem ca și cum ar fi locală. Abstractizează complexitatea comunicației în rețea, oferind programatorilor un model de programare familiar.

### Comparație JSON-RPC vs XML-RPC vs gRPC

| Caracteristică | JSON-RPC | XML-RPC | gRPC |
|----------------|----------|---------|------|
| Format date | JSON | XML | Protocol Buffers |
| Transport | HTTP/WebSocket | HTTP | HTTP/2 |
| Tipare date | Dinamic | Static | Static (compilat) |
| Dimensiune payload | Mic | Mare | Foarte mic |
| Citibil de om | Da | Da | Nu |
| Streaming | Nu | Nu | Da |
| Batching | Da | Nu | Da |

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 5321 - Simple Mail Transfer Protocol
- RFC 2045-2049 - Multipurpose Internet Mail Extensions (MIME)
- JSON-RPC 2.0 Specification (https://www.jsonrpc.org/specification)
- gRPC Documentation (https://grpc.io/docs/)

---

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker: week12_lab                           │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │ Server SMTP  │ │  JSON-RPC    │ │   XML-RPC    │ │    gRPC    │  │
│  │    :1025     │ │    :6200     │ │    :6201     │ │   :6251    │  │
│  │              │ │   HTTP/1.1   │ │   HTTP/1.1   │ │   HTTP/2   │  │
│  │  Text-based  │ │     JSON     │ │     XML      │ │  Protobuf  │  │
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘  │
│                                                                     │
│                    Rețea: 172.28.12.0/24 (week12_net)               │
└─────────────────────────────────────────────────────────────────────┘
         │                  │                │               │
         ▼                  ▼                ▼               ▼
    ┌─────────┐        ┌─────────┐      ┌─────────┐    ┌──────────┐
    │ netcat  │        │  curl   │      │  curl   │    │  Client  │
    │ telnet  │        │ Python  │      │ Python  │    │  Python  │
    └─────────┘        └─────────┘      └─────────┘    └──────────┘
      Client             Client           Client          Client

    Portainer (global): http://localhost:9000
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

### Probleme Specifice Săptămânii 12

**Problemă:** Portul 1025/6200/6201/6251 este deja ocupat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 1025

# Sau verifică toate porturile laboratorului
for port in 1025 6200 6201 6251; do
  echo "Port $port:"
  sudo ss -tlnp | grep $port
done

# Oprește procesul sau folosește alt port în configurație
```

**Problemă:** Erori de import gRPC
```bash
# Instalează pachetele necesare
pip install grpcio grpcio-tools --break-system-packages

# Regenerează fișierele stub
cd src/apps/rpc/grpc
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

**Problemă:** Serverele nu pornesc în container
```bash
# Verifică log-urile containerului
docker logs week12_lab

# Accesează consola containerului
docker exec -it week12_lab bash

# Verifică procesele
ps aux | grep python
```

**Problemă:** Dialog SMTP nu funcționează
```bash
# Verifică că serverul SMTP răspunde
nc -zv localhost 1025

# Testează manual
nc localhost 1025
# Apoi tastează: HELO test
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week12_net

# Verifică DNS în container
docker exec week12_lab cat /etc/resolv.conf
```

**Problemă:** Erori de conectivitate între servicii
```bash
# Verifică că toate serviciile răspund
curl http://localhost:6200  # JSON-RPC
curl http://localhost:6201  # XML-RPC
nc -zv localhost 6251       # gRPC
nc -zv localhost 1025       # SMTP
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT12/12roWSL

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
docker stop $(docker ps -q --filter "name=week12_")

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

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
