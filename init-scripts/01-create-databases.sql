-- PostgreSQL Initialization Script
-- Creates databases for each meta-repository

-- nebula-cloud-platform database
CREATE DATABASE nebula_db;
COMMENT ON DATABASE nebula_db IS 'Database for nebula-cloud-platform (cost tracking, usage monitoring)';

-- sentinel-ai-engine database
CREATE DATABASE sentinel_db;
COMMENT ON DATABASE sentinel_db IS 'Database for sentinel-ai-engine (MLflow metadata)';

-- chronos-data-platform database
CREATE DATABASE chronos_db;
COMMENT ON DATABASE chronos_db IS 'Database for chronos-data-platform (Airflow metadata, data warehouse)';

-- titan-microservices-mesh databases (one per service)
CREATE DATABASE titan_orders_db;
COMMENT ON DATABASE titan_orders_db IS 'Database for Order Service';

CREATE DATABASE titan_payments_db;
COMMENT ON DATABASE titan_payments_db IS 'Database for Payment Service';

CREATE DATABASE titan_inventory_db;
COMMENT ON DATABASE titan_inventory_db IS 'Database for Inventory Service';

-- aurora-fullstack-saas database
CREATE DATABASE aurora_db;
COMMENT ON DATABASE aurora_db IS 'Database for aurora-fullstack-saas application';

-- Grant privileges (development only)
GRANT ALL PRIVILEGES ON DATABASE nebula_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE sentinel_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE chronos_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE titan_orders_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE titan_payments_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE titan_inventory_db TO postgres;
GRANT ALL PRIVILEGES ON DATABASE aurora_db TO postgres;

-- Log completion
DO $$
BEGIN
    RAISE NOTICE 'All meta-repository databases created successfully';
END $$;
