# Săptămâna 4: Nivelul Fizic, Nivelul Legătură de Date și Protocoale Personalizate

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | Laborator
>
> realizat de Revolvix

---

## Notificare Mediu

Acest kit de laborator funcționează în mediul **WSL2 + Ubuntu 22.04 + Docker + Portainer**.

Repository: https://github.com/antonioclim/netROwsl
Folder curent: `04roWSL`

Arhitectura mediului:
```
Windows 11 → WSL2 → Ubuntu 22.04 (implicit) → Docker Engine → Portainer CE
```

Credențiale standard:

| Serviciu | Utilizator | Parolă |
|----------|------------|--------|
| Ubuntu WSL | `stud` | `stud` |
| Portainer | `stud` | `studstudstud` |

---

## Cuprins

1. [Clonare](#clonare)
2. [Configurare Inițială](#configurare-inițială)
3. [Portainer](#portainer)
4. [Wireshark](#wireshark)
5. [Exerciții de Laborator](#exerciții-de-laborator)
6. [Protocoale](#protocoale)
7. [Depanare](#depanare)
8. [Curățare](#curățare)

Pentru detalii teoretice, vezi [Rezumat Teoretic](docs/theory_summary.md).
Pentru depanare detaliată, consultă [Ghid Troubleshooting](docs/troubleshooting.md).
Pentru debugging pas-cu-pas, vezi [Ghid Debugging](docs/debugging_guide.md).

---

## Clonare

### Pasul 1: Deschide PowerShell (Windows)

Apasă `Win + X` → Selectează "Windows Terminal" sau "PowerShell"

### Pasul 2: Navighează și Clonează

```powershell
# Creează folderul de rețele dacă nu există
mkdir D:\RETELE -ErrorAction SilentlyContinue
cd D:\RETELE

# Clonează Săptămâna 4
git clone https://github.com/antonioclim/netROwsl.git SAPT4
cd SAPT4
```

### Pasul 3: Verifică Clonarea

```powershell
dir
# Ar trebui să vezi: 04roWSL/
cd 04roWSL
dir
# Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
```

### Structura Directoarelor

După clonare:
```
D:\RETELE\
└── SAPT4\
    └── 04roWSL\
        ├── artifacts/       # Rezultate generate
        ├── docker/          # Configurație Docker
        ├── docs/            # Documentație suplimentară
        ├── homework/        # Teme pentru acasă
        ├── pcap/            # Fișiere de captură
        ├── scripts/         # Scripturi de automatizare
        ├── setup/           # Configurare mediu
        ├── src/             # Cod sursă exerciții
        │   ├── apps/        # Servere și clienți protocol
        │   ├── exercises/   # Exerciții de laborator
        │   └── utils/       # Utilitare protocol
        ├── tests/           # Teste automatizate
        └── README.md        # Acest fișier
```

---

## Configurare Inițială

### Pasul 1: Deschide Terminalul Ubuntu

Din Windows poți accesa Ubuntu în mai multe moduri: direct din meniul Start (caută "Ubuntu"), din PowerShell cu comanda `wsl`, din Windows Terminal selectând tab-ul Ubuntu, sau din VS Code prin Terminal → New Terminal → Ubuntu.

Vei vedea promptul:
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

---
**Predicție:** Înainte de a rula `docker ps`, răspunde:
1. Câte containere ar trebui să vezi dacă mediul e configurat corect?
2. Ce status vor avea? (Up/Exited)
3. Ce se întâmplă dacă vezi 0 containere?
---

Output așteptat:
```
CONTAINER ID   IMAGE                    STATUS          NAMES
abc123...      portainer/portainer-ce   Up 2 hours      portainer
```

Dacă vezi containerul `portainer` în listă, mediul este pregătit.

### Pasul 3: Verifică Accesul la Portainer

1. Deschide browser-ul web (Chrome, Firefox, Edge)
2. Navighează la: http://localhost:9000

Credențiale:
- Utilizator: `stud`
- Parolă: `studstudstud`

Ce să faci dacă Portainer nu răspunde:
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
cd /mnt/d/RETELE/SAPT4/04roWSL

# Verifică conținutul
ls -la
```

---

## Portainer

### Prezentare Dashboard

După autentificare la http://localhost:9000, vei vedea:
1. **Home** - Lista mediilor Docker disponibile
2. **local** - Click pentru a gestiona Docker-ul local

### Vizualizarea Containerelor

Navighează: Home → local → Containers

Vei vedea un tabel cu toate containerele care include numele containerului (saptamana4-text, saptamana4-binar, saptamana4-senzor), starea (Running/Stopped/Paused), imaginea Docker folosită și mapările de porturi.

### Operații de Bază

| Acțiune | Cum |
|---------|-----|
| Start/Stop/Restart | Butoanele ▶ ■ ↻ din toolbar |
| Logs | Click pe container → tab "Logs" |
| Console | Click pe container → "Console" → "Connect" |

### Inspecție Avansată

| Acțiune | Descriere |
|---------|-----------|
| Inspect | Configurație JSON completă |
| Stats | CPU/Memorie/Rețea în timp real |

### Vizualizarea Rețelei

1. Navighează: Networks → retea_saptamana4
2. Observă containerele conectate și configurația rețelei
3. Vezi adresele IP ale containerelor serviciilor protocol

### Modificarea Porturilor Containerului

1. În Portainer: selectează containerul → "Inspect" → derulează la "HostConfig.PortBindings"
2. Pentru a modifica permanent, editează `docker/docker-compose.yml`:
   ```yaml
   ports:
     - "5400:5400"   # Protocol TEXT
     - "5401:5401"   # Protocol BINAR
     - "5402:5402/udp"   # Senzor UDP
   ```
3. Recreează containerul:
   ```bash
   docker compose -f docker/docker-compose.yml down
   docker compose -f docker/docker-compose.yml up -d
   ```

⚠️ **NU folosi NICIODATĂ portul 9000** - acesta este rezervat exclusiv pentru Portainer!

---

## Wireshark

### Când să Deschizi Wireshark

Deschide Wireshark în următoarele situații:
- ÎNAINTE de a genera traficul de rețea pe care vrei să-l capturezi
- Când exercițiile menționează "captură", "analizează pachete", sau "observă trafic"
- Pentru a examina structura mesajelor protocoalelor TEXT, BINAR și UDP
- Pentru a verifica validarea CRC32

### Pasul 1: Lansează Wireshark

Din Meniul Start Windows: Caută "Wireshark" → Click pentru a deschide

Alternativ, din PowerShell:
```powershell
& "C:\Program Files\Wireshark\Wireshark.exe"
```

### Pasul 2: Selectează Interfața de Captură

Selectează interfața corectă pentru traficul WSL:

| Interfață | Când folosești |
|-----------|----------------|
| vEthernet (WSL) | Cel mai frecvent - capturează traficul Docker WSL |
| vEthernet (WSL) (Hyper-V firewall) | Alternativă dacă prima nu funcționează |
| Loopback Adapter | Doar pentru trafic localhost (127.0.0.1) |

Dublu-click pe numele interfeței SAU selecteaz-o și click pe icoana aripioarei albastre de rechin.

### Pasul 3: Generează Trafic

Cu Wireshark capturând (vei vedea pachete apărând în timp real), rulează exercițiile:

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT4/04roWSL

# Testează protocolul TEXT
python3 src/apps/text_proto_client.py

# Testează protocolul BINAR
python3 src/apps/binary_proto_client.py

# Trimite date UDP de senzor
python3 src/apps/udp_sensor_client.py --sensor-id 1 --temp 23.5 --location "Lab"
```

### Pasul 4: Oprește Captura

Click pe butonul pătrat roșu (Stop) când ai terminat de generat trafic.

### Filtre Wireshark pentru Săptămâna 4

Filtre port:

| Filtru | Scop |
|--------|------|
| `tcp.port == 5400` | Protocol TEXT |
| `tcp.port == 5401` | Protocol BINAR |
| `udp.port == 5402` | Senzor UDP |
| `tcp.port == 5400 or tcp.port == 5401` | Ambele TCP |

Filtre conținut:

| Filtru | Scop |
|--------|------|
| `tcp contains "PING"` | Mesaje PING |
| `tcp.len > 14` | Pachete cu payload |

Pentru filtrare complexă, combinați cu `and`/`or`: `tcp.port == 5401 and tcp.flags.syn == 1` arată doar handshake-urile pentru protocolul BINAR.

### Salvarea Capturilor

```
File → Save As → pcap/captura_mea.pcapng
```

Pentru mai multe filtre și comenzi, vezi [Fișa de Comenzi](docs/commands_cheatsheet.md).

---

## Exerciții de Laborator

### Pornirea Mediului

```bash
cd /mnt/d/RETELE/SAPT4/04roWSL
python3 scripts/start_lab.py
```

---
**Predicție:** Înainte de `docker compose up -d`:
1. Câte containere vor porni? (Hint: verifică docker-compose.yml)
2. Ce porturi vor fi expuse?
3. Cât durează pornirea completă?
---

Output așteptat:
```
============================================================
Pornire Mediu Laborator Săptămâna 4
Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică
============================================================
Se încearcă pornirea serviciului Docker...
✓ Docker a fost pornit cu succes!
Pornire containere...
Așteptare inițializare servicii...
  Progres: 5/5 secunde...
Verificare Server Protocol TEXT...
  ✓ Server Protocol TEXT activ pe port 5400
Verificare Server Protocol BINAR...
  ✓ Server Protocol BINAR activ pe port 5401
Verificare Server Senzor UDP...
  ✓ Server Senzor UDP activ pe port 5402

============================================================
✓ Mediul de laborator este pregătit!

Puncte de acces:
  • Portainer:       http://localhost:9000
  • Protocol TEXT:   localhost:5400
  • Protocol BINAR:  localhost:5401
  • Senzor UDP:      localhost:5402

Pentru a opri laboratorul:
  python3 scripts/stop_lab.py
============================================================
```

### Lista Exercițiilor

| Nr | Fișier | Descriere | Tip |
|----|--------|-----------|-----|
| 1 | `src/exercises/ex1_text_client.py` | Client protocol TEXT | Cod |
| 2 | `src/exercises/ex2_binary_client.py` | Client protocol BINAR | Cod |
| 3 | `src/exercises/ex3_udp_sensor.py` | Client senzor UDP | Cod |
| 4 | `src/exercises/ex4_crc_detection.py` | Detectare erori CRC32 | Cod |
| 5 | `src/exercises/ex5_pair_debugging.py` | Debugging în perechi | Pair Programming |
| 6 | `src/exercises/ex6_wireshark_trace.md` | Analiză Wireshark | Non-cod |

### Rularea unui Exercițiu

```bash
# Exemplu: Exercițiul 1
python3 src/exercises/ex1_text_client.py
```

### Oprirea Mediului

```bash
python3 scripts/stop_lab.py
```

---

## Protocoale

### Protocol TEXT (TCP:5400)

Protocol simplu, lizibil de către om, bazat pe prefix de lungime.

Format mesaj:
```
<LUNGIME> <COMANDĂ> [<ARGUMENTE>]
```

---
**Predicție:** Dacă trimiți `PING` la serverul TEXT:
1. Ce răspuns aștepți? (format: `<lungime> <conținut>`)
2. Câți bytes are răspunsul complet?
---

Comenzi disponibile:

| Comandă | Format | Descriere |
|---------|--------|-----------|
| PING | `4 PING` | Test conectivitate |
| SET | `<L> SET <cheie> <valoare>` | Setare valoare |
| GET | `<L> GET <cheie>` | Citire valoare |
| DEL | `<L> DEL <cheie>` | Ștergere cheie |
| COUNT | `5 COUNT` | Numărare chei |
| KEYS | `4 KEYS` | Listare chei |
| QUIT | `4 QUIT` | Închidere conexiune |

Exemplu conversație:
```
Client: 4 PING
Server: 4 PONG

Client: 13 SET cheie valoare
Server: 2 OK

Client: 9 GET cheie
Server: 7 valoare
```

### Protocol BINAR (TCP:5401)

Protocol eficient cu antet fix de 14 octeți și verificare CRC32.

Structura antetului:
```
┌─────────┬──────────┬─────┬────────┬──────────┬───────┐
│ Magic   │ Versiune │ Tip │ Lungime│ Secvență │ CRC32 │
│ 2 octeți│ 1 octet  │1 oct│ 2 oct  │ 4 octeți │ 4 oct │
│  "NP"   │    1     │     │        │          │       │
└─────────┴──────────┴─────┴────────┴──────────┴───────┘
```

Tipuri de mesaje:

| Cod | Nume | Descriere |
|-----|------|-----------|
| 0x01 | PING | Verificare conexiune |
| 0x02 | PONG | Răspuns PING |
| 0x03 | SET | Setare valoare |
| 0x04 | GET | Citire valoare |
| 0x05 | DELETE | Ștergere cheie |
| 0x06 | RESPONSE | Răspuns generic |
| 0xFF | ERROR | Eroare |

Pentru detalii despre CRC32 și diagrame, vezi [Rezumat Teoretic](docs/theory_summary.md) și [Arhitectură](docs/architecture.md).

### Protocol Senzor UDP (UDP:5402)

Protocol pentru dispozitive IoT cu datagrame de dimensiune fixă (23 octeți).

Structura datagramei:
```
┌──────────┬─────────┬─────────────┬─────────┬───────┬──────────┐
│ Versiune │ ID Senz │ Temperatură │ Locație │ CRC32 │ Rezervat │
│ 1 octet  │ 2 oct   │ 4 oct (flt) │ 10 oct  │ 4 oct │ 2 oct    │
└──────────┴─────────┴─────────────┴─────────┴───────┴──────────┘
```

### Comparație TCP vs UDP

| Caracteristică | TCP | UDP |
|----------------|-----|-----|
| Orientat conexiune | Da | Nu |
| Fiabilitate | Garantată | Negarantată |
| Ordonare | Garantată | Negarantată |
| Control flux | Da | Nu |
| Overhead | Mai mare (~40B) | Mai mic (~8B) |
| Utilizare | Web, email, fișiere | Streaming, jocuri, DNS, IoT |

### De ce Alegem UDP pentru Senzori?

Pentru senzori IoT pe baterie care trimit date la fiecare câteva secunde:
- O citire pierdută nu e critică (vine alta imediat)
- Overhead-ul mic economisește energie
- Implementarea e mai simplă (fără handshake, fără stare)

---

## Depanare

### Probleme Docker

**"Cannot connect to Docker daemon"**
```bash
# Pornește serviciul Docker în WSL
sudo service docker start
# Parolă: stud

# Verifică statusul
sudo service docker status

# Verifică că funcționează
docker ps
```

**Permisiune refuzată la rularea docker**
```bash
# Adaugă utilizatorul la grupul docker
sudo usermod -aG docker $USER

# Aplică modificările
newgrp docker

# Sau deconectează-te și reconectează-te din WSL
exit
wsl
```

### Probleme Portainer

**Nu pot accesa http://localhost:9000**
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

### Probleme Wireshark

**Nu se capturează pachete**
- Verifică interfața corectă selectată (vEthernet WSL)
- Asigură-te că traficul este generat ÎN TIMPUL capturii
- Verifică că filtrul de afișare nu ascunde pachetele (șterge filtrul)
- Încearcă "Capture → Options" și activează modul promiscuous

**Filtrul devine roșu (sintaxă invalidă)**
- Verifică ghilimelele și parantezele
- Folosește `==` pentru egalitate, nu `=`
- Exemple corecte: `tcp.port == 5400`, `udp.port == 5402`

### Probleme Protocoale

**CRC32 nu se validează corect**
```python
# Verificare ordine bytes
# Folosește network byte order (big-endian)
import struct
struct.pack('!I', crc_value)  # '!' = network order, NU fără '!'
```

Pentru depanare detaliată, consultă [Troubleshooting](docs/troubleshooting.md) și [Ghid Debugging](docs/debugging_guide.md).

---

## Curățare

### Sfârșit de Sesiune (Rapidă)

```bash
# În terminalul Ubuntu
cd /mnt/d/RETELE/SAPT4/04roWSL

# Oprește containerele de laborator (Portainer rămâne activ!)
docker compose -f docker/docker-compose.yml down

# Verifică - ar trebui să arate încă portainer
docker ps
```

### Sfârșit de Săptămână (Completă)

```bash
# Elimină containerele și rețelele acestei săptămâni
docker compose -f docker/docker-compose.yml down --volumes

# Elimină imaginile nefolosite
docker image prune -f

# Elimină rețelele nefolosite
docker network prune -f

# Verifică utilizarea discului
docker system df
```

### Resetare Totală (Înainte de Semestru Nou)

```bash
# Oprește toate containerele EXCEPTÂND Portainer
docker stop $(docker ps -q --filter "name=saptamana")

# Elimină containerele oprite (nu Portainer)
docker container prune -f

# Elimină imaginile nefolosite
docker image prune -a -f

# Elimină rețelele nefolosite  
docker network prune -f

# Verifică că Portainer încă rulează
docker ps
```

⚠️ **NU rula NICIODATĂ `docker system prune -a` fără să excluzi Portainer!**

---

## Diagramă Arhitectură

```
┌─────────────────────────────────────────────────────────────────────┐
│                      GAZDĂ WINDOWS (WSL2)                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐    ┌─────────────┐    ┌─────────────┐           │
│   │  Wireshark  │    │  PowerShell │    │   VS Code   │           │
│   │  (Analiză)  │    │  (Comenzi)  │    │  (Editor)   │           │
│   └──────┬──────┘    └──────┬──────┘    └─────────────┘           │
│          │                  │                                      │
│          │    localhost:5400/5401/5402                            │
│          │                  │                                      │
├──────────┼──────────────────┼──────────────────────────────────────┤
│          │     DOCKER ENGINE (WSL2)                                │
│          │                  │                                      │
│   ┌──────┴──────────────────┴───────────────────────────────┐     │
│   │              Containere Laborator                        │     │
│   │                                                          │     │
│   │   ┌───────────┐ ┌───────────┐ ┌───────────────┐        │     │
│   │   │  Server   │ │  Server   │ │    Server     │        │     │
│   │   │   TEXT    │ │   BINAR   │ │  Senzor UDP   │        │     │
│   │   │ TCP:5400  │ │ TCP:5401  │ │   UDP:5402    │        │     │
│   │   └───────────┘ └───────────┘ └───────────────┘        │     │
│   │                                                          │     │
│   │   Rețea: retea_saptamana4                               │     │
│   └──────────────────────────────────────────────────────────┘     │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────┐     │
│   │              Portainer (global)                          │     │
│   │              http://localhost:9000                       │     │
│   └─────────────────────────────────────────────────────────┘     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

Pentru diagrame detaliate ale protocoalelor, vezi [Arhitectură](docs/architecture.md).

---

## Referințe

- Kurose, J. & Ross, K. (2016). *Computer Networking: A Top-Down Approach* (7th ed.). Pearson.
- Rhodes, B. & Goetzen, J. (2014). *Foundations of Python Network Programming*. Apress.
- RFC 768 - User Datagram Protocol
- RFC 793 - Transmission Control Protocol
- Documentația Python: modulele `socket` și `struct`

Pentru mai multe resurse, vezi [Lectură Suplimentară](docs/further_reading.md).

---

## Întrebări Frecvente

Consultă [FAQ](docs/faq.md) pentru răspunsuri la întrebările comune.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
*Adaptat pentru mediul WSL2 + Ubuntu 22.04 + Docker + Portainer*
