all: dev

install:
	@pip install -r requirements.txt

pre-install:
#	@pip freeze > requirements.txt
	@pip install pipreqs
	@pipreqs --force .

ARGS = $(filter-out $@,$(MAKECMDGOALS))

# Prevent Make from treating arguments as targets
%:
	@:

dev:
	@python src/main.py $(ARGS)

test:
	@make dev ARGS="test"

run-random:
	@make dev ARGS="run_random"

run-dynamic:
	@make dev ARGS="run_dynamic"

clean:
	@rm -rf __pycache__ src/__pycache__ src/*.pyc src/*/__pycache__ src/*/*.pyc

.PHONY: docs # The default target is to build the docs

pre-docs:
	@pip install pdoc

docs:
	@python src/doc_generator.py

docs-clean:
	@rm -rf docs

relatorio: relatorio-build

relatorio-build:
	@echo "Compilando relatorio..."
	@typst compile relatorio/relatorio.typ

relatorio-watch:
	@echo "Assistindo alteracoes no relatorio..."
	@typst watch relatorio/relatorio.typ

relatorio-clean:
	@rm -rf relatorio/relatorio.pdf