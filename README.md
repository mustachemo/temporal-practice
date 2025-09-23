# Temporal Workflow Practice Project

A comprehensive Temporal workflow application built with Python, FastAPI, and Hydra configuration management. This project demonstrates best practices for building scalable, reliable workflow systems.

## 🚀 Features

- **Temporal Workflows**: Complex workflow orchestration with activities
- **FastAPI API**: RESTful API for workflow management
- **Hydra Configuration**: Flexible configuration management with environment overrides
- **Comprehensive Logging**: Structured logging with Loguru and Rich
- **Monitoring**: Performance metrics and health checks
- **Testing**: Unit, integration, and end-to-end tests
- **Docker Support**: Containerized deployment with Docker Compose

## 🏗️ Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Client] --> B[FastAPI API]
    end
    
    subgraph "Application Layer"
        B --> C[Workflow Service]
        C --> D[Temporal Client]
    end
    
    subgraph "Workflow Engine"
        D --> E[Temporal Server]
        E --> F[Workflow Workers]
        F --> G[Activities]
    end
    
    subgraph "Data Layer"
        G --> H[Database]
        G --> I[External APIs]
        G --> J[File System]
    end
    
    subgraph "Infrastructure"
        K[Docker Compose]
        L[Redis Cache]
        M[PostgreSQL]
    end
```

## 📁 Project Structure

```
temporal-practice/
├── .cursor/                    # Cursor IDE rules
├── conf/                      # Hydra configuration
├── docs/                      # Documentation
├── src/                       # Source code
│   ├── api/                   # FastAPI application
│   ├── workflows/             # Temporal workflows
│   ├── activities/            # Temporal activities
│   ├── workers/               # Temporal workers
│   ├── models/                # Pydantic models
│   ├── services/              # Business logic
│   └── utils/                 # Utilities
├── tests/                     # Test suite
├── scripts/                   # Utility scripts
├── docker/                    # Docker configuration
└── logs/                      # Log files
```

## 🛠️ Technology Stack

- **Python 3.11+**: Core language
- **Temporal**: Workflow orchestration
- **FastAPI**: Web framework
- **Hydra**: Configuration management
- **Loguru**: Logging
- **Rich**: Console output
- **Pydantic**: Data validation
- **Pytest**: Testing framework
- **Docker**: Containerization

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd temporal-practice
   ```

2. **Install dependencies**
   ```bash
   # Using uv (recommended)
   uv pip install -e ".[dev]"
   
   # Or using pip
   pip install -e ".[dev]"
   ```

3. **Start infrastructure services**
   ```bash
   make run-docker
   ```

4. **Run the application**
   ```bash
   # Start the API server
   make run-dev
   
   # In another terminal, start the worker
   make run-worker
   ```

### Development Setup

1. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

2. **Run tests**
   ```bash
   make test
   ```

3. **Format code**
   ```bash
   make format
   ```

4. **Lint code**
   ```bash
   make lint
   ```

## 📖 Usage

### Starting a Workflow

```bash
curl -X POST "http://localhost:8000/api/v1/workflows/start" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "complex_workflow",
    "input_data": {
      "user_id": "user_123",
      "data": {"key": "value"}
    },
    "user_id": "user_123"
  }'
```

### Checking Workflow Status

```bash
curl "http://localhost:8000/api/v1/workflows/{workflow_id}/status"
```

### Getting Workflow Result

```bash
curl "http://localhost:8000/api/v1/workflows/{workflow_id}/result"
```

## 🔧 Configuration

The application uses Hydra for configuration management. Configuration files are located in the `conf/` directory:

- `conf/config.yaml`: Main configuration
- `conf/config/`: Configuration modules
- `conf/env/`: Environment-specific overrides

### Environment Variables

```bash
# Required
ENVIRONMENT=development
DATABASE_URL=postgresql://user:password@localhost:5432/temporal_db
REDIS_URL=redis://localhost:6379/0
TEMPORAL_HOST=localhost:7233

# Optional
SECRET_KEY=your-secret-key
LOG_LEVEL=INFO
```

## 🧪 Testing

### Run All Tests
```bash
make test
```

### Run Specific Test Types
```bash
# Unit tests only
make test-unit

# Integration tests only
make test-integration

# End-to-end tests only
make test-e2e
```

### Test Coverage
```bash
make test
# Coverage report will be generated in htmlcov/
```

## 📊 Monitoring

### Health Checks
- Basic: `GET /health`
- Detailed: `GET /health/detailed`

### Metrics
- Workflow execution metrics
- Activity performance metrics
- API request metrics
- System resource metrics

### Logging
- Structured JSON logs
- Rich console output
- Log rotation and retention
- Correlation IDs for tracing

## 🐳 Docker

### Build Images
```bash
make build
```

### Run with Docker Compose
```bash
make run-docker
```

### Stop Services
```bash
make stop-docker
```

## 📚 API Documentation

Once the application is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Add tests for new functionality
4. Ensure all tests pass
5. Format and lint your code
6. Submit a pull request

### Development Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit often
git add .
git commit -m "feat: add new workflow feature"

# Push changes
git push origin feature/your-feature-name
```

## 📝 Code Standards

This project follows strict coding standards defined in `.cursor/rules/`:

- **Python Standards**: Type hints, docstrings, error handling
- **Temporal Patterns**: Workflow and activity best practices
- **FastAPI Standards**: API design and testing patterns
- **Configuration**: Hydra configuration management
- **Logging**: Structured logging and monitoring
- **Testing**: Comprehensive test coverage

## 🐛 Troubleshooting

### Common Issues

1. **Temporal Server Connection**
   ```bash
   # Check if Temporal server is running
   docker-compose ps temporal
   ```

2. **Database Connection**
   ```bash
   # Check database connectivity
   docker-compose exec postgresql psql -U temporal -d temporal
   ```

3. **Port Conflicts**
   ```bash
   # Check if ports are in use
   lsof -i :8000  # API server
   lsof -i :7233  # Temporal server
   ```

### Logs

```bash
# Application logs
make logs

# Worker logs
make logs-worker

# All services
docker-compose logs -f
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Temporal](https://temporal.io/) for workflow orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Hydra](https://hydra.cc/) for configuration management
- [Loguru](https://loguru.readthedocs.io/) for logging
- [Rich](https://rich.readthedocs.io/) for beautiful console output
