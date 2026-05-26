import random
from typing import List
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. CONFIGURACIÓN DE LA BASE DE DATOS SQLITE
DATABASE_URL = "sqlite:///./nexus.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. MODELO DE LA TABLA EN LA BASE DE DATOS (SQLAlchemy)
class ClienteDB(Base):
    __tablename__ = "clientes"

    id_db = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_avatar = Column(String, index=True)
    nombre = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    pais = Column(String)
    rol = Column(String)
    factura = Column(Float)
    estado_factura = Column(String)

# Crear el archivo nexus.db y sus tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

# 3. ESQUEMAS DE VALIDACIÓN (Pydantic)
class ClienteCreate(BaseModel):
    nombre: str
    email: EmailStr
    pais: str
    rol: str

class ClienteResponse(BaseModel):
    id_db: int
    id_avatar: str
    nombre: str
    email: str
    pais: str
    rol: str
    factura: float
    estado_factura: str

    class Config:
        from_attributes = True

# 4. INICIALIZACIÓN DE FASTAPI Y CONTROL DE CORS
app = FastAPI(title="Nexus Enterprise API", version="1.0")

# Permite que tu archivo dashboard.html (que corre localmente) se comunique con la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependencia para manejar los ciclos de conexión a la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 5. ENDPOINTS DE LA API

@app.get("/api/clientes", response_model=List[ClienteResponse])
def obtener_clientes(db: Session = Depends(get_db)):
    """Trae todos los clientes guardados en la base de datos."""
    return db.query(ClienteDB).all()

@app.post("/api/clientes", response_model=ClienteResponse, status_code=201)
def guardar_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Registra un nuevo cliente, genera su avatar e inicializa su factura."""
    
    # Evitar correos duplicados en la base de datos
    db_existente = db.query(ClienteDB).filter(ClienteDB.email == cliente.email).first()
    if db_existente:
        raise HTTPException(status_code=400, detail="El correo electrónico ya está registrado.")

    # Generar ID de Avatar automáticamente con las iniciales (Ej: Andrés Mendoza -> AM)
    partes = cliente.nombre.strip().split()
    iniciales = "".join([p[0].upper() for p in partes if p])[:2]
    id_avatar = iniciales if iniciales else "??"

    # Asignar costo de factura simulado según el plan seleccionado en el HTML
    valores_plan = {"Estándar": 49.00, "Premium": 149.00, "Admin": 0.00}
    monto_factura = valores_plan.get(cliente.rol, 25.00)
    
    # Asignar un estado aleatorio para dar dinamismo visual al dashboard
    estado_factura = random.choice(["Completado", "Pendiente", "Cancelado"]) if monto_factura > 0 else "Completado"

    nuevo_cliente = ClienteDB(
        id_avatar=id_avatar,
        nombre=cliente.nombre,
        email=cliente.email,
        pais=cliente.pais.upper(),
        rol=cliente.rol,
        factura=monto_factura,
        estado_factura=estado_factura
    )

    db.add(nuevo_cliente)
    db.commit()
    db.refresh(nuevo_cliente)
    return nuevo_cliente

# 6. EJECUCIÓN DEL SERVIDOR
# 6. EJECUCIÓN DEL SERVIDOR
if __name__ == "__main__":
    import uvicorn
    # Cambiado a "main:app", host "0.0.0.0" y port 8080 para acoplarse a tu entorno de red
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)