# Exerciții pentru Lucru în Perechi – Săptămâna 5

> Activități structurate de pair programming
> Laborator Rețele de Calculatoare – ASE, Informatică Economică

---

## Cum Funcționează Pair Programming

### Roluri

| Rol | Responsabilitate |
|-----|------------------|
| **Driver** | Tastează codul, execută comenzile |
| **Navigator** | Ghidează strategia, verifică greșeli, consultă documentația |

**Reguli:**
- Schimbați rolurile la fiecare exercițiu
- Navigatorul NU atinge tastatura
- Driver-ul explică ce face pe măsură ce tastează
- Comunicați constant

---

## Exercițiul P1: Debug Subrețea Greșită

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 15 min | ★★☆☆☆ | ANALYZE | Formula prefix |

**Roluri:** Navigator calculează, Driver verifică

### Scenariu

Colegul tău a calculat următoarele subrețele pentru departamentul DEV care are nevoie de **120 de gazde**.

El a alocat: `192.168.0.0/26`

**Este corect?**

### Pași

1. **Navigator:** Calculează pe hârtie prefixul necesar pentru 120 de gazde
   - Formula: `32 - ceil(log2(120 + 2))`
   - Rezultat așteptat: ?

2. **Driver:** Verifică cu scriptul:
   ```bash
   python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.0.0/26
   ```

3. **Navigator:** Compară rezultatul cu cerința de 120 gazde

4. **Driver:** Propune prefixul corect și verifică:
   ```bash
   python3 src/exercises/ex_5_01_cidr_flsm.py analizeaza 192.168.0.0/??
   ```

5. **Ambii:** Discutați diferența și documentați

### Soluție

<details>
<summary>Click pentru soluție</summary>

**/26 oferă doar 62 de gazde** — insuficient pentru 120.

Calcul corect:
- 120 + 2 = 122 adrese necesare
- ceil(log2(122)) = 7 biți pentru gazde
- Prefix = 32 - 7 = **25**
- /25 oferă 126 gazde ✓

</details>

### ✓ Checkpoint

Înainte de a trece mai departe, verificați:
- [ ] Ambii înțelegeți de ce /26 e insuficient
- [ ] Ambii puteți calcula prefixul pentru orice număr de gazde

### Schimb Roluri → Exercițiul P2

---

## Exercițiul P2: Design VLSM de la Zero

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 25 min | ★★★☆☆ | CREATE | Algoritm VLSM |

**Roluri:** Navigator planifică, Driver implementează

### Scenariu

Firma **CloudNine SRL** are următoarele departamente:

| Departament | Gazde Necesare |
|-------------|----------------|
| Development | 45 |
| Marketing | 20 |
| HR | 8 |
| Server Room | 4 |
| Link WAN | 2 |

Rețeaua de bază: `10.100.0.0/24`

### Pași

1. **Navigator:** Pe hârtie, sortează cerințele descrescător și calculează prefixurile necesare:

   | Departament | Gazde | Prefix Necesar | Subrețea |
   |-------------|-------|----------------|----------|
   | | | | |
   | | | | |
   | | | | |
   | | | | |
   | | | | |

2. **Driver:** Verifică cu scriptul VLSM:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.100.0.0/24 \
       --cerinte 45,20,8,4,2
   ```

3. **Navigator:** Compară rezultatul scriptului cu calculele manuale

4. **Driver:** Generează output JSON pentru documentare:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 10.100.0.0/24 \
       --cerinte 45,20,8,4,2 --json > /tmp/cloudnine_vlsm.json
   ```

5. **Ambii:** Calculați eficiența totală:
   ```
   Eficiență = Gazde cerute / Gazde alocate * 100%
   ```

### Soluție

<details>
<summary>Click pentru soluție</summary>

| Departament | Gazde | Prefix | Subrețea | Disponibil |
|-------------|-------|--------|----------|------------|
| Development | 45 | /26 | 10.100.0.0/26 | 62 |
| Marketing | 20 | /27 | 10.100.0.64/27 | 30 |
| HR | 8 | /28 | 10.100.0.96/28 | 14 |
| Server Room | 4 | /29 | 10.100.0.112/29 | 6 |
| Link WAN | 2 | /30 | 10.100.0.120/30 | 2 |

Total cerut: 79 gazde  
Total alocat: 114 gazde  
Eficiență: 79/114 = **69%**

</details>

### Schimb Roluri → Exercițiul P3

---

## Exercițiul P3: Comparație FLSM vs VLSM

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 20 min | ★★★☆☆ | EVALUATE | FLSM, VLSM |

**Roluri:** Fiecare calculează o metodă, apoi comparați

### Scenariu

Firma **TechStart** are 4 departamente cu cerințe identice: **30 de gazde fiecare**.  
Rețeaua de bază: `192.168.50.0/24`

### Pași

1. **Driver:** Calculează cu FLSM (4 subrețele egale):
   ```bash
   python3 src/exercises/ex_5_01_cidr_flsm.py flsm 192.168.50.0/24 4
   ```

2. **Navigator:** Calculează cu VLSM:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py vlsm 192.168.50.0/24 \
       --cerinte 30,30,30,30
   ```

3. **Ambii:** Completați tabelul comparativ:

   | Aspect | FLSM | VLSM |
   |--------|------|------|
   | Prefix rezultat | | |
   | Gazde per subrețea | | |
   | Total gazde alocate | | |
   | Spațiu rămas | | |
   | Complexitate | | |

4. **Discuție:** În ce situații e mai bun FLSM? Când VLSM?

### Soluție

<details>
<summary>Click pentru soluție</summary>

Pentru cerințe identice, **FLSM și VLSM dau același rezultat**:
- Ambele: /26 per subrețea (62 gazde fiecare)
- Total alocat: 248 gazde
- Spațiu rămas: 8 adrese

**Concluzie:** VLSM aduce avantaj doar când cerințele diferă.

</details>

### ✓ Checkpoint

- [ ] Ambii înțelegeți când VLSM e mai eficient
- [ ] Ambii puteți explica de ce rezultatele sunt identice aici

---

## Exercițiul P4: Troubleshooting Docker Network

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 15 min | ★★★☆☆ | ANALYZE | Docker basics |

**Roluri:** Navigator diagnostichează, Driver execută

### Scenariu

Containerul `week5_python` nu poate comunica cu `week5_udp-server`.  
Trebuie să diagnosticați problema.

### Pași

1. **Driver:** Verifică starea containerelor:
   ```bash
   docker ps
   ```

2. **Navigator:** Dictează comenzile de diagnosticare:
   ```bash
   # Verifică rețelele
   docker network ls | grep week5
   
   # Inspectează rețeaua
   docker network inspect week5_labnet
   
   # Verifică IP-urile
   docker exec week5_python ip addr
   docker exec week5_udp-server ip addr
   ```

3. **Driver:** Testează conectivitatea:
   ```bash
   docker exec week5_python ping -c 3 10.5.0.20
   ```

4. **Ambii:** Documentați ce ați găsit:
   - Containerele sunt pe aceeași rețea?
   - IP-urile sunt cele așteptate?
   - Ping-ul funcționează?

5. **Dacă ping eșuează:** Navigator propune soluții, Driver le implementează.

### Checklist Diagnosticare

| Verificare | OK? | Acțiune dacă NU |
|------------|-----|-----------------|
| Containere pornite | ☐ | `docker compose up -d` |
| Aceeași rețea | ☐ | Verifică docker-compose.yml |
| IP-uri corecte | ☐ | Repornește containerele |
| Ping funcționează | ☐ | Verifică firewall |

---

## Exercițiul P5: IPv6 Hands-On

| ⏱️ Timp | 🧠 Complexitate | 📚 Nivel Bloom | 🔧 Prerequisite |
|---------|-----------------|----------------|-----------------|
| 15 min | ★★☆☆☆ | APPLY | Comprimare IPv6 |

**Roluri:** Alternativ la fiecare pas

### Scenariu

Firma primește prefixul IPv6 `2001:db8:acad::/48` și trebuie să creeze subrețele pentru 5 departamente.

### Pași

1. **Driver:** Generează subrețelele:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py subretele-ipv6 \
       "2001:db8:acad::/48" --numar 5
   ```

2. **Navigator:** Pentru fiecare subrețea, identifică:
   - Adresa de rețea
   - Prima adresă utilizabilă
   - Link-local address tipic

3. **Schimb roluri**

4. **Navigator (fost Driver):** Comprimă următoarele adrese:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-comprimare \
       "2001:0db8:acad:0001:0000:0000:0000:0001"
   ```

5. **Driver (fost Navigator):** Expandează:
   ```bash
   python3 src/exercises/ex_5_02_vlsm_ipv6.py ipv6-expandare \
       "2001:db8:acad:1::1"
   ```

6. **Verificare:** Rezultatele de la comprimare și expandare ar trebui să fie complementare.

---

## ✓ Checklist de Evaluare

După fiecare exercițiu, ambii parteneri completează:

| Criteriu | Driver | Navigator |
|----------|--------|-----------|
| Am comunicat clar | ☐ | ☐ |
| Am ascultat activ | ☐ | ☐ |
| Am învățat ceva nou | ☐ | ☐ |
| Am contribuit la soluție | ☐ | ☐ |

### Reflecție Finală

Discutați:
1. Care exercițiu a fost cel mai dificil? De ce?
2. Ce ați face diferit data viitoare?
3. Ce concept a devenit mai clar după lucrul în pereche?

---

## Navigare Rapidă

| ← Anterior | Document | Următor → |
|------------|----------|-----------|
| [Peer Instruction](peer_instruction.md) | **Exerciții Perechi** | [Exerciții Trace](exercitii_trace.md) |

## Documente Înrudite

- [README Principal](../README.md) — Ghid laborator
- [Peer Instruction](peer_instruction.md) — Întrebări MCQ
- [Exerciții Trace](exercitii_trace.md) — Non-coding
- [Referință API](api_reference.md) — Documentație funcții

---

*Material Pair Programming pentru Laborator Rețele de Calculatoare – ASE București*
