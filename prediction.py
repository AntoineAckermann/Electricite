import pandas as pd
import marginal_price
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error, r2_score
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data_prod_prix_FR.csv", sep=";", encoding="latin-1")


var_explicatives = ["Consommation", "Fioul", "Gaz", "Charbon", "Nucléaire", "Eolien", "Solaire", "Hydraulique", "Bioénergies", "Ech. physiques"]
var_cible = "Day-ahead Price"



X = df[var_explicatives]
y = df[var_cible]

# Standardisation des variables explicatives
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Division en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# Création et entraînement du modèle Lasso
# On fixe alpha pour contrôler la régularisation (à ajuster selon les résultats)
model = RandomForestRegressor(n_estimators=100)
model.fit(X_train, y_train)



# Prédictions
y_pred = model.predict(X_test)

# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
mape = mean_absolute_percentage_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"\nÉvaluation du modèle avec Lasso :")
print(f"Erreur quadratique moyenne (MSE) : {mse:.2f}")
print(f"Erreur absolue moyenne en pourcentage (MAPE) : {mape * 100:.2f} %")
print(f"Coefficient de détermination (R²) : {r2:.2f}")

import matplotlib.pyplot as plt
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='red', linestyle='--')
plt.xlabel("Valeurs réelles")
plt.ylabel("Valeurs prédites")
plt.title("Valeurs réelles vs prédictions")
plt.show()