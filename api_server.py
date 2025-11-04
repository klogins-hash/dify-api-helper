#!/usr/bin/env python3
"""
Flask API Server for Dify Client
Provides REST API endpoints to manage Dify apps programmatically
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dify_client import DifyClient
from functools import wraps

app = Flask(__name__)
CORS(app)

# Global client instance
client = None

def require_auth(f):
    """Decorator to ensure client is authenticated"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        global client
        if client is None:
            return jsonify({"error": "Not authenticated. Call /login first"}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "dify-api-helper"})

@app.route('/login', methods=['POST'])
def login():
    """Login to Dify"""
    global client
    
    data = request.json
    email = data.get('email')
    password = data.get('password')
    base_url = data.get('base_url', os.getenv('DIFY_API_URL', 'https://api-production-50f6.up.railway.app'))
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        client = DifyClient(base_url)
        result = client.login(email, password)
        return jsonify({"success": True, "message": "Logged in successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 401

@app.route('/apps', methods=['GET'])
@require_auth
def get_apps():
    """Get all apps"""
    try:
        result = client.get_apps()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>', methods=['GET'])
@require_auth
def get_app_detail(app_id):
    """Get app details"""
    try:
        result = client.get_app_detail(app_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps', methods=['POST'])
@require_auth
def create_app():
    """Create a new app"""
    data = request.json
    try:
        result = client.create_app(
            name=data.get('name'),
            mode=data.get('mode', 'chat'),
            icon=data.get('icon', '🤖'),
            description=data.get('description', '')
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>', methods=['PUT'])
@require_auth
def rename_app(app_id):
    """Rename app"""
    data = request.json
    try:
        result = client.rename_app(
            app_id=app_id,
            new_name=data.get('name'),
            icon=data.get('icon'),
            description=data.get('description')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>', methods=['DELETE'])
@require_auth
def delete_app(app_id):
    """Delete app"""
    try:
        result = client.delete_app(app_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>/prompt', methods=['PUT'])
@require_auth
def update_prompt(app_id):
    """Update app prompt"""
    data = request.json
    try:
        result = client.update_prompt(
            app_id=app_id,
            prompt=data.get('prompt'),
            mode=data.get('mode', 'chat')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>/model', methods=['PUT'])
@require_auth
def update_model_settings(app_id):
    """Update model settings"""
    data = request.json
    try:
        result = client.update_model_settings(
            app_id=app_id,
            model_name=data.get('model_name'),
            temperature=data.get('temperature', 0.7),
            max_tokens=data.get('max_tokens', 2048),
            top_p=data.get('top_p', 1.0)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>/variables', methods=['POST'])
@require_auth
def add_variable(app_id):
    """Add variable to app"""
    data = request.json
    try:
        result = client.add_variable(
            app_id=app_id,
            variable_name=data.get('variable_name'),
            variable_type=data.get('variable_type', 'text-input'),
            label=data.get('label', ''),
            required=data.get('required', False),
            max_length=data.get('max_length', 48)
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>/opening', methods=['PUT'])
@require_auth
def update_opening_statement(app_id):
    """Update opening statement"""
    data = request.json
    try:
        result = client.update_opening_statement(
            app_id=app_id,
            opening_statement=data.get('opening_statement'),
            suggested_questions=data.get('suggested_questions')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/apps/<app_id>/knowledge', methods=['POST'])
@require_auth
def link_knowledge_base(app_id):
    """Link knowledge base to app"""
    data = request.json
    try:
        result = client.link_knowledge_base(
            app_id=app_id,
            dataset_id=data.get('dataset_id'),
            retrieval_model=data.get('retrieval_model', 'multiple')
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/datasets', methods=['GET'])
@require_auth
def get_datasets():
    """Get all datasets"""
    try:
        result = client.get_datasets()
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/datasets', methods=['POST'])
@require_auth
def create_dataset():
    """Create a new dataset"""
    data = request.json
    try:
        result = client.create_dataset(
            name=data.get('name'),
            description=data.get('description', '')
        )
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
