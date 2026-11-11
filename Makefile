PYTHON ?= python

.PHONY: analyze clean test

analyze:
	$(PYTHON) scripts/nettoyage_ventes.py
	$(PYTHON) scripts/analyse_ventes.py

clean:
	$(PYTHON) -c "from pathlib import Path; files = [Path('data/ventes_propres.csv'), Path('data/ventes_propres.parquet'), Path('data/metadata_run.json'), Path('images/ventes_par_produit.png'), Path('images/ventes_par_ville.png'), Path('images/evolution_chiffre_affaires.png')]; [path.unlink() for path in files if path.exists()]"

test:
	$(PYTHON) -m pytest
