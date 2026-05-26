# Nexus Enterprise - Dashboard Pro 🚀

Este es un sistema de gestión y administración comercial estructurado con una arquitectura full-stack moderna, ligera y eficiente. Permite el registro dinámico de clientes, cálculo automatizado de facturación según planes y persistencia de datos local.

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3 con **FastAPI** (Estructuración de API REST asíncrona).
* **Base de Datos:** **SQLite** administrado mediante **SQLAlchemy** (ORM).
* **Frontend:** HTML5, **Tailwind CSS** (Estilos responsivos integrados) y **Chart.js** (Renderizado dinámico de métricas financieras).
* **Servidor ASGI:** Uvicorn.

## 📦 Características del Sistema

* **Persistencia Real:** Los datos no se borran al recargar; se almacenan de forma segura en una base de datos SQLite (`nexus.db`).
* **Lógica en Backend:** Generación automatizada de avatares basados en iniciales y asignación de costos financieros según el plan contratado desde el core en Python.
* **Interfaz Autodocumentada:** Documentación interactiva completa integrada mediante Swagger UI.

## 🚀 Instrucciones de Instalación y Uso

### 1. Clonar el repositorio
```bash
git clone [https://github.com/hannerzamora1405-spec/nexus-dashboard.git](https://github.com/hannerzamora1405-spec/nexus-dashboard.git)
cd nexus-dashboard