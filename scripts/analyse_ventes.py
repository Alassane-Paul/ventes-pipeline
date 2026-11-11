from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data_path = PROJECT_ROOT / "data" / "ventes_propres.csv"
    images_path = PROJECT_ROOT / "images"
    images_path.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(data_path, parse_dates=["date_commande"])

    chiffre_affaires_total = df["montant_total"].sum()
    print(f"Chiffre d'affaires total : {chiffre_affaires_total:,.0f} FCFA")

    ventes_par_produit = (
        df.groupby("produit")["montant_total"].sum().sort_values(ascending=False)
    )
    print("\nChiffre d'affaires par produit :")
    print(ventes_par_produit)

    ventes_par_ville = (
        df.groupby("ville")["montant_total"].sum().sort_values(ascending=False)
    )
    print("\nChiffre d'affaires par ville :")
    print(ventes_par_ville)

    top_clients = df.groupby("client")["montant_total"].sum().sort_values(ascending=False)
    print("\nTop clients :")
    print(top_clients)

    ventes_par_produit.plot(
        kind="bar", title="Chiffre d'affaires par produit", ylabel="Montant en FCFA"
    )
    plt.tight_layout()
    plt.savefig(images_path / "ventes_par_produit.png")
    plt.close()

    ventes_par_ville.plot(
        kind="bar", title="Chiffre d'affaires par ville", ylabel="Montant en FCFA"
    )
    plt.tight_layout()
    plt.savefig(images_path / "ventes_par_ville.png")
    plt.close()
    print("\nGraphiques générés dans le dossier images/.")

    commande_total = df["commande_id"].count()
    print(f"\nNombre total de commandes : {commande_total}")

    panier_moyen = df["montant_total"].mean()
    print(f"\nPanier moyen : {panier_moyen:,.0f} FCFA")

    top_ville = ventes_par_ville.head(1)
    print("\nVille générant plus de revenus")
    print(top_ville)

    top_3_clients = top_clients.head(3)
    print("\nTop 3 clients :")
    print(top_3_clients)

    evolution = df.groupby(df["date_commande"].dt.date)["montant_total"].sum()
    evolution.plot(
        kind="line",
        title="Évolution du chiffre d’affaires",
        ylabel="Montant en FCFA",
    )
    plt.tight_layout()
    plt.savefig(images_path / "evolution_chiffre_affaires.png")
    plt.close()


if __name__ == "__main__":
    main()
