# Proiectul 19: Instrument de scanare a porturilor pentru analiza securității rețelei

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
https://github.com/[username]/retele-proiect-19
```

#### Structura obligatorie a repository-ului

```
retele-proiect-19/
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

**Format:** `NUME_Prenume_GGGG_P19_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P19 | Numărul proiectului | P19 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P19_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P19_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P19_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect are ca temă dezvoltarea unui utilitar simplu de scanare a porturilor și utilizarea sa pentru a evalua configurația de securitate a unui sistem din rețea. Scopul este de a înțelege cum funcționează scanarea porturilor – o tehnică folosită atât de administratorii de rețea (pentru inventarierea serviciilor deschise), cât și de potențiali atacatori (pentru identificarea punctelor vulnerabile)[6][7]. Studenții vor implementa o aplicație care, dat fiind un nume de host sau o adresă IP, încearcă conexiuni către o serie de porturi (ex. 1-1024 sau un subset relevant) și raportează care porturi sunt deschise, închise sau filtrate. Scanarea se va realiza inițial la nivel de TCP connect() – adică prin încercarea de a stabili o conexiune TCP pe fiecare port și observarea rezultatului – metodă simplă ce indică porturile deschise dacă conexiunea reușește. După implementare, utilitarul va fi folosit pentru a scana un sistem de test, iar rezultatele vor fi analizate: ce servicii rulează pe porturile deschise, ce implicații de securitate există și ce măsuri ar trebui luate (de exemplu, închiderea porturilor neutilizate sau protejarea serviciilor expuse). Proiectul oferă astfel o perspectivă practică asupra securității rețelei la nivel de host și a modalităților de identificare a vulnerabilităților simple.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Limbaj de programare cu acces la socket-uri raw sau TCP – Python recomandat (simplifică paralelizarea și tratarea excepțiilor), posibile biblioteci precum socket, threading/asyncio. Eventual utilizarea modulului scapy (avansat, pentru SYN scan, dar opțional). Sistem de operare: preferabil Linux pentru teste mai facile de rețea, dar și Windows e posibil. Utilitare de monitorizare (pentru a vedea dacă porturile sunt deschise – de ex. netstat) și eventual un instrument third-party (nmap) pentru a compara rezultatele scanner-ului realizat cu cele ale unui instrument consacrat. Totodată, cunoștințe despre servicii comune (pentru interpretarea rezultatului scanării). Proiectul nu necesită hardware special, doar acces la o mașină de test (poate fi chiar localhost-ul).
Legătura cu săptămânile și kiturile: Proiectul se conectează cu săptămâna 13, unde au fost studiate noțiuni de securitate în rețele și instrumente precum scanarea de porturi și testarea vulnerabilităților. În laboratorul 7 (Interceptarea pachetelor și scanarea porturilor) studenții au experimentat probabil folosirea unor unelte ca nmap sau implementarea unui mic filtru de pachete. Kitul de laborator aferent (ex. script de scanare parțial implementat sau exemple de rezultate nmap) va servi ca punct de plecare. Proiectul extinde aceste cunoștințe, solicitând studenților să își dezvolte propriul program de scanare, consolidând totodată cunoștințele de socket programming (săptămânile 2-3) și de protocoale de transport (săptămâna 8). Astfel, este un exemplu integrator: folosește programare de rețea pentru un scop de securitate, reunind elemente de curs din capitole diferite.
Structura pe 4 etape: 1. Etapa 1: Definirea specificațiilor și mediului de lucru. În prima etapă, se stabilește ce tip de scanare se va implementa și care este ținta de test. De exemplu, echipa decide să implementeze un TCP connect scan pe un interval de porturi 1-1024 al unui server de test (care poate fi o mașină locală sau o adresă IP din rețeaua proprie, cu permisiune). Se pregătește mediul de lucru: se identifică o mașină țintă cu câteva porturi cunoscute deschise (ex. se poate activa pe mașina țintă un server web pe port 80, un SSH pe 22, etc., pentru a avea rezultate de scanare variate). Totodată, se conturează algoritmul: iterarea peste porturi și pentru fiecare port, încercarea de conectare TCP cu un anumit timeout. Se selectează limbajul de implementare și se configurează proiectul. 2. Etapa 2: Implementarea scanner-ului de porturi. Echipa dezvoltă programul conform planului. Se implementează citirea parametrilor (de exemplu IP țintă și range de porturi de scanat). Pentru fiecare port din interval, se creează un socket TCP neconectat și se apelează metoda de conectare (connect) către IP-ul țintă la acel port, cu un timeout scurt (ex. 1-2 secunde). Dacă conexiunea este stabilită cu succes, rezultatul se notează ca “port deschis”, apoi se închide imediat conexiunea. Dacă se primește refuz de conexiune (error de tip connection refused), se notează “port închis”. Dacă apelul expiră (timeout) fără răspuns, este posibil un “port filtrat” (nesigur, dar se va interpreta ca posibil filtrat de firewall). Pentru eficiență, se poate implementa această scanare în paralel: de exemplu, folosind thread-uri sau task-uri asincrone pentru a scana mai multe porturi simultan, ținând cont însă de limitările resurselor. Rezultatele fiecărui test sunt stocate (de exemplu într-o structură de date) pentru a fi raportate ulterior. Codul trebuie să fie solid, gestionând excepțiile posibile (erori de rețea, cazuri în care ținta nu este disponibilă deloc etc.). 3. Etapa 3: Testarea aplicației și colectarea rezultatelor. Odată implementat scanner-ul, se trece la testarea sa pe ținta aleasă. Se rulează scanarea și se observă output-ul generat – care porturi au fost raportate deschise. Echipa validează aceste rezultate comparând cu realitatea: de exemplu, dacă știu că pe mașina țintă rulează un serviciu pe portul X, acesta ar trebui să apară ca deschis; dacă portul Y a fost blocat de firewall, scanner-ul lor ar trebui să arate timeout. Opțional, se poate rula în paralel un instrument consacrat (cum ar fi nmap -sT) pe același target și port range, pentru a verifica dacă rezultatele propriului utilitar sunt corecte sau dacă au ratat ceva. Se fac ajustări dacă e nevoie (de exemplu, mărirea timeout-ului dacă rețeaua e mai lentă, sau corectarea interpretării unor erori). În final, se obține o listă de porturi deschise pe sistemul de test. 4. Etapa 4: Analiza de securitate și documentarea. Ultima etapă este dedicată interpretării rezultatelor scanării și scrierii raportului. Echipa va identifica, pentru fiecare port deschis găsit, ce serviciu probabil rulează acolo (prin convențiile cunoscute – de exemplu 80 http, 22 ssh, 3389 RDP etc., sau eventual folosind mici pachete de banner grabbing: trimiterea unei cereri simple și citirea răspunsului, dacă doresc). Se va discuta implicarea fiecărui serviciu în securitatea sistemului: de exemplu, “am găsit portul 21 deschis, ceea ce sugerează un server FTP – se știe că FTP transmite datele necriptat și ar putea reprezenta un risc de securitate dacă nu e configurat adecvat”. Se vor recomanda măsuri de remediere pentru a securiza sistemul: închiderea porturilor ne-necesare, aplicarea de politici firewall, actualizarea serviciilor, utilizarea de versiuni securizate (ex. SFTP în loc de FTP). Raportul va descrie și cum funcționează scanner-ul implementat, ce limitări are (spre exemplu, faptul că detectarea unui port filtrat nu e 100% sigură, sau că scanarea TCP connect este mai lentă și mai zgomotoasă față de un SYN scan). Vor fi incluse fragmente de cod relevante (pseudo-cod) și eventual capturi cu execuții. Echipa va reflecta asupra modului în care acest proiect i-a ajutat să înțeleagă mai bine atât programarea de rețea, cât și perspectiva unui administrator de securitate ce examinează suprafața de atac a propriului sistem.
Extensii pentru echipe de 3/2/1: - Echipe de 3 persoane: Se pot aventura în implementarea unor caracteristici avansate care să îmbunătățească scanner-ul sau analiza de securitate. De exemplu, implementarea unui mod de scanare UDP pentru câteva porturi importante (deși mai dificil de interpretat deoarece UDP nu răspunde cu ACK la succes) sau implementarea unui SYN scan (trimițând manual pachete TCP SYN folosind o bibliotecă ca Scapy, și interpretând răspunsurile SYN/ACK sau RST – practic replicând comportamentul nmap -sS). O altă extensie utilă ar fi includerea de banner grabbing: pentru porturile deschise identificate, programul poate încerca să trimită automat o solicitare minimă (de exemplu, un “HEAD / HTTP/1.0” pentru portul 80) și să capteze răspunsul pentru a identifica versiunea serviciului. În plus, echipa poate extinde analiza post-scanare: de pildă, interogarea unei baze de date de vulnerabilități cunoscute pe baza versiunii serviciilor (aceasta însă doar la nivel de discuție, nu implementare integrată). Aceste extensii vor demonstra cunoștințe aprofundate și abilități tehnice ridicate, dar nu sunt obligatorii. - Echipe de 2 persoane: Vor realiza scanner-ul de porturi standard și analiza de securitate de bază, conform descrierilor din etapele 2-4. Distribuirea muncii poate fi astfel încât un membru se concentrează pe partea de cod și funcționalitatea tehnică, iar celălalt pe documentare și interpretare, deși ambele părți trebuie să colaboreze strâns. O mică extensie posibilă pentru două persoane este rularea scanner-ului pe mai multe ținte din rețea (de exemplu, scanarea a 2-3 mașini diferite) și compararea rezultatelor, pentru a oferi un context mai larg în raport. Important este însă ca utilitarul să funcționeze corect și raportul să conțină o discuție coerentă despre securitatea sistemului scanat. - Echipe de 1 persoană: Un student individual poate reduce anvergura proiectului pentru a fi realizabil într-un timp mai scurt, dar păstrând esența educațională. De exemplu, se poate limita scanarea la primele 1024 porturi TCP ale propriei mașini (localhost), unde studentul știe ce servicii sunt active, și astfel poate verifica ușor rezultatele. Implementarea poate fi secvențială (fără paralelizare), dacă gestionarea thread-urilor e prea complexă de integrat de o singură persoană – accentul va fi pe corectitudinea detecției porturilor deschise. Analiza de securitate va fi mai simplă și focalizată pe interpretarea câtorva porturi găsite (ex: “Am scanat localhost și am găsit portul 80 deschis – am un server Apache, trebuie să mă asigur că e actualizat la zi și configurat corespunzător.”). Chiar și fără toate optimizările, studentul trebuie să demonstreze că a înțeles mecanismul și poate comenta asupra implicațiilor de securitate, în loc să ofere doar un cod funcțional.

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

Bhuyan, M. H., Bhattacharyya, D. K., & Kalita, J. K. (2011). Surveying Port Scans and Their Detection Methodologies. The Computer Journal, 54(10), 1565–1581. DOI: 10.1093/comjnl/bxr035
Abu Bakar, R., & Kijsirikul, B. (2023). Enhancing Network Visibility and Security with Advanced Port Scanning Techniques. Sensors, 23(17), 7541. DOI: 10.3390/s23177541
---

## 🔮 Verificare înțelegere — Rețele

Înainte de configurare:

1. **Ce tip de adresă este 192.168.1.50?**
   - Adresă privată (RFC 1918)

2. **Câte adrese IP utilizabile sunt într-o rețea /24?**
   - 254 (256 - 1 rețea - 1 broadcast)

3. **Ce face NAT?**
   - Traduce adrese private în publice pentru acces Internet

---

## 📊 Peer Instruction — Rețele

**Întrebare:** Un dispozitiv are IP 192.168.1.50. Ce tip de adresă este?

- A) Adresă publică
- B) Adresă privată (RFC 1918) ✓
- C) Adresă loopback
- D) Adresă broadcast


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
- TCP connect scan, socket timeout

**Fișiere recomandate:**
- `02roWSL/README.md` — prezentare generală și pași de laborator
- `02roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `02roWSL/docs/fisa_comenzi.md` — comenzi utile
- `02roWSL/src/` — exemple de cod Python
- `02roWSL/homework/` — exerciții similare


### 📁 `07roWSL/` — Interceptare Pachete

**Ce găsești relevant:**
- Analiza răspunsurilor TCP

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `13roWSL/` — Securitate

**Ce găsești relevant:**
- Ethical hacking, vulnerability assessment

**Fișiere recomandate:**
- `13roWSL/README.md` — prezentare generală și pași de laborator
- `13roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `13roWSL/docs/fisa_comenzi.md` — comenzi utile
- `13roWSL/src/` — exemple de cod Python
- `13roWSL/homework/` — exerciții similare


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
