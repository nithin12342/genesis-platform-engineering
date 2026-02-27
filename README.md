# Shared Infrastructure

This directory contains shared services used across all 6 meta-repositories:

- **HashiCorp Vault**: Secrets management (development mode)
- **PostgreSQL**: Shared database for development
- **Redis**: Shared cache and pub/sub
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Bash shell (for setup scripts)

### Start All Services

```bash
# Navigate to shared-infrastructure directory
cd shared-infrastructure

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Initialize Vault

```bash
# Make setup script executable
chmod +x vault-setup.sh

# Run Vault setup
./vault-setup.sh
```

## 📦 Services

### HashiCorp Vault

**Purpose**: Centralized secrets management for all meta-repositories

**Access**:
- UI: http://localhost:8200
- Token: `dev-root-token` (development only)

**Usage**:
```bash
# Set environment variables
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='dev-root-token'

# Read a secret
vault kv get secret/nebula/database

# Write a secret
vault kv put secret/myapp/config key=value

# List secrets
vault kv list secret/
```

**Python Example**:
```python
import hvac

client = hvac.Client(
    url='http://localhost:8200',
    token='dev-root-token'
)

# Read secret
secret = client.secrets.kv.v2.read_secret_version(
    path='nebula/database'
)
print(secret['data']['data'])
```

### PostgreSQL

**Purpose**: Shared database for development and testing

**Access**:
- Host: localhost
- Port: 5432
- User: postgres
- Password: postgres
- Database: shared_db

**Connection String**:
```
postgresql://postgres:postgres@localhost:5432/shared_db
```

**Usage**:
```bash
# Connect with psql
docker exec -it shared-postgres psql -U postgres -d shared_db

# Create database for a meta-repo
docker exec -it shared-postgres psql -U postgres -c "CREATE DATABASE nebula_db;"
```

### Redis

**Purpose**: Shared cache and pub/sub for all services

**Access**:
- Host: localhost
- Port: 6379
- No password (development only)

**Usage**:
```bash
# Connect with redis-cli
docker exec -it shared-redis redis-cli

# Test connection
docker exec -it shared-redis redis-cli ping
```

**Python Example**:
```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('key', 'value')
print(r.get('key'))
```

### Prometheus

**Purpose**: Metrics collection from all services

**Access**:
- UI: http://localhost:9090
- Metrics endpoint: http://localhost:9090/metrics

**Configuration**:
- Edit `prometheus/prometheus.yml` to add scrape targets
- Reload configuration: `docker-compose restart prometheus`

**Adding a Service**:
```yaml
# Add to prometheus/prometheus.yml
scrape_configs:
  - job_name: 'my-service'
    static_configs:
      - targets: ['my-service:8000']
        labels:
          service: 'my-service'
          meta_repo: 'my-meta-repo'
```

### Grafana

**Purpose**: Metrics visualization and dashboards

**Access**:
- UI: http://localhost:3000
- Username: admin
- Password: admin

**Features**:
- Pre-configured Prometheus datasource
- Create custom dashboards
- Set up alerts

**Creating a Dashboard**:
1. Open Grafana UI
2. Click "+" → "Dashboard"
3. Add panel with Prometheus query
4. Save dashboard

## 🔧 Configuration

### Environment Variables

Create a `.env` file in this directory:

```bash
# Vault
VAULT_DEV_ROOT_TOKEN_ID=dev-root-token

# PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=shared_db

# Grafana
GF_SECURITY_ADMIN_USER=admin
GF_SECURITY_ADMIN_PASSWORD=admin
```

### Network Configuration

All services are on the `shared-network` bridge network. Meta-repositories can connect to this network:

```yaml
# In meta-repo docker-compose.yml
networks:
  default:
    external:
      name: shared-infrastructure_shared-network
```

## 🛠️ Management

### Start Services

```bash
docker-compose up -d
```

### Stop Services

```bash
docker-compose down
```

### Stop and Remove Volumes

```bash
docker-compose down -v
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f vault
```

### Restart a Service

```bash
docker-compose restart vault
```

### Check Service Health

```bash
# All services
docker-compose ps

# Specific service
docker-compose ps vault
```

## 📊 Monitoring

### Prometheus Targets

Check target health: http://localhost:9090/targets

### Grafana Dashboards

Access dashboards: http://localhost:3000/dashboards

### Service Health Checks

All services have health checks configured. Check status:

```bash
docker-compose ps
```

## 🔒 Security Notes

**⚠️ DEVELOPMENT ONLY**

This configuration is for local development only:

- Vault is in dev mode (data not persisted)
- Default passwords are used
- No TLS/SSL encryption
- Services exposed on localhost

**For Production**:
- Use Vault in production mode with proper storage backend
- Use strong passwords and rotate regularly
- Enable TLS/SSL for all services
- Use proper network segmentation
- Implement access controls

## 🐛 Troubleshooting

### Vault Not Starting

```bash
# Check logs
docker-compose logs vault

# Restart Vault
docker-compose restart vault

# Verify Vault status
docker exec -it shared-vault vault status
```

### PostgreSQL Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Test connection
docker exec -it shared-postgres psql -U postgres -c "SELECT 1;"

# Check logs
docker-compose logs postgres
```

### Redis Connection Issues

```bash
# Test Redis
docker exec -it shared-redis redis-cli ping

# Check logs
docker-compose logs redis
```

### Prometheus Not Scraping

```bash
# Check Prometheus config
docker exec -it shared-prometheus cat /etc/prometheus/prometheus.yml

# Reload config
docker-compose restart prometheus

# Check targets
curl http://localhost:9090/api/v1/targets
```

### Grafana Not Accessible

```bash
# Check Grafana logs
docker-compose logs grafana

# Restart Grafana
docker-compose restart grafana

# Verify health
curl http://localhost:3000/api/health
```

## 📚 Resources

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)

## 🤝 Contributing

When adding new shared services:

1. Add service to `docker-compose.yml`
2. Add configuration files if needed
3. Update this README
4. Add health checks
5. Document access and usage

## 📝 Notes

- All data is stored in Docker volumes
- Volumes persist between restarts
- Use `docker-compose down -v` to remove all data
- Backup important data before removing volumes

---

**Part of the meta-repository consolidation project**
