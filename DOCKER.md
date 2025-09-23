# Docker Integration Guide

This guide explains how to run the Temporal Workflow Practice project using Docker Compose.

## Architecture

The Docker setup includes the following services:

- **PostgreSQL**: Database for Temporal server and visibility store
- **Temporal Server**: Core workflow engine
- **Temporal UI**: Web interface for monitoring workflows
- **Redis**: Caching and session storage
- **FastAPI API**: REST API for workflow management
- **Temporal Worker**: Processes workflow tasks

## Quick Start

### 1. Start All Services

```bash
# Start all services in detached mode
make docker-up

# Or start with build
make docker-up-build
```

### 2. Check Service Status

```bash
# Check if all services are running
make docker-status

# Check health of all services
make health-check
```

### 3. View Logs

```bash
# View all logs
make docker-logs

# View specific service logs
make docker-logs-api
make docker-logs-worker
make docker-logs-temporal
```

## Service URLs

Once running, you can access:

- **Temporal UI**: http://localhost:8080
- **FastAPI API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379
- **Temporal Server**: localhost:7233

## Development Workflow

### Start Development Environment

```bash
# Complete setup (first time only)
make dev-setup

# Start core services (Temporal, PostgreSQL, Redis)
make dev-start

# Run API locally (in another terminal)
make run-dev

# Run worker locally (in another terminal)
make run-worker
```

### Stop Development Environment

```bash
# Stop all services
make dev-stop

# Or stop and remove volumes
make docker-down-volumes
```

## Service Management

### Start Specific Services

```bash
# Start only Temporal services
make start-temporal

# Start only application services
make start-app
```

### Restart Services

```bash
# Restart API
make restart-api

# Restart worker
make restart-worker
```

## Testing the Setup

### 1. Check API Health

```bash
curl http://localhost:8000/api/v1/health/
```

### 2. Start a Workflow

```bash
curl -X POST http://localhost:8000/api/v1/workflows/start \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "simple_workflow",
    "input_data": {"required_field": "test_value"},
    "user_id": "test_user"
  }'
```

### 3. Monitor in Temporal UI

Visit http://localhost:8080 to see:
- Running workflows
- Workflow history
- Activity executions
- Task queue status

## Configuration

### Environment Variables

The services use the following environment variables:

- `ENVIRONMENT`: Set to `development` for local development
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `TEMPORAL_HOST`: Temporal server address
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

### Database Setup

The PostgreSQL service automatically creates:
- `temporal` database for Temporal server
- `temporal_visibility` database for workflow visibility

## Troubleshooting

### Common Issues

1. **Services not starting**: Check if ports are already in use
2. **Database connection errors**: Wait for PostgreSQL to be ready
3. **Temporal connection errors**: Ensure Temporal server is healthy

### Debug Commands

```bash
# Check service logs
make docker-logs

# Check specific service status
docker-compose ps

# Restart problematic service
docker-compose restart <service-name>

# View detailed logs
docker-compose logs --tail=100 <service-name>
```

### Clean Reset

```bash
# Stop all services and remove volumes
make docker-down-volumes

# Clean up Docker resources
make docker-clean

# Start fresh
make docker-up-build
```

## Production Considerations

For production deployment:

1. **Security**: Change default passwords and secrets
2. **Persistence**: Use named volumes for data persistence
3. **Networking**: Configure proper network security
4. **Monitoring**: Add monitoring and alerting
5. **Scaling**: Configure multiple worker instances

## File Structure

```
docker/
├── Dockerfile              # Multi-stage Docker build
├── init-db.sh             # Database initialization script
└── temporal-config/
    └── development-sql.yaml  # Temporal server configuration

docker-compose.yml         # Main Docker Compose configuration
Makefile                   # Development commands
DOCKER.md                  # This documentation
```

## Next Steps

1. Explore the Temporal UI to understand workflow execution
2. Try the API endpoints using the interactive docs
3. Modify workflows and activities in `src/workflows/`
4. Add new API endpoints in `src/api/routes/`
5. Run tests to ensure everything works correctly
