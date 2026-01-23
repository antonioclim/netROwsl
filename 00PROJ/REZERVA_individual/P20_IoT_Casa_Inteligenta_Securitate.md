# Proiectul 20: Rețea IoT pentru casă inteligentă – simulare și măsuri de securitate

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
https://github.com/[username]/retele-proiect-20
```

#### Structura obligatorie a repository-ului

```
retele-proiect-20/
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

**Format:** `NUME_Prenume_GGGG_P20_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P20 | Numărul proiectului | P20 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P20_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P20_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P20_S07.zip` — Verificare săptămâna 7

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

Descriere: Proiectul își propune realizarea unei simulări de casă inteligentă (smart home) folosind dispozitive IoT (Internet of Things) și evaluarea aspectelor de securitate asociate. Studenții vor crea, în Cisco Packet Tracer (sau mediu similar), o mică rețea IoT ce include senzori și actuatori (de exemplu: un senzor de temperatură, un senzor de mișcare, o cameră IP, o lumină inteligentă sau o yală inteligentă), interconectate printr-un hub / gateway IoT către rețeaua locală și Internet. Dispozitivele IoT vor fi programate să comunice – de pildă, senzorul de mișcare detectează prezența și trimite un semnal care aprinde automat lumina. Simularea va evidenția protocoalele folosite de dispozitive (HTTP, MQTT etc.) și modul în care datele sunt transmise în rețea. A doua componentă majoră a proiectului este securitatea: se vor analiza riscurile de securitate într-o astfel de rețea (comunicații necriptate, dispozitive neautentificate, rețea Wi-Fi vulnerabilă) și se vor implementa măsuri de protecție de bază. De exemplu, se va activa criptarea WPA2 pe rețeaua Wi-Fi folosită de dispozitivele IoT, se va folosi un canal securizat (HTTPS/MQTTS) pentru comunicarea datelor senzorilor către serverul central, și se vor configura parole puternice pentru accesul la dispozitive. Proiectul combină astfel cunoștințele de rețelistică cu noțiuni moderne de IoT și securitate, oferind o perspectivă integratoare asupra aplicării rețelelor în mediul smart home.

### 🎯 Obiective de învățare


### 📖 Concepte cheie


### 🛠️ Tehnologii și unelte

Legătura cu săptămânile și kiturile: Proiectul sintetizează tema din săptămâna 13 (IoT și securitatea în rețele). În curs, la final, s-au discutat conceptele IoT și provocările de securitate, iar acest proiect le materializează într-un exemplu concret. La laboratorul final (săptămâna 13) probabil studenții au văzut demonstrații sau au lucrat cu dispozitive IoT în Packet Tracer, ori au analizat securitatea unor servicii IoT. Kitul de laborator aferent (ex. un fișier Packet Tracer cu câteva device-uri IoT configurate minimal) va servi ca punct de plecare, pe care studenții îl vor extinde adăugând propriile automatizări și configurări de securitate. Proiectul este un capstone ce reunește cunoștințe din multiple arii: rețele wireless (capitolul de legătură de date și Wi-Fi), protocoale de nivel aplicație (HTTP/REST – capitolele 10-12) și securitate (ultimul capitol), aplicându-le asupra IoT, un domeniu de actualitate. Astfel, studenții vor vedea aplicabilitatea concretă a conceptelor în implementarea unei case inteligente sigure.
Structura pe 4 etape: 1. Etapa 1: Proiectarea scenariului IoT și a rețelei. Se începe prin definirea cazului de utilizare: de exemplu, monitorizarea și controlul automat al unei case inteligente. Echipa decide ce dispozitive IoT să includă și ce reguli de automatizare vor implementa. Se desenează o schiță a rețelei: casa va avea un router/gateway care oferă conexiune la internet (simulat) și un Home Gateway IoT la care se conectează senzorii și actuatoarele (în Packet Tracer, Home Gateway-ul poate fi un device dedicat care comunică wireless cu device-urile IoT). Se va stabili modul de conectare: se prevede o rețea Wi-Fi la care se conectează camerele IP și alte device-uri, iar cele IoT pot folosi protocolul propriu (PT are concept de IoT Network over wireless). Totodată, se identifică potențiale riscuri de securitate din design și se notează unde se vor aplica măsuri (ex: conexiunea Wi-Fi – va fi securizată, accesul remote – va fi restricționat). La finalul acestei etape există un plan clar cu lista dispozitivelor (ex: 1 senzor de ușă, 1 senzor de mișcare, 1 cameră, 1 bec inteligent, 1 hub IoT, 1 router), protocoalele de comunicație pentru fiecare și obiectivele de securitate. 2. Etapa 2: Implementare în simulator a rețelei și funcționalității IoT. Echipa construiește topologia în Cisco Packet Tracer conform designului. Se configurează routerul principal al casei (adresare IP, DHCP pentru dispozitive, activare Wi-Fi AP). Se plasează Home Gateway-ul IoT și dispozitivele IoT (senzori, actuatori) și se conectează la rețea (în PT, de obicei senzorii se conectează wireless la Home Gateway pe o rețea IoT distinctă, iar Home Gateway se conectează la routerul principal). Se implementează logica IoT: de exemplu, în PT, pentru un senzor de mișcare și o lampă, se poate folosi Physical Workspace și Programming – se accesează interfața senzorului și se creează o asociere: “dacă MotionDetector detectează = true, atunci trimite mesaj de ON la SmartLamp”. Se configurează camera IP cu o adresă IP din LAN și se simulează streaming-ul (deși PT nu arată video, putem considera serviciul activ pe port). La această etapă, echipa se asigură că din punct de vedere funcțional sistemul merge: dacă se declanșează senzorul, lumina se aprinde (PT vizualizează asta), dacă se accesează interfata camerei (via IP) se primește un răspuns etc. Comunicarea către un server extern (dacă există de ex. un serviciu cloud) se poate simula prin trimiterea datelor senzorilor la un IoT Server (PT are un IoT cloud server configurabil) – de exemplu, Home Gateway transmite datele către un server central (acesta putând fi un PC server din internet). 3. Etapa 3: Implementarea și testarea măsurilor de securitate. Odată funcțional sistemul, se trece la securizarea lui. Se configurează rețeaua Wi-Fi a casei cu WPA2-PSK: se setează o parolă puternică și se reconectează device-urile Wi-Fi folosind această parolă (PT permite setarea securității pe modulul wireless). Se verifică că un dispozitiv neautorizat (adăugat de test în apropiere) nu se poate conecta fără cheie. Apoi, se asigură că comunicațiile IoT sensibile sunt criptate: de exemplu, dacă Home Gateway transmite datele senzorilor la un server extern, se optează pentru un protocol securizat – dacă inițial era HTTP, se schimbă la HTTPS (în simulare se poate presupune, chiar dacă PT nu simulează complet TLS, se poate folosi un server ce acceptă numai conexiuni pe portul SSL). Dacă se folosește MQTT, se poate menționa MQTT peste TLS (MQTTS) – PT însă nu detaliază asta, dar se poate explica teoretic în documentație. Totodată, se setează credențiale pe dispozitive: de exemplu, camera IP – se configurează un username/parolă pentru acces (dacă PT permite), Home Gateway – se schimbă parola implicită de admin. Echipa va simula și potențiale atacuri: de exemplu, va încerca o captură de pachete Wi-Fi (PT poate arăta că datele sunt criptate și deci neinteligibile) sau va încerca să se conecteze la Home Gateway fără autorizare (eșuând). Se vor documenta aceste teste ca dovadă că măsurile implementate au efect. Tot în această etapă, se pot configura reguli de bază de firewall pe routerul principal al casei (ex: blocarea accesului din internet către dispozitivele IoT, permițând doar conexiuni inițiate din LAN). 4. Etapa 4: Documentare și prezentarea concluziilor. În raportul final, se descrie arhitectura sistemului IoT realizat, cu diagrame care evidențiază conexiunile dintre componente. Se explică funcționalitatea (ce face fiecare senzor, ce acțiuni automatizate au loc) și se menționează protocoalele folosite. Apoi, un accent important al documentației este pe analiza de securitate: se enumeră vulnerabilitățile identificate inițial și se descrie pentru fiecare ce contramăsură s-a aplicat. De exemplu: “Traficul inițial al senzorului era necriptat HTTP, susceptibil la interceptare – am rezolvat folosind HTTPS pentru transmiterea datelor.”, “Rețeaua wireless era inițial deschisă – am activat WPA2 cu o parolă complexă.”, “Camera IP avea credențiale default – le-am schimbat și am restricționat accesul din exterior prin firewall.”. Se pot include capturi din simulare, cum ar fi configurațiile de securitate sau rezultate ale testelor (ex: un ping din afara rețelei către un dispozitiv IoT blocat de firewall). În concluzii, echipa va discuta importanța securității în IoT, evidențiind cât de ușor pot fi compromise astfel de sisteme dacă sunt lăsate nesecurizate și cum măsurile luate îmbunătățesc semnificativ postura de securitate. Totodată, se pot menționa soluții adiționale ce depășesc sfera proiectului (ex: rețele separate pentru IoT, monitorizarea traficului IoT pentru anomalii, actualizarea firmware-ului dispozitivelor periodic etc.), arătând o viziune completă asupra problemei.

### 📖 Concepte cheie


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

Riahi Sfar, A., Natalizio, E., Challal, Y., & Chtourou, Z. (2018). A roadmap for security challenges in the Internet of Things. Digital Communications and Networks, 4(2), 118–137. DOI: 10.1016/j.dcan.2017.04.003
Sebestyen, H., & Popescu, D. E. (2025). A Literature Review on Security in the Internet of Things: Identifying and Analysing Critical Categories. Computers, 14(2), 61. DOI: 10.3390/computers14020061
[1] TXT - » RFC Editor
https://www.rfc-editor.org/refs/ref3022.txt
[2] [3] [PDF] RFC 7857 - Updates to Network Address Translation †NAT ...
https://people.computing.clemson.edu/~jmarty/courses/commonCourseContent/Module5-NetworkConceptsAppliedToLinuxNetworkProgramming/AdditionalMaterial/rfc7857.pdf
[4] Foundations of Python network programming | WorldCat.org
https://search.worldcat.org/it/title/Foundations-of-Python-network-programming/oclc/894116307
[5] Staff View: Foundations of Python Network Programming
https://psnz.umt.edu.my/seal/Record/978-1-4302-5855-1/Details
[6] Machine Learning and Port Scans: A Systematic Review - arXiv
https://arxiv.org/abs/2301.13581
[7] A Survey on different Port Scanning Methods and the Tools used to ...
https://www.semanticscholar.org/paper/A-Survey-on-different-Port-Scanning-Methods-and-the-Upadhya/89b68de41599859989a7564091b6df7f8f03bd2e
---

## 🔮 Verificare înțelegere — IoT și MQTT

Înainte de testare:

1. **Cine primește mesajul publicat pe "casa/living/temp"?**
   - Toți clienții abonați la acest topic sau "casa/living/#"

2. **Ce se întâmplă dacă broker-ul MQTT nu rulează?**
   - Eroare: Connection refused

3. **Ce QoS folosim pentru date critice?**
   - QoS 2 (Exactly once)


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


### 💡 Pentru MQTT și IoT

MQTT e similar cu WebSockets pe care le-ai folosit poate în TW:

```python
# WebSocket (TW) vs MQTT (Rețele)

# WebSocket: conexiune bidirecțională client-server
# MQTT: publish/subscribe prin broker

import paho.mqtt.client as mqtt

# Similar cu socket.on('message', callback) din Socket.IO
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

# Similar cu socket.emit() dar prin broker
client.connect("localhost", 1883)
client.subscribe("casa/living/temp")  # Similar cu socket.join('room')
client.publish("casa/living/temp", "22.5")  # Similar cu io.to('room').emit()
```


### 💡 Pentru Securitate și Criptare

Din TW ai folosit HTTPS și poate crypto în Node.js:

```python
# Node.js crypto → Python cryptography

# Criptare simetrică (AES)
from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(b"mesaj secret")

# Hash (similar cu crypto.createHash în Node)
import hashlib
hash_obj = hashlib.sha256(b"password")
hash_hex = hash_obj.hexdigest()

# În Express aveai middleware pentru autentificare
# În Python implementezi manual sau folosești biblioteci
```

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `13roWSL/` — IoT și Securitate

**Ce găsești relevant:**
- Dispozitive IoT, securitate, autentificare

**Fișiere recomandate:**
- `13roWSL/README.md` — prezentare generală și pași de laborator
- `13roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `13roWSL/docs/fisa_comenzi.md` — comenzi utile
- `13roWSL/src/` — exemple de cod Python
- `13roWSL/homework/` — exerciții similare


### 📁 `03roWSL/` — Multicast

**Ce găsești relevant:**
- Comunicare între dispozitive

**Fișiere recomandate:**
- `03roWSL/README.md` — prezentare generală și pași de laborator
- `03roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `03roWSL/docs/fisa_comenzi.md` — comenzi utile
- `03roWSL/src/` — exemple de cod Python
- `03roWSL/homework/` — exerciții similare


### 📁 `10roWSL/` — REST

**Ce găsești relevant:**
- API-uri pentru control dispozitive

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
