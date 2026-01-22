# Teme pentru Acasă - Săptămâna 1

> Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix

## Prezentare Generală

Acest director conține temele pentru acasă aferente Săptămânii 1.
Fiecare temă include: descrierea cerințelor, script de pornire (starter), și criterii de evaluare.

## Teme Disponibile

### Tema 1: Raport de Configurare a Rețelei

**Obiectiv:** Documentați configurația completă a rețelei pe calculatorul personal.

**Cerințe:**
1. Rulați scriptul `exercises/tema_1_01_raport_retea.py`
2. Completați secțiunile marcate cu `TODO`
3. Analizați și interpretați rezultatele
4. Răspundeți la întrebările din șablon

**Livrabile:**
- `raport_retea.md` - raportul completat cu analiza voastră

**Criterii de Evaluare:**
| Criteriu | Punctaj |
|----------|---------|
| Completitudine date | 40% |
| Corectitudine | 30% |
| Analiză și interpretare | 20% |
| Formatare | 10% |

---

### Tema 2: Analiza Protocoalelor TCP/UDP

**Obiectiv:** Capturați și comparați traficul TCP și UDP.

**Cerințe:**
1. Capturați trafic TCP pe portul 9090
2. Capturați trafic UDP pe portul 9091
3. Identificați handshake-ul TCP în captură
4. Comparați overhead-ul celor două protocoale

**Livrabile:**
- `tcp_analiza.pcap` - captura traficului TCP
- `udp_analiza.pcap` - captura traficului UDP
- `analiza_protocol.md` - raportul de analiză

**Criterii de Evaluare:**
| Criteriu | Punctaj |
|----------|---------|
| PCAP-uri valide | 30% |
| Identificare handshake | 25% |
| Comparație overhead | 30% |
| Calitate raport | 15% |

---

## Lucrul în Perechi (Recomandat)

Temele sunt **individuale**, dar discuțiile și debugging-ul în perechi sunt încurajate. Cercetările arată că Pair Programming îmbunătățește înțelegerea și reduce erorile.

### Metoda Driver-Navigator

| Rol | Ce face | Durată |
|-----|---------|--------|
| **Driver** | Scrie cod, tastează comenzi, navighează în fișiere | 15-20 min |
| **Navigator** | Verifică ce scrie Driver-ul, sugerează abordări, caută în documentație | 15-20 min |

După 15-20 minute, **schimbați rolurile**. Rotația e importantă!

### Reguli de Aur

**Navigator-ul POATE:**
- ✅ Spune "încearcă comanda `ss -tlnp`"
- ✅ Întreba "ce crezi că va afișa asta?"
- ✅ Sugera "hai să verificăm documentația pentru parametrul ăsta"
- ✅ Indica erori: "cred că lipsește un două puncte pe linia 15"

**Navigator-ul NU poate:**
- ❌ Dicta cod linie cu linie ("scrie i-p-space-a-d-d-r...")
- ❌ Lua tastatura din mâna Driver-ului
- ❌ Critica în loc să sugereze

**Driver-ul TREBUIE:**
- ✅ Să explice ce face și de ce
- ✅ Să asculte sugestiile Navigator-ului
- ✅ Să întrebe dacă ceva nu e clar

### Ce Este Permis în Perechi

| ✅ Permis | ❌ Interzis |
|-----------|-------------|
| Discuții despre concepte | Copierea codului final |
| Debugging împreună | Un singur om face toată munca |
| Împărtășirea resurselor găsite | Predarea aceluiași cod |
| Explicarea abordărilor | Împărțirea temei ("tu faci 1, eu fac 2") |

### Găsirea unui Partener

- Întreabă colegii de grupă la laborator
- Folosește canalul Discord/Teams al cursului
- Lucrează la biblioteca facultății

**Notă:** Chiar dacă lucrezi în perechi pentru debugging, tema predată trebuie să fie munca ta proprie.

---

## Instrucțiuni de Predare

### Format

Arhivați livrabilele într-un fișier ZIP cu numele:
```
tema1_<nr_matricol>_<nr_tema>.zip
```

Exemplu: `tema1_123456_1.zip`

### Structura Arhivei

```
tema1_123456_1/
├── raport_retea.md
└── (alte fișiere necesare)
```

### Termen Limită

Verificați platforma de e-learning pentru data exactă de predare.

## Integritate Academică

- Temele sunt **individuale**
- Copierea este **strict interzisă**
- Discuțiile despre concepte sunt permise
- Predarea codului altcuiva = 0 puncte pentru ambele părți

### Ce este permis:

✓ Consultarea documentației oficiale
✓ Utilizarea exemplelor din laborator
✓ Discuții conceptuale cu colegii
✓ Căutarea de soluții la erori specifice
✓ Pair Programming pentru debugging

### Ce NU este permis:

✗ Copierea codului de la colegi
✗ Partajarea soluțiilor complete
✗ Utilizarea soluțiilor de pe internet fără înțelegere
✗ Predarea muncii altcuiva
✗ Folosirea ChatGPT/AI pentru a genera soluția completă

## Resurse Utile

- `../docs/rezumat_teoretic.md` - Concepte teoretice + analogii CPA
- `../docs/fisa_comenzi.md` - Comenzi utile
- `../docs/depanare.md` - Soluții la probleme comune
- `../docs/intrebari_peer_instruction.md` - Întrebări pentru auto-evaluare
- `../src/exercises/` - Exemple de cod

## Întrebări Frecvente

**Î: Pot folosi alt limbaj decât Python?**
R: Da, dar trebuie să documentați cum se rulează codul.

**Î: Ce fac dacă scriptul nu funcționează?**
R: Verificați `docs/depanare.md` sau cereți ajutor la laborator.

**Î: Pot preda mai devreme?**
R: Da, oricând înainte de termen.

**Î: Ce se întâmplă dacă ratez termenul?**
R: Consultați politica de întârzieri din syllabus.

**Î: Pot lucra în perechi?**
R: Da, pentru discuții și debugging. Tema predată trebuie să fie munca ta.

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică | by Revolvix*
