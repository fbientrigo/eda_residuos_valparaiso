.PHONY: install test demo sources
install:
	python -m pip install -e ".[dev]"

test:
	pytest

demo:
	residuos-valpo run-all --config configs/vina_del_mar.yaml

sources:
	residuos-valpo sources validate --config configs/vina_del_mar.yaml
