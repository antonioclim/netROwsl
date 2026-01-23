# Proiectul 05: Implementarea unui protocol de rutare personalizat în Python

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
https://github.com/[username]/retele-proiect-05
```

#### Structura obligatorie a repository-ului

```
retele-proiect-05/
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

**Format:** `NUME_Prenume_GGGG_P05_TT.zip`

| Câmp | Descriere | Exemplu |
|------|-----------|---------|
| NUME | Numele de familie (MAJUSCULE, fără diacritice) | POPESCU |
| Prenume | Prenumele (prima literă mare) | Ion |
| GGGG | Numărul grupei (4 cifre) | 1098 |
| P05 | Numărul proiectului | P05 |
| TT | Tipul livrabilului (E1-E4 sau SXX) | E1 |

**Exemple pentru acest proiect:**
- `POPESCU_Ion_1098_P05_E1.zip` — Etapa 1
- `POPESCU_Ion_1098_P05_E2.zip` — Etapa 2
- `POPESCU_Ion_1098_P05_S07.zip` — Verificare săptămâna 7

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
Acest proiect are ca obiectiv simularea și implementarea unui protocol de rutare la scară mică, pentru a înțelege modul în care calculatoarele și routerele își distribuie informații de rutare într-o rețea. Studenții vor crea o aplicație (sau un set de aplicații) în Python care rulează pe mai multe noduri (de exemplu, pe instanțe Mininet sau pe mai multe mașini virtuale) și care comunică între ele pentru a face schimb de tabele de rutare. Se poate alege fie modelarea unui protocol de rutare vectorial la distanță (în stilul RIP, cu schimb de vectori de distanță periodic), fie a unui protocol de rutare de stare a legăturii (în stilul OSPF, cu schimb de metrici și calcul global de drumuri).
Un scenariu posibil: se vor emula 3-5 noduri (ca și cum ar fi routere) interconectate într-o anumită topologie (ex: un cerc sau o topologie generală). Fiecare nod va rula o instanță a programului de rutare dezvoltat. Nodurile vor comunica prin socket-uri UDP sau TCP, trimițând mesaje de actualizare de rută la intervale regulate sau la detectarea unei modificări. De exemplu, într-o abordare de tip Distance Vector, fiecare nod își va trimite lista curentă de destinații cunoscute și costuri către vecinii săi; aceștia vor actualiza tabelele lor folosind algoritmul Bellman-Ford (sau varianta simplificată specifică RIP). În abordarea Link State, fiecare nod va transmite vecinilor săi pachete de stare a legăturilor (LSA) conținând costurile spre vecinii direcți; eventual, fiecare nod va avea astfel cunoștința întregului graf și va calcula local rutele folosind un algoritm ca Dijkstra.
Proiectul implică și tratarea unor probleme clasice de rutare, precum convergența (asigurarea că toți ajung la tabele consistente), gestionarea topologiilor dinamice (dacă un nod/punct de legătură cade, protocolul ar trebui să actualizeze rutele) și prevenirea problemelor ca bucla de rutare (ex: în Distance Vector se pot experimenta situații de count-to-infinity, care pot fi abordate prin limite sau split horizon, etc., dacă timpul permite). Rezultatul final va fi un demo al protocolului: se va putea porni instanțele pe noduri, acestea vor realiza schimbul de mesaje de rutare și, după o perioadă, fiecare nod își afișează tabelul de rutare stabilizat (cu destinații și next-hop/cost). Opțional, se poate demonstra adaptarea: dacă se deconectează un nod sau se schimbă costul unei legături, noile rute sunt recalculate și propagate.

### 🎯 Obiective de învățare

Aprofundarea principiilor algoritmilor de rutare dinamică (vectorii de distanță și starea legăturii) într-un mod practic, văzând cum se traduc în mesaje și actualizări.

### 🛠️ Tehnologii și unelte

Învățarea importanței conceptelor de convergență și stabilitate într-o rețea: cum mici diferențe (timpi sau pierderi de pachete) pot afecta momentul în care toate nodurile au informații corecte.
Exersarea depanării de rețea la nivel logic – studenții vor trebui să verifice conținutul mesajelor de rutare și evoluția tabelelor de rutare, eventual folosind log-uri sau mesaje de debug, similar cu modul în care s-ar inspecta pachetele într-un protocol real.
Înțelegerea limitărilor protocoalelor reale (RIP, OSPF) prin comparare cu implementarea lor simplificată – de exemplu, de ce RIP are metrică limitată la 15 sau cum OSPF evită inundațiile excesive. Acest proiect poate oferi un context practic acestor discuții teoretice.

### 📖 Concepte cheie

Algoritmi de rutare – Distance Vector (Bellman-Ford) și Link State (Dijkstra), actualizarea tabelelor de rută, metrici (costuri) ale legăturilor.
Protocoale de rutare inter-routere – mecanisme de anunțare a rutelor (mesaje periodic vs. evenimential), formate de pachete (ex: un mesaj DV conține perechi destinație-cost; un mesaj LS conține identificator de nod și lista de vecini cu costuri).
Topologii de rețea și grafuri – reprezentarea rețelei ca graf de noduri și legături; noțiunea de cost al drumului și calculul celui mai scurt drum.
Convergență și stabilitate – propagarea schimbărilor, detectarea link-urilor căzute (ex: prin time-out dacă nu mai primim anunțuri de la un vecin), probleme ca routing loops și soluții (split horizon, hold-down timers – pot fi menționate sau implementate dacă se alege).
Adrese IP și rutare – în implementare putem folosi IP reale ale mașinilor/VM-urilor pentru a simula adresele rețelelor destinație; conceptul de next hop și de mască poate fi menționat (deși se poate simplifica considerând fiecare nod identificat de un ID sau IP distinct fără subrețele multiple).
Tehnologii implicate
Python – limbaj pentru implementare, ușor pentru manipularea pachetelor. Se vor folosi socket-uri (probabil UDP, dat fiind că multe protocoale de rutare reale folosesc UDP pentru anunțuri, ex RIP pe port 520). TCP ar putea fi folosit, dar UDP reflectă mai bine natura “connectionless” a anunțurilor de rutare.
Biblioteci Python – eventual struct pentru a construi pachete binare (dacă se dorește simularea la nivel de byte), deși e acceptabil să se trimită mesaje JSON sau pickled (Python objects) pentru simplitate. Threading sau asyncio poate fi util pentru a asculta și trimite mesaje simultan.
Mediu de test – se poate folosi Mininet pentru a crea noduri virtuale și legături cu latențe sau costuri (costul poate fi asimilat timpului de ping sau lățimii de bandă invers proporțional, sau setat static). Alternativ, mai multe procese pe un singur PC, diferențiate prin porturi UDP, pot simula nodurile de rețea (costurile configurate manual în cod).
Instrumente de monitorizare – Wireshark pentru a vedea mesajele UDP de rutare (dacă sunt în format clar sau se poate defini un dissector custom rudimentar, deși nu e obligatoriu), logging intern în fișiere pentru a înregistra starea tabelelor de rutare după fiecare iterație, facilitând debug-ul.
Configurație – un fișier de configurare (ex: .json sau text) care descrie topologia (ce noduri sunt vecine cu costurile respective) ar fi util; aplicația îl poate citi la pornire astfel încât rețeaua simulată e clar definită.
Legătura cu temele din săptămânile cursului
Săptămâna 5: Adresarea IP și subrețele – un protocol de rutare are ca scop propagarea informației despre ce adrese IP sunt accesibile printr-un anumit nod. Cunoștințele despre adrese și prefixe din sapt. 5 sunt temelia pe care se construiește înțelegerea rutării.
Săptămâna 6: Protocoale de rutare – acest proiect este practic aplicarea subiectelor discutate în săptămâna 6 (unde, conform fișei, probabil s-au acoperit algoritmi de rutare, RIP, OSPF, etc.). Proiectul vine ca o extensie practică a laboratorului Week6 („Simulare algoritmi de rutare” din arhivă), prin implementare reală.
Săptămâna 3: Echipamente de rețea – studenții vor simula comportamentul unor routere, deci se leagă de cunoștințele despre rolul routerelor și interconectarea rețelelor din sapt. 3.
Săptămâna 12: Programare de rețea – se folosesc socket-uri și programare concurentă, abilități exersate în cursul de programare a rețelei. În special, lucrul cu UDP (nelivrat, posibil pierdere de pachete) este legat și de discuțiile despre transport vs. rețea.
Etapele proiectului

### 📋 Etapa 1 (Săptămâna 5) – Definirea topologiei și a protocolului de rutare: Se va alege tipul de protocol (Distance Vector simplu sau Link State simplu) și se va defini o topologie de test (numărul de noduri și cum sunt conectate). De exemplu, se decide: “Vom implementa un protocol de rutare vectorial la distanță în stil RIP, metrică = număr de hopuri, topologia: nodurile A-B-C formează un lanț, plus legătură A-C directă etc.”. Se va redacta și un pseudo-cod al algoritmului de actualizare (Bellman-Ford): cum procesează un nod informațiile primite de la vecin. Totodată, se definește formatul mesajelor de rutare: de ex., “mesaj DV = [ (destinație, cost), (destinație, cost), ... ], trimis UDP pe port X ”. Livrabil: un document de design care include diagrama topologiei (cu costuri inițiale pe fiecare legătură), specificația protocolului (algoritm + format mesaje) și planul de test (ce situații se vor verifica – ex: calculul inițial, apoi deconectarea unui nod etc.).


### 🔨 Etapa 2 (Săptămâna 9) – Implementare inițială și test pe convergență statică: Se implementează aplicația de rutare conform design-ului. În prima versiune, se poate presupune că topologia rămâne fixă pe durata testului (fără căderi de noduri). Fiecare instanță pornită pe un nod citește configurația (cine îi sunt vecinii și costurile către ei), pornește un listener UDP și începe să trimită periodic mesaje de rutare. Se instrumentează codul astfel încât fiecare nod să afișeze periodic tabela sa de rutare (destinație -> cost, next hop). Se rulează toți demonii de rutare și se observă dacă, după un anumit timp, tabelele se stabilizează conținând drumurile corecte (cele mai scurte). Livrabil: codul sursă (în repository) și un log/rezultat al rulării pe un caz de test, care să arate evoluția tabelelor de la start (când fiecare cunoaște doar pe sine și vecinii) până la convergență (când toți cunosc rutele optime). De exemplu, se pot prezenta capturi în care la început nodul A știe doar B cu cost 1, iar după convergență știe și de C cu cost 2 prin B, etc.


### 🔮 VERIFICARE ÎNȚELEGERE - CONCEPTE REȚEA

Înainte de configurare, verificați că înțelegeți:

1. Ce tip de adresă este 192.168.1.50?
   → Adresă privată (RFC 1918), nu poate fi rutată direct pe Internet

2. Câte adrese IP utilizabile sunt într-o rețea /24?
   → 254 adrese (256 total minus 1 pentru rețea minus 1 pentru broadcast)

3. Ce rol are NAT în rețeaua voastră?
   → Traduce adresele IP private în adresa publică pentru acces Internet


### ✅ Etapa 3 (Săptămâna 13) – Implementare evenimente dinamice și optimizări: În această etapă se introduce capacitatea protocolului de a reacționa la schimbări: de exemplu, se deconectează un nod (nu mai trimite mesaje; vecinii ar trebui după un timeout să îl considere inactiv și să-și actualizeze tabelele). Sau se modifică costul unei legături (dacă se poate simula, de ex. in Mininet prin schimbarea delay-ului) și se observă adaptarea. Se pot adăuga mecanisme suplimentare pentru solidețe, precum un timer de invalidare (dacă într-un interval nu se primește nicio actualizare de la un vecin, rutele prin acel vecin sunt marcate inaccesibile – similar cu "timeout" din RIP). Dacă echipa dorește, pot implementa și prevenirea buclelor prin “split horizon” (nu anunță unei rute înapoi pe interfața de unde au venit). Livrabil: codul final (care include tratarea evenimentelor de cădere) și un set de experimente documentate: ex. un scenariu în care nodul X cade și cum tabelele se modifică (se așteaptă câteva intervale, se scot rutele ce duceau la X). Alt scenariu: creșterea costului pe o legătură cauzează recalcularea drumului alternativ (dacă există) cu cost mai mic. Rezultatele pot fi prezentate sub formă de loguri înainte/după eveniment, evidențiind reacția corectă a algoritmului.


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


### 🎤 Etapa 4 (Săptămâna 14) – Prezentare finală: Echipa va prezenta conceptul protocolului implementat, comparându-l cu echivalentul real (dacă DV, atunci cu RIP; dacă LS, cu OSPF). Vor arăta vizual topologia de test și, posibil, vor ilustra pe slide-uri cum se propagă informația de rutare (ex: “Pasul 1: A știe doar 0 pt A și inf pt restul; Pasul 2: A primește de la B distanțele ...” etc.). Demo-ul practic poate consta în rularea aplicației cu 3 noduri în consolă, arătând cum pornesc cu rute locale și ajung să cunoască întreaga rețea. Opțional, se poate demonstra un caz de failover: se oprește unul din procese (simulând căderea unui nod) și se vede cum celelalte actualizează că destinațiile prin acel nod nu mai sunt accesibile. Livrabil: prezentarea (cu diagrame și eventual pseudocod) și demonstrația live sau pre-înregistrată a funcționării protocolului.

Extensii posibile pentru echipe de 3 vs. 2/1 studenți
Echipe de 3 studenți: pot încerca implementarea ambelor tipuri de algoritmi (DV și LS) și compararea lor. De exemplu, pot realiza modulul principal comun iar algoritmul de actualizare să fie plug-in: rulat fie ca DV, fie ca LS, și să demonstreze ambele metode în topologii similare. Echipa lărgită poate extinde proiectul spre vizualizarea rețelei – de exemplu, generarea unui grafic (folosind Graphviz) al topologiei cunoscute de fiecare nod, pentru a vedea diferențe. O altă extindere ambițioasă: integrarea proiectului cu configurarea reală a rutării pe un router software (ex: folosind Quagga prin API – dar asta ar fi destul de complex, deci doar ca experiment).
Echipe 1-2 studenți: pot simplifica proiectul reducând numărul de noduri și situațiile gestionate. De exemplu, pentru 2 studenți, o topologie triunghiulară statică (3 noduri complet interconectate) este suficientă pentru a demonstra conceptul, fără să mai trateze căderi de nod (fiecare cunoaște tot oricum într-un triunghi complet). Totodată, pot evita implementarea optimizărilor de buclă și pot presupune metrici fixe (fără recalcularea costurilor la runtime). Astfel, ei se concentrează pe implementarea de bază a algoritmului și pe convergența inițială, ceea ce acoperă oricum o bună parte din obiectivele de învățare.

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

Tanenbaum, A. S., Feamster, N., & Wetherall, D. (2021). Computer Networks (6th ed.). Pearson. (Capitolele despre algoritmii de rutare și protocoalele RIP/OSPF – oferă fundalul teoretic necesar)
Kurose, J. F., & Ross, K. W. (2021). Computer Networking: A Top-Down Approach (8th ed.). Pearson. (Vezi capitolul privind rutarea: descrie conceptele de vector distanță și stare legătură, utile pentru orientare în implementare)
Hedrick, C. (1988). RFC 1058: Routing Information Protocol. IETF. (Standardul pentru RIP v1 – conține detalii despre formatul mesajelor și algoritm, care pot fi parcurse pentru inspirație, deși proiectul implementat este o versiune simplificată)
Moy, J. (1998). RFC 2328: OSPF Version 2. IETF. (Descrierea oficială a OSPF – utilă pentru înțelegerea conceptului de link-state, flooding de pachete LSA, chiar dacă nu se implementează în detaliu, oferă perspectivă asupra cerințelor unui protocol real)
Grime, S. (2019). Networking Algorithms: An Applied Approach. TechPress. (Include studii de caz de implementare simplă a algoritmilor de rutare în cod – poate servi ca exemplu suplimentar de structurare a aplicației de rutare)
(Notă: Proiectele 6–20 vor continua în același format detaliat, acoperind restul de subiecte avansate și moderate, conform cerințelor.)
... (documentul continuă cu proiectele 6–15 – avansate, și 16–20 – cu dificultate ușor redusă, structurate similar ca mai sus) ...
Tabel de planificare a etapelor pe săptămâni
[1] Static Equivalence Checking for OpenFlow Networks - MDPI
https://www.mdpi.com/2079-9292/10/18/2207
[2] Mininet - Washington
https://courses.cs.washington.edu/courses/cse461/22au/assignments/mininet.html
[3] Containernet | Use Docker containers as hosts in Mininet emulations.
https://containernet.github.io/
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

---

## 📚 MATERIALE DE LABORATOR RELEVANTE

Consultă aceste resurse din arhiva **netROwsl** pentru conceptele necesare:


### 📁 `05roWSL/` — Adresare IPv4/IPv6, Subrețele și VLSM

**Ce găsești relevant:**
- Calculul rutelor, tabele de rutare

**Fișiere recomandate:**
- `05roWSL/README.md` — prezentare generală și pași de laborator
- `05roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `05roWSL/docs/fisa_comenzi.md` — comenzi utile
- `05roWSL/src/` — exemple de cod Python
- `05roWSL/homework/` — exerciții similare


### 📁 `04roWSL/` — Protocoale Personalizate

**Ce găsești relevant:**
- Definirea și implementarea protocolului

**Fișiere recomandate:**
- `04roWSL/README.md` — prezentare generală și pași de laborator
- `04roWSL/docs/rezumat_teoretic.md` — concepte teoretice
- `04roWSL/docs/fisa_comenzi.md` — comenzi utile
- `04roWSL/src/` — exemple de cod Python
- `04roWSL/homework/` — exerciții similare


### 📁 `06roWSL/` — NAT/PAT și SDN

**Ce găsești relevant:**
- Routing decisions, forwarding

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
