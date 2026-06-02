# Sync Service Handler

Этот модуль реализует handler для синхронизации сообщений между микросервисами.

## Структура

```
sync_service/
├── app/
│   ├── handler/
│   │   ├── __init__.py          # Экспорт SyncHandler
│   │   ├── sync_handler.py      # Основной класс синхронизации
│   │   ├── main_handler.py      # Обработчик сообщений из Kafka
│   │   ├── node.py              # Функции для синхронизации узлов
│   │   ├── type.py              # Функции для синхронизации типов узлов
│   │   └── connection.py        # Функции для синхронизации связей
│   ├── schemas/
│   │   ├── nodetype_schemas.py  # Схемы для типов узлов
│   │   ├── node_schemas.py      # Схемы для узлов
│   │   └── connection_schemas.py # Схемы для связей
│   └── kafka/
│       ├── __init__.py
│       └── consumer.py          # Kafka consumer
├── main.py                      # Точка входа
├── requirements.txt
└── .env                         # Пример конфигурации
```

## Основные компоненты

### 1. SyncHandler

Основной класс для синхронизации между хостами. Получает список хостов из переменной окружения `SYNC_HOSTS`.

```python
from app.handler.sync_handler import SyncHandler
from app.schemas.node_schemas import NodeCreateParams

handler = SyncHandler()
params = NodeCreateParams(id=1, type_id=1, x=1.0, y=1.0, z=1.0, name="test")
results = await handler.sync_node_create(params)  # Вернет список результатов для каждого хоста
```

### 2. main_handler

Обработчик сообщений из Kafka. Автоматически маршрутизирует сообщения в соответствующие функции синхронизации.

### 3. Schemas

Все параметры передаются через Pydantic схемы:

- `NodeTypeCreateParams`, `NodeTypeDeleteParams`
- `NodeCreateParams`, `NodeUpdateParams`, `NodeDeleteParams`
- `ConnectionCreateParams`, `ConnectionUpdateParams`, `ConnectionDeleteParams`

## Использование

### Настройка переменных окружения

Создайте файл `.env` в директории sync_service:

```env
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_GROUP_ID=nav-consumer
KAFKA_TOPIC=nav-updates
SYNC_HOSTS=http://localhost:8001,http://localhost:8002
```

### Запуск

```bash
python -m sync_service.main
```

### Структура сообщений из Kafka

Сообщения должны быть в формате JSON:

```json
{
  "event": "NODE_CREATE",
  "data": {
    "id": 1,
    "type_id": 1,
    "x": 1.0,
    "y": 1.0,
    "z": 1.0,
    "latitude": 55.0,
    "longitude": 37.0,
    "name": "Test Node"
  }
}
```

Поддерживаемые события:
- `NODE_TYPE_CREATE`
- `NODE_TYPE_DELETE`
- `NODE_CREATE`
- `NODE_UPDATE`
- `NODE_DELETE`
- `CONNECTION_CREATE`
- `CONNECTION_UPDATE`
- `CONNECTION_DELETE`

## Принцип работы

1. Kafka consumer получает сообщение
2. `main_handler` парсит сообщение и определяет тип события
3. Соответствующая функция из `sync_handler` вызывается
4. `SyncHandler` проходит по списку хостов из `SYNC_HOSTS`
5. Для каждого хоста отправляется HTTP запрос с параметрами из схемы
6. Возвращается список результатов для каждого хоста

## Эндпоинты

Все запросы отправляются на эндпоинты `navigation_service`:

- `POST /sync/node-type` - создание типа узла
- `PUT /sync/node-type/{id}` - обновление типа узла
- `DELETE /sync/node-type/{id}` - удаление типа узла
- `POST /sync/node` - создание узла
- `PUT /sync/node/{id}` - обновление узла
- `DELETE /sync/node/{id}` - удаление узла
- `POST /sync/connection` - создание связи
- `PUT /sync/connection/{id}` - обновление связи
- `DELETE /sync/connection/{id}` - удаление связи
