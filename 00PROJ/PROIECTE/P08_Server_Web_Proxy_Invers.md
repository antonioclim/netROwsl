# Proiectul 08: Server web personalizat și proxy invers

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
https://github.com/[username]/retele-proiect-08
```

#### Structura obligatorie a repository-ului

```
retele-proiect-08/
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

**Format:** `NUME_Prenume_GGGG_P08_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P08 | Numărul proiectului | P08 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P08_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P08_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P08_S07.zip` — Verificare săptămâna 7

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

Descriere: În acest proiect, studenții vor construi un sistem web simplificat, format dintr-un server HTTP creat de la zero și un proxy invers plasat în fața acestuia, cu scopul de a îmbunătăți scalabilitatea și securitatea serviciului. Practic, aplicația constă într-un server web minimal (realizat de studenți, de exemplu în Python, folosind socket-uri TCP) care poate răspunde la cereri HTTP de bază (precum cereri GET pentru anumite resurse statice), iar în fața acestuia un server de tip proxy invers (precum Nginx configurat corespunzător, sau chiar o aplicație custom) care primește cererile clienților și le redirecționează către serverul backend. Proxy-ul invers poate oferi funcționalități suplimentare precum cache (pentru a servi direct cererile repetitive fără a mai deranja backend-ul), terminarea conexiunilor TLS (dacă se extinde proiectul pe partea de securizare HTTPS) sau echilibrarea încărcării între mai multe instanțe de server (dacă serverul web este replicat, de exemplu, pe porturi diferite). Scopul educațional al proiectului este dublu: (1) studenții înțeleg în profunzime protocolul HTTP prin implementarea unui server “de la firul ierbii”, parcurgând întregul flux de procesare a unei cereri web (citirea cererii brute, interpretarea header-elor HTTP, formarea unui răspuns valid conform protocolului); (2) studenții se familiarizează cu arhitectura pe mai multe straturi a aplicațiilor web moderne, unde un proxy invers acționează ca intermediar între clienți și serverele de aplicație, aducând beneficii de performanță și securitate. Proiectul este extrem de practic: de la rularea serverului web personalizat (de exemplu, pornirea lui pe un anumit port și servirea unui fișier HTML simplu) până la configurarea unui proxy (de exemplu, Nginx sau Apache în mod proxy) care să preia traficul de pe portul 80 și să îl redirecționeze intern către portul pe care rulează serverul custom. Se vor realiza teste cu browsere reale sau cu utilitare precum curl, pentru a confirma că întreg lanțul funcționează: o cerere HTTP de la client trece prin proxy, ajunge la serverul implementat de student, acesta generează un răspuns (de exemplu, conținutul unui fișier sau un mesaj dinamic), iar răspunsul se întoarce la client prin proxy. Studenții vor putea observa îmbunătățirile aduse de proxy: de exemplu, dacă se activează caching, a doua cerere pentru aceeași resursă statică nu mai ajunge la backend (proxy-ul răspunde direct), scăzând latența. Opțional, se poate experimenta pornirea a două instanțe ale serverului backend (pe diferite porturi) și configurarea proxy-ului să facă load balancing (rund robin) – opțional, ca extensie – pentru a vedea cum se distribuie cererile. Toate aceste activități contribuie la consolidarea cunoștințelor despre protocoalele web și despre infrastructura serverelor web.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Limbaj de programare pentru server (Python este sugestia, folosind modulul socket sau biblioteci web simple; alternativ Java cu servlets minime, sau C cu sockets – dar Python va fi mai accesibil). Server proxy – de preferat Nginx, dat fiind că este foarte folosit ca reverse proxy și studenții ar beneficia să-l învețe; se vor scrie fișiere de configurare Nginx (bloc server cu directiva proxy_pass către backend). Opțional, Docker poate fi folosit pentru a containeriza serverul custom și Nginx-ul, demonstrând astfel portabilitatea configurației (de exemplu, un docker-compose cu două servicii: web și proxy). Instrumente de test: curl (pentru a trimite cereri HTTP manual și a vedea răspunsul brut), browsere web (pentru a testa accesul la serviciul web prin proxy), ab (ApacheBench) sau wrk (pentru teste de performanță rudimentare, ca să compare timpi cu caching vs. fără caching). Pentru debugging, Wireshark poate fi util dacă se doresc inspectate pachetele HTTP brute, însă log-urile text ale serverelor vor fi probabil suficiente.
Legătura cu temele și kiturile săptămânilor 1–13: Acest proiect cumulează cunoștințe din mai multe săptămâni, în principal din zona serviciilor Internet studiate după jumătatea cursului. Săptămâna 8 este direct relevantă: acolo studenții au parcurs implementarea unui server HTTP simplu și conceptul de proxy invers (probabil prin exemple practice cu Nginx). Proiectul extinde exact aceste aspecte – practic, este o aplicare amplă a tematicii de la seminarul 8. Totodată, realizarea serverului custom are legături cu săptămânile 2–4, când s-a discutat programarea pe socket-uri și implementarea de protocoale text/binar pe TCP/UDP. În acele laboratoare, studenții au dobândit abilitățile tehnice de bază pentru a construi acum un protocol ca HTTP (care este tot un protocol text bazat pe TCP) – ei au implementat poate un chat TCP simplu sau un protoco tip echo server, iar acum ridică complexitatea la nivelul unui protocol real, HTTP. Săptămâna 9, deși axată pe FTP și testare multi-client cu containere, este utilă deoarece noțiunile de concurență și testare sub încărcare apar și aici (serverul web trebuie testat cu mai mulți clienți simultan, similr cu testarea FTP). Săptămâna 11 (Aplicații distribuite cu Nginx și Docker) este foarte relevantă: acolo studenții au văzut cum se pot folosi containere multiple cu Docker Compose și un proxy pentru a gestiona trafic către mai multe servicii – cunoștințe direct aplicabile în extensiile proiectului (de exemplu, containerizarea soluției sau folosirea Nginx la potențial maxim). Chiar și săptămâna 13 (securitatea) are legătură: se poate menționa, de exemplu, cum proxy-ul invers poate oferi un punct central pentru implementarea unor politici de securitate (filtrarea unor URL-uri malițioase, protecție împotriva unor atacuri web simple). Astfel, proiectul servește ca punte de legătură între mai multe subiecte din fișa disciplinei: programare de rețea, servicii web, infrastructură distribuită și securitate, într-un tot unitar.
Structură în 4 etape:
Extensii pentru echipe de 3 vs. echipe de 2/1: Proiectul este conceput să fie modular, permițând echipelor mai mari să implementeze caracteristici adiționale care demonstrează un plus de cunoaștere. O echipă de 3 studenți, de exemplu, ar trebui să abordeze atât partea de server custom, cât și configurarea avansată a proxy-ului. Ei ar putea implementa suport pentru mai multe tipuri de conținut pe serverul web (de exemplu, servirea dinamică a unui conținut generat pe loc – un script CGI simplu sau un răspuns care include data curentă, nu doar fișiere statice). Totodată, ar putea gestiona conexiuni simultane prin multithreading sau multiprocessing pe serverul custom, asigurându-se că pot deservi cel puțin 5-10 clienți concurenți fără blocaje. Pe componenta de proxy, echipa de 3 poate activa și ajusta parametri de performanță (dimensiunea cache-ului, politici de expirare) și poate prezenta metrici cuantificabile (cache hit rate, reducerea load-ului pe backend). O altă extensie valoroasă este containerizarea completă a aplicației: echipa poate furniza un fișier Docker Compose cu două servicii (backend-ul custom și Nginx) astfel încât proiectul să poată fi pornit ușor oriunde, consolidând totodată cunoștințele legate de săptămâna 11. Pentru echipele mai mici (2 studenți sau individual), se recomandă focalizarea pe cerințele de bază – un singur server backend și un proxy funcțional – eventual fără implementarea echilibrării încărcării pe multiple instanțe. Un student singur, de exemplu, ar putea decide să nu activeze TLS sau autentificare, concentrându-se în schimb pe asigurarea compatibilității HTTP și pe cache. Diferențierea se va vedea și în nivelul de detaliu al documentației: echipele mari pot furniza o documentație mai amplă (inclusiv tutorial de deploy, scripturi de automatizare), pe când cele mici pot livra un raport mai succint. Esențial este că toate echipele, indiferent de mărime, vor obține o mai bună înțelegere a funcționării serverelor web și a proxy-urilor, dar complexitatea și polish-ul implementării vor fi mai ridicate în proiectele echipelor de 3, conform așteptărilor.

### ❓ ÎNTREBĂRI FRECVENTE - HTTP/WIRESHARK

Q: Nu văd niciun trafic HTTP în Wireshark
A: Verificați:
   - Interfața selectată (pentru localhost, folosiți loopback/lo)
   - Filtrul aplicat (http sau tcp.port == 80)
   - Că serverul și clientul sunt pornite

Q: Traficul HTTPS apare ca date criptate, nu pot vedea conținutul
A: Este comportamentul normal și corect al HTTPS. Pentru debugging:
   - Folosiți HTTP pentru teste locale (nu în producție!)
   - Sau configurați Wireshark cu cheile TLS (avansat)

Q: Cum pornesc rapid un server HTTP pentru teste?
A: Python oferă un server simplu:
   python3 -m http.server 8080
   Apoi accesați http://localhost:8080


### 📚 Bibliografie

Fielding, R. T., & Reschke, J. (2014). Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing. RFC 7230 (IETF). https://doi.org/10.17487/RFC7230
Mohan, K., & Rengarajan, A. (2024). Reverse Proxy Technology. International Journal of Innovative Research in Computer and Communication Engineering, 12(2), 1067-1071. https://doi.org/10.15680/IJIRCCE.2024.1202057
Skvorc, D., & Ilakovac, V. (2014). An Educational HTTP Proxy Server. Procedia Engineering, 69, 128-132. https://doi.org/10.1016/j.proeng.2014.02.212
---

## 🔮 Verificare înțelegere — HTTP

Înainte de a captura trafic:

1. **Câte pachete TCP apar pentru o cerere HTTP GET?**
   - 3 handshake + request + response + FIN = minim 6-8 pachete

2. **Ce cod de status indică "resursă negăsită"?**
   - 404 Not Found

3. **Ce diferență există între HTTP și HTTPS în Wireshark?**
   - HTTP: conținut vizibil în clar
   - HTTPS: date criptate TLS

---

## 📊 Peer Instruction — HTTP

**Întrebare:** Ce înseamnă codul HTTP 301?

- A) Cerere reușită (OK)
- B) Resursă mutată permanent (redirect) ✓
- C) Eroare de server
- D) Resursa nu există

**Explicație:** 2xx=Success, 3xx=Redirect, 4xx=Client error, 5xx=Server error


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

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `08roWSL/` — Server HTTP și Proxy Invers

**Ce găsești relevant:**
- HTTP protocol, reverse proxy cu Nginx

**Fișiere recomandate:**
- `08roWSL/README.md` — prezentare generală și pași de laborator
- `08roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `08roWSL/docs/fisa_comenzi.md` — comenzi utile
- `08roWSL/src/` — exemple de cod Python
- `08roWSL/homework/` — exerciții similare


### 📁 `10roWSL/` — HTTP/S și REST

**Ce găsești relevant:**
- Request/response handling, headers

**Fișiere recomandate:**
- `10roWSL/README.md` — prezentare generală și pași de laborator
- `10roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `10roWSL/docs/fisa_comenzi.md` — comenzi utile
- `10roWSL/src/` — exemple de cod Python
- `10roWSL/homework/` — exerciții similare


### 📁 `11roWSL/` — Load Balancing

**Ce găsești relevant:**
- Distribuția cererilor între backend-uri

**Fișiere recomandate:**
- `11roWSL/README.md` — prezentare generală și pași de laborator
- `11roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `11roWSL/docs/fisa_comenzi.md` — comenzi utile
- `11roWSL/src/` — exemple de cod Python
- `11roWSL/homework/` — exerciții similare


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
