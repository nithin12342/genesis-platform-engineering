// Azure Bicep Template - Azure Storage Account
// Genesis Platform Engineering

@description('Environment name')
param environment string = 'prod'

@description('Azure region')
param location string = resourceGroup().location

@description('Storage account name (must be globally unique)')
param storageAccountName string = 'stgenesis${environment}'

@description('SKU name')
param skuName string = 'Standard_LRS'

@description('Kind')
param kind string = 'StorageV2'

@description('Access tier')
param accessTier string = 'Hot'

@description('Enable HTTPS traffic only')
param enableHttpsTrafficOnly bool = true

@description('Allow blob public access')
param allowBlobPublicAccess bool = false

@description('Minimum TLS version')
param minimumTlsVersion string = 'TLS1_2'

@description('Enable versioning')
param enableVersioning bool = true

@description('Enable soft delete')
param enableSoftDelete bool = true

@description('Soft delete retention days')
param softDeleteRetentionDays int = 7

// Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  kind: kind
  sku: {
    name: skuName
  }
  properties: {
    supportsHttpsTrafficOnly: enableHttpsTrafficOnly
    allowBlobPublicAccess: allowBlobPublicAccess
    minimumTlsVersion: minimumTlsVersion
    networkAcls: {
      defaultAction: 'Allow'
    }
    accessTier: accessTier
  }
}

// Blob Services
resource blobServices 'Microsoft.Storage/storageAccounts/blobServices@2023-01-01' = {
  parent: storageAccount
  name: 'default'
  properties: {
    cors: {
      corsRules: [
        {
          allowedOrigins: ['https://genesis-platform.io', 'https://app.genesis-platform.io']
          allowedMethods: ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS']
          allowedHeaders: ['*']
          exposedHeaders: ['*']
          maxAgeInSeconds: 3600
        }
      ]
    }
    deleteRetentionPolicy: {
      enabled: enableSoftDelete
      days: softDeleteRetentionDays
    }
    versioning: {
      enabled: enableVersioning
    }
    changeFeed: {
      enabled: true
    }
  }
}

// Container - Files (Private)
resource filesContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobServices
  name: 'files'
  properties: {
    publicAccess: 'None'
    metadata: {}
  }
}

// Container - Uploads (Private)
resource uploadsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobServices
  name: 'uploads'
  properties: {
    publicAccess: 'None'
    metadata: {}
  }
}

// Container - Exports (Blob)
resource exportsContainer 'Microsoft.Storage/storageAccounts/blobServices/containers@2023-01-01' = {
  parent: blobServices
  name: 'exports'
  properties: {
    publicAccess: 'Blob'
    metadata: {}
  }
}

// File Share
resource fileShare 'Microsoft.Storage/storageAccounts/fileServices/shares@2023-01-01' = {
  parent: storageAccount
  name: 'genesis-files'
  properties: {
    shareQuota: 5120
  }
}

// Queue
resource queue 'Microsoft.Storage/storageAccounts/queueServices/queues@2023-01-01' = {
  parent: storageAccount
  name: 'job-queue'
  properties: {
    metadata: {}
  }
}

output storageAccountName string = storageAccount.name
output storageAccountId string = storageAccount.id
output storageAccountPrimaryEndpoints object = storageAccount.properties.primaryEndpoints
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob
output fileEndpoint string = storageAccount.properties.primaryEndpoints.file
output queueEndpoint string = storageAccount.properties.primaryEndpoints.queue
