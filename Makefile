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

run-dynamic:
	@make dev ARGS="run_dynamic"

run:
	@make dev ARGS="run_irl"

clean:
	@rm -rf __pycache__ src/__pycache__ src/*.pyc src/*/__pycache__ src/*/*.pyc

relatorio: relatorio-build

relatorio-build:
	@echo "Compilando relatorio..."
	@typst compile relatorio/relatorio.typ

relatorio-watch:
	@echo "Assistindo alteracoes no relatorio..."
	@typst watch relatorio/relatorio.typ

relatorio-clean:
	@rm -rf relatorio/relatorio.pdf