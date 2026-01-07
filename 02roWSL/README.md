# Săptămâna 2: Modele Arhitecturale și Programare Socket

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
> 
> by Revolvix

## Prezentare Generală

Această săptămână explorează fundamentele arhitecturale ale rețelelor de calculatoare, concentrându-se pe două modele esențiale: **modelul OSI** (Open Systems Interconnection) cu cele 7 straturi ale sale și **modelul TCP/IP** cu 4 straturi, care reprezintă baza practică a Internetului contemporan.

Componenta practică introduce **programarea socket-urilor**, mecanismul fundamental prin care aplicațiile comunică prin rețea. Veți implementa servere TCP concurente și servere UDP cu protocoale personalizate, observând diferențele comportamentale dintre comunicația orientată pe conexiune (TCP) și cea fără conexiune (UDP).

Laboratorul pune accent pe observarea practică a traficului de rețea folosind Wireshark, permițându-vă să vizualizați handshake-ul TCP în trei pași, schimbul de date și terminarea conexiunii, consolidând astfel înțelegerea teoretică prin experiență directă.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** și **enumerați** cele 7 straturi ale modelului OSI și cele 4 straturi ale modelului TCP/IP
2. **Explicați** diferențele fundamentale dintre TCP (orientat pe conexiune, fiabil) și UDP (fără conexiune, best-effort)
3. **Implementați** un server TCP concurent folosind thread-uri în Python
4. **Construiți** un protocol de aplicație personalizat peste UDP cu comenzi multiple
5. **Analizați** traficul de rețea în Wireshark, identificând handshake-ul TCP și schimbul UDP
6. **Evaluați** scenariile în care TCP sau UDP reprezintă alegerea optimă

## Cerințe Preliminare

### Cunoștințe Necesare
- Concepte de bază ale rețelelor (adrese IP, porturi)
- Programare Python la nivel intermediar
- Familiaritate cu linia de comandă

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau mai recent
- Git (opțional, recomandat)

### Cerințe Hardware
- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conexiune la rețea

## Pornire Rapidă

### Prima Configurare (O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK2_WSLkit_RO

# Verificați cerințele preliminare
python setup/verify_environment.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/install_prerequisites.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/start_lab.py

# Verificați că totul funcționează
python scripts/start_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Server TCP | localhost:9090 | - |
| Server UDP | localhost:9091 | - |

## Exerciții de Laborator

### Exercițiul 1: Server TCP Concurent

**Obiectiv:** Implementarea și testarea unui server TCP care poate gestiona mai mulți clienți simultan folosind thread-uri.

**Durată estimată:** 30-40 minute

**Descrierea Protocolului:**
- Clientul trimite un mesaj text
- Serverul răspunde cu textul convertit la majuscule, prefixat cu "OK: "
- Conexiunea rămâne deschisă pentru mesaje multiple

**Pași:**

1. **Porniți serverul în modul threaded:**
   ```powershell
   # În containerul Docker
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --mode threaded
   ```

2. **Conectați un client:**
   ```powershell
   # Într-un alt terminal
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py client --message "salut lume"
   ```

3. **Testați concurența cu mai mulți clienți:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py load --clients 5 --messages 10
   ```

4. **Comparați cu modul iterativ:**
   ```powershell
   # Opriți serverul anterior (Ctrl+C), apoi:
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py server --mode iterative
   # Rulați din nou testul de încărcare și observați diferența
   ```

**Ce să observați:**
- În modul threaded, clienții primesc răspunsuri în paralel
- În modul iterativ, clienții sunt procesați secvențial
- Wireshark: identificați cele 3 pachete ale handshake-ului TCP (SYN, SYN-ACK, ACK)

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 1
```

---

### Exercițiul 2: Server UDP cu Protocol Personalizat

**Obiectiv:** Construirea unui server UDP care implementează un protocol de aplicație cu comenzi multiple.

**Durată estimată:** 25-35 minute

**Comenzile Protocolului:**
| Comandă | Descriere | Exemplu |
|---------|-----------|---------|
| `ping` | Verifică disponibilitatea | Răspuns: `PONG` |
| `upper:text` | Convertește la majuscule | `upper:salut` → `SALUT` |
| `lower:TEXT` | Convertește la minuscule | `lower:SALUT` → `salut` |
| `reverse:text` | Inversează textul | `reverse:abc` → `cba` |
| `echo:text` | Returnează textul neschimbat | `echo:test` → `test` |
| `time` | Returnează ora serverului | Răspuns: `2025-01-06 14:30:45` |
| `help` | Listează comenzile disponibile | - |

**Pași:**

1. **Porniți serverul UDP:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py server
   ```

2. **Testați în modul interactiv:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --interactive
   ```
   
   În modul interactiv, introduceți comenzi direct:
   ```
   > ping
   PONG
   > upper:rețele de calculatoare
   REȚELE DE CALCULATOARE
   > time
   2025-01-06 14:30:45
   > quit
   ```

3. **Trimiteți comenzi individuale:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --command "reverse:Python"
   ```

**Ce să observați:**
- UDP nu are handshake - datagramele sunt trimise direct
- Fiecare cerere-răspuns este independentă (fără stare)
- În Wireshark: observați că nu există SYN/ACK, doar pachete de date

**Verificare:**
```powershell
python tests/test_exercises.py --exercise 2
```

---

### Exercițiul 3: Capturarea și Analiza Traficului

**Obiectiv:** Utilizarea Wireshark pentru capturarea și analiza traficului TCP și UDP.

**Durată estimată:** 20-30 minute

**Pași:**

1. **Porniți captura:**
   ```powershell
   python scripts/capture_traffic.py --interface any --output pcap/week2_capture.pcap
   ```

2. **Generați trafic TCP:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_01_tcp.py client --message "test captură"
   ```

3. **Generați trafic UDP:**
   ```powershell
   docker exec -it week2_lab python /app/exercises/ex_2_02_udp.py client --command "ping"
   ```

4. **Opriți captura (Ctrl+C) și deschideți în Wireshark:**
   ```powershell
   # Fișierul se află în directorul pcap/
   ```

5. **Aplicați filtre Wireshark:**
   - Pentru TCP: `tcp.port == 9090`
   - Pentru UDP: `udp.port == 9091`
   - Pentru handshake: `tcp.flags.syn == 1`

**Ce să identificați în Wireshark:**
- **TCP:** SYN → SYN-ACK → ACK (handshake), PSH-ACK (date), FIN-ACK (terminare)
- **UDP:** Doar pachete de date, fără confirmare

## Demonstrații

### Demo 1: Comparație TCP vs UDP

Demonstrație automatizată care evidențiază diferențele comportamentale dintre cele două protocoale.

```powershell
python scripts/run_demo.py --demo 1
```

**Ce veți observa:**
- TCP: Latență inițială mai mare (handshake), dar livrare garantată
- UDP: Răspuns imediat, dar fără garanții de livrare
- Statistici comparative în timp real

### Demo 2: Gestionarea Clienților Concurenți

Demonstrație a modului în care un server threaded gestionează conexiuni multiple simultan.

```powershell
python scripts/run_demo.py --demo 2
```

**Ce veți observa:**
- 10 clienți conectați simultan
- Răspunsuri intercalate (nu secvențiale)
- Timpul total vs. timpul cumulativ

## Capturarea și Analiza Pachetelor

### Pornirea Capturii

```powershell
# Capturare cu filtrare
python scripts/capture_traffic.py --filter "port 9090 or port 9091" --output pcap/week2_lab.pcap

# Sau folosiți Wireshark direct
# Deschideți Wireshark > Selectați interfața potrivită
```

### Filtre Wireshark Recomandate

```
# Trafic TCP pe portul serverului
tcp.port == 9090

# Trafic UDP pe portul serverului
udp.port == 9091

# Doar pachete SYN (inițiere conexiune TCP)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Doar pachete FIN (terminare conexiune TCP)
tcp.flags.fin == 1

# Retransmisii TCP (probleme de rețea)
tcp.analysis.retransmission

# Combinație: tot traficul laboratorului
tcp.port == 9090 || udp.port == 9091
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```powershell
# Opriți toate containerele (păstrează datele)
python scripts/stop_lab.py

# Verificați oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python scripts/cleanup.py --full

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de lucru individual.

### Tema 1: Server TCP cu Protocol de Autentificare
Extindeți serverul TCP pentru a suporta autentificare simplă (utilizator/parolă) înainte de procesarea comenzilor.

### Tema 2: Client UDP cu Retry și Timeout
Implementați un client UDP robust care reîncearcă automat trimiterea dacă nu primește răspuns în 2 secunde.

## Depanare

### Probleme Frecvente

#### Problema: Portul este deja în uz
**Soluție:** 
```powershell
# Găsiți procesul care folosește portul
netstat -ano | findstr :9090
# Opriți procesul sau folosiți alt port
python scripts/cleanup.py --full
```

#### Problema: Docker nu pornește
**Soluție:**
```powershell
# Verificați că Docker Desktop rulează
# Reporniți Docker Desktop din System Tray
# Verificați că WSL2 este activ:
wsl --status
```

#### Problema: Conexiune refuzată la server
**Soluție:**
```powershell
# Verificați că serverul rulează
docker ps
# Verificați logurile
docker logs week2_lab
```

#### Problema: Wireshark nu vede traficul Docker
**Soluție:**
- Selectați interfața corectă (de obicei `vEthernet` sau `docker0`)
- Alternativ, capturați din interiorul containerului cu `tcpdump`

Consultați `docs/troubleshooting.md` pentru mai multe soluții.

## Fundamente Teoretice

### Modelul OSI (7 Straturi)

| Nr. | Strat | Funcție | Exemple |
|-----|-------|---------|---------|
| 7 | Aplicație | Interfață cu utilizatorul | HTTP, FTP, SMTP |
| 6 | Prezentare | Formatare, criptare | SSL/TLS, JPEG |
| 5 | Sesiune | Gestiunea dialogului | NetBIOS, RPC |
| 4 | Transport | Livrare end-to-end | TCP, UDP |
| 3 | Rețea | Rutare, adresare logică | IP, ICMP |
| 2 | Legătură de Date | Acces la mediu, cadre | Ethernet, Wi-Fi |
| 1 | Fizic | Biți pe mediu fizic | Cabluri, semnale |

### Modelul TCP/IP (4 Straturi)

| Nr. | Strat TCP/IP | Echivalent OSI | Protocoale |
|-----|--------------|----------------|------------|
| 4 | Aplicație | 5, 6, 7 | HTTP, FTP, DNS |
| 3 | Transport | 4 | TCP, UDP |
| 2 | Internet | 3 | IP, ICMP, ARP |
| 1 | Acces la Rețea | 1, 2 | Ethernet, Wi-Fi |

### TCP vs UDP

| Caracteristică | TCP | UDP |
|----------------|-----|-----|
| Conexiune | Orientat pe conexiune | Fără conexiune |
| Fiabilitate | Garantată (ACK, retransmisie) | Best-effort |
| Ordine | Păstrată | Nu este garantată |
| Control flux | Da (fereastră glisantă) | Nu |
| Overhead | Mai mare (header 20+ bytes) | Mai mic (header 8 bytes) |
| Utilizare | Web, email, transfer fișiere | Streaming, DNS, jocuri |

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────┐
│                         Windows Host                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌──────────────┐ │
│  │   PowerShell    │    │    Wireshark    │    │   Browser    │ │
│  │   (scripturi)   │    │  (analiză pcap) │    │  (Portainer) │ │
│  └────────┬────────┘    └────────┬────────┘    └──────┬───────┘ │
│           │                      │                     │         │
│  ─────────┴──────────────────────┴─────────────────────┴──────── │
│                              WSL2                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                     Docker Network                           │ │
│  │                    (week2_network)                           │ │
│  │                     10.0.2.0/24                              │ │
│  │  ┌─────────────────────────────────────────────────────┐    │ │
│  │  │              Container: week2_lab                    │    │ │
│  │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │ │
│  │  │  │ Server TCP  │  │ Server UDP  │  │   tcpdump   │  │    │ │
│  │  │  │  :9090      │  │   :9091     │  │  (captură)  │  │    │ │
│  │  │  └─────────────┘  └─────────────┘  └─────────────┘  │    │ │
│  │  └─────────────────────────────────────────────────────┘    │ │
│  │  ┌─────────────────────────────────────────────────────┐    │ │
│  │  │              Container: portainer                    │    │ │
│  │  │                     :9443                            │    │ │
│  │  └─────────────────────────────────────────────────────┘    │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

Handshake TCP (3-Way):
┌────────┐                              ┌────────┐
│ Client │                              │ Server │
└───┬────┘                              └───┬────┘
    │                                       │
    │  ──────── SYN (seq=x) ─────────────►  │
    │                                       │
    │  ◄─────── SYN-ACK (seq=y, ack=x+1) ── │
    │                                       │
    │  ──────── ACK (ack=y+1) ────────────► │
    │                                       │
    │        [Conexiune stabilită]          │
    │                                       │

Schimb UDP (fără handshake):
┌────────┐                              ┌────────┐
│ Client │                              │ Server │
└───┬────┘                              └───┬────┘
    │                                       │
    │  ──────── Datagramă cerere ────────►  │
    │                                       │
    │  ◄─────── Datagramă răspuns ───────── │
    │                                       │
    │    [Fără confirmare de primire]       │
```

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1*. Addison-Wesley.
- Documentația Python: [socket — Low-level networking interface](https://docs.python.org/3/library/socket.html)

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
