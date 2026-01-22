# Săptămâna 3: Programare în Rețea - Broadcast, Multicast și Tunel TCP

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
>
> by Revolvix

---

## ⚠️ Notificare Mediu

Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

**Repository:** https://github.com/antonioclim/netROwsl
**Folderul Acestei Săptămâni:** `03roWSL`

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

# Clonează Săptămâna 3
git clone https://github.com/antonioclim/netROwsl.git SAPT3
cd SAPT3
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 03roWSL/
cd 03roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Completă a Directoarelor

După clonare, structura va fi:
```
D:\RETELE\
└── SAPT3\
    └── 03roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        ├── docs/            # Documentație suplimentară
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
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
cd /mnt/d/RETELE/SAPT3/03roWSL

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
- **Nume** - Identificatorul containerului
- **Stare** - Running/Stopped/Paused
- **Imagine** - Imaginea Docker folosită
- **Creat** - Data creării
- **Adresă IP** - Adresa IP în rețeaua Docker
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

### Vizualizarea Rețelei week3_network

1. Navighează: **Networks → week3_network**
2. Vezi configurația IPAM curentă: 172.20.0.0/24
3. Observă containerele conectate și adresele lor IP:
   - server: 172.20.0.10
   - router: 172.20.0.254
   - client: 172.20.0.100
   - receiver: 172.20.0.101

### Modificarea Configurației de Rețea

Pentru a modifica subrețeaua sau adresele IP:
1. Oprește containerele care folosesc rețeaua
2. Editează fișierul `docker/docker-compose.yml`:
   ```yaml
   networks:
     week3_network:
       ipam:
         config:
           - subnet: 172.20.0.0/24  # Modifică subrețeaua aici
             gateway: 172.20.0.1    # Modifică gateway-ul aici
   ```
3. Recreează mediul:
   ```bash
   cd /mnt/d/RETELE/SAPT3/03roWSL
   docker-compose -f docker/docker-compose.yml down
   docker-compose -f docker/docker-compose.yml up -d
   ```
4. Verifică în Portainer: Networks → vezi noua configurație

### Modificarea Porturilor Containerului

1. În Portainer: selectează containerul → "Inspect" → derulează la "HostConfig.PortBindings"
2. Pentru a modifica permanent, editează `docker/docker-compose.yml`:
   ```yaml
   ports:
     - "8080:8080"   # Format: "port_host:port_container"
     - "9090:9090"   # Tunel TCP
   ```
3. Recreează containerul:
   ```bash
   docker-compose -f docker/docker-compose.yml down
   docker-compose -f docker/docker-compose.yml up -d
   ```
4. Verifică: Noile porturi apar în lista de containere din Portainer

**⚠️ NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## 🦈 Configurarea și Utilizarea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- **ÎNAINTE** de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru demonstrații care necesită vizualizarea traficului în timp real
- Pentru a observa diferențele dintre broadcast, multicast și unicast

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

Cu Wireshark capturând (vei vedea pachete apărând în timp real), rulează exercițiile de laborator:

```bash
# În terminalul Ubuntu
docker exec -it week3_client bash

# Exemplu pentru broadcast
python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 3

# Exemplu pentru multicast
python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod sender --numar 3
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark Esențiale pentru Săptămâna 3

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

| Filtru | Scop | Exemplu Utilizare |
|--------|------|-------------------|
| `eth.dst == ff:ff:ff:ff:ff:ff` | Trafic broadcast (Layer 2) | Detectare pachete broadcast |
| `ip.dst == 255.255.255.255` | Broadcast limitat (Layer 3) | Broadcast UDP |
| `ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255` | Trafic multicast | Toate grupurile multicast |
| `ip.dst == 239.0.0.1` | Grup multicast specific | Grup laborator |
| `igmp` | Mesaje IGMP | Join/Leave grup multicast |
| `udp.port == 5007` | Port broadcast laborator | Trafic exercițiu 1 |
| `udp.port == 5008` | Port multicast laborator | Trafic exercițiu 2 |
| `tcp.port == 8080` | Server Echo TCP | Conexiuni directe |
| `tcp.port == 9090` | Tunel TCP | Conexiuni prin relay |
| `ip.addr == 172.20.0.0/24` | Tot traficul rețelei lab | Filtrare per rețea |

**Combinarea filtrelor:**
- ȘI: `udp.port == 5007 && eth.dst == ff:ff:ff:ff:ff:ff`
- SAU: `tcp.port == 8080 || tcp.port == 9090`
- NU: `!arp && !dns`

### Identificarea Tipurilor de Trafic în Wireshark

| Tip Trafic | Adresa MAC Destinație | Adresa IP Destinație | Caracteristici |
|------------|----------------------|---------------------|----------------|
| **Unicast** | Adresă specifică (00:...) | IP specific (172.20.0.10) | Punct-la-punct |
| **Broadcast** | ff:ff:ff:ff:ff:ff | 255.255.255.255 sau .255 | Toate stațiile |
| **Multicast** | 01:00:5e:... | 224.x.x.x - 239.x.x.x | Doar membrii grupului |

### Analiza IGMP pentru Multicast

Filtru: `igmp`

Tipuri de mesaje IGMP de observat:
- **Membership Query** (Type 0x11): Router întreabă despre grupuri
- **Membership Report V2** (Type 0x16): Stație se înscrie în grup
- **Leave Group** (Type 0x17): Stație părăsește grupul

### Urmărirea Tunelării TCP

1. Aplică filtrul: `tcp.port == 9090 || tcp.port == 8080`
2. Observă două conexiuni TCP separate:
   - Client → Router (port 9090)
   - Router → Server (port 8080)
3. Click dreapta pe un pachet → **Follow → TCP Stream**
4. Comută între stream-uri pentru a vedea ambele conexiuni

### Codificarea Culorilor în Wireshark

| Culoare | Semnificație |
|---------|--------------|
| Violet deschis | Trafic TCP |
| Albastru deschis | Trafic UDP |
| Verde deschis | Trafic HTTP |
| Text negru, fundal roșu | Erori, checksum-uri greșite |
| Text negru, fundal galben | Avertismente, retransmisii |
| Fundal gri | TCP SYN/FIN (evenimente conexiune) |
| Verde-albăstrui | Pachete IGMP |

### Salvarea Capturilor

1. **File → Save As** (sau Ctrl+Shift+S)
2. Navighează la: `D:\RETELE\SAPT3\03roWSL\pcap\`
3. Nume fișier sugestiv: `captura_broadcast_multicast.pcap`
4. Format: Wireshark/pcap sau pcapng (implicit)

### Exportarea Datelor pentru Analiză

1. **File → Export Packet Dissections → As CSV**
2. Selectează câmpurile de exportat
3. Salvează în folderul `artifacts/` pentru procesare Python

---

## Prezentare Generală

Această sesiune de laborator explorează mecanismele fundamentale de comunicare în rețea prin intermediul programării cu socket-uri: transmisia broadcast, comunicarea multicast și tunelarea TCP. Aceste moduri de comunicare reprezintă piloni esențiali ai arhitecturilor distribuite moderne, de la descoperirea serviciilor în rețele locale până la sisteme multimedia și infrastructuri VPN.

Transmisia **broadcast** permite unui singur emițător să comunice simultan cu toate dispozitivele dintr-un segment de rețea, eliminând necesitatea cunoașterii prealabile a destinatarilor. **Multicast** extinde acest concept prin crearea grupurilor de interes, unde doar stațiile membre primesc traficul, optimizând astfel utilizarea lățimii de bandă. **Tunelarea TCP** oferă mecanisme de redirecționare transparentă a conexiunilor, fundamentale pentru proxy-uri, load balancere și rețele virtuale private.

Exercițiile practice utilizează containere Docker pentru simularea unei topologii de rețea izolate, permițând observarea comportamentului protocoalelor fără a afecta infrastructura reală. Analiza pachetelor cu Wireshark completează înțelegerea teoretică prin vizualizarea directă a structurii cadrelor și fluxurilor de date.

### 💡 Gândește Concret Înainte de Abstract

Înainte de a te scufunda în cod, înțelege conceptele prin analogii din viața reală:

| Concept | Analogie | Ce înseamnă |
|---------|----------|-------------|
| **Broadcast** | Anunț pe megafon în piață | Toți aud, indiferent dacă vor sau nu |
| **Multicast** | Grup de WhatsApp | Doar membrii grupului primesc mesajele |
| **IGMP Join** | Abonare la newsletter | Te înscrii activ pentru a primi |
| **TTL** | Bilet de metrou valabil N stații | La fiecare router traversat, "o stație" se consumă |
| **Tunel TCP** | Poștaș care redirecționează | Primește scrisori și le trimite mai departe |
| **SO_BROADCAST** | Permis de megafon | Fără el, sistemul refuză să transmită broadcast |

**Revino la aceste analogii** când întâmpini dificultăți cu conceptele tehnice sau cu depanarea.

### 📋 Auto-Evaluare

Înainte de a începe exercițiile, verifică-ți cunoștințele:
→ [Întrebări de Recapitulare](docs/intrebari_recapitulare.md)

Dacă nu poți răspunde la întrebările REMEMBER, recitește [Rezumatul Teoretic](docs/rezumat_teoretic.md).



## Obiective de Învățare

La finalul acestei sesiuni de laborator, veți fi capabili să:

1. **Identificați** diferențele dintre comunicarea unicast, broadcast și multicast la nivel conceptual și practic
2. **Explicați** mecanismul IGMP pentru gestionarea apartenenței la grupuri multicast și rolul TTL în propagarea pachetelor
3. **Implementați** aplicații client-server folosind socket-uri UDP cu opțiuni SO_BROADCAST și IP_ADD_MEMBERSHIP
4. **Construiți** un tunel TCP bidirecțional pentru redirecționarea transparentă a conexiunilor între endpoint-uri
5. **Analizați** traficul de rețea capturat, identificând tipare specifice broadcast-ului, multicast-ului și tunelării
6. **Evaluați** avantajele și dezavantajele fiecărui mod de comunicare în scenarii practice

## Cerințe Preliminare

### Cunoștințe Necesare

- Fundamentele modelului TCP/IP și adresării IPv4
- Programare Python de bază (funcții, clase, module)
- Diferențele dintre protocoalele TCP și UDP
- Utilizarea liniei de comandă (PowerShell, Bash)

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git (opțional, recomandat)

### Cerințe Hardware

- Minimum 8GB RAM (16GB recomandat)
- 10GB spațiu liber pe disc
- Conectivitate la rețea

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschideți terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT3/03roWSL

# Verificați cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă există probleme, rulați asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT3/03roWSL

# Porniți toate serviciile (fără receiver)
python3 scripts/porneste_lab.py

# Sau cu toate serviciile (inclusiv receiver pentru broadcast/multicast)
python3 scripts/porneste_lab.py --broadcast

# Verificați că totul funcționează
python3 scripts/porneste_lab.py --status
```

### Accesarea Serviciilor

| Serviciu | URL/Port | Credențiale |
|----------|----------|-------------|
| Portainer | http://localhost:9000 | stud / studstudstud |
| Server Echo | localhost:8080 | - |
| Tunel TCP | localhost:9090 | - |
| Receiver Broadcast | 172.20.0.101:5007 | - |

**Notă:** Portainer rulează global și nu trebuie pornit/oprit cu laboratorul.

## Exerciții de Laborator

### Exercițiul 1: Transmisie UDP Broadcast

**Obiectiv:** Implementarea și testarea comunicării broadcast folosind socket-uri UDP cu opțiunea SO_BROADCAST.

**Durată estimată:** 30 minute

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` cu filtrul `udp.port == 5007 && eth.dst == ff:ff:ff:ff:ff:ff` ÎNAINTE de a începe exercițiul.

**Fundament teoretic:**
Broadcast-ul permite transmiterea unui singur pachet către toate stațiile dintr-un segment de rețea. Adresa de broadcast limitat (255.255.255.255) nu traversează routere, fiind confinată la rețeaua locală. Socket-urile necesită activarea explicită a opțiunii SO_BROADCAST pentru a permite astfel de transmisii.


**🔮 PREDICȚIE:** Înainte de a rula, răspunde mental:
- Ce adresă MAC va avea pachetul broadcast la Layer 2? (Hint: începe cu ff:)
- Dacă sunt 4 containere în rețea, câte vor primi mesajul broadcast?
- Ce se întâmplă dacă receptorul face bind la IP-ul său specific în loc de 0.0.0.0?

**Pași:**

1. Porniți containerul receiver într-un terminal:
   ```bash
   docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod receiver
   ```

2. Într-un alt terminal, porniți emițătorul:
   ```bash
   docker exec -it week3_server python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 5
   ```

3. Observați mesajele primite și notați:
   - Adresa sursă a pachetelor
   - Timpul de propagare
   - Comportamentul când multiple receivere sunt active

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 1
```

**Întrebări de reflecție:**
- De ce este necesară opțiunea SO_BROADCAST?
- Ce se întâmplă dacă adresa de broadcast este înlocuită cu o adresă unicast?

---

### Exercițiul 2: Comunicare UDP Multicast

**Obiectiv:** Configurarea socket-urilor pentru comunicare multicast și înțelegerea mecanismului IGMP de înscriere în grupuri.

**Durată estimată:** 35 minute

**Pregătire Wireshark:** Schimbă filtrul la `igmp || (udp.port == 5008 && ip.dst == 239.0.0.1)` pentru a observa traficul multicast și mesajele IGMP.

**Fundament teoretic:**
Multicast-ul permite comunicarea eficientă unul-la-mulți prin utilizarea adreselor din intervalul 224.0.0.0 - 239.255.255.255. Receptorii se înscriu în grupuri folosind protocolul IGMP (Internet Group Management Protocol), iar rețeaua livrează pachetele doar membrilor activi. Spre deosebire de broadcast, multicast-ul poate traversa routere configurate corespunzător.


**🔮 PREDICȚIE:** Înainte de a rula receptorul, răspunde:
- Ce tip de mesaj IGMP va trimite receptorul când pornește? (Join sau Leave?)
- Ce vei vedea în Wireshark dacă filtrezi cu `igmp`?
- De ce multicast-ul este mai eficient decât broadcast-ul pentru 10 receptori din 100 de dispozitive?

**Pași:**

1. Porniți primul receptor:
   ```bash
   docker exec -it week3_client python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver
   ```

2. Porniți al doilea receptor (terminal separat):
   ```bash
   docker exec -it week3_receiver python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver
   ```

3. Transmiteți mesaje către grup:
   ```bash
   docker exec -it week3_server python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod sender --numar 5
   ```

4. Verificați înscrierea în grup IGMP:
   ```bash
   docker exec week3_client cat /proc/net/igmp
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 2
```

**Întrebări de reflecție:**
- Care este diferența dintre broadcast și multicast din perspectiva eficienței rețelei?
- Ce rol joacă TTL în propagarea pachetelor multicast?

---

### Exercițiul 3: Tunel TCP Bidirecțional

**Obiectiv:** Construirea unui releu TCP care redirecționează transparent conexiunile între client și server.

**Durată estimată:** 40 minute

**Pregătire Wireshark:** Aplică filtrul `tcp.port == 9090 || tcp.port == 8080` pentru a observa ambele conexiuni TCP.

**Fundament teoretic:**
Tunelarea TCP implică acceptarea conexiunilor pe un port și redirecționarea traficului către o destinație diferită. Acest pattern este fundamental pentru proxy-uri, load balancere și gateway-uri de securitate. Implementarea corectă necesită gestionarea bidirecțională a datelor și tratarea elegantă a deconectărilor.


**🔮 PREDICȚIE:** Înainte de a testa tunelul, răspunde:
- Câte conexiuni TCP separate vor exista? (1, 2 sau 3?)
- Ce IP sursă va vedea serverul echo - IP-ul clientului sau IP-ul routerului/tunelului?
- Câte segmente TCP SYN vei vedea în Wireshark pentru o singură cerere prin tunel?

**Pași:**

1. Verificați că serverul echo funcționează:
   ```bash
   echo "Test direct" | docker exec -i week3_client nc 172.20.0.10 8080
   ```

2. Testați conexiunea prin tunel:
   ```bash
   echo "Test prin tunel" | docker exec -i week3_client nc 172.20.0.254 9090
   ```

3. Examinați codul tunelului și identificați:
   - Cum se creează conexiunea către server
   - Cum se gestionează traficul bidirecțional
   - Cum se tratează deconectările

4. Monitorizați conexiunile active:
   ```bash
   docker exec week3_router ss -tnp
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

**Întrebări de reflecție:**
- De ce este necesară utilizarea thread-urilor pentru relay-ul bidirecțional?
- Ce avantaje oferă un tunel TCP față de conexiunea directă?

---

### Exercițiul 4: Analiză cu Wireshark

**Obiectiv:** Capturarea și analiza traficului de rețea pentru identificarea tiparelor specifice fiecărui tip de comunicare.

**Durată estimată:** 25 minute

**Pași:**

1. Porniți captura de trafic:
   ```bash
   python3 scripts/captureaza_trafic.py --container server --durata 60 --output pcap/analiza_week3.pcap
   ```

2. În timpul capturii, executați exercițiile 1-3

3. Deschideți fișierul pcap în Wireshark:
   ```powershell
   # În PowerShell
   & "C:\Program Files\Wireshark\Wireshark.exe" "D:\RETELE\SAPT3\03roWSL\pcap\analiza_week3.pcap"
   ```

4. Aplicați filtrele și documentați observațiile:
   ```
   # Trafic broadcast
   eth.dst == ff:ff:ff:ff:ff:ff
   
   # Trafic multicast
   ip.dst >= 239.0.0.0 and ip.dst <= 239.255.255.255
   
   # Mesaje IGMP
   igmp
   
   # Trafic tunel
   tcp.port == 9090 or tcp.port == 8080
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

## Demonstrații

### Demo 1: Broadcast în Acțiune

Demonstrație automată care ilustrează propagarea mesajelor broadcast către multiple receptoare.

```bash
python3 scripts/ruleaza_demo.py --demo broadcast
```

**Ce trebuie observat:**
- Toate containerele primesc același mesaj simultan
- Adresa MAC destinație este ff:ff:ff:ff:ff:ff
- Nu există confirmare de primire (UDP)

### Demo 2: Grupuri Multicast

Demonstrație a înscrierii și comunicării în grupuri multicast.

```bash
python3 scripts/ruleaza_demo.py --demo multicast
```

**Ce trebuie observat:**
- Rapoartele IGMP la înscriere și părăsire
- Doar membrii grupului primesc mesaje
- Adresa IP destinație este în intervalul multicast

### Demo 3: Tunelare TCP

Demonstrație a redirecționării transparente prin tunel.

```bash
python3 scripts/ruleaza_demo.py --demo tunel
```

**Ce trebuie observat:**
- Două conexiuni TCP separate (client-tunel, tunel-server)
- Datele sunt relayate transparent
- Conexiunile se închid sincronizat

## Captură și Analiză Pachete

### Capturarea Traficului

```bash
# Pornire captură (în terminalul Ubuntu)
python3 scripts/captureaza_trafic.py --container eth0 --output pcap/captura_week3.pcap

# Sau folosind Wireshark direct pe Windows
# Selectați interfața vEthernet (WSL)
```

### Filtre Wireshark Recomandate

```
# Broadcast UDP
udp and eth.dst == ff:ff:ff:ff:ff:ff

# Multicast specific
ip.dst == 239.0.0.1 and udp.port == 5008

# Tot traficul laboratorului
ip.addr == 172.20.0.0/24

# Trafic TCP tunel
tcp.port == 8080 or tcp.port == 9090
```

## Oprire și Curățare

### Sfârșitul Sesiunii

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT3/03roWSL

# Opriți toate containerele de laborator (Portainer rămâne activ!)
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

Consultați directorul `homework/` pentru exercițiile de rezolvat acasă.

### Tema 1: Receiver Broadcast cu Statistici
Extindeți receiver-ul UDP pentru a colecta și afișa statistici detaliate despre traficul primit.

### Tema 2: Aplicație Chat Multicast
Implementați o aplicație de chat bazată pe multicast cu suport pentru mai mulți utilizatori.

### Tema 3: Tunel TCP cu Logging și Metrici
Îmbunătățiți tunelul TCP cu logging detaliat, metrici de performanță și limite de conexiuni.

## Depanare

### Probleme Frecvente

#### Eroare: `OSError: [Errno 10013] Permission denied`
**Soluție:** Rulați în containerele Docker unde permisiunile sunt deja configurate.

#### Eroare: `Address already in use`
**Soluție:** Opriți procesele anterioare sau reporniți containerul:
```bash
docker restart week3_server
```

#### Mesajele broadcast nu sunt primite
**Soluție:** Verificați că receiver-ul este legat la `0.0.0.0`, nu la o adresă IP specifică.

#### Multicast nu funcționează
**Soluție:** Verificați înscrierea în grup:
```bash
docker exec week3_client cat /proc/net/igmp | grep 239
```

Consultați `docs/depanare.md` pentru mai multe soluții.

## Fundament Teoretic

### Broadcast vs Multicast vs Unicast

| Caracteristică | Unicast | Broadcast | Multicast |
|---------------|---------|-----------|-----------|
| Destinatari | Unul | Toți din segment | Membrii grupului |
| Eficiență | O copie/destinatar | O copie/segment | O copie/grup |
| Traversare routere | Da | Nu (limitat) | Da (cu suport) |
| Adresă exemplu | 172.20.0.10 | 255.255.255.255 | 239.0.0.1 |

### Opțiuni Socket Relevante

- **SO_BROADCAST**: Permite transmisia broadcast
- **SO_REUSEADDR**: Permite rebindarea rapidă a portului
- **IP_ADD_MEMBERSHIP**: Înscrie socket-ul într-un grup multicast
- **IP_MULTICAST_TTL**: Controlează propagarea multicast
- **IP_MULTICAST_LOOP**: Controlează primirea propriilor mesaje

### Structura IGMP

Internet Group Management Protocol gestionează apartenența la grupuri multicast:
- **Membership Query**: Router-ul întreabă ce grupuri sunt active
- **Membership Report**: Stația raportează apartenența la grup
- **Leave Group**: Stația notifică părăsirea grupului

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 919 - Broadcasting Internet Datagrams
- RFC 1112 - Host Extensions for IP Multicasting
- RFC 2236 - Internet Group Management Protocol, Version 2

## Diagrama Arhitecturii

```
┌─────────────────────────────────────────────────────────────────┐
│                      Rețea Docker: 172.20.0.0/24                │
│                                                                 │
│   ┌─────────────┐         ┌─────────────┐         ┌───────────┐│
│   │   SERVER    │         │   ROUTER    │         │  CLIENT   ││
│   │ 172.20.0.10 │◄────────│172.20.0.254 │◄────────│172.20.0.100│
│   │  Port 8080  │  Tunel  │  Port 9090  │         │ (testare) ││
│   │ (Echo TCP)  │         │ (Relay TCP) │         │           ││
│   └─────────────┘         └─────────────┘         └───────────┘│
│                                                                 │
│                           ┌─────────────┐                       │
│                           │  RECEIVER   │                       │
│                           │172.20.0.101 │                       │
│                           │  Port 5007  │                       │
│                           │(Broadcast/  │                       │
│                           │ Multicast)  │                       │
│                           └─────────────┘                       │
│                                                                 │
│   ════════════════════════════════════════════════════════════  │
│   Broadcast: 255.255.255.255:5007  │  Multicast: 239.0.0.1:5008 │
│                                                                 │
│   ┌─────────────────────────────────────────────────────────┐   │
│   │              Portainer (global)                          │   │
│   │              http://localhost:9000                       │   │
│   └─────────────────────────────────────────────────────────┘   │
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

**Problemă:** Nu văd traficul broadcast/multicast
- Selectează interfața `vEthernet (WSL)`, nu `Ethernet` sau `Wi-Fi`
- Pentru multicast, verifică că ești înscris în grup înainte de a trimite

**Problemă:** Filtrul devine roșu (sintaxă invalidă)
- Verifică ghilimelele și parantezele
- `==` pentru egalitate, nu `=`
- Exemple corecte: `eth.dst == ff:ff:ff:ff:ff:ff`, `ip.dst == 239.0.0.1`

### Probleme Broadcast/Multicast

**Problemă:** Mesajele broadcast nu ajung
```bash
# Verifică că receiver-ul ascultă pe 0.0.0.0, nu pe IP specific
docker exec week3_client ss -lnup | grep 5007

# Verifică conectivitatea în rețea
docker exec week3_server ping -c 1 172.20.0.100
```

**Problemă:** IGMP Join nu funcționează
```bash
# Verifică grupurile multicast active
docker exec week3_client cat /proc/net/igmp

# Verifică routing multicast
docker exec week3_client ip maddr
```

### Probleme Tunel TCP

**Problemă:** Conexiunea prin tunel eșuează
```bash
# Verifică că serverul echo funcționează
docker exec week3_client nc -zv 172.20.0.10 8080

# Verifică că tunelul rulează
docker exec week3_router ss -tlnp | grep 9090

# Verifică log-urile tunelului
docker logs week3_router
```

### Probleme de Rețea

**Problemă:** Containerul nu poate accesa internetul
```bash
# Verifică rețeaua Docker
docker network ls
docker network inspect week3_network

# Verifică DNS în container
docker exec week3_client cat /etc/resolv.conf
```

**Problemă:** Portul este deja utilizat
```bash
# Găsește ce folosește portul (în WSL)
sudo ss -tlnp | grep 8080

# Oprește procesul sau folosește alt port în docker-compose.yml
```

---

## 🧹 Procedura Completă de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT3/03roWSL

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
docker ps -q | xargs -I {} sh -c 'docker inspect --format="{{.Name}}" {} | grep -v portainer && docker stop {}' 2>/dev/null

# Metodă alternativă mai sigură:
docker stop $(docker ps -q --filter "name=week")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite  
docker network prune -f

# Elimină volumele nefolosite (ATENȚIE: nu portainer_data!)
docker volume ls | grep -v portainer | awk 'NR>1 {print $2}' | xargs -r docker volume rm

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

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
