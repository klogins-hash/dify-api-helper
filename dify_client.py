#!/usr/bin/env python3
"""
Dify API Client Helper
Interact with your Dify backend programmatically
"""

import requests
import json
from typing import Optional, Dict, Any

class DifyClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """
        Initialize Dify API Client
        
        Args:
            base_url: Base URL of your Dify instance (e.g., https://api-production-50f6.up.railway.app)
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.console_api = f"{self.base_url}/console/api"
        self.public_api = f"{self.base_url}/api"
        self.api_key = api_key
        self.session = requests.Session()
        
    def set_api_key(self, api_key: str):
        """Set or update the API key"""
        self.api_key = api_key
        
    def login(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login to get access token
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Response with access token
        """
        url = f"{self.console_api}/login"
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        
        # Store the access token
        if 'data' in data and 'access_token' in data['data']:
            self.session.headers.update({
                'Authorization': f"Bearer {data['data']['access_token']}"
            })
        
        return data
    
    def get_apps(self) -> Dict[str, Any]:
        """Get list of all apps"""
        url = f"{self.console_api}/apps"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def get_app_detail(self, app_id: str) -> Dict[str, Any]:
        """Get details of a specific app"""
        url = f"{self.console_api}/apps/{app_id}"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def create_app(self, name: str, mode: str = "chat", icon: str = "🤖", 
                   description: str = "") -> Dict[str, Any]:
        """
        Create a new app
        
        Args:
            name: App name
            mode: App mode (chat, completion, agent-chat, workflow)
            icon: App icon emoji
            description: App description
        """
        url = f"{self.console_api}/apps"
        payload = {
            "name": name,
            "mode": mode,
            "icon": icon,
            "description": description
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def update_app_config(self, app_id: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Update app model configuration"""
        url = f"{self.console_api}/apps/{app_id}/model-config"
        response = self.session.post(url, json=config)
        response.raise_for_status()
        return response.json()
    
    def get_app_parameters(self, app_id: str) -> Dict[str, Any]:
        """Get app parameters and configuration"""
        url = f"{self.console_api}/apps/{app_id}/parameters"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def update_app_parameters(self, app_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Update app parameters (variables, opening statement, etc.)"""
        url = f"{self.console_api}/apps/{app_id}/parameters"
        response = self.session.post(url, json=parameters)
        response.raise_for_status()
        return response.json()
    
    def get_prompt_config(self, app_id: str) -> Dict[str, Any]:
        """Get current prompt configuration"""
        url = f"{self.console_api}/apps/{app_id}/model-config"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def update_prompt(self, app_id: str, prompt: str, mode: str = "chat") -> Dict[str, Any]:
        """
        Update app prompt/instructions
        
        Args:
            app_id: App ID
            prompt: New prompt text
            mode: App mode (chat, completion, etc.)
        """
        # Get current config first
        current_config = self.get_prompt_config(app_id)
        
        # Update the prompt
        if mode == "chat":
            current_config['prompt_template'] = prompt
        else:
            current_config['completion_params']['prompt'] = prompt
        
        return self.update_app_config(app_id, current_config)
    
    def update_model_settings(self, app_id: str, model_name: str, 
                             temperature: float = 0.7, max_tokens: int = 2048,
                             top_p: float = 1.0) -> Dict[str, Any]:
        """
        Update model settings (model, temperature, max tokens, etc.)
        
        Args:
            app_id: App ID
            model_name: Model identifier (e.g., 'gpt-4', 'claude-3-sonnet')
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            top_p: Nucleus sampling parameter
        """
        config = {
            "model": {
                "name": model_name,
                "completion_params": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "top_p": top_p
                }
            }
        }
        return self.update_app_config(app_id, config)
    
    def add_variable(self, app_id: str, variable_name: str, variable_type: str = "text-input",
                    label: str = "", required: bool = False, max_length: int = 48) -> Dict[str, Any]:
        """
        Add a user input variable to the app
        
        Args:
            app_id: App ID
            variable_name: Variable key name
            variable_type: Type (text-input, select, paragraph, number)
            label: Display label
            required: Whether variable is required
            max_length: Maximum length for text inputs
        """
        params = self.get_app_parameters(app_id)
        
        new_variable = {
            "variable": variable_name,
            "type": variable_type,
            "label": label or variable_name,
            "required": required,
            "max_length": max_length
        }
        
        if 'user_input_form' not in params:
            params['user_input_form'] = []
        
        params['user_input_form'].append(new_variable)
        return self.update_app_parameters(app_id, params)
    
    def update_opening_statement(self, app_id: str, opening_statement: str,
                                suggested_questions: list = None) -> Dict[str, Any]:
        """
        Update app opening statement and suggested questions
        
        Args:
            app_id: App ID
            opening_statement: Opening message text
            suggested_questions: List of suggested question strings
        """
        params = self.get_app_parameters(app_id)
        params['opening_statement'] = opening_statement
        
        if suggested_questions:
            params['suggested_questions'] = suggested_questions
        
        return self.update_app_parameters(app_id, params)
    
    def get_workflow(self, app_id: str) -> Dict[str, Any]:
        """Get workflow configuration for workflow apps"""
        url = f"{self.console_api}/apps/{app_id}/workflows/draft"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def update_workflow(self, app_id: str, workflow_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update workflow configuration
        
        Args:
            app_id: App ID
            workflow_data: Complete workflow configuration
        """
        url = f"{self.console_api}/apps/{app_id}/workflows/draft"
        response = self.session.post(url, json=workflow_data)
        response.raise_for_status()
        return response.json()
    
    def publish_workflow(self, app_id: str) -> Dict[str, Any]:
        """Publish workflow changes"""
        url = f"{self.console_api}/apps/{app_id}/workflows/publish"
        response = self.session.post(url, json={})
        response.raise_for_status()
        return response.json()
    
    def add_tool_to_app(self, app_id: str, tool_name: str, tool_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a tool/plugin to the app
        
        Args:
            app_id: App ID
            tool_name: Tool identifier
            tool_config: Tool configuration
        """
        config = self.get_prompt_config(app_id)
        
        if 'agent_mode' not in config:
            config['agent_mode'] = {'enabled': True, 'tools': []}
        
        config['agent_mode']['tools'].append({
            'tool_name': tool_name,
            'tool_config': tool_config
        })
        
        return self.update_app_config(app_id, config)
    
    def link_knowledge_base(self, app_id: str, dataset_id: str, 
                           retrieval_model: str = "multiple") -> Dict[str, Any]:
        """
        Link a knowledge base/dataset to the app
        
        Args:
            app_id: App ID
            dataset_id: Dataset/knowledge base ID
            retrieval_model: Retrieval mode (single, multiple)
        """
        url = f"{self.console_api}/apps/{app_id}/datasets"
        payload = {
            "datasets": [{
                "dataset_id": dataset_id,
                "retrieval_model": retrieval_model
            }]
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def delete_app(self, app_id: str) -> Dict[str, Any]:
        """Delete an app"""
        url = f"{self.console_api}/apps/{app_id}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()
    
    def rename_app(self, app_id: str, new_name: str, icon: str = None, 
                  description: str = None) -> Dict[str, Any]:
        """
        Rename app and update metadata
        
        Args:
            app_id: App ID
            new_name: New app name
            icon: New icon emoji (optional)
            description: New description (optional)
        """
        url = f"{self.console_api}/apps/{app_id}"
        payload = {"name": new_name}
        
        if icon:
            payload["icon"] = icon
        if description:
            payload["description"] = description
        
        response = self.session.put(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_datasets(self) -> Dict[str, Any]:
        """Get list of all datasets/knowledge bases"""
        url = f"{self.console_api}/datasets"
        response = self.session.get(url)
        response.raise_for_status()
        return response.json()
    
    def create_dataset(self, name: str, description: str = "") -> Dict[str, Any]:
        """Create a new dataset/knowledge base"""
        url = f"{self.console_api}/datasets"
        payload = {
            "name": name,
            "description": description
        }
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def upload_document(self, dataset_id: str, file_path: str) -> Dict[str, Any]:
        """Upload a document to a dataset"""
        url = f"{self.console_api}/datasets/{dataset_id}/documents"
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = self.session.post(url, files=files)
        response.raise_for_status()
        return response.json()
    
    def chat_completion(self, app_key: str, query: str, user: str = "user",
                       conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat message to an app (Public API)
        
        Args:
            app_key: App API key (get from app settings)
            query: User message
            user: User identifier
            conversation_id: Optional conversation ID for context
        """
        url = f"{self.public_api}/chat-messages"
        headers = {
            'Authorization': f'Bearer {app_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            "query": query,
            "user": user,
            "response_mode": "blocking"
        }
        if conversation_id:
            payload["conversation_id"] = conversation_id
            
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_conversations(self, app_key: str, user: str = "user") -> Dict[str, Any]:
        """Get conversation history"""
        url = f"{self.public_api}/conversations"
        headers = {
            'Authorization': f'Bearer {app_key}',
        }
        params = {'user': user}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


# Example usage
if __name__ == "__main__":
    # Initialize client
    client = DifyClient("https://api-production-50f6.up.railway.app")
    
    print("Dify API Client")
    print("=" * 50)
    print("\nTo use this client:")
    print("1. Login with your credentials:")
    print("   client.login('your-email@example.com', 'your-password')")
    print("\n2. Get your apps:")
    print("   apps = client.get_apps()")
    print("\n3. Create a new app:")
    print("   app = client.create_app('My App', mode='chat')")
    print("\n4. For public API access, get the app API key from the web UI")
    print("   then use: client.chat_completion(app_key, 'Hello!')")
    print("\n" + "=" * 50)
