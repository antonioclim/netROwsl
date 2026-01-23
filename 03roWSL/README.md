# Săptămâna 3: Programare în Rețea - Broadcast, Multicast și Tunel TCP

> Laborator Rețele de Calculatoare - ASE, Informatică Economică
>
> by Revolvix

---

## Notificare Mediu

⚠️ Acest kit de laborator este proiectat pentru mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

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

## Ce ar trebui să știi deja

Înainte de a începe laboratorul Săptămânii 3, verifică dacă poți răspunde la următoarele întrebări:

**Din Săptămânile anterioare:**
- Ce este un socket și care sunt tipurile principale (TCP vs UDP)?
- Cum funcționează modelul client-server?
- Ce este un port și de ce avem nevoie de el?
- Care este diferența dintre conexiuni orientate pe flux (TCP) și datagrame (UDP)?

**Cunoștințe generale de rețelistică:**
- Diferența dintre adrese IP și adrese MAC
- Ce înseamnă Layer 2 (Data Link) vs Layer 3 (Network) în modelul OSI
- Cum să navighezi în terminal (cd, ls, pwd în Linux; cd, dir în PowerShell)

**Dacă nu ești sigur pe răspunsuri**, recitește [Rezumatul Teoretic](docs/rezumat_teoretic.md) și parcurge [Întrebările de Recapitulare](docs/intrebari_recapitulare.md) înainte de a continua.

---

## Clonarea Laboratorului

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` și selectează "Windows Terminal" sau "PowerShell".

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

### Structura Directoarelor

După clonare, vei avea următoarea structură:

```
D:\RETELE\
└── SAPT3\
    └── 03roWSL\
        ├── artifacts/       # Rezultate generate (capturi, loguri)
        ├── docker/          # Configurație Docker și Compose
        ├── docs/            # Documentație suplimentară
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură Wireshark
        ├── scripts/         # Scripturi de automatizare Python
        ├── setup/           # Configurare și verificare mediu
        ├── src/             # Cod sursă exerciții și aplicații
        ├── tests/           # Teste automatizate
        └── README.md        # Acest fișier
```

---

## Configurarea Inițială a Mediului

⚠️ Această secțiune se execută doar prima dată când configurezi mediul.

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows poți deschide Ubuntu în mai multe moduri: click pe "Ubuntu" în Start, tastează `wsl` în PowerShell, sau selectează tab-ul Ubuntu din Windows Terminal.

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

Deschide browser-ul web (Chrome, Firefox, Edge) și navighează la **http://localhost:9000**.

Credențiale: utilizator `stud`, parolă `studstudstud`.

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
cd /mnt/d/RETELE/SAPT3/03roWSL
ls -la
```

---

## Quick Wins - Verifică că totul funcționează

Înainte de a continua cu exercițiile, verifică rapid că mediul funcționează corect.

**Test 30 secunde - Echo Server:**
```bash
# Pornește laboratorul
cd /mnt/d/RETELE/SAPT3/03roWSL
python3 scripts/porneste_lab.py

# Testează conexiunea
echo "test" | docker exec -i week3_client nc 172.20.0.10 8080
# Ar trebui să vezi: ECHO: test
```

**Test 60 secunde - Broadcast:**
```bash
# Terminal 1: Pornește receptorul
docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod receiver &

# Terminal 2: Trimite mesaj
docker exec week3_server python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 1
# Ar trebui să vezi mesajul primit în output
```

Dacă ambele teste funcționează, mediul este configurat corect și poți continua.

---

## Înțelegerea Interfeței Portainer

### Prezentare Generală Dashboard

După autentificare la http://localhost:9000, vei vedea pagina Home cu lista mediilor Docker disponibile. Click pe **local** pentru a gestiona Docker-ul local.

### Vizualizarea Containerelor

Navighează: **Home → local → Containers**

Vei vedea un tabel cu toate containerele care include: numele containerului, starea (Running/Stopped/Paused/Exited), imaginea Docker de bază, timestamp-ul creării, adresa IP în rețeaua Docker, și mapările de porturi host:container.

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

### Vizualizarea Rețelei week3_network

Navighează la **Networks → week3_network** pentru a vedea configurația IPAM curentă (172.20.0.0/24) și containerele conectate cu adresele lor IP: server (172.20.0.10), router (172.20.0.254), client (172.20.0.100), receiver (172.20.0.101).

### Modificarea Configurației de Rețea

Pentru a modifica subrețeaua sau adresele IP, oprește containerele care folosesc rețeaua, editează fișierul `docker/docker-compose.yml`, apoi recreează mediul:

```bash
cd /mnt/d/RETELE/SAPT3/03roWSL
docker compose -f docker/docker-compose.yml down
docker compose -f docker/docker-compose.yml up -d
```

⚠️ **NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## Configurarea și Folosirea Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark **ÎNAINTE** de a genera traficul pe care vrei să-l capturezi. Situații tipice: când exercițiile menționează "captură", "analizează pachete" sau "observă trafic"; pentru demonstrații care necesită vizualizarea traficului în timp real; pentru a observa diferențele dintre broadcast, multicast și unicast.

### Pasul 1: Lansează Wireshark

Din Meniul Start Windows caută "Wireshark" și click pentru a deschide.

Alternativ, din PowerShell:
```powershell
& "C:\Program Files\Wireshark\Wireshark.exe"
```

### Pasul 2: Selectează Interfața de Captură

⚠️ **CRITIC:** Selectează interfața corectă pentru traficul WSL:

| Interfață | Când să folosești |
|-----------|-------------------|
| **vEthernet (WSL)** | Cel mai frecvent - capturează traficul Docker WSL |
| **vEthernet (WSL) (Hyper-V firewall)** | Alternativă dacă prima nu funcționează |
| **Loopback Adapter** | Doar pentru trafic localhost (127.0.0.1) |
| **Ethernet/Wi-Fi** | Trafic rețea fizică (nu Docker) |

Dublu-click pe numele interfeței sau selecteaz-o și click pe icoana aripioarei albastre de rechin.

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

### Filtre Wireshark pentru Săptămâna 3

Tastează în bara de filtrare (devine verde când filtrul este valid) și apasă Enter:

| Filtru | Scop |
|--------|------|
| `eth.dst == ff:ff:ff:ff:ff:ff` | Trafic broadcast (Layer 2) |
| `ip.dst == 255.255.255.255` | Broadcast limitat (Layer 3) |
| `ip.dst >= 224.0.0.0 and ip.dst <= 239.255.255.255` | Trafic multicast |
| `ip.dst == 239.0.0.1` | Grup multicast specific laborator |
| `igmp` | Mesaje IGMP (Join/Leave grup) |
| `udp.port == 5007` | Port broadcast laborator |
| `udp.port == 5008` | Port multicast laborator |
| `tcp.port == 8080` | Server Echo TCP |
| `tcp.port == 9090` | Tunel TCP |
| `ip.addr == 172.20.0.0/24` | Tot traficul rețelei laborator |

**Combinarea filtrelor:** folosește `&&` pentru ȘI, `||` pentru SAU, `!` pentru NU.

### Identificarea Tipurilor de Trafic în Wireshark

| Tip Trafic | Adresa MAC Destinație | Adresa IP Destinație | Caracteristici |
|------------|----------------------|---------------------|----------------|
| **Unicast** | Adresă specifică (00:...) | IP specific (172.20.0.10) | Punct-la-punct |
| **Broadcast** | ff:ff:ff:ff:ff:ff | 255.255.255.255 sau .255 | Toate stațiile |
| **Multicast** | 01:00:5e:... | 224.x.x.x - 239.x.x.x | Doar membrii grupului |

### Salvarea Capturilor

**File → Save As** (sau Ctrl+Shift+S), navighează la `D:\RETELE\SAPT3\03roWSL\pcap\`, și salvează cu nume sugestiv (ex: `captura_broadcast.pcap`).

---

## Prezentare Generală

Această sesiune de laborator studiază mecanismele fundamentale de comunicare în rețea prin intermediul programării cu socket-uri: transmisia broadcast, comunicarea multicast și tunelarea TCP.

### Comparație Vizuală: Unicast vs Broadcast vs Multicast

```
UNICAST (1:1)              BROADCAST (1:ALL)          MULTICAST (1:MANY)
┌───┐                      ┌───┐                      ┌───┐
│ S │──────►┌───┐          │ S │──┬──►┌───┐          │ S │──┬──►┌───┐ ✓ membru
└───┘       │ R │          └───┘  │   │R1 │          └───┘  │   │R1 │
            └───┘                 │   └───┘                 │   └───┘
                                  ├──►┌───┐                 └──►┌───┐ ✓ membru
                                  │   │R2 │                     │R2 │
                                  │   └───┘                     └───┘
                                  └──►┌───┐                     ┌───┐ ✗ nu e membru
                                      │R3 │                     │R3 │
                                      └───┘                     └───┘
                            Toți primesc              Doar membrii primesc
```

**Transmisia broadcast** permite unui singur emițător să comunice simultan cu toate dispozitivele dintr-un segment de rețea, eliminând necesitatea cunoașterii prealabile a destinatarilor.

**Multicast** extinde acest concept prin crearea grupurilor de interes, unde doar stațiile membre primesc traficul, optimizând astfel folosirea lățimii de bandă.

**Tunelarea TCP** oferă mecanisme de redirecționare transparentă a conexiunilor, fundamentale pentru proxy-uri, load balancere și rețele virtuale private.

### Gândește Concret Înainte de Abstract

Înainte de a te scufunda în cod, înțelege conceptele prin analogii din viața reală:

| Concept | Analogie | Ce înseamnă tehnic |
|---------|----------|-------------------|
| **Broadcast** | Anunț pe megafon în piață | Toți aud, indiferent dacă vor sau nu |
| **Multicast** | Grup de WhatsApp | Doar membrii grupului primesc mesajele |
| **IGMP Join** | Abonare la newsletter | Te înscrii activ pentru a primi |
| **TTL** | Bilet de metrou valabil N stații | La fiecare router, "o stație" se consumă |
| **Tunel TCP** | Poștaș care redirecționează | Primește scrisori și le trimite mai departe |
| **SO_BROADCAST** | Permis de megafon | Fără el, sistemul refuză să transmită broadcast |

**Revino la aceste analogii** când întâmpini dificultăți cu conceptele tehnice sau cu depanarea.

### Auto-Evaluare

Înainte de a începe exercițiile, verifică-ți cunoștințele: [Întrebări de Recapitulare](docs/intrebari_recapitulare.md)

Dacă nu poți răspunde la întrebările REMEMBER, recitește [Rezumatul Teoretic](docs/rezumat_teoretic.md).

---

## Obiective de Învățare

La finalul acestei sesiuni de laborator, vei fi capabil să:

1. **Identifici** diferențele dintre comunicarea unicast, broadcast și multicast la nivel conceptual și practic
2. **Explici** mecanismul IGMP pentru gestionarea apartenenței la grupuri multicast și rolul TTL în propagarea pachetelor
3. **Implementezi** aplicații client-server folosind socket-uri UDP cu opțiuni SO_BROADCAST și IP_ADD_MEMBERSHIP
4. **Construiești** un tunel TCP bidirecțional pentru redirecționarea transparentă a conexiunilor între endpoint-uri
5. **Analizezi** traficul de rețea capturat, identificând tipare specifice broadcast-ului, multicast-ului și tunelării
6. **Evaluezi** avantajele și dezavantajele fiecărui mod de comunicare în scenarii practice

---

## Cerințe Preliminare

### Cunoștințe Necesare

Pentru a parcurge acest laborator ai nevoie de: fundamentele modelului TCP/IP și adresării IPv4, programare Python de bază (funcții, clase, module), diferențele dintre protocoalele TCP și UDP, și folosirea liniei de comandă (PowerShell și Bash).

### Cerințe Software

- Windows 10/11 cu WSL2 activat
- Docker Engine (în WSL2)
- Portainer CE (rulează global pe portul 9000)
- Wireshark (aplicație Windows nativă)
- Python 3.11 sau versiune ulterioară
- Git (opțional, recomandat)

### Cerințe Hardware

Minimum 8GB RAM (16GB recomandat), 10GB spațiu liber pe disc, conectivitate la rețea.

---

## Pornire Rapidă

### Configurare Inițială (Se Execută O Singură Dată)

```bash
# Deschide terminalul Ubuntu (wsl în PowerShell)
cd /mnt/d/RETELE/SAPT3/03roWSL

# Verifică cerințele preliminare
python3 setup/verifica_mediu.py

# Dacă există probleme, rulează asistentul de instalare
python3 setup/instaleaza_cerinte.py
```

### Pornirea Laboratorului

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT3/03roWSL

# Pornește toate serviciile (fără receiver)
python3 scripts/porneste_lab.py

# Sau cu toate serviciile (inclusiv receiver pentru broadcast/multicast)
python3 scripts/porneste_lab.py --broadcast

# Verifică că totul funcționează
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

---

## Exerciții de Laborator

### Exercițiul 1: Transmisie UDP Broadcast

**Obiectiv:** Implementarea și testarea comunicării broadcast folosind socket-uri UDP cu opțiunea SO_BROADCAST.

**Durată estimată:** 30 minute

**Lectură pregătitoare:** [Rezumat Teoretic - Broadcast](docs/rezumat_teoretic.md#transmisia-broadcast)  
**Troubleshooting:** [Probleme Broadcast](docs/depanare.md#probleme-socket-și-broadcast)

**Pregătire Wireshark:** Deschide Wireshark pe Windows și pornește captura pe interfața `vEthernet (WSL)` cu filtrul `udp.port == 5007 && eth.dst == ff:ff:ff:ff:ff:ff` ÎNAINTE de a începe exercițiul.

**Fundament teoretic:**
Broadcast-ul permite transmiterea unui singur pachet către toate stațiile dintr-un segment de rețea. Adresa de broadcast limitat (255.255.255.255) nu traversează routere, fiind confinată la rețeaua locală. Socket-urile necesită activarea explicită a opțiunii SO_BROADCAST pentru a permite astfel de transmisii.

🔮 **PREDICȚIE:** Înainte de a rula, răspunde mental:
- Ce adresă MAC va avea pachetul broadcast la Layer 2? (Hint: începe cu ff:)
- Dacă sunt 4 containere în rețea, câte vor primi mesajul broadcast?
- Ce se întâmplă dacă receptorul face bind la IP-ul său specific în loc de 0.0.0.0?

**Pași:**

1. Pornește containerul receiver într-un terminal:
   ```bash
   docker exec -it week3_client python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod receiver
   ```

2. Într-un alt terminal, pornește emițătorul:
   ```bash
   docker exec -it week3_server python3 /app/src/exercises/ex_3_01_udp_broadcast.py --mod sender --numar 5
   ```

3. Observă mesajele primite și notează adresa sursă a pachetelor, timpul de propagare, și comportamentul când multiple receivere sunt active.

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

**Lectură pregătitoare:** [Rezumat Teoretic - Multicast](docs/rezumat_teoretic.md#comunicarea-multicast)  
**Troubleshooting:** [Probleme Multicast](docs/depanare.md#probleme-multicast)

**Pregătire Wireshark:** Schimbă filtrul la `igmp || (udp.port == 5008 && ip.dst == 239.0.0.1)` pentru a observa traficul multicast și mesajele IGMP.

**Fundament teoretic:**
Multicast-ul permite comunicarea eficientă unul-la-mulți prin folosirea adreselor din intervalul 224.0.0.0 - 239.255.255.255. Receptorii se înscriu în grupuri folosind protocolul IGMP (Internet Group Management Protocol), iar rețeaua livrează pachetele doar membrilor activi. Spre deosebire de broadcast, multicast-ul poate traversa routere configurate corespunzător.

🔮 **PREDICȚIE:** Înainte de a rula receptorul, răspunde:
- Ce tip de mesaj IGMP va trimite receptorul când pornește? (Join sau Leave?)
- Ce vei vedea în Wireshark dacă filtrezi cu `igmp`?
- De ce multicast-ul este mai eficient decât broadcast-ul pentru 10 receptori din 100 de dispozitive?

**Pași:**

1. Pornește primul receptor:
   ```bash
   docker exec -it week3_client python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver
   ```

2. Pornește al doilea receptor (terminal separat):
   ```bash
   docker exec -it week3_receiver python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod receiver
   ```

3. Transmite mesaje către grup:
   ```bash
   docker exec -it week3_server python3 /app/src/exercises/ex_3_02_udp_multicast.py --mod sender --numar 5
   ```

4. Verifică înscrierea în grup IGMP:
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

**Lectură pregătitoare:** [Rezumat Teoretic - Tunelare](docs/rezumat_teoretic.md#tunelarea-tcp)  
**Troubleshooting:** [Probleme Tunel](docs/depanare.md#probleme-tunel-tcp)

**Pregătire Wireshark:** Aplică filtrul `tcp.port == 9090 || tcp.port == 8080` pentru a observa ambele conexiuni TCP.

**Fundament teoretic:**
Tunelarea TCP implică acceptarea conexiunilor pe un port și redirecționarea traficului către o destinație diferită. Acest pattern este fundamental pentru proxy-uri, load balancere și gateway-uri de securitate. Implementarea corectă necesită gestionarea bidirecțională a datelor și tratarea elegantă a deconectărilor.

🔮 **PREDICȚIE:** Înainte de a testa tunelul, răspunde:
- Câte conexiuni TCP separate vor exista? (1, 2 sau 3?)
- Ce IP sursă va vedea serverul echo - IP-ul clientului sau IP-ul routerului/tunelului?
- Câte segmente TCP SYN vei vedea în Wireshark pentru o singură cerere prin tunel?

**Pași:**

1. Verifică că serverul echo funcționează:
   ```bash
   echo "Test direct" | docker exec -i week3_client nc 172.20.0.10 8080
   ```

2. Testează conexiunea prin tunel:
   ```bash
   echo "Test prin tunel" | docker exec -i week3_client nc 172.20.0.254 9090
   ```

3. Examinează codul tunelului și identifică cum se creează conexiunea către server, cum se gestionează traficul bidirecțional, și cum se tratează deconectările.

4. Monitorizează conexiunile active:
   ```bash
   docker exec week3_router ss -tnp
   ```

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 3
```

**Întrebări de reflecție:**
- De ce este necesară folosirea thread-urilor pentru relay-ul bidirecțional?
- Ce avantaje oferă un tunel TCP față de conexiunea directă?

---

### Exercițiul 4: Analiză cu Wireshark

**Obiectiv:** Capturarea și analiza traficului de rețea pentru identificarea tiparelor specifice fiecărui tip de comunicare.

**Durată estimată:** 25 minute

**Pași:**

1. Pornește captura de trafic:
   ```bash
   python3 scripts/captureaza_trafic.py --container server --durata 60 --output pcap/analiza_week3.pcap
   ```

2. În timpul capturii, execută exercițiile 1-3.

3. Deschide fișierul pcap în Wireshark:
   ```powershell
   # În PowerShell
   & "C:\Program Files\Wireshark\Wireshark.exe" "D:\RETELE\SAPT3\03roWSL\pcap\analiza_week3.pcap"
   ```

4. Aplică filtrele și documentează observațiile:
   - Trafic broadcast: `eth.dst == ff:ff:ff:ff:ff:ff`
   - Trafic multicast: `ip.dst >= 239.0.0.0 and ip.dst <= 239.255.255.255`
   - Mesaje IGMP: `igmp`
   - Trafic tunel: `tcp.port == 9090 or tcp.port == 8080`

**Verificare:**
```bash
python3 tests/test_exercitii.py --exercitiu 4
```

---

## Demonstrații

### Demo 1: Broadcast în Acțiune

Demonstrație automată care ilustrează propagarea mesajelor broadcast către multiple receptoare.

```bash
python3 scripts/ruleaza_demo.py --demo broadcast
```

**Ce trebuie observat:** toate containerele primesc același mesaj simultan, adresa MAC destinație este ff:ff:ff:ff:ff:ff, nu există confirmare de primire (UDP).

### Demo 2: Grupuri Multicast

Demonstrație a înscrierii și comunicării în grupuri multicast.

```bash
python3 scripts/ruleaza_demo.py --demo multicast
```

**Ce trebuie observat:** rapoartele IGMP la înscriere și părăsire, doar membrii grupului primesc mesaje, adresa IP destinație este în intervalul multicast.

### Demo 3: Tunelare TCP

Demonstrație a redirecționării transparente prin tunel.

```bash
python3 scripts/ruleaza_demo.py --demo tunel
```

**Ce trebuie observat:** două conexiuni TCP separate (client-tunel, tunel-server), datele sunt relayate transparent, conexiunile se închid sincronizat.

---

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

## Flux TTL la Traversarea Routerelor

```
┌─────────┐    TTL=3    ┌─────────┐    TTL=2    ┌─────────┐    TTL=1    ┌─────────┐
│ Sender  │ ──────────► │Router 1 │ ──────────► │Router 2 │ ──────────► │Receiver │
│         │             │  -1     │             │  -1     │             │ PRIMIT! │
└─────────┘             └─────────┘             └─────────┘             └─────────┘

                        Dacă TTL=0 înainte de a ajunge:
┌─────────┐    TTL=1    ┌─────────┐    TTL=0    
│ Sender  │ ──────────► │Router 1 │ ──────────► ❌ DROPPED (Time Exceeded)
│         │             │  -1     │             
└─────────┘             └─────────┘             

ANALOGIE: TTL este ca un bilet de metrou valabil pentru N stații.
          La fiecare router traversat, se "perforează" o stație.
          Când nu mai ai stații, ești dat jos din tren.
```

---

## Structura IGMP

Internet Group Management Protocol gestionează apartenența la grupuri multicast:

```
┌─────────┐                    ┌─────────┐
│  Host   │  IGMP Join (0x16)  │ Router  │
│         │ ─────────────────► │         │
│         │                    │         │
│         │  IGMP Query (0x11) │         │
│         │ ◄───────────────── │ (60s)   │
│         │                    │         │
│         │  IGMP Report       │         │
│         │ ─────────────────► │         │
│         │                    │         │
│         │  IGMP Leave (0x17) │         │
│         │ ─────────────────► │         │
└─────────┘                    └─────────┘
```

- **Membership Query**: Router-ul întreabă ce grupuri sunt active
- **Membership Report**: Stația raportează apartenența la grup
- **Leave Group**: Stația notifică părăsirea grupului

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (ed. 7). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 919 - Broadcasting Internet Datagrams
- RFC 1112 - Host Extensions for IP Multicasting
- RFC 2236 - Internet Group Management Protocol, Version 2

---

## Depanare Extinsă

Pentru probleme comune, consultă ghidul detaliat: [Depanare](docs/depanare.md)

### Probleme Docker

**Problemă:** "Cannot connect to Docker daemon"
```bash
sudo service docker start
sudo service docker status
docker ps
```

**Problemă:** Permisiune refuzată la rularea docker
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Probleme Portainer

**Problemă:** Nu pot accesa http://localhost:9000
```bash
docker ps -a | grep portainer
docker start portainer
docker logs portainer
```

### Probleme Wireshark

**Problemă:** Nu se capturează pachete
- Verifică interfața corectă selectată (vEthernet WSL)
- Asigură-te că traficul este generat ÎN TIMPUL capturii
- Verifică că filtrul de afișare nu ascunde pachetele

### Probleme Broadcast/Multicast

**Problemă:** Mesajele broadcast nu ajung
```bash
docker exec week3_client ss -ulnp | grep 5007
docker exec week3_server ping -c 1 172.20.0.100
```

**Problemă:** IGMP Join nu funcționează
```bash
docker exec week3_client cat /proc/net/igmp
docker exec week3_client ip maddr
```

---

## Procedura de Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
cd /mnt/d/RETELE/SAPT3/03roWSL
docker compose -f docker/docker-compose.yml down
docker ps
# Ar trebui să arate încă portainer
```

### Sfârșit de Săptămână (Completă)

```bash
docker compose -f docker/docker-compose.yml down --volumes
docker image prune -f
docker network prune -f
docker system df
```

### Resetare Totală

⚠️ **ATENȚIE:** Aceasta elimină TOTUL în afară de Portainer

```bash
docker stop $(docker ps -q --filter "name=week")
docker container prune -f
docker image prune -a -f
docker network prune -f
```

**NU rula NICIODATĂ `docker system prune -a` fără să excluzi Portainer!**

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*  
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
