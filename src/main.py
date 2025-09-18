# main.py
from fastapi import FastAPI
from src.api.analytics import router as analytics_router   # ajusta el import según dónde guardaste analytics.py

app = FastAPI(
    title="API Financiera PyME",
    description="API para exponer métricas y análisis de transacciones",
    version="1.0.0"
)

# Aquí registras el router de analytics
app.include_router(analytics_router)

# Puedes agregar más routers si tienes más módulos
# from routers import transacciones, usuarios
# app.include_router(transacciones.router)
# app.include_router(usuarios.router)

# Si quieres definir un endpoint raíz de prueba
@app.get("/")
def root():
    return {"message": "API Financiera PyME funcionando correctamente"}
