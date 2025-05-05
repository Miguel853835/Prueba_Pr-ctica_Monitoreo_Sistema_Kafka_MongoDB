# Monitoreo de Métricas de Sistema con Kafka y MongoDB Atlas

Este proyecto simula un entorno de monitoreo en tiempo real para sistemas distribuidos, utilizando Kafka para la transmisión de métricas y MongoDB Atlas para su almacenamiento y análisis.

## 🧩 Componentes

- **Productor (productor_metrics_iabd11.py)**: Genera métricas simuladas para servidores ficticios y las publica en un tópico de Kafka.
- **Consumidor (consumidor_metrics_iabd11.py)**: Escucha mensajes del tópico Kafka, los guarda en MongoDB Atlas y calcula KPIs cada 20 mensajes.

## 🐳 Docker y Servicios

### Servicios utilizados:

- Kafka
- Zookeeper
- MongoDB Atlas (externo)

Los servicios de Kafka y Zookeeper se levantan con `docker-compose`.

## 🚀 Instrucciones

### 1. Clona el repositorio y entra en el directorio

```bash
git clone <repo-url>
cd <repo>
```

### 2. Levanta los servicios

```bash
docker-compose up -d
```

### 3. Ejecuta el Productor

```bash
docker build -t productor .
docker run --env KAFKA_BROKER=localhost:29092 --env KAFKA_TOPIC=system-metrics-topic-iabdXX productor
```

### 4. Ejecuta el Consumidor

```bash
docker build -t consumidor .
docker run --env KAFKA_BROKER=localhost:29092 --env KAFKA_TOPIC=system-metrics-topic-iabdXX --env MONGO_URI="mongodb+srv://..." consumidor
```

## 📊 KPIs Calculados

Cada 20 mensajes el consumidor calcula:

- Promedio de uso de CPU
- Promedio de uso de Memoria
- Promedio de E/S de disco
- Promedio de tráfico de red
- Suma de errores
- Tasa de procesamiento (msg/s)

Los resultados se guardan en `system_metrics_kpis_iabdXX` en MongoDB.

## 🛑 Manejo de SIGTERM

Ambos scripts manejan la señal `SIGTERM` para cerrar el proceso limpiamente cuando Docker detiene el contenedor.

## 🧪 Tests Básicos

Incluye scripts de prueba para verificar la conexión con Kafka y MongoDB.

---

Este proyecto es ideal para practicar el monitoreo de sistemas, el procesamiento en tiempo real y la integración con bases de datos NoSQL en la nube.
