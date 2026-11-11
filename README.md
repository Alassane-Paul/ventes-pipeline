# Analyse des ventes

Petit projet Python de préparation et d’analyse de données de ventes. Le pipeline nettoie les commandes brutes, calcule des indicateurs de chiffre d’affaires et produit des graphiques.

## Structure du projet

```text
.
├── data/
│   ├── ventes_brutes.csv       # Données source
│   ├── ventes_propres.csv      # Données nettoyées, générées par le pipeline
│   ├── ventes_propres.parquet  # Export Parquet
│   └── metadata_run.json       # Métadonnées de la dernière exécution
├── images/                     # Graphiques générés par l’analyse
├── notebooks/
│   └── analyse_ventes.ipynb
├── scripts/
│   ├── nettoyage_ventes.py     # Préparation des données
│   └── analyse_ventes.py       # Calcul des indicateurs et graphiques
├── tests/
│   └── test_nettoyage_ventes.py
├── Makefile
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

Depuis la racine du projet, utilisez GNU Make (ou exécutez les commandes Python directement) :

```sh
make clean
make analyze
make test
```

Sans GNU Make, lancez les scripts dans cet ordre :

```powershell
python scripts\nettoyage_ventes.py
python scripts\analyse_ventes.py
python -m pytest
```

`make analyze` nettoie puis analyse les données. Le nettoyage supprime les doublons, remplace les villes manquantes par `Inconnue`, et rejette les lignes dont la quantité ou le prix est manquant, non numérique ou négatif, ou dont la date est invalide. Il calcule ensuite `montant_total` (quantité × prix unitaire) et produit le CSV, un export Parquet et `data/metadata_run.json`. Ce manifeste contient l’heure UTC d’exécution, les nombres de lignes avant/après, les rejets par type et les doublons supprimés. Les colonnes d’entrée supplémentaires sont conservées.

Les tests `pytest` couvrent les valeurs invalides, les exports, les métadonnées et un CSV dont le contenu et les colonnes changent. GitHub Actions exécute les tests et le pipeline à chaque push et pull request.

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