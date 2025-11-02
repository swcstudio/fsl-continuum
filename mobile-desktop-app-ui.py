#!/usr/bin/env python3
"""
FSL Continuum - Mobile & Desktop App UI Components

React Native mobile app and Electron desktop app UI components
for Copilot Task Agent with prompt uplift and terminal-like execution.

This provides the actual mobile/desktop interface that connects to the
Copilot Task Agent API for instant prompt-to-schema conversion
and terminal-like execution speed.
"""

import React from 'react';
import { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  FlatList,
  ScrollView,
  Alert,
  ActivityIndicator,
  StyleSheet,
  Platform,
  KeyboardAvoidingView,
  SafeAreaView
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import Icon from 'react-native-vector-icons/MaterialIcons';

// API Configuration
const API_BASE_URL = Platform.OS === 'web' ? 
  'http://localhost:8000' : 'https://api.fsl-continuum.com';

// Mobile App Components
const MobileCopilotAgentApp = () => {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentSchema, setCurrentSchema] = useState(null);
  const [executionResult, setExecutionResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [quickActions, setQuickActions] = useState([
    { id: 1, title: 'Analyze Repository', icon: 'search', prompt: 'Analyze this repository structure and suggest improvements' },
    { id: 2, title: 'Create Tech Stack', icon: 'build', prompt: 'Create modern tech stack for web application' },
    { id: 3, title: 'Add Features', icon: 'add-circle', prompt: 'Add authentication and user management features' },
    { id: 4, title: 'Upgrade Architecture', icon: 'architecture', prompt: 'Upgrade architecture to microservices with event-driven design' }
  ]);

  // Load history on component mount
  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/request-history?limit=20`);
      const data = await response.json();
      if (data.success) {
        setHistory(data.history);
      }
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const upliftPrompt = async (naturalInput) => {
    if (!naturalInput.trim()) return;
    
    setIsProcessing(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/prompt-uplift`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          natural_input: naturalInput,
          target_platform: 'mobile',
          execution_preference: 'terminal_like',
          ai_system_preference: 'auto_detect'
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setCurrentSchema(result.openspec_schema);
        
        // Auto-execute if validation is good
        if (result.validation_status === 'valid') {
          await executeTask(result.openspec_schema);
        } else {
          Alert.alert('Validation Issue', 'Please review the generated schema before execution.');
        }
      } else {
        Alert.alert('Error', result.message || 'Failed to uplift prompt');
      }
    } catch (error) {
      console.error('Prompt uplift failed:', error);
      Alert.alert('Error', 'Failed to process your request. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  const executeTask = async (schema) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/execute-task`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          openspec_schema: schema,
          execution_mode: 'terminal_like'
        })
      });

      const result = await response.json();
      
      if (result.status === 'completed') {
        setExecutionResult(result.result);
        await loadHistory(); // Refresh history
      } else {
        Alert.alert('Execution Error', 'Task execution failed. Please check the schema.');
      }
    } catch (error) {
      console.error('Task execution failed:', error);
      Alert.alert('Error', 'Failed to execute task. Please try again.');
    }
  };

  const handleQuickAction = (action) => {
    setPrompt(action.prompt);
    upliftPrompt(action.prompt);
  };

  const handleVoiceInput = () => {
    // Voice input implementation would go here
    Alert.alert('Voice Input', 'Voice input feature coming soon!');
  };

  const renderQuickAction = ({ item }) => (
    <TouchableOpacity 
      style={styles.quickActionItem}
      onPress={() => handleQuickAction(item)}
    >
      <Icon name={item.icon} size={24} color="#007AFF" />
      <Text style={styles.quickActionText}>{item.title}</Text>
    </TouchableOpacity>
  );

  const renderHistoryItem = ({ item }) => (
    <View style={styles.historyItem}>
      <Text style={styles.historyTitle}>{item.title}</Text>
      <Text style={styles.historyType}>{item.spec_type}</Text>
      <Text style={styles.historyTime}>
        {new Date(item.timestamp * 1000).toLocaleDateString()}
      </Text>
    </View>
  );

  if (isProcessing) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#007AFF" />
        <Text style={styles.loadingText}>Processing your request...</Text>
        <Text style={styles.loadingSubtext}>Uplifting to OpenSpec schema...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView style={styles.keyboardAvoid} behavior="padding">
        <ScrollView style={styles.scrollView}>
          {/* Header */}
          <View style={styles.header}>
            <Text style={styles.headerTitle}>Copilot Task Agent</Text>
            <Text style={styles.headerSubtitle}>Prompt → Schema → Execution (Terminal Speed)</Text>
          </View>

          {/* Quick Actions */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Quick Actions</Text>
            <FlatList
              data={quickActions}
              renderItem={renderQuickAction}
              keyExtractor={(item) => item.id.toString()}
              numColumns={2}
              scrollEnabled={false}
              contentContainerStyle={styles.quickActionsContainer}
            />
          </View>

          {/* Prompt Input */}
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Describe Your Task</Text>
            <View style={styles.inputContainer}>
              <TextInput
                style={styles.textInput}
                placeholder="Enter natural language description..."
                value={prompt}
                onChangeText={setPrompt}
                multiline
                numberOfLines={4}
                textAlignVertical="top"
              />
              <TouchableOpacity 
                style={styles.voiceButton}
                onPress={handleVoiceInput}
              >
                <Icon name="mic" size={20} color="#666" />
              </TouchableOpacity>
            </View>
            <TouchableOpacity 
              style={[styles.actionButton, !prompt.trim() && styles.actionButtonDisabled]}
              onPress={() => upliftPrompt(prompt)}
              disabled={!prompt.trim()}
            >
              <Text style={styles.actionButtonText}>Create & Execute</Text>
            </TouchableOpacity>
          </View>

          {/* Current Schema */}
          {currentSchema && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Generated OpenSpec Schema</Text>
              <View style={styles.schemaContainer}>
                <Text style={styles.schemaTitle}>{currentSchema.title}</Text>
                <Text style={styles.schemaType}>{currentSchema.spec_type}</Text>
                <Text style={styles.schemaDescription}>{currentSchema.description}</Text>
                
                {currentSchema.requirements.length > 0 && (
                  <View style={styles.requirementsContainer}>
                    <Text style={styles.requirementsTitle}>Requirements:</Text>
                    {currentSchema.requirements.map((req, index) => (
                      <Text key={index} style={styles.requirementItem}>• {req}</Text>
                    ))}
                  </View>
                )}
                
                <View style={styles.validationContainer}>
                  <Text style={[
                    styles.validationText,
                    { color: currentSchema.validation_status === 'valid' ? '#28a745' : '#dc3545' }
                  ]}>
                    Status: {currentSchema.validation_status.toUpperCase()}
                  </Text>
                </View>
              </View>
            </View>
          )}

          {/* Execution Result */}
          {executionResult && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Execution Result</Text>
              <View style={styles.resultContainer}>
                <Text style={[
                  styles.resultStatus,
                  { color: executionResult.execution_success ? '#28a745' : '#dc3545' }
                ]}>
                  {executionResult.execution_success ? '✅ SUCCESS' : '❌ FAILED'}
                </Text>
                
                {executionResult.message && (
                  <Text style={styles.resultMessage}>{executionResult.message}</Text>
                )}
                
                {executionResult.generated_files && executionResult.generated_files.length > 0 && (
                  <View style={styles.filesContainer}>
                    <Text style={styles.filesTitle}>Generated Files:</Text>
                    {executionResult.generated_files.map((file, index) => (
                      <Text key={index} style={styles.fileName}>• {file}</Text>
                    ))}
                  </View>
                )}
              </View>
            </View>
          )}

          {/* Recent History */}
          {history.length > 0 && (
            <View style={styles.section}>
              <Text style={styles.sectionTitle}>Recent History</Text>
              <FlatList
                data={history}
                renderItem={renderHistoryItem}
                keyExtractor={(item, index) => index.toString()}
                scrollEnabled={true}
                style={styles.historyList}
              />
            </View>
          )}
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  keyboardAvoid: {
    flex: 1,
  },
  scrollView: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginTop: 10,
  },
  loadingSubtext: {
    fontSize: 14,
    color: '#666',
    marginTop: 5,
  },
  header: {
    backgroundColor: '#fff',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e9ecef',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
  },
  section: {
    backgroundColor: '#fff',
    margin: 15,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#333',
    marginBottom: 15,
  },
  quickActionsContainer: {
    paddingBottom: 10,
  },
  quickActionItem: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#f8f9fa',
    padding: 15,
    margin: 5,
    borderRadius: 8,
    borderWidth: 1,
    borderColor: '#e9ecef',
  },
  quickActionText: {
    fontSize: 14,
    fontWeight: '500',
    color: '#333',
    marginLeft: 10,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    backgroundColor: '#fff',
  },
  textInput: {
    flex: 1,
    fontSize: 16,
    padding: 15,
    minHeight: 80,
    color: '#333',
  },
  voiceButton: {
    padding: 15,
    justifyContent: 'center',
  },
  actionButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 8,
    alignItems: 'center',
    marginTop: 10,
  },
  actionButtonDisabled: {
    backgroundColor: '#ccc',
  },
  actionButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: '600',
  },
  schemaContainer: {
    backgroundColor: '#f8f9fa',
    padding: 15,
    borderRadius: 8,
    borderLeftWidth: 4,
    borderLeftColor: '#007AFF',
  },
  schemaTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  schemaType: {
    fontSize: 14,
    color: '#007AFF',
    backgroundColor: '#e7f3ff',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    alignSelf: 'flex-start',
    marginBottom: 10,
  },
  schemaDescription: {
    fontSize: 14,
    color: '#666',
    lineHeight: 20,
    marginBottom: 15,
  },
  requirementsContainer: {
    marginTop: 10,
  },
  requirementsTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  requirementItem: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
    paddingLeft: 10,
  },
  validationContainer: {
    marginTop: 10,
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: '#e9ecef',
  },
  validationText: {
    fontSize: 14,
    fontWeight: '600',
  },
  resultContainer: {
    padding: 15,
    backgroundColor: '#f8f9fa',
    borderRadius: 8,
  },
  resultStatus: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 10,
  },
  resultMessage: {
    fontSize: 14,
    color: '#666',
    marginBottom: 15,
  },
  filesContainer: {
    marginTop: 10,
  },
  filesTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 8,
  },
  fileName: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
    paddingLeft: 10,
  },
  historyItem: {
    padding: 15,
    backgroundColor: '#f8f9fa',
    marginBottom: 10,
    borderRadius: 8,
    borderLeftWidth: 3,
    borderLeftColor: '#007AFF',
  },
  historyTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#333',
    marginBottom: 5,
  },
  historyType: {
    fontSize: 12,
    color: '#007AFF',
    backgroundColor: '#e7f3ff',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 3,
    alignSelf: 'flex-start',
    marginBottom: 5,
  },
  historyTime: {
    fontSize: 12,
    color: '#666',
  },
  historyList: {
    maxHeight: 200,
  },
});

export default MobileCopilotAgentApp;

// Desktop App UI Components (Electron)
const { 
  BrowserWindow, 
  app, 
  ipcMain, 
  Menu, 
  MenuItem 
} = require('electron');
const path = require('path');

const DesktopCopilotAgentApp = () => {
  const [prompt, setPrompt] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [currentSchema, setCurrentSchema] = useState(null);
  const [executionResult, setExecutionResult] = useState(null);
  const [selectedAI, setSelectedAI] = useState('auto_detect');
  const [executionMode, setExecutionMode] = useState('terminal_like');
  const [history, setHistory] = useState([]);

  // Desktop-specific features
  const handleFileDrop = useCallback((event) => {
    event.preventDefault();
    const files = Array.from(event.dataTransfer.files);
    
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        // Process dropped file content
        processDroppedFile(file.name, content);
      };
      reader.readAsText(file);
    });
  }, []);

  const handleKeyboardShortcut = useCallback((event) => {
    // Ctrl/Cmd + Enter to execute
    if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
      if (prompt.trim()) {
        upliftPrompt(prompt);
      }
    }
    // Ctrl/Cmd + K for quick actions
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
      event.preventDefault();
      // Open quick actions modal
    }
  }, [prompt]);

  const processDroppedFile = (filename, content) => {
    try {
      // Try to parse as JSON/OpenSpec
      const data = JSON.parse(content);
      if (data.spec_type || data.requirements) {
        setCurrentSchema(data);
        Alert.success('OpenSpec file loaded successfully');
      } else {
        // Treat as natural language prompt
        setPrompt(content);
        Alert.info('File content loaded as prompt');
      }
    } catch (error) {
      // Treat as natural language prompt
      setPrompt(content);
      Alert.info('File content loaded as prompt');
    }
  };

  // Quick actions for desktop
  const desktopQuickActions = [
    { 
      id: 1, 
      title: 'Analyze Repository', 
      shortcut: 'Ctrl+Shift+A',
      icon: '🔍',
      prompt: 'Analyze this repository structure and suggest improvements' 
    },
    { 
      id: 2, 
      title: 'Create Tech Stack', 
      shortcut: 'Ctrl+Shift+T',
      icon: '🏗️',
      prompt: 'Create modern tech stack for web application with React, Node.js, PostgreSQL' 
    },
    { 
      id: 3, 
      title: 'Add Features', 
      shortcut: 'Ctrl+Shift+F',
      icon: '➕',
      prompt: 'Add authentication, authorization, and user management features with JWT tokens' 
    },
    { 
      id: 4, 
      title: 'Upgrade Architecture', 
      shortcut: 'Ctrl+Shift+U',
      icon: '🔄',
      prompt: 'Upgrade monolith architecture to microservices with event-driven design and API gateway' 
    },
    { 
      id: 5, 
      title: 'API Design', 
      shortcut: 'Ctrl+Shift+P',
      icon: '🌐',
      prompt: 'Design RESTful API with GraphQL endpoint, rate limiting, and comprehensive documentation' 
    }
  ];

  // API calls (same as mobile but with desktop-specific features)
  const upliftPrompt = async (naturalInput) => {
    if (!naturalInput.trim()) return;
    
    setIsProcessing(true);
    
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/prompt-uplift`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          natural_input: naturalInput,
          target_platform: 'desktop',
          execution_preference: executionMode,
          ai_system_preference: selectedAI
        })
      });

      const result = await response.json();
      
      if (result.success) {
        setCurrentSchema(result.openspec_schema);
        
        // Auto-execute for desktop (more powerful)
        if (result.validation_status === 'valid') {
          await executeTask(result.openspec_schema);
        }
      } else {
        Alert.error('Validation Issue', 'Please review the generated schema before execution.');
      }
    } catch (error) {
      console.error('Prompt uplift failed:', error);
      Alert.error('Error', 'Failed to process your request. Please try again.');
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="desktop-app" onDrop={handleFileDrop} onDragOver={(e) => e.preventDefault()}>
      <header className="app-header">
        <h1>Copilot Task Agent - Desktop</h1>
        <div className="header-controls">
          <select 
            value={selectedAI} 
            onChange={(e) => setSelectedAI(e.target.value)}
            className="ai-selector"
          >
            <option value="auto_detect">Auto Detect</option>
            <option value="github_copilot_cli">GitHub Copilot CLI</option>
            <option value="droid_advanced">Droid Advanced</option>
            <option value="unified_orchestrator">Unified Orchestrator</option>
          </select>
          
          <select 
            value={executionMode} 
            onChange={(e) => setExecutionMode(e.target.value)}
            className="mode-selector"
          >
            <option value="terminal_like">Terminal Like</option>
            <option value="fast_execution">Fast Execution</option>
            <option value="bulk_operation">Bulk Operation</option>
          </select>
        </div>
      </header>

      <main className="app-main">
        <section className="quick-actions-section">
          <h2>Quick Actions</h2>
          <div className="quick-actions-grid">
            {desktopQuickActions.map(action => (
              <button 
                key={action.id}
                className="quick-action-button"
                onClick={() => {
                  setPrompt(action.prompt);
                  upliftPrompt(action.prompt);
                }}
                title={action.shortcut}
              >
                <span className="action-icon">{action.icon}</span>
                <span className="action-title">{action.title}</span>
                <span className="action-shortcut">{action.shortcut}</span>
              </button>
            ))}
          </div>
        </section>

        <section className="prompt-section">
          <h2>Natural Language Prompt</h2>
          <div className="prompt-container">
            <textarea
              className="prompt-textarea"
              placeholder="Enter your task description in natural language..."
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              onKeyDown={handleKeyboardShortcut}
              rows={6}
            />
            <div className="prompt-controls">
              <button className="voice-input-btn" title="Voice Input">
                🎤
              </button>
              <button 
                className="execute-btn" 
                onClick={() => upliftPrompt(prompt)}
                disabled={!prompt.trim() || isProcessing}
              >
                {isProcessing ? '⏳ Processing...' : '🚀 Create & Execute'}
              </button>
            </div>
          </div>
          
          <div className="drop-zone" onDrop={handleFileDrop} onDragOver={(e) => e.preventDefault()}>
            <p>📁 Drop OpenSpec files or prompt text here</p>
            <p className="drop-zone-hint">Or drag files from your file explorer</p>
          </div>
        </section>

        <section className="schema-section" style={{ display: currentSchema ? 'block' : 'none' }}>
          <h2>Generated OpenSpec Schema</h2>
          <div className="schema-viewer">
            <div className="schema-header">
              <h3>{currentSchema?.title}</h3>
              <span className={`schema-type ${currentSchema?.spec_type}`}>
                {currentSchema?.spec_type}
              </span>
            </div>
            <p className="schema-description">{currentSchema?.description}</p>
            
            {currentSchema?.requirements && currentSchema.requirements.length > 0 && (
              <div className="requirements-section">
                <h4>Requirements</h4>
                <ul>
                  {currentSchema.requirements.map((req, index) => (
                    <li key={index}>{req}</li>
                  ))}
                </ul>
              </div>
            )}
            
            {currentSchema?.execution_plan && currentSchema.execution_plan.length > 0 && (
              <div className="execution-plan-section">
                <h4>Execution Plan</h4>
                <ol>
                  {currentSchema.execution_plan.map((step, index) => (
                    <li key={index}>
                      <strong>{step.action}</strong>: {step.description}
                    </li>
                  ))}
                </ol>
              </div>
            )}
            
            <div className="validation-section">
              <span className={`validation-status ${currentSchema?.validation_status}`}>
                Status: {currentSchema?.validation_status?.toUpperCase()}
              </span>
            </div>
          </div>
        </section>

        <section className="result-section" style={{ display: executionResult ? 'block' : 'none' }}>
          <h2>Execution Result</h2>
          <div className={`result-viewer ${executionResult?.execution_success ? 'success' : 'error'}`}>
            <div className="result-status">
              {executionResult?.execution_success ? '✅ EXECUTION SUCCESSFUL' : '❌ EXECUTION FAILED'}
            </div>
            
            {executionResult?.message && (
              <p className="result-message">{executionResult.message}</p>
            )}
            
            {executionResult?.generated_files && executionResult.generated_files.length > 0 && (
              <div className="generated-files">
                <h4>Generated Files:</h4>
                <ul>
                  {executionResult.generated_files.map((file, index) => (
                    <li key={index}>
                      <span className="file-icon">📄</span>
                      {file}
                    </li>
                  ))}
                </ul>
              </div>
            )}
            
            {executionResult?.tech_stack && (
              <div className="tech-stack-result">
                <h4>Generated Tech Stack:</h4>
                <div className="tech-stack-details">
                  {Object.entries(executionResult.tech_stack).map(([key, value]) => (
                    <div key={key} className="tech-item">
                      <strong>{key}:</strong> {value}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <div className="status-bar">
          <span className="status-indicator">🟢 Connected to FSL Continuum</span>
          <span className="execution-mode">Mode: {executionMode}</span>
          <span className="ai-system">AI: {selectedAI}</span>
        </div>
      </footer>
    </div>
  );
};

// CSS for Desktop App
const desktopAppCSS = `
.desktop-app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background: #f8f9fa;
}

.app-header {
  background: #fff;
  padding: 15px 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.app-header h1 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

.header-controls {
  display: flex;
  gap: 15px;
}

.ai-selector, .mode-selector {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  background: #fff;
  font-size: 14px;
}

.app-main {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}

.quick-actions-section h2 {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 15px;
  margin-bottom: 30px;
}

.quick-action-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background: #fff;
  border: 1px solid #e9ecef;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.quick-action-button:hover {
  border-color: #007AFF;
  box-shadow: 0 2px 8px rgba(0,122,255,0.1);
}

.action-icon {
  font-size: 24px;
  margin-bottom: 10px;
}

.action-title {
  font-weight: 600;
  color: #333;
  margin-bottom: 5px;
  text-align: center;
}

.action-shortcut {
  font-size: 11px;
  color: #666;
  background: #f1f3f4;
  padding: 2px 6px;
  border-radius: 3px;
}

.prompt-section h2 {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.prompt-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e9ecef;
  margin-bottom: 30px;
}

.prompt-textarea {
  width: 100%;
  border: none;
  outline: none;
  resize: vertical;
  font-size: 16px;
  line-height: 1.5;
  font-family: inherit;
}

.prompt-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
}

.voice-input-btn {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  padding: 8px;
}

.execute-btn {
  background: #007AFF;
  color: #fff;
  border: none;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;
}

.execute-btn:hover:not(:disabled) {
  background: #0056b3;
}

.execute-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

.drop-zone {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  margin-top: 15px;
  background: #f8f9fa;
}

.drop-zone p {
  margin: 5px 0;
  color: #666;
}

.drop-zone-hint {
  font-size: 14px;
  color: #999;
}

.schema-section, .result-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  border: 1px solid #e9ecef;
  margin-bottom: 20px;
}

.schema-viewer, .result-viewer {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  border-left: 4px solid #007AFF;
}

.schema-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.schema-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.schema-type {
  background: #e7f3ff;
  color: #007AFF;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 500;
}

.schema-description {
  margin: 15px 0;
  line-height: 1.6;
  color: #666;
}

.requirements-section, .execution-plan-section {
  margin: 20px 0;
}

.requirements-section h4, .execution-plan-section h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.requirements-section ul, .execution-plan-section ol {
  margin: 0;
  padding-left: 20px;
}

.requirements-section li, .execution-plan-section li {
  margin: 5px 0;
  color: #666;
}

.validation-section {
  margin-top: 20px;
  padding-top: 15px;
  border-top: 1px solid #e9ecef;
}

.validation-status.valid {
  color: #28a745;
  font-weight: 600;
}

.validation-status.invalid, .validation-status.warning {
  color: #dc3545;
  font-weight: 600;
}

.result-viewer.success {
  border-left-color: #28a745;
}

.result-viewer.error {
  border-left-color: #dc3545;
}

.result-status {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 15px;
}

.result-message {
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

.generated-files h4, .tech-stack-result h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.generated-files ul, .tech-stack-details {
  background: #fff;
  border-radius: 6px;
  padding: 15px;
  margin-top: 10px;
}

.generated-files li {
  display: flex;
  align-items: center;
  padding: 5px 0;
  color: #666;
}

.file-icon {
  margin-right: 10px;
}

.tech-stack-details {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.tech-item {
  padding: 8px 0;
  border-bottom: 1px solid #f1f3f4;
}

.app-footer {
  background: #fff;
  border-top: 1px solid #e9ecef;
  padding: 10px 20px;
}

.status-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #666;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 5px;
}
`;

// Electron main process setup
const createWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 1400,
    height: 900,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  // Load the app
  mainWindow.loadFile(path.join(__dirname, 'desktop-app.html'));

  // Create menu
  const menu = new Menu();
  menu.append(new MenuItem({ label: 'File', submenu: [
    new MenuItem({ label: 'New Task', accelerator: 'CmdOrCtrl+N', click: () => {
      mainWindow.webContents.send('new-task');
    }}),
    new MenuItem({ label: 'Open OpenSpec', accelerator: 'CmdOrCtrl+O', click: () => {
      mainWindow.webContents.send('open-openspec');
    }}),
    new MenuItem({ label: 'Save Result', accelerator: 'CmdOrCtrl+S', click: () => {
      mainWindow.webContents.send('save-result');
    }}),
  ]}));
  
  menu.append(new MenuItem({ label: 'Edit', submenu: [
    new MenuItem({ label: 'Copy', accelerator: 'CmdOrCtrl+C', role: 'copy' }),
    new MenuItem({ label: 'Paste', accelerator: 'CmdOrCtrl+V', role: 'paste' }),
  ]}));
  
  menu.append(new MenuItem({ label: 'View', submenu: [
    new MenuItem({ label: 'Toggle Fullscreen', accelerator: 'F11', role: 'togglefullscreen' }),
    new MenuItem({ label: 'Developer Tools', accelerator: 'F12', role: 'toggleDevTools' }),
  ]}));
  
  Menu.setApplicationMenu(menu);

  return mainWindow;
};

app.whenReady().then(() => {
  const window = createWindow();
  
  // IPC handlers
  ipcMain.handle('new-task', () => {
    window.webContents.send('clear-prompt');
  });
  
  ipcMain.handle('open-openspec', async () => {
    const { dialog } = require('electron');
    const result = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [
        { name: 'OpenSpec Files', extensions: ['json', 'spec'] }
      ]
    });
    
    if (!result.canceled && result.filePaths.length > 0) {
      window.webContents.send('load-openspec', result.filePaths[0]);
    }
  });
  
  ipcMain.handle('save-result', async () => {
    const { dialog } = require('electron');
    const result = await dialog.showSaveDialog({
      defaultPath: 'copilot-task-result.json',
      filters: [
        { name: 'JSON Files', extensions: ['json'] }
      ]
    });
    
    return result;
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

module.exports = { MobileCopilotAgentApp, DesktopCopilotAgentApp, desktopAppCSS };
