# Imagini pentru Documentație

> Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix

Acest folder ar trebui să conțină screenshot-uri pentru documentație.

## Screenshot-uri Recomandate

### Pentru Portainer

1. **portainer_dashboard.png** — Pagina principală după login
2. **portainer_containers.png** — Lista containerelor s11_*
3. **portainer_network.png** — Vizualizarea rețelei s11_network
4. **portainer_logs.png** — Exemplu de vizualizare log-uri

### Pentru Wireshark

5. **wireshark_interface.png** — Selectarea interfeței vEthernet (WSL)
6. **wireshark_http.png** — Captură trafic HTTP cu filtrul tcp.port == 8080
7. **wireshark_dns.png** — Captură trafic DNS

## Cum să Creezi Screenshot-uri

### Windows (Portainer, Wireshark)

1. Deschide aplicația
2. Apasă `Win + Shift + S` pentru Snipping Tool
3. Selectează zona dorită
4. Salvează în acest folder cu numele specificat

### Din WSL (opțional)

```bash
# Instalează scrot
sudo apt install scrot

# Face screenshot
scrot screenshot.png
```

## Note

- Dimensiune recomandată: 800x600 sau 1024x768
- Format: PNG (preferabil) sau JPG
- Evitați informații sensibile în screenshot-uri

---

*Laborator Rețele de Calculatoare — ASE, Informatică Economică | de Revolvix*
