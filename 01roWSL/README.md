# Săptămâna 1: Fundamentele Rețelelor de Calculatoare

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator
>
> by Revolvix

## Prezentare Generală

Această sesiune de laborator introduce conceptele fundamentale ale rețelelor de calculatoare, concentrându-se pe instrumentele de diagnostic și tehnicile de analiză esențiale pentru înțelegerea comunicării în rețea. Studenții vor dobândi experiență practică cu utilitare de rețea la nivel de linie de comandă, captură de pachete și paradigme de programare a socket-urilor.

Laboratorul acoperă stiva TCP/IP de la o perspectivă practică, demonstrând modul în care datele traversează straturile rețelei și cum pot fi observate, capturate și analizate diferitele protocoale. Această cunoaștere fundamentală formează baza pentru toate sesiunile de laborator ulterioare.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** interfețele de rețea, adresele IP și tabelele de rutare folosind utilitare Linux
2. **Explicați** diferențele dintre protocoalele TCP și UDP în ceea ce privește stabilirea conexiunii și fiabilitatea
3. **Demonstrați** conectivitatea de bază a rețelei folosind ping, netcat și socket-uri Python
4. **Analizați** traficul de rețea capturat folosind tcpdump, tshark și Wireshark
5. **Construiți** aplicații simple client-server folosind socket-uri TCP în Python
6. **Evaluați** modelele de trafic de rețea prin analiza fișierelor PCAP

## Cerințe Preliminare

### Cunoștințe Necesare
- Operarea de bază în linia de comandă Linux
- Cunoștințe elementare de programare Python
- Înțelegerea numerotării binare și hexazecimale
- Familiaritate cu modelul stratificat TCP/IP

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (nativ Windows)
- Python 3.11 sau mai recent
- Git

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate de rețea

## Pornire Rapidă

### Configurare Inițială (Rulați o Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK1_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/instaleaza_prerequisite.py
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
| Container Lab | localhost:9090 (TCP) | N/A |
| Container Lab | localhost:9091 (UDP) | N/A |

## Arhitectura Laboratorului

```
┌─────────────────────────────────────────────────────────────────┐
│                        Windows 10/11                            │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────────┐  │
│  │   Wireshark  │  │  PowerShell  │  │    Docker Desktop     │  │
│  │  (Analiză)   │  │  (Scripturi) │  │    (Backend WSL2)     │  │
│  └──────────────┘  └──────────────┘  └───────────────────────┘  │
│         │                 │                      │              │
│         └─────────────────┼──────────────────────┘              │
│                           │                                     │
├───────────────────────────┼─────────────────────────────────────┤
│                         WSL2                                    │
│  ┌────────────────────────┴────────────────────────────────┐    │
│  │                    Docker Engine                         │    │
│  │  ┌─────────────────────────────────────────────────┐    │    │
│  │  │              week1_network (172.20.1.0/24)      │    │    │
│  │  │  ┌─────────────────────┐  ┌──────────────────┐  │    │    │
│  │  │  │    week1_lab        │  │    portainer     │  │    │    │
│  │  │  │  ├─ Python 3.12     │  │  (opțional)      │  │    │    │
│  │  │  │  ├─ tcpdump/tshark  │  │  :9443           │  │    │    │
│  │  │  │  ├─ netcat          │  └──────────────────┘  │    │    │
│  │  │  │  └─ iproute2        │                        │    │    │
│  │  │  │  :9090 (TCP)        │                        │    │    │
│  │  │  │  :9091 (UDP)        │                        │    │    │
│  │  │  └─────────────────────┘                        │    │    │
│  │  └─────────────────────────────────────────────────┘    │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

## Exerciții de Laborator

### Exercițiul 1: Inspectarea Interfețelor de Rețea

**Obiectiv:** Identificați și documentați toate interfețele de rețea și configurările acestora.

**Durată:** 15 minute

**Pași:**

1. Conectați-vă la containerul de laborator:
   ```bash
   docker exec -it week1_lab bash
   ```

2. Afișați toate interfețele de rețea:
   ```bash
   ip addr show
   ip -br addr show  # format scurt
   ```

3. Examinați tabela de rutare:
   ```bash
   ip route show
   ```

4. Vizualizați socket-urile active:
   ```bash
   ss -tunap
   ```

**Ce să observați:**
- Adrese IPv4 și IPv6 pe fiecare interfață
- Stările interfețelor (UP/DOWN)
- Gateway-ul implicit în tabela de rutare
- Porturi în starea LISTEN

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 1
```

---

### Exercițiul 2: Testarea Conectivității

**Obiectiv:** Testați conectivitatea rețelei folosind ICMP și măsurați latența.

**Durată:** 20 minute

**Pași:**

1. Testați conectivitatea loopback:
   ```bash
   ping -c 4 127.0.0.1
   ping -c 4 localhost
   ```

2. Testați conectivitatea la gateway:
   ```bash
   # Aflați gateway-ul
   ip route | grep default
   
   # Pingați gateway-ul (înlocuiți cu adresa voastră)
   ping -c 4 172.20.1.1
   ```

3. Rulați exercițiul Python de măsurare a latenței:
   ```bash
   cd /work/src/exercises
   python ex_1_01_latenta_ping.py
   ```

**Ce să observați:**
- Timpii de răspuns (RTT - Round Trip Time)
- Variația în latență
- Pierderi de pachete (dacă există)

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 2
```

---

### Exercițiul 3: Comunicarea TCP

**Obiectiv:** Stabiliți o conexiune TCP și observați stările socket-urilor.

**Durată:** 25 minute

**Pași:**

1. Porniți un server TCP cu netcat:
   ```bash
   # Terminal 1: Pornește serverul
   nc -l -p 9090
   ```

2. Conectați-vă de la un alt terminal:
   ```bash
   # Terminal 2: Conectează clientul
   nc localhost 9090
   ```

3. Trimiteți mesaje în ambele direcții și observați.

4. Într-un al treilea terminal, vizualizați starea conexiunii:
   ```bash
   # Terminal 3: Verifică socket-urile
   ss -tnp | grep 9090
   ```

5. Rulați exercițiul Python server-client:
   ```bash
   cd /work/src/exercises
   python ex_1_02_tcp_server_client.py
   ```

**Ce să observați:**
- Procesul de handshake în trei pași (SYN, SYN-ACK, ACK)
- Stările socket-urilor: LISTEN, ESTABLISHED, TIME_WAIT
- Transferul bidirecțional de date

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Captura de Trafic

**Obiectiv:** Capturați și salvați traficul de rețea pentru analiză.

**Durată:** 25 minute

**Pași:**

1. Porniți captura de trafic:
   ```bash
   # În containerul lab
   tcpdump -i lo -w /work/pcap/captura_tcp.pcap port 9090 &
   ```

2. Generați trafic TCP (ca în exercițiul 3).

3. Opriți captura:
   ```bash
   pkill tcpdump
   ```

4. Analizați captura:
   ```bash
   # Afișare rezumat
   tshark -r /work/pcap/captura_tcp.pcap
   
   # Numărare pachete
   tshark -r /work/pcap/captura_tcp.pcap | wc -l
   
   # Afișare flag-uri TCP
   tshark -r /work/pcap/captura_tcp.pcap -Y tcp -T fields -e tcp.flags.str
   ```

5. Opțional - Deschideți fișierul PCAP în Wireshark pe Windows.

**Ce să observați:**
- Structura pachetelor TCP
- Secvența handshake-ului
- Numerele de secvență și acknowledgement

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 4
```

---

### Exercițiul 5: Analiza Fișierelor PCAP

**Obiectiv:** Extrageți și procesați date statistice din capturi de trafic.

**Durată:** 25 minute

**Pași:**

1. Exportați datele capturii în format CSV:
   ```bash
   tshark -r /work/pcap/captura_tcp.pcap \
       -T fields \
       -e frame.number \
       -e frame.time_relative \
       -e ip.src \
       -e ip.dst \
       -e tcp.srcport \
       -e tcp.dstport \
       -e frame.len \
       -E header=y \
       -E separator=, > /work/pcap/captura.csv
   ```

2. Procesați CSV-ul cu Python:
   ```bash
   cd /work/src/exercises
   python ex_1_03_parsare_csv.py
   python ex_1_04_statistici_pcap.py
   ```

3. Calculați statistici:
   - Număr total de pachete
   - Dimensiunea medie a pachetelor
   - Durata conversației
   - Distribuția pe porturi

**Ce să observați:**
- Structura datelor exportate
- Modele de trafic
- Corelația între dimensiunea pachetelor și protocol

**Verificare:**
```bash
python tests/test_exercitii.py --exercitiu 5
```

## Demonstrații

### Demo 1: Diagnostic de Rețea

Demonstrație automatizată a comenzilor de diagnostic:

```powershell
python scripts/ruleaza_demo.py --demo 1
```

**Ce să observați:**
- Progresie logică: interfețe → rute → socket-uri → conectivitate
- Formatarea și interpretarea ieșirilor
- Depanarea sistematică a problemelor de rețea

### Demo 2: Comparație TCP vs UDP

Demonstrație paralelă a protocoalelor TCP și UDP:

```powershell
python scripts/ruleaza_demo.py --demo 2
```

**Ce să observați:**
- Overhead-ul handshake-ului TCP
- Diferențele în numărul de pachete
- Comportamentul la pierdere de pachete

### Demo 3: Socket-uri Python

Execuție live a exercițiilor cu socket-uri:

```powershell
python scripts/ruleaza_demo.py --demo 3
```

**Ce să observați:**
- Procesul de bind/listen/accept (server)
- Procesul de connect/send/recv (client)
- Tratarea erorilor și timeout-urile

## Captura și Analiza Pachetelor

### Capturarea Traficului

```powershell
# Pornirea capturii
python scripts/captura_trafic.py --interfata lo --output pcap/captura_saptamana1.pcap

# Sau folosiți Wireshark direct
# Deschideți Wireshark > Selectați interfața corespunzătoare
```

### Filtre Wireshark Sugerate

```
# Trafic TCP pe portul specific
tcp.port == 9090

# Doar pachete SYN (începutul conexiunii)
tcp.flags.syn == 1 and tcp.flags.ack == 0

# Handshake complet
tcp.flags.syn == 1 or (tcp.flags.syn == 1 and tcp.flags.ack == 1)

# Trafic UDP
udp

# Pachete ICMP (ping)
icmp

# Trafic de la/către o adresă IP specifică
ip.addr == 172.20.1.2
```

## Oprire și Curățare

### Sfârșit de Sesiune

```powershell
# Opriți toate containerele (păstrează datele)
python scripts/opreste_lab.py

# Verificați oprirea
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```powershell
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python scripts/curatare.py --complet

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de făcut acasă.

### Tema 1: Raport de Configurare a Rețelei
Documentați configurația completă a rețelei pe calculatorul personal.

### Tema 2: Analiza Protocoalelor TCP/UDP
Capturați și comparați traficul TCP și UDP, identificând diferențele.

## Depanare

### Probleme Frecvente

#### Problemă: Docker nu pornește
**Soluție:** Verificați că Docker Desktop rulează și are backend-ul WSL2 activat. Reporniți Docker Desktop dacă este necesar.

#### Problemă: Permisiuni insuficiente pentru captură
**Soluție:** Rulați comanda cu sudo în container sau verificați capabilitățile NET_ADMIN.

#### Problemă: Portul este deja utilizat
**Soluție:** Identificați procesul cu `ss -tlnp | grep PORT` și opriți-l sau folosiți alt port.

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundament Teoretic

Această săptămână acoperă fundamentele rețelelor, inclusiv:

- **Modelul TCP/IP**: Arhitectura pe patru straturi și funcțiile fiecărui strat
- **Adresarea IP**: Structura adreselor IPv4, notația CIDR și subrețele
- **Protocoale de transport**: TCP (orientat pe conexiune) vs UDP (fără conexiune)
- **Socket-uri**: Endpoints pentru comunicarea în rețea
- **Instrumente de diagnostic**: ip, ss, ping, netcat, tcpdump, tshark

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Tanenbaum, A. S. & Wetherall, D. J. (2011). *Computer Networks* (5th ed.). Pearson.
- Stevens, W. R. (1994). *TCP/IP Illustrated, Volume 1: The Protocols*. Addison-Wesley.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
