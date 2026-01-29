param foundryResourceName string
param projectResourceName string
param mcpCrimeServerConnectionName string = 'MCPCrimeServerTool'
param targetUrlCrimeMCP string
param crimeMCPServerKey string

resource foundry 'Microsoft.CognitiveServices/accounts@2025-04-01-preview' existing = {
  name: foundryResourceName
}

resource project 'Microsoft.CognitiveServices/accounts/projects@2025-04-01-preview' existing = {
  parent: foundry
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
    metadata: {
      type: 'custom_MCP'
    }
  }
}

output crimeMCPServerConnectionId string = crimeMCPServerConnection.id
