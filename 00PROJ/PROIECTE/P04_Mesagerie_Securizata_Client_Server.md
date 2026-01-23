# Proiectul 04: Aplicație de mesagerie securizată client-server

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
https://github.com/[username]/retele-proiect-04
```

#### Structura obligatorie a repository-ului

```
retele-proiect-04/
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

**Format:** `NUME_Prenume_GGGG_P04_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P04 | Numărul proiectului | P04 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P04_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P04_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P04_S07.zip` — Verificare săptămâna 7

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
În acest proiect, studenții vor dezvolta o aplicație de chat client-server criptată, punând accent pe securizarea comunicațiilor în rețea. Practic, se va implementa un server de mesagerie multi-client și un client de chat, folosind Python (sau alt limbaj de nivel înalt), care comunică peste TCP. Spre deosebire de aplicațiile de chat simple, proiectul de față va integra mecanisme de criptare end-to-end sau pe canal, asigurând confidențialitatea mesajelor transmise. Inițial, aplicația poate funcționa în mod text (consolă) – utilizatorii se conectează la server și pot trimite mesaje text care sunt distribuite celorlalți (chat în grup simplu) sau direct către un alt utilizator (chat privat), în funcție de specificațiile echipei.
Pentru securitate, se poate folosi fie criptografie simetrică (ex: algoritmul AES cu o cheie pre-partajată între client și server) fie o abordare cu criptografie asimetrică (ex: serverul are o cheie publică/privată RSA; clienții negociază o cheie de sesiune, similar cu un handshake TLS simplificat). Un design fezabil este implementarea unui protocol simplu de tip SSL: la conectare, clientul preia certificatul public al serverului (auto-semnat, generat în prealabil) și îl folosește pentru a trimite în siguranță o cheie simetrică random (cheia de sesiune). Ulterior, toate mesajele client-server sunt criptate simetric cu acea cheie. Serverul, având cheia privată pentru a descifra cheia de sesiune, poate apoi citi mesajele și le poate retransmite altor clienți, eventual recriptând pe canalul cu fiecare destinatar. Alternativ, pentru simplitate, toți participanții pot folosi aceeași cheie simetrică (pre-definită în cod) – mai puțin sigur, dar mai ușor de implementat, adecvat pentru a demonstra conceptul.
Proiectul implică așadar atât dezvoltarea funcționalităților de bază ale unui chat (gestionarea conexiunilor multiple, transmiterea și afișarea mesajelor în timp real), cât și integrarea bibliotecilor de criptografie (cum ar fi ssl din Python sau biblioteci precum PyCryptodome) pentru a asigura că mesajele sunt inteligibile doar pentru părțile autorizate. Se vor realiza teste într-o rețea locală (sau pe același calculator, cu mai multe instanțe de client) pentru a verifica că mesajele interceptate (de exemplu, cu Wireshark) apar criptate și nu în clar. Acest proiect oferă o introducere practică în protocoalele de securitate și evidențiază importanța criptării datelor transmise peste rețea.

### 🎯 Obiective de învățare

Consolidarea cunoștințelor de programare a socket-urilor în model client-server, gestionând concomitent comunicarea cu mai mulți clienți (ex. folosind fire de execuție sau mecanisme de multiplexare I/O).
Însușirea principiilor de bază ale criptografiei aplicate în rețele: criptare simetrică vs. asimetrică, schimb de chei, certificate, și modul de integrare a acestora într-un protocol de comunicație.
Înțelegerea noțiunilor de confidențialitate și integritate a datelor transmise prin rețea și a riscurilor atunci când acestea lipsesc (ex: interceptarea traficului în clar).
Dezvoltarea unei mici convenții de protocol personalizat (stabilirea formatului mesajelor, eventual comenzi precum "/login", "/list" pentru listarea utilizatorilor, etc.) și respectarea acestei specificații în implementare.

### 🛠️ Tehnologii și unelte


### 📖 Concepte cheie

Modelul Client-Server – conexiune TCP persistentă, rolul serverului de releu între clienți, concurență (threads sau async) pentru a servi mai multe conexiuni simultan.
Protocoale criptografice – schimbul de chei, criptare simetrică (ex: AES CBC/GCM), criptare asimetrică (RSA) și utilizarea lor combinată (precum în TLS).
Managementul cheilor – generarea și distribuția cheii de criptare, stocarea în siguranță a cheilor private, eventual folosirea certificatelor digitale.
Integritatea mesajelor – opțional, se poate discuta/adăuga calculul unui MAC (HMAC) pentru fiecare mesaj, pentru a asigura integritatea și autenticitatea (dar dacă se folosește un mod autenticat de criptare precum AES-GCM, integritatea e asigurată implicit).
Aplicații de nivel transport – cum se delimitează mesajele într-un flux TCP (folosirea unui protocol text cu terminator de linie sau a unui protocol binar cu length-prefix), gestiunea erorilor de rețea, reconectarea clienților etc.
Tehnologii implicate
Python – limbaj ideal pentru prototipare rapidă: utilizarea modulului socket pentru comunicații TCP, modulelor threading sau asyncio pentru concurență, și biblioteca ssl sau PyCryptodome pentru funcții criptografice.
Biblioteci de criptografie – de exemplu ssl (poate fi folosit pentru a îmbrăca un socket existent într-un context SSL simplificat), sau PyCryptodome pentru implementarea manuală a algoritmilor (AES, RSA).
OpenSSL – se poate folosi pentru a genera cheia privată și certificatul autosigiliat al serverului (folosit dacă se implementează varianta cu RSA). De exemplu, comanda openssl genrsa și openssl req -x509 pentru a obține un certificat .pem pe care serverul îl încarcă.
Wireshark – pentru testarea securității: prin capturarea pachetelor se va verifica dacă textul mesajelor nu apare în clar. Dacă se configurează Wireshark cu cheia privată a serverului (în variantă RSA), se poate tenta decriptarea traficului pentru a confirma că numai cu cheia corespunzătoare se poate citi conținutul.
Protocol propriu – definirea unui format, de exemplu JSON peste TCP (fiecare mesaj JSON conține câmpuri "user", "msg", "timestamp", criptate ca text) sau un protocol text simplu (linie de text per mesaj, criptată la nivel de flux).
Legătura cu temele din săptămânile cursului
Săptămâna 7: Protocolul TCP – aplicația de chat folosește TCP pentru transport fiabil; cunoștințele despre conexiuni, porturi, segmentare și reasamblare (din curs) sunt aplicate direct.
Săptămâna 8: Protocoale de aplicație – se leagă de subiectul protocoalelor de nivel înalt: aici definim practic un mini-protocol de chat. Totodată, conceptul de protocol securizat (similar relației HTTP-HTTPS, aici chat vs. chat securizat) extinde discuția din curs privind securizarea protocolelor de aplicație.
Săptămâna 9: Securitate – proiectul este o aplicație practică a criptografiei în rețea, completând teoria din curs (ex: dacă în Week9 s-a discutat despre TLS/SSL, certificate, criptografie, proiectul exemplifică aceste lucruri).
Săptămâna 12: Programare de rețea – baza codului de chat necriptat este direct inspirată din exemplele de socket programming din laboratorul săptămânii 12 (vezi „Chat server Python” din arhiva WEEK12), peste care se adaugă partea de criptare.
Etapele proiectului

### 📋 Etapa 1 (Săptămâna 5) – Proiectarea protocolului și a funcționalităților: Stabilirea caracteristicilor aplicației: va fi chat de grup sau privat? Cum se vor identifica utilizatorii (ex: printr-un nume de utilizator trimis la conectare)? Ce algoritmi de criptare se vor folosi și cum vor fi gestionați cheile? Se va întocmi un mini-schelet de protocol descriind pașii de inițializare (ex: Client -> Server: salut + nume user; Server -> Client: confirmare + certificatul public; Client -> Server: cheie de sesiune criptată etc.) și formatul mesajelor ulterioare. Livrabil: un document de design care include diagrama de flux a protocolului de comunicare (atât partea de autentificare/cripto inițială, cât și fluxul de mesaje de chat), plus detalii despre alegerea algoritmilor (de exemplu, “vom folosi AES-256-CBC cu o cheie simetrică de 32 bytes generată aleator de client la fiecare sesiune” sau alt plan). Se vor alege librăriile și se va pregăti mediul (instalarea PyCryptodome dacă e necesar). Opțional, se poate livra și generarea cheilor/certificatelor necesare (un fișier PEM cu cheia privată a serverului și certificatul public autosemis).


### 🔨 Etapa 2 (Săptămâna 9) – Implementare bază (chat necriptat): Ca prim pas, se implementează chat-ul propriu-zis fără criptare, pentru a asigura că logica de rețea funcționează corect. Serverul trebuie să accepte conexiuni multiple (thread pe conexiune sau un mecanism asincron) și să retransmită mesajele primite de la un client către toți ceilalți (sau către destinatarii vizați, dacă se suportă mesaje private). Clientul trebuie să citească de la tastatură mesaje și să le trimită serverului, afișând în același timp mesajele primite de la alții. Livrabil: codul sursă al serverului și al clientului (posibil într-o formă simplă, ex. rulare în consolă) care permite deja comunicarea tip chat. Se vor furniza capturi de ecran sau log-uri ce demonstrează 2-3 clienți trimițând mesaje unii altora prin intermediul serverului. În această etapă, mesajele sunt în clar, deci e util pentru testare să se confirme că toată lumea primește corect mesajele.


### 🔮 VERIFICARE ÎNȚELEGERE - SOCKET-URI TCP

Înainte de a rula serverul, răspundeți:

1. Ce se întâmplă dacă portul specificat este deja ocupat?
   → Eroare: Address already in use
   → Soluție: folosiți SO_REUSEADDR sau alegeți alt port

2. Câte conexiuni poate gestiona serverul simultan?
   → Depinde de parametrul backlog din listen() și de implementarea cu thread-uri

3. Ce se întâmplă când un client se deconectează brusc?
   → Serverul primește 0 bytes la recv() sau excepție ConnectionResetError


### ✅ Etapa 3 (Săptămâna 13) – Implementare securitate și testare completă: Se integrează mecanismele de criptare proiectate în Etapa 1. Pentru varianta cu cheie simetrică comună, asta înseamnă că atât serverul cât și clienții includ acea cheie și o folosesc pentru a cifra/decifra mesajele. Pentru varianta mai complexă cu chei publice, se implementează pasul de handshake: serverul încarcă cheia sa privată și trimite clienților cheia publică (sau certificatul); clientul generează o cheie simetrică random, o criptează cu cheia publică a serverului și o trimite; serverul o decodifică cu cheia privată. După acest schimb, se folosește respectiva cheie simetrică de sesiune pentru a cifra tot traficul ulterior. Se vor folosi moduri de criptare sigure (ex: AES-GCM care oferă și integritate). Odată criptarea adăugată, se retestează scenariile: clienții trebuie să poată comunica ca înainte, transparent (criptarea/decriptarea fiind internă). Se verifică cu Wireshark că datele brute pe rețea nu mai sunt lizibile. Livrabil: codul final al aplicației (server și client) documentat, plus un manual scurt de utilizare (cum se generează cheile, cum se pornește serverul, cum se pornesc clienții, ce dependențe sunt necesare). Totodată, un raport final ce include capturi Wireshark (sau alt output) demonstrând că un mesaj “Hello” trimis de un client apare ca text cifrat pe rețea, și doar aplicația de pe celălalt capăt îl afișează corect în clar. Raportul va discuta și nivelul de securitate obținut (ex: dacă s-a folosit cheie comună hardcodată, se va menționa că nu e recomandat în producție, etc.).


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


### 🎤 Etapa 4 (Săptămâna 14) – Prezentare finală: Se prezintă arhitectura aplicației (modul în care clientul și serverul interacționează, eventual un exemplu de mesaj criptat vs decriptat). Demonstrația live poate consta în rularea unui server și a doi clienți: se trimit mesaje între clienți, arătând că acestea apar criptate într-un output Wireshark. Opțional, se poate demonstra ce se întâmplă dacă un client neautorizat (care nu cunoaște cheia) încearcă să se alăture – ideal, nu poate comunica inteligibil. Se evidențiază astfel importanța distribuției de chei. Livrabil: slide-uri și demonstrația practică, cu explicații despre implementare și despre cum s-ar putea extinde (ex: pentru autentificare de utilizator, pentru interfață grafică etc.).

Extensii posibile pentru echipe de 3 vs. 2/1 studenți
Echipele de 3 studenți pot aborda facilități suplimentare ce adaugă complexitate: de exemplu, implementarea unei autentificări a utilizatorilor cu parolă (serverul verifică parole și transmite cheia de criptare numai după autentificare, oferind confidențialitate doar utilizatorilor legitimi) sau adăugarea unei interfețe grafice (folosind Tkinter sau PyQt pentru a face aplicația mai user-friendly decât consola). O altă extindere ar fi suportul pentru mesaje offline sau stocarea în siguranță a mesajelor (criptate) pe server. Echipa extinsă ar putea implementa nu doar confidențialitate, ci și integritate și autentificare end-to-end – adică fiecare mesaj să fie semnat digital de expeditor (folosind chei private per client) astfel încât destinatarii să poată verifica sursa.
Echipele mai mici (2 sau 1 student) pot simplifica proiectul prin alegerea unor metode mai ușoare de criptare: de pildă, pot folosi direct modulul ssl din Python pentru a crea un wrap SSL în jurul socket-urilor, evitând implementarea manuală a schimbului de chei (practic, folosind biblioteca pentru a face un tunel TLS – deși mai puțin didactic, e mai simplu din punct de vedere al codului). Dacă și asta e dificil, pot opta pentru o cheie simetrică fixă cunoscută de ambele părți, concentrându-se pe implementarea criptării/decriptării mesajelor cu acea cheie. În plus, echipa mică poate limita funcționalitatea la chat de grup (fără mesaje private sau alte comenzi speciale) pentru a reduce volumul de cod de gestionare a logicii aplicației.

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

Paar, C., & Pelzl, J. (2010). Understanding Cryptography: A Textbook for Students and Practitioners. Springer. (Capitolele despre AES și RSA oferă fundamentele teoretice folosite în proiect)
Nagpal, D. (2018). Building Network Security Tools. Packt Publishing. (Include studii de caz practice privind crearea de aplicații sigure de rețea în Python, cu exemple de chat securizat și utilizare a PyCryptodome)
Rescorla, E. (2001). SSL and TLS: Designing and Building Secure Systems. Addison-Wesley. (Deși dedicată TLS, cartea explică pașii unui handshake și componentele securității unui canal de comunicare – sursă de inspirație pentru protocolul proiectului)
PyCryptodome Documentation – PyCryptodome Library Documentation. (2022). Disponibil la: https://pycryptodome.readthedocs.io (Manualul oficial al bibliotecii de criptografie în Python, cu exemple de utilizare a algoritmilor simetrici și asimetrici)
Stallings, W. (2017). Cryptography and Network Security: Principles and Practice (7th ed.). Pearson. (Oferă context academic despre protocoalele de securitate și algoritmi; util pentru înțelegerea de ansamblu a soluției implementate)
---

## 🔮 Verificare înțelegere — Socket-uri TCP

Înainte de a rula serverul:

1. **Ce se întâmplă dacă portul e ocupat?**
   - Eroare: "Address already in use"
   - Soluție: `SO_REUSEADDR` sau alt port

2. **Câte conexiuni poate accepta serverul?**
   - Depinde de `listen()` și threading

3. **Ce se întâmplă când un client se deconectează brusc?**
   - `recv()` returnează 0 bytes sau excepție `ConnectionResetError`


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


### 📁 `02roWSL/` — Programare Socket

**Ce găsești relevant:**
- TCP sockets, client-server concurent

**Fișiere recomandate:**
- `02roWSL/README.md` — prezentare generală și pași de laborator
- `02roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `02roWSL/docs/fisa_comenzi.md` — comenzi utile
- `02roWSL/src/` — exemple de cod Python
- `02roWSL/homework/` — exerciții similare


### 📁 `09roWSL/` — Nivelul Sesiune și Prezentare

**Ce găsești relevant:**
- Criptare, autentificare, sesiuni

**Fișiere recomandate:**
- `09roWSL/README.md` — prezentare generală și pași de laborator
- `09roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `09roWSL/docs/fisa_comenzi.md` — comenzi utile
- `09roWSL/src/` — exemple de cod Python
- `09roWSL/homework/` — exerciții similare


### 📁 `03roWSL/` — Broadcast și Multicast

**Ce găsești relevant:**
- Grupuri de utilizatori, mesaje de grup

**Fișiere recomandate:**
- `03roWSL/README.md` — prezentare generală și pași de laborator
- `03roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `03roWSL/docs/fisa_comenzi.md` — comenzi utile
- `03roWSL/src/` — exemple de cod Python
- `03roWSL/homework/` — exerciții similare


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
