# 👥 Ghid Pair Programming — Săptămâna 7
## Rețele de Calculatoare — ASE, CSIE | by Revolvix

---

## Ce este Pair Programming?

Pair programming este o tehnică în care **doi studenți lucrează împreună** la același cod, pe același calculator:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PAIR PROGRAMMING                                     │
├───────────────────────────────────┬─────────────────────────────────────────┤
│           DRIVER 🚗               │           NAVIGATOR 🗺️                 │
│  (la tastatură)                   │  (observă și ghidează)                  │
├───────────────────────────────────┼─────────────────────────────────────────┤
│  • Scrie codul                    │  • Verifică sintaxa                     │
│  • Explică ce face în timp ce     │  • Gândește la pasul următor            │
│    tastează                       │  • Propune îmbunătățiri                 │
│  • Implementează ideile           │  • Caută erori și bug-uri               │
│    navigatorului                  │  • Consultă documentația                │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

---

## Reguli de bază

1. **Schimbați rolurile la fiecare 10 minute** (folosiți un timer!)
2. **Comunicați constant** — tăcerea nu e permisă
3. **Respectați ideile partenerului** — nu există idei proaste
4. **Driver-ul nu ia decizii singur** — consultă Navigator-ul

---

## Exerciții Pair Programming — Săptămâna 7


### Exercițiul PP1: Filtru pachete simplu

**Timp:** 30 minute (3 rotații)

**Obiectiv:** Creați un script care parsează output-ul tcpdump.

**Cerințe:**
1. Rulează tcpdump pentru 5 secunde
2. Parsează output-ul și extrage IP-uri sursă
3. Numără câte pachete vin de la fiecare IP

**Driver începe cu:** Comanda subprocess pentru tcpdump
**Navigator ghidează:** Regex-ul pentru extragere IP-uri


---

## Întrebări de reflecție (după exercițiu)

1. Ce ai învățat de la partenerul tău?
2. Care rol ți s-a părut mai dificil: Driver sau Navigator?
3. Cum ai comunica mai bine data viitoare?
4. Ce greșeală ați evitat datorită pair programming?
