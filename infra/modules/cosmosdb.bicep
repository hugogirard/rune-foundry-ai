param location string
param cosmosDBResourceName string

resource cosmosDB 'Microsoft.DocumentDB/databaseAccounts@2025-05-01-preview' = {
  name: cosmosDBResourceName
  location: location
  tags: {
    defaultExperience: 'Core (SQL)'
    'hidden-workload-type': 'Development/Testing'
    'hidden-cosmos-mmspecial': ''
    SecurityControl: 'Ignore'
    Workload: 'Threads'
  }
  kind: 'GlobalDocumentDB'
  properties: {
    publicNetworkAccess: 'Enabled'
    enableAutomaticFailover: false
    enableMultipleWriteLocations: false
    isVirtualNetworkFilterEnabled: false
    virtualNetworkRules: []
    disableKeyBasedMetadataWriteAccess: false
    enableFreeTier: false
    enableAnalyticalStorage: false
    analyticalStorageConfiguration: {
      schemaType: 'WellDefined'
    }
    databaseAccountOfferType: 'Standard'
    enableMaterializedViews: false
    capacityMode: 'Provisioned'
    defaultIdentity: 'FirstPartyIdentity'
    networkAclBypass: 'None'
    disableLocalAuth: false
    enablePartitionMerge: false
    enablePerRegionPerPartitionAutoscale: true
    enableBurstCapacity: false
    enablePriorityBasedExecution: false
    //defaultPriorityLevel: 'High'
    minimalTlsVersion: 'Tls12'
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
      maxIntervalInSeconds: 5
      maxStalenessPrefix: 100
    }
    locations: [
      {
        locationName: location
        failoverPriority: 0
        isZoneRedundant: false
      }
    ]
    cors: []
    capabilities: [
      {
        name: 'EnableNoSQLVectorSearch'
      }
    ]
    ipRules: []
    backupPolicy: {
      type: 'Periodic'
      periodicModeProperties: {
        backupIntervalInMinutes: 240
        backupRetentionIntervalInHours: 8
        backupStorageRedundancy: 'Geo'
      }
    }
    networkAclBypassResourceIds: []
    diagnosticLogSettings: {
      enableFullTextQuery: 'None'
    }
    capacity: {
      totalThroughputLimit: 1000
    }
  }
}

resource dbChat 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2025-11-01-preview' = {
  parent: cosmosDB
  name: 'conversation'
  properties: {
    resource: {
      id: 'conversation'
    }
  }
}

resource dbSkyrim 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases@2025-11-01-preview' = {
  parent: cosmosDB
  name: 'skyrim'
  properties: {
    resource: {
      id: 'skyrim'
    }
  }
}

resource container 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-11-01-preview' = {
  parent: dbSkyrim
  name: 'crime'
  properties: {
    resource: {
      id: 'crime'
      partitionKey: {
        paths: [
          '/crimeType'
        ]
        kind: 'Hash'
      }
      vectorEmbeddingPolicy: {
        vectorEmbeddings: [
          {
            dataType: 'float32'
            dimensions: 1536
            distanceFunction: 'cosine'
            path: '/descriptionVector'
          }
        ]
      }
      fullTextPolicy: {
        defaultLanguage: 'en-US'
        fullTextPaths: [
          {
            language: 'en-US'
            path: '/crimeName'
          }
          {
            language: 'en-US'
            path: '/description'
          }
        ]
      }
      indexingPolicy: {
        fullTextIndexes: [
          {
            path: '/description'
          }
          {
            path: '/crimeName'
          }
        ]
      }
    }
  }
}

resource containerChat 'Microsoft.DocumentDB/databaseAccounts/sqlDatabases/containers@2025-11-01-preview' = {
  parent: dbChat
  name: 'thread'
  properties: {
    resource: {
      id: 'thread'
      partitionKey: {
        paths: [
          '/userId'
        ]
        kind: 'Hash'
      }
    }
  }
}

output cosmosDbAccountName string = cosmosDB.name
output skyrimDatabaseName string = dbSkyrim.name
output skyrimContaineName string = dbSkyrim.name
