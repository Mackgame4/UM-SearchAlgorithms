all: dev

dev:
	@python src/main.py $(args)

test:
	@python src/main.py test

run_dynamic:
	@python src/main.py run_dynamic

relatorio: relatorio_build

relatorio_build:
	@echo "Compilando relatorio..."
	@typst compile relatorio/relatorio.typ

relatorio_watch:
	@echo "Assistindo alteracoes no relatorio..."
	@typst watch relatorio/relatorio.typ

relatorio_clean:
	@rm -rf relatorio/relatorio.pdf