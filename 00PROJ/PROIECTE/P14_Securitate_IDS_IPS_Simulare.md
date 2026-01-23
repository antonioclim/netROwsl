# Proiectul 14: Securitatea rețelelor – simularea unui sistem de detecție a intruziunilor (IDS/IPS)

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
https://github.com/[username]/retele-proiect-14
```

#### Structura obligatorie a repository-ului

```
retele-proiect-14/
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

**Format:** `NUME_Prenume_GGGG_P14_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P14 | Numărul proiectului | P14 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P14_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P14_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P14_S07.zip` — Verificare săptămâna 7

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

Descriere: Proiectul abordează o temă critică din securitatea rețelelor: detectarea și prevenirea intruziunilor. Studenții vor proiecta și implementa un mediu de rețea virtual (folosind instrumente precum mașini virtuale, containere Docker sau chiar Mininet) în care vor configura un Sistem de Detecție a Intruziunilor (IDS) de tip rețea, de exemplu Snort sau Suricata, și vor simula diverse atacuri cibernetice pentru a testa capacitatea sistemului de a le detecta și, opțional, bloca. Rețeaua de test ar putea consta într-un segment protejat (o mașină victimă care găzduiește un serviciu vulnerabil – de exemplu un server web intenționat neactualizat) și un segment extern de pe care se lansează atacurile (o mașină attackera). IDS-ul va fi plasat fie ca sondă de monitorizare a traficului (conectat la un port mirroring al unui switch virtual, sau în modul inline dacă se dorește și prevenție). Scenariile de atac simulate pot include: scanări de porturi (folosind nmap), atacuri de tip DoS simple (ping flood), încercări de exploatare a unor vulnerabilități cunoscute (ex: un SQL injection sau un buffer overflow pentru care există semnături Snort), sau acces neautorizat (bruteforce pe SSH, etc.). Studenții vor configura regulile IDS astfel încât acesta să alerteze la detectarea acestor activități suspecte. De exemplu, pot fi folosite seturile de reguli default (Emerging Threats) și/sau pot scrie reguli personalizate Snort pentru anumite tipare de trafic. Pentru partea de prevenție (IPS), dacă este abordată, se poate activa modul inline al Snort/Suguri care blochează pachetele malițioase (sau, mai simplu, scripturi care adaugă dynamic firewall rules – iptables – când IDS semnalează un atac). Proiectul are o componentă aplicativă foarte puternică: studenții vor învăța practic cum se instalează și configurează un IDS open-source, cum se interpretează alertele generate și cum se pot corela aceste alerte cu acțiunile unui atacator. Se pune accent și pe metodologie – de exemplu, rularea unor teste controlate pentru a “înscrie” amprenta unui atac în trafic și a verifica dacă sistemul o recunoaște. Din punct de vedere pedagogic, proiectul consolidează cunoștințele de securitate rețea prin experimentare directă, evidențiind atât beneficiile utilizării IDS (vizibilitate sporită asupra traficului și atacurilor) cât și limitările acestora (alerte fals pozitive, incapacitatea de a detecta atacuri necunoscute etc.). La final, echipa va prezenta rezultatele sub forma unui raport de securitate ce sumarizează atacurile încercate și modul în care au fost (sau nu) detectate și blocate.

### 🎯 Obiective de învățare


### 📖 Concepte cheie

Tehnologii implicate: Distribuții Linux (ex: Ubuntu) pentru instalarea instrumentelor de securitate; Snort 2.x sau 3.x (sau Suricata) ca motor IDS – cu actualizarea regulilor de la comunitatea Emerging Threats; Wireshark pentru analiza detaliată a traficului la nivel de pachet; Nmap pentru scanări de porturi și recunoaștere; eventual Metasploit sau exploit-uri dedicate pentru a genera trafic malițios (dacă se dorește simularea unui atac specific); Scapy (bibliotecă Python) sau hping3 pentru a fabrica pachete custom, utile în testarea anumitor semnături; Docker sau Mașini Virtuale (VirtualBox/VMware) pentru a crea medii izolate (de exemplu un container rulând Snort care monitorizează rețeaua host-ului, etc.); scripturi Bash/Python pentru automatizarea testelor (ex: trimiterea unui val de pachete și observarea reacției IDS). Se poate utiliza și Mininet pentru a construi rapid o topologie virtuală (de ex. host1 = atacator, host2 = server, cu un switch central și IDS conectat pasiv la switch prin port mirroring – Mininet suportă astfel de configurări).
Legătura cu săptămânile și kiturile (WEEK1-14): Proiectul este ancorat în materia din săptămâna 13, dedicată securității rețelelor, unde au fost discutate concepte de scanare de porturi, vulnerabilități și unelte de securitate. Kitul practic al săptămânii 13 probabil conține exerciții introductive cu nmap și poate exemple de output de la Snort, oferind studenților punctul de plecare pentru propriile experimente. Proiectul se bazează pe cunoștințe din săptămâna 7 (interceptarea pachetelor, implementarea unui filtru de pachete) – care oferă fundamentele privind structurarea pachetelor și modul de filtrare, elemente direct relevante pentru definirea regulilor IDS. Noțiunile din primele săptămâni referitoare la protocoalele de rețea (IP, TCP, UDP – săptămânile 3-5) sunt indispensabile pentru a înțelege vectorii de atac (de exemplu, ce înseamnă un TCP SYN flood sau un scan FIN). Proiectul vine ca o încununare a acestor cunoștințe, aplicându-le într-un context practic de securitate, și pregătește studenții să coreleze aspectele teoretice de rețea cu probleme reale din industrie (securizarea infrastructurii).
Structura proiectului în 4 etape: - Etapa 1 (săptămâna 5): Proiectarea mediului de test și pregătirea infrastructurii. Echipa va decide ce topologie de rețea și ce scenarii de atac să abordeze. Se stabilește, de exemplu: un server victimă (ce serviciu rulează, pe ce porturi), tipurile de atacuri ce vor fi simulate și unde va fi plasat IDS-ul. Totodată, se alege platforma: VM-uri separate (ex: o VM Kali Linux ca atacator, o VM Ubuntu ca server+IDS) sau containere pe aceeași mașină. În această etapă, studenții instalează efectiv software-ul necesar – de exemplu, instalarea Snort și a dependențelor sale, obținerea fișierelor de reguli default. Se realizează un test inițial al IDS-ului într-un mediu simplificat: rularea Snort în modul sniffer pentru a vedea că poate capta trafic sau rularea unei comenzi snort -T pentru a verifica sintaxa configurației. Tot acum, se documentează planul de atac: ce comenzi vor fi folosite pentru port scan, ce exploit (dacă e cazul) va fi încercat etc., asigurându-se că sunt disponibile instrumentele respective (instalare nmap, etc.). - Etapa 2 (săptămâna 9): Executarea primelor teste de intruziune și calibrarea sistemului IDS. Până la acest moment, echipa va fi configurat IDS-ul în rețeaua de test și va începe să lanseze atacuri simple pentru a genera alerte. De exemplu, se poate porni Snort în modul IDS cu un set de reguli de bază și se lansează un scan de porturi intens de pe mașina atacator (nmap -T4 -p- VictimIP). Se observă dacă Snort generează alertă (“Nmap scan detected” sau similar). Dacă nu, studenții analizează de ce – poate regula nu era activă, sau traficul nu ajungea la Snort – și fac ajustări (activează toate regulile relevante, se asigură că Snort ascultă pe interfața corectă). Se continuă cu alte atacuri de bază: un ping flood (folosind ping -f sau hping3) pentru DoS și eventual un mic atac web (dacă serverul victimă e un web server, se pot trimite cereri conținând cunoscute string-uri de atac XSS/SQLi). La fiecare pas, se vor colecta alertele și se va verifica corelația lor cu acțiunile întreprinse. Etapa 2 are rolul de tunare: echipa va ajusta sensibilitatea sistemului (eliminarea unor reguli care provoacă false pozitive irelevante pentru test, modificarea priorităților etc.) astfel încât mediul de test să fie pregătit pentru scenariile complexe. - Etapa 3 (săptămâna 13): Scenarii avansate de atac și implementarea contramăsurilor. În această etapă finală de dezvoltare, se derulează testele complexe planificate. De pildă, se poate simula un atac de tip Brute Force asupra serviciului SSH al victimei (folosind un tool ca hydra sau medusa pentru a încerca multiple parole) – Snort ar trebui să emită alerte de tip “Multiple login failures” dacă are regula corespunzătoare. Un alt scenariu ar fi utilizarea unui exploit real: dacă victima are un serviciu vulnerabil cunoscut (ex. DVWA – Damn Vulnerable Web App, sau un vsftpd backdoor), se lansează exploit-ul și se vede dacă IDS-ul îl detectează (multe IDS au semnături pentru exploit-uri populare). Pentru prevenție, se poate activa Snort în modul inline (dacă topologia permite) sau, mai simplu, echipa poate crea un script integrat cu log-urile Snort: de exemplu, un script Python/Bash care rulează continuu, parsează fișierul de alerte și când vede o alertă critică (ex: “ATTACK DETECTED from X”) adaugă imediat o regulă iptables de blocare a IP-ului sursă X. Astfel, se demonstrează acțiunea de IPS. Toate aceste scenarii sunt rulate de câteva ori pentru a aduna date: log-urile Snort (alerte declanșate, timestamp-uri), comportamentul sistemului (ex: serverul a blocat efectiv atacatorul după declanșarea IPS). Studenții vor aduna și statistici agregate, de exemplu număr de alerte per tip de atac, rata de succes a detecției. Totodată, vor verifica dacă au existat atacuri “scăpate” nedetectate și vor nota posibile motive (poate lipsa unei semnături sau trafic criptat pe care Snort nu îl poate inspecta). - Etapa 4 (prezentarea în săptămâna 14): Prezentarea finală va avea forma unui raport de securitate și a unei demonstrații practice. În raport, echipa va descrie pe scurt configurarea mediului (topologia, versiunea de Snort/Suricata, tipuri de reguli activate, eventuale personalizări făcute) și va lista scenariile de atac testate, împreună cu capturi de ecran sau extrase din log-uri care arată detecția. De exemplu, pentru un port scan se poate include alerta Snort generată (cu ID-ul semnăturii), pentru un exploit web se poate arăta log-ul cu payload-ul detectat. Se va discuta eficacitatea: care atacuri au fost imediat detectate, care au necesitat ajustări, dacă au existat alarme false (de exemplu, Snort ar putea marca un trafic legitim ca suspect – studenții vor menționa dacă au întâlnit astfel de situații și cum le-au mitigat). În cadrul demonstrației live, echipa poate relua unul dintre atacurile emblematice (de pildă un portscan sau un DoS mic) și arăta audienței cum apare alerta în consola IDS sau cum IP-ul atacator este blocat automat de firewall (dacă au IPS). Prezentarea se va încheia cu concluzii privind utilitatea practicii: studenții vor reflecta asupra faptului că un IDS oferă un nivel crucial de vizibilitate în rețea[4], dar că administrarea lui necesită finețe (tunarea regulilor, actualizarea constantă a semnăturilor). Ei pot sugera și lucrări viitoare, de exemplu integrarea cu un sistem SIEM sau testarea pe trafic criptat (TLS), arătând astfel o înțelegere matură a subiectului.

### 🔮 VERIFICARE ÎNȚELEGERE - CONCEPTE REȚEA

Înainte de configurare, verificați că înțelegeți:

1. Ce tip de adresă este 192.168.1.50?
   → Adresă privată (RFC 1918), nu poate fi rutată direct pe Internet

2. Câte adrese IP utilizabile sunt într-o rețea /24?
   → 254 adrese (256 total minus 1 pentru rețea minus 1 pentru broadcast)

3. Ce rol are NAT în rețeaua voastră?
   → Traduce adresele IP private în adresa publică pentru acces Internet


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


### Extensii pentru echipe de 3 vs. 2/1 membri: O echipă de 3 studenți poate explora în profunzime aspecte suplimentare de securitate. De exemplu, pot implementa un sistem hibrid IDS (rețea + host-based): pe lângă Snort, să configureze și OSSEC sau Wazuh (IDS la nivel de gazdă) pe serverul victimă, corelând alertele ambelor sisteme pentru o imagine mai cuprinzătoare. Sau pot configura Suricata în paralel cu Snort pentru a compara detecția (analizând diferențele de alerte generate de cele două motoare pe același trafic). În plus, echipele mai mari pot extinde gama atacurilor testate – de exemplu includerea unui atac de tip Man-in-the-Middle (cu ARP poisoning în Mininet, de exemplu) sau un malware beaconing (simulat) pentru a vedea dacă IDS-ul detectează comunicații anormale. Pentru echipele de 2 studenți, setul de atacuri poate fi mai restrâns (se pot concentra pe 2-3 tipuri principale, cum ar fi portscan, DoS, exploit). Configurațiile pot fi simplificate, de pildă rulând totul pe o singură mașină cu Snort ascultând pe interfața loopback (limitat dar suficient pentru a demonstra conceptul). Chiar și doar cu Snort și fără partea de IPS, studenții în echipă mică pot obține un proiect reușit dacă demonstrează câteva detecții corecte și prezintă o înțelegere solidă a motivelor tehnice. Pentru un singur student, proiectul ar putea fi limitat la folosirea exclusiv a setului de reguli predefinite și simularea unor atacuri foarte clare (ex: folosirea traficului din kitul de laborator sau PCAP-uri cunoscute în loc de generarea manuală). Indiferent de mărimea echipei, se va aprecia calitatea interpretării rezultatelor și modul sistematic în care au fost abordați pașii de testare.


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


### 📁 `13roWSL/` — Securitate

**Ce găsești relevant:**
- Snort/Suricata, reguli de detecție

**Fișiere recomandate:**
- `13roWSL/README.md` — prezentare generală și pași de laborator
- `13roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `13roWSL/docs/fisa_comenzi.md` — comenzi utile
- `13roWSL/src/` — exemple de cod Python
- `13roWSL/homework/` — exerciții similare


### 📁 `07roWSL/` — Interceptare Pachete

**Ce găsești relevant:**
- Captură trafic, analiza pattern-urilor

**Fișiere recomandate:**
- `07roWSL/README.md` — prezentare generală și pași de laborator
- `07roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `07roWSL/docs/fisa_comenzi.md` — comenzi utile
- `07roWSL/src/` — exemple de cod Python
- `07roWSL/homework/` — exerciții similare


### 📁 `04roWSL/` — Protocoale Custom

**Ce găsești relevant:**
- Parsarea payload-urilor pentru detecție

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
