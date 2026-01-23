# Proiectul 02: Rețea hibridă cu Mininet și containere Docker

> **Disciplina:** Rețele de Calculatoare  
> **Program:** Informatică Economică, Anul 3, Semestrul 2  
> **Instituție:** ASE București - CSIE  
> **Tip proiect:** Principal

---

## 📋 GHID DE EVALUARE ȘI LIVRARE

### ⚠️ IMPORTANT: Evaluarea cu prezență fizică

**Evaluarea proiectului se face EXCLUSIV la facultate, cu prezență fizică obligatorie.**

- Prezentarea finală (Etapa 4) se susține în fața profesorului/comisiei
- Trebuie să demonstrezi că înțelegi codul și arhitectura proiectului
- Întrebări din implementare și concepte teoretice sunt posibile
- Lipsa de la prezentare = nepromovare proiect

---

### 📅 Calendarul etapelor

| Etapa | Săptămâna | Deadline | Ce livrezi | Punctaj |
|-------|-----------|----------|------------|---------|
| **E1** - Design | Săpt. 5 | Săpt. 5 (2026) | Specificații + Diagrame + Plan | 20% |
| **E2** - Prototip | Săpt. 9 | Săpt. 9 (2026) | Implementare parțială funcțională | 25% |
| **E3** - Final | Săpt. 13 | Săpt. 13 (2026) | Versiune completă + Documentație | 35% |
| **E4** - Prezentare | Săpt. 14 | Săpt. 14 (2026) | Demo live + Susținere orală | 20% |

**Verificări intermediare (opțional, pentru feedback):** Săptămânile 3, 6, 8, 11

---

### 🐙 Publicare pe GitHub

**OBLIGATORIU:** Proiectul trebuie publicat pe GitHub înainte de fiecare etapă.

#### Repository-ul tău

```
https://github.com/[username]/retele-proiect-02
```

#### Structura obligatorie a repository-ului

```
retele-proiect-02/
├── README.md                 # Descriere proiect, instrucțiuni rulare
├── docs/                     # Documentație
│   ├── specificatii.md       # [E1] Specificații tehnice
│   ├── diagrame/             # [E1] Diagrame arhitectură
│   ├── raport_progres.md     # [E2] Raport etapa 2
│   └── documentatie_finala.md # [E3] Documentație completă
├── src/                      # Cod sursă
│   ├── main.py               # Punct de intrare
│   ├── modules/              # Module aplicație
│   └── utils/                # Utilitare
├── docker/                   # Configurații Docker
│   ├── docker-compose.yml
│   ├── Dockerfile
│   └── configs/              # Fișiere configurare servicii
├── tests/                    # Teste
│   ├── test_basic.py
│   └── expected_outputs/
├── artifacts/                # Output-uri (capturi, loguri)
│   └── screenshots/
├── MANIFEST.txt              # Fișier semnătură (generat automat)
├── CHANGELOG.md              # Istoric modificări
└── .gitignore
```

#### Ce publici la fiecare etapă

| Etapa | Fișiere/Foldere obligatorii pe GitHub |
|-------|---------------------------------------|
| **E1** | `README.md`, `docs/specificatii.md`, `docs/diagrame/`, `.gitignore` |
| **E2** | + `src/` (cod funcțional parțial), `docker/`, `docs/raport_progres.md` |
| **E3** | + `tests/`, `artifacts/`, `docs/documentatie_finala.md`, `CHANGELOG.md` |
| **E4** | Repository complet + tag `v1.0-final` |

#### Comenzi Git pentru fiecare etapă

```bash
# Etapa 1 - După ce ai pregătit specificațiile
git add docs/ README.md .gitignore
git commit -m "E1: Specificații și design inițial"
git push origin main

# Etapa 2 - După implementarea prototipului
git add src/ docker/ docs/raport_progres.md
git commit -m "E2: Prototip funcțional"
git push origin main

# Etapa 3 - Versiunea finală
git add tests/ artifacts/ docs/documentatie_finala.md CHANGELOG.md
git commit -m "E3: Versiune finală completă"
git tag -a v1.0-final -m "Versiune finală proiect"
git push origin main --tags

# Etapa 4 - Ultimele ajustări înainte de prezentare
git add .
git commit -m "E4: Pregătire prezentare"
git push origin main
```

---

### 📦 Convenția de denumire arhive

**Format:** `NUME_Prenume_GGGG_P02_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P02 | Numărul proiectului | P02 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P02_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P02_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P02_S07.zip` — Verificare săptămâna 7

---

### 📊 Rubrică de evaluare

#### Etapa 1 — Design (100 puncte)

| Criteriu | Puncte | Descriere |
|----------|--------|-----------|
| Specificații complete | 30 | Toate cerințele identificate și documentate |
| Diagrame arhitectură | 20 | Topologie rețea, flux date, componente |
| Plan implementare | 15 | Timeline realist cu milestones |
| Repository inițializat | 15 | GitHub configurat corect cu structura de bază |
| MANIFEST.txt corect | 10 | Semnătură validă |
| Denumire arhivă | 10 | Respectă convenția |

#### Etapa 2 — Prototip (100 puncte)

| Criteriu | Puncte | Descriere |
|----------|--------|-----------|
| Funcționalitate parțială | 35 | Minim 50% din cerințe funcționale |
| Calitate cod | 25 | Curat, comentat, structurat |
| Docker configurat | 15 | Compose funcțional, containere pornesc |
| Raport progres | 10 | Documentează ce e gata și ce mai rămâne |
| MANIFEST.txt | 10 | Semnătură validă |
| Livrare la timp | 5 | Respectă deadline |

#### Etapa 3 — Versiune Finală (100 puncte + 10 bonus)

| Criteriu | Puncte | Descriere |
|----------|--------|-----------|
| Funcționalitate completă | 40 | Toate cerințele implementate |
| Calitate cod finală | 20 | Cod production-ready |
| Teste | 15 | Teste unitare și integrare |
| Documentație | 10 | README complet, comentarii cod |
| Analiză comparativă | 5 | Comparație cu alternative |
| MANIFEST.txt | 10 | Semnătură validă |
| **Bonus extensii** | +10 | Funcționalități suplimentare (echipe 3) |

#### Etapa 4 — Prezentare (100 puncte)

| Criteriu | Puncte | Descriere |
|----------|--------|-----------|
| Demo live funcțional | 35 | Aplicația rulează și demonstrează cerințele |
| Prezentare tehnică | 25 | Explică arhitectura și deciziile |
| Răspunsuri la întrebări | 20 | Demonstrează înțelegerea profundă |
| Contribuție echipă | 15 | Fiecare membru știe tot codul |
| Respectare timp | 5 | 10-15 minute per echipă |

---

### 👥 Dimensiunea echipei

| Echipă | Cerințe |
|--------|---------|
| **1 persoană** | Funcționalitate de bază completă |
| **2 persoane** | + Testare extinsă + Documentație detaliată |
| **3 persoane** | + Extensii avansate + Analiză performanță |

---

## 📚 DESCRIEREA PROIECTULUI

Descriere detaliată
Acest proiect propune construirea unei rețele hibride care integrează noduri containerizate Docker într-o topologie virtuală Mininet. Scopul este de a experimenta cu conectivitatea containerelor într-un mediu de rețea personalizat și de a explora modul în care aplicațiile containerizate comunică peste rețea. Practic, se va extinde funcționalitatea Mininet prin utilizarea unei platforme precum Containernet (o versiune extinsă a Mininet care suportă containere Docker ca host-uri)[3]. Astfel, unele noduri din topologia emulată nu vor fi simple host-uri Linux generice, ci containere Docker care rulează servicii reale (de exemplu, un server web Nginx sau o bază de date MySQL).
Scenariul concret al proiectului ar putea fi simularea unei mici infrastructuri de microservicii: de pildă, un container rulează un serviciu web, alt container rulează un serviciu de baze de date, iar alte containere acționează ca clienți. Aceste containere sunt interconectate prin switch-uri virtuale în Mininet, permițând controlul detaliat al topologiei (de exemplu, putem insera un router virtual între servicii pentru a testa latența sau putem limita banda între containere). Proiectul va demonstra cum se configurează rețeaua Docker (bridge, interfețe virtuale) în contextul Mininet și cum pot fi orchestrate containerele în cadrul unei rețele personalizate. Totodată, oferă ocazia de a testa comunicarea inter-container în condiții variate (ex. restricții de rețea, latență simulată, pierdere de pachete) și de a observa performanța. Rezultatul final va fi o platformă de test reproductibilă, care combină flexibilitatea Mininet cu realismul containerelor, utilă pentru prototiparea serviciilor distribuite.

### 🎯 Obiective de învățare

Înțelegerea modului în care containerele Docker se conectează în rețea (bridge networks, veth pairs, etc.) și modul de integrare a acestora într-o topologie personalizată.
Familiarizarea cu conceptul de virtualizare la nivel de container versus virtualizare de rețea (Mininet) și explorarea beneficiilor integrării lor.
Dezvoltarea abilităților de configurare a ambiențelor de rețea complexe, care imită scenarii reale de microservicii, într-un mediu controlat de laborator.
Măsurarea și analizarea performanței rețelei containerizate: latență, debit (throughput), comportament în condiții de pierdere a pachetelor, etc., utilizând instrumente de test (iperf, ping, Apache Benchmark pentru HTTP, etc.).

### 🛠️ Tehnologii și unelte


### 📖 Concepte cheie

Rețele virtualizate – folosirea Mininet pentru a crea rețele virtuale personalizate (nivel 2/3) cu parametri controlați (topologie, bandwidth, delay).
Containere Docker – noțiuni de containerizare, imagini Docker, rețeaua implicită a containerelor (bridge Docker) vs. rețele personalizate.
Integrarea containerelor în rețea – conectarea containerelor la switch-urile Mininet prin interfețe virtuale, utilizarea Containernet sau configurare manuală cu veth pairs.
Protocoale de comunicație client-server – exemplificate de serviciile rulate în containere (HTTP pentru web, SQL pentru DB, etc.), plus mecanisme de rezoluție DNS interne Docker, dacă e cazul.
Testare și monitorizare de rețea – folosirea de utilitare (tcpdump, iperf, ab - Apache Benchmark) pentru a genera trafic și a colecta date de performanță.
Tehnologii implicate
Mininet/Containernet – platforma de emulare a rețelei. Containernet extinde Mininet pentru a suporta containere Docker ca noduri.
Docker – pentru a crea containere ce rulează servicii (imagini de Linux cu aplicațiile necesare). Vor fi utilizate comenzi Docker Compose sau Docker CLI pentru gestionarea containerelor.
Python – limbaj folosit pentru a orchestra scenariul (Mininet are API Python; se poate scrie un script Python care construiește topologia, lansează containere și configurează legăturile).
Linux networking tools – tc (Traffic Control) pentru a induce latență/pierderea de pachete pe linkuri dacă se dorește, brctl/ovs-vsctl pentru configurări fine ale bridge-urilor (dacă e cazul la nivel jos).
Servicii de test – ex: server HTTP (Nginx/Apache în container), server de bază de date (MySQL/PostgreSQL), plus clienți (curl, wget, scripturi Python) pentru a genera trafic de test.
Legătura cu temele din săptămânile cursului
Săptămâna 10: Virtualizare de rețea – proiectul combină virtualizarea rețelei (Mininet) cu virtualizarea containerelor (Docker), extinzând conceptele discutate în curs (vezi fișierul „Virtualizare și Cloud” din arhiva WEEK10).
Săptămâna 11: Rețele de containere și Docker – se aplică direct cunoștințele despre rețelele containerelor Docker (bridge, overlay) prezentate în săptămâna 11 (ex. laboratorul „Docker Networking” din arhivă), integrând containere în topologia Mininet.
Săptămâna 5: Adresare IP – definirea adreselor IP pentru containere în rețeaua Mininet cere înțelegerea subrețelelor (similar cu exercițiile din Week5 privind configurarea adreselor IP manual pentru noduri).
Săptămâna 8: Protocoale de aplicație – rularea unui serviciu web și a unei baze de date în containere atinge conceptele discutate în curs despre protocoale de nivel aplicație (HTTP, SQL over TCP etc.) și modul lor de funcționare în rețea.
Etapele proiectului

### 📋 Etapa 1 (Săptămâna 5) – Planificare și setup inițial: Investigarea modului în care Containernet (sau alternativa manuală) permite integrarea containerelor în Mininet. Alegerea unui scenariu de utilizare – de exemplu, aplicație web cu 2-3 microservicii. Se vor defini rolurile containerelor (ex: container A – server web, container B – bază de date, container C – client simulând utilizatorul). Livrabil: document de design ce include diagrama topologiei rețelei (arată switch-urile, containerele și legăturile dintre ele, plus subrețelele/IP-urile alocate fiecărui container), precum și pașii de configurare a mediului (versiuni de Mininet/Containernet, imagini Docker ce vor fi folosite sau create). Se va pregăti mediul de dezvoltare: instalarea Mininet/Containernet și crearea unui repository pentru proiect (cu eventuale Dockerfile-uri sau un docker-compose.yml de bază).


### 🔨 Etapa 2 (Săptămâna 9) – Implementare parțială: Construirea efectivă a topologiei și rularea containerelor. Se poate realiza un script Python care pornește Mininet, adaugă noduri de tip Docker container (folosind API-ul Containernet) și configurează conexiunile. Se vor crea sau descărca imaginile Docker necesare (de exemplu, o imagine cu serverul web configurat). Se testează comunicarea de bază: de exemplu, clientul din container C face o cerere HTTP către containerul A (server web) – pachetul traversează rețeaua Mininet și răspunsul ajunge înapoi. Livrabil: codul sursă al scriptului de configurare a rețelei (în repository), fișierele Dockerfile sau compose pentru definirea containerelor, și un jurnal de teste inițiale (loguri care arată că containerele se pingăsc reciproc, că serverul web răspunde la cereri din partea clientului etc.).


### 🔮 VERIFICARE ÎNȚELEGERE - SDN ȘI OPENFLOW

Înainte de a rula comenzile, răspundeți la următoarele întrebări:

1. Când rulați pingall în Mininet, între care perechi de host-uri va eșua ping-ul?
   → Analizați regulile de firewall din controller pentru a prezice rezultatul.

2. Ce mesaje OpenFlow vor apărea în log-ul controller-ului la primul ping?
   → Răspuns așteptat: PacketIn (cerere ICMP), apoi FlowMod (instalare regulă).

3. După instalarea regulii, ce se întâmplă la al doilea ping între aceleași host-uri?
   → Pachetele sunt procesate direct de switch, fără PacketIn către controller.

4. Câte reguli vor fi în tabela de flux după pingall?
   → Verificați cu: dpctl dump-flows


### ✅ Etapa 3 (Săptămâna 13) – Experimente și finalizare: Introducerea de scenarii de test mai complexe și colectarea rezultatelor. De exemplu, măsurarea timpului de răspuns al serviciului web din container A pentru diferite dimensiuni de trafic sau sub diferite întârzieri simulate pe legătura către client. Se pot aplica limite de bandă sau latență pe legăturile din Mininet pentru a vedea impactul asupra performanței aplicației distribuite. Totodată, se va asigura solideză: containerele pornesc în ordinea corectă, dacă un container este repornit, rețeaua încă funcționează etc. Livrabil: codul final (script Python, configurații) însoțit de documentație (README cu instrucțiuni clare de rulare a experimentului de către oricine), grafică/diagrama actualizată a topologiei finale și un raport de experimentare. Raportul va include descrierea testelor efectuate, metricile culese (latență, throughput, timpi de răspuns) sub formă de tabele/grafice, plus discuții. Se vor evidenția eventualele probleme întâlnite și soluțiile adoptate.


### 📊 PEER INSTRUCTION - DOCKER ȘI REȚELE CONTAINERE

Discutați cu colegii și alegeți împreună răspunsul corect:

Întrebarea 1: Containerele web și db sunt în aceeași rețea Docker bridge. Cum poate web să se conecteze la portul 5432 al db?

A) localhost:5432 - containerele partajează același localhost
B) db:5432 - Docker DNS rezolvă automat numele serviciului ✓
C) 172.17.0.1:5432 - adresa gateway-ului bridge
D) host.docker.internal:5432 - referință la mașina host

Explicație: Docker Compose creează DNS intern. Containerele se găsesc prin numele serviciului, nu prin localhost (care e izolat per container).

Întrebarea 2: Un container expune portul 8080:80. Ce înseamnă această configurare?

A) Containerul ascultă pe 8080, host-ul expune pe 80
B) Host-ul ascultă pe 8080, containerul intern pe 80 ✓
C) Ambele porturi sunt echivalente
D) Portul 8080 este blocat de firewall

Explicație: Formatul este HOST_PORT:CONTAINER_PORT. Accesați serviciul din browser la http://localhost:8080


### 🎤 Etapa 4 (Săptămâna 14) – Prezentare finală: Prezentarea va sublinia arhitectura hibridă a rețelei create, modul de integrare Docker–Mininet și rezultatele cheie ale experimentelor. Se va realiza o demonstrație: de exemplu, accesarea serviciului web din containerul A de către containerul C, cu monitorizarea traficului în direct (folosind ping sau ab pentru a arăta latența și throughput-ul). Livrabil: slide-urile prezentării și un demo live (sau înregistrat) care să ilustreze funcționalitatea rețelei hibride și eventual diferențele față de o configurație clasică.

Extensii posibile pentru echipe de 3 vs. 2/1 studenți
Pentru echipele de 3: proiectul se poate extinde prin creșterea complexității topologiei și a serviciilor. De exemplu, se pot lansa mai multe instanțe de containere pentru scalare (simulând un cluster de microservicii) și implementa un load-balancer în rețea care distribuie traficul între ele. O altă extensie ar fi integrarea unui orchestrator simplu (ex. Docker Compose sau chiar Kubernetes minikube dacă se dorește un challenge suplimentar) pentru a gestiona containerele la scară mai mare. Tot pentru echipe mai mari, s-ar putea monitoriza resursele (CPU, memorie) consumate de containere sub sarcină și include analiza acestor date în raport.
Pentru echipe mai mici (2 sau 1 student): se recomandă limitarea numărului de servicii/container la cele esențiale (de exemplu doar 2 containere care comunică direct) și evitarea configurărilor foarte complicate de rețea. Un singur switch și o singură subrețea pot fi suficiente. Opțional, se poate reduce amploarea testelor de performanță – de pildă, evaluarea se poate face doar calitativ (se vede că comunicarea are loc) și cu câteva măsurători simple de timp de răspuns, fără a intra în optimizări avansate. Astfel, încă se demonstrează integrarea Docker-Mininet, dar volumul de muncă rămâne gestionabil.

### ❓ ÎNTREBĂRI FRECVENTE - DOCKER

Q: Eroare "port is already allocated" la pornirea containerelor
A: Portul e ocupat de alt proces. Soluții:
   - Verificați: ss -tlnp | grep :PORT
   - Opriți procesul existent sau schimbați portul în docker-compose.yml

Q: Containerele nu pot comunica între ele
A: Verificați configurarea rețelei:
   - docker network ls (listează rețelele)
   - docker network inspect NETWORK_NAME (detalii)
   - Asigurați-vă că serviciile sunt în aceeași rețea

Q: Cum văd log-urile unui container pentru debugging?
A: Folosiți comenzile:
   - docker logs CONTAINER_NAME
   - docker compose logs SERVICE_NAME
   - docker compose logs -f (follow în timp real)


### 📚 Bibliografie

Dupont, C., & Qu, C. (2018). Containernet: A Network Emulator with Docker Support for SDN Experimentation. In Proceedings of the IEEE Conference on Network Function Virtualization and Software Defined Networks (NFV-SDN) (pp. 1-2). (Containernet – introducere și utilizare practică)
Hausenblas, M. (2018). Container Networking: From Docker to Kubernetes. O’Reilly Media. (prezentare a conceptelor de rețele pentru containere Docker și integrarea în infrastructuri cloud)
Merkel, D. (2014). Docker: Lightweight Linux Containers for Consistent Development and Deployment. Linux Journal, 2014(239), Articol 2. (introducere în containerizarea Docker și avantajele sale în medii de dezvoltare)
Alwahibee, A., Köpsel, A., & Karl, H. (2019). A Performance Evaluation of Container Networking. IEEE Transactions on Network and Service Management, 16(4), 1550-1563. https://doi.org/10.1109/TNSM.2019.2947599 (lucrare academică ce evaluează performanța rețelelor containerizate, relevantă pentru teste de performanță)
Documentație Containernet: Containernet GitHub Repository & Wiki. (2021). Disponibil la: https://github.com/containernet/containernet/wiki (resursă practică pentru configurarea Containernet și exemple de utilizare).
---

## 🔮 Verificare înțelegere — SDN și OpenFlow

Înainte de a rula comenzile, răspunde la aceste întrebări:

1. **Când rulezi `pingall` în Mininet, între care host-uri va eșua ping-ul?**
   - Analizează regulile de firewall din controller
   - Răspuns așteptat: Perechile care încalcă regulile (ex: ICMP blocat)

2. **Ce mesaje OpenFlow apar în log-ul controller-ului la primul ping?**
   - PacketIn (cerere ICMP) → FlowMod (instalare regulă)

3. **Ce se întâmplă la al doilea ping între aceleași host-uri?**
   - Switch-ul procesează direct, fără PacketIn

Verifică cu `dpctl dump-flows` câte reguli sunt instalate.

---

## 📊 Peer Instruction — SDN

**Întrebare:** După ce controller-ul instalează o regulă cu `actions=drop`, ce se întâmplă cu pachetele?

- A) Sunt trimise înapoi cu ICMP unreachable
- B) Sunt șterse silențios fără notificare ✓
- C) Sunt redirecționate către controller
- D) Sunt puse în coadă

**Explicație:** Acțiunea `drop` elimină pachetul complet, fără nicio notificare.


---

## ❓ Întrebări frecvente — Docker

**Q: Eroare "port is already allocated"**  
A: Portul e ocupat. Verifică: `ss -tlnp | grep :PORT` și oprește procesul sau schimbă portul.

**Q: Containerele nu comunică între ele**  
A: Verifică rețeaua: `docker network ls` și `docker network inspect NETWORK`

**Q: Cum văd logurile unui container?**  
A: `docker logs CONTAINER` sau `docker compose logs SERVICE`


---


---

## 🔗 TRANZIȚIE JAVASCRIPT → PYTHON

Ai experiență solidă în JavaScript din cursul de Tehnologii Web. Iată cum se traduc conceptele în Python pentru networking:

### Echivalențe de bază

| JavaScript (TW) | Python (Rețele) | Notă |
|-----------------|-----------------|------|
| `const fn = (x) => x * 2` | `fn = lambda x: x * 2` | Arrow functions → lambda |
| `arr.map(x => x * 2)` | `[x * 2 for x in arr]` | List comprehension e mai pythonic |
| `arr.filter(x => x > 0)` | `[x for x in arr if x > 0]` | Sau `filter()` |
| `arr.reduce((a,b) => a+b, 0)` | `sum(arr)` sau `functools.reduce()` | Python are `sum()` built-in |
| `JSON.parse(str)` | `json.loads(str)` | Parsare JSON |
| `JSON.stringify(obj)` | `json.dumps(obj)` | Serializare JSON |
| `async/await` | `async/await` cu `asyncio` | Sintaxa e similară! |
| `fetch(url)` | `requests.get(url)` | Sau `aiohttp` pentru async |
| `Buffer.from(str)` | `str.encode('utf-8')` | Conversie text → bytes |
| `buf.toString()` | `bytes.decode('utf-8')` | Conversie bytes → text |

### Servere: Express.js vs Python

```javascript
// Express.js (TW)
const express = require('express');
const app = express();

app.get('/api/data', (req, res) => {
    res.json({ message: 'Hello' });
});

app.listen(3000);
```

```python
# Flask (Python)
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/api/data')
def get_data():
    return jsonify({'message': 'Hello'})

app.run(port=3000)
```

### Async: Promises vs asyncio

```javascript
// JavaScript async (TW)
async function fetchData() {
    const response = await fetch(url);
    const data = await response.json();
    return data;
}
```

```python
# Python asyncio
import aiohttp
import asyncio

async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
```

### Sockets: Node.js vs Python

```javascript
// Node.js net module
const net = require('net');
const client = net.createConnection({ port: 8080 }, () => {
    client.write('Hello');
});
client.on('data', (data) => console.log(data.toString()));
```

```python
# Python socket
import socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 8080))
client.send(b'Hello')
data = client.recv(1024)
print(data.decode())
```


### 💡 Pentru Docker și Containere

Din TW știi npm și package.json. Docker e similar dar pentru mediu complet:

```yaml
# docker-compose.yml e similar cu package.json pentru dependențe
# dar include și mediul de runtime

services:
  web:
    image: nginx
    ports:
      - "8080:80"  # Similar cu "scripts": {"start": "node index.js"} pe port
  
  api:
    build: ./api    # Similar cu npm install din package.json
    environment:
      - DB_HOST=db  # Similar cu process.env.DB_HOST
```

```bash
# Comenzi similare
npm install     →  docker compose build
npm start       →  docker compose up
npm stop        →  docker compose down
npm run dev     →  docker compose up --watch
```


### 💡 Pentru Socket Programming

Din TW știi `fetch()` pentru HTTP. Acum lucrezi la nivel mai jos:

```python
# Serverul tău de chat e similar cu Express, dar la nivel TCP
import socket
import threading

def handle_client(conn, addr):
    """Similar cu app.get('/route', handler) dar pentru conexiuni raw"""
    while True:
        data = conn.recv(1024)  # Similar cu req.body
        if not data:
            break
        conn.send(data)  # Similar cu res.send()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 5000))  # Similar cu app.listen(5000)
server.listen(5)

while True:
    conn, addr = server.accept()
    # threading e similar cu async în conceptul de concurență
    threading.Thread(target=handle_client, args=(conn, addr)).start()
```

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `06roWSL/` — NAT/PAT și SDN

**Ce găsești relevant:**
- Integrarea rețelelor virtuale cu containere

**Fișiere recomandate:**
- `06roWSL/README.md` — prezentare generală și pași de laborator
- `06roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `06roWSL/docs/fisa_comenzi.md` — comenzi utile
- `06roWSL/src/` — exemple de cod Python
- `06roWSL/homework/` — exerciții similare


### 📁 `02roWSL/` — Programare Socket

**Ce găsești relevant:**
- Comunicarea între noduri

**Fișiere recomandate:**
- `02roWSL/README.md` — prezentare generală și pași de laborator
- `02roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `02roWSL/docs/fisa_comenzi.md` — comenzi utile
- `02roWSL/src/` — exemple de cod Python
- `02roWSL/homework/` — exerciții similare


### 📁 `01roWSL/` — Fundamentele Rețelelor

**Ce găsești relevant:**
- Topologii, adresare, comenzi de bază

**Fișiere recomandate:**
- `01roWSL/README.md` — prezentare generală și pași de laborator
- `01roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `01roWSL/docs/fisa_comenzi.md` — comenzi utile
- `01roWSL/src/` — exemple de cod Python
- `01roWSL/homework/` — exerciții similare


### 📁 `00-startAPPENDIX(week0)/PYTHON ghid de auto-perfectionare/`

**Resurse pentru Python networking:**
- `GHID_PYTHON_NETWORKING_RO.md` — ghid complet Python pentru rețele
- `cheatsheets/PYTHON_RAPID.md` — referință rapidă sintaxă
- `examples/01_socket_tcp.py` — exemplu sockets TCP
- `examples/02_bytes_vs_str.py` — lucrul cu bytes (important!)
- `examples/03_struct_parsing.py` — parsarea datelor binare


### 📁 `00-startAPPENDIX(week0)/00CURS/`

**Materiale teoretice:**
- Prezentări HTML pentru fiecare săptămână (S1-S14)
- Concepte aprofundate pentru examen


## 📝 Note finale

- **Verifică întotdeauna** că repository-ul GitHub e actualizat înainte de deadline
- **Testează** aplicația pe un calculator curat înainte de prezentare
- **Pregătește** răspunsuri pentru întrebări despre arhitectură și cod
- **Comunică** cu echipa pentru a vă coordona contribuțiile

---

*Ultima actualizare: 23 January 2026*  
*Rețele de Calculatoare — ASE București*
