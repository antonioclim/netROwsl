# Săptămâna 10: Nivelul Aplicație - HTTP/S, REST și Servicii de Rețea

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
> 
> by Revolvix

---

## Cuprins

- [Notificare Mediu](#️-notificare-mediu)
- [Filozofie de Învățare](#-filozofie-de-învățare)
- [Clonarea Laboratorului](#-clonarea-laboratorului-acestei-săptămâni)
- [Configurarea Inițială](#-configurarea-inițială-a-mediului-doar-prima-dată)
- [Interfața Portainer](#️-înțelegerea-interfeței-portainer)
- [Configurarea Wireshark](#-configurarea-și-utilizarea-wireshark)
- [Prezentare Generală](#prezentare-generală)
- [Obiective de Învățare](#obiective-de-învățare)
- [Pornire Rapidă](#pornire-rapidă)
- [Exerciții de Laborator](#exerciții-de-laborator)
  - [Ex 1: HTTP](#exercițiul-1-explorarea-serviciului-http)
  - [Ex 2: DNS](#exercițiul-2-rezoluția-dns)
  - [Ex 3: SSH](#exercițiul-3-comunicația-ssh-criptată)
  - [Ex 4: FTP](#exercițiul-4-protocolul-ftp-multi-canal)
  - [Ex 5: HTTPS](#exercițiul-5-https-cu-tls-auto-semnat)
  - [Ex 6: REST](#exercițiul-6-nivelurile-de-maturitate-rest)
- [Demonstrații](#demonstrații)
- [Captură și Analiză](#captură-și-analiză-de-trafic)
- [Depanare](#-depanare-extinsă)
- [Curățare](#-procedura-completă-de-curățare)
- [Referințe](#referințe)

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `10roWSL`

**Arhitectura Mediului:**
```
Windows 11 → WSL2 → Ubuntu 22.04 (implicit) → Docker Engine → Portainer CE
```

**Credențiale Standard:**
| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |
| Server SSH | `labuser` | `labpass` |
| Server FTP | `labftp` | `labftp` |

---

## 💡 Filozofie de Învățare

**Erorile sunt normale și valoroase.**

În acest laborator vei întâlni erori - și asta e bine. Fiecare eroare este o oportunitate de a înțelege mai profund cum funcționează protocoalele de rețea.

Când vezi o eroare:
1. **Citește mesajul complet** - conține indicii despre cauză
2. **Verifică docs/depanare.md** - majoritatea problemelor sunt documentate
3. **Încearcă să înțelegi cauza** înainte să aplici soluția

Nimeni nu se naște știind networking. Toți experții au trecut prin aceleași erori pe care le vei întâlni tu.

**Sfat:** Înainte de a rula o comandă, oprește-te o secundă și prezice ce se va întâmpla. Verificarea predicției te ajută să înveți mai profund.

---

## 📥 Clonarea Laboratorului Acestei Săptămâni

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 10
git clone https://github.com/antonioclim/netROwsl.git SAPT10
cd SAPT10
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 10roWSL/
cd 10roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT10\
    └── 10roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker
        │   ├── debug/       # Container debug
        │   ├── dns-server/  # Server DNS personalizat
        │   ├── ftp-server/  # Server FTP
        │   ├── ssh-client/  # Client SSH Paramiko
        │   ├── ssh-server/  # Server OpenSSH
        │   └── www/         # Conținut web static
        ├── docs/            # Documentație suplimentară
        │   ├── depanare.md
        │   ├── glosar.md
        │   ├── peer_instruction.md
        │   ├── rezultate_asteptate.md
        │   └── sumar_teorie.md
        ├── homework/        # Teme pentru acasă
        │   └── exercises/   # tema1_dns_extins, tema2_client_rest
        ├── pcap/            # Fișiere de captură .pcap
        ├── scripts/         # Scripturi de automatizare
        │   └── utils/       # Utilitare Docker și rețea
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă
        │   ├── apps/        # demo_ftp, demo_ssh
        │   ├── exercises/   # ex_10_01_https, ex_10_02_rest_levels
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
cd /mnt/d/RETELE/SAPT10/10roWSL

# Verifică conținutul
ls -la
```

---

## 🖥️ Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor pentru Săptămâna 10

Navighează: **Home → local → Containers**

Vei vedea containerele specifice laboratorului:
- **week10_web** - Server HTTP Python (172.20.0.10:8000)
- **week10_dns** - Server DNS personalizat (172.20.0.53:5353/udp)
- **week10_ssh** - Server OpenSSH (172.20.0.22:2222)
- **week10_ftp** - Server FTP pyftpdlib (172.20.0.21:2121)
- **week10_ssh_client** - Client SSH Paramiko (172.20.0.100)
- **week10_debug** - Container utilitar (172.20.0.200)

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

### Vizualizarea Rețelei week10_labnet

1. Navighează: **Networks**
2. Click pe **week10_labnet**
3. Vezi configurația IPAM: 172.20.0.0/24, gateway 172.20.0.1
4. Vezi toate containerele conectate și IP-urile lor

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a observa diferențele între HTTP și HTTPS
- Pentru analiza rezoluției DNS și negocierii TLS

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
cd /mnt/d/RETELE/SAPT10/10roWSL

# Pornește mediul de laborator
python3 scripts/porneste_lab.py

# Testează serverul HTTP
curl -v http://localhost:8000/

# Testează DNS
dig @localhost -p 5353 web.lab.local
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 10

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

**Filtre pentru Trafic HTTP:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `http` | Tot traficul HTTP | Analiză generală HTTP |
| `http.request` | Doar cererile HTTP | Vezi ce trimite clientul |
| `http.response` | Doar răspunsurile HTTP | Vezi ce returnează serverul |
| `http.request.method == "GET"` | Doar cereri GET | Analiză cereri de citire |
| `http.request.method == "POST"` | Doar cereri POST | Analiză cereri de creare |
| `http.response.code == 200` | Răspunsuri OK | Succes |
| `http.response.code >= 400` | Erori HTTP | Depanare |
| `tcp.port == 8000` | Trafic server web | Doar serverul web |

**Filtre pentru Trafic DNS:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `dns` | Tot traficul DNS | Analiză generală DNS |
| `udp.port == 5353` | Server DNS laborator | Doar serverul DNS local |
| `dns.qry.name contains "lab.local"` | Domenii laborator | Filtrare domenii specifice |
| `dns.flags.response == 0` | Doar interogări | Cereri DNS |
| `dns.flags.response == 1` | Doar răspunsuri | Răspunsuri DNS |

**Filtre pentru Trafic SSH:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tcp.port == 2222` | Trafic SSH laborator | Conexiuni SSH |
| `ssh` | Protocol SSH | Analiză SSH |

**Notă:** Traficul SSH este criptat - vei vedea doar handshake-ul și pachetele criptate!

**Filtre pentru Trafic FTP:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `ftp` | Control FTP | Comenzi și răspunsuri FTP |
| `ftp-data` | Date FTP | Transferuri de fișiere |
| `tcp.port == 2121` | Port control FTP | Canalul de control |
| `tcp.portrange == 30000-30009` | Porturi passive | Canalul de date |
| `ftp.request.command == "USER"` | Autentificare | Username |
| `ftp.request.command == "PASS"` | Autentificare | Parolă |
| `ftp.request.command == "LIST"` | Listare | Conținut director |
| `ftp.request.command == "PASV"` | Mod pasiv | Activare passive mode |

**Filtre pentru Trafic HTTPS/TLS:**

| Filtru | Scop | Când să îl folosești |
|--------|------|----------------------|
| `tls` | Tot traficul TLS | Analiza securității |
| `tcp.port == 4443` | Port HTTPS laborator | Server HTTPS |
| `tls.handshake` | Handshake TLS | Negociere conexiune |
| `tls.handshake.type == 1` | Client Hello | Inițiere conexiune |
| `tls.handshake.type == 2` | Server Hello | Răspuns server |
| `tls.handshake.type == 11` | Certificate | Certificat server |

**Filtre pentru Rețeaua Laboratorului:**

| Filtru | Scop | Container |
|--------|------|-----------|
| `ip.addr == 172.20.0.10` | Server web | week10_web |
| `ip.addr == 172.20.0.53` | Server DNS | week10_dns |
| `ip.addr == 172.20.0.22` | Server SSH | week10_ssh |
| `ip.addr == 172.20.0.21` | Server FTP | week10_ftp |
| `ip.addr == 172.20.0.200` | Debug | week10_debug |
| `ip.addr == 172.20.0.0/24` | Toată rețeaua | Toate |

**Combinarea filtrelor:**
- ȘI: `http && tcp.port == 8000`
- SAU: `dns || http`
- NU: `!arp && !icmp`

### Analiza Diferențelor HTTP vs HTTPS

1. Capturează trafic HTTP pe portul 8000
2. Observă că poți vedea conținutul în clar (cereri, răspunsuri, date)
3. Capturează trafic HTTPS pe portul 4443
4. Observă că vezi doar handshake TLS și date criptate

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP normal |
| Albastru deschis | Trafic UDP (DNS) |
| Verde deschis | Trafic HTTP |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Text negru, fundal roșu | Erori TCP |
| Text negru, fundal galben | Avertismente, retransmisii |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT10\10roWSL\pcap\`
3. Nume fișier conform exercițiului:
   - `captura_s10_http.pcap` - Trafic HTTP
   - `captura_s10_dns.pcap` - Rezoluție DNS
   - `captura_s10_ssh.pcap` - Conexiuni SSH
   - `captura_s10_ftp.pcap` - Transfer FTP
   - `captura_s10_https.pcap` - TLS/HTTPS
4. Format: Wireshark/pcap sau pcapng (implicit)

---

## Prezentare Generală

În acest laborator lucrăm cu **protocoalele de nivel aplicație**: HTTP/HTTPS, DNS, SSH și FTP. Vom configura servere, vom analiza traficul în Wireshark și vom înțelege cum funcționează fiecare protocol prin experimente practice.

Mediul de laborator folosește containere Docker pentru a simula o infrastructură de rețea realistă. Fiecare serviciu rulează izolat, permițând analiza traficului fără interferențe externe.

**Ce înveți aici folosești direct când:**
- Configurezi un server web sau API
- Depanezi probleme de DNS sau conectivitate
- Securizezi conexiuni cu TLS/HTTPS
- Automatizezi transferuri de fișiere

---

## Diagrama Fluxului de Lucru

```
┌─────────────────────────────────────────────────────────────────┐
│                    WORKFLOW LABORATOR                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │PowerShell│───>│   WSL    │───>│  Docker  │───>│ Portainer│  │
│  │          │    │  Ubuntu  │    │ Compose  │    │   GUI    │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│       │               │               │               │         │
│       v               v               v               v         │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐  │
│  │   git    │    │ python3  │    │Containere│    │ Vizual-  │  │
│  │  clone   │    │ scripts  │    │  active  │    │  izare   │  │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘  │
│                                        │                        │
│                                        v                        │
│                               ┌────────────────┐                │
│                               │   Wireshark    │                │
│                               │(Windows nativ) │                │
│                               │Captură trafic  │                │
│                               └────────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** componentele principale ale unei cereri și răspuns HTTP, incluzând metodele, headerele și codurile de stare
2. **Explicați** diferențele dintre HTTP și HTTPS, descriind rolul TLS în securizarea comunicației
3. **Implementați** un server REST simplu care demonstrează nivelurile de maturitate Richardson (0-3)
4. **Analizați** traficul DNS folosind instrumente de captură, interpretând structura mesajelor de interogare și răspuns
5. **Comparați** modurile de transfer FTP (activ vs. pasiv) și implicațiile lor pentru traversarea firewall-urilor
6. **Evaluați** securitatea relativă a diferitelor protocoale de nivel aplicație

---

## Cerințe Preliminare

### Cunoștințe Necesare
- Fundamentele modelului TCP/IP și ale comunicării client-server
- Experiență de bază cu linia de comandă Linux/Windows
- Noțiuni elementare de programare Python
- Familiaritate cu conceptul de containere Docker

### Cerințe Software
- Windows 10/11 cu WSL2 activat (Ubuntu 22.04)
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git (opțional, pentru versionare)

### Cerințe Hardware
- Minim 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate de rețea

---

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT10/10roWSL

# Verifică cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă apar probleme, rulează asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT10/10roWSL

# Pornește toate serviciile
python3 scripts/porneste_lab.py

# Verifică starea serviciilor
python3 scripts/porneste_lab.py --stare
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Server Web | http://localhost:8000 | - |
| Server DNS | localhost:5353/udp | - |
| Server SSH | localhost:2222 | labuser / labpass |
| Server FTP | localhost:2121 | labftp / labftp |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

---

## Exerciții de Laborator

### Exercițiul 1: Explorarea Serviciului HTTP

**Obiectiv:** Înțelegerea structurii cererilor și răspunsurilor HTTP prin interacțiune directă cu serverul web containerizat.

**Durată estimată:** 20 minute

**Pași:**

1. Verificați că serverul web rulează:

   > 🔮 **PREDICȚIE:** Înainte de a rula comanda, ce cod de stare HTTP te aștepți să primești? Ce headere crezi că vor fi în răspuns?

   ```bash
   curl -v http://localhost:8000/
   ```

   > ✅ **VERIFICĂ:** Ai prezis corect codul 200? Ai identificat headerele `Server` și `Content-Type`?

2. Observați headerele răspunsului:
   - `Content-Type` - tipul MIME al conținutului
   - `Content-Length` - dimensiunea în octeți
   - `Server` - identificarea serverului

3. Testați diferite metode HTTP:

   > 🔮 **PREDICȚIE:** Ce diferență va fi între răspunsul la HEAD și cel la GET?

   ```bash
   # Cerere HEAD (doar headere, fără corp)
   curl -I http://localhost:8000/hello.txt
   
   # Cerere cu header personalizat
   curl -H "Accept-Language: ro" http://localhost:8000/
   ```

4. Folosiți containerul debug pentru teste din interiorul rețelei:

   > 🔮 **PREDICȚIE:** Va funcționa `http://web:8000/` din container? De ce?

   ```bash
   docker exec -it week10_debug curl http://web:8000/
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

**Ce trebuie observat:**
- Corelația dintre codul de stare HTTP și succesul operației
- Diferența dintre cererile din exterior (localhost) și interior (numele containerului)

---

### Exercițiul 2: Rezoluția DNS

**Obiectiv:** Analiza procesului de rezoluție DNS folosind serverul DNS personalizat și instrumentele de diagnosticare.

**Durată estimată:** 15 minute

**Pași:**

1. Interogați serverul DNS pentru înregistrările configurate:

   > 🔮 **PREDICȚIE:** Pentru domeniul `web.lab.local`, ce adresă IP te aștepți să primești? (Hint: verifică docker-compose.yml)

   ```bash
   # Din containerul debug
   docker exec -it week10_debug dig @dns-server -p 5353 web.lab.local
   
   # Din sistemul gazdă
   dig @localhost -p 5353 myservice.lab.local
   ```

2. Testați rezoluția pentru toate domeniile configurate:
   - `myservice.lab.local` → 10.10.10.10
   - `api.lab.local` → 10.10.10.20
   - `web.lab.local` → 172.20.0.10
   - `ssh.lab.local` → 172.20.0.22
   - `ftp.lab.local` → 172.20.0.21

3. Observați răspunsul pentru un domeniu inexistent:

   > 🔮 **PREDICȚIE:** Ce răspuns DNS vei primi pentru un domeniu care NU există? NOERROR sau NXDOMAIN?

   ```bash
   dig @localhost -p 5353 inexistent.lab.local
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

**Ce trebuie observat:**
- Structura răspunsului DNS (secțiunile QUESTION, ANSWER, AUTHORITY)
- Codul de răspuns pentru domenii inexistente (NXDOMAIN)

---

### Exercițiul 3: Comunicația SSH Criptată

**Obiectiv:** Demonstrarea comunicației securizate prin SSH și analiza procesului de autentificare.

**Durată estimată:** 15 minute

**Pași:**

1. Conectați-vă la serverul SSH din linia de comandă:

   > 🔮 **PREDICȚIE:** Ce avertisment vei vedea la prima conectare? De ce apare?

   ```bash
   ssh -p 2222 labuser@localhost
   # Parolă: labpass
   ```

2. Executați comenzi pe serverul remote:
   ```bash
   whoami
   hostname
   ls -la
   exit
   ```

3. Rulați demonstrația Paramiko din container:
   ```bash
   docker exec -it week10_ssh_client python /app/paramiko_client.py
   ```

4. Sau rulați scriptul local:
   ```bash
   python3 src/apps/demo_ssh.py
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

**Ce trebuie observat:**
- Avertismentul despre cheia gazdei la prima conectare
- Imposibilitatea de a citi conținutul traficului SSH în Wireshark (criptat)

---

### Exercițiul 4: Protocolul FTP Multi-Canal

**Obiectiv:** Înțelegerea separării între canalul de control și canalul de date în FTP.

**Durată estimată:** 15 minute

**Pași:**

1. Conectați-vă la serverul FTP:

   > 🔮 **PREDICȚIE:** Câte conexiuni TCP va deschide clientul FTP? (Hint: FTP are două canale)

   ```bash
   # Folosind clientul ftp integrat
   ftp localhost 2121
   # Utilizator: labftp
   # Parolă: labftp
   ```

2. Executați comenzi FTP de bază:
   ```ftp
   pwd
   ls
   passive
   ls
   quit
   ```

3. Rulați demonstrația Python:
   ```bash
   python3 src/apps/demo_ftp.py
   ```

4. Din containerul debug, folosiți lftp:
   ```bash
   docker exec -it week10_debug lftp -u labftp,labftp ftp-server:2121
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

**Ce trebuie observat:**
- Diferența între modul activ și pasiv
- Porturile utilizate pentru canalul de date (30000-30009)

---

### Exercițiul 5: HTTPS cu TLS Auto-Semnat

**Obiectiv:** Implementarea unui server HTTPS cu certificat auto-semnat și înțelegerea negocierii TLS.

**Durată estimată:** 25 minute

**Pași:**

1. Rulați exercițiul HTTPS:
   ```bash
   python3 src/exercises/ex_10_01_https.py
   ```

2. Într-un terminal separat, testați conexiunea:

   > 🔮 **PREDICȚIE:** Ce avertisment vei primi de la curl? De ce?

   ```bash
   # Ignoră verificarea certificatului pentru certificate auto-semnate
   curl -k https://localhost:4443/
   
   # Vedeți detaliile certificatului
   curl -kv https://localhost:4443/ 2>&1 | grep -A 5 "Server certificate"
   ```

3. Capturați traficul TLS cu Wireshark:

   > 🔮 **PREDICȚIE:** Vei putea citi conținutul răspunsului HTTPS în Wireshark?

   - Filtru: `tcp.port == 4443`
   - Observați handshake-ul TLS (Client Hello, Server Hello, Certificate)

4. Comparați cu HTTP necriptat:
   - Filtru: `tcp.port == 8000`
   - Observați că conținutul este vizibil în clar

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 5
```

**Ce trebuie observat:**
- Diferența dintre traficul HTTP (text vizibil) și HTTPS (criptat)
- Etapele negocierii TLS în Wireshark
- Avertismentul pentru certificate auto-semnate

---

### Exercițiul 6: Nivelurile de Maturitate REST

**Obiectiv:** Implementarea și compararea celor 4 niveluri de maturitate REST (Richardson Maturity Model).

**Durată estimată:** 30 minute

**Pași:**

1. Porniți serverul REST:
   ```bash
   python3 src/exercises/ex_10_02_rest_levels.py
   ```

2. Testați Nivelul 0 (RPC):

   > 🔮 **PREDICȚIE:** La Nivelul 0, toate cererile vor fi POST pe același endpoint. De ce nu e considerat RESTful?

   ```bash
   curl http://localhost:5000/api/nivel0
   
   curl -X POST -H "Content-Type: application/json" \
        -d '{"actiune": "creeaza", "date": {"nume": "Produs"}}' \
        http://localhost:5000/api/nivel0
   ```

3. Testați Nivelul 1 (Resurse):
   ```bash
   curl http://localhost:5000/api/nivel1/produse
   curl -X POST -H "Content-Type: application/json" \
        -d '{"nume": "Laptop"}' \
        http://localhost:5000/api/nivel1/produse
   ```

4. Testați Nivelul 2 (Verbe HTTP):

   > 🔮 **PREDICȚIE:** Ce cod de stare vei primi pentru DELETE reușit? 200, 201 sau 204?

   ```bash
   curl http://localhost:5000/api/nivel2/produse
   curl -X POST -H "Content-Type: application/json" \
        -d '{"nume": "Monitor"}' \
        http://localhost:5000/api/nivel2/produse
   curl -X PUT -H "Content-Type: application/json" \
        -d '{"nume": "Monitor 4K"}' \
        http://localhost:5000/api/nivel2/produse/1
   curl -X DELETE http://localhost:5000/api/nivel2/produse/1
   ```

5. Testați Nivelul 3 (HATEOAS):

   > 🔮 **PREDICȚIE:** Ce vei găsi în plus în răspunsul de la Nivelul 3 față de Nivelul 2?

   ```bash
   curl http://localhost:5000/api/nivel3/produse
   # Observați linkurile _links în răspuns
   ```

6. Rulați auto-testarea:
   ```bash
   python3 src/exercises/ex_10_02_rest_levels.py --selftest
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 6
```

**Ce trebuie observat:**
- Evoluția de la un singur endpoint (L0) la resurse cu linkuri (L3)
- Utilizarea corectă a codurilor de stare HTTP la fiecare nivel

---

## Demonstrații

### Demonstrație 1: Tur Complet al Serviciilor

Demonstrație automată care prezintă toate serviciile din laborator:

```bash
python3 scripts/ruleaza_demo.py --demo 1
```

**Ce se va observa:**
- Pornirea și verificarea tuturor containerelor
- Teste de conectivitate pentru fiecare serviciu
- Exemple de interacțiune cu HTTP, DNS, SSH și FTP

### Demonstrație 2: Comparație REST

```bash
python3 scripts/ruleaza_demo.py --demo 2
```

**Ce se va observa:**
- Diferențele vizuale între nivelurile de maturitate REST
- Evoluția răspunsurilor de la RPC la HATEOAS

---

## Captură și Analiză de Trafic

### Capturarea Traficului

```bash
# În terminalul Ubuntu
# Pornire captură
python3 scripts/captura_trafic.py --interfata eth0 --iesire pcap/week10_captura.pcap

# Sau folosiți Wireshark direct pe Windows
# Selectați interfața vEthernet (WSL)
```

### Filtre Wireshark Recomandate

```
# Trafic HTTP
http or tcp.port == 8000

# Trafic DNS
udp.port == 5353

# Trafic SSH
tcp.port == 2222 or tcp.port == 22

# Trafic FTP (control și date)
tcp.port == 2121 or tcp.portrange == 30000-30009

# Trafic HTTPS/TLS
tcp.port == 4443 or tls

# Doar traficul din rețeaua laboratorului
ip.addr == 172.20.0.0/24
```

---

## Oprire și Curățare

### La Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT10/10roWSL

# Oprirea containerelor (Portainer rămâne activ!)
python3 scripts/opreste_lab.py

# Verificare oprire
docker ps
# Ar trebui să vezi doar: portainer
```

### Curățare Completă (Înainte de Săptămâna Următoare)

```bash
# Elimină toate containerele, rețelele și volumele acestei săptămâni
python3 scripts/curata.py --complet

# Verificare curățare
docker system df
```

---

## Teme pentru Acasă

Consultați directorul `homework/` pentru exercițiile de realizat acasă.

### Tema 1: Server DNS Extins
Extindeți serverul DNS pentru a suporta înregistrări MX și CNAME.

### Tema 2: Client REST Complet
Implementați un client Python care interacționează cu toate cele 4 niveluri REST.

---

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Rețeaua Laboratorului Week 10                     │
│                      week10_labnet (172.20.0.0/24)                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   web       │  │ dns-server  │  │ ssh-server  │  │ ftp-server  │ │
│  │ 172.20.0.10 │  │ 172.20.0.53 │  │ 172.20.0.22 │  │ 172.20.0.21 │ │
│  │   :8000     │  │  :5353/udp  │  │    :22      │  │   :2121     │ │
│  │  (HTTP)     │  │   (DNS)     │  │   (SSH)     │  │   (FTP)     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │                │        │
│         └────────────────┴────────────────┴────────────────┘        │
│                                   │                                  │
│  ┌─────────────┐  ┌─────────────┐ │                                  │
│  │ ssh-client  │  │   debug     │ │                                  │
│  │172.20.0.100 │  │172.20.0.200 │ │                                  │
│  │ (Paramiko)  │  │(dig,curl,..)│ │                                  │
│  └─────────────┘  └─────────────┘ │                                  │
│                                   │                                  │
├───────────────────────────────────┼──────────────────────────────────┤
│                          Docker Host                                 │
│                                   │                                  │
│    Porturi expuse:  8000 ←───────┤                                  │
│                     5353/udp ←────┤                                  │
│                     2222 ←────────┤                                  │
│                     2121 ←────────┤                                  │
│                                                                      │
│    Portainer (global): http://localhost:9000                         │
└─────────────────────────────────────────────────────────────────────┘
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

### Probleme Specifice Săptămânii 10

**Problemă:** Server DNS nu răspunde
```bash
# Verifică că containerul rulează
docker ps | grep week10_dns

# Verifică log-urile
docker logs week10_dns

# Testează manual
dig @localhost -p 5353 web.lab.local
```

**Problemă:** Conexiune SSH refuzată
```bash
# Verifică că serverul SSH rulează
docker ps | grep week10_ssh

# Verifică log-urile
docker logs week10_ssh

# Testează conectivitatea
nc -zv localhost 2222

# Resetează known_hosts dacă e necesar
ssh-keygen -R "[localhost]:2222"
```

**Problemă:** Server FTP nu acceptă conexiuni passive
```bash
# Verifică că porturile passive sunt expuse
docker port week10_ftp

# Verifică log-urile
docker logs week10_ftp

# Testează conexiunea
ftp localhost 2121
```

**Problemă:** Certificat HTTPS auto-semnat respins
```bash
# Folosește -k pentru a ignora verificarea
curl -k https://localhost:4443/

# Sau în browser, acceptă excepția de securitate
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week10_labnet

# Verifică DNS în container
docker exec week10_debug cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 8000

# Oprește procesul sau folosește alt port
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT10/10roWSL

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
docker stop $(docker ps -q --filter "name=week10_")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite
docker network prune -f

# Elimină volumele acestei săptămâni
docker volume rm week10_ssh_data week10_ftp_data 2>/dev/null

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

## Fundamente Teoretice

### Protocolul HTTP/HTTPS

HTTP (Hypertext Transfer Protocol) operează la nivelul aplicație, folosind TCP ca transport. Structura unei cereri include: linia de cerere (metodă, URI, versiune), headere și opțional un corp. HTTPS adaugă un strat TLS/SSL pentru criptare, autentificare și integritate.

### Modelul REST

REST (Representational State Transfer) definește un stil arhitectural pentru sisteme distribuite. Modelul de maturitate Richardson clasifică API-urile în 4 niveluri:
- **Nivelul 0:** HTTP ca tunel pentru RPC
- **Nivelul 1:** Resurse individuale cu URI-uri distincte
- **Nivelul 2:** Utilizarea corectă a verbelor HTTP
- **Nivelul 3:** HATEOAS - hypermedia ca motor al stării aplicației

### Protocolul DNS

DNS (Domain Name System) traduce nume de domenii în adrese IP. Mesajele DNS conțin secțiuni pentru întrebare, răspuns, autoritate și informații adiționale. Tipurile comune de înregistrări includ A (IPv4), AAAA (IPv6), MX (mail) și CNAME (alias).

### Protocolul SSH

SSH (Secure Shell) oferă comunicație criptată pentru acces remote. Arhitectura include trei straturi: transport (criptare, integritate), autentificare utilizator și conexiune (multiplexare canale).

### Protocolul FTP

FTP (File Transfer Protocol) folosește două conexiuni separate: canalul de control (port 21) pentru comenzi și canalul de date pentru transferuri. Modul pasiv rezolvă problemele de traversare a firewall-urilor prin inițierea conexiunii de date de către client.

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- Fielding, R. T. (2000). *Architectural Styles and the Design of Network-based Software Architectures*. Doctoral dissertation, University of California, Irvine.
- RFC 2616 - Hypertext Transfer Protocol -- HTTP/1.1
- RFC 8446 - The Transport Layer Security (TLS) Protocol Version 1.3
- RFC 1035 - Domain Names - Implementation and Specification
- RFC 4253 - The Secure Shell (SSH) Transport Layer Protocol
- RFC 959 - File Transfer Protocol

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
