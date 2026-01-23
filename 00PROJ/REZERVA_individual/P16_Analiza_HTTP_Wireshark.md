# Proiectul 16: Analiza traficului HTTP utilizând Wireshark

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
https://github.com/[username]/retele-proiect-16
```

#### Structura obligatorie a repository-ului

```
retele-proiect-16/
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

**Format:** `NUME_Prenume_GGGG_P16_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P16 | Numărul proiectului | P16 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P16_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P16_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P16_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect constă în examinarea detaliată a comunicării HTTP prin capturarea și analiza pachetelor de rețea. Studenții vor configura un mediu de test (de exemplu, un server web simplu și un browser web client) și vor folosi Wireshark pentru a captura traficul HTTP. Se va observa structura cererilor și răspunsurilor HTTP, incluzând antetele, codurile de stare și conținutul transmis. Scopul este de a înțelege în mod practic modul de funcționare al protocolului HTTP la nivel de pachet și de a evidenția importanța elementelor precum metodele HTTP (GET/POST), codurile de stare (200, 404 etc.) și lipsa criptării pe HTTP. Analiza comparativă a traficului poate include și diferențe între HTTP și HTTPS, subliniind necesitatea securizării comunicațiilor web. Proiectul are un caracter aplicativ, ajutând la consolidarea cunoștințelor teoretice despre protocolul HTTP prin experimentare directă cu instrumente de analiză a rețelei.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Wireshark (analizor de pachete), un browser web (sau utilitar HTTP precum curl), eventual un server web simplu (ex: Python HTTP server sau Apache local) pentru generarea traficului, protocolul TCP/IP (suport pentru transportul HTTP), sistem de operare pentru rularea experimentelor (Windows/Linux), conexiune de rețea localhost sau LAN pentru testare.
Legătura cu săptămânile și kiturile: Proiectul valorifică cunoștințele predate în săptămâna 1 (fundamentele rețelelor și instrumente de monitorizare) și săptămâna 10 (nivelul aplicație – protocolul HTTP). Se bazează pe kitul de captură și analiză a traficului introdus la laboratorul din săptămâna 1 (configurare Wireshark, utilitare de generare trafic) și aplică în practică conceptele teoretice despre HTTP discutate în cursul din săptămâna 10. Studenții vor folosi abilitățile de filtrare și interpretare a pachetelor dobândite anterior pentru a realiza acest proiect.
Structura pe 4 etape: 1. Etapa 1: Pregătirea mediului și documentarea. În prima etapă, echipa se familiarizează cu protocolul HTTP (revizuind specificațiile de bază și exemple) și instalează/configurează instrumentele necesare (Wireshark, server web local dacă este cazul). Se definește scenariul de test – de exemplu, descărcarea unei pagini web simple – și se verifică conectivitatea între client și server. 2. Etapa 2: Capturarea traficului HTTP. Se execută scenariul de test configurat, generând trafic HTTP (de exemplu, accesarea paginii web de test prin browser). Wireshark este folosit pentru a captura pachetele în timpul comunicării. Echipa aplică filtre adecvate (de ex. http sau port 80) pentru a izola pachetele relevante. Se salvează capturile pentru analiza ulterioară. 3. Etapa 3: Analiza și interpretarea datelor. În această etapă, echipa inspectează în detaliu pachetele capturate. Se identifică cererea HTTP (linia de cerere, antetele trimise de client) și răspunsul HTTP (linia de status, antetele serverului și eventual corpul mesajului). Se analizează campurile importante precum URL-ul solicitat, codul de status al răspunsului, tipul de conținut, lungimea conținutului etc. Totodată, se urmărește succesiunea pachetelor pentru a înțelege handshake-ul TCP inițial și terminarea conexiunii. Dacă se compară HTTP cu HTTPS, se observă că pachetele HTTPS sunt criptate (datele din payload nu sunt în clar). Se notează constatările, eventual cu capturi de ecran din Wireshark adnotate. 4. Etapa 4: Concluzii și documentare. Echipa interpretează rezultatele analizei, formulând concluzii despre modul de funcționare al HTTP și aspectele de securitate. De exemplu, se poate evidenția cum informațiile (inclusiv eventuale credențiale) circulă în clar prin HTTP și riscurile asociate, respectiv beneficiile trecerii la HTTPS. Se elaborează raportul final al proiectului, care va include descrierea metodologiei, capturi relevante ale pachetelor și explicațiile lor, precum și concluzii privind înțelegerea aprofundată a protocolului. Raportul va fi redactat academic, cu referiri la conceptele teoretice și bibliografia de specialitate.

### 🔮 VERIFICARE ÎNȚELEGERE

Înainte de a continua, răspundeți:

1. Ce tip de adresă este 192.168.1.50?
   → Adresă privată (RFC 1918)

2. Câte adrese IP utilizabile sunt într-o rețea /24?
   → 254 (256 - 1 rețea - 1 broadcast)

3. Ce cod HTTP indică "resursă negăsită"?
   → 404 Not Found


📊 PEER INSTRUCTION

Întrebare: Ce face NAT (Network Address Translation)?

A) Criptează traficul
B) Traduce adrese private în publice ✓
C) Alocă adrese automat
D) Filtrează pachete

Explicație: NAT permite dispozitivelor cu IP privat să acceseze Internetul.


### 📊 Extensii pentru echipe de 3/2/1: - Echipe de 3 persoane: Pe lângă scenariul de bază, se va analiza traficul pentru varietate de cazuri HTTP. De exemplu, echipa poate realiza capturi pentru o cerere POST (trimiterea unui formular) sau descărcarea unui fișier, și va compara aceste tipuri de trafic cu cererile GET. Totodată, se va include o analiză comparativă HTTP vs HTTPS, arătând exact ce informații sunt vizibile în HTTP dar ascunse în HTTPS (prin realizarea unei capturi Wireshark pe accesarea aceluiași site prin HTTP și apoi prin HTTPS). Această extensie demonstrează înțelegerea aprofundată a securității comunicațiilor web. - Echipe de 2 persoane: Se va realiza scenariul standard descris mai sus, concentrându-se pe o singură interacțiune HTTP (de exemplu, accesarea unei pagini web) și analiza detaliată a acesteia. Echipa va evidenția componentele cererii și răspunsului și va discuta problemele de securitate, dar complexitatea cazurilor analizate poate fi mai redusă decât la echipele de 3 (de exemplu, se poate omite compararea cu HTTPS dacă timpul nu permite). - Echipe de 1 persoană: Proiectul va fi redus ca amploare – de exemplu, analiza unei tranzacții HTTP foarte simple (cum ar fi o singură cerere GET către un server local și răspunsul aferent). Studentul individual va captura traficul și va identifica elementele esențiale (metoda, URL, cod status, antete principale), elaborând un scurt raport. Extensiile opționale (compararea mai multor metode HTTP sau HTTPS) nu sunt obligatorii pentru echipa de o persoană, însă pot fi menționate ca parte din concluzii teoretice.


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

Fielding, R. T., Gettys, J., Mogul, J. C., Frystyk, H., Masinter, L., Leach, P., & Berners-Lee, T. (1999). Hypertext Transfer Protocol – HTTP/1.1. RFC 2616, IETF. DOI: 10.17487/RFC2616
Luthfansa, Z. M., & Rosiani, U. D. (2021). Pemanfaatan Wireshark untuk Sniffing Komunikasi Data Berprotokol HTTP pada Jaringan Internet. Journal of Information Engineering and Educational Technology, 5(1), 34–39. DOI: 10.26740/jieet.v5n1.p34-39
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


### 📁 `07roWSL/` — Interceptarea Pachetelor

**Ce găsești relevant:**
- Wireshark, filtre de display și capture

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `08roWSL/` — Server HTTP

**Ce găsești relevant:**
- HTTP request/response, headers, status codes

**Fișiere recomandate:**
- `08roWSL/README.md` — prezentare generală și pași de laborator
- `08roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `08roWSL/docs/fisa_comenzi.md` — comenzi utile
- `08roWSL/src/` — exemple de cod Python
- `08roWSL/homework/` — exerciții similare


### 📁 `10roWSL/` — HTTPS

**Ce găsești relevant:**
- TLS handshake, certificate inspection

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
