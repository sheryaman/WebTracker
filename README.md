# WebTracker

Sistema de monitoreo de sitios web en tiempo real para verificar disponibilidad, tiempo de respuesta y certificados SSL.

## Descripcion

WebTracker es una aplicacion completa de monitoreo web que permite rastrear multiples sitios web automaticamente. El sistema verifica periodicamente cada sitio registrado y registra su estado, tiempo de respuesta y seguridad SSL.

## Caracteristicas

- Monitoreo automatico de sitios web cada 60 segundos
- Verificacion de tiempo de respuesta en milisegundos
- Deteccion de certificados SSL/HTTPS
- Dashboard en tiempo real con React y TypeScript
- API REST con FastAPI
- Sistema de colas con Celery y Redis
- Base de datos PostgreSQL
- Monitoreo de metricas con Prometheus
- Visualizacion de datos con Grafana
- Tests automatizados con pytest
- Manejo robusto de errores
- Arquitectura basada en contenedores Docker

## Arquitectura

El sistema utiliza una arquitectura de microservicios con los siguientes componentes:

- **API FastAPI**: Servidor principal que gestiona las peticiones HTTP
- **PostgreSQL**: Base de datos para almacenar sitios y registros de monitoreo
- **Redis**: Broker de mensajes para el sistema de colas
- **Celery Worker**: Procesa las tareas de monitoreo en segundo plano
- **Celery Beat**: Orquestador que programa las tareas periodicas
- **Prometheus**: Recopila metricas del sistema
- **Grafana**: Dashboard para visualizar las metricas
- **React Frontend**: Interfaz de usuario para gestionar sitios

## Requisitos Previos

- Docker y Docker Compose
- Node.js y npm (para desarrollo del frontend)
- Python 3.10+ (para desarrollo local del backend)

## Instalacion

1. Clonar el repositorio:
```bash
git clone <repository-url>
cd WebTracker
```

2. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

3. Iniciar los servicios con Docker:
```bash
docker compose up -d
```

4. Iniciar el frontend (desarrollo):
```bash
cd frontend-dashboard
npm install
npm run dev
```

## Uso

### Acceder a la aplicacion

- Frontend: http://localhost:5173
- API: http://localhost:8000
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090

### Agregar un sitio

1. Navegar al frontend en http://localhost:5173
2. Completar el formulario con nombre y URL del sitio
3. Hacer clic en "Añadir Sitio al Monitor"
4. El sistema comenzara a monitorear el sitio automaticamente

### Ver estado de monitoreo

Cada tarjeta de sitio muestra:
- Estado actual (Operational/Down/Pendiente)
- Tiempo de respuesta en milisegundos
- Estado del certificado SSL
- Boton para eliminar el sitio

## Endpoints de la API

### Sitios

- `POST /api/v1/sites/` - Crear nuevo sitio
- `GET /api/v1/sites/` - Listar todos los sitios
- `DELETE /api/v1/sites/{id}` - Eliminar un sitio

### Metricas

- `GET /metrics` - Metricas en formato Prometheus
- `GET /` - Estado de la API

## Tests

Ejecutar tests del backend:
```bash
docker compose exec api pytest app/tests/ -v
```

## Estructura del Proyecto

```
WebTracker/
├── backend/                 # API FastAPI
│   ├── app/
│   │   ├── api/           # Endpoints
│   │   ├── core/          # Configuracion y base de datos
│   │   ├── crud/          # Operaciones de base de datos
│   │   ├── models/        # Modelos SQLAlchemy
│   │   ├── schemas/       # Schemas Pydantic
│   │   ├── tasks.py       # Tareas Celery
│   │   └── tests/         # Tests pytest
│   ├── requirements.txt
│   └── Dockerfile
├── frontend-dashboard/     # React + TypeScript
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   └── App.tsx        # Componente principal
│   ├── package.json
│   └── vite.config.ts
├── prometheus/             # Configuracion de Prometheus
│   └── prometheus.yml
├── docker-compose.yml
├── .env.example
└── README.md
```

## Tecnologias Utilizadas

### Backend
- FastAPI - Framework web
- SQLAlchemy - ORM
- PostgreSQL - Base de datos
- Celery - Sistema de colas
- Redis - Broker de mensajes
- Pytest - Testing

### Frontend
- React - Framework UI
- TypeScript - Tipado estatico
- Vite - Build tool
- Tailwind CSS - Estilos
- Lucide React - Iconos

### DevOps
- Docker - Contenedores
- Docker Compose - Orquestacion
- Prometheus - Monitoreo
- Grafana - Visualizacion

## Funcionamiento del Monitoreo

1. El usuario agrega un sitio web a traves del frontend
2. La API crea el registro en PostgreSQL
3. Celery Beam programa una tarea inmediata de monitoreo
4. Cada 60 segundos, Celery Beam descubre sitios activos
5. Los Workers de Celery ejecutan peticiones HTTP a cada sitio
6. Los resultados (status code, tiempo de respuesta, SSL) se guardan en la base de datos
7. El frontend actualiza la informacion cada 10 segundos
8. Prometheus recopila metricas para analisis
9. Grafana visualiza las metricas en dashboards

## Manejo de Errores

El sistema incluye manejo robusto de errores:

- Validacion de URLs y nombres en el backend
- Mensajes de error especificos para el usuario
- Indicadores de carga en la interfaz
- Diferenciacion entre tipos de errores (400, 404, 500)
- Cascading delete para mantener integridad de datos

## Desarrollo

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend-dashboard
npm install
npm run dev
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## Licencia

Este proyecto es de codigo abierto y esta disponible bajo la licencia MIT.

