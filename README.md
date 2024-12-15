# Экспортер для системных метрик

Этот проект представляет собой экспортер для Prometheus, который собирает системные метрики, такие как загрузка процессоров, использование памяти и дисков. Экспортер предоставляет эти метрики в формате, совместимом с Prometheus, что упрощает мониторинг производительности вашей системы.

## Функциональность

- **Загрузка процессоров**: Показывает процент использования для каждого ядра процессора.
- **Использование памяти**: Отображает общий объём памяти и объём используемой памяти в мегабайтах (MB).
- **Использование дисков**: Отображает общий объём и объём используемого пространства для каждого подключенного диска в гигабайтах (GB).

## Требования

- Python 3.6+
- Prometheus
- Библиотека psutil

## Установка

1. Клонируйте репозиторий:
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Установите переменные окружения (необязательно):
   - `EXPORTER_HOST`: Адрес хоста для экспортера (по умолчанию: `localhost`).
   - `EXPORTER_PORT`: Порт для экспортера (по умолчанию: `8000`).

## Использование

1. Запустите экспортер:
   ```bash
   EXPORTER_HOST=localhost EXPORTER_PORT=8000 python exporter.py
   ```

2. Перейдите на страницу метрик в браузере или используйте curl:
   ```bash
   curl http://localhost:8000/
   ```

3. Настройте Prometheus для сбора метрик от экспортера. Добавьте следующий джоб в файл `prometheus.yml`:
   ```yaml
   scrape_configs:
     - job_name: 'system_metrics'
       static_configs:
         - targets: ['localhost:8000']
   ```

4. Перезапустите Prometheus, чтобы применить изменения.

## Метрики

Экспортер предоставляет следующие метрики:

### Метрики процессоров
- **`cpu_usage`**: Процент загрузки каждого ядра процессора.
  - Пример:
    ```
    cpu_usage{core="core_0"} 15.0
    cpu_usage{core="core_1"} 20.0
    ```

### Метрики памяти
- **`memory_total`**: Общий объём памяти в мегабайтах (MB).
  - Пример:
    ```
    memory_total 16292.1484375
    ```

- **`memory_used`**: Используемая память в мегабайтах (MB).
  - Пример:
    ```
    memory_used 9987.640625
    ```

### Метрики дисков
- **`disk_total`**: Общий объём диска в гигабайтах (GB), указанный для каждого диска.
  - Пример:
    ```
    disk_total{disk="/dev/sda1"} 465.0
    ```

- **`disk_used`**: Используемое пространство на диске в гигабайтах (GB), указано для каждого диска.
  - Пример:
    ```
    disk_used{disk="/dev/sda1"} 250.0
    ```

## Настройка

Вы можете изменить скрипт `exporter.py`, чтобы собирать дополнительные метрики или изменять интервал обновления данных. По умолчанию метрики обновляются каждые 10 секунд.=
