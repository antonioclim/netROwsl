# Proiectul 09: Server FTP simplificat și testare multi-client cu containere

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
https://github.com/[username]/retele-proiect-09
```

#### Structura obligatorie a repository-ului

```
retele-proiect-09/
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

**Format:** `NUME_Prenume_GGGG_P09_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P09 | Numărul proiectului | P09 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P09_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P09_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P09_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect se concentrează pe realizarea unui serviciu de transfer de fișiere în rețea, similar ca principiu cu protocolul FTP (File Transfer Protocol), însă într-o versiune simplificată și adaptată pentru scop didactic. Studenții vor implementa un server de fișiere care poate gestiona conexiuni de la mai mulți clienți simultan, permițând acestora să listeze fișierele disponibile pe server și să descarce sau încărceze fișiere. Protocolul implementat poate fi inspirat de FTP clasic – cu o conexiune de control prin care se transmit comenzi precum LIST, GET (download), PUT (upload), și eventual o conexiune separată de date pentru transferul efectiv al fișierelor – sau poate fi o variantă simplificată ce folosește o singură conexiune TCP atât pentru comenzi cât și pentru date (pentru a reduce complexitatea). Indiferent de arhitectura aleasă, accentul va fi pus pe tratarea concurenței (mulți clienți pot cere simultan fișiere), pe integritatea transferurilor și pe gestionarea erorilor (de ex., dacă un client cere un fișier inexistent, serverul trimite un mesaj de eroare adecvat). După implementarea serverului și a unui client elementar de test (sau folosirea unui client generic de telnet/FTP dacă protocolul e compatibil), proiectul trece la a doua componentă majoră: testarea și evaluarea în mediu multi-client folosind containere Docker. Practic, echipa va crea un mediu de test automatizat în care mai multe instanțe de client (realizate fie ca scripturi, fie folosind imagini Docker care rulează comenzi de transfer) se conectează la serverul FTP implementat, pentru a demonstra că acesta poate deservi concomitent mai mulți utilizatori și pentru a măsura performanța (ex. timp de răspuns, lățime de bandă utilizată, eventual detectarea condițiilor de bottleneck). Se urmărește ca studenții să deprindă utilizarea containerelor pentru simularea unui mediu de rețea complex: de exemplu, se poate folosi Docker Compose pentru a lansa un container server și N containere client, fiecare client executând un set de operațiuni (download/upload) către server. Astfel, testele pot evidenția cum crește timpul de transfer când mai mulți clienți descarcă același fișier simultan (limitare de lățime de bandă) sau cum serverul face față la cereri paralele (prin thread-uri sau procese multiple). Pe latura educațională, proiectul oferă o înțelegere solidă a protocolului FTP și a problemelor practice precum segmentarea fișierelor, confirmarea primirii datelor, gestionarea directorilor, dar și o perspectivă asupra orchestrării containerelor pentru teste. Studenții vor învăța importanța sincronizării accesului la resurse comune (de exemplu, două transferuri simultane care scriu în același fișier pe server pot cauza probleme ce trebuie evitate) și vor acumula experiență în dezvoltarea de aplicații client-server solide.

### 🎯 Obiective de învățare


### 📖 Concepte cheie


### 🛠️ Tehnologii și unelte

Legătura cu temele și kiturile săptămânilor 1–13: Proiectul este strâns legat de săptămânile de curs/laborator în care s-au discutat protocoalele de aplicatie și programarea pe socket-uri. În special, săptămâna 3 și 4 – “Programare pe socket-uri: implementarea unui server concurent TCP și UDP și a clienților aferenți plus analiza traficului” – oferă baza pentru implementarea serverului FTP: în acele laboratoare studenții au scris servere concurrente simple (de chat, de exemplu) și acum aplică aceleași principii într-un context mai complex de transfer de fișiere. Săptămâna 5 (“Adresare și rutare; introducere simulator de rețea; configurare infrastructură”) a pregătit studenții în configurarea mediilor de rețea, cunoștințe utile pentru înțelegerea modului în care Docker conectează containerele într-o rețea virtuală izolată (conceptual similar cu un simulator de rețea). Săptămâna 8 (servicii Internet – implementare server HTTP) este înrudită, deoarece și acolo s-a implementat un protocol textual client-server; experiența dobândită la proiectul 8 poate fi reutilizată aici și viceversa. În mod deosebit, săptămâna 9 este direct relevantă: la seminarul 9 studenții au experimentat cu un server FTP custom și testare multi-client în containere – practic exact ceea ce face obiectul proiectului, deci proiectul consolidează și extinde laboratorul 9. Studenții pot folosi chiar soluțiile sau ideile din kitul săptămânii 9 ca punct de plecare, îmbunătățindu-le. Mai mult, proiectul atinge și conceptele de orchestrare din săptămâna 11 (containere multiple cu Docker Compose) când vine vorba de a porni întregul mediu de test. Săptămâna 13 (securitatea în rețele) poate fi tangential implicată dacă discutăm aspecte de securizare a FTP (protocol notoriu pentru transmiterea parolelor in clar – dacă echipa implementează autentificare, pot discuta despre acest risc și despre FTP Secure etc., deși implementarea efectivă de criptare e în afara scopului). Per ansamblu, proiectul este un excelent exemplu de integrare a cunoștințelor de rețele (socket-uri, protocoale, concurrency) cu cele de inginerie software (utilizarea containerelor, testare automatizată) dobândite pe parcursul semestrului.
Structură în 4 etape:
Extensii pentru echipe de 3 vs. echipe de 2/1: Pentru echipele de 3 studenți, se așteaptă o abordare mai cuprinzătoare a proiectului, eventual cu implementarea unor caracteristici suplimentare față de cerințele de bază. De exemplu, o echipă mare ar putea introduce autentificare pe serverul FTP simplificat: clienții trebuie să trimită un nume de utilizator și o parolă la început (ex. comanda USER și PASS ca în FTP), iar serverul verifică datele (într-un fișier de config simplu) înainte de a permite accesul la comenzi. Aceasta aduce în discuție și gestiunea permisiunilor – echipa ar putea implementa și conceptul de directoare home separate pentru utilizatori (sau cel puțin restricționarea accesului la anumite fișiere). O altă extensie posibilă pentru 3 membri este compatibilitatea cu un client FTP existent: de exemplu, ajustarea protocolului și a formatului mesajelor astfel încât un client standard (FileZilla sau linia de comandă ftp) să poată realiza cel puțin operațiile elementare (LIST, RETR, STOR) cu serverul lor. Aceasta ar necesita eforturi de conformitate cu RFC 959 (standardul FTP), dar ar fi foarte instructiv. Totodată, echipele de 3 ar trebui să pună accent și pe aspecte de securitate: pot implementa un mod pasiv în care serverul deschide un port dinamic pentru transfer de date (mai apropiat de FTP-ul original) sau pot adăuga o funcționalitate de checksum la finalul transferurilor pentru verificarea integrității (clientul trimite hash-ul fișierului încărcat, serverul îl compară cu hash-ul local calculat). În ceea ce privește testarea, echipele mari ar putea crește nivelul de complexitate: de exemplu, să testeze cu 10-15 containere client rulând simultan, sau să folosească un utilitar de testare automată a performanței (scripting cu expect sau pexpect pentru a simula interacțiuni reale). În schimb, echipele de 1-2 studenți se pot limita la cerințele esențiale: server concurent, transfer corect de fișiere, teste cu ~3 clienți simultani. Pentru aceștia, focusul ar fi pe a livra o implementare stabilă și bine documentată a cerințelor de bază, lăsând aspectele precum autentificarea sau compatibilitatea extinsă ca discuție teoretică la prezentare, nu neapărat implementate. Indiferent de mărimea echipei, calitatea codului (structurare, claritatea protocului), a testelor și capacitatea de a interpreta rezultatele este fundamentală și va fi criteriul principal de evaluare, extensiile fiind un bonus ce reflectă efortul suplimentar al echipelor mai numeroase.

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

Postel, J. B., & Reynolds, J. K. (1985). File Transfer Protocol (FTP). RFC 959 (IETF). https://doi.org/10.17487/RFC0959
Ponmalar, P. P., & Elakkiya, G. (2023). Multiple Client-Server Communication Using Socket in Python. International Journal of Science and Research, 12(4), 253-256. https://doi.org/10.21275/SR23326120021
Boettiger, C. (2015). An introduction to Docker for reproducible research. ACM SIGOPS Operating Systems Review, 49(1), 71-79. https://doi.org/10.1145/2723872.2723882
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


### 💡 Pentru Programare Asincronă

Din TW cunoști async/await cu Promises. Python e similar:

```python
# JavaScript Promise → Python asyncio

# JS: const results = await Promise.all([fetch(url1), fetch(url2)]);
# Python:
results = await asyncio.gather(
    fetch_async(url1),
    fetch_async(url2)
)

# JS: setTimeout(() => {}, 1000)
# Python:
await asyncio.sleep(1)

# JS: .then().catch()
# Python: try/except în async function
```

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `11roWSL/` — FTP, DNS, SSH

**Ce găsești relevant:**
- Protocolul FTP, comenzi, transfer fișiere

**Fișiere recomandate:**
- `11roWSL/README.md` — prezentare generală și pași de laborator
- `11roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `11roWSL/docs/fisa_comenzi.md` — comenzi utile
- `11roWSL/src/` — exemple de cod Python
- `11roWSL/homework/` — exerciții similare


### 📁 `02roWSL/` — Programare Socket

**Ce găsești relevant:**
- Server concurent, threading/async

**Fișiere recomandate:**
- `02roWSL/README.md` — prezentare generală și pași de laborator
- `02roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `02roWSL/docs/fisa_comenzi.md` — comenzi utile
- `02roWSL/src/` — exemple de cod Python
- `02roWSL/homework/` — exerciții similare


### 📁 `09roWSL/` — Nivelul Sesiune

**Ce găsești relevant:**
- Autentificare, sesiuni utilizator

**Fișiere recomandate:**
- `09roWSL/README.md` — prezentare generală și pași de laborator
- `09roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `09roWSL/docs/fisa_comenzi.md` — comenzi utile
- `09roWSL/src/` — exemple de cod Python
- `09roWSL/homework/` — exerciții similare


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
