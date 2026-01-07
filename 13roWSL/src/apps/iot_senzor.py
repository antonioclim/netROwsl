#!/usr/bin/env python3
"""
Senzor IoT Simulat
Curs REȚELE DE CALCULATOARE - ASE, Informatică | de Revolvix

Simulează un senzor IoT care publică periodic date
de temperatură și umiditate prin MQTT.

UTILIZARE:
    python iot_sensor.py --broker localhost --port 1883 --locatie camera1
    python iot_sensor.py --broker localhost --port 8883 --tls --interval 5
"""

import argparse
import json
import random
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


class SenzorIoT:
    """
    Simulare senzor IoT pentru temperatură și umiditate.
    
    Publică date pe topicuri MQTT la intervale regulate.
    """
    
    def __init__(self, broker: str, port: int, locatie: str,
                 tls: bool = False, ca_cert: str = None):
        self.broker = broker
        self.port = port
        self.locatie = locatie
        self.tls = tls
        
        # Valori inițiale
        self.temperatura = 22.0
        self.umiditate = 50.0
        
        # Creează clientul MQTT
        try:
            self.client = mqtt.Client(
                callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                client_id=f"senzor-{locatie}-{int(time.time())}"
            )
        except (AttributeError, TypeError):
            self.client = mqtt.Client(client_id=f"senzor-{locatie}-{int(time.time())}")
        
        self.client.on_connect = self._la_conectare
        self.client.on_disconnect = self._la_deconectare
        
        # Configurează TLS
        if tls and ca_cert:
            self.client.tls_set(
                ca_certs=ca_cert,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLS_CLIENT
            )
            self.client.tls_insecure_set(True)
        
        self.conectat = False
    
    def _la_conectare(self, client, userdata, flags, rc, properties=None):
        """Callback la conectare."""
        if rc == 0:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Conectat la broker")
            self.conectat = True
        else:
            print(f"[EROARE] Conexiune eșuată: cod {rc}")
    
    def _la_deconectare(self, client, userdata, rc, properties=None):
        """Callback la deconectare."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Deconectat de la broker")
        self.conectat = False
    
    def _genereaza_temperatura(self) -> float:
        """Generează o valoare de temperatură simulată."""
        # Variație aleatoare mică
        variatie = random.uniform(-0.5, 0.5)
        self.temperatura += variatie
        
        # Menține în intervalul realist
        self.temperatura = max(15.0, min(30.0, self.temperatura))
        
        return round(self.temperatura, 1)
    
    def _genereaza_umiditate(self) -> float:
        """Generează o valoare de umiditate simulată."""
        variatie = random.uniform(-2.0, 2.0)
        self.umiditate += variatie
        
        self.umiditate = max(20.0, min(80.0, self.umiditate))
        
        return round(self.umiditate, 1)
    
    def publica(self):
        """Publică datele curente ale senzorului."""
        timestamp = datetime.now().isoformat()
        
        # Date temperatură
        date_temp = {
            "temp": self._genereaza_temperatura(),
            "unitate": "C",
            "locatie": self.locatie,
            "timestamp": timestamp
        }
        
        # Date umiditate
        date_umid = {
            "umiditate": self._genereaza_umiditate(),
            "unitate": "%",
            "locatie": self.locatie,
            "timestamp": timestamp
        }
        
        # Publică
        topic_temp = f"senzori/temperatura/{self.locatie}"
        topic_umid = f"senzori/umiditate/{self.locatie}"
        
        self.client.publish(topic_temp, json.dumps(date_temp))
        self.client.publish(topic_umid, json.dumps(date_umid))
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Publicat:")
        print(f"  {topic_temp}: {date_temp['temp']}°C")
        print(f"  {topic_umid}: {date_umid['umiditate']}%")
    
    def porneste(self, interval: int = 10):
        """
        Pornește senzorul și publică la intervale regulate.
        
        Args:
            interval: Interval între publicări în secunde
        """
        print("=" * 50)
        print("SENZOR IoT - LABORATOR SĂPTĂMÂNA 13")
        print("=" * 50)
        print(f"Broker: {self.broker}:{self.port}")
        print(f"Locație: {self.locatie}")
        print(f"Interval: {interval} secunde")
        print(f"TLS: {'Da' if self.tls else 'Nu'}")
        print("-" * 50)
        print("Apăsați Ctrl+C pentru oprire\n")
        
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            
            # Așteaptă conectarea
            time.sleep(1)
            
            while True:
                if self.conectat:
                    self.publica()
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[INFO] Oprire senzor...")
        finally:
            self.client.loop_stop()
            self.client.disconnect()


def main():
    parser = argparse.ArgumentParser(description="Senzor IoT Simulat")
    parser.add_argument("--broker", "-b", default="localhost")
    parser.add_argument("--port", "-p", type=int, default=1883)
    parser.add_argument("--locatie", "-l", default="camera1",
                        help="Identificatorul locației senzorului")
    parser.add_argument("--interval", "-i", type=int, default=10,
                        help="Interval publicare în secunde")
    parser.add_argument("--tls", action="store_true")
    parser.add_argument("--ca-cert", default=None)
    
    args = parser.parse_args()
    
    senzor = SenzorIoT(
        broker=args.broker,
        port=args.port,
        locatie=args.locatie,
        tls=args.tls,
        ca_cert=args.ca_cert
    )
    
    senzor.porneste(args.interval)


if __name__ == "__main__":
    main()
