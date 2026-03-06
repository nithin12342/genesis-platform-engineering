# Genesis Platform Engineering

Internal Developer Platform (IDP) meta-repository for Dulux Tech.

## Overview

Genesis is an Internal Developer Platform that provides self-service infrastructure provisioning, service scaffolding, GitOps deployment, and developer portal capabilities.

## Features

### Developer Portal
- **Backstage** - Internal developer portal with service catalog, tech docs, and software templates
- **Service Catalog** - Central registry of all services, APIs, and resources
- **Software Templates** - Pre-configured service templates for quick onboarding

### GitOps
- **ArgoCD** - GitOps deployment controller for Kubernetes
- **Application Sets** - Declarative multi-cluster deployments
- **Automated Sync** - Continuous deployment with self-healing

### Self-Service Infrastructure
- **Crossplane** - Cloud control plane for self-service provisioning
- **Database Composition** - Azure SQL, PostgreSQL, MySQL
- **Cache Composition** - Redis, Memcached
- **Storage Composition** - Blob storage, containers
- **Kubernetes Clusters** - AKS provisioning

### Service Scaffolding
- **Go Service** - Go microservice template
- **Python Service** - FastAPI template
- **Node.js Service** - Express template
- **Java Service** - Spring Boot template

## Directory Structure

```
genesis-platform-engineering/
├── .github/
│   └── workflows/
│       └── platform-ci.yml      # CI/CD pipeline
├── configs/
│   ├── backstage-config.yaml    # Backstage configuration
│   ├── argocd-applications.yaml # ArgoCD applications
│   └── crossplane-compositions.yaml # Infrastructure compositions
├── scripts/
│   └── create-app.sh           # Service creation script
├── templates/                   # Service templates
├── tests/
│   └── platform_test.sh       # Test suite
├── context-spec.json           # Project specification
└── harness.json               # Implementation harness
```

## Usage

### Start Backstage Portal

```bash
# Using Docker
docker run -it -p 3000:3000 \
  -v $(pwd)/configs/backstage-config.yaml:/app/backstage-config.yaml \
  backstage:latest
```

### Deploy ArgoCD Applications

```bash
# Install ArgoCD
kubectl apply -f configs/argocd-applications.yaml

# Sync applications
argocd app sync genesis-platform
```

### Create New Service

```bash
# Create Go service
SERVICE_NAME=order-service TEMPLATE=go-service ./scripts/create-app.sh

# Create Python service
SERVICE_NAME=user-service TEMPLATE=python-service ./scripts/create-app.sh

# Create Node.js service
SERVICE_NAME=payment-service TEMPLATE=node-service ./scripts/create-app.sh

# Create Java service
SERVICE_NAME=notification-service TEMPLATE=java-service ./scripts/create-app.sh
```

### Provision Infrastructure

```bash
# Apply Crossplane composition
kubectl apply -f configs/crossplane-compositions.yaml

# Create database claim
kubectl apply -f - <<EOF
apiVersion: genesis.dulux.tech/v1alpha1
kind: Database
metadata:
  name: production-db
spec:
  parameters:
    size: S1
  compositionSelector:
    matchLabels:
      provider: azure
      type: database
EOF
```

## GitHub Actions

The platform CI/CD pipeline runs automatically on:
- Every push to main/develop
- Every pull request
- Manual trigger

Pipeline stages:
1. Validate YAML configs
2. Security scanning (Trivy, Checkov)
3. Test service templates
4. Deploy to ArgoCD

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| GITHUB_TOKEN | GitHub token for repository access |
| ARGOCD_SERVER | ArgoCD server URL |
| ARGOCD_TOKEN | ArgoCD authentication token |
| AZURE_CLIENT_ID | Azure service principal client ID |
| AZURE_CLIENT_SECRET | Azure service principal secret |
| AZURE_TENANT_ID | Azure tenant ID |

### Backstage Configuration

Edit `configs/backstage-config.yaml` to customize:
- Authentication providers
- Catalog locations
- Kubernetes clusters
- ArgoCD integration
- Plugin settings

### ArgoCD Applications

Edit `configs/argocd-applications.yaml` to:
- Add new applications
- Configure sync policies
- Set up application sets

## Templates

### Go Service Template
- REST API with standard library
- Dockerfile with multi-stage build
- Kubernetes deployment
- Helm chart

### Python Service Template
- FastAPI REST API
- Uvicorn ASGI server
- Dockerfile
- Kubernetes deployment

### Node.js Service Template
- Express.js REST API
- NPM scripts
- Dockerfile
- Kubernetes deployment

### Java Service Template
- Spring Boot application
- Maven build
- Dockerfile
- Kubernetes deployment

## Development

### Prerequisites
- Kubernetes cluster
- kubectl
- Helm 3
- Docker (for local testing)
- ArgoCD CLI
- Crossplane CLI

### Local Development

1. Install dependencies:
```bash
# Install ArgoCD CLI
brew install argocd

# Install Crossplane CLI
brew install crossplane
```

2. Configure kubectl:
```bash
kubectl config use-context your-cluster
```

3. Deploy platform:
```bash
kubectl apply -f configs/argocd-applications.yaml
```

4. Verify deployment:
```bash
kubectl get pods -n platform
argocd app list
```

## Compliance

- SOC 2 controls implemented
- ISO 27001 security controls
- GDPR data protection
- HIPAA compliance for healthcare

## Monitoring

### Metrics
- Deployment frequency
- Lead time for changes
- Mean time to recovery (MTTR)
- Change failure rate

### Dashboards
- Platform Health
- Developer Experience
- Cost Overview

## License

Proprietary - Dulux Tech

## Author

Dulux Tech Platform Team

## Version

1.0.0
