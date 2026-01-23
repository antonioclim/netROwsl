# 🎬 Ghid Live Coding pentru Instructori
## Rețele de Calculatoare — ASE, CSIE | by Revolvix

---

## 1. Ce este Live Coding?

Live coding este o tehnică de predare în care instructorul **scrie cod în timp real** în fața studenților, explicând fiecare decizie. Este fundamental diferit de a prezenta cod pre-scris deoarece:

- Studenții văd **procesul de gândire**, nu doar rezultatul
- Greșelile devin **momente de învățare**
- Ritmul este natural și permite întrebări

---

## 2. Structura unei sesiuni (15-20 minute)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CICLUL LIVE CODING                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  1. CONTEXT (2 min)                                                   │  │
│  │     "Astăzi vom crea un server TCP simplu. Scopul este să înțelegem   │  │
│  │      ordinea operațiilor: socket → bind → listen → accept"            │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  2. STRUCTURĂ (2 min)                                                 │  │
│  │     Schițează pe tablă/slide: "Vom avea 4 funcții principale:         │  │
│  │     crează_socket(), bind_la_port(), așteaptă_client(), trimite()"    │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  3. IMPLEMENTARE INCREMENTALĂ (10-15 min)                             │  │
│  │     ┌────────────────────────────────────────────────────────────┐   │  │
│  │     │  a) Scrie 2-5 linii de cod                                 │   │  │
│  │     │  b) ÎNTREABĂ: "Ce credeți că va afișa asta?"               │   │  │
│  │     │  c) Rulează și verifică predicțiile                        │   │  │
│  │     │  d) Explică rezultatul                                     │   │  │
│  │     │  e) REPETĂ                                                 │   │  │
│  │     └────────────────────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│                                    ▼                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  4. RECAPITULARE (2 min)                                              │  │
│  │     "Am creat un server TCP care: creează socket, se leagă la port,   │  │
│  │      așteaptă conexiuni, și procesează clienți."                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Regulile de Aur

### 3.1 GREȘEȘTE INTENȚIONAT

Planifică 1-2 greșeli pe sesiune:
```python
# GREȘEALĂ PLANIFICATĂ: uită să importe socket
# sock = socket.socket(...)  # NameError: name 'socket' is not defined

# "Hopa! Ce am uitat? Cine poate să-mi spună?"
# După corectare: "De ce e important să avem import-urile la început?"
```

### 3.2 CERE PREDICȚII CONSTANT

Înainte de FIECARE execuție:
```python
print("Conectat la server!")
# ÎNTREABĂ: "Ce se va întâmpla dacă serverul nu rulează?"
```

### 3.3 VORBEȘTE ÎN TIMP CE TASTEZI

```python
# "Acum creez un socket... folosesc AF_INET pentru IPv4..."
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# "...și SOCK_STREAM pentru TCP"
```

### 3.4 NU TE GRĂBI

- Mai bine acoperi 70% din materie și studenții înțeleg 90%
- Decât 100% din materie și studenții înțeleg 30%

### 3.5 FOLOSEȘTE COMENTARII PE LOC

```python
# TODO: Aici vom adăuga error handling
# HACK: Temporar folosim port fix, ideal ar fi dinamic
# ÎNTREBARE: De ce am ales portul 8080?
```

---

## 4. Checklist Pre-Sesiune

### Tehnic
- [ ] Am testat tot codul pe sistemul din sală?
- [ ] Docker rulează? Portainer e accesibil?
- [ ] Fontul în terminal e minim 18pt?
- [ ] Am dezactivat notificările pe ecran?
- [ ] Am backup la cod în caz că ceva se strică?

### Pedagogic
- [ ] Am pregătit 2-3 greșeli intenționate?
- [ ] Am pregătit 5-10 întrebări de predicție?
- [ ] Am identificat conceptele unde studenții greșesc tipic?
- [ ] Am timp buffer pentru întrebări (10% din sesiune)?

---

## 5. Exemple pe Săptămâni

### Săptămâna 1: ping și diagnoză

```python
# LIVE CODING: Script de verificare conectivitate

# PAS 1: "Să vedem dacă putem face ping din Python"
import subprocess

# ÎNTREBARE: "Ce comandă Linux face ping?"
result = subprocess.run(['ping', '-c', '1', 'google.com'], capture_output=True)

# PAS 2: "Ce cod de ieșire înseamnă succes?"
print(f"Return code: {result.returncode}")
# ÎNTREBARE: "0 înseamnă succes sau eșec?"

# GREȘEALĂ PLANIFICATĂ: Uită -c și ping rulează infinit
# "Hopa! Cum opresc asta? Ctrl+C! De ce a rulat la infinit?"
```

### Săptămâna 2: Socket TCP

```python
# LIVE CODING: Server Echo simplu

# PAS 1
import socket

# PAS 2: "Creăm socket-ul"
# ÎNTREBARE: "SOCK_STREAM sau SOCK_DGRAM pentru TCP?"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# PAS 3: "Ne legăm la port"
# GREȘEALĂ: Folosește un port ocupat (80)
# server.bind(('', 80))  # Permission denied!
# "De ce nu merge? Ce porturi necesită sudo?"

server.bind(('', 8080))
print("Bound to port 8080")

# PAS 4
server.listen(1)
# ÎNTREBARE: "Ce face parametrul 1 la listen()?"
```

### Săptămâna 8: HTTP Request

```python
# LIVE CODING: Parser HTTP Request simplu

# PAS 1
request = b"GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n"

# ÎNTREBARE: "Ce delimitează liniile în HTTP?"
lines = request.decode().split('\r\n')

# PAS 2
# ÎNTREBARE: "Care e prima linie și ce conține?"
first_line = lines[0]
method, path, version = first_line.split(' ')

print(f"Method: {method}")
print(f"Path: {path}")

# GREȘEALĂ PLANIFICATĂ: Uită de cazul când path-ul lipsește
# "Ce se întâmplă dacă clientul trimite cerere invalidă?"
```

---

## 6. Gestionarea Întrebărilor

### Întrebări bune (răspunde imediat):
- "De ce folosim port 8080 și nu 80?"
- "Ce se întâmplă dacă clientul se deconectează?"

### Întrebări care necesită amânare:
- "Cum funcționează TLS?" → "Excelentă întrebare! O vom acoperi în Săptămâna 10."

### Întrebări off-topic:
- "Putem face asta în Rust?" → "Interesant, dar hai să ne concentrăm pe Python acum. Vorbim la pauză."

---

## 7. După Sesiune

- [ ] Publică codul scris live (cu comentariile adăugate)
- [ ] Notează întrebările bune pentru viitoare sesiuni
- [ ] Notează ce a mers bine și ce de îmbunătățit
