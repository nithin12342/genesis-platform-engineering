// Azure Bicep Template - Key Vault
// Genesis Platform Engineering

@description('Environment name')
param environment string = 'prod'

@description('Azure region')
param location string = resourceGroup().location

@description('Key Vault name (must be globally unique)')
param keyVaultName string = 'kv-genesis-${environment}'

@description('Tenant ID')
param tenantId string = subscription().tenantId

@description('SKU name')
param skuName string = 'standard'

@description('Soft delete retention days')
param softDeleteRetentionDays int = 90

@description('Enable purge protection')
param enablePurgeProtection bool = false

@description('Enable RBAC authorization')
param enableRbacAuthorization bool = true

var networkAcls = {
  defaultAction: 'Allow'
  bypass: 'AzureServices'
}

// Key Vault
resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: keyVaultName
  location: location
  properties: {
    tenantId: tenantId
    sku: {
      family: 'A'
      name: skuName
    }
    enableRbacAuthorization: enableRbacAuthorization
    enableSoftDelete: true
    softDeleteRetentionInDays: softDeleteRetentionDays
    enablePurgeProtection: enablePurgeProtection
    networkAcls: networkAcls
    
    secrets: {
      #disable-next-line BCP037
      enabledForDeployment: true
      #disable-next-line BCP037
      enabledForDiskEncryption: true
      #disable-next-line BCP037
      enabledForTemplateDeployment: true
    }
    
    enableAzureVirtualNetworkAccess: false
  }
}

// Secret - Database Connection String
resource dbConnectionSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'DbConnectionString'
  properties: {
    value: 'Server=tcp:sql-genesis-${environment}.database.windows.net,1433;Database=genesis_platform;User Id=admin;Password=ChangeMe123!;Encrypt=true;Connection Timeout=30;'
    contentType: 'string'
    attributes: {
      enabled: true
    }
  }
}

// Secret - Azure Storage Connection
resource storageConnectionSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'AzureStorageConnection'
  properties: {
    value: 'DefaultEndpointsProtocol=https;AccountName=stgenesis${environment};AccountKey=ChangeMe123!;EndpointSuffix=core.windows.net'
    contentType: 'string'
    attributes: {
      enabled: true
    }
  }
}

// Secret - Redis Cache Connection
resource redisConnectionSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'RedisConnection'
  properties: {
    value: 'redis.redis.cache.windows.net:6380,password=ChangeMe123!,ssl=True,abortConnect=False'
    contentType: 'string'
    attributes: {
      enabled: true
    }
  }
}

// Secret - SendGrid API Key
resource sendgridApiKeySecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'SendGridApiKey'
  properties: {
    value: 'SG.ChangeMe123!ChangeMe123!'
    contentType: 'string'
    attributes: {
      enabled: true
    }
  }
}

// Secret - JWT Secret
resource jwtSecret 'Microsoft.KeyVault/vaults/secrets@2023-02-01' = {
  parent: keyVault
  name: 'JwtSecret'
  properties: {
    value: 'ChangeMe123!JwtSecretKeyForGenesisPlatform2024!'
    contentType: 'string'
    attributes: {
      enabled: true
    }
  }
}

output keyVaultName string = keyVault.name
output keyVaultUri string = keyVault.properties.vaultUri
