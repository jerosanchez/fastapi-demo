VENV_ACTIVATE = source .venv/bin/activate &&
MAX_LINE_LENGTH = 90

## --- Dependency management commands

install: ## Install dependencies in virtual environment
	bash -c "$(VENV_ACTIVATE) pip install -r requirements.txt"

freeze: ## Freeze current dependencies
	bash -c "$(VENV_ACTIVATE) pip freeze > requirements.txt"

## TODO: Split dev and prod dependencies in separate files

## --- Application commands

lint: ## Run linting
	bash -c "$(VENV_ACTIVATE) flake8 app/ --max-line-length=$(MAX_LINE_LENGTH)"
	bash -c "$(VENV_ACTIVATE) black --check app/ --line-length=$(MAX_LINE_LENGTH)"
	bash -c "$(VENV_ACTIVATE) isort --check-only app/ --profile=black --line-length=$(MAX_LINE_LENGTH)"

format: ## Format code
	bash -c "$(VENV_ACTIVATE) black app/ --line-length=$(MAX_LINE_LENGTH)"
	bash -c "$(VENV_ACTIVATE) isort app/ --profile=black --line-length=$(MAX_LINE_LENGTH)"

test: ## Run tests
	bash -c "$(VENV_ACTIVATE) pytest tests/"

run: ## Run the application
	bash -c "$(VENV_ACTIVATE) fastapi dev app/main.py"

clean: ## Clean cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

## --- Database commands

db-reset: ## Reset Docker PostgreSQL volumes
	@echo "WARNING: This will delete all PostgreSQL data!"
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]
	docker compose -f docker-compose.local.yml down -v
	docker volume prune -f

db-revision: ## Create a new migration
	@read -p "Enter migration message: " msg; \
	bash -c "$(VENV_ACTIVATE) alembic revision --autogenerate -m \"$$msg\""

db-migrate: ## Run database migrations
	bash -c "$(VENV_ACTIVATE) alembic upgrade head"

db-sample-data: ## Insert sample data into the database
	docker exec -i fastapi-demo-api-db-1 \
	psql -U admin_user -d fastapi_demo_db < scripts/insert_sample_data.sql

## --- Docker commands

dev-up: ## Start development environment
	docker image prune -f
	docker compose -f docker-compose.local.yml up --build -d

dev-down: ## Stop development environment
	docker compose -f docker-compose.local.yml down

push-dev: ## Build and push the image for development
	docker login
	docker build -f Dockerfile --target development -t jerosanchez/fastapi-demo .
	docker push jerosanchez/fastapi-demo

push-prod: ## Build and push the image for production
	docker login
	docker build -f Dockerfile --target production -t jerosanchez/fastapi-demo .
	docker push jerosanchez/fastapi-demo

.PHONY: install freeze run lint format test clean db-migrate db-revision db-reset db-sample-data dev-up dev-down push-dev push-prod