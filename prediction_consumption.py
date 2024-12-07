import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error
import pickle
import itertools

# Charger les données
# df : dataframe avec un index temporel (horaire) et une colonne 'consumption'
# Exemple : df = pd.read_csv('consumption_hourly.csv', parse_dates=['timestamp'], index_col='timestamp')
# Assurez-vous que l'index est horaire !

df = pd.read_pickle("data_generation_prices_FR.pkl")
df = df[df["Consommation (MW)"].notna()]
df["Consommation (MW)"] = df["Consommation (MW)"].astype('int32')
df = df.groupby(df.index).mean()
df = df.asfreq("H")
df = df["2021-01-01":]
print(df)

# Étape 1 : Détecter la saisonnalité (ici m = 24 pour des cycles journaliers)
m = 24  # Testez aussi avec 168 pour des cycles hebdomadaires




model = SARIMAX(
    df['Consommation (MW)'],
    order=(1,1,1),
    seasonal_order=(1,1,1,m),
    enforce_stationarity=False,
    enforce_invertibility=False
)
results = model.fit(disp=True)

with open('sarimax_model.pkl', 'wb') as f:
    pickle.dump(results, f)

