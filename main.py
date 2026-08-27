import json
import os

import paho.mqtt.client as mqtt
from dotenv import load_dotenv

from database import salvar_leitura

load_dotenv()


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        topic = os.getenv("MQTT_TOPIC")
        client.subscribe(topic)
        print(f"MQTT conectado | tópico: {topic}")
    else:
        print(f"Falha MQTT: {reason_code}")


def on_message(client, userdata, msg):
    try:
        dados = json.loads(msg.payload.decode("utf-8"))

        print(
            f"Recebido: {dados.get('id')} | "
            f"{dados.get('ts')} | "
            f"{dados.get('temp_c')} °C"
        )

        salvar_leitura(dados)

        print("Registro salvo no MySQL")

    except Exception as erro:
        print(f"Erro ao processar mensagem: {erro}")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="meteoflow-worker"
)

client.username_pw_set(
    os.getenv("MQTT_USER"),
    os.getenv("MQTT_PASSWORD")
)

client.tls_set()

client.on_connect = on_connect
client.on_message = on_message

print("MeteoFlow iniciado")

try:
    client.connect(
        os.getenv("MQTT_HOST"),
        int(os.getenv("MQTT_PORT", 8883)),
        60
    )

    client.loop_forever()

except KeyboardInterrupt:
    print("\nMeteoFlow encerrado pelo usuário.")
    client.disconnect()