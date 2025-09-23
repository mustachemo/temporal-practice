# Makefile for Temporal Workflow Practice Project

.PHONY: help install test lint format clean build run-dev run-worker run-docker stop-docker logs logs-worker

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	uv pip install -e ".[dev]"

test: ## Run tests
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term

test-unit: ## Run unit tests only
	pytest tests/unit/ -v

test-integration: ## Run integration tests only
	pytest tests/integration/ -v

test-e2e: ## Run end-to-end tests only
	pytest tests/e2e/ -v

lint: ## Run linting
	uv lint src/ tests/

format: ## Format code
	uv format src/ tests/

clean: ## Clean build artifacts
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: ## Build Docker image
	docker build -f docker/Dockerfile -t temporal-practice:latest .

run-dev: ## Run development server
	python -m src.main --config-name=config environment=development

run-worker: ## Run Temporal worker
	python scripts/run_worker.py --config-name=config environment=development

run-docker: ## Run with Docker Compose
	docker-compose -f docker/docker-compose.yml up --build

stop-docker: ## Stop Docker Compose
	docker-compose -f docker/docker-compose.yml down

logs: ## Show application logs
	docker-compose -f docker/docker-compose.yml logs -f app

logs-worker: ## Show worker logs
	docker-compose -f docker/docker-compose.yml logs -f worker
