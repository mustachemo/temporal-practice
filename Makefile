# Makefile for Temporal Workflow Practice Project

.PHONY: help install test lint format clean build run-dev run-worker docker-up docker-down docker-logs docker-clean

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Development Commands
install: ## Install dependencies
	uv pip install -e ".[dev]"

test: ## Run tests
	uv run pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit: ## Run unit tests only
	uv run pytest tests/unit/ -v

test-integration: ## Run integration tests only
	uv run pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests only
	uv run pytest tests/e2e/ -v

lint: ## Run linting
	uv run uv lint src/ tests/

format: ## Format code
	uv run uv format src/ tests/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Local Development
run-dev: ## Run development server
	uv run python -m src.main --config-name=config environment=development

run-worker: ## Run Temporal worker
	uv run python -m scripts.run_worker --config-name=config environment=development

# Docker Commands
docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start all services with Docker Compose
	docker-compose up -d

docker-up-build: ## Start all services and build images
	docker-compose up --build -d

docker-down: ## Stop all services
	docker-compose down

docker-down-volumes: ## Stop all services and remove volumes
	docker-compose down -v

docker-logs: ## Show logs for all services
	docker-compose logs -f

docker-logs-api: ## Show API logs
	docker-compose logs -f api

docker-logs-worker: ## Show worker logs
	docker-compose logs -f worker

docker-logs-temporal: ## Show Temporal server logs
	docker-compose logs -f temporal

docker-logs-postgres: ## Show PostgreSQL logs
	docker-compose logs -f postgresql

docker-status: ## Show status of all services
	docker-compose ps

docker-clean: ## Clean up Docker resources
	docker-compose down -v --remove-orphans
	docker system prune -f

# Service-specific commands
start-temporal: ## Start only Temporal services (server + UI + postgres)
	docker-compose up -d postgresql temporal temporal-ui

start-app: ## Start all services (Temporal, API, Worker, UI)
	docker-compose up -d

restart-api: ## Restart API service
	docker-compose restart api

restart-worker: ## Restart worker service
	docker-compose restart worker

# Health checks
health-check: ## Check health of all services
	@echo "Checking service health..."
	@curl -f http://localhost:8000/api/v1/health/ && echo "✅ API: Healthy" || echo "❌ API: Unhealthy"
	@curl -f http://localhost:8080/ && echo "✅ Temporal UI: Healthy" || echo "❌ Temporal UI: Unhealthy"
	@docker-compose exec temporal temporal workflow list --address localhost:7233 > /dev/null && echo "✅ Temporal Server: Healthy" || echo "❌ Temporal Server: Unhealthy"

# Development workflow
dev-setup: ## Complete development setup
	@echo "Setting up development environment..."
	uv venv
	uv sync
	@echo "✅ Development environment ready!"

dev-start: ## Start development environment
	@echo "Starting development environment..."
	docker-compose up -d postgresql temporal temporal-ui redis
	@echo "Waiting for services to be ready..."
	sleep 10
	@echo "✅ Development environment started!"
	@echo "🌐 Temporal UI: http://localhost:8080"
	@echo "🗄️  PostgreSQL: localhost:5432"
	@echo "📊 Redis: localhost:6379"
	@echo "⚡ Temporal Server: localhost:7233"

dev-stop: ## Stop development environment
	docker-compose down
	@echo "✅ Development environment stopped!"
