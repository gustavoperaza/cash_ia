import pandas as pd
from src.services.transaction_service import obtener_df_transformado

class AnalyticsService:

    @staticmethod

    def resumen_general()-> dict:
        df=obtener_df_transformado() #necesito llamar a la funcion colocando ()
        total_transacciones = len(df)
        total_ingresos =df.loc[df["Aut."].notna(), "Total cobrado"].sum() #solo sumaremos los importes con autorizacion
        transacciones_exitosas= df["Aut."].notna().sum() #solo sumaremos las transacciones que tienen autorizacion
        transacciones_fallidas = df ["Aut."].isna().sum() #solo sumaremos las transacciones sin autorizacion 

        return {

            "total_transacciones": int(total_transacciones),
            "total_ingresos": float(total_ingresos),
            "transacciones_exitosas": int(transacciones_exitosas),
            "transacciones_canceladas": int(transacciones_fallidas)
        }

        
    @staticmethod

    def ingresos_auth_concepto() -> pd.DataFrame:
        df=obtener_df_transformado()
        #la sumatoria de los ingresos autorizados clasificados por concepto de pago (predial, multipagos)
        return (
            df[df["Aut."].notna()].groupby("Concepto")["Total cobrado"].sum().reset_index(name="total_ingresos") # se va agrupar por concepto y se calculara la metrica sobre total importe
    
        )


    @staticmethod 
    # la sumatoria de los ingresos autorizados agrupados por medio de pago
    def ingresos_auth_metod() -> pd.DataFrame:
        df=obtener_df_transformado()
        return (
            df[df["Aut."].notna()].groupby("Medio de Pago")["Total cobrado"].sum().reset_index(name="total_ingresos")
        )
    
    @staticmethod

    def ingresos_auth_dia() -> pd.DataFrame:
        df=obtener_df_transformado()
        return (
            df[df["Aut."].notna()].groupby(df["Fecha"].dt.date)["Total cobrado"]. sum().reset_index(name="total_ingresos")# aqui lo que hago es convertir la columna de echa para que me envie solo la fecha sin la hra
            # luego groupby  agrupa por fecha  y se aplicara la metrica de la sumatoria de total importe dentro de cada grupo
        )