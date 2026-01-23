# Proiectul 03: Monitorizarea traficului și detectarea intruziunilor cu Python

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
https://github.com/[username]/retele-proiect-03
```

#### Structura obligatorie a repository-ului

```
retele-proiect-03/
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

**Format:** `NUME_Prenume_GGGG_P03_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P03 | Numărul proiectului | P03 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P03_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P03_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P03_S07.zip` — Verificare săptămâna 7

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
Acest proiect vizează realizarea unui sistem simplificat de monitorizare a traficului de rețea combinat cu elemente de IDS (Intrusion Detection System), utilizând instrumente software și scripturi Python. Studenții vor dezvolta o aplicație capabilă să captureze pachete într-o rețea locală (sau să proceseze fișiere capturate) și să le analizeze pentru a identifica tipare suspecte sau activități malițioase de tip atac informatic. Practic, proiectul constă în două componente principale: (1) un modul de captură și înregistrare a traficului de rețea (de exemplu folosind biblioteca pcapy sau scapy în Python, ori prin interfata tshark/Wireshark), și (2) un modul de detecție a anomaliilor bazat pe acele capturi (folosind reguli simple sau praguri prestabilite).
Scenariile de atac ce pot fi detectate de sistemul propus includ, de exemplu, un scan de porturi (caracterizat de un număr mare de conexiuni către porturi diferite într-un interval scurt), un posibil atac de tip DoS (un val intens de pachete ICMP Echo Request – ping – către o țintă), sau trafic ce indică o tentativă de acces neautorizat (de exemplu, multiple încercări de autentificare eșuate într-un protocol). Echipa va defini un set de semnături sau euristici simple pentru astfel de evenimente și va implementa logica în Python: pe măsură ce pachetele sunt procesate, scriptul va genera alerte dacă este depășit un anumit prag (ex: >100 de conexiuni pe secundă de la aceeași sursă) sau dacă apar tipare cunoscute (ex: un string specific într-un payload care corespunde unui exploit). Rezultatul va fi un tool de monitorizare care poate afișa statistici de trafic în timp real și raporta alerte de securitate, demonstrând conceptele de bază ale unui sistem de detecție a intruziunilor.

### 🎯 Obiective de învățare

Familiarizarea cu captura de trafic la nivel de pachete în rețea și formatele de stocare (PCAP), alături de instrumente precum tcpdump sau Wireshark pentru inspecția traficului.

### 🛠️ Tehnologii și unelte

Înțelegerea conceptelor de bază din securitatea rețelelor, cum ar fi tipurile de atacuri (scanare, DoS, brute-force), și definirea de heuristici de detecție pentru acestea.
Dezvoltarea abilităților de a proiecta un sistem de monitorizare: colectare de date, procesare în timp real (sau aproape real), generare de log-uri/alerte și prezentarea informației într-un mod util.
Conștientizarea limitărilor unui IDS simplu și a conceptului de rată de alarme fals pozitive vs. fals negative, precum și a importanței ajustării pragurilor de detecție.

### 📖 Concepte cheie

Protocoale de rețea și formate de pachete – structură de pachete Ethernet, IP, TCP/UDP, ICMP; interpretarea header-elor (adrese, porturi, flag-uri) din perspective de securitate.
Analiza traficului – metrici de trafic (număr de pachete, byte transferați, sesiuni active), distribuții pe protocoale/porturi; folosirea filtrării BPF (Berkeley Packet Filter) pentru a selecta pachete relevante.
Detecția intruziunilor – semnături vs. detecție pe bază de anomalii; exemple de semnături simple (ex: secvență de bytes specifici într-un payload ce indică un exploit cunoscut) și exemple de anomalii (trafic voluminos atipic).
Securitate rețea – tipuri de atacuri comune (scanare porturi, Ping flood, SYN flood, atacuri la nivel aplicație) și impactul lor asupra rețelei; mecanisme defensive (IDS/IPS, firewall) și locul unui IDS în infrastructură.
Programare Python avansată – lucru cu pachete binare, structuri de date eficiente pentru contorizare (dicționare pentru numărarea conexiunilor per IP, de exemplu), programare orientată eveniment (captură continuă de pachete).
Tehnologii implicate
Limbajul Python – limbaj principal pentru implementare; se vor folosi module third-party specializate:
Scapy – bibliotecă puternică pentru manipularea pachetelor (poate captura, construi și interpreta pachete de la nivel link până la aplicație).
Pcapy/dpkt – biblioteci alternative bazate pe libpcap pentru captură raw de pachete.
Wireshark/Tshark – instrument grafic (Wireshark) sau linie de comandă (tshark) pentru capturarea și inspectarea traficului, utilizat pentru validarea funcționării (de ex., compararea rezultatelor scriptului Python cu cele capturate de Wireshark).
Linux – se va folosi un mediu Linux pentru acces la interfața de rețea în modul promiscuu. Utilitare precum tcpdump pot fi folosite la nevoie pentru a genera fișiere PCAP ce vor fi analizate offline de script.
Rețea de test – se poate folosi fie rețeaua locală reală (în limite sigure) pentru a genera trafic (ex: scanare de porturi cu nmap pe un host de test), fie o rețea virtuală izolată (ex: 2-3 VM-uri în VirtualBox/Mininet) unde să se lanseze atacuri simulate.
Biblioteci de logare și alertare – ex: module Python pentru log (logging) sau chiar email/SMS (dacă se dorește trimiterea alertelor într-un anumit format).
Legătura cu temele din săptămânile cursului
Săptămâna 7: Transport (TCP/UDP) – interpretarea flag-urilor TCP (SYN, FIN, etc.) este esențială pentru a detecta anumite atacuri (ex: scanare TCP SYN); conceptele studiate la curs ajută la recunoașterea comportamentelor anormale în secvențele TCP.
Săptămâna 9: Securitatea rețelelor – proiectul se bazează direct pe noțiunile de atac și apărare discutate în cursul din sapt. 9 (vezi prezentarea „Introducere IDS și IPS” din arhiva WEEK9, care oferă context teoretic).
Săptămâna 12: Programare de rețea în Python – se aplică practic cunoștințele de scripting de rețea din lab. Week12 („Packet Sniffing cu Python” din arhivă), extinzându-le cu logică de detecție a intruziunilor.
Săptămâna 8: Protocoale de aplicație – anumite atacuri țintesc nivelul aplicație (ex: HTTP flood), deci înțelegerea modului în care funcționează protocoalele de aplicație (discutate în curs) poate ajuta la interpretarea traficului capturat.
Etapele proiectului

### 📋 Etapa 1 (Săptămâna 5) – Documentare și definire specificații: Cercetarea tipurilor de atacuri de rețea ce pot fi detectate cu metode simple și alegerea a 2-3 tipare de detectat (de exemplu: scanare de porturi, ICMP flood, autentificare eșuată repetată pe FTP). Se stabilește metodologia: captura în timp real vs. offline (din fișier), instrumentele ce vor fi folosite (ex: scapy pentru captura live). Livrabil: un plan de proiect ce conține lista de scenarii de atac ce vor fi detectate, pentru fiecare specificându-se ce metrică sau semnătură va fi folosită (ex: “scanare porturi – criteriu: >20 de porturi distincte accesate de același IP sursă în < 1 minut”). Totodată, se va pregăti mediul de lucru: instalarea bibliotecilor necesare (scapy etc.) și eventual scrierea unui script Python minimal care să captureze pachete și să afișeze câteva informații (ca proof-of-concept). Codul inițial se încarcă în repository.


### 🔨 Etapa 2 (Săptămâna 9) – Dezvoltare componentă de captură și monitorizare: Implementarea modulului care colectează traficul și calculează statisticile necesare. De exemplu, se poate realiza un sniffer care rulează pe o interfață de rețea și înregistrează pachetele într-o structură de date. Se vor folosi dicționare sau contori pentru a ține evidența numărului de conexiuni/pachete per adresă IP sursă, per port destinație etc., în timp real. Se implementează afișarea periodică (ex: la fiecare 5 secunde) a unor statistici sumare pe consolă (trafic total, top 5 adrese sursă după număr de pachete, etc.). Livrabil: codul Python actualizat în repository, cu funcționalitatea de sniffing și monitorizare de bază completată, plus un scurt raport/intermediar sau capturi de ecran care demonstrează rularea sniffer-ului pe o rețea de test (de ex., se pornește scriptul și se execută un ping de test, iar scriptul loghează pachetele ICMP observate).


### 🔮 VERIFICARE ÎNȚELEGERE - CONCEPTE REȚEA

Înainte de configurare, verificați că înțelegeți:

1. Ce tip de adresă este 192.168.1.50?
   → Adresă privată (RFC 1918), nu poate fi rutată direct pe Internet

2. Câte adrese IP utilizabile sunt într-o rețea /24?
   → 254 adrese (256 total minus 1 pentru rețea minus 1 pentru broadcast)

3. Ce rol are NAT în rețeaua voastră?
   → Traduce adresele IP private în adresa publică pentru acces Internet


### ✅ Etapa 3 (Săptămâna 13) – Dezvoltare componentă de detecție și alerte & testare finală: Se integrează în script logica de detecție a intruziunilor conform specificațiilor stabilite. De exemplu, se implementează o funcție care, la fiecare interval, analizează datele colectate: dacă o anumită adresă IP are comunicări către > X porturi unice, se generează o alertă de tip “Possible port scan from IP ...”. Similar pentru celelalte tipare (DoS – pps peste prag, etc.). Alerta poate fi sub formă de mesaj în consolă, log în fișier sau notificare. Se vor genera apoi într-un mediu controlat trafice care să declanșeze aceste alerte (de exemplu, folosind nmap pentru scanare, sau un script care face multe conexiuni). Se evaluează acuratețea: alertele apar când trebuie și absența alertelor false la trafic normal. Livrabil: codul sursă final (documentat, cu eventuale fișiere de configurare pentru praguri), alături de un jurnal de testare detaliat. Jurnalul va descrie cum s-a simulat fiecare scenariu de atac și dacă sistemul a detectat, incluzând fragmente de loguri/alerte generate. Se vor nota limitări (ex: “sistemul nu distinge între scanare și un program legitim care face conexiuni multiple – posibile alarme false”).


### 📊 PEER INSTRUCTION - CONCEPTE REȚEA

Discutați cu colegii și alegeți împreună răspunsul corect:

Întrebarea 1: Un dispozitiv are adresa IP 192.168.1.50. Ce tip de adresă este aceasta?

A) Adresă publică, rutabilă pe Internet
B) Adresă privată conform RFC 1918 ✓
C) Adresă de loopback
D) Adresă broadcast

Explicație: Range-uri private: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16. Acestea necesită NAT pentru acces Internet.

Întrebarea 2: Într-o rețea cu masca /24, câte adrese IP sunt disponibile pentru dispozitive?

A) 256 adrese
B) 254 adrese ✓
C) 255 adrese
D) 252 adrese

Explicație: /24 = 256 adrese totale. Scădem: 1 adresă de rețea (ex: .0) și 1 broadcast (ex: .255) = 254 utilizabile.


### 🎤 Etapa 4 (Săptămâna 14) – Prezentare finală: În cadrul prezentării, echipa va explica arhitectura soluției (modul de captură, modul de detecție), apoi va demonstra live funcționarea IDS-ului. De exemplu, vor rula scriptul pe o interfață de rețea în timp ce un membru execută un atac de test (cum ar fi un port scan), arătând cum alerta apare în consola aplicației. Se vor discuta pe scurt și idei de îmbunătățire (cum ar fi folosirea unor algoritmi de învățare automată pentru detecție avansată, deși neimplementați aici). Livrabil: prezentarea (slides) și, opțional, un set de fișiere PCAP pregătite pentru demo (în cazul în care se preferă redarea offline a unui atac în locul execuției lui live, pentru consecvență).

Extensii posibile pentru echipe de 3 vs. 2/1 studenți
O echipă de 3 studenți ar putea extinde considerabil proiectul spre un IDS mai sofisticat. De pildă, ar putea implementa o interfață grafică simplă (GUI web) care afișează în timp real grafic traficul și alertele, folosind un framework Python (Flask + chart libraries). Totodată, s-ar putea adăuga mai multe tipuri de detecții (ex: detecție de scanare DNS sau de atacuri SQL injection la nivel de conținut, dacă se analizează payload-ul pachetelor). O altă extensie ar fi includerea unei componente de ** răspuns activ** – de exemplu, la detectarea unui atac, scriptul să ruleze o comandă de blocare a IP-ului agresor (prin configurarea unui firewall local).
O echipă de 1-2 studenți se poate limita la implementarea nucleului functional: captură și una-două reguli de detecție de bază. De exemplu, un proiect simplificat ar putea doar să detecteze scanările de porturi, fără alte tipuri de atac. În plus, dacă implementarea capturii live se dovedește complicată, echipa mică poate alege să analizeze fișiere PCAP capturate anterior, concentrându-se mai mult pe partea de analiză offline decât pe ingineria timp-real. Astfel volumul de cod scade, dar obiectivele de învățare (analiza traficului și recunoașterea tiparelor) rămân atinse.

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

Scarfone, K., & Mell, P. (2007). Guide to Intrusion Detection and Prevention Systems (IDPS). NIST Special Publication 800-94. (Ghid exhaustiv oferit de NIST despre conceptele și practicile IDS/IPS)
Sanders, C. (2010). Practical Packet Analysis: Using Wireshark to Solve Real-World Network Problems (2nd ed.). No Starch Press. (Carte orientată pe interpretarea pachetelor și trafic, utilă pentru partea de monitorizare și înțelegere a tiparelor de trafic)
Biondi, P. (2004). Scapy Project Documentation. Retrieved 2023, from https://scapy.readthedocs.io (Documentația oficială Scapy, incluzând tutoriale despre sniffing și exemple de utilizare a librăriei în scenarii de securitate)
Roesch, M. (1999). Snort - Lightweight Intrusion Detection for Networks. Proceedings of the 13th USENIX Conference on System Administration (LISA ’99), 229-238. (Lucrarea inițială care prezintă Snort, un IDS open-source; oferă context despre detectarea bazată pe semnături și performanța în timp real)
RFC 783 – Postel, J., & Reynolds, J. (1981). TFTP Protocol (Revision 2). IETF. (Exemplu de protocol simplu susceptibil la abuz; deși nu este adresat direct în proiect, RFC-ul ilustrează structurarea unui protocol, utilă când interpretăm payload-urile – referință opțională pentru detalii de implementare protocolară)
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


### 📁 `07roWSL/` — Interceptarea și Filtrarea Pachetelor

**Ce găsești relevant:**
- Captură și analiză pachete cu Scapy/tshark

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `13roWSL/` — IoT și Securitate

**Ce găsești relevant:**
- Detectarea intruziunilor, pattern matching

**Fișiere recomandate:**
- `13roWSL/README.md` — prezentare generală și pași de laborator
- `13roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `13roWSL/docs/fisa_comenzi.md` — comenzi utile
- `13roWSL/src/` — exemple de cod Python
- `13roWSL/homework/` — exerciții similare


### 📁 `04roWSL/` — Protocoale Personalizate

**Ce găsești relevant:**
- Parsarea header-elor, struct module

**Fișiere recomandate:**
- `04roWSL/README.md` — prezentare generală și pași de laborator
- `04roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `04roWSL/docs/fisa_comenzi.md` — comenzi utile
- `04roWSL/src/` — exemple de cod Python
- `04roWSL/homework/` — exerciții similare


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
