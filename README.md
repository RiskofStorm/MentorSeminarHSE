# MentorSeminarHSE
final project of mentor's seminar in first semester of master degree

# Как работать с репозиторием 

## 1. Склонировать репозиторий  

```bash
git clone https://github.com/RiskofStorm/MentorSeminarHSE.git
```
## 2. Краткое описание приложений и их эндпоинтов
<b>TODO-сервис</b>  - Реализует CRUD-операции для списка задач с
хранением данных в SQLite
```commandline
 Эндпоинты:
– POST /items: Создание задачи (title, description?, completed=false).
– GET /items: Получение списка всех задач.
– GET /items/{item_id}: Получение задачи по ID.
– PUT /items/{item_id}: Обновление задачи по ID.
– DELETE /items/{item_id}: Удаление задачи.

```
<b>Short_ulr_app</b> -Позволяет создавать короткие  
ссылки для длинных URL, перенаправлять по короткому  
идентификатору и предоставлять информацию о ссылке.  
Также хранение данных в SQLite    
  
```  
 Эндпоинты:
- POST /shorten: Принимает полный URL (JSON: {"url":"..."}) и возвращает короткую ссылку.  
- GET /{short_id}: Перенаправляет на полный URL, если он существует.  
- GET /
```
## 3. Запуск приложений локально

1. В консоли перейти в папку любого приложения
2. Выполнить команды:
Создаем виртуальное окружение:
```commandline
python -m venv venv
```
Активируем его:
```bash
Linux: source venv/bin/activate
```
```commandline
Windows PowerShell: ./venv/Sripts/activate.ps1
```
И установить зависимости приложения: 
```bash
python3 -m pip install --upgrade pip
```

```bash
pip install -r requirements.txt
```
Для запуска приложений выполнить команду:

<b>Находясь в папке TODO-сервис</b>
```commandline
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

<b>Находясь в папке Short_ulr_app и другой открытой консоли </b>
```commandline
python -m uvicorn main:app --host 0.0.0.0 --port 8001
```

## 4. Сборка docker образа
#### Убедитесь, что текущая директория в командной строке - это папка приложения с dockerfile 

<b>TODO-сервис</b>

```

docker build -t riskofstorm/todo_service_app .

```

<b>Short_ulr_app</b>

```

docker build -t riskofstorm/shorturl_app .

```

## 5. Запуск docker образов

<b>TODO-сервис</b>

```bash
docker run -d  -p 8000:80 -v todo_data:/app/data  riskofstorm/todo_app:latest
```

<b>Short_ulr_app</b>

```bash
docker run -d  -p 8001:80 -v -v shorturl_d:/app/data  riskofstorm/shorturl_app:latest
```