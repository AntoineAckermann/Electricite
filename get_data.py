import pandas as pd


def download_RTE_data():
    """ Télécharge les données éCO2mix depuis la plateforme ODRE. Les données sont en deux parties : fichier "temps réel" et fichier "données définitives"""
    
    url_RTE_tr = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"
    url_RTE_cons = "https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-cons-def/exports/csv?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B"

    RTE_tr = pd.read_csv(url_RTE_tr, sep=";") # données temps réel
    RTE_cons = pd.read_csv(url_RTE_cons, sep=";") # données consolidées
    
    return RTE_tr, RTE_cons

def get_clean_RTE_data(download=True, pkl=True, csv=True):
    """
    Retourne un Dataframe pandas des données RTE éCO2mix depuis 2012.
    
    Args:
        download (bool): indique si les données sont déjà présentes en local ou sont à télécharger.
        pkl (bool): indique si le dataframe doit être exporté en format .pkl
        csv (bool): indique si le dataframe doit être exporté en format .csv
        
    Returns:
        pd.DataFrame: le dataframe contenant les données
        """
        
    if download:
        print("Téléchargement en cours...")
        df_tr, df_cons = download_RTE_data()
    
    else:
        df_cons = pd.read_csv("eco2mix-national-cons-def.csv", sep=";")
        df_tr = pd.read_csv("eco2mix-national-tr.csv", sep=";")
        
    df_cons.rename(columns={"Date et Heure":"Date - Heure"}, inplace=True)
    
    df_RTE = pd.concat([df_tr, df_cons], join="inner")

    
    to_drop = ["Périmètre", "Nature", "Date", "Heure"]
    df_RTE.drop(to_drop, axis=1, inplace=True)
    
    df_RTE["Date - Heure"] = pd.to_datetime(df_RTE["Date - Heure"], format="%Y-%m-%dT%H:%M:%S%z", errors="coerce")
    df_RTE["Date - Heure"] = df_RTE["Date - Heure"].apply(lambda x: x.replace(tzinfo=None))
    df_RTE.set_index("Date - Heure", inplace=True)
    df_RTE = df_RTE.sort_values(by=["Date - Heure"])
    df_RTE = df_RTE.apply(pd.to_numeric, errors="coerce")

    df_RTE = df_RTE[df_RTE["Consommation (MW)"].notna()] #suppression des valeurs pour les 1/4 heures 
    df_RTE = df_RTE.resample("H").mean()
    
    if pkl:
        df_RTE.to_pickle("df_RTE_national.pkl")
    if csv:
        df_RTE.to_csv("df_RTE_national.csv", sep=";", encoding="latin-1")

    return df_RTE


def get_ENTSOE_prices(country="FR", pkl=True, csv=True):
    """
    Retourne un Dataframe pandas des prix day-ahead de ENTSOE. Nécessite que les fichiers annuels correspondants soient téléchargés en local.

    Args:
        country (str): choix du pays pour les données
        pkl (bool): indique si le dataframe doit être exporté en format .pkl
        csv (bool): indique si le dataframe doit être exporté en format .csv
        
    Returns:
        pd.DataFrame: le dataframe contenant les données
    """
    
    files = []
    for j in range(2015, 2025):
        f = pd.read_csv(f"prices_{country}/Day-ahead Prices_{j}01010000-{j+1}01010000.csv")
        f["MTU (CET/CEST)"] = f["MTU (CET/CEST)"].apply(lambda x: x.split(" -", 1)[0])
        f["MTU (CET/CEST)"] = pd.to_datetime(f["MTU (CET/CEST)"], format="%d.%m.%Y %H:%M")
        f.rename({f.columns[1]: "Day-ahead Price"}, axis=1, inplace=True)
     
        f.set_index("MTU (CET/CEST)", inplace = True)
        f = f[["Day-ahead Price", "Currency"]]
        
        files.append(f)
        
    data_ENTSOE_prices = pd.concat(files)
    data_ENTSOE_prices["Day-ahead Price"] = data_ENTSOE_prices["Day-ahead Price"].apply(pd.to_numeric, errors="coerce")
  
    
    
    if pkl:
        data_ENTSOE_prices.to_pickle("input_data/processed/data_prices_FR_2015_2024.pkl")
    if csv:
        data_ENTSOE_prices.to_csv("df_RTE_national.csv", sep=";", encoding="latin-1")

    return data_ENTSOE_prices

def merge_RTE_ENTSOE(df_RTE, df_ENTSOE, pkl=True, csv=True):
    
    data_generation_prices = df_RTE.merge(df_ENTSOE["Day-ahead Price"], how="left", left_index=True, right_index=True)
    
    if pkl:
        data_generation_prices.to_pickle("data_generation_prices_FR.pkl")
    if csv:
        data_generation_prices.to_csv("data_generation_prices_FR.csv", sep=";", encoding="latin-1")

    return data_generation_prices


rte = get_clean_RTE_data(download=True, pkl=False, csv=False)
entsoe = get_ENTSOE_prices(country="FR", pkl=False, csv=False)

data_generation_prices = merge_RTE_ENTSOE(rte, entsoe, pkl=True, csv=True)
