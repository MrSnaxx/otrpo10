from prometheus_client import Gauge, start_http_server
import psutil
import time
import os

# Метрики для процессоров
cpu_usage = Gauge("cpu_usage", "CPU usage per core", ['core'])

# Метрики для памяти
memory_total = Gauge("memory_total", "Total memory in MB")
memory_used = Gauge("memory_used", "Used memory in MB")

# Метрики для дисков
disk_total = Gauge("disk_total", "Total disk space per disk in GB", ['disk'])
disk_used = Gauge("disk_used", "Used disk space per disk in GB", ['disk'])

def collect_metrics():
    # Сбор данных о загрузке CPU
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        cpu_usage.labels(core=f"core_{i}").set(percentage)

    # Сбор данных о памяти
    memory_info = psutil.virtual_memory()
    memory_total.set(memory_info.total / (1024 ** 2))  # Преобразование в MB
    memory_used.set(memory_info.used / (1024 ** 2))    # Преобразование в MB

    # Сбор данных о дисках
    partitions = psutil.disk_partitions()
    for partition in partitions:
        try:
            disk_info = psutil.disk_usage(partition.mountpoint)
            disk_name = partition.device  # Имя диска
            disk_total.labels(disk=disk_name).set(disk_info.total / (1024 ** 3))  # Преобразование в GB
            disk_used.labels(disk=disk_name).set(disk_info.used / (1024 ** 3))    # Преобразование в GB
        except PermissionError:
            # Если доступ к диску запрещён, пропускаем его
            continue

if __name__ == "__main__":
    # Читаем переменные окружения для хоста и порта
    host = os.getenv("EXPORTER_HOST", "localhost")
    port = int(os.getenv("EXPORTER_PORT", 8000))

    # Запускаем HTTP-сервер Prometheus
    print(f"Starting exporter on {host}:{port}")
    start_http_server(port, addr=host)

    # Обновляем метрики каждые 10 секунд
    while True:
        collect_metrics()
        time.sleep(10)
