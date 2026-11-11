import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "commande_id",
    "client",
    "ville",
    "produit",
    "categorie",
    "quantite",
    "prix_unitaire",
    "date_commande",
}
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def clean_sales(
    input_csv: Path | str,
    output_csv: Path | str,
    output_parquet: Path | str | None = None,
    metadata_json: Path | str | None = None,
) -> tuple[pd.DataFrame, dict[str, object]]:
    raw = pd.read_csv(input_csv)
    missing_columns = REQUIRED_COLUMNS.difference(raw.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colonnes obligatoires manquantes : {missing}")

    rows_before = len(raw)
    unique = raw.drop_duplicates().copy()
    duplicates_removed = rows_before - len(unique)

    unique["quantite"] = pd.to_numeric(unique["quantite"], errors="coerce")
    unique["prix_unitaire"] = pd.to_numeric(
        unique["prix_unitaire"], errors="coerce"
    )
    unique["date_commande"] = pd.to_datetime(
        unique["date_commande"], errors="coerce", format="mixed"
    )

    invalid_quantity = (
        unique["quantite"].isna()
        | ~np.isfinite(unique["quantite"])
        | (unique["quantite"] < 0)
    )
    invalid_price = (
        unique["prix_unitaire"].isna()
        | ~np.isfinite(unique["prix_unitaire"])
        | (unique["prix_unitaire"] < 0)
    )
    invalid_date = unique["date_commande"].isna()
    rejected = invalid_quantity | invalid_price | invalid_date

    rejection_reasons = {
        "quantite_invalide": int(invalid_quantity.sum()),
        "prix_unitaire_invalide": int(invalid_price.sum()),
        "date_commande_invalide": int(invalid_date.sum()),
    }

    cleaned = unique.loc[~rejected].copy()
    cleaned["ville"] = cleaned["ville"].fillna("Inconnue")
    cleaned["montant_total"] = cleaned["quantite"] * cleaned["prix_unitaire"]

    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(output_csv, index=False)

    if output_parquet is not None:
        output_parquet = Path(output_parquet)
        output_parquet.parent.mkdir(parents=True, exist_ok=True)
        cleaned.to_parquet(output_parquet, index=False)

    metadata: dict[str, object] = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "rows_before": rows_before,
        "rows_after": len(cleaned),
        "rejected_rows": int(rejected.sum()),
        "duplicates_removed": duplicates_removed,
        "rejection_reasons": rejection_reasons,
    }
    if metadata_json is not None:
        metadata_json = Path(metadata_json)
        metadata_json.parent.mkdir(parents=True, exist_ok=True)
        metadata_json.write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    return cleaned, metadata


def main() -> None:
    cleaned, metadata = clean_sales(
        PROJECT_ROOT / "data" / "ventes_brutes.csv",
        PROJECT_ROOT / "data" / "ventes_propres.csv",
        PROJECT_ROOT / "data" / "ventes_propres.parquet",
        PROJECT_ROOT / "data" / "metadata_run.json",
    )
    print("Nettoyage terminé.")
    print(f"Lignes conservées : {metadata['rows_after']} / {metadata['rows_before']}")
    print(f"Lignes rejetées : {metadata['rejected_rows']}")
    print("Sorties : data/ventes_propres.csv, data/ventes_propres.parquet")
    print(cleaned.head())


if __name__ == "__main__":
    main()
