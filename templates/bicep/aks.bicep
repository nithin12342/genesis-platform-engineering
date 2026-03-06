// Azure Bicep Template - AKS Cluster
// Genesis Platform Engineering

@description('Environment name')
param environment string = 'prod'

@description('Azure region')
param location string = resourceGroup().location

@description('AKS cluster name')
param aksName string = 'aks-genesis-${environment}'

@description('DNS prefix')
param dnsPrefix string = 'genesis'

@description('Kubernetes version')
param kubernetesVersion string = '1.28'

@description('Node count')
param nodeCount int = 3

@description('VM size')
param vmSize string = 'Standard_DS2_v2'

var vnetName = 'vnet-genesis-${environment}'
var subnetName = 'snet-aks'
var identityName = 'id-genesis-aks-${environment}'

// Virtual Network
resource vnet 'Microsoft.Network/virtualNetworks@2023-04-01' = {
  name: vnetName
  location: location
  addressSpace: {
    addressPrefixes: ['10.3.0.0/16']
  }
  subnets: [
    {
      name: subnetName
      addressPrefix: '10.3.1.0/24'
      delegations: [
        {
          name: 'Microsoft.ContainerService.managedClusters'
          properties: {
            serviceName: 'Microsoft.ContainerService.managedClusters'
          }
        }
      ]
    }
  ]
}

// User Assigned Identity
resource aksIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
}

// AKS Cluster
resource aks 'Microsoft.ContainerService/managedClusters@2023-10-01' = {
  name: aksName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${aksIdentity.id}': {}
    }
  }
  sku: {
    name: 'Standard'
    tier: 'Standard'
  }
  kubernetesVersion: kubernetesVersion
  dnsPrefix: dnsPrefix
  
  agentPoolProfiles: [
    {
      name: 'system'
      count: nodeCount
      vmSize: vmSize
      type: 'VirtualMachineScaleSets'
      mode: 'System'
      vnetSubnetID: vnet.properties.subnets[0].id
      enableNodePublicIP: false
      osSKU: 'Ubuntu'
    }
    {
      name: 'user'
      count: 2
      vmSize: 'Standard_D4s_v3'
      type: 'VirtualMachineScaleSets'
      mode: 'User'
      vnetSubnetID: vnet.properties.subnets[0].id
      enableNodePublicIP: false
      osSKU: 'Ubuntu'
    }
  ]
  
  networkProfile: {
    networkPlugin: 'azure'
    networkPolicy: 'calico'
    serviceCidr: '10.4.0.0/16'
    dnsServiceIP: '10.4.0.10'
    loadBalancerSku: 'standard'
  }
  
  addonProfiles: {
    azurepolicy: {
      enabled: true
      config: {
        version: 'v2'
      }
    }
    omsagent: {
      enabled: true
      config: {
        logAnalyticsWorkspaceResourceID: '/subscriptions/${subscription().id}/resourceGroups/rg-genesis-${environment}/providers/Microsoft.OperationalInsights/workspaces/law-genesis-${environment}'
      }
    }
    azureKeyvaultSecretsProvider: {
      enabled: true
      config: {}
    }
  }
  
  enableRBAC: true
  
  azureActiveDirectoryProfile: {
    managed: true
    enableAzureRbac: true
  }
  
  workloadIdentityProfile: {
    enabled: true
  }
}

// Role Assignment for Kubelet
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(subscription().id, aksName, 'Network Contributor')
  scope: vnet
  roleDefinitionId: '4d97b98b-1d4f-4787-a291-c51934cd3db3'
  principalId: aks.properties.identityProfile.kubeletidentity.objectId
  principalType: 'ServicePrincipal'
}

output aksName string = aks.name
output aksFqdn string = aks.properties.fqdn
output nodeResourceGroup string = aks.properties.nodeResourceGroup
