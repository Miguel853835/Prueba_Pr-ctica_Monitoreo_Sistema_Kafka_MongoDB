import random
import time
from datetime import datetime, timezone
import uuid
import json
from kafka import KafkaProducer

# --- Configuración ---
SERVER_IDS = ["web01", "web02", "db01", "app01", "cache01"]
REPORTING_INTERVAL_SECONDS = 10
TOPIC_NAME = "system-metrics-topic-iabd11"

producer = KafkaProducer(
    bootstrap_servers="localhost:29092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

if __name__ == "__main__":
    print("Iniciando simulación de generación de métricas...")
    try:
        while True:
            print(f"\n{datetime.now()}: Generando reporte de métricas...")
            for server_id in SERVER_IDS:
                cpu = random.uniform(5.0, 75.0)
                if random.random() < 0.1:
                    cpu = random.uniform(85.0, 98.0)
                memory = random.uniform(20.0, 85.0)
                if random.random() < 0.05:
                    memory = random.uniform(90.0, 99.0)
                disk = random.uniform(0.1, 50.0)
                net = random.uniform(1.0, 100.0)
                errors = random.randint(1, 3) if random.random() < 0.08 else 0

                metric_message = {
                    "server_id": server_id,
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "metrics": {
                        "cpu_percent": round(cpu, 2),
                        "memory_percent": round(memory, 2),
                        "disk_io_mbps": round(disk, 2),
                        "network_mbps": round(net, 2),
                        "error_count": errors
                    },
                    "message_uuid": str(uuid.uuid4())
                }

                producer.send(TOPIC_NAME, metric_message)
                print(f"✅ Enviada métrica de {server_id} a Kafka.")

            print(f"\n⏳ Esperando {REPORTING_INTERVAL_SECONDS} segundos...")
            time.sleep(REPORTING_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n🛑 Simulación detenida por el usuario.")
    finally:
        producer.close()
        print("\n🛑 El productor se ha detenido correctamente.")
