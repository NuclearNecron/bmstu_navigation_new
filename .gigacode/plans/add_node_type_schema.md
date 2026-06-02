# План добавления NodeTypeCreateParams

## Задачи

1. **Добавить схему NodeTypeCreateParams в `object_models_schemas.py`**
   - Создать новый файл `node_type_schemas.py` или добавить в существующий
   - Добавить модель NodeTypeCreateParams с полями id, uni, campus, complex, corpus, building, floor, transit, room, exit_point

2. **Добавить метод в object_handler.py для рекурсивного сбора родителей**
   - Метод должен принимать id объекта
   - Использовать один SQL запрос с CTE для получения всей цепочки родителей
   - Возвращать структуру в формате NodeTypeCreateParams

## Реализация

### 1. Файл: `backend_op/app/schemas/object_models_schemas.py`

Добавить класс NodeTypeCreateParams в конец файла:

```python
class NodeTypeCreateParams(BaseModel):
    """Параметры для создания типа узла."""

    id: int
    uni: int | None = None
    campus: int | None = None
    complex: int | None = None
    corpus: int | None = None
    building: int | None = None
    floor: int | None = None
    transit: int | None = None
    room: int | None = None
    exit_point: int | None = None
```

### 2. Файл: `backend_op/app/handlers/object_handler.py`

Добавить метод `get_parent_chain` который будет:
- Принимать session и object_id
- Выполнять CTE запрос для получения всей цепочки родителей
- Собирать структуру с заполненными полями в зависимости от уровня объекта

```python
from sqlalchemy import text, bindparam

async def get_parent_chain(self, session: AsyncSession, object_id: int) -> NodeTypeCreateParams:
    """
    Рекурсивно собрать цепочку родителей объекта.
    
    Args:
        session: Асинхронная сессия SQLAlchemy
        object_id: Идентификатор объекта
        
    Returns:
        NodeTypeCreateParams с заполненными полями родителей
    """
    log.info("Собираем цепочку родителей для object_id=%s", object_id)
    
    # CTE запрос для получения всей цепочки родителей
    query = text("""
        WITH RECURSIVE parent_chain AS (
            SELECT id, parent_id, kind_id
            FROM object
            WHERE id = :object_id
            
            UNION ALL
            
            SELECT o.id, o.parent_id, o.kind_id
            FROM object o
            INNER JOIN parent_chain pc ON o.id = pc.parent_id
        )
        SELECT * FROM parent_chain ORDER BY id
    """)
    
    result = await session.execute(query, {"object_id": object_id})
    rows = result.fetchall()
    
    # Словарь для хранения родителей по уровням
    parents = {}
    
    for row in rows:
        # Определяем уровень по kind_id (нужно уточнить, как определяется уровень)
        # Пока используем простую логику: uni - верхний уровень
        parents[row.id] = {
            "id": row.id,
            "parent_id": row.parent_id,
            "kind_id": row.kind_id
        }
    
    # Собираем финальную структуру
    result_params = NodeTypeCreateParams(id=object_id)
    
    # Заполняем поля в зависимости от типа объекта (kind_id)
    # Нужно уточнить логику маппинга kind_id -> уровень (uni, campus, complex, etc.)
    
    return result_params
```

## Дополнительные замечания

- Нужно уточнить, как определяется уровень объекта (по kind_id или по другому признаку)
- Возможно потребуется создать таблицу справочник для маппинга kind_id на уровни
- Метод должен возвращать структуру с заполненными полями от object_id до uni
