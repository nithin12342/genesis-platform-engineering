#!/bin/bash
# Genesis Platform Engineering - Service Creation Script
# Creates new services from templates

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }

# Default values
TEMPLATE="${TEMPLATE:-go-service}"
SERVICE_NAME="${SERVICE_NAME:-}"
NAMESPACE="${NAMESPACE:-default}"
OUTPUT_DIR="${OUTPUT_DIR:-./services}"

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
    -t, --template TEMPLATE    Template to use (go-service, python-service, node-service, java-service)
    -n, --name NAME           Service name (required)
    -o, --output DIR          Output directory (default: ./services)
    -h, --help                Show this help message

Examples:
    $0 -t go-service -n order-service
    $0 --template node-service --name user-service --output ./my-services

Templates available:
    go-service       - Go microservice
    python-service   - Python FastAPI service
    node-service     - Node.js Express service
    java-service     - Java Spring Boot service
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--template)
            TEMPLATE="$2"
            shift 2
            ;;
        -n|--name)
            SERVICE_NAME="$2"
            shift 2
            ;;
        -o|--output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            log_warn "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate required parameters
if [ -z "$SERVICE_NAME" ]; then
    log_warn "Service name is required"
    usage
    exit 1
fi

log_info "Creating service: $SERVICE_NAME"
log_info "Template: $TEMPLATE"
log_info "Output: $OUTPUT_DIR/$SERVICE_NAME"

# Create output directory
mkdir -p "$OUTPUT_DIR/$SERVICE_NAME"

# Create service based on template
case "$TEMPLATE" in
    go-service)
        log_info "Creating Go service template..."
        cat > "$OUTPUT_DIR/$SERVICE_NAME/main.go" << 'EOF'
package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "Hello from %s!", "{{.ServiceName}}")
	})

	log.Println("Server starting on :8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatal(err)
	}
}
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/go.mod" << EOF
module github.com/dulux-tech/{{.ServiceName}}

go 1.21
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/Dockerfile" << 'EOF'
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o /service

FROM alpine:latest
RUN apk --no-cache add ca-certificates
COPY --from=builder /service /service
EXPOSE 8080
ENTRYPOINT ["/service"]
EOF
        ;;
    
    python-service)
        log_info "Creating Python service template..."
        cat > "$OUTPUT_DIR/$SERVICE_NAME/main.py" << EOF
from fastapi import FastAPI

app = FastAPI(title="{{.ServiceName}}")

@app.get("/")
def read_root():
    return {"message": "Hello from {{.ServiceName}}!"}
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/requirements.txt" << 'EOF'
fastapi>=0.100.0
uvicorn>=0.23.0
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/Dockerfile" << 'EOF'
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
EOF
        ;;
    
    node-service)
        log_info "Creating Node.js service template..."
        cat > "$OUTPUT_DIR/$SERVICE_NAME/index.js" << EOF
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({ message: 'Hello from {{.ServiceName}}!' });
});

app.listen(8080, () => {
    console.log('Server running on port 8080');
});
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/package.json" << EOF
{
  "name": "{{.ServiceName}}",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js",
    "dev": "nodemon index.js"
  },
  "dependencies": {
    "express": "^4.18.0"
  }
}
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/Dockerfile" << 'EOF'
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 8080
CMD ["node", "index.js"]
EOF
        ;;
    
    java-service)
        log_info "Creating Java service template..."
        cat > "$OUTPUT_DIR/$SERVICE_NAME/pom.xml" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>com.dulux.tech</groupId>
    <artifactId>{{.ServiceName}}</artifactId>
    <version>1.0.0-SNAPSHOT</version>
    <packaging>jar</packaging>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>3.1.0</version>
    </parent>
    
    <properties>
        <java.version>17</java.version>
    </properties>
    
    <dependencies>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
    </dependencies>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
EOF
        cat > "$OUTPUT_DIR/$SERVICE_NAME/src/main/java/com/dulux/tech/Application.java" << EOF
package com.dulux.tech;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
EOF
        ;;
    
    *)
        log_warn "Unknown template: $TEMPLATE"
        exit 1
        ;;
esac

# Create Kubernetes deployment
mkdir -p "$OUTPUT_DIR/$SERVICE_NAME/k8s"
cat > "$OUTPUT_DIR/$SERVICE_NAME/k8s/deployment.yaml" << EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{.ServiceName}}
  namespace: {{.Namespace}}
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {{.ServiceName}}
  template:
    metadata:
      labels:
        app: {{.ServiceName}}
    spec:
      containers:
      - name: {{.ServiceName}}
        image: duluxtech/{{.ServiceName}}:latest
        ports:
        - containerPort: 8080
---
apiVersion: v1
kind: Service
metadata:
  name: {{.ServiceName}}
  namespace: {{.Namespace}}
spec:
  selector:
    app: {{.ServiceName}}
  ports:
  - port: 80
    targetPort: 8080
EOF

# Create Helm chart
mkdir -p "$OUTPUT_DIR/$SERVICE_NAME/helm"
cat > "$OUTPUT_DIR/$SERVICE_NAME/helm/Chart.yaml" << EOF
apiVersion: v2
name: {{.ServiceName}}
description: A Helm chart for {{.ServiceName}}
version: 1.0.0
EOF
cat > "$OUTPUT_DIR/$SERVICE_NAME/helm/values.yaml" << EOF
replicas: 3
image:
  repository: duluxtech/{{.ServiceName}}
  tag: latest
  pullPolicy: IfNotPresent
service:
  port: 80
  targetPort: 8080
EOF

log_info "Service created successfully at: $OUTPUT_DIR/$SERVICE_NAME"
