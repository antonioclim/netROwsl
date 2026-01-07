# Săptămâna 12: Protocoale de Email (SMTP) și Apel de Procedură la Distanță (RPC)

> Laborator de Rețele de Calculatoare - ASE, Informatică Economică
>
> de Revolvix

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
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau ulterior
- Git (opțional, pentru controlul versiunilor)

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK12_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă există probleme, rulați asistentul de instalare
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
| Server SMTP | localhost:1025 | Fără autentificare |
| Server JSON-RPC | localhost:6200 | Fără autentificare |
| Server XML-RPC | localhost:6201 | Fără autentificare |
| Server gRPC | localhost:6251 | Fără autentificare |

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
   # Din Windows PowerShell sau WSL
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

```powershell
# Într-un terminal separat, înainte de a începe dialogul
python scripts/captura_trafic.py --port 1025 --output pcap/smtp_dialog.pcap --durata 120
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
python tests/test_exercitii.py --exercitiu 1
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
   python src/apps/rpc/jsonrpc/jsonrpc_client.py
   ```

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 2
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
       <methodName>multiply</methodName>
       <params>
         <param><value><int>7</int></value></param>
         <param><value><int>8</int></value></param>
       </params>
     </methodCall>'
   ```

4. Utilizați clientul Python:
   ```bash
   python src/apps/rpc/xmlrpc/xmlrpc_client.py
   ```

**Comparați dimensiunile cererilor/răspunsurilor între JSON-RPC și XML-RPC pentru operații echivalente.**

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Apeluri gRPC cu Protocol Buffers

**Obiectiv:** Efectuarea de apeluri gRPC și examinarea serializării binare

**Durată:** 25-30 minute

**Fundament Teoretic:**

gRPC utilizează Protocol Buffers (protobuf) pentru definirea serviciilor și serializarea mesajelor. Oferă performanță superioară prin serializare binară compactă, siguranța tipurilor la compilare și suport pentru streaming bidirecțional prin HTTP/2.

**Pași:**

1. Examinați definiția serviciului:
   ```bash
   cat src/apps/rpc/grpc/calculator.proto
   ```

2. Rulați clientul gRPC:
   ```bash
   python src/apps/rpc/grpc/grpc_client.py
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
python tests/test_exercitii.py --exercitiu 4
```

---

### Exercițiul 5: Benchmark Comparativ RPC

**Obiectiv:** Măsurarea și compararea performanței celor trei framework-uri RPC

**Durată:** 20-25 minute

**Pași:**

1. Rulați scriptul de benchmark:
   ```bash
   python src/apps/rpc/benchmark_rpc.py
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

```powershell
python scripts/ruleaza_demo.py --demo smtp
```

**Ce să observați:**
- Secvența de comenzi și răspunsuri
- Codurile de stare SMTP
- Stocarea mesajului în directorul spool

### Demo 2: Comparație RPC

```powershell
python scripts/ruleaza_demo.py --demo rpc-compara
```

**Ce să observați:**
- Diferențele de sintaxă între protocoale
- Dimensiunile relative ale mesajelor
- Timpii de răspuns

### Demo 3: Benchmark Complet

```powershell
python scripts/ruleaza_demo.py --demo benchmark
```

**Ce să observați:**
- Graficele de performanță
- Statisticile comparative
- Analiza overhead-ului

---

## Capturarea și Analiza Traficului

### Capturarea Traficului

```powershell
# Capturați tot traficul Week 12 pentru 60 de secunde
python scripts/captura_trafic.py --durata 60 --output pcap/week12_sesiune.pcap

# Sau pentru un protocol specific
python scripts/captura_trafic.py --port 1025 --output pcap/smtp.pcap
python scripts/captura_trafic.py --port 6200 --output pcap/jsonrpc.pcap
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

Consultați directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Client SMTP cu Atașamente MIME
Implementați un client SMTP în Python capabil să trimită emailuri cu atașamente binare folosind codificarea MIME.

### Tema 2: Metodă JSON-RPC Personalizată
Extindeți serverul JSON-RPC cu o metodă `statistici_text` care analizează un șir de caractere.

### Tema 3: Raport de Analiză a Protocoalelor
Realizați o analiză comparativă detaliată a celor patru protocoale folosind capturi Wireshark.

---

## Depanare

### Probleme Frecvente

#### Problema: Portul 1025/6200/6201/6251 este deja ocupat
**Soluție:** Verificați ce proces folosește portul și opriți-l:
```powershell
netstat -ano | findstr :1025
taskkill /PID <pid> /F
```

#### Problema: Docker nu răspunde
**Soluție:** Reporniți Docker Desktop și așteptați inițializarea completă.

#### Problema: Erori de import gRPC
**Soluție:** Regenerați fișierele stub:
```bash
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. calculator.proto
```

Consultați `docs/depanare.md` pentru mai multe soluții.

---

## Fundament Teoretic

### Protocolul SMTP

SMTP (Simple Mail Transfer Protocol, RFC 5321) este protocolul standard pentru transmisia poștei electronice pe Internet. Funcționează pe portul 25 (sau 587 pentru submission, 465 pentru SMTPS), folosind un dialog bazat pe text în care clientul trimite comenzi iar serverul răspunde cu coduri numerice pe trei cifre:
- 2xx: Succes
- 3xx: Mai sunt necesare date
- 4xx: Eroare temporară
- 5xx: Eroare permanentă

### Remote Procedure Call (RPC)

RPC este o paradigmă de comunicare în sistemele distribuite care permite unui program să execute o procedură pe un alt sistem ca și cum ar fi locală. Abstractizează complexitatea comunicării în rețea, oferind programatorilor un model de programare familiar.

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
```

---

*Laborator de Rețele de Calculatoare - ASE, Informatică Economică | de Revolvix*
