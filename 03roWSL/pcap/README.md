# Director Capturi de Pachete

> Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix

## Scop

Acest director stochează fișierele de captură de pachete (`.pcap`) generate
în timpul laboratorului pentru analiză cu Wireshark.

## Convenție de Denumire

```
week3_<exercitiu>_<descriere>_<timestamp>.pcap
```

**Exemple:**
- `week3_broadcast_test_20240115_103000.pcap`
- `week3_multicast_igmp_20240115_104500.pcap`
- `week3_tunel_conectare_20240115_110000.pcap`

## Metode de Captură

### 1. Folosind Scriptul de Captură

```powershell
python scripts/captureaza_trafic.py --container server --durata 30 --output pcap/captura.pcap
```

### 2. tcpdump Direct în Container

```bash
# Pornire captură
docker exec week3_client tcpdump -i eth0 -w /tmp/captura.pcap

# Copiere fișier
docker cp week3_client:/tmp/captura.pcap pcap/captura.pcap
```

### 3. Wireshark pe Windows

1. Deschideți Wireshark
2. Selectați interfața asociată cu Docker/WSL
3. Aplicați filtrele de captură necesare
4. Salvați în acest director

## Filtre de Captură Recomandate

| Exercițiu | Filtru |
|-----------|--------|
| Broadcast | `port 5007` |
| Multicast | `port 5008 or igmp` |
| Tunel TCP | `port 8080 or port 9090` |
| Tot lab | `net 172.20.0.0/24` |

## Dimensiuni Fișiere

- **Tipic:** 100KB - 1MB per sesiune de captură
- **Maxim recomandat:** 50MB (pentru trimitere)
- **Curățare:** Ștergeți capturile vechi înainte de următorul laborator

## Curățare

```powershell
# Șterge toate capturile (păstrează README)
python scripts/curata.py --complet
```

## Trimitere pentru Teme

Dacă tema cere o captură demonstrativă:
1. Păstrați fișierul sub 5MB
2. Includeți doar traficul relevant
3. Denumiți clar: `tema_3_X_nume_student.pcap`

## Depanare

### Fișier gol (0 bytes)

- Verificați că există trafic în timpul capturii
- Verificați interfața de captură

### Pachete lipsă

- Asigurați-vă că captura include și traficul dorit
- Verificați filtrele de captură

### Permisiuni

Pe Linux/WSL, tcpdump poate necesita sudo sau capabilities speciale.

---

*Laborator Rețele de Calculatoare - ASE, Informatică Economică | by Revolvix*
