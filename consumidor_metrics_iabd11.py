from kafka import KafkaConsumer
from pymongo import MongoClient
import json
from datetime import datetime, timezone
import time

TOPIC_NAME = "system-metrics-topic-iabd11"
GROUP_ID = "grupo_iabd11_id"
MONGO_URI = "mongodb+srv://IABD11:iabdiabd11@basedatosaplicados.w7upd.mongodb.net/?retryWrites=true&w=majority&appName=BaseDatosAplicados"

client = MongoClient(MONGO_URI)
db = client["monitoring_iabd11"]
raw_collection = db["system_metrics_raw_iabd11"]
kpi_collection = db["system_metrics_kpis_iabd11"]

consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers="localhost:29092",
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=GROUP_ID,
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

print("🟢 Consumidor conectado. Esperando mensajes...")

window = []
start_time = time.time()

try:
    for message in consumer:
        metric = message.value
        raw_collection.insert_one(metric)
        window.append(metric)

        if len(window) == 20:
            end_time = time.time()
            duration = end_time - start_time
            kpi = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "window_duration_seconds": round(duration, 2),
                "num_messages": len(window),
                "cpu_avg": round(sum(m["metrics"]["cpu_percent"] for m in window) / 20, 2),
                "memory_avg": round(sum(m["metrics"]["memory_percent"] for m in window) / 20, 2),
                "disk_avg": round(sum(m["metrics"]["disk_io_mbps"] for m in window) / 20, 2),
                "network_avg": round(sum(m["metrics"]["network_mbps"] for m in window) / 20, 2),
                "total_errors": sum(m["metrics"]["error_count"] for m in window),
                "processing_rate_msgs_per_sec": round(20 / duration, 2)
            }
            kpi_collection.insert_one(kpi)
            print("📊 KPI calculado y almacenado:", kpi)
            window = []
            start_time = time.time()
except KeyboardInterrupt:
    print("🛑 Consumo detenido.")
finally:
    consumer.close()
    client.close()
