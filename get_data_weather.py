import urllib.request
import pandas as pd
import gzip
import os
import gc


def appartenance_dep(dep):
    dep_to_region = {
        '01': 'Auvergne-Rhône-Alpes', '03': 'Auvergne-Rhône-Alpes', '07': 'Auvergne-Rhône-Alpes',
        '15': 'Auvergne-Rhône-Alpes', '26': 'Auvergne-Rhône-Alpes', '38': 'Auvergne-Rhône-Alpes',
        '42': 'Auvergne-Rhône-Alpes', '43': 'Auvergne-Rhône-Alpes', '63': 'Auvergne-Rhône-Alpes',
        '69': 'Auvergne-Rhône-Alpes', '73': 'Auvergne-Rhône-Alpes', '74': 'Auvergne-Rhône-Alpes',
        '21': 'Bourgogne-Franche-Comté', '25': 'Bourgogne-Franche-Comté', '39': 'Bourgogne-Franche-Comté',
        '58': 'Bourgogne-Franche-Comté', '70': 'Bourgogne-Franche-Comté', '71': 'Bourgogne-Franche-Comté',
        '89': 'Bourgogne-Franche-Comté', '90': 'Bourgogne-Franche-Comté',
        '35': 'Bretagne', '22': 'Bretagne', '56': 'Bretagne', '29': 'Bretagne',
        '18': 'Centre-Val de Loire', '28': 'Centre-Val de Loire', '36': 'Centre-Val de Loire',
        '37': 'Centre-Val de Loire', '41': 'Centre-Val de Loire', '45': 'Centre-Val de Loire',
        '2A': 'Corse', '2B': 'Corse',
        '08': 'Grand Est', '10': 'Grand Est', '51': 'Grand Est', '52': 'Grand Est',
        '54': 'Grand Est', '55': 'Grand Est', '57': 'Grand Est', '67': 'Grand Est',
        '68': 'Grand Est', '88': 'Grand Est',
        '971': 'Guadeloupe', '973': 'Guyane', '974': 'La Réunion', '972': 'Martinique',
        '02': 'Hauts-de-France', '59': 'Hauts-de-France', '60': 'Hauts-de-France',
        '62': 'Hauts-de-France', '80': 'Hauts-de-France',
        '75': 'Île-de-France', '77': 'Île-de-France', '78': 'Île-de-France',
        '91': 'Île-de-France', '92': 'Île-de-France', '93': 'Île-de-France',
        '94': 'Île-de-France', '95': 'Île-de-France',
        '14': 'Normandie', '27': 'Normandie', '50': 'Normandie',
        '61': 'Normandie', '76': 'Normandie',
        '16': 'Nouvelle-Aquitaine', '17': 'Nouvelle-Aquitaine', '19': 'Nouvelle-Aquitaine',
        '23': 'Nouvelle-Aquitaine', '24': 'Nouvelle-Aquitaine', '33': 'Nouvelle-Aquitaine',
        '40': 'Nouvelle-Aquitaine', '47': 'Nouvelle-Aquitaine', '64': 'Nouvelle-Aquitaine',
        '79': 'Nouvelle-Aquitaine', '86': 'Nouvelle-Aquitaine', '87': 'Nouvelle-Aquitaine',
        '09': 'Occitanie', '11': 'Occitanie', '12': 'Occitanie', '30': 'Occitanie',
        '31': 'Occitanie', '32': 'Occitanie', '34': 'Occitanie', '46': 'Occitanie',
        '48': 'Occitanie', '65': 'Occitanie', '66': 'Occitanie', '81': 'Occitanie',
        '82': 'Occitanie',
        '44': 'Pays de la Loire', '49': 'Pays de la Loire', '53': 'Pays de la Loire',
        '72': 'Pays de la Loire', '85': 'Pays de la Loire',
        '04': 'Provence-Alpes-Côte d\'Azur', '05': 'Provence-Alpes-Côte d\'Azur', '06': 'Provence-Alpes-Côte d\'Azur',
        '13': 'Provence-Alpes-Côte d\'Azur', '83': 'Provence-Alpes-Côte d\'Azur', '84': 'Provence-Alpes-Côte d\'Azur'
    }

    return dep_to_region.get(dep, "Département inconnu")
        
def code_insee(reg):
    regions_insee = {
    "Auvergne-Rhône-Alpes": "84",
    "Bourgogne-Franche-Comté": "27",
    "Bretagne": "53",
    "Centre-Val de Loire": "24",
    "Corse": "94",
    "Grand Est": "44",
    "Hauts-de-France": "32",
    "Île-de-France": "11",
    "Normandie": "28",
    "Nouvelle-Aquitaine": "75",
    "Occitanie": "76",
    "Pays de la Loire": "52",
    "Provence-Alpes-Côte d'Azur": "93"
    }
    
    return regions_insee.get(reg, "Région inconnue")


def main(): 

    departement = [f"{i:02d}" for i in range (1,95+1)]
    periodes = ["2010-2019", "previous-2020-2022", "latest-2023-2024"]
    file_name = "H_01_previous-2020-2022.csv.gz"
    
    columns_needed = ["NUM_POSTE", "NOM_USUEL", "AAAAMMJJHH", "T", "TN", "TX"]
    
    for dep in departement:
        files = []
        for periode in periodes:
            
            link = f"https://object.files.data.gouv.fr/meteofrance/data/synchro_ftp/BASE/HOR/H_{dep}_{periode}.csv.gz"
            file_name = f"H_{dep}_{periode}.csv.gz"
            urllib.request.urlretrieve(link, file_name)
        
        
        
            with gzip.open(file_name, 'rb') as f:
                hor_dep = pd.read_csv(f, sep=";", usecols=columns_needed, parse_dates=["AAAAMMJJHH"], date_format="%Y%m%d%H")
            
            #hor_dep = hor_dep[["NUM_POSTE", "NOM_USUEL", "AAAAMMJJHH", "T", "TN", "TX"]]
            hor_dep.rename({"AAAAMMJJHH":"Date - Heure"}, axis=1, inplace=True)
            #hor_dep["Date - Heure"] = pd.to_datetime(hor_dep["Date - Heure"], format="%Y%m%d%H", errors="coerce")
            hor_dep.set_index("Date - Heure", inplace=True)
            hor_dep.dropna(inplace=True)
            #hor_dep.sort_values(by="Date - Heure", inplace=True)
            hor_dep = hor_dep[["T", "TN", "TX"]].resample("H").mean().round(1)
            hor_dep["Département"] = dep
            region = appartenance_dep(dep)
            hor_dep["Région"] = region
            hor_dep["Code INSEE Région"] = code_insee(region)
            
            files.append(hor_dep)
            
            os.remove(file_name)
            
            gc.collect()
          
        concatenation_periodes = pd.concat(files)
        print(concatenation_periodes)
        concatenation_periodes.to_pickle(f"H_{dep}.pkl")
        del concatenation_periodes 
        print(f"{dep} : ok")
    

    
fichiers_dep = [pd.read_pickle(f"H_{i:02d}.pkl") for i in range(1, 95+1)]
mega_fichier = pd.concat(fichiers_dep)
mega_fichier.to_pickle("temperatures_departements_2010_2024.pkl")


