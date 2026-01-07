# Săptămâna 9: Nivelul Sesiune și Nivelul Prezentare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică
> 
> de Revolvix

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
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau versiune ulterioară
- Git

### Cerințe Hardware
- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```powershell
# Deschide PowerShell ca Administrator
cd WEEK9_WSLkit_RO

# Verifică prerequisitele
python setup/verifica_mediu.py

# Dacă apar probleme, rulează instalatorul
python setup/instaleaza_prerequisite.py
```

### Pornirea Laboratorului

```powershell
# Pornește toate serviciile
python scripts/porneste_lab.py

# Verifică starea serviciilor
python scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Server FTP | localhost:2121 | test / 12345 |
| Porturi Passive | 60000-60010 | - |

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
python tests/test_exercitii.py --exercitiu 1
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
python tests/test_exercitii.py --exercitiu 2
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
python scripts/ruleaza_demo.py --demo multi_client
```

## Demonstrații

### Demo 1: Conversie Endianness

Demonstrație automată a diferențelor de codificare binară.

```powershell
python scripts/ruleaza_demo.py --demo endianness
```

**Ce se observă:**
- Aceeași valoare numerică produce secvențe de octeți diferite
- Importanța standardizării pentru interoperabilitate

### Demo 2: Sesiune FTP Completă

Simulare a unui flux complet de autentificare și transfer.

```powershell
python scripts/ruleaza_demo.py --demo ftp_sesiune
```

**Ce se observă:**
- Schimbul de mesaje USER/PASS
- Răspunsurile serverului (coduri 220, 331, 230)
- Separarea canalelor de control și date

### Demo 3: Protocol Binar Personalizat

Demonstrație a construirii unui protocol cu header, lungime și CRC.

```powershell
python scripts/ruleaza_demo.py --demo protocol_binar
```

## Capturarea și Analiza Traficului

### Pornirea Capturii

```powershell
# Folosind scriptul helper
python scripts/captureaza_trafic.py --interfata eth0 --output pcap/saptamana9_captura.pcap

# Sau cu Wireshark direct
# Deschide Wireshark > Selectează "\\.\pipe\docker_engine" sau interfața potrivită
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

```powershell
# Oprește toate containerele (păstrează datele)
python scripts/opreste_lab.py

# Verifică oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Elimină toate containerele, rețelele și volumele pentru această săptămână
python scripts/curata.py --complet

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
```powershell
netstat -ano | findstr :2121
taskkill /PID <pid> /F
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

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 959: File Transfer Protocol (FTP)
- RFC 4217: Securing FTP with TLS

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
│  │  60000-60010     │  │              │  │              │     │
│  │  (passive)       │  │              │  │              │     │
│  └──────────────────┘  └──────────────┘  └──────────────┘     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Gazdă Windows  │
                    │                  │
                    │  - Wireshark     │
                    │  - Python 3.11   │
                    │  - Portainer     │
                    └──────────────────┘
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
