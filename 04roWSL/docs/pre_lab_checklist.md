# Checklist Pre-Laborator: Săptămâna 4

> Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix

Verifică aceste puncte **ÎNAINTE** de a veni la laborator pentru a evita pierderea timpului cu configurări.

---

## Mediu de Lucru (5 minute acasă)

### WSL2

- [ ] WSL2 este instalat și funcțional
  ```powershell
  wsl --version
  # Ar trebui să vezi "WSL version: 2.x.x"
  ```

- [ ] Ubuntu pornește fără erori
  ```powershell
  wsl -d Ubuntu
  # Ar trebui să vezi promptul: stud@CALCULATOR:~$
  ```

### Docker

- [ ] Docker este instalat în WSL
  ```bash
  docker --version
  # Ar trebui să vezi: Docker version 24.x sau mai nou
  ```

- [ ] Docker daemon poate fi pornit
  ```bash
  sudo service docker start
  docker ps
  # Ar trebui să funcționeze fără erori
  ```

### Portainer

- [ ] Portainer este accesibil la http://localhost:9000
- [ ] Poți face login cu `stud` / `studstudstud`

---

## Software Windows (verifică o singură dată)

- [ ] **Wireshark** instalat
  - Descarcă de la: https://www.wireshark.org/download.html
  - Verifică: caută "Wireshark" în meniul Start

- [ ] **Git** instalat (pentru clonare)
  ```powershell
  git --version
  ```

- [ ] **VS Code** sau alt editor (opțional dar recomandat)

---

## Cunoștințe Teoretice (10 minute citit)

Citește **înainte** de laborator:

- [ ] [Rezumat Teoretic](theory_summary.md) — conceptele de bază
- [ ] Secțiunea despre structura protocoalelor BINAR și TEXT

### Verificare rapidă — răspunde mental:

1. Care e diferența principală între TCP și UDP?
2. Ce face CRC32?
3. Ce înseamnă network byte order?
4. Câți bytes are antetul protocolului BINAR?

Dacă nu poți răspunde la acestea, recitește teoria.

---

## Pregătire Repository (5 minute)

- [ ] Repository-ul este clonat
  ```powershell
  cd D:\RETELE
  git clone https://github.com/antonioclim/netROwsl.git SAPT4
  ```

- [ ] Poți naviga la folder în WSL
  ```bash
  cd /mnt/d/RETELE/SAPT4/04roWSL
  ls
  # Ar trebui să vezi: docker/, scripts/, src/, README.md, etc.
  ```

---

## Verificare Finală (2 minute)

Rulează aceste comenzi pentru a verifica totul:

```bash
# În terminalul Ubuntu WSL
cd /mnt/d/RETELE/SAPT4/04roWSL

# Verifică Python
python3 --version
# Python 3.10+ necesar

# Verifică Docker
docker ps
# Ar trebui să funcționeze

# Verifică fișierele laboratorului
ls docker/
# Ar trebui să vezi: docker-compose.yml, Dockerfile
```

---

## Ce să faci dacă ceva nu funcționează

| Problemă | Soluție rapidă |
|----------|----------------|
| WSL nu pornește | `wsl --shutdown` apoi repornește |
| Docker nu pornește | `sudo service docker start` |
| Portainer nu răspunde | `docker start portainer` |
| Nu găsesc fișierele | Verifică `cd /mnt/d/RETELE/...` |

Pentru probleme mai complexe, consultă [Troubleshooting](troubleshooting.md).

---

## Timp Total Pregătire

| Activitate | Timp |
|------------|------|
| Verificare mediu | 5 min |
| Citire teorie | 10 min |
| Clonare repo | 5 min |
| **TOTAL** | **~20 min** |

---

## La Laborator — Primele 5 Minute

1. Deschide Ubuntu terminal
2. Pornește Docker: `sudo service docker start`
3. Navighează la folder: `cd /mnt/d/RETELE/SAPT4/04roWSL`
4. Pornește laboratorul: `python3 scripts/start_lab.py`
5. Verifică Portainer: http://localhost:9000

Dacă totul funcționează, ești gata să începi exercițiile!

---

*Curs REȚELE DE CALCULATOARE - ASE, Informatică Economică | realizat de Revolvix*
