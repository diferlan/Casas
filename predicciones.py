import joblib
import pandas as pd
import json

def predicciones(json_file, modelo_path='/Users/diferlanderos/Desktop/RetoCasas/Casas/pipeline_houses_final_v2.joblib'):
    modelo = joblib.load(modelo_path)
    print(modelo.feature_names_in_)
    with open(json_file, 'r') as archivo:
        casas_json = json.load(archivo)
    # Convierte el JSON nuevamente en un DataFrame
    df = pd.DataFrame(casas_json['casas'])  
    # df.drop(['Precio de venta'], axis=1, inplace=True)
    # print(df.columns)   
    X = df.iloc[-1].copy()  # Copia la última fila
    X = X.drop('Precio de venta') # Elimina la columna de precio de venta
    X = X.to_frame() # Convierte X en un DataFrame de una columna
    print(X.columns)    # Calcula la media de las columnas específicas y rellena los valores faltantes en X
    medias = df[['YrBlt', 'YearRemodAdd', 'GarageYrBlt', 'Yrsold']].mean()
    X[['YrBlt', 'YearRemodAdd', 'GarageYrBlt', 'Yrsold']].fillna(medias)
    X.fillna(0, inplace=True)
    print(X)
    # Realiza la transformación de las características utilizando el preprocesador
    X_transformed = modelo.named_steps['preprocessor'].transform(X)
    # Realiza la predicción
    prediccion = modelo.predict(X_transformed)
    # Agrega el resultado de la predicción a X
    X['Precio de venta'] = prediccion
    # Convierte X a un diccionario y genera el JSON de salida
    resultado_json = X[['Tamaño del lote', 'Colonia', 'Precio de venta']].to_dict(orient='records')
    # Guarda el JSON de resultado en un archivo
    with open('prediccion.json', 'w') as archivo_salida:
        json.dump(resultado_json, archivo_salida, indent=4)
    return resultado_json

json_file = '/Users/diferlanderos/Desktop/RetoCasas/Casas/casas.json'
resultado = predicciones(json_file)
print(resultado)
