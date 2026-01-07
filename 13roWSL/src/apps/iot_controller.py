#!/usr/bin/env python3
"""
Controller IoT
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Simulează un controller IoT care primește date de la senzori
prin MQTT și ia decizii de automatizare.

UTILIZARE:
    python iot_controller.py --broker localhost --port 1883
    python iot_controller.py --broker localhost --port 8883 --tls
"""

import argparse
import json
import ssl
import sys
import time
from datetime import datetime

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("[EROARE] Biblioteca paho-mqtt nu este instalată!")
    print("         Instalați cu: pip install paho-mqtt")
    sys.exit(1)


class ControllerIoT:
    """
    Controller IoT pentru automatizare bazată pe date de la senzori.
    
    Funcționalități:
    - Abonare la topicuri de senzori
    - Procesare date și luare decizii
    - Publicare comenzi către actuatoare
    """
    
    def __init__(self, broker: str, port: int, tls: bool = False, ca_cert: str = None):
        self.broker = broker
        self.port = port
        self.tls = tls
        self.ca_cert = ca_cert
        
        # Starea sistemului
        self.temperaturi = {}
        self.umiditate = {}
        self.praguri = {
            'temperatura_minima': 18.0,
            'temperatura_maxima': 26.0,
            'umiditate_minima': 30.0,
            'umiditate_maxima': 70.0
        }
        
        # Creează clientul MQTT
        try:
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=f"controller-{int(time.time())}"
            )
        except (AttributeError, TypeError):
            self.client = mqtt.Client(client_id=f"controller-{int(time.time())}")
        
        self.client.on_connect = self._la_conectare
        self.client.on_message = self._la_mesaj
        self.client.on_disconnect = self._la_deconectare
        
        # Configurează TLS
        if tls and ca_cert:
            self.client.tls_set(
                ca_certs=ca_cert,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS_CLIENT
            )
            self.client.tls_insecure_set(True)
    
    def _la_conectare(self, client, userdata, flags, rc, properties=None):
        """Callback la conectare."""
        if rc == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Conectat la broker")
            
            # Abonare la topicuri senzori
            topicuri = [
                "senzori/temperatura/#",
                "senzori/umiditate/#",
                "senzori/miscare/#"
            ]
            
            for topic in topicuri:
                client.subscribe(topic)
                print(f"  [ABONAT] {topic}")
        else:
            print(f"[EROARE] Conexiune eșuată: cod {rc}")
    
    def _la_deconectare(self, client, userdata, rc, properties=None):
        """Callback la deconectare."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Deconectat de la broker")
    
    def _la_mesaj(self, client, userdata, msg):
        """Callback la primirea unui mesaj."""
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        try:
            # Încearcă să parseze ca JSON
            payload = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            payload = msg.payload.decode()
        
        print(f"\n[{timestamp}] Mesaj primit:")
        print(f"  Topic: {msg.topic}")
        print(f"  Valoare: {payload}")
        
        # Procesează bazat pe tip
        if "temperatura" in msg.topic:
            self._proceseaza_temperatura(msg.topic, payload)
        elif "umiditate" in msg.topic:
            self._proceseaza_umiditate(msg.topic, payload)
        elif "miscare" in msg.topic:
            self._proceseaza_miscare(msg.topic, payload)
    
    def _proceseaza_temperatura(self, topic: str, valoare):
        """Procesează date de temperatură și ia decizii."""
        # Extrage identificatorul locației
        parti = topic.split('/')
        locatie = parti[-1] if len(parti) > 2 else "necunoscut"
        
        # Extrage valoarea numerică
        if isinstance(valoare, dict):
            temp = valoare.get('temp', valoare.get('temperatura', 0))
        else:
            try:
                temp = float(valoare)
            except ValueError:
                return
        
        self.temperaturi[locatie] = temp
        
        # Verifică pragurile
        if temp < self.praguri['temperatura_minima']:
            self._trimite_comanda("actuatoare/incalzire", {
                "actiune": "porneste",
                "locatie": locatie,
                "motiv": f"Temperatura {temp}°C sub pragul minim"
            })
        elif temp > self.praguri['temperatura_maxima']:
            self._trimite_comanda("actuatoare/racire", {
                "actiune": "porneste",
                "locatie": locatie,
                "motiv": f"Temperatura {temp}°C peste pragul maxim"
            })
    
    def _proceseaza_umiditate(self, topic: str, valoare):
        """Procesează date de umiditate."""
        parti = topic.split('/')
        locatie = parti[-1] if len(parti) > 2 else "necunoscut"
        
        if isinstance(valoare, dict):
            umid = valoare.get('umiditate', 0)
        else:
            try:
                umid = float(valoare)
            except ValueError:
                return
        
        self.umiditate[locatie] = umid
        
        if umid < self.praguri['umiditate_minima']:
            self._trimite_comanda("actuatoare/umidificator", {
                "actiune": "porneste",
                "locatie": locatie
            })
        elif umid > self.praguri['umiditate_maxima']:
            self._trimite_comanda("actuatoare/dezumidificator", {
                "actiune": "porneste",
                "locatie": locatie
            })
    
    def _proceseaza_miscare(self, topic: str, valoare):
        """Procesează detectarea mișcării."""
        parti = topic.split('/')
        locatie = parti[-1] if len(parti) > 2 else "necunoscut"
        
        if valoare in [True, 1, "1", "true", "detectat"]:
            self._trimite_comanda("actuatoare/lumini", {
                "actiune": "porneste",
                "locatie": locatie
            })
            self._trimite_comanda("alerte/miscare", {
                "locatie": locatie,
                "timestamp": datetime.now().isoformat()
            })
    
    def _trimite_comanda(self, topic: str, payload: dict):
        """Trimite o comandă către un actuator."""
        print(f"  [COMANDĂ] {topic}: {json.dumps(payload)}")
        self.client.publish(topic, json.dumps(payload))
    
    def porneste(self):
        """Pornește controller-ul."""
        print("=" * 50)
        print("CONTROLLER IoT - LABORATOR SĂPTĂMÂNA 13")
        print("=" * 50)
        print(f"Broker: {self.broker}:{self.port}")
        print(f"TLS: {'Da' if self.tls else 'Nu'}")
        print("-" * 50)
        print("Apăsați Ctrl+C pentru oprire\n")
        
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_forever()
        except KeyboardInterrupt:
            print("\n[INFO] Oprire controller...")
            self.client.disconnect()


def main():
    parser = argparse.ArgumentParser(description="Controller IoT")
    parser.add_argument("--broker", "-b", default="localhost")
    parser.add_argument("--port", "-p", type=int, default=1883)
    parser.add_argument("--tls", action="store_true")
    parser.add_argument("--ca-cert", default=None)
    
    args = parser.parse_args()
    
    controller = ControllerIoT(
        broker=args.broker,
        port=args.port,
        tls=args.tls,
        ca_cert=args.ca_cert
    )
    
    controller.porneste()


if __name__ == "__main__":
    main()
