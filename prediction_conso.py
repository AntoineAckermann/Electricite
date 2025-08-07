import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.preprocessing import StandardScaler


data_temp = pd.read_csv("temperature-quotidienne-regionale.csv", sep=';')

data_temp["ID"] = data_temp["ID"].apply(lambda x: '-'.join(x.split("-")[:-1]))
data_temp["ID"] = pd.to_datetime(data_temp["ID"], format="%Y-%m-%dT%H:%M:%S")
# data_temp = data_temp.loc[data_temp["ID"].dt.year == 2023]
data_temp = data_temp.select_dtypes(include="number").drop(
    ["Code INSEE région"], axis=1).groupby(data_temp["ID"].dt.date).mean()
data_temp.index = pd.to_datetime(data_temp.index)

data_ferie = pd.read_csv("jours_feries_metropole.csv",
                         sep=",", encoding="latin-1")
data_ferie["date"] = pd.to_datetime(data_ferie["date"], format="%Y-%m-%d")
data_ferie.set_index("date", inplace=True)
data_ferie["est_ferie"] = data_ferie["nom_jour_ferie"].notna().astype(int)
data_ferie.drop(["zone", "nom_jour_ferie", "annee"], axis=1, inplace=True)

data_vacances = pd.read_csv("vacances.csv", sep=",")
data_vacances["date"] = pd.to_datetime(
    data_vacances["date"], format="%Y-%m-%d")
data_vacances.set_index("date", inplace=True)
data_vacances.drop(["nom_vacances"], inplace=True, axis=1)
data_vacances = data_vacances.astype(int)
# data_vacances = data_vacances.applymap(lambda x: 1 if str(x) == "True" else 0)

data_vacances.to_csv("test.csv", sep=";", encoding="latin-1")


data_prod_prix = pd.read_pickle("data_prod_consolidees_FR.pkl")

df = data_prod_prix.resample("D").mean().merge(
    data_temp, how="inner", left_index=True, right_index=True)
df.dropna(inplace=True)

df = df.merge(data_ferie, how="left", left_index=True, right_index=True)
df["est_ferie"] = df["est_ferie"].fillna(0)

df = df.merge(data_vacances, how="left", left_index=True, right_index=True)

print(df)
memory = 5
for i in range(memory):
    df[f"J-{i}"] = df["Consommation"].shift(i)

df = df.iloc[5:,:]


df['Mois'] = df.index.month
df['Jour de la semaine'] = df.index.weekday

print(df)

# df.to_csv("test.csv", sep=";", encoding="latin-1")

var_explicatives = ["TMax (°C)", "TMoy (°C)", "TMin (°C)", "Mois", "Jour de la semaine",
                    "est_ferie", "vacances_zone_a", "vacances_zone_b", "vacances_zone_c"] + [f"J-{i}" for i in range(memory)]
var_cible = "Consommation"


X = df[var_explicatives]
y = df[var_cible]

# Standardisation des variables explicatives
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Division en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.3, random_state=42)

# Création et entraînement du modèle Lasso
# On fixe alpha pour contrôler la régularisation (à ajuster selon les résultats)
model = RandomForestRegressor()
model.fit(X_train, y_train)


# Prédictions
y_pred = model.predict(X_test)

# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nÉvaluation du modèle avec RFRgressor :")
print(f"Erreur quadratique moyenne (MSE) : {mse:.2f}")
print(f"Erreur absolue moyenne en pourcentage (MAPE) : {mape * 100:.2f} %")
print(f"Coefficient de détermination (R²) : {r2:.2f}")


plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(),
         y_test.max()], color='red', linestyle='--')
plt.xlabel("Valeurs réelles")
plt.ylabel("Valeurs prédites")
plt.title("Valeurs réelles vs prédictions")
plt.show()
