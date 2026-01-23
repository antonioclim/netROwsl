# Proiectul 18: Aplicație de chat client-server utilizând socket-uri TCP

> **Disciplina:** Rețele de Calculatoare  
> **Program:** Informatică Economică, Anul 3, Semestrul 2  
> **Instituție:** ASE București - CSIE  
> **Tip proiect:** Rezervă (individual)

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
https://github.com/[username]/retele-proiect-18
```

#### Structura obligatorie a repository-ului

```
retele-proiect-18/
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

**Format:** `NUME_Prenume_GGGG_P18_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P18 | Numărul proiectului | P18 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P18_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P18_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P18_S07.zip` — Verificare săptămâna 7

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

Descriere: Proiectul propune dezvoltarea unei aplicații simple de tip chat (mesagerie în timp real) care funcționează pe arhitectura client-server folosind socket-uri de rețea. În esență, se va implementa un server care acceptă conexiuni de la mai mulți clienți și retransmite mesajele primite către toți participanții (un chat în grup în linie de comandă). Clienții vor fi aplicații care se conectează la server prin TCP și trimit/recepționează mesaje text. Scopul proiectului este de a oferi studenților o experiență practică în programarea pe socket-uri și gestionarea comunicării concurente, ilustrând modul în care datele aplicative circulă prin rețea și cum se poate construi un serviciu de comunicații în timp real. Proiectul pune accent pe conceptele de bază: conectarea la un server prin adresa IP și port, schimbul de mesaje prin intermediul fluxurilor TCP, tratarea evenimentelor de rețea (noutăți, deconectări) și închiderea corectă a conexiunilor.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Un limbaj de programare suportând socket-uri – Python (recomandat, datorită simplității, folosind modulul socket și eventual threading/asyncio), sau alternativ Java, C#, C etc. Biblioteci standard de rețea. Eventual bibliotecă de threading sau async a limbajului. Wireshark sau utilitare de rețea pentru testare (opțional, pentru a vizualiza traficul). Mediul de dezvoltare la alegere (PyCharm, Eclipse, etc.). Protocolul TCP/IP va fi folosit la nivel de transport, iar aplicația definește un protocol simplu la nivel de conținut al mesajelor.
Legătura cu săptămânile și kiturile: Acest proiect se bazează pe cunoștințele acumulate în săptămâna 3 (Introducere în programarea de rețea – conceptul de socket) și săptămâna 8 (Nivelul transport – TCP/UDP, care oferă fundamentele teoretice despre conexiuni și porturi). În laborator, seminariile 2 și 3 au acoperit programarea de bază pe socket-uri (inclusiv un server concurent TCP și comunicarea cu mai mulți clienți). Kitul de pornire oferit la laborator (exemplu de cod de server și client simplu) va fi punctul de plecare în realizarea proiectului. Studenții vor extinde acele exemple pentru a implementa funcționalitatea de chat multi-client. Proiectul este astfel o continuare practică a exercițiilor de laborator, demonstrând într-un mod integrat cunoștințele despre socket-uri și programare concurentă în rețea.
Structura pe 4 etape: 1. Etapa 1: Proiectarea aplicației și setarea mediului de dezvoltare. Echipa definește cerințele aplicației de chat: formatul mesajelor, funcționalitățile dorite (de exemplu, toți utilizatorii văd mesajele tuturor, posibil un prefix cu numele expeditorului). Se stabilește limbajul de programare ce va fi folosit și se configurează mediul (crearea proiectului, verificarea bibliotecilor de socket disponibile, eventual realizarea unui plan de clasă/modul). Totodată, se decide protocolul textual simplu (de exemplu, mesajele trimise de server către clienți vor fi prefixate cu “[User]: mesaj”). La finalul acestei etape, se realizează o diagramă sau pseudo-cod care explică fluxul: clientul se conectează, serverul acceptă și pornește un fir de execuție dedicat, apoi orice mesaj de la un client este recepționat de server și retransmis tuturor. 2. Etapa 2: Implementarea serverului de chat. În această etapă se scrie codul pentru server. Serverul va crea un socket, îl va lega la un port (configurat implicit, de exemplu 5000), și va asculta (listen) conexiuni. Se implementează bucla de acceptare: când un client se conectează, serverul lansează un thread nou sau o sarcină asincronă care se ocupă de comunicarea cu acel client. Fiecare thread va primi mesajele de la clientul asociat și le va pune la dispoziția serverului central pentru difuzare. Trebuie menținută o listă înregistrată a tuturor conexiunilor clienților activi. Se acordă atenție sincronizării accesului la această listă dacă se folosesc thread-uri multiple. Se implementează funcționalitatea de broadcast: atunci când se primește un mesaj de la un client, serverul îl trimite tuturor celorlalți clienți (sau tuturor, inclusiv expeditorul, în funcție de decizie). Se tratează și cazul special al deconectării unui client (thread-ul asociat detectează EOF pe socket, anunță serverul central să elimine clientul din listă și se închide). 3. Etapa 3: Implementarea clientului și testarea comunicării. În paralel sau după server, se implementează aplicația client. Clientul va crea un socket și se va conecta (connect) la server (IP-ul serverului și portul cunoscut). După conectare, clientul poate avea două componente: una de citire (care ascultă mesaje venite de la server și le afișează utilizatorului) și una de scriere (preia input de la utilizator de la consolă și trimite mesaje serverului). Aceste componente pot fi implementate fie cu thread-uri separate (un thread pentru recepția de mesaje, unul pentru trimiterea lor, pentru a putea funcționa concurent) fie folosind mecanisme non-blocante. Se testează aplicația rulând un server și apoi mai mulți clienți (de exemplu, în console separate) și verificând că mesajele trimise de un client apar la ceilalți. Se vor realiza teste cu diferite scenarii: clienți care trimit mesaje simultan, clienți care se conectează și deconectează pe parcurs, etc., pentru a se asigura că serverul rămâne stabil și distribuie corect mesajele. 4. Etapa 4: Îmbunătățiri, securitate și documentare. Ultima etapă este dedicată eventualelor extensii opționale și întocmirii documentației. Extensiile pot include implementarea unor comenzi speciale (de ex. un client poate trimite /exit pentru a ieși, iar serverul gestionează acest eveniment), sau adăugarea unui mecanism simplu de login/alias astfel încât utilizatorii să aibă nume în chat. Opțional, se poate discuta despre securitatea minimală a aplicației – de exemplu, conștientizarea că mesajele circulă în clar și că aplicația nu are autentificare, menționând posibile remedieri (criptare cu TLS, parole). Documentația va descrie structura aplicației (modul în care serverul și clientul au fost implementați, eventuala diagramă de clase), protocolul de comunicare text (inclusiv exemple de mesaje brute), și instrucțiuni de utilizare (cum se pornește serverul, cum se pornesc clienții, ce rezultate se obțin). Se vor include capturi de ecran sau loguri de exemplu de la o sesiune de chat în care se văd mesajele transmise. Lucrarea se încheie cu concluzii privind experiența de programare de rețea dobândită și legătura între teorie (socket/TCP) și practică.
Extensii pentru echipe de 3/2/1: - Echipe de 3 persoane: Se recomandă implementarea unor funcționalități suplimentare care să aducă un plus de complexitate proiectului. De exemplu: suport pentru mesaje private (adresate de un client către un anumit alt client, identificat printr-un nume sau ID), o interfață grafică simplă pentru client (folosind o bibliotecă GUI, dacă timpul permite, în locul consolei), sau implementarea unui protocol rudimentar de criptare a mesajelor (de tip XOR sau alt algoritm simplu, doar pentru a ilustra securizarea). Orice astfel de extensie care implică design și cod suplimentar va evidenția capacitatea echipei de a coordona o aplicație mai complexă. Echipa de 3 poate scrie teste mai ample, măsurând de exemplu performanța serverului (câți clienți poate deservi, latența medie la trimiterea mesajelor) și include aceste observații în documentație. - Echipe de 2 persoane: Vor implementa versiunea standard a aplicației de chat, conform descrierii de bază: comunicare multi-client prin server, interfață în consolă, distribuția tuturor mesajelor către toți clienții. Sarcinile pot fi împărțite între membri (unul se ocupă preponderent de server, altul de client, apoi teste în comun). Extensiile complicate nu sunt necesare, dar pot fi incluse mici îmbunătățiri cum ar fi afișarea orei mesajului sau curățarea elegantă a resurselor la închiderea aplicației. Se va pune accent pe solideză: de ex., tratarea eventualelor erori de rețea fără ca aplicația să se oprească abrupt. - Echipe de 1 persoană: Un proiect individual va realiza o aplicație de chat funcțională, însă posibil cu limitări față de cerințele complete. De exemplu, studentul poate implementa inițial un chat unul-la-unu (un singur client și un server care comunică) pentru a stăpâni bazele, apoi poate extinde la mai mulți clienți dacă timpul permite. Dacă implementarea multi-client este dificilă, se poate accepta o versiune cu doi clienți și server (fire separate) pentru demonstrarea conceptului. Important este ca studentul să demonstreze că știe să folosească socket-urile și să explice în raport cum ar extinde aplicația pentru mai mulți utilizatori. În documentație, pot fi menționate și elemente neimplementate din lipsă de timp (de exemplu, “cum ar fi putut fi adăugat un thread suplimentar pentru al treilea client” etc.), arătând astfel înțelegerea conceptului chiar dacă implementarea practică este limitată.

### ❓ ÎNTREBĂRI FRECVENTE - MEDIU DE LUCRU

Q: WSL nu pornește sau este foarte lent
A: Verificări recomandate:
   - Virtualizarea e activată în BIOS
   - Rulați: wsl --update
   - Alocați mai multă memorie în .wslconfig

Q: Cum accesez fișierele Windows din WSL Ubuntu?
A: Sunt montate în /mnt/:
   - /mnt/c/ pentru C:   - /mnt/d/ pentru D:
Q: Comenzile docker nu funcționează
A: Verificați:
   - docker --version (instalat corect?)
   - Docker Desktop e pornit (pe Windows)
   - Userul e în grupul docker: sudo usermod -aG docker $USER


### 📚 Bibliografie

Rhodes, B., & Goerzen, J. (2014). Foundations of Python Network Programming (Third Edition). Apress. DOI: 10.1007/978-1-4302-5855-1
Postel, J. (1981). Transmission Control Protocol – DARPA Internet Program Protocol Specification. RFC 793, IETF. DOI: 10.17487/RFC0793
---

## 🔮 Verificare înțelegere — Socket-uri TCP

Înainte de a rula serverul:

1. **Ce se întâmplă dacă portul e ocupat?**
   - Eroare: "Address already in use"
   - Soluție: `SO_REUSEADDR` sau alt port

2. **Câte conexiuni poate accepta serverul?**
   - Depinde de `listen()` și threading

3. **Ce se întâmplă când un client se deconectează brusc?**
   - `recv()` returnează 0 bytes sau excepție `ConnectionResetError`


---

## ❓ Întrebări frecvente

**Q: WSL nu pornește sau e lent**  
A: Verifică virtualizarea în BIOS și rulează `wsl --update`

**Q: Cum accesez fișierele Windows din WSL?**  
A: Sunt în `/mnt/c/`, `/mnt/d/` etc.

**Q: Docker nu funcționează**  
A: Verifică: `docker --version`, Docker Desktop pornit, user în grupul docker


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


### 📁 `02roWSL/` — Programare Socket

**Ce găsești relevant:**
- TCP sockets, server concurent

**Fișiere recomandate:**
- `02roWSL/README.md` — prezentare generală și pași de laborator
- `02roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `02roWSL/docs/fisa_comenzi.md` — comenzi utile
- `02roWSL/src/` — exemple de cod Python
- `02roWSL/homework/` — exerciții similare


### 📁 `03roWSL/` — Broadcast

**Ce găsești relevant:**
- Mesaje către toți utilizatorii

**Fișiere recomandate:**
- `03roWSL/README.md` — prezentare generală și pași de laborator
- `03roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `03roWSL/docs/fisa_comenzi.md` — comenzi utile
- `03roWSL/src/` — exemple de cod Python
- `03roWSL/homework/` — exerciții similare


### 📁 `09roWSL/` — Nivelul Sesiune

**Ce găsești relevant:**
- Gestionarea sesiunilor utilizator

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
