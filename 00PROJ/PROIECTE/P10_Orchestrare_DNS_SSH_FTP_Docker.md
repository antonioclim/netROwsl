# Proiectul 10: Orchestrarea serviciilor de rețea (DNS, SSH, FTP) cu Docker

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
https://github.com/[username]/retele-proiect-10
```

#### Structura obligatorie a repository-ului

```
retele-proiect-10/
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

**Format:** `NUME_Prenume_GGGG_P10_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P10 | Numărul proiectului | P10 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P10_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P10_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P10_S07.zip` — Verificare săptămâna 7

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

Descriere: Proiectul numărul 10 își propune realizarea unei mici infrastructuri de rețea containerizate care integrează mai multe servicii esențiale – un server DNS, un server SSH și un server FTP – orchestrate într-un mediu Docker comun. Scopul este ca studenții să înțeleagă modul în care diferite servicii de rețea pot coopera și pot fi gestionate împreună folosind instrumente moderne de containerizare și orchestrare. Concret, echipa va configura trei containere principale, fiecare rulând câte un serviciu: - Un container DNS (folosind de exemplu BIND9 sau un server DNS minimalist) care să rezolve numele celorlalte servicii în rețeaua virtuală (de exemplu, un nume de domeniu intern precum ftp.local către IP-ul serverului FTP și ssh.local către IP-ul serverului SSH). - Un container SSH (bazat pe o imagine de Linux care are un server OpenSSH instalat) permițând logarea remote securizată. Acesta va simula o mașină în care utilizatorii se pot conecta prin SSH. - Un container FTP (de exemplu rulând vsftpd sau folosind serverul implementat în Proiectul 9 dacă se dorește reutilizarea) pentru transfer de fișiere.
Toate aceste containere vor fi plasate în aceeași rețea Docker internă, astfel încât să poată comunica între ele prin hostname-urile definite (DNS-ul custom va juca un rol crucial aici). În plus, se va include un container client (sau se vor folosi direct utilitare pe host) pentru a testa accesul la aceste servicii: de exemplu, rularea unor comenzi nslookup către DNS, ssh către serverul SSH și ftp către serverul FTP, folosind numele de domeniu interne stabilite. Proiectul implică astfel configurarea corectă a fiecărui serviciu (zone DNS, utilizatori și chei SSH, directoare și permisiuni FTP etc.), precum și scrierea unui fișier Docker Compose care să pornească toată suita de containere și să asigure conectivitatea lor. Un aspect important este gestionarea rețelelor Docker: se va crea o rețea custom (bridge network) pentru aceste servicii, în care DNS-ul poate funcționa ca nameserver central. Studenții vor învăța cum să expună porturile serviciilor către sistemul gazdă (dacă doresc acces din exterior, de exemplu portul 21 FTP, 22 SSH, 53 DNS), dar accentul proiectului este pe serviciile ce comunică între ele în interior. Se vor aborda aspecte de securitate și izolare: fiecare serviciu rulează într-un container dedicat, astfel încât eventualele probleme ale unuia (ex. un crash sau un atac asupra serverului FTP) să nu compromită direct celelalte servicii. Studenții vor experimenta actualizarea unei componente fără a le opri pe celelalte (ex. reconfigurarea serverului DNS și repornirea containerului DNS, verificând că SSH și FTP rămân funcționale). În ansamblu, proiectul reflectă scenariul real din administrația de sistem, la scară mică, demonstrând beneficiile containerizării în rularea serviciilor de infrastructură de rețea.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Docker și Docker Compose (ultimele versiuni) vor fi instrumentele centrale. Imaginii docker: - Pentru DNS: imagine oficială bind9 sau construirea unei imagini pornind de la Debian/Alpine cu bind instalat și configurat. - Pentru SSH: imagine linux (ex. atmoz/sftp pentru un setup rapid de SFTP, sau ubuntu:latest cu OpenSSH server configurat). - Pentru FTP: imagine vsftpd (există imagini pregătite pe DockerHub) sau un server custom (dacă se folosește proiectul anterior, se creează un Dockerfile ce copiază binarul/serverul Python și rulează). - Pentru testare se poate folosi alpine cu utilitarele dig, ftp, ssh instalate pentru a executa comenzi de test. Configurări: fișiere de zonă DNS (montate ca volum în containerul DNS), fișier de config vsftpd (volum la container FTP), chei SSH (volum la container SSH pentru persistență). Linux command-line tools: dig (DNS lookup), ping, ftp/lftp, ssh/scp, etc., pentru verificări. Eventual netcat pentru debug de porturi. Git pentru versionare și poate un Makefile pentru a porni/opri rapid Compose.
Legătura cu temele și kiturile săptămânilor 1–13: Acest proiect este practic încununarea multor subiecte parcurse de-a lungul semestrului, punându-le cap la cap într-un sistem complet. Legătura directă este cu săptămâna 10 – “Servicii de rețea: DNS, SSH, FTP în containere orchestrate cu Docker”. Conform fișei, exact asta au făcut studenții la seminarul 10, deci proiectul extinde laboratorul acela, cerând o realizare mai amplă și integrată. În acel context, studenții au deja cunoștințele de bază despre configurarea DNS (probabil s-au jucat cu dnsmasq sau BIND), despre configurarea unui server FTP/SSH în container. Proiectul îi forțează să refacă acele configuri pe cont propriu, ceea ce consolidează învățarea. Proiectul atinge și săptămâna 11 (Aplicații distribuite cu Docker Compose, Nginx etc.) deoarece folosesc Compose pentru orchestrare și creează un mic ecosistem de containere – exact conceptul de microservicii studiat. Săptămâna 7 și 13 (securitate rețele) pot fi aduse în discuție: ex. în securizarea SSH (chei in loc de parole), în izolare. Săptămâna 5 (config infrastructură) e tangential relevantă – modul în care se atribuie IP-uri containerelor e similar cu configurarea unei rețele virtuale. Săptămâna 8 (reverse proxy) nu e direct folosită aici, deși studenții ar putea, ca extensie, să introducă și un proxy invers în fața FTP pentru a securiza conexiunile, dar nu este necesar. Una peste alta, proiectul se bazează intens pe seminarele 9-11, integrând totodată cunoștințe de la început (protocoluri de bază) și de la final (administrare securizată). Este ultimul pas înainte de proiectul final, deci se potrivește ca nivel de dificultate cumulativă.
Structură în 4 etape:
Extensii pentru echipe de 3 vs. echipe de 2/1: O echipă de 3 studenți va putea aborda proiectul într-un mod mai cuprinzător, posibil integrând servicii adiționale sau configurări mai complexe. De exemplu, o extensie valoroasă pentru echipele mari ar fi adăugarea unui proxy invers și server web la infrastructură: implementarea unui container cu Nginx configurat ca reverse proxy pentru serverul FTP (transformând accesul la fișiere într-un serviciu web HTTP) sau pentru a oferi o interfață web către un depozit de fișiere. Aceasta ar demonstra cunoștințele din proiectul 8 integrate aici. Totodată, echipele de 3 ar putea configura replicare DNS – adică să aibă un al doilea container DNS ca slave pentru zona, simulând redundanța. Un alt aspect de extins este securitatea: de exemplu, implementarea SSL/TLS pentru serviciul FTP (FTPS) și pentru serviciul SSH forțarea autentificării prin chei și dezactivarea parolelor, plus eventuale iptables rules în containere (deși rețeaua e izolată). Echipele mai numeroase ar putea automatiza testele cu un script care rulează în containerul client și raportează succesele (facilitând verificarea). Tot ele ar putea documenta modul de recuperare în caz de eșec: ex. dacă DNS-ul cade, cum se reconfirmă rezolvarea (script de healthcheck în Compose). Pentru echipele de 1-2 studenți, focalizarea va fi pe a face cele 3 servicii să funcționeze corect împreună conform cerințelor de bază, fără neapărat a adăuga componente extra. Un student singur ar putea alege să folosească imagini deja existente și să integreze totul mai degrabă decât să construiască imagini de la zero, ceea ce e acceptabil dacă configurarea este totuși personalizată. Complexitatea orchestratului poate fi redusă: de exemplu, dacă întâmpină dificultăți majore cu DNS-ul custom, un student ar putea folosi DNS-ul intern al Docker (care rezolvă numele containerelor după service name), deși nu e atât de educativ – totuși, minim ar trebui să demonstreze că numele DNS funcționează. Diferența de evaluare va ține cont de aceste aspecte: echipele mari, prin implementările și extensiile lor, vor arăta o stăpânire mai bună a subiectului și vor fi punctate în consecință, în timp ce echipele mici vor fi apreciate pentru simplitatea funcțională și claritatea cu care acoperă cerințele esențiale.

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

Mockapetris, P. V. (1987). Domain names - Implementation and Specification. RFC 1035 (IETF). https://doi.org/10.17487/RFC1035
Burns, B., Grant, B., Oppenheimer, D., Brewer, E., & Wilkes, J. (2016). Borg, Omega, and Kubernetes. Communications of the ACM, 59(5), 50-57. https://doi.org/10.1145/2890784
Yazán, A., Tipantuña, C., & Carvajal-Rodriguez, J. (2024). Containers-Based Network Services Deployment: A Practical Approach. Enfoque UTE, 15(1), 36-44. https://doi.org/10.29019/enfoqueute.1005
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

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `11roWSL/` — FTP, DNS, SSH

**Ce găsești relevant:**
- Configurare BIND, vsftpd, OpenSSH

**Fișiere recomandate:**
- `11roWSL/README.md` — prezentare generală și pași de laborator
- `11roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `11roWSL/docs/fisa_comenzi.md` — comenzi utile
- `11roWSL/src/` — exemple de cod Python
- `11roWSL/homework/` — exerciții similare


### 📁 `10roWSL/` — Servicii de Rețea

**Ce găsești relevant:**
- Docker Compose, orchestrare multi-container

**Fișiere recomandate:**
- `10roWSL/README.md` — prezentare generală și pași de laborator
- `10roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `10roWSL/docs/fisa_comenzi.md` — comenzi utile
- `10roWSL/src/` — exemple de cod Python
- `10roWSL/homework/` — exerciții similare


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
