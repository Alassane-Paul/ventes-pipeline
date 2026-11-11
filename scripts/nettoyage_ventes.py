import pandas as pd

df = pd.read_csv("data/ventes_brutes.csv")

print("Aperçu des données :")
print(df.head())

print("\nInformations générales :")
print(df.info())

print("\nValeurs manquantes :")
print(df.isnull().sum())

df = df.drop_duplicates()

df["ville"] = df["ville"].fillna("Inconnue")

df["date_commande"] = pd.to_datetime(df["date_commande"])
df["quantite"] = pd.to_numeric(df["quantite"], errors="coerce")
df["prix_unitaire"] = pd.to_numeric(df["prix_unitaire"], errors="coerce")

df = df.dropna(subset=["quantite", "prix_unitaire"])

df["montant_total"] = df["quantite"] * df["prix_unitaire"]

df.to_csv("data/ventes_propres.csv", index=False)

print("\nNettoyage terminé. Les données propres ont été enregistrées dans 'data/ventes_propres.csv'.")
print(df.head())