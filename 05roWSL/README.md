# Săptămâna 5: Nivelul Rețea – Adresare IPv4/IPv6, Subrețele și VLSM

> Laborator Rețele de Calculatoare – ASE, Informatică Economică
> 
> realizat de Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `05roWSL`

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

# Clonează Săptămâna 5
git clone https://github.com/antonioclim/netROwsl.git SAPT5
cd SAPT5
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 05roWSL/
cd 05roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT5\
    └── 05roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        │   ├── configs/     # Configurații suplimentare
        │   └── volumes/     # Volume persistente
        ├── docs/            # Documentație suplimentară
        │   ├── depanare.md
        │   ├── fisa_comenzi.md
        │   └── rezumat_teorie.md
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
        │   ├── apps/        # Aplicații (calculator subrețea, UDP echo)
        │   ├── exercises/   # Exerciții de laborator
        │   └── utils/       # Utilitare de rețea
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
cd /mnt/d/RETELE/SAPT5/05roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor

Navighează: **Home → local → Containers**

Vei vedea un tabel cu toate containerele care include:
- **Nume** - Identificatorul containerului (week5_python, week5_udp-server, week5_udp-client)
- **Stare** - Running/Stopped/Paused
- **Imagine** - Imaginea Docker folosită
- **Porturi** - Mapările de porturi host:container

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

### Vizualizarea Rețelei week5_labnet

1. Navighează: **Networks → week5_labnet**
2. Observă configurația rețelei:
   - Subnet: 10.5.0.0/24
   - Gateway: 10.5.0.1
3. Vezi containerele conectate:
   - week5_python: 10.5.0.10
   - week5_udp-server: 10.5.0.20
   - week5_udp-client: 10.5.0.30

### Modificarea Configurației Rețelei

1. Pentru a modifica subrețeaua, editează `docker/docker-compose.yml`:
   ```yaml
   networks:
     labnet:
       ipam:
         config:
           - subnet: 10.5.0.0/24    # Modifică aici
             gateway: 10.5.0.1      # Modifică aici
   ```
2. Recreează rețeaua:
   ```bash
   docker-compose -f docker/docker-compose.yml down
   docker-compose -f docker/docker-compose.yml up -d
   ```

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a examina anteturile IP și UDP în comunicarea între containere
- Pentru a verifica adresele sursă/destinație în pachete

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
cd /mnt/d/RETELE/SAPT5/05roWSL

# Rulează demonstrația UDP
python3 scripts/ruleaza_demo.py --demo udp

# Sau accesează direct containerul
docker exec -it week5_python bash
ping 10.5.0.20
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 5

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `ip.version == 4` | Trafic IPv4 | Analiză adresare IPv4 |
| `ipv6` | Trafic IPv6 | Analiză adresare IPv6 |
| `udp.port == 9999` | Server UDP Echo | Trafic demonstrație |
| `ip.addr == 10.5.0.10` | Container Python | Trafic specific container |
| `ip.addr == 10.5.0.20` | Server UDP | Trafic server |
| `ip.addr == 10.5.0.30` | Client UDP | Trafic client |
| `ip.src == 10.5.0.0/24` | Trafic din rețeaua laborator | Tot traficul week5_labnet |
| `icmp` | Pachete ICMP (ping) | Teste conectivitate |
| `ip.ttl == 64` | Pachete cu TTL specific | Analiză hop count |
| `udp` | Tot traficul UDP | Analiză generală UDP |

**Combinarea filtrelor:**
- ȘI: `udp.port == 9999 && ip.addr == 10.5.0.20`
- SAU: `ip.addr == 10.5.0.10 || ip.addr == 10.5.0.20`
- NU: `!arp && !dns`

### Analiza Antetului IP în Wireshark

1. Selectează un pachet IP în lista de captură
2. Expandează "Internet Protocol Version 4" în panoul de detalii
3. Observă câmpurile:
   - **Version:** 4 (IPv4) sau 6 (IPv6)
   - **Header Length:** Lungimea antetului (tipic 20 bytes)
   - **Total Length:** Dimensiunea totală a pachetului
   - **TTL (Time to Live):** Numărul de hop-uri rămase
   - **Protocol:** Următorul protocol (6=TCP, 17=UDP)
   - **Source Address:** Adresa IP sursă
   - **Destination Address:** Adresa IP destinație

### Analiza Antetului UDP în Wireshark

1. Expandează "User Datagram Protocol" pentru pachete UDP
2. Observă câmpurile:
   - **Source Port:** Portul sursă
   - **Destination Port:** Portul destinație (9999 pentru server)
   - **Length:** Lungimea datagramei
   - **Checksum:** Suma de control

### Verificarea Comunicării UDP Echo

1. Capturează trafic cu filtrul `udp.port == 9999`
2. Observă perechile de pachete:
   - Client → Server: Mesaj trimis
   - Server → Client: Răspuns echo (același conținut)
3. Compară payload-ul celor două pachete

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Text negru, fundal roșu | Erori, checksum-uri greșite |
| Text negru, fundal galben | Avertismente, retransmisii |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT5\05roWSL\pcap\`
3. Nume fișier sugestiv: `udp_echo_demo.pcap` sau `ipv4_analysis.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

## Prezentare Generală

Această sesiune de laborator explorează **Nivelul Rețea** din modelul TCP/IP, concentrându-se pe mecanismele fundamentale de adresare care permit comunicarea între dispozitive în rețele interconectate. Studenții vor examina atât arhitectura IPv4, cât și IPv6, înțelegând principiile de proiectare, schemele de adresare și tehnicile de subnetare care stau la baza infrastructurii moderne de internet.

Componenta practică pune accent pe calculele de subnetare prin două metodologii distincte: **FLSM** (Fixed-Length Subnet Mask – Mască de subrețea de lungime fixă) și **VLSM** (Variable-Length Subnet Mask – Mască de subrețea de lungime variabilă). Prin exerciții interactive Python și observarea traficului în containere Docker, studenții vor dezvolta competențe în proiectarea schemelor de adresare eficiente care minimizează risipa de adrese IP, respectând în același timp cerințele organizaționale.

Mediul de laborator utilizează Docker pentru a simula mai multe segmente de rețea, permițând studenților să observe comportamentul pachetelor, să analizeze anteturile IP și să verifice configurațiile de adresare folosind instrumente standard de rețea.

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** rolul și funcțiile Nivelului Rețea în arhitecturile OSI și TCP/IP
2. **Explicați** diferențele dintre adresarea IPv4 și IPv6, inclusiv notația și structura
3. **Calculați** adrese de rețea, adrese de broadcast și intervale de gazde utilizabile pentru orice bloc CIDR
4. **Aplicați** tehnicile FLSM și VLSM pentru a divide rețelele în subrețele în funcție de cerințe
5. **Proiectați** scheme de adresare eficiente care minimizează risipa de adrese IP
6. **Evaluați** compromisurile dintre simplitatea FLSM și eficiența VLSM în scenarii din lumea reală

## Cerințe Preliminare

### Cunoștințe Necesare

- Sisteme de numerație binară și hexazecimală
- Concepte de bază ale rețelelor de calculatoare (din săptămânile 1-4)
- Înțelegerea stratificării protocoalelor și încapsulării
- Familiaritate cu operațiile de linie de comandă

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git

### Cerințe Hardware

- Minim 8GB RAM (recomandat 16GB)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se execută o singură dată)

```bash
# Deschideți terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT5/05roWSL

# Verificați cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulați asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT5/05roWSL

# Porniți toate serviciile
python3 scripts/porneste_laborator.py

# Verificați că totul funcționează
python3 scripts/porneste_laborator.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Container Python | 10.5.0.10 | Acces prin docker exec |
| Server UDP | 10.5.0.20:9999 | Fără autentificare |
| Client UDP | 10.5.0.30 | Acces prin docker exec |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Analiză CIDR și Subnetare FLSM

**Obiectiv:** Analizați blocuri CIDR pentru a extrage proprietățile rețelei și aplicați FLSM pentru a crea subrețele de dimensiuni egale.

**Durată:** 25-30 minute

**Pași:**

1. Deschideți un terminal în directorul kitului:
   ```bash
   cd /mnt/d/RETELE/SAPT5/05roWSL
   ```

2. Rulați scriptul de analiză CIDR cu o adresă exemplu:
   ```bash
   python3 src/exercises/ex_5_01_cidr_flsm.py 192.168.10.14/26
   ```

3. Examinați rezultatul care afișează:
   - Adresa de rețea și adresa de broadcast
   - Intervalul de gazde utilizabile
   - Reprezentarea binară a măștii
   - Clasa de adresă și tipul (public/privat)

4. Testați subnetarea FLSM:
   ```bash
   python3 src/exercises/ex_5_01_cidr_flsm.py 10.0.0.0/16 --subretele 4
   ```

5. Observați cum rețeaua /16 este divizată în 4 subrețele egale /18

**Verificare:**
```bash
# Comanda pentru verificarea succesului
python3 tests/test_exercitii.py --exercitiu 1
```

**Rezultat Așteptat:**
- Analiza 192.168.10.14/26 ar trebui să raporteze 62 de gazde utilizabile
- Divizarea FLSM a 10.0.0.0/16 în 4 subrețele produce blocuri /18

---

### Exercițiul 2: Alocare VLSM și Operații IPv6

**Obiectiv:** Implementați alocarea VLSM pentru cerințe variabile de gazde și efectuați operații de adresare IPv6.

**Durată:** 30-35 minute

**Pași:**

1. Rulați alocatorul VLSM cu cerințe multiple de departamente:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py --vlsm 172.16.0.0/16 --cerinte 500,120,60,30,2
   ```

2. Analizați cum algoritmul:
   - Sortează cerințele descrescător
   - Alocă dimensiunea minimă a blocului pentru fiecare cerință
   - Menține alinierea la granițe de bloc
   - Maximizează utilizarea spațiului de adrese

3. Comparați eficiența VLSM vs FLSM pentru aceleași cerințe

4. Explorați operațiile IPv6:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py --ipv6-comprimare "2001:0db8:0000:0000:0000:0000:0000:0001"
   python3 src/exercises/ex_5_02_vlsm_ipv6.py --ipv6-expandare "2001:db8::1"
   ```

5. Generați subrețele IPv6 dintr-o alocare /48:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py --subretele-ipv6 "2001:db8:abcd::/48" --numar 8
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

**Rezultat Așteptat:**
- Alocarea VLSM ar trebui să producă 5 subrețele cu prefixe variate (/23, /25, /26, /27, /30)
- Comprimarea IPv6 ar trebui să producă `2001:db8::1`
- Expandarea ar trebui să restabilească formatul complet pe 32 de caractere hexazecimale

---

### Exercițiul 3: Chestionar Interactiv de Subnetare

**Obiectiv:** Testați-vă cunoștințele de subnetare printr-un quiz interactiv.

**Durată:** 15-20 minute

**Pași:**

1. Lansați generatorul de quiz:
   ```bash
   python3 src/exercises/ex_5_03_generator_quiz.py
   ```

2. Răspundeți la întrebări despre:
   - Calculul adreselor de rețea
   - Determinarea adreselor de broadcast
   - Identificarea gazdelor utilizabile
   - Selectarea măștii corecte pentru cerințele de gazde

3. Revedeți explicațiile pentru răspunsurile incorecte

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

---

### Exercițiul 4: Comunicare UDP în Rețea Containerizată

**Obiectiv:** Observați comunicarea UDP între containere și capturați traficul de rețea.

**Durată:** 20-25 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` cu filtrul `udp.port == 9999` ÎNAINTE de a începe exercițiul.

**Pași:**

1. Asigurați-vă că mediul de laborator este pornit:
   ```bash
   python3 scripts/porneste_laborator.py --status
   ```

2. Într-un terminal, porniți captura de trafic:
   ```bash
   python3 scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/udp_demo.pcap
   ```

3. În alt terminal, rulați demonstrația UDP:
   ```bash
   python3 scripts/ruleaza_demo.py --demo udp
   ```

4. Opriți captura (Ctrl+C) și deschideți fișierul pcap în Wireshark

5. Analizați:
   - Anteturile IP (adrese sursă și destinație)
   - Anteturile UDP (porturi sursă și destinație)
   - Încărcătura utilă a mesajelor echo

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

## Demonstrații

### Demo 1: Analiză CIDR Completă

Demonstrație automată a analizei blocurilor CIDR cu reprezentare vizuală.

```bash
python3 scripts/ruleaza_demo.py --demo cidr
```

**Ce să observați:**
- Conversia binară a adreselor IP
- Aplicarea măștii pentru derivarea adresei de rețea
- Calculul intervalului de difuzare

### Demo 2: Comparație FLSM vs VLSM

Comparație vizuală a eficienței celor două tehnici de subnetare.

```bash
python3 scripts/ruleaza_demo.py --demo vlsm
```

**Ce să observați:**
- Risipa de adrese în FLSM când cerințele variază
- Alocarea optimă în VLSM
- Calcule de eficiență procentuală

### Demo 3: Operații IPv6

Demonstrarea comprimării și expandării adreselor IPv6.

```bash
python3 scripts/ruleaza_demo.py --demo ipv6
```

**Ce să observați:**
- Regulile de comprimare (zerouri consecutivi, grupuri de conducere)
- Validarea formatului de adresă
- Generarea subrețelelor /64

### Demo 4: Comunicare UDP

Demonstrarea trimiterii și primirii pachetelor UDP între containere.

```bash
python3 scripts/ruleaza_demo.py --demo udp
```

**Ce să observați:**
- Rezoluția adreselor IP între containere
- Structura pachetelor UDP
- Mecanismul de echo pentru verificare

## Captură și Analiză de Pachete

### Capturarea Traficului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT5/05roWSL

# Pornirea capturii
python3 scripts/captureaza_trafic.py --interfata eth0 --iesire pcap/captura_sapt5.pcap

# Sau utilizați Wireshark direct pe Windows
# Selectați interfața vEthernet (WSL)
```

### Filtre Wireshark Sugerate

```
# Trafic IPv4
ip.version == 4

# Trafic IPv6
ipv6

# Trafic UDP pe portul 9999
udp.port == 9999

# Trafic ICMP (ping)
icmp

# Trafic de la/către container specific
ip.addr == 10.5.0.10

# Pachete cu TTL specific
ip.ttl == 64
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT5/05roWSL

# Opriți toate containerele de laborator (Portainer rămâne activ!)
python3 scripts/opreste_laborator.py

# Verificați oprirea - ar trebui să vedeți doar portainer
docker ps
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Eliminați toate containerele, rețelele și volumele pentru această săptămână
python3 scripts/curata.py --complet

# Verificați curățarea
docker system df
```

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de rezolvat acasă.

### Tema 1: Proiectare Rețea Corporativă

Proiectați o schemă de adresare VLSM pentru o companie cu 5 departamente având cerințe diferite de gazde. Documentați alegerile și justificați eficiența.

### Tema 2: Plan de Migrare IPv6

Elaborați un plan de tranziție de la IPv4 la IPv6 pentru o rețea mică, incluzând:
- Schemă de adresare IPv6
- Mecanisme de coexistență (dual-stack, tunneling)
- Cronologie de implementare

## Depanare

### Probleme Frecvente

#### Problemă: Containerele nu pornesc
**Soluție:** Verificați că Docker rulează în WSL2.
```bash
sudo service docker start
docker info
```

#### Problemă: Nu se poate accesa Portainer
**Soluție:** Verificați că Portainer rulează pe portul 9000.
```bash
docker ps | grep portainer
```

#### Problemă: Scripturile Python nu găsesc modulele
**Soluție:** Asigurați-vă că rulați din directorul rădăcină al kitului și că PYTHONPATH include directorul curent.
```bash
cd /mnt/d/RETELE/SAPT5/05roWSL
export PYTHONPATH=$PWD:$PYTHONPATH
```

#### Problemă: Captura de pachete nu funcționează
**Soluție:** Containerele necesită capabilități NET_ADMIN și NET_RAW. Verificați configurația docker-compose.yml.

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundamente Teoretice

### Nivelul Rețea în Modelul OSI

Nivelul Rețea (Layer 3) oferă adresare logică și rutare, permițând comunicarea între rețele diferite. Funcțiile principale includ:

- **Adresare logică:** Atribuirea de identificatori unici (adrese IP) dispozitivelor
- **Rutare:** Determinarea căii optime pentru pachete între rețele
- **Fragmentare:** Divizarea pachetelor pentru a se încadra în MTU-ul rețelei
- **Încapsulare:** Adăugarea antetului IP la datele de la nivelurile superioare

### Arhitectura IPv4

Adresele IPv4 constau din 32 de biți, reprezentați în notație zecimală cu punct (ex: 192.168.1.1). Spațiul de adrese este organizat în:

- **Clase tradiționale:** A, B, C, D (multicast), E (experimental)
- **CIDR (Classless Inter-Domain Routing):** Permite prefixe de lungime arbitrară
- **Adrese private:** 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

### Subnetare FLSM vs VLSM

**FLSM** împarte o rețea în subrețele de dimensiuni egale, simplificând administrarea dar risipind adrese când cerințele diferă.

**VLSM** permite subrețele de dimensiuni diferite, maximizând eficiența prin adaptarea dimensiunii blocului la cerințele reale.

### Arhitectura IPv6

IPv6 utilizează adrese de 128 de biți în notație hexazecimală cu două puncte. Caracteristici cheie:

- **Spațiu de adrese extins:** 2^128 adrese posibile
- **Header simplificat:** Structură fixă de 40 de octeți
- **Autoconfigurare:** SLAAC (Stateless Address Autoconfiguration)
- **Tipuri de adrese:** Unicast, multicast, anycast (fără broadcast)

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 791 - Internet Protocol (IPv4)
- RFC 8200 - Internet Protocol, Version 6 (IPv6)
- RFC 4632 - Classless Inter-domain Routing (CIDR)

## Diagramă de Arhitectură

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEEK5_WSLkit Environment                     │
│                    Rețea: week5_labnet (10.5.0.0/24)           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  week5_python   │  │ week5_udp-server│  │ week5_udp-client│ │
│  │                 │  │                 │  │                 │ │
│  │  IP: 10.5.0.10  │  │  IP: 10.5.0.20  │  │  IP: 10.5.0.30  │ │
│  │                 │  │  Port: 9999     │  │                 │ │
│  │  • Python 3.11  │  │  • Server Echo  │  │  • Client UDP   │ │
│  │  • Exerciții    │  │  • UDP Socket   │  │  • Testare      │ │
│  │  • Utilitare    │  │                 │  │                 │ │
│  └────────┬────────┘  └────────┬────────┘  └────────┬────────┘ │
│           │                    │                    │          │
│           └────────────────────┼────────────────────┘          │
│                                │                               │
│                    ┌───────────┴───────────┐                   │
│                    │   Docker Bridge Net   │                   │
│                    │    10.5.0.0/24        │                   │
│                    └───────────────────────┘                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│  Portainer: http://localhost:9000                               │
│  Capabilități: NET_ADMIN, NET_RAW (pentru tcpdump)             │
└─────────────────────────────────────────────────────────────────┘
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

### Probleme Exerciții Python

**Problemă:** ModuleNotFoundError pentru pachete
```bash
# Instalează pachetele necesare
pip install docker requests pyyaml --break-system-packages

# Sau în virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r setup/requirements.txt
```

**Problemă:** Erori la calculele CIDR/VLSM
- Verifică formatul adresei: `IP/PREFIX` (ex: 192.168.1.0/24)
- Asigură-te că prefixul este valid (0-32 pentru IPv4, 0-128 pentru IPv6)

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week5_labnet

# Verifică DNS în container
docker exec week5_python cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 9999

# Oprește procesul sau folosește alt port
```

**Problemă:** Containerele nu comunică între ele
```bash
# Verifică că sunt în aceeași rețea
docker network inspect week5_labnet

# Testează conectivitatea
docker exec week5_python ping -c 3 10.5.0.20
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT5/05roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
docker-compose -f docker/docker-compose.yml down

# Verifică - ar trebui să arate încă portainer
docker ps
# OUTPUT așteptat:
# CONTAINER ID   IMAGE                    NAMES
# abc123...      portainer/portainer-ce   portainer
```

### Sfârșit de Săptămână (Completă)

```bash
# Elimină containerele și rețelele acestei săptămâni
docker-compose -f docker/docker-compose.yml down --volumes

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
docker stop $(docker ps -q --filter "name=week5")

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

*Laborator Rețele de Calculatoare – ASE, Informatică Economică | realizat de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
