# Proiectul 01: Firewall SDN în Mininet

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
https://github.com/[username]/retele-proiect-01
```

#### Structura obligatorie a repository-ului

```
retele-proiect-01/
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

**Format:** `NUME_Prenume_GGGG_P01_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P01 | Numărul proiectului | P01 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P01_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P01_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P01_S07.zip` — Verificare săptămâna 7

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
Acest proiect urmărește realizarea unui firewall de rețea folosind paradigma Software-Defined Networking (SDN). În locul unui firewall tradițional bazat pe dispozitive hardware dedicate, se va implementa o aplicație de firewall la nivel de controler SDN, care să filtreze traficul între nodurile unei rețele virtuale. Platforma de emulare Mininet va fi utilizată pentru a crea o topologie virtuală de rețea (calculatoare și switch-uri OpenFlow), controlată de un controler SDN (precum POX sau Ryu) programat în Python. Firewall-ul SDN va inspecta pachetele (de exemplu, pe baza adreselor IP, porturilor TCP/UDP sau tipului de protocol) și va aplica reguli de filtrare (permitere/blocare) în mod dinamic, prin instalarea de fluxuri OpenFlow în switch-urile rețelei.
Proiectul presupune parcurgerea etapelor de design al politicilor de securitate (de ex. ce tipuri de trafic sunt permise sau blocate), configurarea topologiei de rețea în Mininet și dezvoltarea logicii firewall-ului în controlerul SDN. Se va testa funcționalitatea firewall-ului trimițând trafic de test între host-urile din Mininet (de ex. ping, HTTP, etc.) și verificând că pachetele interzise sunt filtrate corect. Acest demers oferă o perspectivă practică asupra modului în care rețelele pot fi programate și securizate dinamic folosind SDN, separând planul de control de dispozitivele de date[1][2]. Rezultatul final va fi o aplicație firewall configurabilă, rulând într-o rețea virtuală, împreună cu un raport ce descrie arhitectura soluției și teste de verificare.

### 🎯 Obiective de învățare


### 🛠️ Tehnologii și unelte

Însușirea conceptelor de firewall și liste de control al accesului (ACL) într-un mediu de rețea programabilă.
Dezvoltarea abilităților practice de a utiliza Mininet pentru emularea rețelelor și de a programa un controler SDN simplu în Python.
Înțelegerea modului de monitorizare și filtrare a pachetelor la nivel de rețea, precum și evaluarea impactului regulilor de securitate asupra traficului.
Dezvoltarea abilităților critice privind securitatea rețelelor și modul în care arhitectura SDN poate simplifica implementarea politicilor de securitate.

### 📖 Concepte cheie

Software-Defined Networking (SDN) – separarea planului de control de cel de date, controler centralizat, protocolul OpenFlow[2].
Firewall de rețea – filtrarea pachetelor pe baza regulilor (adrese IP sursă/destinație, porturi, protocol).
Protocoale de nivel rețea și transport – IPv4/IPv6, TCP/UDP (utilizate pentru a identifica fluxurile de trafic ce vor fi filtrate).
Comutare și rutare OpenFlow – fluxuri în switch-urile virtuale care implementează regulile de firewall prin acțiuni de drop sau forward.
Securitatea rețelelor – noțiuni de acces permis/interzis, protecția segmentelor de rețea, politici de securitate distribuite.
Tehnologii implicate
Mininet – emulare de topologii de rețea virtuale (switch-uri OpenFlow și host-uri Linux).
Python – limbajul folosit pentru a programa logica firewall în controlerul SDN (ex. folosind POX, Ryu sau alt framework SDN).
Protocolul OpenFlow – pentru definirea regulilor în switch (prin intermediul controlerului).
Wireshark (opțional) – pentru captură și inspecție de pachete, în vederea verificării comportamentului firewall-ului.
Sisteme Linux – configurarea mediului de dezvoltare (Mininet rulează pe Linux) și utilizarea utilitarelor de rețea (ping, iperf) pentru testare.
Legătura cu temele din săptămânile cursului
Săptămâna 9: Securitatea rețelelor – proiectul aplică concepte de firewall și control al accesului (vezi materialul „Firewall și liste de acces” din arhiva WEEK9).
Săptămâna 10: Rețele definite prin software (SDN) – se folosiază arhitectura SDN și OpenFlow conform laboratorului din Week10 („Mininet – OpenFlow Basic”).
Săptămâna 12: Programare de rețea în Python – dezvoltarea controlerului OpenFlow în Python valorifică cunoștințele de socket programming și biblioteci SDN prezentate în cursul din Week12.
Etapele proiectului

### 📋 Etapa 1 (Săptămâna 5) – Analiză și design: Documentarea conceptelor SDN și OpenFlow; definirea politicii de securitate (ce tipuri de trafic vor fi blocate/permisive). Se va realiza o schiță a topologiei Mininet (ex: 2 switch-uri și 4 host-uri, cu firewall aplicat între segmente) și se va alege platforma de controler (ex. POX). Livrabil: raport scurt cu specificațiile firewall-ului (listă de reguli intenționate), diagrama topologiei de rețea propuse și un plan de implementare. Se va iniția și un repository (ex. pe GitHub) cu structura de fișiere a proiectului (de exemplu, un fișier README și un fișier-schelet pentru controlerul SDN).


### 🔨 Etapa 2 (Săptămâna 9) – Prototip funcțional: Implementarea parțială a firewall-ului SDN. Se va construi topologia în Mininet și se va dezvolta codul Python al controlerului pentru a impune cel puțin o regulă de filtrare (ex: blocarea ping-urilor sau a traficului HTTP). Se testează prototipul prin trimiterea traficului de test și se colectează rezultate (capturi Wireshark sau log-uri din controler). Livrabil: codul sursă al controlerului (actualizat în repository, bine structurat și comentat), un fișier de configurare/topologie pentru Mininet (dacă e cazul) și un scurt raport de testare care demonstrează o regulă de firewall în acțiune.


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


### ✅ Etapa 3 (Săptămâna 13) – Versiunea finală și teste extensive: Extinderea implementării pentru a acoperi întregul set de reguli de firewall planificate (de ex. filtrare pe multiple porturi/protocoale, eventual logging al pachetelor blocate). Se realizează teste extensive în diferite scenarii (trafic permis vs. blocat, simularea unui atac scanare porturi, etc.) și se optimizează performanța sau claritatea codului. Livrabil: proiectul final – codul complet (în repository, însoțit de instrucțiuni de rulare și eventual scripturi pentru reproducerea mediului), fișiere de configurare, plus un raport final care include arhitectura soluției, capturi de ecran/log-uri din teste și discuții asupra funcționalității și limitărilor.


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


### 📊 CERINȚĂ SUPLIMENTARĂ: ANALIZĂ COMPARATIVĂ

În raportul final, includeți o secțiune de 1-2 pagini cu:
1. Comparație cu cel puțin 2 alternative tehnologice
2. Metrici de performanță măsurate (latență, throughput)
3. Limitări și posibile îmbunătățiri ale soluției


### 🎤 Etapa 4 (Săptămâna 14) – Prezentare finală: Echipa va susține o prezentare de ~15 minute în care descrie pe scurt conceptul de firewall SDN, modul de implementare și va demonstra live funcționarea pe un caz de test (de ex. două terminale – unul care încearcă să comunice și este blocat conform regulilor). Livrabil: diapozitivele prezentării și eventual un scurt videoclip demonstrativ (opțional, dacă se dorește evidențierea scenariilor de test).

Extensii posibile pentru echipe de 3 vs. 2/1 studenți
Pentru o echipă de 3 studenți, se poate extinde proiectul implementând funcționalități avansate de firewall, cum ar fi filtrare dinamică (ex: încărcarea regulilor dintr-un fișier de configurare în timp real) sau un firewall stateful simplificat (menținerea unei tabele de sesiuni active, permițând automat traficul de răspuns la conexiuni inițiate). Totodată, s-ar putea integra o mică interfață (ex. linie de comandă sau GUI elementar) pentru a adăuga/șterge reguli de filtrare la rulare.
Pentru o echipă mai restrânsă (2 sau 1 student), focusul poate rămâne pe un firewall stateless de bază cu un set fix de reguli implementate direct în cod. Complexitatea poate fi redusă la filtrarea după criterii esențiale (ex: blocarea totului în afară de trafic pe portul X între două host-uri specifice). Chiar și în formă mai simplă, proiectul va atinge obiectivele educaționale, dar cu un volum de lucru mai adecvat resurselor echipei.

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

Kreutz, D., Ramos, F. M. V., Veríssimo, P. E., Rothenberg, C. E., Azodolmolky, S., & Uhlig, S. (2015). Software-Defined Networking: A complet Survey. IEEE Communications Surveys & Tutorials, 17(1), 27-51. https://doi.org/10.1109/COMST.2014.2326417
Lantz, B., Heller, B., & McKeown, N. (2010). A network in a laptop: rapid prototyping for software-defined networks. Proceedings of the 9th ACM SIGCOMM Workshop on Hot Topics in Networks (HotNets-IX), 19. https://doi.org/10.1145/1868447.1868466
Hu, H., Han, W., Ahn, G.-J., & Zhao, Z. (2014). FlowGuard: Building solid firewalls for software-defined networks. In Proceedings of the ACM SIGCOMM Workshop on Hot Topics in SDN (HotSDN ’14) (pp. 97-102). ACM. https://doi.org/10.1145/2620728.2620749
Göransson, P., Black, C., & Culver, T. (2014). Software Defined Networks: A complet Approach. Morgan Kaufmann Publishers.
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


### 📁 `06roWSL/` — NAT/PAT, Protocoale de Suport și Rețele Definite prin Software

**Ce găsești relevant:**
- Conceptele SDN și OpenFlow, controlere, flow tables

**Fișiere recomandate:**
- `06roWSL/README.md` — prezentare generală și pași de laborator
- `06roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `06roWSL/docs/fisa_comenzi.md` — comenzi utile
- `06roWSL/src/` — exemple de cod Python
- `06roWSL/homework/` — exerciții similare


### 📁 `07roWSL/` — Interceptarea și Filtrarea Pachetelor

**Ce găsești relevant:**
- Wireshark, filtre de captură, analiza traficului

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `02roWSL/` — Modele Arhitecturale și Programare Socket

**Ce găsești relevant:**
- Fundamentele socket-urilor pentru comunicarea controller-switch

**Fișiere recomandate:**
- `02roWSL/README.md` — prezentare generală și pași de laborator
- `02roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `02roWSL/docs/fisa_comenzi.md` — comenzi utile
- `02roWSL/src/` — exemple de cod Python
- `02roWSL/homework/` — exerciții similare


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
