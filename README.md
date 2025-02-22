[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com/)
[![SQLAdmin](https://img.shields.io/badge/-SQLAdmin-464646?style=flat-square&logo=SQLAdmin)](https://aminalaee.dev/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat-square&logo=Alembic)](https://alembic.sqlalchemy.org/en/latest/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat-square&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![Docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Redis](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)](https://redis.io/)
[![Poetry](https://img.shields.io/badge/-Poetry-464646?style=flat-square&logo=Poetry)](https://python-poetry.org/)

![Deploy](https://github.com/BookProjectPGUTI/back/actions/workflows/deploy.yml/badge.svg)

# Book Project

## Запуск проекта  
  
1. Копируем файл с настройками  
  
   ```
   cp .env.example .env
   ```  
  
   > При необходимости настройки правим в файле .env

2. Копируем [.migration.env.example](mobile/.migration.env.example)

    ```
    cd mobile
    ```
    ```
    cp .migration.env.example .migration.env
    ```
  
3. Запускаем контейнеры  
  
    ```
    docker compose up -d --build
    ```
   > Чтобы работал reload нужно запустить с командой --watch
   ```
   docker compose up --build --watch
   ```
   
## Миграции

### Создание новых миграций 

Для создания миграций должен быть запущен проект.



1. Запускаем создание миграции

    ```
    cd mobile
    ```
   
    ```
    alembic revision --a -m "описание изменений в моделях"
    ```



