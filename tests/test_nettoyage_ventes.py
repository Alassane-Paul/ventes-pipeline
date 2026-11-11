import json

import pandas as pd
import pytest

from scripts.nettoyage_ventes import clean_sales


CSV_COLUMNS = [
    "commande_id",
    "client",
    "ville",
    "produit",
    "categorie",
    "quantite",
    "prix_unitaire",
    "date_commande",
]


def write_csv(path, rows, columns=CSV_COLUMNS):
    pd.DataFrame(rows, columns=columns).to_csv(path, index=False)


def valid_row(
    commande_id=1,
    quantite=1,
    prix_unitaire=10,
    date_commande="2026-01-15",
    ville="Lomé",
):
    return [
        commande_id,
        "Awa",
        ville,
        "Formation Python",
        "Développement",
        quantite,
        prix_unitaire,
        date_commande,
    ]


def test_rejects_invalid_values_and_writes_run_outputs(tmp_path):
    source = tmp_path / "input.csv"
    output_csv = tmp_path / "nested" / "clean.csv"
    output_parquet = tmp_path / "nested" / "clean.parquet"
    metadata_json = tmp_path / "nested" / "run.json"
    rows = [
        valid_row(ville=None),
        valid_row(ville=None),
        valid_row(commande_id=2, quantite=-1),
        valid_row(commande_id=3, prix_unitaire=-2),
        valid_row(commande_id=4, date_commande="2026-02-30"),
        valid_row(commande_id=5, prix_unitaire="invalide"),
        valid_row(commande_id=6, quantite=0),
    ]
    write_csv(source, rows)

    cleaned, metadata = clean_sales(
        source, output_csv, output_parquet, metadata_json
    )

    assert cleaned["commande_id"].tolist() == [1, 6]
    assert cleaned["ville"].tolist() == ["Inconnue", "Lomé"]
    assert cleaned["montant_total"].tolist() == [10, 0]
    assert metadata["rows_before"] == 7
    assert metadata["rows_after"] == 2
    assert metadata["rejected_rows"] == 4
    assert metadata["duplicates_removed"] == 1
    assert metadata["rejection_reasons"] == {
        "quantite_invalide": 1,
        "prix_unitaire_invalide": 2,
        "date_commande_invalide": 1,
    }

    assert pd.read_parquet(output_parquet)["commande_id"].tolist() == [1, 6]
    assert pd.read_csv(output_csv)["commande_id"].tolist() == [1, 6]
    assert json.loads(metadata_json.read_text(encoding="utf-8")) == metadata
    assert pd.Timestamp(metadata["run_at"]).tzinfo is not None


def test_cleaning_adapts_to_changed_csv_rows_and_extra_columns(tmp_path):
    source = tmp_path / "changed.csv"
    output = tmp_path / "clean.csv"
    columns = CSV_COLUMNS + ["source_batch"]
    rows = [
        valid_row(commande_id=10) + ["batch-a"],
        valid_row(commande_id=11, quantite=3) + ["batch-b"],
    ]
    write_csv(source, rows, columns)

    cleaned, metadata = clean_sales(source, output)

    assert len(cleaned) == 2
    assert cleaned["source_batch"].tolist() == ["batch-a", "batch-b"]
    assert cleaned["montant_total"].tolist() == [10, 30]
    assert metadata["rows_before"] == 2
    assert metadata["rows_after"] == 2
    assert metadata["rejected_rows"] == 0


def test_missing_required_columns_fails_explicitly(tmp_path):
    source = tmp_path / "incomplete.csv"
    write_csv(source, [valid_row()[:-1]], CSV_COLUMNS[:-1])

    with pytest.raises(ValueError, match="date_commande"):
        clean_sales(source, tmp_path / "clean.csv")
