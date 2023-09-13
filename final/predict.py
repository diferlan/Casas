import joblib
import pandas as pd
import json

def predicciones(json_file, modelo_path='/Users/diferlanderos/Desktop/RetoCasas/Casas/pipeline_houses_final_v3.joblib'):
    modelo = joblib.load(modelo_path)
    #print(modelo.feature_names_in_)
    with open(json_file, 'r') as archivo:
        casas_json = json.load(archivo)
    # Convierte el JSON nuevamente en un DataFrame
    df = pd.DataFrame(casas_json['casas'])
    X = df.drop('SalePrice', axis=1)
    #print(X.head())
    # Calcula la media de las columnas específicas y rellena los valores faltantes en X
    medias = df[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']].mean()
    X[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']] = X[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']].fillna(medias)
    X.fillna(0, inplace=True)
    predicciones=modelo.predict(X)
    #print(predicciones[-1])
    df.at[df.index[-1], 'SalePrice'] = predicciones[-1]
    return df.tail(1).to_dict(orient='records')

json_file = '/Users/diferlanderos/Desktop/RetoCasas/Casas/casas.json'
resultado=predicciones(json_file)
print(resultado)