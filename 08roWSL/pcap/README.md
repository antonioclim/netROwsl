# Capturi de Pachet

> Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix

## Scop

Acest director stochează fișierele de captură de pachete (.pcap) generate în timpul exercițiilor de laborator.

## Capturare Trafic

### Folosind scriptul helper

```bash
python scripts/captureaza_trafic.py --interfata lo --iesire pcap/captura.pcap
```

### Folosind tcpdump

```bash
# Captură pe interfața loopback
sudo tcpdump -i lo port 8080 -w pcap/captura.pcap

# Limitare la 100 pachete
sudo tcpdump -i lo port 8080 -c 100 -w pcap/handshake.pcap
```

### Folosind Wireshark

1. Deschideți Wireshark
2. Selectați interfața "Loopback"
3. Aplicați filtrul: `port 8080`
4. Porniți captura
5. Salvați: File → Save As → pcap/captura.pcap

## Capturi Recomandate

| Fișier | Descriere | Filtru |
|--------|-----------|--------|
| handshake_tcp.pcap | Stabilire conexiune TCP | tcp.flags.syn == 1 |
| cerere_http.pcap | Cerere și răspuns HTTP | http |
| echilibrare.pcap | Distribuție între backend-uri | tcp.port == 8080 |
| handshake_tls.pcap | Negociere TLS (pentru tema HTTPS) | ssl |

## Analiză

Deschideți fișierele .pcap în Wireshark pentru analiză:

```bash
wireshark pcap/captura.pcap
```

## Curățare

Fișierele din acest director sunt șterse la curățarea completă:

```bash
python scripts/curatare.py --complet
```

---

*Cursul de REȚELE DE CALCULATOARE - ASE, Informatică Economică | de Revolvix*
