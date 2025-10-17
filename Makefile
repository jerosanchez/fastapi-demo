install: ## Install dependencies in virtual environment
	bash -c "source .venv/bin/activate && pip install -r requirements.txt"

freeze: ## Freeze current dependencies
	bash -c "source .venv/bin/activate && pip freeze > requirements.txt"

lint: ## Run linting
	bash -c "source .venv/bin/activate && flake8 app/ --max-line-length=80"
	bash -c "source .venv/bin/activate && black --check app/ --line-length=80"
	bash -c "source .venv/bin/activate && isort --check-only app/ --profile=black --line-length=80"

format: ## Format code
	bash -c "source .venv/bin/activate && black app/ --line-length=80"
	bash -c "source .venv/bin/activate && isort app/ --profile=black --line-length=80"

clean: ## Clean cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

migrate: ## Run database migrations
	bash -c "source .venv/bin/activate && alembic upgrade head"

db-revision: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	bash -c "source .venv/bin/activate && alembic revision --autogenerate -m \"$$msg\""

db-reset: ## Reset Docker PostgreSQL volumes
	@echo "WARNING: This will delete all PostgreSQL data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]
	docker compose -f docker-compose.local.yml down -v
	docker volume prune -f

dev-up: ## Start development environment
	docker compose -f docker-compose.local.yml up --build -d

dev-down: ## Stop development environment
	docker compose -f docker-compose.local.yml down

.PHONY: install freeze run lint format clean migrate db-revision db-reset dev-up dev-down