# Proiectul 15: Simularea unei rețele IoT cu procesare de tip Edge Computing

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
https://github.com/[username]/retele-proiect-15
```

#### Structura obligatorie a repository-ului

```
retele-proiect-15/
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

**Format:** `NUME_Prenume_GGGG_P15_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P15 | Numărul proiectului | P15 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P15_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P15_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P15_S07.zip` — Verificare săptămâna 7

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

Descriere: Acest proiect explorează domeniul emergent al Internetului Lucrurilor (IoT) și al procesării la marginea rețelei (Edge Computing) prin realizarea unei simulări a unei rețele de dispozitive inteligente conectate. Scopul este construirea unui mediu în care multiple “dispozitive” IoT (simulate software) colectează și transmit date către un nod central de tip edge (gateway local), care realizează prelucrări primare ale datelor și le trimite mai departe către un serviciu de cloud (simulat) pentru stocare sau analiză aprofundată. În termeni practici, studenții vor implementa un set de noduri senzori (de exemplu, simulând citiri de temperatură, umiditate, mișcare sau alți parametri) care se conectează prin rețea la un broker de mesaje IoT (precum MQTT broker – de exemplu Eclipse Mosquitto). Dispozitivele vor publica periodic datele colectate pe anumite topici MQTT, în timp ce nodul edge (un subsistem local, posibil un mini-server) va acționa ca abonat la aceste topici, agregând informațiile de la senzori. Acest edge server poate efectua calcul local – de exemplu, filtrarea datelor (eliminarea anomaliilor), combinarea valorilor de la mai mulți senzori sau declanșarea unor alerte dacă valorile depășesc praguri – demonstrând avantajul edge computing: reducerea volumului de date trimis spre cloud și răspuns mai rapid la evenimente locale. Datele prelucrate sumar de edge vor fi apoi transmise către un serviciu central (cloud) pentru arhivare sau analiza globală (în practică ar putea fi o bază de date centrală sau un dashboard web; în simulare, poate fi un alt proces care primește aceste date). Comunicarea dintre edge și cloud se poate face tot printr-un protocol standard (MQTT, HTTP REST API, etc.). Proiectul pune accent pe aspectele de rețea și protocoale specifice IoT: comunicare publish-subscribe, gestionarea unui număr potențial mare de dispozitive, limitări de lățime de bandă și latență, formatele ușoare de mesaje (JSON, CBOR). Totodată, aspecte de securitate pot fi abordate – autentificarea dispozitivelor la broker, transmisia criptată TLS (dacă timpul permite). Pedagogic, studenții vor înțelege modul în care IoT extinde conceptul de rețea la miliarde de dispozitive fizice și necesită arhitecturi diferite (de ex. edge computing) pentru a face față volumului de date și constrângerilor de timp real. Simularea realizată va oferi oportunitatea de a observa comportamentul rețelei IoT în diferite condiții: de exemplu, ce se întâmplă dacă un senzor “cade” (nu mai transmite), dacă latența rețelei crește sau dacă brokerul se aglomerează cu mesaje. Studenții vor putea experimenta și optimizări precum reglarea frecvenței de eșantionare a senzorilor sau folosirea unor mecanisme de buffering la edge.

### 🎯 Obiective de învățare


### 📖 Concepte cheie


### 🛠️ Tehnologii și unelte

Legătura cu săptămânile și kiturile (WEEK1-14): Deși subiectul IoT nu apare explicit în programa primelor 13 săptămâni, proiectul se bazează pe principiile generale de rețele predate de-a lungul cursului și le aplică într-un context modern. În special, conceptul de arhitectură distribuită din săptămâna 12 (RPC și comunicarea inter-proces) este extins aici sub altă formă (comunicare publish-subscribe). De asemenea, săptămâna 8 privind protocoalele la nivel de aplicație (HTTP, arhitecturi client-server) oferă un contrast față de modelul pub-sub utilizat în MQTT – studenții vor putea compara cele două paradigme. Tematica de securitate din săptămâna 13 se leagă de proiect prin discuțiile de securitate IoT (IoT aduce probleme speciale de securitate, cum ar fi dispozitive slab protejate, comunicații necriptate, etc., ce pot fi amintite în proiect). Chiar și aspecte din săptămâna 5-6 (rutare, adresare) sunt relevante: într-o rețea IoT, alocarea adreselor IP (posibil IPv6 pentru număr mare de dispozitive) și rutarea eficientă (protocole specifice rețelelor de senzori, cum ar fi RPL) sunt subiecte de interes – acestea pot fi menționate teoretic. Prin urmare, proiectul funcționează ca o sinteză și aplicație practică integratoare, demonstrând aplicarea conceptelor de rețea într-un scenariu actual de IoT, chiar dacă nu a fost detaliat la curs – abordarea fiind conformă cu obiectivele disciplinei de a conecta cunoștințele la tendințele recente.
Structura proiectului în 4 etape: - Etapa 1 (săptămâna 5): Definirea scenariului IoT și a arhitecturii de sistem. Echipa stabilește contextul: de exemplu, “monitorizarea inteligentă a clădirilor” cu senzori de temperatură și mișcare pe fiecare etaj, sau “agricultură smart” cu senzori de umiditate în sol și temperatură aer transmițând date la un nod edge aflat la fermă care decide irigarea, etc. Se delimitează clar ce tipuri de senzori vor fi simulați și ce fel de date vor transmite (inclusiv unități, interval de valori). Apoi se schițează arhitectura: câți senzori (procese) vor exista, ce broker se folosește, ce face nodul edge cu datele, cum transmite mai departe la cloud. Se va alege protocolul de comunicare – cel mai probabil MQTT pentru senzor->edge și tot MQTT sau HTTP pentru edge->cloud. În această etapă se pregătesc și mediile: instalarea broker-ului MQTT (Mosquitto) local sau într-un container Docker, testarea lui minimală (ex: se încearcă o subscriere și o publicare manual, cu utilitare mosquitto_pub și mosquitto_sub). Se documentează formatul mesajelor ce vor fi transmise (e.g., JSON: { sensor_id: "S1", value: 23.5, unit: "C" }). - Etapa 2 (săptămâna 9): Implementarea prototipurilor pentru senzori și nodul edge – flux simplu de date. Până la sfârșitul acestei etape, studenții vor realiza un prim sistem funcțional simplificat: de exemplu, un singur senzor scriptat în Python care publică date fictive către broker și nodul edge care primește aceste date și le afișează sau loghează. Se testează comunicarea publish-subscribe end-to-end. Tot acum se implementează și partea de trimitere către “cloud” a datelor de la edge (chiar dacă inițial cloud-ul poate fi doar un log pe disc). Accentul este pe a valida că toate componentele pot comunica: senzor -> broker (mesaj publicat corect și recepționat de edge) -> edge -> (eventual HTTP POST) -> cloud. Dacă se folosesc multiple subiecte, se verifică că edge-ul se abonează la toate cele necesare. Se pot folosi date de test generate simplu (ex: valori random pentru senzori) doar pentru a exercita sistemul. La acest stadiu, se pot identifica și eventuale probleme de configurare (de exemplu, mărimea maximă a mesajelor MQTT, sau time-out la client) și se rezolvă. - Etapa 3 (săptămâna 13): Extinderea simulării la mai multe dispozitive, introducerea procesării edge și evaluarea performanței. Aceasta este etapa de realizare integrală a scenariului. Se lansează multipli senzori – de exemplu, se generalizează scriptul de senzor astfel încât prin parametri diferiți (sau instanțe diferite) să reprezinte senzori diferiți (poate chiar de tipuri diferite: temperatură, umiditate, etc.). Se configurează un interval de publicare realist (ex: la fiecare 5 secunde un senzor trimite o valoare). Nodul edge devine mai inteligent: se implementează logica de agregare/filtrare – de pildă, calculul mediei temperaturilor din ultimele N citiri pentru a trimite la cloud doar media la fiecare minut (în loc de fiecare valoare individuală) sau detectarea unei condiții de alertă (dacă 3 senzori de mișcare declanșează simultan, edge-ul trimite un eveniment “alarmă” către cloud). Apoi se realizează teste de încărcare: de exemplu, se crește numărul de senzori sau frecvența cu care trimit date și se observă cum face față sistemul (broker-ul MQTT are vreun delay, edge-ul consumă mult CPU?). Se pot adăuga și testări de reziliență: se oprește temporar broker-ul sau nodul cloud pentru a vedea ce se întâmplă cu mesajele (MQTT QoS1/2 pot reține mesajele neconfirmate). Dacă se implementează securitate, acum e momentul: configurarea autentificării pe broker (utilizatori și parole pentru senzori), eventual activarea TLS (cerere de certificate – poate complex, dar echipe avansate pot demonstra unul-două noduri comunicând criptat). La finalul acestei etape, sistemul ar trebui să fie capabil să simuleze câteva zeci de dispozitive trimițând date și edge-ul să proceseze și să retransmită rezumate fără pierderi notabile. - Etapa 4 (prezentarea în săptămâna 14): Echipa va prezenta rețeaua IoT simulată printr-o demonstrație și o analiză a comportamentului sistemului. Demonstrația ar putea include rularea în direct a, să zicem, 5 senzori virtuali – se va vedea în consola edge-ului cum primește datele de la fiecare și cum trimite mai departe un mesaj agregat la cloud (poate cloud-ul e tot un script ce afișează ce primește). Opțional, se poate demonstra cum edge-ul reacționează la un eveniment: de exemplu, se crește brusc valoarea simulatǎ a unui senzor (peste un prag) și se arată că edge-ul detectează condiția și trimite alertă imediat către cloud. În prezentare, studenții vor discuta avantajele observate: de exemplu, volumul de date trimis la cloud a scăzut datorită procesării locale – pot cuantifica “fără edge trimiteam X mesaje/oră, cu edge trimitem X/2 mesaje/oră” – și latența unei alerte locale este mult mai mică (ex: se declanșează instant local, pe când dacă s-ar aștepta decizia din cloud, ar fi întârziere mai mare). Vor menționa și limitările întâlnite: de exemplu, complexitatea sincronizării a multor noduri, eventual dificultatea configurării securității. Un aspect important: studenții vor corela experiența lor cu principiile teoretice – de pildă, vor menționa că IoT implică comunicarea autonomă între obiecte fizice[5] și vor evidenția importanța protocoalelor ușoare precum MQTT pentru constrângeri de rețea. Concluziile vor sublinia că proiectul le-a oferit o perspectivă practică asupra modului în care rețelele de calculatoare evoluează pentru a integra dispozitive IoT și necesitatea edge computing pentru eficiență.

### 🔮 VERIFICARE ÎNȚELEGERE - IoT ȘI MQTT

Înainte de a testa sistemul IoT, răspundeți:

1. Dacă senzorul publică pe topic-ul casa/living/temperatura, cine primește mesajul?
   → Toți clienții abonați la acest topic sau la casa/living/# sau casa/#

2. Ce se întâmplă dacă broker-ul MQTT nu este pornit când senzorul încearcă să publice?
   → Eroare: Connection refused. Senzorul trebuie să implementeze retry logic.

3. Ce nivel QoS ar trebui folosit pentru date critice (ex: alarmă incendiu)?
   → QoS 2 (Exactly once) pentru a garanta livrarea mesajului


### 📊 PEER INSTRUCTION - DOCKER ȘI REȚELE CONTAINERE

Discutați cu colegii și alegeți împreună răspunsul corect:

Întrebarea 1: Containerele web și db sunt în aceeași rețea Docker bridge. Cum poate web să se conecteze la portul 5432 al db?

A) localhost:5432 - containerele partajează același localhost
B) db:5432 - Docker DNS rezolvă automat numele serviciului ✓
C) 172.17.0.1:5432 - adresa gateway-ului bridge
D) host.docker.internal:5432 - referință la mașina host

Explicație: Docker Compose creează DNS intern. Containerele se găsesc prin numele serviciului, nu prin localhost (care e izolat per container).

Întrebarea 2: Un container expune portul 8080:80. Ce înseamnă această configurare?

A) Containerul ascultă pe 8080, host-ul expune pe 80
B) Host-ul ascultă pe 8080, containerul intern pe 80 ✓
C) Ambele porturi sunt echivalente
D) Portul 8080 este blocat de firewall

Explicație: Formatul este HOST_PORT:CONTAINER_PORT. Accesați serviciul din browser la http://localhost:8080


### Extensii pentru echipe de 3 vs. 2/1 membri: O echipă de 3 studenți poate ambiționa un scenariu IoT de scară mai mare sau mai complex. De exemplu, pot simula 20-30 de senzori și să realizeze scripturi de orchestrare care pornesc automat aceste entități (posibil chiar folosind Docker Compose pentru a porni multe containere-senzor). Totodată, pot diversifica tipurile de device-uri: senzori și și actuatori – de pildă, să includă în simulare un “dispozitiv” actuator (cum ar fi un sistem de udat plantele) care se activează doar când primește de la edge comanda (publish pe un topic special) – asta ar implica o buclă închisă de control. Pe zona de cloud, pot realiza un mic dashboard web (cu Python/Flask sau Node.js) care afișează în timp real datele primite de la edge, ceea ce ar îmbogăți prezentarea vizual. Implementarea securității MQTT (TLS, autentificare) ar fi și ea o extensie potrivită pentru o echipă numeroasă, având în vedere configurarea mai laborioasă. Pentru echipele de 2 studenți, proiectul poate fi ținut la nivelul de bază: ~5-10 senzori, fără elemente de actuatori, accent pe funcționalitatea principală publish-subscribe și agregare edge. Se pot limita la securitate simplă (poate doar autentificare cu parolă pe broker, fără TLS). În cazul unui student individual, se poate reduce și mai mult complexitatea – de exemplu 3 senzori trimițând direct la cloud fără edge distinct (practic doar demonstrând MQTT pub-sub), sau un singur senzor care trimite la edge și edge la cloud, pentru a proba lanțul complet cu minimum de componente. Important este ca și varianta simplificată să respecte paradigmă IoT (senzor, rețea, consumator date) și studentul să explice cum s-ar extinde la scară mai mare. În toate cazurile, evaluarea va ține cont de nivelul de dificultate asumat voluntar de echipă și de gradul de realizare a funcționalităților propuse.


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


### ❓ ÎNTREBĂRI FRECVENTE - DOCKER

Q: Eroare "port is already allocated" la pornirea containerelor
A: Portul e ocupat de alt proces. Soluții:
   - Verificați: ss -tlnp | grep :PORT
   - Opriți procesul existent sau schimbați portul în docker-compose.yml

Q: Containerele nu pot comunica între ele
A: Verificați configurarea rețelei:
   - docker network ls (listează rețelele)
   - docker network inspect NETWORK_NAME (detalii)
   - Asigurați-vă că serviciile sunt în aceeași rețea

Q: Cum văd log-urile unui container pentru debugging?
A: Folosiți comenzile:
   - docker logs CONTAINER_NAME
   - docker compose logs SERVICE_NAME
   - docker compose logs -f (follow în timp real)


### 📚 Bibliografie

[1]  Kreutz, D., Ramos, F.M.V., Esteves Verissimo, P., Esteve Rothenberg, C., Azodolmolky, S. and Uhlig, S. (2015) Software-Defined Networking A complet Survey. Proceedings of the IEEE, 103, 14-76. - References - Scientific Research Publishing
https://www.scirp.org/reference/referencespapers?referenceid=3911400
[2] Defense-in-Depth Methods in Microservices Access Control
https://trepo.tuni.fi/bitstream/123456789/27172/4/suomalainen.pdf
[3] Remote procedure call - Wikipedia
https://en.wikipedia.org/wiki/Remote_procedure_call
[4] usenix.org
https://www.usenix.org/legacy/event/lisa99/full_papers/roesch/roesch.pdf
[5] A Review on Internet of Things -Protocols, Issues - Academia.edu
https://www.academia.edu/32025103/A_Review_on_Internet_of_Things_Protocols_Issues
---

## 🔮 Verificare înțelegere — IoT și MQTT

Înainte de testare:

1. **Cine primește mesajul publicat pe "casa/living/temp"?**
   - Toți clienții abonați la acest topic sau "casa/living/#"

2. **Ce se întâmplă dacă broker-ul MQTT nu rulează?**
   - Eroare: Connection refused

3. **Ce QoS folosim pentru date critice?**
   - QoS 2 (Exactly once)


---

## ❓ Întrebări frecvente — Docker

**Q: Eroare "port is already allocated"**  
A: Portul e ocupat. Verifică: `ss -tlnp | grep :PORT` și oprește procesul sau schimbă portul.

**Q: Containerele nu comunică între ele**  
A: Verifică rețeaua: `docker network ls` și `docker network inspect NETWORK`

**Q: Cum văd logurile unui container?**  
A: `docker logs CONTAINER` sau `docker compose logs SERVICE`


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


### 💡 Pentru MQTT și IoT

MQTT e similar cu WebSockets pe care le-ai folosit poate în TW:

```python
# WebSocket (TW) vs MQTT (Rețele)

# WebSocket: conexiune bidirecțională client-server
# MQTT: publish/subscribe prin broker

import paho.mqtt.client as mqtt

# Similar cu socket.on('message', callback) din Socket.IO
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}, Message: {msg.payload.decode()}")

client = mqtt.Client()
client.on_message = on_message

# Similar cu socket.emit() dar prin broker
client.connect("localhost", 1883)
client.subscribe("casa/living/temp")  # Similar cu socket.join('room')
client.publish("casa/living/temp", "22.5")  # Similar cu io.to('room').emit()
```


### 💡 Pentru Docker și Containere

Din TW știi npm și package.json. Docker e similar dar pentru mediu complet:

```yaml
# docker-compose.yml e similar cu package.json pentru dependențe
# dar include și mediul de runtime

services:
  web:
    image: nginx
    ports:
      - "8080:80"  # Similar cu "scripts": {"start": "node index.js"} pe port
  
  api:
    build: ./api    # Similar cu npm install din package.json
    environment:
      - DB_HOST=db  # Similar cu process.env.DB_HOST
```

```bash
# Comenzi similare
npm install     →  docker compose build
npm start       →  docker compose up
npm stop        →  docker compose down
npm run dev     →  docker compose up --watch
```

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `13roWSL/` — IoT și Securitate

**Ce găsești relevant:**
- MQTT, Mosquitto broker, senzori

**Fișiere recomandate:**
- `13roWSL/README.md` — prezentare generală și pași de laborator
- `13roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `13roWSL/docs/fisa_comenzi.md` — comenzi utile
- `13roWSL/src/` — exemple de cod Python
- `13roWSL/homework/` — exerciții similare


### 📁 `03roWSL/` — Broadcast și Multicast

**Ce găsești relevant:**
- Publish/subscribe pattern

**Fișiere recomandate:**
- `03roWSL/README.md` — prezentare generală și pași de laborator
- `03roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `03roWSL/docs/fisa_comenzi.md` — comenzi utile
- `03roWSL/src/` — exemple de cod Python
- `03roWSL/homework/` — exerciții similare


### 📁 `10roWSL/` — REST

**Ce găsești relevant:**
- Edge gateway, API-uri pentru senzori

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
