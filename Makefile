# Variables
VENV   = venv
PIP    = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3

all: diapo.pdf run
	@echo "make done."

run: src/main.py $(VENV)/pygame_installed
	@$(PYTHON) src/main.py

uidemo: src/main.py $(VENV)/pygame_installed
	@$(PYTHON) src/main.py uidemo

diapo.pdf: diapo/*.tex
	@pdflatex -halt-on-error -output-directory=diapo/ diapo/diapo.tex
	@mv diapo/diapo.pdf .

$(VENV)/pygame_installed: $(VENV)
	@$(PIP) install pygame
	touch $(VENV)/pygame_installed

$(VENV):
	@echo "Création de l'environement virtuel..."
	@python3 -m venv $(VENV)
	@echo "Fait."

clean:
	@rm -rf $(VENV)
	@echo "Environement virtuel supprimé."
	@rm diapo.pdf diapo/*.aux diapo/*.snm diapo/*.nav diapo/*.log diapo/*.toc diapo/*.out

.PHONY: run clean all