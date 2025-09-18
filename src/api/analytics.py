
from fastapi import APIRouter
from pandas import DataFrame
from src.services.analytics_service import AnalyticsService
from src.services.transaction_service import obtener_df_transformado # es una función

#MINI TABLERO DE RUTAS 
router = APIRouter(prefix="/analytics", tags=["Analytics"]) #prefix es para decirle a todas las rutas que le antepondremos analytics , tags es solo para swagger 



@router.get("/resumen")
def resumen_general():
    #df= obtener_df_transformado()
    return AnalyticsService.resumen_general()  # ya es dict, no necesita .to_dict

@router.get("/ingresos/concepto")
def ingresos_concepto():
    #df= obtener_df_transformado()
    return AnalyticsService.ingresos_auth_concepto().reset_index().to_dict(orient="records")

@router.get("/ingresos/metodo_pago")
def ingresos_metodo():
    #df= obtener_df_transformado()
    return AnalyticsService.ingresos_auth_metod().reset_index().to_dict(orient="records")

@router.get("/ingresos/dia")
def ingresos_dia():
    #df= obtener_df_transformado()
    return AnalyticsService.ingresos_auth_dia().reset_index().to_dict(orient="records")
