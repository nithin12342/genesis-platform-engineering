// Azure Bicep Template - Azure SQL Database
// Genesis Platform Engineering

@description('Environment name')
param environment string = 'prod'

@description('Azure region')
param location string = resourceGroup().location

@description('SQL Server name')
param sqlServerName string = 'sql-genesis-${environment}'

@description('Database name')
param databaseName string = 'genesis_platform'

@description('Administrator login')
param administratorLogin string = 'sqladmin'

@description('Administrator password')
@secure()
param administratorPassword string

@description('SQL DTU capacity')
param dtuCapacity int = 50

@description('Database max size in MB')
param maxSizeMb int = 102400

// SQL Server
resource sqlServer 'Microsoft.Sql/servers@2022-11-01' = {
  name: sqlServerName
  location: location
  properties: {
    administratorLogin: administratorLogin
    administratorPassword: administratorPassword
    version: '12.0'
    minimalTlsVersion: '1.2'
    publicNetworkAccess: 'Enabled'
    firewallRules: [
      {
        name: 'AllowAllAzureIPs'
        properties: {
          startIpAddress: '0.0.0.0'
          endIpAddress: '0.0.0.0'
        }
      }
    ]
  }
}

// Database
resource database 'Microsoft.Sql/servers/databases@2022-11-01' = {
  parent: sqlServer
  name: databaseName
  location: location
  sku: {
    name: 'Basic'
    tier: 'Basic'
    capacity: dtuCapacity
  }
  properties: {
    collation: 'SQL_Latin1_General_CP1_CI_AS'
    maxSizeBytes: maxSizeMb * 1024 * 1024
    catalogCollation: 'SQL_Latin1_General_CP1_CI_AS'
    zoneRedundant: false
    readScale: 'Disabled'
    requestedBackupStorageRedundancy: 'Geo'
  }
}

// Threat Detection Policy
resource threatDetection 'Microsoft.Sql/servers/databases/securityAlertPolicies@2022-11-01' = {
  parent: database
  name: 'Default'
  properties: {
    state: 'Enabled'
    disabledAlerts: ''
    emailAddresses: 'security@genesis-platform.io'
    retentionDays: 30
  }
}

// Transparent Data Encryption
resource tde 'Microsoft.Sql/servers/databases/transparentDataEncryption@2022-11-01' = {
  parent: database
  name: 'Current'
  properties: {
    status: 'Enabled'
  }
}

// Audit Settings
resource audit 'Microsoft.Sql/servers/databases/auditingSettings@2022-11-01' = {
  parent: database
  name: 'Default'
  properties: {
    state: 'Enabled'
    auditActionsAndGroups: [
      'SUCCESSFUL_DATABASE_AUTHENTICATION_GROUP'
      'FAILED_DATABASE_AUTHENTICATION_GROUP'
      'BATCH_COMPLETED_GROUP'
    ]
    isStorageSecondaryKeyInUse: false
    queueDelayMs: 1000
  }
}

output sqlServerName string = sqlServer.name
output sqlServerFqdn string = sqlServer.properties.fullyQualifiedDomainName
output databaseName string = database.name
output connectionString string = 'Server=tcp:${sqlServer.properties.fullyQualifiedDomainName},1433;Database=${database.name};User Id=${administratorLogin}@${sqlServerName};Password=${administratorPassword};Encrypt=true;Connection Timeout=30;'
