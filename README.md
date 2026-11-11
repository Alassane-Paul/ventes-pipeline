# Analyse des ventes

Petit projet Python de préparation et d’analyse de données de ventes. Le pipeline nettoie les commandes brutes, calcule des indicateurs de chiffre d’affaires et produit des graphiques.

## Structure du projet

```text
.
├── data/
│   ├── ventes_brutes.csv       # Données source
│   └── ventes_propres.csv      # Données nettoyées, générées par le pipeline
├── images/                     # Graphiques générés par l’analyse
├── notebooks/
│   └── analyse_ventes.ipynb
├── scripts/
│   ├── nettoyage_ventes.py     # Préparation des données
│   └── analyse_ventes.py       # Calcul des indicateurs et graphiques
└── requirements.txt
```

## Prérequis

- Python 3
- `pip`

Depuis la racine du projet, créez un environnement virtuel et installez les dépendances (PowerShell) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Exécution

Lancez les scripts depuis la racine du projet, dans cet ordre. Le second script utilise le fichier produit par le premier.

```powershell
python scripts\nettoyage_ventes.py
python scripts\analyse_ventes.py
```

Le nettoyage supprime les doublons, remplace les villes manquantes par `Inconnue`, convertit la date et les valeurs numériques, écarte les lignes sans quantité ou prix unitaire valide, puis calcule `montant_total` (quantité × prix unitaire). Le résultat est enregistré dans `data/ventes_propres.csv`.

L’analyse affiche le chiffre d’affaires total et par produit et par ville, les clients classés par chiffre d’affaires, le nombre de commandes, le panier moyen, la ville la plus rentable et les trois meilleurs clients. Elle génère également les graphiques suivants dans `images/` :

- `ventes_par_produit.png`
- `ventes_par_ville.png`
- `evolution_chiffre_affaires.png`

## Données d’entrée

`data/ventes_brutes.csv` doit contenir les colonnes suivantes :

| Colonne | Description |
|---|---|
| `commande_id` | Identifiant de la commande |
| `client` | Nom du client |
| `ville` | Ville du client |
| `produit` | Produit commandé |
| `categorie` | Catégorie du produit |
| `quantite` | Quantité commandée |
| `prix_unitaire` | Prix unitaire en FCFA |
| `date_commande` | Date de la commande |

Le montant total est calculé par ligne et exprimé en FCFA.