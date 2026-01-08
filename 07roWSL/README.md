# Săptămâna 7: Interceptarea și Filtrarea Pachetelor

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | Laborator Rețele de Calculatoare
> 
> by Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `07roWSL`

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

# Clonează Săptămâna 7
git clone https://github.com/antonioclim/netROwsl.git SAPT7
cd SAPT7
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 07roWSL/
cd 07roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT7\
    └── 07roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker
        │   └── configs/     # Profile firewall JSON
        ├── docs/            # Documentație suplimentară
        │   ├── comenzi_rapide.md
        │   ├── depanare.md
        │   ├── lecturi_suplimentare.md
        │   └── rezumat_teorie.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/   # Exerciții hw_7_01.py, hw_7_02.py
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # Aplicații (server_tcp, receptor_udp, filtru_pachete, etc.)
        │   └── exercises/   # Exerciții de laborator
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
cd /mnt/d/RETELE/SAPT7/07roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 7

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **week7_server_tcp** - Server TCP Echo (10.0.7.100:9090)
- **week7_receptor_udp** - Receptor UDP (10.0.7.200:9091)
- **week7_filtru_pachete** - Filtru la nivel aplicație (10.0.7.50:8888)
- **week7_demo** - Container pentru demonstrații

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

### Vizualizarea Rețelei week7net

1. Navighează: **Networks**
2. Click pe **week7net**
3. Vezi configurația IPAM: 10.0.7.0/24, gateway 10.0.7.1

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a observa comportamentul REJECT vs DROP
- Pentru analiza handshake-ului TCP și mesajelor ICMP

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
cd /mnt/d/RETELE/SAPT7/07roWSL

# Rulează exercițiul de referință
python3 src/exercises/ex_7_01_captura_referinta.py

# Sau demonstrația TCP
python3 scripts/ruleaza_demo.py --demo tcp
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 7

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Exercițiile de Laborator:**

| Filtru | Scop | Exercițiu |
|--------|------|-----------|
| `tcp.port == 9090` | Trafic TCP Echo | Ex. 1, 2 |
| `udp.port == 9091` | Trafic UDP | Ex. 1, 3 |
| `tcp.port == 8888` | Filtru aplicație | Ex. 4 |
| `tcp.port == 9090 or udp.port == 9091` | Tot traficul laborator | Referință |
| `tcp.port == 9090 or udp.port == 9091 or icmp` | Analiză completă | General |

**Filtre pentru Analiza Comportamentului:**

| Filtru | Scop | Ce să Observi |
|--------|------|---------------|
| `tcp.flags.syn == 1 && tcp.flags.ack == 0` | Doar SYN inițial | Începuturi conexiuni |
| `tcp.flags.syn == 1` | SYN și SYN-ACK | Handshake TCP |
| `tcp.flags.reset == 1` | Pachete RST | Comportament REJECT |
| `icmp.type == 3` | ICMP Destination Unreachable | REJECT sau DROP detectat |
| `icmp.type == 3 && icmp.code == 3` | Port Unreachable | REJECT explicit |
| `tcp.analysis.retransmission` | Retransmisii | Indiciu de DROP (timeout) |

**Filtre pentru Sondarea Porturilor:**

| Filtru | Scop | Ex. 5 |
|--------|------|-------|
| `tcp.dstport >= 9080 && tcp.dstport <= 9100` | Interval scanat | Sondare |
| `tcp.flags.syn == 1 && tcp.dstport >= 9080` | SYN în interval | Cereri sondare |

**Combinarea filtrelor:**
- ȘI: `tcp.port == 9090 && ip.addr == 10.0.7.100`
- SAU: `tcp.port == 9090 || tcp.port == 9091`
- NU: `!arp && !dns`

### Analiza Comportamentului REJECT vs DROP în Wireshark

**REJECT (Exercițiul 2):**
1. Observă pachetul SYN trimis de client
2. Imediat urmează RST (Reset) sau ICMP Port Unreachable
3. Nicio retransmisie - eșec instantaneu
4. Timp de răspuns: milisecunde

**DROP (Exercițiul 3):**
1. Observă datagrama UDP trimisă
2. **NICUN RĂSPUNS** - absolut nimic
3. Pentru TCP, vei vedea retransmisii multiple ale SYN
4. Timp eșec: timeout (secunde)

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Albastru deschis | Trafic UDP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori, RST, checksum-uri greșite |
| Text negru, fundal galben | Avertismente, retransmisii |

### Urmărirea unei Conversații TCP

1. Găsește orice pachet din conversația pe care vrei să o examinezi
2. Click dreapta → **Follow → TCP Stream**
3. O fereastră arată conversația completă în text lizibil
   - Text roșu: Date trimise de client
   - Text albastru: Date trimise de server (echo)
4. Folosește dropdown-ul pentru a comuta între vizualizări ASCII/Hex/Raw
5. Închide fereastra pentru a reveni la lista de pachete

### Analiza Handshake-ului TCP în Trei Pași

Caută această secvență pentru o conexiune reușită:
1. **SYN**: Client → Server (Flags: SYN)
2. **SYN-ACK**: Server → Client (Flags: SYN, ACK)
3. **ACK**: Client → Server (Flags: ACK)

Filtru pentru a vedea doar handshake-uri: `tcp.flags.syn == 1`

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT7\07roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `saptamana7_ex1_referinta.pcap`
   - `saptamana7_ex2_tcp_reject.pcap`
   - `saptamana7_ex3_udp_drop.pcap`
   - `saptamana7_ex4_filtru_aplicatie.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

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
- Windows 10/11 cu WSL2 activat (Ubuntu 22.04)
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație nativă Windows)
- Python 3.11 sau ulterior
- Git (opțional, dar recomandat)

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT7/07roWSL

# Verificați cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT7/07roWSL

# Porniți toate serviciile
python3 scripts/porneste_lab.py

# Verificați că totul funcționează
python3 scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Server TCP Echo | localhost:9090 | Niciunul |
| Receptor UDP | localhost:9091 | Niciunul |
| Filtru Pachete (Proxy) | localhost:8888 | Niciunul |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Conectivitate de Bază și Captură

**Obiectiv:** Stabiliți conectivitatea de referință și capturați traficul TCP/UDP normal pentru analiză comparativă ulterioară.

**Durată:** 20-25 minute

**Pregătire:** Deschide Wireshark și pornește captura pe `vEthernet (WSL)` ÎNAINTE de a rula exercițiul.

**Pași:**

1. Porniți mediul de laborator:
   ```bash
   python3 scripts/porneste_lab.py
   ```

2. Deschideți Wireshark și selectați interfața de rețea Docker

3. Aplicați filtrul: `tcp.port == 9090 or udp.port == 9091`

4. Rulați exercițiul de conectivitate de bază:
   ```bash
   python3 src/exercises/ex_7_01_captura_referinta.py
   ```

5. Observați în Wireshark:
   - Handshake-ul în trei pași TCP (SYN, SYN-ACK, ACK)
   - Transmisia datelor și răspunsul echo
   - Datagramele UDP trimise către receptor

6. Salvați captura ca: `pcap/saptamana7_ex1_referinta.pcap`

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

### Exercițiul 2: Filtrarea TCP cu REJECT

**Obiectiv:** Implementați o regulă de firewall care respinge conexiunile TCP și observați comportamentul caracteristic în capturile de pachete.

**Durată:** 25-30 minute

**Pași:**

1. Asigurați-vă că Wireshark capturează cu filtrul: `tcp.port == 9090`

2. Aplicați profilul de firewall care blochează TCP:
   ```bash
   python3 scripts/ruleaza_demo.py --demo tcp
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
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

### Exercițiul 3: Filtrarea UDP cu DROP

**Obiectiv:** Implementați o regulă de firewall care elimină silențios pachetele UDP și observați absența oricărui răspuns.

**Durată:** 25-30 minute

**Pași:**

1. Resetați la profilul de bază:
   ```bash
   python3 scripts/ruleaza_demo.py --demo referinta
   ```

2. În Wireshark, aplicați filtrul: `udp.port == 9091`

3. Aplicați profilul de firewall care blochează UDP:
   ```bash
   python3 scripts/ruleaza_demo.py --demo udp
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
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

### Exercițiul 4: Filtru la Nivel Aplicație

**Obiectiv:** Înțelegeți cum filtrarea la nivel aplicație diferă de filtrarea la nivel rețea prin observarea că conexiunile TCP reușesc dar anumite cereri sunt blocate.

**Durată:** 30-35 minute

**Pași:**

1. Porniți serviciul de filtrare la nivel aplicație:
   ```bash
   python3 scripts/porneste_lab.py --proxy
   ```

2. În Wireshark, aplicați filtrul: `tcp.port == 8888`

3. Testați cu conținut permis:
   ```bash
   python3 src/apps/client_tcp.py --host localhost --port 8888 --mesaj "test normal"
   ```

4. Testați cu conținut blocat:
   ```bash
   python3 src/apps/client_tcp.py --host localhost --port 8888 --mesaj "malware test"
   ```

5. Observați diferența:
   - Ambele conexiuni TCP se stabilesc cu succes
   - Doar cererile cu cuvinte cheie blocate sunt refuzate la nivel aplicație

6. Salvați captura ca: `pcap/saptamana7_ex4_filtru_aplicatie.pcap`

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

### Exercițiul 5: Sondare Defensivă a Porturilor

**Obiectiv:** Utilizați tehnici de sondare a porturilor pentru a identifica serviciile active și regulile de firewall, înțelegând perspectiva unui administrator de securitate.

**Durată:** 25-30 minute

**Pași:**

1. În Wireshark, aplicați filtrul: `tcp.flags.syn == 1`

2. Rulați instrumentul de sondare a porturilor:
   ```bash
   python3 src/apps/sonda_porturi.py --tinta localhost --interval 9080-9100
   ```

3. Analizați rezultatele:
   - **DESCHIS**: SYN → SYN-ACK (serviciu activ)
   - **ÎNCHIS**: SYN → RST (niciun serviciu, niciun filtru)
   - **FILTRAT**: SYN → (timeout) (regulă DROP activă)

4. Documentați descoperirile într-un raport de securitate simplu

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 5
```

## Demonstrații

### Demo 1: Comparație REJECT vs DROP

Demonstrație automatizată care evidențiază diferențele comportamentale:

```bash
python3 scripts/ruleaza_demo.py --demo reject_vs_drop
```

**Ce să observați:**
- REJECT: Eșec rapid (milisecunde), dezvăluie prezența firewall-ului
- DROP: Eșec lent (timeout), pare o problemă de rețea
- Diferența de timp este dramatică și măsurabilă

### Demo 2: Secvență Completă

Rulează toate scenariile secvențial pentru prezentare:

```bash
python3 scripts/ruleaza_demo.py --demo complet
```

## Capturarea și Analiza Pachetelor

### Capturarea Traficului

```bash
# Pornire captură (din WSL)
python3 scripts/capteaza_trafic.py --interfata eth0 --iesire pcap/captura_saptamana7.pcap

# Sau folosind Wireshark direct
# Deschideți Wireshark > Selectați interfața vEthernet (WSL)
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

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT7/07roWSL

# Opriți toate containerele (păstrează datele, Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verificați oprirea
docker ps
# Ar trebui să vezi doar: portainer
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/curata.py --complet

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

#### Problemă: Docker nu pornește în WSL
**Soluție:** Pornește serviciul manual:
```bash
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status
```

#### Problemă: Containerele nu pornesc
**Soluție:** Verificați că porturile nu sunt ocupate:
```bash
ss -tlnp | grep 9090
ss -tlnp | grep 9091
```

#### Problemă: Wireshark nu vede traficul Docker
**Soluție:** Selectați interfața corectă: `vEthernet (WSL)`, nu `Ethernet` sau `Wi-Fi`

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
│   localhost:9000 ──► Portainer (administrare globală)       │
│                                                             │
│   Wireshark ──► Captură trafic pe interfața vEthernet (WSL) │
└─────────────────────────────────────────────────────────────┘
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

### Probleme Specifice Săptămânii 7

**Problemă:** Regulile iptables nu funcționează
```bash
# Verifică regulile curente
docker exec week7_demo iptables -L -n

# Verifică profilul aplicat
cat docker/configs/firewall_profiles.json
```

**Problemă:** Server TCP Echo nu răspunde
```bash
# Verifică că containerul rulează
docker ps | grep week7_server_tcp

# Verifică log-urile
docker logs week7_server_tcp

# Testează conectivitatea
nc -zv localhost 9090
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week7net

# Verifică DNS în container
docker exec week7_server_tcp cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 9090

# Oprește procesul sau folosește alt port
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT7/07roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_lab.py --force

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
docker stop $(docker ps -q --filter "name=week7")

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

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
