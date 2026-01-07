#!/usr/bin/env python3
"""
Controler IoT
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Se abonează la topicuri de senzori și procesează datele primite.
Poate declanșa acțiuni bazate pe praguri configurate.
"""

import argparse
import json
import sys
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[EROARE] paho-mqtt nu este instalat!")
    print("         Rulați: pip install paho-mqtt")
    sys.exit(1)


class ControlerIoT:
    """
    Controler pentru dispozitive IoT.
    
    Monitorizează senzori și declanșează acțiuni bazate pe praguri.
    """
    
    def __init__(self, praguri: dict = None):
        """
        Inițializează controlerul.
        
        Args:
            praguri: Dicționar cu praguri pentru alertare
        """
        self.praguri = praguri or {
            'temperatura_max': 30.0,
            'temperatura_min': 15.0,
            'umiditate_max': 80.0,
            'umiditate_min': 30.0
        }
        self.citiri = []
        self.alerte = []
    
    def proceseaza_mesaj(self, topic: str, payload: str):
        """
        Procesează un mesaj primit de la senzor.
        
        Args:
            topic: Topic-ul MQTT
            payload: Conținutul mesajului (JSON)
        """
        try:
            date = json.loads(payload)
        except json.JSONDecodeError:
            print(f"[EROARE] Payload invalid: {payload}")
            return
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        senzor_id = date.get('senzor_id', 'necunoscut')
        
        print(f"\n[{timestamp}] Date de la {senzor_id}")
        print(f"  Topic: {topic}")
        
        # Verifică temperatura
        if 'temperatura' in date:
            temp = date['temperatura']
            print(f"  Temperatură: {temp}°C", end="")
            
            if temp > self.praguri['temperatura_max']:
                print(f" ⚠️ ALERTĂ: Prea cald!")
                self._declanseaza_alerta('temperatura_ridicata', senzor_id, temp)
            elif temp < self.praguri['temperatura_min']:
                print(f" ⚠️ ALERTĂ: Prea frig!")
                self._declanseaza_alerta('temperatura_scazuta', senzor_id, temp)
            else:
                print(" ✓")
        
        # Verifică umiditatea
        if 'umiditate' in date:
            umid = date['umiditate']
            print(f"  Umiditate: {umid}%", end="")
            
            if umid > self.praguri['umiditate_max']:
                print(f" ⚠️ ALERTĂ: Umiditate ridicată!")
                self._declanseaza_alerta('umiditate_ridicata', senzor_id, umid)
            elif umid < self.praguri['umiditate_min']:
                print(f" ⚠️ ALERTĂ: Umiditate scăzută!")
                self._declanseaza_alerta('umiditate_scazuta', senzor_id, umid)
            else:
                print(" ✓")
        
        # Stochează citirea
        self.citiri.append({
            'timestamp': timestamp,
            'topic': topic,
            'date': date
        })
    
    def _declanseaza_alerta(self, tip: str, senzor: str, valoare: float):
        """Înregistrează o alertă."""
        alerta = {
            'timestamp': datetime.now().isoformat(),
            'tip': tip,
            'senzor': senzor,
            'valoare': valoare
        }
        self.alerte.append(alerta)
    
    def afiseaza_statistici(self):
        """Afișează statisticile sesiunii."""
        print("\n" + "=" * 50)
        print("STATISTICI CONTROLER")
        print("=" * 50)
        print(f"Total citiri procesate: {len(self.citiri)}")
        print(f"Total alerte generate:  {len(self.alerte)}")
        
        if self.alerte:
            print("\nUltimele alerte:")
            for alerta in self.alerte[-5:]:
                print(f"  - {alerta['tip']}: {alerta['valoare']} ({alerta['senzor']})")


def la_conectare(client, userdata, flags, rc, properties=None):
    """Callback la conectare."""
    if rc == 0:
        print("[CONECTAT] Controler conectat la broker")
        # Abonează la topicuri
        for topic in userdata.get('topicuri', ['senzori/#']):
            client.subscribe(topic, qos=1)
            print(f"[ABONAT] {topic}")
    else:
        print(f"[EROARE] Cod conectare: {rc}")


def la_mesaj(client, userdata, msg):
    """Callback la primirea mesajului."""
    controler = userdata.get('controler')
    if controler:
        controler.proceseaza_mesaj(msg.topic, msg.payload.decode('utf-8'))


def main():
    """Funcția principală."""
    parser = argparse.ArgumentParser(
        description="Controler IoT MQTT"
    )
    parser.add_argument("--broker", "-b", default="localhost",
                        help="Adresa broker-ului MQTT")
    parser.add_argument("--port", "-p", type=int, default=1883,
                        help="Portul broker-ului")
    parser.add_argument("--topicuri", "-t", nargs="+", default=["senzori/#"],
                        help="Topicuri pentru abonare")
    parser.add_argument("--temp-max", type=float, default=30.0,
                        help="Prag maxim temperatură")
    parser.add_argument("--temp-min", type=float, default=15.0,
                        help="Prag minim temperatură")
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("CONTROLER IoT")
    print("=" * 50)
    print(f"Broker:   {args.broker}:{args.port}")
    print(f"Topicuri: {', '.join(args.topicuri)}")
    print(f"Praguri:  Temp [{args.temp_min}°C - {args.temp_max}°C]")
    print("-" * 50)
    print("Apăsați Ctrl+C pentru a opri\n")
    
    # Creează controlerul
    controler = ControlerIoT(praguri={
        'temperatura_max': args.temp_max,
        'temperatura_min': args.temp_min,
        'umiditate_max': 80.0,
        'umiditate_min': 30.0
    })
    
    # Creează clientul MQTT
    userdata = {
        'controler': controler,
        'topicuri': args.topicuri
    }
    
    try:
        client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id="controler-iot",
            userdata=userdata
        )
    except (AttributeError, TypeError):
        client = mqtt.Client(client_id="controler-iot", userdata=userdata)
    
    client.on_connect = la_conectare
    client.on_message = la_mesaj
    
    try:
        client.connect(args.broker, args.port, keepalive=60)
        client.loop_forever()
            
    except KeyboardInterrupt:
        print("\n[INFO] Oprit de utilizator")
        controler.afiseaza_statistici()
    finally:
        client.disconnect()
        print("[DECONECTAT]")


if __name__ == "__main__":
    main()
