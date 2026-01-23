# Proiectul 07: Sistem de monitorizare a traficului și firewall software (IDS simplu)

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
https://github.com/[username]/retele-proiect-07
```

#### Structura obligatorie a repository-ului

```
retele-proiect-07/
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

**Format:** `NUME_Prenume_GGGG_P07_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P07 | Numărul proiectului | P07 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P07_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P07_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P07_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect își propune realizarea unui sistem personalizat de monitorizare și filtrare a traficului de rețea, combinând funcționalitățile unui sniffer (capturator de pachete) cu cele ale unui firewall/IDS (Intrusion Detection System) simplu. Studenții vor dezvolta o aplicație (de regulă în Python) capabilă să intercepteze pachetele care tranzitează o interfață de rețea, să analizeze header-ele protocoalelor (Ethernet, IP, TCP/UDP etc.) și să aplice un set de reguli de filtrare sau de detectare a activităților suspecte. Proiectul are două componente majore: (a) Monitorizarea pasivă a traficului, în care aplicația loghează pachetele capturate (sau cel puțin statisticile relevante despre ele) pentru a oferi vizibilitate asupra comunicațiilor din rețea; și (b) Filtrarea/alertarea activă, în care anumite pachete ce corespund unor criterii prestabilite sunt fie blocate, fie declanșează alerte de securitate. Un exemplu concret ar fi implementarea unui modul de detectare a scanărilor de porturi: aplicația poate identifica când un anumit host trimite pachete SYN către un număr mare de porturi într-un interval scurt, interpretând acest comportament ca port scan și generând o alertă sau blocând temporar pachetele de la hostul respectiv. Totodată, se pot defini filtre simple, precum blocarea tuturor pachetelor către un anumit port (simulând un firewall care blochează de exemplu portul 23/Telnet) sau capturarea doar a traficului de un anumit tip (ex: doar pachete HTTP pe portul 80) pentru inspecție detaliată. Pe lângă latura practică de programare a unui astfel de instrument, proiectul are și o puternică componentă educațională: studenții vor aprofunda cunoașterea formatului pachetelor de rețea, a modului în care funcționează protocoalele la nivel de bit/byte, precum și a metodelor prin care atacurile pot fi detectate prin tipare de trafic. Ei vor învăța despre limitările unui IDS bazat pe semnături simple versus importanța analizelor mai complexe (dar care depășesc scopul acestui proiect introductiv) și vor conștientiza provocările în timp real ale procesării traficului (performanță, acuratețe, rate de alarme false). Proiectul permite testarea soluției dezvoltate folosind instrumente cunoscute: de exemplu, cu nmap se poate simula un port scan asupra unei mașini din rețea pentru a verifica dacă sistemul implementat detectează și semnalează corespunzător evenimentul. Astfel, studenții vor obține atât unelte practice (un mini-IDS pe care îl pot extinde ulterior), cât și înțelegerea de bază a conceptelor de securitate activă în rețele.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Python cu biblioteci de rețea de nivel jos – în special Scapy (o bibliotecă Python puternică pentru manipularea pachetelor, care permite atât captură cât și creare de pachete) sau socket (modulul standard Python, folosind socket.AF_PACKET în Linux pentru captură brută). Alternativ, se poate folosi libpcap în C/C++ sau PyShark (un wrapper pentru TShark/Wireshark). Pentru testare se vor utiliza nmap (scanner de porturi) și eventual generatoare de trafic (scripturi Python, hping3 etc.). Linux va fi mediul preferat (dat fiind accesul facil la raw sockets și la utilitare ca iptables pentru comparație). Totodată, Wireshark poate fi utilizat pentru a valida capturile efectuate de aplicația implementată. Optional, Docker poate fi folosit pentru a lansa containere care să joace rolul de surse de trafic malițios sau victime, facilitând scenarii de test controlate.
Legătura cu temele și kiturile săptămânilor 1–13: Proiectul are o legătură directă cu săptămânile din curs care tratează analiza și securitatea traficului. În mod specific, săptămâna 7 (“Interceptarea pachetelor TCP & UDP; implementarea unui filtru de pachete; scanarea porturilor”) constituie fundamentul teoretic al acestui proiect. În acea săptămână, studenții au văzut cum pot fi capturate pachetele cu unelte ca Wireshark sau tshark și au discutat despre scanările de porturi și filtrarea traficului – cunoștințe puse acum în practică, deoarece proiectul îi pune să construiască propriul “Wireshark light” și “Snort light”. Totodată, noțiunile din săptămâna 13 (Securitatea rețelelor de calculatoare) sunt aprofundate: concepte precum IDS, detectarea intruziunilor și tipuri de atacuri comune sunt aplicate în componenta de alertare a proiectului. Chiar și materialul din primele săptămâni este pertinent: de pildă, înțelegerea formatului pachetelor Ethernet și IP (prezentată în introducerea cursului, săptămânile 1-2) este esențială pentru a putea scrie un analizator de pachete corect. Săptămânile despre programarea pe socket-uri (3 și 4) sunt și ele relevante – în acele laboratoare studenții au dobândit abilități de a folosi API-ul de socket-uri, abilități care acum sunt extinse către programarea de raw sockets pentru captură. În rezumat, proiectul capitalizează pe întreg parcursul de învățare al disciplinei: începe cu elemente de rețea de nivel jos (structura pachetelor, socket-uri) și culminează cu aspecte de securitate (firewall, IDS), oferind un context integrator ce reflectă obiectivele disciplinei de a pregăti studenții în a asigura funcționarea și protecția rețelelor.
Structură în 4 etape:
Extensii pentru echipe de 3 vs. echipe de 2/1: O echipă mai mare (3 membri) este așteptată să abordeze proiectul într-un mod mai cuprinzător, implementând reguli și funcții suplimentare față de minimul necesar. De exemplu, echipele de 3 ar putea implementa o interfață grafică simplă pentru IDS (un tablou de bord web sau cu biblioteci Python precum Tkinter) unde să afișeze în timp real alertele și statisticile de trafic – acest lucru ar adăuga o dimensiune practică deosebită, permițând administratorului să vizualizeze ușor starea rețelei. Totodată, ar putea suporta un fișier de configurare extern pentru reguli, astfel încât noile filtre (ex. “blocare port X”) să poată fi adăugate fără a modifica codul sursă, simulând modul de lucru al unui firewall real. În plus, ar fi de dorit ca echipele mari să testeze sistemul într-un mediu mai complex, poate într-o rețea reală de laborator sau folosind containere multiple ce generează trafic simultan, pentru a demonstra scalabilitatea (ex. folosind Docker Compose pentru a lansa 5 containere client care trimit trafic spre 2 servere și un container dedicat IDS-ului). Pentru echipele mai mici (2 sau 1 membru), cerințele minime – captură, o mână de filtre simple și detectarea unui tip de atac – sunt suficiente, dar complexitatea poate fi ajustată: de exemplu, un student singur s-ar putea concentra doar pe detectarea port scan-urilor și pe blocarea unui singur port per configurare, fără interfață sau alte extrase. Important este ca fiecare echipă să acopere partea esențială (captură + filtrare + alertare) și să demonstreze că soluția funcționează. Extensiile menționate (interfață, configurabilitate sporită, suport extins pentru multiple tipuri de atacuri – ex. detectarea unui atac de tip DoS prin analiză de trafic agregat) vor diferenția proiectele excelente, realizate de echipe cu resurse mai numeroase, de proiectele corecte realizate de echipe mai mici.

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

Joseph, G., Osamor, J., & Olajide, F. (2024). A Systematic Review of Network Packet Sniffing Tools for Enhancing Cybersecurity in Business Applications. International Journal of Intelligent Computing Research, 15(1), 1292-1307. https://doi.org/10.20533/ijicr.2042.4655.2024.0157
Abu Bakar, R., & Kijsirikul, B. (2023). Enhancing Network Visibility and Security with Advanced Port Scanning Techniques. Sensors, 23(17), 7541. https://doi.org/10.3390/s23177541
Grossi, M., Alfonsi, F., Prandini, M., & Gabrielli, A. (2023). A Highly Configurable Packet Sniffer Based on Field-Programmable Gate Arrays for Network Security Applications. Electronics, 12(21), 4412. https://doi.org/10.3390/electronics12214412
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


### 📁 `07roWSL/` — Interceptarea și Filtrarea Pachetelor

**Ce găsești relevant:**
- iptables, reguli de filtrare

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `13roWSL/` — Securitate

**Ce găsești relevant:**
- Detectarea atacurilor, logging

**Fișiere recomandate:**
- `13roWSL/README.md` — prezentare generală și pași de laborator
- `13roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `13roWSL/docs/fisa_comenzi.md` — comenzi utile
- `13roWSL/src/` — exemple de cod Python
- `13roWSL/homework/` — exerciții similare


### 📁 `06roWSL/` — NAT/PAT

**Ce găsești relevant:**
- Firewall rules, NAT traversal

**Fișiere recomandate:**
- `06roWSL/README.md` — prezentare generală și pași de laborator
- `06roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `06roWSL/docs/fisa_comenzi.md` — comenzi utile
- `06roWSL/src/` — exemple de cod Python
- `06roWSL/homework/` — exerciții similare


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
