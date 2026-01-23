# Proiectul 17: Proiectarea unei rețele locale cu NAT și DHCP în Cisco Packet Tracer

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
https://github.com/[username]/retele-proiect-17
```

#### Structura obligatorie a repository-ului

```
retele-proiect-17/
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

**Format:** `NUME_Prenume_GGGG_P17_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P17 | Numărul proiectului | P17 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P17_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P17_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P17_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect urmărește crearea și configurarea unei mici rețele locale (LAN) într-un mediu simulat (Cisco Packet Tracer), punând accent pe mecanismele de adresare IP și acces la Internet prin NAT. Studenții vor proiecta o topologie ce include cel puțin un router, un switch și un set de calculatoare/clienți. Router-ul va fi configurat să aloce adrese IP dintr-un domeniu privat folosind DHCP (Dynamic Host Configuration Protocol) și să realizeze NAT (Network Address Translation) pentru a permite dispozitivelor din rețeaua locală accesul către o rețea externă (simulând Internetul). Se vor aplica concepte de subnetting pentru a configura adresele IP eficient. Proiectul are un caracter practic de network design și administrare, oferind studenților oportunitatea de a pune cap la cap componentele studiate (adresare IP, routing de bază, traducerea adreselor) într-un exemplu realist de rețea de companie mică sau domiciliu.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Cisco Packet Tracer (instrument de simulare a rețelelor), echipamente Cisco simulate (Router Cisco, Switch Cisco, PC-uri), protocolul DHCP, protocolul NAT (implementat pe router conform standardelor RFC)[3], protocoale ICMP (pentru ping), TCP/UDP (pentru testarea traficului prin NAT), eventual configurări de routing (statis sau dinamice de bază). Nu este necesar hardware real, toată implementarea având loc în mediu virtual.
Legătura cu săptămânile și kiturile: Proiectul se leagă direct de materialul din săptămâna 5 (adresare IP, subnetting IPv4/IPv6) și săptămâna 6 (configurații de rețea – NAT, DHCP, protocoale de configurare și management). Kiturile de laborator relevante includ scheletul de rețea LAN și exercițiile de configurare a routerelor din săptămânile 5-6 (de exemplu, un fișier Packet Tracer de bază cu dispozitive preplasate sau exemple de configurări de DHCP/NAT). Studenții vor porni de la aceste exemple practice, extinzându-le în proiectul actual. Astfel, proiectul consolidează cunoștințele acumulate în prima jumătate a cursului, oferind o perspectivă practică unitară asupra construirii unei rețele funcționale.
Structura pe 4 etape: 1. Etapa 1: Proiectarea rețelei și stabilirea parametrilor. Se începe cu definirea cerințelor rețelei: numărul de subrețele și de host-uri necesare, spațiul de adrese IP disponibil. Echipa realizează un design logic al topologiei (ex: o subrețea LAN pentru stații, un router conectat la Internet simulat). Se calculează un plan de subnetting (de exemplu, dintr-o adresă de clasă C privată se determină subrețeaua potrivită). Se documentează adresele IP ce vor fi atribuite (rețea, gateway, DHCP pool etc.) și se pregătește diagrama topologică. 2. Etapa 2: Configurare în Cisco Packet Tracer – partea de bază. Folosind Packet Tracer, se realizează practic topologia propusă: se plasează router-ul, switch-ul și PC-urile și se conectează cu cabluri adecvate. Se configurează interfețele router-ului (de exemplu, interfata LAN cu adresă statică din subnetul local, și interfata WAN cu o adresă simulând o rețea publică). Apoi, se activează și configurează serviciul DHCP pe router (specificând rețeaua, masca, gateway-ul, DNS eventual). PC-urile sunt setate să obțină IP dinamic. După aceea, se configurează NAT pe router: se stabilește care interfață este „inside” și care „outside”, se definește o listă de acces sau se folosește comanda simplificată pentru NAT masquat (PAT) și se verifică traducerile (de exemplu cu show ip nat translations). Această etapă asigură că rețeaua locală are configurate toate elementele pentru conectivitate internă. 3. Etapa 3: Testare și ajustări. În această etapă, se testează funcționalitatea rețelei. Se pornește fiecare PC, care ar trebui să primească automat o adresă IP de la DHCP – se verifică în Packet Tracer configurarea IP a fiecărui PC. Apoi, se testează conexiunea către exterior (de exemplu, routerul poate avea ca „Internet” un cloud PT conectat sau un alt router simulând ISP-ul). Se folosește comanda ping de pe un PC către o adresă externă (de exemplu, interfata WAN a routerului ISP) și se observă dacă există răspuns. Dacă testul e pozitiv, înseamnă că DHCP și NAT funcționează corect. Se pot realiza și teste suplimentare: de exemplu, trimiterea unui ping din exterior către un PC din LAN (care ar trebui blocat implicit de NAT, evidențiind faptul că LAN-ul nu este direct accesibil din afară). Echipa va depana eventualele probleme (de ex., dacă PC-urile nu obțin IP, se verifică setările DHCP; dacă nu funcționează NAT, se verifică dacă interfețele inside/outside au fost corect desemnate). Se finalizează configurările adăugând eventual un server DNS simulativ sau alte elemente dacă sunt necesare pentru test (opțional). 4. Etapa 4: Documentare și optimizare. În ultima etapă, se realizează documentația proiectului. Aceasta include diagrama rețelei, tabele cu adresele IP alocate, configurațiile relevante extrase de pe router (ex. output de la show run filtrat pentru DHCP și NAT). Totodată, se descrie modul în care s-a realizat configurarea pas cu pas și se explică de ce setările alese sunt corecte. Se analizează funcționalitatea: echipa argumentează cum DHCP ușurează administrarea (față de configurare manuală) și cum NAT permite reutilizarea adreselor private și oferă un nivel de izolare a rețelei interne. Dacă au existat provocări sau optimizări (ex. ajustarea mărimii pool-ului DHCP, rezervarea unor adrese fixe, implementarea de liste de acces pentru securitate rudimentară), acestea sunt discutate. Documentația se încheie cu concluzii despre experiența practică dobândită în configurarea unei rețele reale la scară mică.
Extensii pentru echipe de 3/2/1: - Echipe de 3 persoane: Se va extinde proiectul la o topologie puțin mai complexă. De exemplu, în locul unei singure rețele LAN, se pot configura două subrețele LAN distincte (departamente diferite) interconectate prin router, necesitând rutare statică sau chiar un protocol de rutare dinamică de bază (ex. OSPF pe intern). Fiecare subrețea va avea propriul pool DHCP. Routerul va fi configurat cu NAT pentru ambele subrețele către Internet. Echipa poate integra și IPv6 în proiect (configurând dual-stack cu DHCPv6 sau SLAAC pentru experiență suplimentară). Aceste extinderi aduc provocări suplimentare de configurare și oferă ocazia de a demonstra cunoștințe mai avansate (ex. operarea unui protocol de rutare). - Echipe de 2 persoane: Vor implementa scenariul de bază prezentat, cu o singură rețea LAN deservită de DHCP și acces la Internet prin NAT. Toate cerințele principale (DHCP funcțional, NAT funcțional, conectivitate verificată) trebuie realizate. Extensiile complexe precum a doua subrețea sau IPv6 nu sunt necesare, însă echipa poate opta pentru mici îmbunătățiri, de exemplu definirea unui DNS server local în configurarea DHCP sau testarea funcției de Port Forwarding (NAT static) pentru a înțelege cum ar expune un server intern către Internet. - Echipe de 1 persoană: Un singur student va realiza o versiune simplificată a proiectului. De exemplu, dacă configurarea DHCP și NAT simultan este prea complexă de gestionat individual, se poate limita la DHCP + NAT pe o singură rețea cu un număr redus de host-uri. Studentul poate folosi configurații mai simple (ex. un singur PC client în LAN) pentru a demonstra conceptul. Opțional, se poate permite configurarea manuală a IP-urilor pe PC-uri în loc de DHCP, dacă se dorește reducerea complexității – accentul rămânând pe înțelegerea NAT. Important este ca studentul să explice în raport configurațiile făcute și să demonstreze că a obținut conectivitate la Internet din LAN. Extensiile opționale nu sunt necesare în cazul proiectelor individuale, dar o discuție despre cum s-ar putea extinde rețeaua pe viitor poate fi apreciată.

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

Ambiyar, A., Yondri, S., Irfan, D., Putri, M. D., Zaus, M. A., & Islami, S. (2019). Evaluation of Packet Tracer Application Effectiveness in Computer Design Networking Subject. International Journal on Advanced Science, Engineering and Information Technology, 9(1), 78–85. DOI: 10.18517/ijaseit.9.1.5931
Srisuresh, P., & Egevang, K. (2001). Traditional IP Network Address Translator (Traditional NAT). RFC 3022, IETF. DOI: 10.17487/RFC3022
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


---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `06roWSL/` — NAT/PAT

**Ce găsești relevant:**
- Configurare NAT, port forwarding

**Fișiere recomandate:**
- `06roWSL/README.md` — prezentare generală și pași de laborator
- `06roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `06roWSL/docs/fisa_comenzi.md` — comenzi utile
- `06roWSL/src/` — exemple de cod Python
- `06roWSL/homework/` — exerciții similare


### 📁 `05roWSL/` — Adresare IP

**Ce găsești relevant:**
- DHCP, alocare dinamică adrese

**Fișiere recomandate:**
- `05roWSL/README.md` — prezentare generală și pași de laborator
- `05roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `05roWSL/docs/fisa_comenzi.md` — comenzi utile
- `05roWSL/src/` — exemple de cod Python
- `05roWSL/homework/` — exerciții similare


### 📁 `01roWSL/` — Fundamentele Rețelelor

**Ce găsești relevant:**
- Topologii LAN, adresare

**Fișiere recomandate:**
- `01roWSL/README.md` — prezentare generală și pași de laborator
- `01roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `01roWSL/docs/fisa_comenzi.md` — comenzi utile
- `01roWSL/src/` — exemple de cod Python
- `01roWSL/homework/` — exerciții similare


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
