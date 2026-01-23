# Proiectul 06: Rețea definită prin software (SDN) cu Mininet și controler OpenFlow

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
https://github.com/[username]/retele-proiect-06
```

#### Structura obligatorie a repository-ului

```
retele-proiect-06/
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

**Format:** `NUME_Prenume_GGGG_P06_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P06 | Numărul proiectului | P06 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P06_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P06_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P06_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect abordează conceptul de Software-Defined Networking (SDN) prin dezvoltarea unei rețele simulate în Mininet controlată de un controller OpenFlow implementat de studenți. În esență, studenții vor crea o topologie de rețea virtuală (ex. mai multe noduri și switch-uri virtuale) folosind Mininet și vor programa un controller SDN în Python care gestionează dinamic fluxurile de pachete în rețea. Proiectul pune accent atât pe aspectele tehnice – cum ar fi configurarea și administrarea unei rețele SDN, scrierea de reguli OpenFlow pentru routare, comutare sau filtrare – cât și pe cele educaționale, oferind o înțelegere aprofundată a separării planului de control de planul de date. Studenții vor experimenta modul în care un controller centralizat poate dicta comportamentul întregii rețele (de exemplu, cum sunt direcționate pachetele între host-uri) și vor analiza avantajele SDN față de rețelele tradiționale (flexibilitate, programabilitate, administrare simplificată). Proiectul include teste comparative – cum se comportă rețeaua în diferite scenarii de trafic sau la căderea unui nod – evidențiind modul în care SDN poate reacționa rapid prin reproiectarea rutelor. Totodată, se pune accent pe deprinderea utilizării unor unelte de analiză (ex. Wireshark) pentru a monitoriza traficul în rețeaua Mininet și pe dezvoltarea abilităților de depanare a unei aplicații de rețea complexe. Per ansamblu, proiectul oferă o incursiune practică în arhitectura modernă a rețelelor programabile, consolidând atât cunoștințele teoretice despre protocoalele de control al rețelei, cât și competențele practice de configurare și scripting în medii de simulare de rețea.

### 🎯 Obiective de învățare

- Să evalueze avantajele și dezavantajele soluției implementate comparativ cu alternative.
• Să compare performanța proiectului cu soluții similare sau benchmark-uri.

### 📖 Concepte cheie

Tehnologii implicate: Python (pentru implementarea logicii controller-ului SDN – ex. folosind POX sau Ryu), Mininet (emulator de rețea pentru crearea topologiei virtuale), protocoale OpenFlow (versiunea 1.3+ pentru comunicarea controller-switch), Wireshark/tcpdump (analiza traficului și debug), eventual biblioteci specifice SDN (ex. OpenFlow Python bindings). Totodată, se pot folosi containere Docker pentru a emula host-uri din topologia Mininet (opțional, pentru teste extinse), și Git pentru versionarea codului sursă.
Legătura cu temele și kiturile săptămânilor 1–13: Proiectul valorifică major conținutul săptămânilor 5 și 6 din curs. În săptămâna 5 studenții au învățat despre adresare IP, rutare și au fost introduși în simulatoare de rețea – cunoștințe esențiale pentru a construi topologia virtuală inițială în Mininet (adresarea corectă a host-urilor, setarea legăturilor și înțelegerea rutelor). Săptămâna 6 a adus introducerea conceptului de Software-Defined Networking și a componentelor arhitecturale SDN, precum și familiarizarea cu Mininet și elementele unui switch virtual OpenFlow – acestea reprezintă baza teoretică și practică a proiectului. Proiectul atinge aspecte din săptămâna 7 (interceptarea și filtrarea pachetelor) prin faptul că un controller SDN poate implementa funcționalități de firewall la nivel de rețea prin reguli OpenFlow: studenții pot aplica în controller concepte de filtrare învățate atunci. În săptămâna 8 s-au discutat servicii Internet și proxy-uri, iar studenții pot folosi un mic server HTTP de test în rețeaua Mininet pentru a valida rutarea end-to-end prin rețeaua definită software. Săptămâna 13 (Securitatea în rețele) este și ea relevantă – ca extensie, studenții pot implementa în controller mecanisme de detectare a traficului suspect (de ex. detectarea unui port scan sau limitarea numărului de conexiuni concomitente), aplicând practic noțiuni de securitate. Așadar, proiectul consolidează cunoștințele acumulate pe parcursul disciplinei (adresare, rutare, SDN, filtrare, securitate), oferind totodată un cadru integrator în care acestea sunt puse în practică într-un mod progresiv.
Structură în 4 etape:

### 🔮 VERIFICARE ÎNȚELEGERE

Înainte de a rula comenzile, răspundeți:

1. Câte containere vor fi create conform docker-compose.yml?
   → Numărați serviciile definite în fișier.

2. Ce se întâmplă dacă portul dorit este deja ocupat?
   → Eroare: "port is already allocated". Verificați cu: ss -tlnp | grep :PORT

3. Cum comunică containerele între ele în aceeași rețea Docker?
   → Prin numele serviciului (DNS intern Docker), nu prin localhost.


📊 PEER INSTRUCTION

Discutați cu colegii și alegeți răspunsul corect:

Întrebarea: Containerele web și db sunt în aceeași rețea Docker. Cum se conectează web la db?

A) localhost:5432 
B) db:5432 ✓
C) 172.17.0.1:5432
D) host.docker.internal:5432

Explicație: Docker DNS rezolvă automat numele serviciilor din Compose.

Extensii pentru echipe de 3 vs. echipe de 2/1: Proiectul este dimensionat astfel încât o echipă de 2 studenți sau chiar un singur student să poată implementa cerințele de bază (topologie simplă, controller care realizează forwardare fundamentală pe bază de adrese MAC/IP, eventual o funcție suplimentară). Totuși, pentru echipele de 3 se așteaptă o complexitate sporită și componente adiționale. De exemplu, o echipă de 3 poate configura o topologie SDN mai amplă (cu 3-4 switch-uri interconectate ierarhic, simulând o rețea de campus) și poate implementa un set mai bogat de politici în controller: rutare pe multiple căi cu echilibrarea traficului între ele, mecanisme de securitate (firewalling, filtrare pe criterii variate – adresă IP, port TCP/UDP, tip de trafic), precum și un modul de monitorizare a traficului în timp real (de exemplu, afișarea într-o consolă a numărului de pachete procesate de fiecare switch). Totodată, echipele mai mari ar putea integra și o interfață minimală (CLI sau web simplu) pentru controller, care să permită vizualizarea și modificarea unor reguli de rutare dinamic. În contrast, o echipă mai restrânsă (2 sau 1 student) poate limita scenariul la un singur switch central și câțiva host-uri și la funcționalitățile esențiale (ex. forwardare tip learning switch și un singur exemplu de filtrare). Important este ca toți studenții, indiferent de mărimea echipei, să demonstreze înțelegerea principiilor SDN și să livreze o rețea funcțională; complexitatea și numărul de extensii vor diferenția însă proiectele excepționale realizate de echipe mai numeroase.

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

Kreutz, D., Ramos, F. M. V., Veríssimo, P. E., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-Defined Networking: A complet Survey. Proceedings of the IEEE, 103(1), 14-76. https://doi.org/10.1109/JPROC.2014.2371999
Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: rapid prototyping for software-defined networks. În Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks (HotNets IX). ACM. https://doi.org/10.1145/1868447.1868466
McKeown, N., Anderson, T., Balakrishnan, H., Parulkar, G., Peterson, L., Rexford, J., … & Turner, J. (2008). OpenFlow: enabling innovation in campus networks. ACM SIGCOMM Computer Communication Review, 38(2), 69-74. https://doi.org/10.1145/1355734.1355746
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


### 📁 `06roWSL/` — NAT/PAT și SDN

**Ce găsești relevant:**
- OpenFlow, POX/Ryu controller, flow rules

**Fișiere recomandate:**
- `06roWSL/README.md` — prezentare generală și pași de laborator
- `06roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `06roWSL/docs/fisa_comenzi.md` — comenzi utile
- `06roWSL/src/` — exemple de cod Python
- `06roWSL/homework/` — exerciții similare


### 📁 `07roWSL/` — Interceptarea Pachetelor

**Ce găsești relevant:**
- Analiza traficului pentru decizii de rutare

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


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
