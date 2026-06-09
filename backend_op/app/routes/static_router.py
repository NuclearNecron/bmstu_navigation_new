"""Роутер для раздачи статических файлов (изображений)."""

import os
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import FileResponse

router = APIRouter(prefix="/static", tags=["Static Files"])

# Папка для хранения загруженных файлов - относительно корня проекта
PROJECT_ROOT = Path(__file__).parent.parent.parent
STATIC_DIR = PROJECT_ROOT / "static"
STATIC_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузка файла на сервер."""
    # Проверка расширения файла (только изображения)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
    file_path = Path(file.filename)
    
    if file_path.suffix.lower() not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Недопустимый формат файла. Разрешены: {', '.join(allowed_extensions)}"
        )
    
    # Генерация уникального имени файла (добавляем timestamp)
    import time
    unique_filename = f"{int(time.time())}_{file.filename}"
    destination_path = STATIC_DIR / unique_filename
    
    try:
        with open(destination_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении файла: {str(e)}")
    
    return {
        "filename": unique_filename,
        "url": f"/static/files/{unique_filename}",
        "message": "Файл успешно загружен"
    }


@router.get("/files/{filename}")
async def get_file(filename: str):
    """Получение файла по имени."""
    file_path = STATIC_DIR / filename
    
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    return FileResponse(file_path)


@router.delete("/files/{filename}")
async def delete_file(filename: str):
    """Удаление файла."""
    file_path = STATIC_DIR / filename
    
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail="Файл не найден")
    
    try:
        file_path.unlink()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при удалении файла: {str(e)}")
    
    return {"message": f"Файл '{filename}' успешно удален"}
