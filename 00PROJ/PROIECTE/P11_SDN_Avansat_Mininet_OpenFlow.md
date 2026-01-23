# Proiectul 11: Rețea definită prin software (SDN) cu Mininet și OpenFlow

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
https://github.com/[username]/retele-proiect-11
```

#### Structura obligatorie a repository-ului

```
retele-proiect-11/
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

**Format:** `NUME_Prenume_GGGG_P11_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P11 | Numărul proiectului | P11 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P11_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P11_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P11_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect constă în proiectarea și implementarea unei rețele definite prin software (Software-Defined Network – SDN) folosind emulatorul Mininet și protocolul OpenFlow. SDN este un model modern de arhitectură de rețea care decuplează planul de control de planul de date, oferind flexibilitate sporită și posibilitatea de a programa comportamentul rețelei printr-un controller centralizat[1]. Studenții vor crea o topologie virtuală complexă în Mininet (de exemplu, cu mai multe switch-uri OpenFlow interconectate și zeci de host-uri), apoi vor dezvolta un controller SDN în Python care să gestioneze în mod dinamic traficul în rețea. Controller-ul poate fi realizat fie utilizând o platformă existentă (de tip POX, Ryu etc.), fie prin programarea directă a unor reguli OpenFlow prin API-ul oferit de Mininet. Scopul este implementarea unor funcționalități avansate precum rutarea adaptivă a pachetelor, echilibrarea traficului sau filtrarea și prioritizarea anumitor tipuri de trafic, demonstrând avantajele SDN față de rețelele tradiționale. Proiectul are o componentă tehnică puternică (setarea unui mediu de simulare, programarea controller-ului, analiza traficului) și o componentă pedagogică, întrucât îi provoacă pe studenți să gândească rețeaua în termeni algoritmici și să aplice cunoștințele teoretice despre protocoale la un sistem real emulator. Prin experimentare, echipa va evidenția modul în care controller-ul central reacționează la evenimente din rețea (de ex. căderea unui nod, aglomerarea unei legături) prin instalarea de noi reguli de forwardare în switch-uri. Rezultatul final va fi o rețea virtuală controlată programatic, în care se poate vizualiza în timp real modul de funcționare al algoritmilor de control de nivel rețea.

### 🎯 Obiective de învățare

- Să evalueze avantajele și dezavantajele soluției implementate comparativ cu alternative.
• Să compare performanța proiectului cu soluții similare sau benchmark-uri de referință.

### 📖 Concepte cheie

Tehnologii implicate: Python (pentru programarea logicii controller-ului SDN), Mininet (emulare rețea virtuală), protocolul OpenFlow 1.3+, controller OpenFlow (POX/RYU sau implementare custom), utilitare de monitorizare a traficului (Wireshark, tcpdump) pentru inspectarea pachetelor, eventual Open vSwitch (integrat în Mininet) ca elemente de comutare. Se vor folosi biblioteci specifice Python pentru rețele (exemplu: biblioteca Mininet sau interfete REST API dacă se folosește un controller extern).
Legătura cu săptămânile și kiturile (WEEK1-14): Proiectul valorifică cunoștințele acumulate în săptămânile dedicate rutării și administrării rețelelor. În mod particular, temele din săptămâna 5 (adresare IP, rutare statică și dinamică) și săptămâna 6 (introducere în SDN și virtualizare de rețea) stau la baza cerințelor proiectului. Kitul de laborator al săptămânii 6, care include experimente de bază cu Mininet și OpenFlow, va oferi un punct de pornire practic. Totodată, conceptual, proiectul se leagă de discuțiile despre algoritmi de rutare (săpt. 5-6) și de instrumentele de monitorizare a traficului prezentate în săptămâna 7 (captură de pachete și filtrare), utile pentru testarea soluției SDN.
Structura proiectului în 4 etape: - Etapa 1 (săptămâna 5): Definirea cerințelor și a design-ului arhitectural al rețelei SDN. Echipa va realiza un plan al topologiei (număr de noduri, conexiuni, rolul fiecărui element) și va stabili obiectivele precise (ex: implementarea unui algoritm de rutare adaptivă). În această etapă se vor instala și configura instrumentele de lucru (Mininet, mediul Python, eventuale pachete pentru controller) și se va efectua un experiment inițial simplu în Mininet pentru a verifica funcționarea de bază (ex. ping între host-uri printr-un switch OpenFlow controlat de un controller default). - Etapa 2 (săptămâna 9): Implementarea inițială a controller-ului SDN și realizarea unei rețele funcționale simple. Până la acest punct, studenții vor fi dezvoltat logica de bază a controller-ului (de exemplu, un modul care acționează ca un learning switch sau realizează o rutare statică prestabilită). Topologia creată în Mininet va fi populată cu câteva host-uri de test, iar controller-ul va instala reguli OpenFlow elementare (de tipul forwardare pe bază de MAC sau IP). Se vor testa funcțiile elementare: conectivitatea capăt-la-capăt (folosind ping, iperf), capacitatea controller-ului de a procesa evenimente (ex: pachete PacketIn OpenFlow) și de a insera intrări în tablorile de flux ale switch-urilor. - Etapa 3 (săptămâna 13): Extinderea și finalizarea proiectului SDN cu funcționalități avansate. În această etapă, se implementează toate cerințele complexe asumate: de exemplu, algoritmul adaptiv de rutare care detectează congestia și redirecționează traficul pe rute alternative, sau un modul de securitate care blochează trafic suspect. Se vor realiza teste extensive în scenarii variate: căderea unui nod de rețea (pentru a observa reacția controller-ului), simularea unui volum mare de trafic (pentru a evalua performanța și latența deciziilor controller-ului) etc. Studenții vor aduna metrici (timp de convergență, throughput, rate de pierdere pachete) și le vor analiza critic, pregătind astfel material pentru concluzii. - Etapa 4 (prezentarea în săptămâna 14): Echipa va prezenta proiectul în cadrul seminarului final, demonstrând practic funcționarea rețelei SDN create. Prezentarea va include o descriere arhitecturală (topologia și modul de interacțiune între controller și elementele de rețea), o demonstrație live (de exemplu, rularea Mininet cu controller-ul activ și arătarea modului în care pachetele sunt redirecționate conform regulilor programate) și o discuție asupra rezultatelor obținute. Vor fi evidențiate beneficiile abordării SDN – cum ar fi flexibilitatea reconfigurării rețelei în timp real – și provocările întâmpinate (de pildă, complexitatea depanării sau limitările de performanță).

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


### 📊 PEER INSTRUCTION - SDN ȘI OPENFLOW

Discutați cu colegii și alegeți împreună răspunsul corect:

Întrebarea 1: După ce controller-ul instalează o regulă OpenFlow cu actions=drop, ce se întâmplă cu pachetele care fac match?

A) Sunt trimise înapoi la sursă cu ICMP Destination Unreachable
B) Sunt șterse silențios fără nicio notificare ✓
C) Sunt redirecționate către controller pentru logging
D) Sunt puse în coadă până expiră timeout-ul flow-ului

Explicație: Acțiunea drop elimină pachetul complet. Pentru ICMP unreachable ar fi nevoie de o regulă explicită care să trimită acest mesaj.

Întrebarea 2: Ce tip de mesaj OpenFlow trimite switch-ul către controller când primește un pachet pentru care nu există regulă?

A) FlowMod (modificare flux)
B) PacketIn (pachet primit) ✓
C) PacketOut (trimite pachet)
D) PortStatus (stare port)

Explicație: PacketIn = switch întreabă controller-ul ce să facă. FlowMod = controller instalează regulă în switch.


### Extensii pentru echipe de 3 vs. 2/1 membri: Pentru echipele formate din 3 studenți, se așteaptă un nivel suplimentar de complexitate. De exemplu, echipa poate implementa o rețea multi-domeniu cu două controllere SDN ierarhizate (un controller local și un controller global de coordonare) sau poate adăuga funcții extra precum mecanisme de securitate (firewall SDN integrat) ori algoritmi de load balancing pentru distribuirea traficului între mai multe servere. Totodată, pot fi incluse scripturi de automatizare (ex: un dashboard web simplu pentru vizualizarea topologiei și a fluxurilor în timp real). Pentru echipele de 2 studenți sau individuale, complexitatea poate fi ajustată: este suficientă o singură rețea SDN cu un controller centralizat și un set de funcții de bază (de ex. rutare statică cu posibilitate de actualizare manuală, sau un singur tip de eveniment gestionat – cum ar fi eșecul unui link). Numărul de noduri din topologie poate fi mai redus, iar focusul poate fi pus pe înțelegerea corectă a mecanismelor OpenFlow și mai puțin pe optimizarea perfectă a performanțelor. Astfel, criteriile de evaluare vor ține cont de dimensiunea echipei, punând accent pe originalitatea soluției și corectitudinea funcțională mai degrabă decât pe anvergura implementării în cazul echipelor mai mici.


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


### ❓ ÎNTREBĂRI FRECVENTE - SDN/MININET

Q: Mininet nu pornește și afișează "Error creating interface"
A: Rulați cu sudo și curățați sesiunile anterioare:
   sudo mn -c
   sudo mn --topo single,3 --controller remote

Q: Controller-ul nu primește mesaje PacketIn
A: Verificați că switch-ul e conectat la controller:
   - dpctl show
   - Asigurați-vă că IP-ul controller-ului e corect în topologie

Q: Cum testez că firewall-ul funcționează corect?
A: Folosiți comenzi de test în Mininet CLI:
   - h1 ping h2 (pentru trafic care ar trebui blocat)
   - h1 curl h2:80 (pentru trafic care ar trebui permis)
   - Verificați log-urile controller-ului pentru decizii


### 📚 Bibliografie

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

## ❓ Întrebări frecvente — SDN/Mininet

**Q: Mininet nu pornește - eroare "cannot create interface"**  
A: Rulează cu sudo și curăță sesiunile anterioare:
```bash
sudo mn -c
sudo mn --topo single,3 --controller remote
```

**Q: Controller-ul nu primește PacketIn**  
A: Verifică conexiunea switch-controller cu `dpctl show`

**Q: Cum testez că firewall-ul funcționează?**  
A: Folosește `h1 ping h2` pentru trafic blocat și `h1 curl h2:80` pentru trafic permis


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

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `06roWSL/` — SDN

**Ce găsești relevant:**
- OpenFlow avansate, QoS, traffic engineering

**Fișiere recomandate:**
- `06roWSL/README.md` — prezentare generală și pași de laborator
- `06roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `06roWSL/docs/fisa_comenzi.md` — comenzi utile
- `06roWSL/src/` — exemple de cod Python
- `06roWSL/homework/` — exerciții similare


### 📁 `07roWSL/` — Filtrare Pachete

**Ce găsești relevant:**
- Deep packet inspection, metrici

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `05roWSL/` — Adresare IP

**Ce găsești relevant:**
- Routing decisions bazate pe IP

**Fișiere recomandate:**
- `05roWSL/README.md` — prezentare generală și pași de laborator
- `05roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `05roWSL/docs/fisa_comenzi.md` — comenzi utile
- `05roWSL/src/` — exemple de cod Python
- `05roWSL/homework/` — exerciții similare


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
