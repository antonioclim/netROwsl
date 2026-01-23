# Proiectul 12: Serviciu web distribuit în containere Docker cu echilibrare de încărcare Nginx

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
https://github.com/[username]/retele-proiect-12
```

#### Structura obligatorie a repository-ului

```
retele-proiect-12/
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

**Format:** `NUME_Prenume_GGGG_P12_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P12 | Numărul proiectului | P12 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P12_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P12_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P12_S07.zip` — Verificare săptămâna 7

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


### 🛠️ Tehnologii și unelte


### 🎯 Obiective de învățare


### 📖 Concepte cheie


### 🛠️ Tehnologii și unelte

Legătura cu săptămânile și kiturile (WEEK1-14): Acest proiect integrează cunoștințe din partea a doua a cursului, în special cele legate de servicii Internet și virtualizare. Temele din săptămâna 8 (servicii Web și noțiuni de HTTP, proxy invers), săptămâna 9 (protocolul FTP și testare multi-client cu containere), săptămâna 10 (servicii DNS/SSH/FTP orchestrate în container) și săptămâna 11 (aplicații distribuite, Nginx load balancing pe containere Docker) sunt direct relevante. Kitul practic de la săptămâna 11, care demonstrează utilizarea Nginx ca load balancer pentru aplicații în Docker Compose, constituie un exemplu de bază pe care studenții îl pot extinde substanțial în cadrul proiectului. Totodată, cunoștințele generale despre rețele din săptămânile anterioare (protocolul TCP, modelul client-server din săptămânile 2-4) sunt necesare pentru a înțelege cum comunică microserviciile între ele. Proiectul consolidează și extinde aceste elemente, ducându-le spre un context aplicat de tip enterprise.

### 🛠️ Tehnologii și unelte


### 🔮 VERIFICARE ÎNȚELEGERE - DOCKER ȘI CONTAINERE

Înainte de a executa comenzile, răspundeți:

1. Câte containere vor fi create conform fișierului docker-compose.yml?
   → Numărați serviciile definite în fișierul de configurare.

2. Ce porturi vor fi expuse pe host?
   → Căutați secțiunile ports: din fiecare serviciu.

3. Ce se întâmplă dacă portul dorit este deja ocupat de alt proces?
   → Verificați cu: ss -tlnp | grep :PORT
   → Eroare așteptată: "port is already allocated"

4. Cum comunică containerele între ele în aceeași rețea Docker?
   → Prin numele serviciului (Docker DNS intern), nu prin localhost.


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


### Extensii pentru echipe de 3 vs. 2/1 membri: În cazul unei echipe de 3 studenți, se așteaptă o complexitate mai mare a sistemului. Aceasta poate include adăugarea unui microserviciu suplimentar (de exemplu, un serviciu de autentificare separat, sau un serviciu de caching), implementarea unui sistem de logare centralizată a evenimentelor (de tip ELK stack simplificat) pentru a monitoriza distribuția traficului, sau utilizarea unei scheme mai complexe de orchestrare (precum definirea unui health-check în Docker Compose pentru restartarea automată a containerelor nefuncționale). Totodată, echipele mai numeroase pot investiga și aspecte de securitate, precum rularea containerelor cu privilegii restrânse, folosirea rețelelor Docker distincte pentru izolare sau configurarea HTTPS pe Nginx cu certificate auto-semnate. Pentru echipele de 2 studenți sau individuale, scope-ul poate fi redus: de pildă, pot avea doar două servicii principale (frontend și backend + DB), iar echilibrarea de încărcare să fie demonstrată între două instanțe ale backend-ului. Complexitatea configurărilor Docker poate fi mai mică, concentrându-se pe funcționalitatea de bază (fără optimizări elaborate de securitate sau monitorizare). Important este ca și în varianta simplificată arhitectura pe microservicii și folosirea unui load balancer să fie prezente, chiar dacă la scară redusă, iar studenții să poată explica avantajele obținute (de exemplu, cum adăugarea unei a doua instanțe backend îmbunătățește timpul de răspuns sub sarcină).


═══════════════════════════════════════════════════════════════════════════════
📊 CERINȚĂ SUPLIMENTARĂ: ANALIZĂ COMPARATIVĂ
═══════════════════════════════════════════════════════════════════════════════
Pe lângă implementarea tehnică, includeți în raportul final o secțiune de analiză comparativă (1-2 pagini) care să conțină:

1. COMPARAȚIE CU ALTERNATIVE
   • Identificați cel puțin 2 tehnologii/abordări alternative pentru problema rezolvată
   • Argumentați de ce ați ales abordarea actuală

2. METRICI DE PERFORMANȚĂ
   Măsurați și raportați cel puțin 2 metrici relevante:
   • Latență (timp de răspuns) sau Throughput
   • Timp de convergență sau Utilizare resurse

3. LIMITĂRI ȘI ÎMBUNĂTĂȚIRI
   • Ce limitări conștiente are soluția voastră?
   • Cum ar putea fi extinsă sau îmbunătățită?
═══════════════════════════════════════════════════════════════════════════════


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

---

## 🔮 Verificare înțelegere — Docker

Înainte de a rula comenzile, răspunde:

1. **Câte containere vor fi create conform docker-compose.yml?**
   - Numără serviciile definite în fișier

2. **Ce porturi vor fi expuse pe host?**
   - Caută secțiunile `ports:` din fiecare serviciu

3. **Ce se întâmplă dacă portul 80 e deja ocupat?**
   - Verifică cu: `ss -tlnp | grep :80`
   - Eroare așteptată: "port is already allocated"

După `docker ps`, verifică că toate containerele au status "Up".

---

## 📊 Peer Instruction — Docker

**Întrebare:** Containerele `web` și `db` sunt în aceeași rețea Docker. Cum se conectează `web` la `db`?

- A) `localhost:5432`
- B) `db:5432` ✓
- C) `172.17.0.1:5432`
- D) `host.docker.internal:5432`

**Explicație:** Docker DNS rezolvă automat numele serviciilor din Compose.


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


### 💡 Pentru HTTP/REST

Din TW ai lucrat cu Express.js și REST. Acum construiești de la zero:

```python
# Parsarea HTTP manual vs Express automat
# În Express: req.headers, req.body, req.params

def parse_http_request(raw_data):
    """Ce face Express automat, tu faci manual"""
    lines = raw_data.decode().split('\r\n')
    method, path, version = lines[0].split()  # GET /api/users HTTP/1.1
    
    headers = {}
    for line in lines[1:]:
        if ': ' in line:
            key, value = line.split(': ', 1)
            headers[key] = value
    
    return method, path, headers

# Răspunsul HTTP manual vs res.json()
def http_response(status, body):
    """Ce face res.json() automat"""
    return f"HTTP/1.1 {status}\r\nContent-Type: application/json\r\n\r\n{body}"
```

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `11roWSL/` — Echilibrare de Sarcină

**Ce găsești relevant:**
- Nginx/HAProxy, algoritmi de load balancing

**Fișiere recomandate:**
- `11roWSL/README.md` — prezentare generală și pași de laborator
- `11roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `11roWSL/docs/fisa_comenzi.md` — comenzi utile
- `11roWSL/src/` — exemple de cod Python
- `11roWSL/homework/` — exerciții similare


### 📁 `10roWSL/` — REST și Servicii

**Ce găsești relevant:**
- Microservicii, API gateway

**Fișiere recomandate:**
- `10roWSL/README.md` — prezentare generală și pași de laborator
- `10roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `10roWSL/docs/fisa_comenzi.md` — comenzi utile
- `10roWSL/src/` — exemple de cod Python
- `10roWSL/homework/` — exerciții similare


### 📁 `08roWSL/` — Server HTTP

**Ce găsești relevant:**
- HTTP backend-uri, health checks

**Fișiere recomandate:**
- `08roWSL/README.md` — prezentare generală și pași de laborator
- `08roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `08roWSL/docs/fisa_comenzi.md` — comenzi utile
- `08roWSL/src/` — exemple de cod Python
- `08roWSL/homework/` — exerciții similare


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
