#!/bin/bash
# HashiCorp Vault Setup Script
# This script initializes Vault with example secrets for development

set -e

echo "🔐 Setting up HashiCorp Vault..."

# Wait for Vault to be ready
echo "Waiting for Vault to start..."
sleep 5

# Set Vault address and token
export VAULT_ADDR='http://localhost:8200'
export VAULT_TOKEN='dev-root-token'

# Check Vault status
echo "Checking Vault status..."
vault status

# Enable KV secrets engine (v2)
echo "Enabling KV secrets engine..."
vault secrets enable -version=2 -path=secret kv || echo "KV engine already enabled"

# Create example secrets for each meta-repository
echo "Creating example secrets..."

# nebula-cloud-platform secrets
vault kv put secret/nebula/gcp \
  project_id="my-gcp-project" \
  region="us-central1" \
  credentials="<GCP_SERVICE_ACCOUNT_JSON>"

vault kv put secret/nebula/database \
  host="localhost" \
  port="5432" \
  username="postgres" \
  password="postgres" \
  database="nebula_db"

# sentinel-ai-engine secrets
vault kv put secret/sentinel/mlflow \
  tracking_uri="http://localhost:5000" \
  artifact_uri="s3://mlflow-artifacts"

vault kv put secret/sentinel/model \
  api_key="<MODEL_API_KEY>" \
  model_path="/models/yolov8"

# chronos-data-platform secrets
vault kv put secret/chronos/airflow \
  fernet_key="<AIRFLOW_FERNET_KEY>" \
  secret_key="<AIRFLOW_SECRET_KEY>"

vault kv put secret/chronos/database \
  host="localhost" \
  port="5432" \
  username="postgres" \
  password="postgres" \
  database="chronos_db"

# titan-microservices-mesh secrets
vault kv put secret/titan/kafka \
  bootstrap_servers="localhost:9092" \
  security_protocol="PLAINTEXT"

vault kv put secret/titan/stripe \
  api_key="sk_test_<STRIPE_TEST_KEY>" \
  webhook_secret="whsec_<WEBHOOK_SECRET>"

# obsidian-devsecops-platform secrets
vault kv put secret/obsidian/opa \
  policy_bundle_url="http://localhost:8181"

# aurora-fullstack-saas secrets
vault kv put secret/aurora/nextauth \
  secret="<NEXTAUTH_SECRET>" \
  url="http://localhost:3000"

vault kv put secret/aurora/database \
  host="localhost" \
  port="5432" \
  username="postgres" \
  password="postgres" \
  database="aurora_db"

vault kv put secret/aurora/jwt \
  secret_key="<JWT_SECRET_KEY>" \
  algorithm="HS256" \
  expiration_minutes="30"

echo "✅ Vault setup complete!"
echo ""
echo "Vault UI: http://localhost:8200"
echo "Root Token: dev-root-token"
echo ""
echo "Example: Read a secret"
echo "vault kv get secret/nebula/database"
echo ""
echo "Example: List all secrets"
echo "vault kv list secret/"
