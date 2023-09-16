import joblib
import pandas as pd
import json
from flask import jsonify

def predicciones(json_file, modelo_path='/Users/diferlanderos/Desktop/RetoCasas/Casas/pipeline_houses_final_v4.joblib'):
    modelo = joblib.load(modelo_path)
    #print(modelo.feature_names_in_)
    with open(json_file, 'r') as archivo:
        casas_json = json.load(archivo)
    # Convierte el JSON nuevamente en un DataFrame
    df = pd.DataFrame(casas_json['casas'])
    df = df.applymap(lambda x: x.replace('=', ''))
    df[['id','MSSubClass', 'LotFrontage', 'LotArea', 'OverallQual', 'OverallCond',
       'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2',
       'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF',
       'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces',
       'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
       'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal',
       'MoSold', 'YrSold', 'SalePrice']] = pd.to_numeric(df[['id','MSSubClass', 'LotFrontage', 'LotArea', 'OverallQual', 'OverallCond',
       'YearBuilt', 'YearRemodAdd', 'MasVnrArea', 'BsmtFinSF1', 'BsmtFinSF2',
       'BsmtUnfSF', 'TotalBsmtSF', '1stFlrSF', '2ndFlrSF', 'LowQualFinSF',
       'GrLivArea', 'BsmtFullBath', 'BsmtHalfBath', 'FullBath', 'HalfBath',
       'BedroomAbvGr', 'KitchenAbvGr', 'TotRmsAbvGrd', 'Fireplaces',
       'GarageYrBlt', 'GarageCars', 'GarageArea', 'WoodDeckSF', 'OpenPorchSF',
       'EnclosedPorch', '3SsnPorch', 'ScreenPorch', 'PoolArea', 'MiscVal',
       'MoSold', 'YrSold', 'SalePrice']])
    X = df.drop(['SalePrice','id'], axis=1)
    #print(X.head())
    # Calcula la media de las columnas específicas y rellena los valores faltantes en X
    medias = df[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']].mean()
    X[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']] = X[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']].fillna(medias)
    X.fillna(0, inplace=True)
    predicciones=modelo.predict(X)
    #print(predicciones[-1])
    df.at[df.index[-1], 'SalePrice'] = predicciones[-1]
    return df.tail(1).to_json(orient='records')

json_file = '/Users/diferlanderos/Desktop/RetoCasas/Casas/Codigo ordenado/KREND.json'
resultado=predicciones(json_file)
print(resultado)