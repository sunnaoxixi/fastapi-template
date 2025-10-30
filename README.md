# FastAPI Template con DDD y Alembic

Template de FastAPI siguiendo principios de Domain-Driven Design (DDD) con migraciones de base de datos usando Alembic.

## 🏗️ Arquitectura

Este proyecto sigue una arquitectura DDD con Bounded Contexts:

```
src/
├── contexts/
│   ├── auth/                    # Bounded Context: Autenticación
│   │   ├── domain/             # Lógica de negocio
│   │   ├── application/        # Casos de uso
│   │   └── infrastructure/     # Implementación (DB, API)
│   └── shared/                 # Infraestructura compartida
│       ├── domain/             # Abstracciones de dominio compartidas
│       └── infrastructure/     # Implementaciones compartidas
│           ├── persistence/    # Base de datos
│           ├── cache/          # Cache
│           └── logger/         # Logging
├── main.py                     # Punto de entrada
└── settings.py                 # Configuración
```

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.13+
- PostgreSQL 14+
- Docker y Docker Compose (opcional)
- uv (gestor de paquetes Python)

### Instalación Local

1. **Clonar el repositorio**

   ```bash
   git clone <repository-url>
   cd fastapi-template
   ```

1. **Instalar dependencias**

   ```bash
   uv sync
   ```

1. **Configurar variables de entorno**

   ```bash
   cp secrets/.env.example secrets/.env
   # Editar secrets/.env con tus configuraciones
   ```

1. **Inicializar la base de datos**

   ```bash
   # Asegúrate de que PostgreSQL está corriendo
   uv run alembic upgrade head
   ```

1. **Ejecutar la aplicación**

   ```bash
   uv run fastapi dev src/main.py
   ```

### Con Docker

1. **Iniciar los servicios**

   ```bash
   make start
   # o
   docker compose up
   ```

1. **Ejecutar migraciones**

   ```bash
   make migration-upgrade
   ```

## 🗄️ Migraciones de Base de Datos

Este proyecto usa [Alembic](https://alembic.sqlalchemy.org/) para gestionar migraciones de base de datos.

### Comandos Comunes

#### Crear una nueva migración

```bash
# Con Docker
make migration-create
# Ingresa el mensaje cuando se te pida

# Local
uv run alembic revision --autogenerate -m "descripción del cambio"
```

#### Aplicar migraciones

```bash
# Con Docker
make migration-upgrade

# Local
uv run alembic upgrade head
```

#### Revertir migración

```bash
# Con Docker
make migration-downgrade

# Local
uv run alembic downgrade -1
```

#### Ver historial de migraciones

```bash
# Con Docker
make migration-history

# Local
uv run alembic history
```

Para más información sobre migraciones, consulta [migrations/README.md](migrations/README.md)

## 📁 Estructura del Proyecto

### Contextos (Bounded Contexts)

Cada contexto sigue la estructura de DDD:

- **domain/**: Lógica de negocio pura

  - `aggregates.py`: Entidades agregadas
  - `errors.py`: Excepciones del dominio
  - `repositories.py`: Interfaces de repositorios

- **application/**: Casos de uso de la aplicación

  - `use_cases/`: Lógica de aplicación

- **infrastructure/**: Implementaciones concretas

  - `persistence/`: Modelos SQLAlchemy y repositorios
  - `container.py`: Inyección de dependencias

### Infraestructura Compartida

El contexto `shared` contiene código compartido entre todos los contextos:

- **Database**: Configuración de SQLAlchemy con soporte async
- **Cache**: Cliente de cache (in-memory, Redis)
- **Logger**: Configuración de logging con Loguru
- **Base Models**: Base declarativa para todos los modelos

## 🔧 Desarrollo

### Agregar un Nuevo Bounded Context

1. **Crear la estructura de directorios**

   ```bash
   mkdir -p src/contexts/nuevo_contexto/{domain,application/use_cases,infrastructure/persistence}
   ```

1. **Crear los modelos de dominio**

   ```python
   # src/contexts/nuevo_contexto/domain/aggregates.py
   from dataclasses import dataclass


   @dataclass
   class MiEntidad:
       id: str
       nombre: str
   ```

1. **Crear los modelos de persistencia**

   ```python
   # src/contexts/nuevo_contexto/infrastructure/persistence/models.py
   from sqlalchemy import Column, String
   from src.contexts.shared.infrastructure.persistence.base import Base


   class MiEntidadModel(Base):
       __tablename__ = "mi_tabla"

       id = Column(String(36), primary_key=True)
       nombre = Column(String(100), nullable=False)
   ```

1. **Registrar los modelos en Alembic**

   ```python
   # migrations/env.py
   from src.contexts.nuevo_contexto.infrastructure.persistence import (
       models as nuevo_models,
   )  # noqa: F401
   ```

1. **Generar la migración**

   ```bash
   uv run alembic revision --autogenerate -m "add nuevo_contexto models"
   ```

### Mejores Prácticas

#### 1. Separación de Responsabilidades

- **Domain**: Lógica de negocio pura, sin dependencias externas
- **Application**: Orquestación de casos de uso
- **Infrastructure**: Detalles de implementación (DB, API, etc.)

#### 2. Dependency Injection

Usa `dependency-injector` para inyección de dependencias:

```python
from dependency_injector import containers, providers


class MiContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    repository = providers.Singleton(
        MiRepositorio,
        session_factory=config.session_factory,
    )
```

#### 3. Migraciones

- Siempre revisa las migraciones autogeneradas
- Usa migraciones de datos cuando sea necesario
- Mantén las migraciones reversibles
- Usa las utilidades en `migrations/utils.py`

#### 4. Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=src
```

## 🛠️ Makefile

El proyecto incluye un Makefile con comandos útiles:

```bash
# Docker
make start              # Iniciar servicios
make stop               # Detener servicios
make restart            # Reiniciar servicios
make logs               # Ver logs

# Migraciones (Docker)
make migration-create           # Crear migración
make migration-upgrade          # Aplicar migraciones
make migration-downgrade        # Revertir migración
make migration-history          # Ver historial

# Migraciones (Local)
make local-migration-create     # Crear migración localmente
make local-migration-upgrade    # Aplicar migraciones localmente
make local-migration-downgrade  # Revertir migración localmente

# Utilidades
make shell              # Shell en el contenedor
make db-shell          # Shell de PostgreSQL
make install           # Instalar dependencias localmente
```

## 📝 Variables de Entorno

Copia `secrets/.env.example` a `secrets/.env` y configura:

```bash
# Application
ENVIRONMENT=development
LOG_LEVEL=INFO

# Security
SECRET_KEY=tu-clave-secreta-super-segura

# Database
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
```

## 🔐 Seguridad

- **Nunca** commits el archivo `secrets/.env` al repositorio
- Cambia el `SECRET_KEY` en producción
- Usa variables de entorno para credenciales
- Mantén las dependencias actualizadas

## 📚 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Domain-Driven Design](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [Dependency Injector](https://python-dependency-injector.ets-labs.org/)

## 📄 Licencia

[MIT License](LICENSE)

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
1. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
1. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
1. Push a la rama (`git push origin feature/AmazingFeature`)
1. Abre un Pull Request
