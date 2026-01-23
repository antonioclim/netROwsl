# Întrebări de Recapitulare - Săptămâna 3

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

Folosește aceste întrebări pentru auto-evaluare înainte și după laborator.

---

## REMEMBER (Reamintire)

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

**5.** Broadcast-ul limitat traversează routere?

<details><summary>Răspuns</summary>

**NU.** Adresa 255.255.255.255 rămâne strict în segmentul de rețea local. Routerele nu forwardează niciodată acest tip de broadcast.

</details>

### Multicast

**6.** În ce interval de adrese IP se află adresele multicast?

<details><summary>Răspuns</summary>

`224.0.0.0` - `239.255.255.255`

Pentru teste locale, folosește intervalul administrativ scoped: `239.x.x.x`

</details>

**7.** Ce protocol gestionează înscrierea în grupuri multicast?

<details><summary>Răspuns</summary>

**IGMP** (Internet Group Management Protocol)

- Join = Membership Report (0x16)
- Leave = Leave Group (0x17)
- Query = Membership Query (0x11)

</details>

**8.** Ce valoare TTL înseamnă "doar rețeaua locală" pentru multicast?

<details><summary>Răspuns</summary>

`TTL = 1` - pachetul nu traversează niciun router.

| TTL | Scop |
|-----|------|
| 0 | Doar localhost |
| 1 | Doar rețeaua locală |
| 32 | Organizație |
| 255 | Nelimitat |

</details>

**9.** Ce comandă Linux verifică grupurile multicast active?

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

**10.** Care sunt cele 3 tipuri de mesaje IGMP v2?

<details><summary>Răspuns</summary>

1. **Membership Query (0x11)** - Router-ul întreabă despre grupuri active
2. **Membership Report (0x16)** - Stația anunță înscrierea în grup
3. **Leave Group (0x17)** - Stația anunță părăsirea grupului

</details>

**11.** Ce prefix MAC au adresele multicast la Layer 2?

<details><summary>Răspuns</summary>

`01:00:5e:...`

Ultimii 23 de biți sunt derivați din ultimii 23 de biți ai adresei IP multicast.

Exemplu: 239.0.0.1 → 01:00:5e:00:00:01

</details>

### Tunel TCP

**12.** Câte conexiuni TCP menține un tunel TCP simplu pentru o cerere client?

<details><summary>Răspuns</summary>

**2 conexiuni separate:**
1. Client → Tunel
2. Tunel → Server

Tunelul copiază datele bidirecțional între cele două.

</details>

**13.** Ce IP sursă vede serverul când clientul se conectează prin tunel?

<details><summary>Răspuns</summary>

**IP-ul tunelului**, NU IP-ul clientului original.

Serverul nu știe cine este clientul real - vede doar tunelul ca și client.

</details>

### Mediu Docker/Portainer

**14.** Ce port folosește Portainer implicit?

<details><summary>Răspuns</summary>

**Port 9000** - http://localhost:9000

⚠️ Nu folosi niciodată portul 9000 pentru serviciile tale de laborator!

</details>

**15.** Ce comandă Docker afișează toate containerele, inclusiv cele oprite?

<details><summary>Răspuns</summary>

```bash
docker ps -a
```

Fără `-a` vezi doar containerele în starea Running.

</details>

---

## UNDERSTAND (Înțelegere)

Aceste întrebări verifică dacă înțelegi **de ce** funcționează lucrurile așa cum funcționează.

### Broadcast

**1.** De ce trebuie să faci bind la 0.0.0.0 pentru a primi broadcast, nu la IP-ul specific al mașinii?

<details><summary>Explicație</summary>

Kernelul sistemului de operare livrează pachetele broadcast doar la socket-urile legate la **INADDR_ANY (0.0.0.0)** sau la **adresa de broadcast**.

Când faci bind la un IP specific (ex: 192.168.1.5), kernelul filtrează pachetele și livrează doar pe cele adresate exact acelui IP. Un pachet trimis la 255.255.255.255 nu are destinația 192.168.1.5, deci nu va fi livrat.

**Analogie:** Dacă stai într-un colț specific al pieței, nu auzi megafonul. Trebuie să fii "în centrul pieței" (0.0.0.0) pentru a auzi toate anunțurile.

</details>

**2.** De ce SO_BROADCAST este necesar doar pentru emițător, nu și pentru receptor?

<details><summary>Explicație</summary>

SO_BROADCAST este o **protecție** la nivel de kernel pentru a preveni transmisia accidentală de broadcast. Este o acțiune activă, potențial perturbatoare.

Receptorul nu "face" nimic activ - doar ascultă ce vine pe rețea. Nu există risc în a asculta, deci nu e nevoie de permisiune specială.

**Analogie:** Ai nevoie de permis pentru a folosi megafonul (emițător), dar nu ai nevoie de permis pentru a avea urechi (receptor).

</details>

### Multicast

**3.** Explică diferența dintre broadcast și multicast din perspectiva eficienței folosirii lățimii de bandă.

<details><summary>Explicație</summary>

**Broadcast:**
- Emițătorul trimite 1 pachet
- TOATE dispozitivele din segment îl primesc și procesează
- Dispozitivele neinteresate ignoră pachetul DUPĂ ce l-au primit și procesat
- Overhead: CPU pe toate dispozitivele

**Multicast (cu IGMP snooping):**
- Emițătorul trimite 1 pachet
- Switch-ul știe ce porturi au membri și livrează DOAR acolo
- Dispozitivele neinteresate nu văd deloc pachetul
- Overhead: Zero pe dispozitivele nemembre

**Exemplu numeric:** 100 dispozitive, 10 interesate
- Broadcast: 100 procesează, 90 ignoră = 90% overhead
- Multicast: 10 procesează = 0% overhead

</details>

**4.** De ce multicast-ul poate traversa routere, dar broadcast-ul limitat nu?

<details><summary>Explicație</summary>

**Broadcast limitat (255.255.255.255):**
- Este o adresă specială care înseamnă "toți din acest segment"
- Nu are sens să fie forwardată - "toți" din alt segment sunt alt "toți"
- Routerele sunt proiectate să blocheze acest trafic by design

**Multicast:**
- Folosește adrese IP normale din intervalul 224.x.x.x - 239.x.x.x
- Routerele pot fi configurate să forwardeze trafic multicast (PIM, IGMP snooping)
- TTL controlează câte hopuri poate traversa
- Grupurile multicast pot avea membri în rețele diferite

</details>

**5.** Ce se întâmplă cu un pachet multicast când TTL ajunge la 0?

<details><summary>Explicație</summary>

Pachetul este **dropped (aruncat)** de router și NU se trimite ICMP Time Exceeded (spre deosebire de unicast).

**Motivul:** Multicast poate avea mii de destinatari. Dacă s-ar trimite ICMP Time Exceeded pentru fiecare pachet expirat, ar genera o "furtună" de trafic ICMP.

**Comportament TTL:**
- TTL=0: Pachetul nu părăsește mașina locală
- TTL=1: Pachetul ajunge în segmentul local, dar nu traversează routere
- La fiecare router: TTL este decrementat cu 1
- Când TTL=0 la un router: pachetul este silent dropped

</details>

### Tunel TCP

**6.** De ce un tunel TCP are două conexiuni separate, nu una singură?

<details><summary>Explicație</summary>

TCP este un protocol **end-to-end**. O conexiune TCP este identificată de:
- (IP sursă, Port sursă, IP destinație, Port destinație)

Tunelul este un **intermediar** care trebuie să:
1. Accepte conexiuni de la clienți (Conexiunea 1)
2. Inițieze conexiuni către server (Conexiunea 2)

Nu poate "prelungi" o conexiune existentă - trebuie să fie capăt pentru ambele:
- **Conexiunea 1:** Client ↔ Tunel (tunelul e server)
- **Conexiunea 2:** Tunel ↔ Server (tunelul e client)

Datele sunt copiate bidirecțional între cele două conexiuni.

</details>

**7.** De ce serverul vede IP-ul tunelului, nu IP-ul clientului original?

<details><summary>Explicație</summary>

Din perspectiva serverului, **tunelul este clientul**. Serverul nu are cum să știe că tunelul este doar un intermediar.

Conexiunea 2 (Tunel → Server) are:
- IP sursă: IP-ul tunelului
- Port sursă: portul alocat de tunelul pentru această conexiune

Aceasta este o consecință a modelului TCP end-to-end.

**Soluții pentru a păstra IP-ul original:**
- X-Forwarded-For header (la nivel HTTP)
- PROXY protocol (la nivel TCP)
- IP spoofing (necesită privilegii speciale)

</details>

---

## EVALUATE (Evaluare și Decizie)

Analizează scenariile și alege cea mai bună soluție.

### Scenariu 1: Descoperire Servicii

> Ai o aplicație care trebuie să găsească toate serverele disponibile în rețeaua locală, fără să cunoască IP-urile lor în prealabil.

**Întrebare:** Ce abordare alegi - broadcast sau multicast? Justifică.

<details>
<summary>Analiză completă</summary>

**Broadcast este mai potrivit** pentru acest scenariu:

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

**Multicast este clar superior:**

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

**Folosește un tunel TCP pe un bastion host:**

```
Internet → Bastion (IP public:9090) → Server intern (192.168.1.100:8080)
```

**Avantaje:**
- **Izolare:** Serverul intern nu are IP public
- **Logging centralizat:** Tot traficul trece prin tunel
- **Control acces:** Poți adăuga autentificare pe tunel
- **Rate limiting:** Protecție împotriva abuzului
- **Un singur punct de intrare:** Mai ușor de securizat

**Dezavantaje:**
- Single point of failure (rezolvabil cu redundanță)
- Latență adăugată (~1ms, neglijabil)

</details>

### Scenariu 4: TTL pentru Sincronizare Locală

> Dezvolți o aplicație de sincronizare care trebuie să funcționeze doar în cadrul unei singure clădiri (un singur segment de rețea fizică).

**Întrebare:** Ce TTL setezi și de ce?

<details>
<summary>Analiză completă</summary>

**TTL = 1**

**Rațiune:**
- Pachetele NU traversează niciun router
- Rămân strict în segmentul L2 local
- Previne "scurgerea" accidentală în alte rețele

⚠️ **Atenție:** Dacă clădirea are mai multe VLAN-uri cu routere între ele, TTL=1 NU va funcționa între VLAN-uri. În acest caz:
- TTL=2 pentru a traversa un router
- Sau folosește broadcast (care oricum nu traversează routere)

**Cod:**
```python
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
```

</details>

---

## Verificare Rapidă

Bifează ce poți răspunde corect fără ajutor:

**REMEMBER:**
- [ ] Știu care este adresa de broadcast limitat (255.255.255.255)
- [ ] Știu ce opțiune activează broadcast (SO_BROADCAST)
- [ ] Știu intervalul de adrese multicast (224.x - 239.x)
- [ ] Știu ce protocol gestionează grupurile multicast (IGMP)
- [ ] Știu ce adresă MAC are broadcast la Layer 2 (ff:ff:ff:ff:ff:ff)
- [ ] Știu ce valoare TTL înseamnă "doar localhost" (0)
- [ ] Știu ce port folosește Portainer (9000)
- [ ] Știu câte conexiuni TCP are un tunel (2)

**UNDERSTAND:**
- [ ] Pot explica DE CE receptorul trebuie să facă bind la 0.0.0.0
- [ ] Înțeleg DE CE multicast e mai eficient decât broadcast
- [ ] Pot explica DE CE serverul vede IP-ul tunelului, nu al clientului

**APPLY:**
- [ ] Pot scrie cod pentru a trimite un mesaj broadcast (3 linii esențiale)
- [ ] Pot scrie cod pentru a mă înscrie într-un grup multicast
- [ ] Pot identifica traficul broadcast/multicast în Wireshark

**Țintă:** Toate REMEMBER și UNDERSTAND bifate înainte de exerciții.

**Dacă ai < 10 bifate:** Recitește [Rezumatul Teoretic](rezumat_teoretic.md) și analogiile din README.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
