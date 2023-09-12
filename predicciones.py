import joblib

def predicciones(modelo='pipeline_houses_final.joblib',X):
    media = X_[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']].mean()
    X[['YearBuilt', 'YearRemodAdd','GarageYrBlt','YrSold']].fillna(media)
    X.fillna(0,inplace=True)
    return modelo.predict(X)