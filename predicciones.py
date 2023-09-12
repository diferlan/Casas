import joblib
import pandas as pd

def predicciones(json,modelo='pipeline_houses_final.joblib'):
    with open(json, 'r') as archivo:
        casas_json = json.load(archivo)
    # Convierte el JSON nuevamente en un DataFrame
    df = pd.DataFrame(casas_json['casas'])  
    df.drop(['Precio de venta'],axis=1,inplace=True)   
    X=df.iloc[-1]
    media = [['Año de construccion', 'Año de remodelacion','Año de construccion de garage','Año de venta']].mean()
    X[['Año de construccion', 'Año de remodelacion','Año de construccion de garage','Año de venta']].fillna(media)
    X.fillna(0,inplace=True)
    return modelo.predict(X)