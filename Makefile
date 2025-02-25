# Variables
VENV   = venv
PIP    = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python3

run: src/main.py $(VENV)/pygame_installed
	@$(PYTHON) src/main.py

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

.PHONY: run clean