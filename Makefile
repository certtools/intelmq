# SPDX-FileCopyrightText: 2023 Filip Pokorný
# SPDX-License-Identifier: AGPL-3.0-or-later

.PHONY: coverage docs clean

coverage:
	python -m pytest --cov=intelmq -v

docs: mkdocs.yml docs/* intelmq/etc/feeds.yaml intelmq/etc/harmonization.conf intelmq/lib/harmonization.py
	python3 scripts/generate-feeds-docs.py
	python3 scripts/generate-event-docs.py
	mkdocs build

clean:
	rm -rf docs_build .mypy_cache .coverage .pytest_cache dist