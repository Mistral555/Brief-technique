import pandas as pd
import sqlite3
import requests
import io
import os

####################################################
#         Importations et traitement des fichiers 
####################################################
urls = {
    "produits": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=0&single=true&output=csv",
    "magasins": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=714623615&single=true&output=csv",
    "ventes": "https://docs.google.com/spreadsheets/d/e/2PACX-1vSawI56WBC64foMT9pKCiY594fBZk9Lyj8_bxfgmq-8ck_jw1Z49qDeMatCWqBxehEVoM6U1zdYx73V/pub?gid=760830694&single=true&output=csv"
}


def import_csv(url):
    response = requests.get(url)

    return pd.read_csv(io.StringIO(response.text))

produits_df = import_csv(urls["produits"])
produits_df.rename(columns={"ID RÃ©fÃ©rence produit": "Id_produit"}, inplace=True)
# print(produits_df.head())


magasins_df = import_csv(urls["magasins"])
magasins_df.rename(columns={
    "ID Magasin": "Id_magasin",
    "Nombre de salariÃ©s": "Nbr_salaries"
}, inplace=True)
# print(magasins_df.head())

ventes_df = import_csv(urls["ventes"])
ventes_df.rename(columns={
    "ID RÃ©fÃ©rence produit": "Id_produit",
    "QuantitÃ©": "Quantite",
    "ID Magasin": "Id_magasin"
}, inplace=True)



####################################################
#            Ajout clé primaire pour ventes
#    J'ai choisi de créer une clé qui concatène tout les champs pour éviter l'insertion d'un doublon et que le code sera réutilisable
#    Dans un autre cas on peut faire une clé simple INTEGER mais faudra récupérer dernier élément présent sur la bdd
# 
#    Question :  à discuter lors de l'entretien si possible !
####################################################

ventes_df["Id_vente"] = (
    ventes_df["Date"].astype(str) + "_" +
    ventes_df["Id_produit"].astype(str) + "_" +
    ventes_df["Quantite"].astype(str) + "_" +
    ventes_df["Id_magasin"].astype(str)
)





####################################################
#            Mise en place Base de données 
####################################################

conn = sqlite3.connect("/data/projet.db")
cursor = conn.cursor()


cursor.executescript("""
CREATE TABLE IF NOT EXISTS produits (
    Id_produit TEXT PRIMARY KEY,
    Nom TEXT,
    Prix REAL,
    Stock INTEGER
);
CREATE TABLE IF NOT EXISTS magasins (
    Id_magasin INTEGER PRIMARY KEY,
    Ville TEXT,
    Nbr_salaries INTEGER
);
CREATE TABLE IF NOT EXISTS ventes (
    Id_vente TEXT PRIMARY KEY,
    Id_produit TEXT,
    Id_magasin INTEGER,
    Date DATE,
    Quantite INTEGER,
    FOREIGN KEY(Id_produit) REFERENCES produits(Id_produit),
    FOREIGN KEY(Id_magasin) REFERENCES magasins(Id_magasin)
);

CREATE TABLE IF NOT EXISTS resultats (
    Id_resultat INTEGER PRIMARY KEY,
    Nom TEXT,
    Valeur

""")


####################################################
#                     Insertion 
####################################################

produits_df.to_sql("produits", conn, if_exists="replace", index=False)
magasins_df.to_sql("magasins", conn, if_exists="replace", index=False)


for _, row in ventes_df.iterrows():
    if pd.notna(row["Id_vente"]): 
        cursor.execute("SELECT COUNT(*) FROM ventes WHERE Id_vente = ?", (row["Id_vente"],))
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO ventes (Id_vente, Id_produit, Id_magasin, Date, Quantite)
                VALUES (?, ?, ?, ?, ?)
            """, (row["Id_vente"], row["Id_produit"], row["Id_magasin"], row["Date"], row["Quantite"]))


conn.commit()
conn.close()









