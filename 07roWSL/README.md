# Săptămâna 7: Interceptarea și Filtrarea Pachetelor

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator Rețele de Calculatoare
> 
> by Revolvix

## Prezentare Generală

Această sesiune de laborator explorează mecanismele fundamentale de observare și control al traficului de rețea la nivel de pachet. Studenții vor dobândi experiență practică în capturarea traficului folosind instrumente standard din industrie, implementarea regulilor de filtrare folosind iptables și înțelegerea distincției comportamentale dintre acțiunile REJECT și DROP.

Obiectivul central constă în dezvoltarea competențelor de diagnostic prin examinarea directă a fluxurilor de pachete. Prin observarea secvențelor de handshake TCP, datagramelor UDP și mesajelor de eroare ICMP, studenții vor construi un model mental al modului în care deciziile de filtrare se manifestă ca fenomene observabile în traficul de rețea.

Exercițiile progresează de la stabilirea conectivității de bază până la scenarii de filtrare complexe, culminând cu implementarea unui filtru la nivel aplicație și tehnici de sondare defensivă a porturilor.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** câmpurile cheie ale pachetelor și semnificația lor în capturile de trafic TCP/UDP
2. **Explicați** diferențele observabile dintre comportamentul REJECT și DROP în capturile de pachete
3. **Implementați** reguli de filtrare iptables folosind profiluri JSON predefinite
4. **Analizați** capturile de pachete pentru a diagnostica eșecurile de conectivitate și a determina cauzele fundamentale
5. **Proiectați** profile de firewall personalizate care echilibrează cerințele de securitate cu nevoile operaționale
6. **Evaluați** compromisurile dintre acțiunile REJECT și DROP în diferite scenarii de securitate

## Cerințe Preliminare

### Cunoștințe Necesare
- Înțelegerea modelului de handshake în trei pași TCP și al naturii fără conexiune a UDP
- Familiaritate cu conceptele de bază de adresare IP și porturi
- Experiență de bază cu linia de comandă în medii Linux/Windows

### Cerințe Software
- Windows 10/11 cu WSL2 activat
- Docker Desktop (backend WSL2)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau ulterior
- Git (opțional, dar recomandat)

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```powershell
# Deschideți PowerShell ca Administrator
cd WEEK7_WSLkit_RO

# Verificați cerințele preliminare
python setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```powershell
# Porniți toate serviciile
python scripts/porneste_lab.py

# Verificați că totul funcționează
python scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | https://localhost:9443 | Se setează la prima accesare |
| Server TCP Echo | localhost:9090 | Niciunul |
| Receptor UDP | localhost:9091 | Niciunul |
| Filtru Pachete (Proxy) | localhost:8888 | Niciunul |

## Exerciții de Laborator

### Exercițiul 1: Conectivitate de Bază și Captură

**Obiectiv:** Stabiliți conectivitatea de referință și capturați traficul TCP/UDP normal pentru analiză comparativă ulterioară.

**Durată:** 20-25 minute

**Pași:**

1. Porniți mediul de laborator:
   ```powershell
   python scripts/porneste_lab.py
   ```

2. Deschideți Wireshark și selectați interfața de rețea Docker

3. Aplicați filtrul: `tcp.port == 9090 or udp.port == 9091`

4. Rulați exercițiul de conectivitate de bază:
   ```powershell
   python src/exercises/ex_7_01_captură_referință.py
   ```

5. Observați în Wireshark:
   - Handshake-ul în trei pași TCP (SYN, SYN-ACK, ACK)
   - Transmisia datelor și răspunsul echo
   - Datagramele UDP trimise către receptor

6. Salvați captura ca: `pcap/saptamana7_ex1_referinta.pcap`

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 1
```

### Exercițiul 2: Filtrarea TCP cu REJECT

**Obiectiv:** Implementați o regulă de firewall care respinge conexiunile TCP și observați comportamentul caracteristic în capturile de pachete.

**Durată:** 25-30 minute

**Pași:**

1. Asigurați-vă că Wireshark capturează cu filtrul: `tcp.port == 9090`

2. Aplicați profilul de firewall care blochează TCP:
   ```powershell
   python scripts/ruleaza_demo.py --demo tcp
   ```

3. Observați în captură:
   - Pachetul SYN trimis de client
   - Răspunsul RST imediat (sau ICMP Port Unreachable)
   - **Nici o retransmisie** - conexiunea eșuează instantaneu

4. Comparați cu comportamentul de bază:
   - Timpul de răspuns: milisecunde vs. timeout
   - Tipul răspunsului: RST vs. SYN-ACK

5. Salvați captura ca: `pcap/saptamana7_ex2_tcp_reject.pcap`

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 2
```

### Exercițiul 3: Filtrarea UDP cu DROP

**Obiectiv:** Implementați o regulă de firewall care elimină silențios pachetele UDP și observați absența oricărui răspuns.

**Durată:** 25-30 minute

**Pași:**

1. Resetați la profilul de bază:
   ```powershell
   python scripts/ruleaza_demo.py --demo referinta
   ```

2. În Wireshark, aplicați filtrul: `udp.port == 9091`

3. Aplicați profilul de firewall care blochează UDP:
   ```powershell
   python scripts/ruleaza_demo.py --demo udp
   ```

4. Observați în captură:
   - Datagrama UDP trimisă
   - **Niciun răspuns** - nici ICMP, nici nimic
   - Acest comportament este indistinct de pierderea pachetelor

5. Discutați implicațiile:
   - De ce DROP este considerat mai „stealth"?
   - Cum afectează acest lucru aplicațiile care așteaptă răspuns?

6. Salvați captura ca: `pcap/saptamana7_ex3_udp_drop.pcap`

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 3
```

### Exercițiul 4: Filtru la Nivel Aplicație

**Obiectiv:** Înțelegeți cum filtrarea la nivel aplicație diferă de filtrarea la nivel rețea prin observarea că conexiunile TCP reușesc dar anumite cereri sunt blocate.

**Durată:** 30-35 minute

**Pași:**

1. Porniți serviciul de filtrare la nivel aplicație:
   ```powershell
   python scripts/porneste_lab.py --proxy
   ```

2. În Wireshark, aplicați filtrul: `tcp.port == 8888`

3. Testați cu conținut permis:
   ```powershell
   python src/apps/client_tcp.py --host localhost --port 8888 --mesaj "test normal"
   ```

4. Testați cu conținut blocat:
   ```powershell
   python src/apps/client_tcp.py --host localhost --port 8888 --mesaj "malware test"
   ```

5. Observați diferența:
   - Ambele conexiuni TCP se stabilesc cu succes
   - Doar cererile cu cuvinte cheie blocate sunt refuzate la nivel aplicație

6. Salvați captura ca: `pcap/saptamana7_ex4_filtru_aplicatie.pcap`

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 4
```

### Exercițiul 5: Sondare Defensivă a Porturilor

**Obiectiv:** Utilizați tehnici de sondare a porturilor pentru a identifica serviciile active și regulile de firewall, înțelegând perspectiva unui administrator de securitate.

**Durată:** 25-30 minute

**Pași:**

1. În Wireshark, aplicați filtrul: `tcp.flags.syn == 1`

2. Rulați instrumentul de sondare a porturilor:
   ```powershell
   python src/apps/sonda_porturi.py --tinta localhost --interval 9080-9100
   ```

3. Analizați rezultatele:
   - **DESCHIS**: SYN → SYN-ACK (serviciu activ)
   - **ÎNCHIS**: SYN → RST (niciun serviciu, niciun filtru)
   - **FILTRAT**: SYN → (timeout) (regulă DROP activă)

4. Documentați descoperirile într-un raport de securitate simplu

**Verificare:**
```powershell
python tests/test_exercitii.py --exercitiu 5
```

## Demonstrații

### Demo 1: Comparație REJECT vs DROP

Demonstrație automatizată care evidențiază diferențele comportamentale:

```powershell
python scripts/ruleaza_demo.py --demo reject_vs_drop
```

**Ce să observați:**
- REJECT: Eșec rapid (milisecunde), dezvăluie prezența firewall-ului
- DROP: Eșec lent (timeout), pare o problemă de rețea
- Diferența de timp este dramatică și măsurabilă

### Demo 2: Secvență Completă

Rulează toate scenariile secvențial pentru prezentare:

```powershell
python scripts/ruleaza_demo.py --demo complet
```

## Capturarea și Analiza Pachetelor

### Capturarea Traficului

```powershell
# Pornire captură
python scripts/capteaza_trafic.py --interfata eth0 --iesire pcap/captura_saptamana7.pcap

# Sau folosind Wireshark direct
# Deschideți Wireshark > Selectați interfața Docker corespunzătoare
```

### Filtre Wireshark Sugerate

```
# Trafic TCP pe portul echo
tcp.port == 9090

# Trafic UDP pe portul receptor
udp.port == 9091

# Doar pachete SYN (începuturi de conexiune)
tcp.flags.syn == 1 && tcp.flags.ack == 0

# Pachete RST (reset-uri de conexiune)
tcp.flags.reset == 1

# Mesaje ICMP de eroare
icmp.type == 3

# Combinație pentru analiză completă
tcp.port == 9090 or udp.port == 9091 or icmp
```

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

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de lucrat acasă.

### Tema 1: Proiectare Profil Firewall Personalizat
Creați un profil de firewall original care demonstrează înțelegerea semanticii REJECT vs DROP. Include minim 3 reguli cu justificări documentate.

### Tema 2: Raport de Analiză a Eșecurilor de Rețea
Rulați scenariile de simulare a eșecurilor, capturați traficul și produceți un raport profesional de incident care identifică cauza fundamentală pentru fiecare scenariu.

## Depanare

### Probleme Frecvente

#### Problemă: Docker Desktop nu pornește
**Soluție:** Verificați că WSL2 este activat și actualizat:
```powershell
wsl --update
wsl --set-default-version 2
```

#### Problemă: Containerele nu pornesc
**Soluție:** Verificați că porturile nu sunt ocupate:
```powershell
netstat -ano | findstr :9090
netstat -ano | findstr :9091
```

#### Problemă: Wireshark nu vede traficul Docker
**Soluție:** Selectați interfața corectă (de obicei `vEthernet (WSL)` sau `Ethernet`)

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundamente Teoretice

### Filtrarea Pachetelor și iptables

Netfilter/iptables reprezintă framework-ul standard de filtrare a pachetelor în Linux. Regulile sunt organizate în lanțuri (INPUT, OUTPUT, FORWARD) și tabele (filter, nat, mangle).

### Semantica REJECT vs DROP

| Aspect | REJECT | DROP |
|--------|--------|------|
| Răspuns | RST/ICMP | Niciunul |
| Timp eșec | Instant | Timeout |
| Informare atacator | Da | Nu |
| Experiență utilizator | Eșec rapid | Așteptare lungă |

### Capturarea ca Probă

Capturile de pachete servesc drept evidență obiectivă a comportamentului rețelei. Ele permit:
- Verificarea conformității cu politicile de securitate
- Diagnosticarea eșecurilor de conectivitate
- Analiza forensică post-incident

## Referințe

- Kurose, J. & Ross, K. (2016). *Rețele de Calculatoare: O Abordare Top-Down* (Ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Fundamente ale Programării de Rețea în Python*. Apress.
- Documentația oficială Netfilter/iptables: https://netfilter.org/documentation/
- Ghidul utilizatorului Wireshark: https://www.wireshark.org/docs/

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────┐
│                 Rețea Docker: week7net                      │
│                    (10.0.7.0/24)                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐    ┌──────────────────┐               │
│  │   server_tcp     │    │   receptor_udp   │               │
│  │   10.0.7.100     │    │   10.0.7.200     │               │
│  │   Port: 9090     │    │   Port: 9091     │               │
│  │   (Echo Server)  │    │   (Datagram Rx)  │               │
│  └──────────────────┘    └──────────────────┘               │
│           │                       │                         │
│           └───────────┬───────────┘                         │
│                       │                                     │
│              ┌────────┴────────┐                            │
│              │  filtru_pachete │  ← Proxy nivel aplicație   │
│              │   10.0.7.50     │                            │
│              │   Port: 8888    │                            │
│              └─────────────────┘                            │
│                                                             │
│  ════════════════════════════════════════════════════════   │
│           Reguli iptables (controlate de firewallctl.py)    │
│  Profile: referinta, blocare_tcp_9090, blocare_udp_9091     │
│  ════════════════════════════════════════════════════════   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
          │
          │ Expunere porturi
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      Gazdă Windows                          │
│                                                             │
│   localhost:9090 ──► Server TCP Echo                        │
│   localhost:9091 ──► Receptor UDP                           │
│   localhost:8888 ──► Filtru Aplicație                       │
│   localhost:9443 ──► Portainer (administrare)               │
│                                                             │
│   Wireshark ──► Captură trafic pe interfața Docker          │
└─────────────────────────────────────────────────────────────┘
```

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
