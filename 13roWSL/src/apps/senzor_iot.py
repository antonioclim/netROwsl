#!/usr/bin/env python3
"""
Simulator Senzor IoT
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Simulează un senzor IoT care publică date periodic pe broker-ul MQTT.
"""

import argparse
import json
import random
import sys
import time
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[EROARE] paho-mqtt nu este instalat!")
    print("         Rulați: pip install paho-mqtt")
    sys.exit(1)


def genereaza_citire_temperatura(baza: float = 22.0, variatie: float = 3.0) -> float:
    """Generează o citire simulată de temperatură."""
    return round(baza + random.uniform(-variatie, variatie), 2)


def genereaza_citire_umiditate(baza: float = 50.0, variatie: float = 15.0) -> float:
    """Generează o citire simulată de umiditate."""
    return round(max(0, min(100, baza + random.uniform(-variatie, variatie))), 2)


def genereaza_mesaj_senzor(id_senzor: str, tip: str) -> dict:
    """
    Generează un mesaj de la senzor în format JSON.
    
    Args:
        id_senzor: Identificatorul unic al senzorului
        tip: Tipul senzorului ('temperatura', 'umiditate', 'ambele')
    
    Returns:
        Dicționar cu datele senzorului
    """
    mesaj = {
        "senzor_id": id_senzor,
        "timestamp": datetime.now().isoformat(),
    }
    
    if tip in ['temperatura', 'ambele']:
        mesaj["temperatura"] = genereaza_citire_temperatura()
        mesaj["unitate_temp"] = "°C"
    
    if tip in ['umiditate', 'ambele']:
        mesaj["umiditate"] = genereaza_citire_umiditate()
        mesaj["unitate_umid"] = "%"
    
    return mesaj


def la_conectare(client, userdata, flags, rc, properties=None):
    """Callback la conectare."""
    if rc == 0:
        print(f"[CONECTAT] Senzor conectat la broker")
    else:
        print(f"[EROARE] Cod conectare: {rc}")


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Simulator Senzor IoT MQTT"
    )
    parser.add_argument("--broker", "-b", default="localhost",
                        help="Adresa broker-ului MQTT")
    parser.add_argument("--port", "-p", type=int, default=1883,
                        help="Portul broker-ului")
    parser.add_argument("--topic", "-t", default="senzori/camera1",
                        help="Topic-ul de publicare")
    parser.add_argument("--id", default="senzor-01",
                        help="ID-ul senzorului")
    parser.add_argument("--tip", choices=["temperatura", "umiditate", "ambele"],
                        default="ambele", help="Tipul de date de generat")
    parser.add_argument("--interval", "-i", type=float, default=5.0,
                        help="Interval între citiri (secunde)")
    parser.add_argument("--numar", "-n", type=int, default=0,
                        help="Număr de citiri (0=infinit)")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("SIMULATOR SENZOR IoT")
    print("=" * 50)
    print(f"Broker:   {args.broker}:{args.port}")
    print(f"Topic:    {args.topic}")
    print(f"ID:       {args.id}")
    print(f"Tip:      {args.tip}")
    print(f"Interval: {args.interval}s")
    print("-" * 50)
    print("Apăsați Ctrl+C pentru a opri\n")
    
    # Creează clientul MQTT
    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"senzor-{args.id}"
        )
    except (AttributeError, TypeError):
        client = mqtt.Client(client_id=f"senzor-{args.id}")
    
    client.on_connect = la_conectare
    
    try:
        client.connect(args.broker, args.port, keepalive=60)
        client.loop_start()
        
        contor = 0
        while args.numar == 0 or contor < args.numar:
            mesaj = genereaza_mesaj_senzor(args.id, args.tip)
            payload = json.dumps(mesaj)
            
            client.publish(args.topic, payload, qos=1)
            
            print(f"[PUBLICAT] {args.topic}: {payload}")
            
            contor += 1
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n[INFO] Oprit de utilizator")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[DECONECTAT]")


if __name__ == "__main__":
    main()
