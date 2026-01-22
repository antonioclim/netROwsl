# Întrebări de Recapitulare - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Folosește aceste întrebări pentru auto-evaluare înainte și după laborator.

---

## 🧠 REMEMBER (Reamintire)

Răspunde fără să te uiți în documentație. Dacă nu știi, recitește [Rezumatul Teoretic](rezumat_teoretic.md).

### Broadcast

**1.** Ce opțiune socket trebuie activată pentru a trimite broadcast?

<details><summary>Răspuns</summary>

`SO_BROADCAST` - se setează cu:
```python
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
```

</details>

**2.** Care este adresa de broadcast limitat în IPv4?

<details><summary>Răspuns</summary>

`255.255.255.255` - nu traversează niciodată routerele.

</details>

**3.** La ce adresă trebuie să faci bind() pentru a primi mesaje broadcast?

<details><summary>Răspuns</summary>

`0.0.0.0` (toate interfețele) - NU la o adresă IP specifică!

```python
sock.bind(('0.0.0.0', port))  # Corect
sock.bind(('192.168.1.5', port))  # Greșit pentru broadcast
```

</details>

**4.** Ce adresă MAC are un pachet broadcast la Layer 2?

<details><summary>Răspuns</summary>

`ff:ff:ff:ff:ff:ff` - toate biturile setate la 1.

</details>

### Multicast

**5.** În ce interval de adrese IP se află adresele multicast?

<details><summary>Răspuns</summary>

`224.0.0.0` - `239.255.255.255`

Pentru teste locale, folosește intervalul administrativ scoped: `239.x.x.x`

</details>

**6.** Ce protocol gestionează înscrierea în grupuri multicast?

<details><summary>Răspuns</summary>

**IGMP** (Internet Group Management Protocol)

- Join = Membership Report (0x16)
- Leave = Leave Group (0x17)

</details>

**7.** Ce valoare TTL înseamnă "doar rețeaua locală" pentru multicast?

<details><summary>Răspuns</summary>

`TTL = 1` - pachetul nu traversează niciun router.

| TTL | Scop |
|-----|------|
| 0 | Doar localhost |
| 1 | Doar rețeaua locală |
| 32 | Organizație |
| 255 | Nelimitat |

</details>

**8.** Ce comandă Linux verifică grupurile multicast active?

<details><summary>Răspuns</summary>

```bash
cat /proc/net/igmp
# sau
ip maddr show
```

În containere Docker:
```bash
docker exec container_name cat /proc/net/igmp
```

</details>

### Tunel TCP

**9.** Câte conexiuni TCP menține un tunel TCP simplu pentru o cerere client?

<details><summary>Răspuns</summary>

**2 conexiuni separate:**
1. Client → Tunel
2. Tunel → Server

Tunelul copiază datele bidirecțional între cele două.

</details>

**10.** Ce IP sursă vede serverul când clientul se conectează prin tunel?

<details><summary>Răspuns</summary>

**IP-ul tunelului**, NU IP-ul clientului original.

Serverul nu știe cine este clientul real - vede doar tunelul ca și client.

</details>

---

## ⚖️ EVALUATE (Evaluare și Decizie)

Analizează scenariile și alege cea mai bună soluție.

### Scenariu 1: Descoperire Servicii

> Ai o aplicație care trebuie să găsească toate serverele disponibile în rețeaua locală, fără să cunoască IP-urile lor în prealabil.

**Întrebare:** Ce abordare alegi - broadcast sau multicast? Justifică.

<details>
<summary>Analiză completă</summary>

**✅ Broadcast este mai potrivit** pentru acest scenariu:

| Criteriu | Broadcast | Multicast |
|----------|-----------|-----------|
| Configurare prealabilă | Nu necesită | Serverele trebuie să se înscrie în grup |
| Descoperire | Automată, toți răspund | Doar membrii grupului |
| Complexitate | Simplă | Mai complexă (IGMP) |

**Concluzie:** Pentru descoperire unde nu știi cine există, broadcast-ul este soluția naturală. Multicast ar necesita ca serverele să cunoască deja grupul predefinit.

**Exemple reale:** DHCP folosește broadcast pentru descoperire inițială.

</details>

### Scenariu 2: Streaming Video Intern

> Compania ta vrea să transmită un stream video live către 50 de angajați din diferite departamente, dar nu către toți cei 200 din rețea.

**Întrebare:** Broadcast sau multicast? De ce?

<details>
<summary>Analiză completă</summary>

**✅ Multicast este clar superior:**

| Criteriu | Broadcast | Multicast |
|----------|-----------|-----------|
| Cine primește | Toți 200 | Doar cei 50 abonați |
| Trafic de rețea | 200× procesare | 1× transmisie, 50× recepție |
| Overhead CPU | Foarte mare | Mic |
| Scalabilitate | Proastă | Excelentă |

**Calcul eficiență:**
- Broadcast: Sursa trimite 1 pachet → 200 dispozitive procesează → 150 ignoră
- Multicast: Sursa trimite 1 pachet → Switch-ul livrează doar la 50 → 0 procesare inutilă

**Concluzie:** Pentru distribuție către un subset cunoscut de receptori, multicast optimizează lățimea de bandă și CPU-ul.

</details>

### Scenariu 3: Expunere Server Intern

> Ai un server intern (192.168.1.100:8080) pe care vrei să-l expui clienților externi, dar fără să le dai acces direct la rețeaua internă.

**Întrebare:** Cum rezolvi? Ce avantaje oferă tunelul?

<details>
<summary>Analiză completă</summary>

**✅ Folosește un tunel TCP pe un bastion host:**

```
Internet → Bastion (IP public:9090) → Server intern (192.168.1.100:8080)
```

**Avantaje:**
1. **Izolare:** Serverul intern nu are IP public
2. **Logging centralizat:** Tot traficul trece prin tunel
3. **Control acces:** Poți adăuga autentificare pe tunel
4. **Rate limiting:** Protecție împotriva abuzului
5. **Un singur punct de intrare:** Mai ușor de securizat

**Dezavantaje:**
- Single point of failure (rezolvabil cu redundanță)
- Latență adăugată (~1ms, neglijabil)

</details>

### Scenariu 4: TTL pentru Sincronizare Locală

> Dezvolți o aplicație de sincronizare care trebuie să funcționeze doar în cadrul unei singure clădiri (un singur segment de rețea fizică).

**Întrebare:** Ce TTL setezi și de ce?

<details>
<summary>Analiză completă</summary>

**✅ TTL = 1**

**Rațiune:**
- Pachetele NU traversează niciun router
- Rămân strict în segmentul L2 local
- Previne "scurgerea" accidentală în alte rețele

**⚠️ Atenție:** Dacă clădirea are mai multe VLAN-uri cu routere între ele, TTL=1 NU va funcționa între VLAN-uri. În acest caz:
- TTL=2 pentru a traversa un router
- Sau folosește broadcast (care oricum nu traversează routere)

**Cod:**
```python
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
```

</details>

---

## 🎯 Verificare Rapidă

Bifează ce poți răspunde corect fără ajutor:

- [ ] Știu diferența dintre broadcast limitat și direcționat
- [ ] Pot scrie cod pentru a trimite un mesaj broadcast (3 linii esențiale)
- [ ] Știu cum să mă înscriu într-un grup multicast cu Python (struct.pack + setsockopt)
- [ ] Înțeleg ce face TTL pentru pachete multicast
- [ ] Pot explica când să aleg broadcast vs multicast
- [ ] Știu câte conexiuni TCP menține un tunel și de ce
- [ ] Pot identifica traficul broadcast/multicast în Wireshark

**Țintă:** Toate bifate înainte de a trece la exerciții.

**Dacă ai < 5 bifate:** Recitește [Rezumatul Teoretic](rezumat_teoretic.md) și analogiile din README.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
