param projectResourceName string
param mcpCrimeServerConnectionName string
param targetUrlCrimeMCP string
param crimeMCPServerKey string

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  name: projectResourceName
}

var credentialMcpServer = {
  keys: {
    'x-functions-key': crimeMCPServerKey
  }
}

resource crimeMCPServerConnection 'Microsoft.CognitiveServices/accounts/projects/connections@2025-10-01-preview' = {
  parent: project
  name: mcpCrimeServerConnectionName
  properties: {
    category: 'RemoteTool'
    isSharedToAll: false
    target: targetUrlCrimeMCP
    useWorkspaceManagedIdentity: false
    authType: 'CustomKeys'
    credentials: credentialMcpServer
  }
}

output crimeMCPServerConnectionId string = crimeMCPServerConnection.id
