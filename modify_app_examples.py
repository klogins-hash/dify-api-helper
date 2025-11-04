#!/usr/bin/env python3
"""
Examples of programmatically modifying Dify apps
"""

import os
from dotenv import load_dotenv
from dify_client import DifyClient

load_dotenv()

def setup_client():
    """Initialize and login to Dify"""
    client = DifyClient(os.getenv('DIFY_API_URL', 'https://api-production-50f6.up.railway.app'))
    client.login(
        os.getenv('DIFY_EMAIL'),
        os.getenv('DIFY_PASSWORD')
    )
    return client

# ============================================================================
# EXAMPLE 1: Update App Prompt/Instructions
# ============================================================================
def update_app_prompt_example(client, app_id):
    """Change the system prompt of an app"""
    
    new_prompt = """You are a helpful AI assistant specialized in customer support.
    
Your responsibilities:
- Answer customer questions clearly and concisely
- Be friendly and professional
- If you don't know something, admit it
- Always prioritize customer satisfaction

Guidelines:
- Keep responses under 3 paragraphs
- Use bullet points for lists
- Provide examples when helpful
"""
    
    print("Updating app prompt...")
    result = client.update_prompt(app_id, new_prompt, mode="chat")
    print(f"✓ Prompt updated successfully!")
    return result


# ============================================================================
# EXAMPLE 2: Change Model Settings
# ============================================================================
def update_model_settings_example(client, app_id):
    """Change the AI model and its parameters"""
    
    print("Updating model settings...")
    result = client.update_model_settings(
        app_id=app_id,
        model_name="gpt-4",  # or "claude-3-sonnet", "gpt-3.5-turbo", etc.
        temperature=0.7,      # Lower = more focused, Higher = more creative
        max_tokens=2048,      # Maximum response length
        top_p=0.9            # Nucleus sampling
    )
    print(f"✓ Model settings updated!")
    return result


# ============================================================================
# EXAMPLE 3: Add User Input Variables
# ============================================================================
def add_variables_example(client, app_id):
    """Add custom input fields for users"""
    
    print("Adding user input variables...")
    
    # Add a text input for user's name
    client.add_variable(
        app_id=app_id,
        variable_name="user_name",
        variable_type="text-input",
        label="Your Name",
        required=True,
        max_length=50
    )
    
    # Add a paragraph input for detailed questions
    client.add_variable(
        app_id=app_id,
        variable_name="question_details",
        variable_type="paragraph",
        label="Describe your question in detail",
        required=False,
        max_length=500
    )
    
    print(f"✓ Variables added!")


# ============================================================================
# EXAMPLE 4: Update Opening Statement & Suggested Questions
# ============================================================================
def update_opening_statement_example(client, app_id):
    """Customize the welcome message and suggested questions"""
    
    opening_statement = "👋 Welcome! I'm your AI assistant. How can I help you today?"
    
    suggested_questions = [
        "What features do you offer?",
        "How do I get started?",
        "Can you help me troubleshoot an issue?",
        "What are your pricing plans?"
    ]
    
    print("Updating opening statement...")
    result = client.update_opening_statement(
        app_id=app_id,
        opening_statement=opening_statement,
        suggested_questions=suggested_questions
    )
    print(f"✓ Opening statement updated!")
    return result


# ============================================================================
# EXAMPLE 5: Link Knowledge Base to App
# ============================================================================
def link_knowledge_base_example(client, app_id, dataset_id):
    """Connect a knowledge base to your app for RAG"""
    
    print("Linking knowledge base to app...")
    result = client.link_knowledge_base(
        app_id=app_id,
        dataset_id=dataset_id,
        retrieval_model="multiple"  # or "single" for single document retrieval
    )
    print(f"✓ Knowledge base linked!")
    return result


# ============================================================================
# EXAMPLE 6: Add Tools/Plugins to App
# ============================================================================
def add_tool_example(client, app_id):
    """Add external tools or plugins to your app"""
    
    print("Adding tool to app...")
    
    # Example: Add a web search tool
    tool_config = {
        "enabled": True,
        "config": {
            "api_key": "your-search-api-key",
            "max_results": 5
        }
    }
    
    result = client.add_tool_to_app(
        app_id=app_id,
        tool_name="web_search",
        tool_config=tool_config
    )
    print(f"✓ Tool added!")
    return result


# ============================================================================
# EXAMPLE 7: Rename App and Update Metadata
# ============================================================================
def rename_app_example(client, app_id):
    """Change app name, icon, and description"""
    
    print("Renaming app...")
    result = client.rename_app(
        app_id=app_id,
        new_name="Customer Support Bot v2",
        icon="🤖",
        description="AI-powered customer support assistant with knowledge base integration"
    )
    print(f"✓ App renamed!")
    return result


# ============================================================================
# EXAMPLE 8: Complete App Setup from Scratch
# ============================================================================
def create_and_configure_app_example(client):
    """Create a new app and fully configure it"""
    
    print("\n" + "="*60)
    print("Creating and configuring a complete app...")
    print("="*60 + "\n")
    
    # Step 1: Create the app
    print("1. Creating app...")
    app = client.create_app(
        name="Product Recommendation Assistant",
        mode="chat",
        icon="🛍️",
        description="Helps users find the perfect product"
    )
    app_id = app['id']
    print(f"   ✓ App created with ID: {app_id}")
    
    # Step 2: Set the prompt
    print("\n2. Setting system prompt...")
    prompt = """You are a product recommendation expert. Help users find products that match their needs.

Ask clarifying questions about:
- Budget
- Use case
- Preferences
- Must-have features

Then provide 3-5 personalized recommendations with explanations."""
    
    client.update_prompt(app_id, prompt)
    print("   ✓ Prompt configured")
    
    # Step 3: Configure model
    print("\n3. Configuring AI model...")
    client.update_model_settings(
        app_id=app_id,
        model_name="gpt-4",
        temperature=0.8,  # More creative for recommendations
        max_tokens=1500
    )
    print("   ✓ Model configured")
    
    # Step 4: Add variables
    print("\n4. Adding input variables...")
    client.add_variable(
        app_id=app_id,
        variable_name="budget",
        variable_type="text-input",
        label="Budget Range",
        required=False
    )
    client.add_variable(
        app_id=app_id,
        variable_name="category",
        variable_type="text-input",
        label="Product Category",
        required=True
    )
    print("   ✓ Variables added")
    
    # Step 5: Set opening statement
    print("\n5. Setting welcome message...")
    client.update_opening_statement(
        app_id=app_id,
        opening_statement="🛍️ Hi! I'm here to help you find the perfect product. What are you looking for?",
        suggested_questions=[
            "I need a laptop for programming",
            "Looking for running shoes under $150",
            "Best headphones for music production"
        ]
    )
    print("   ✓ Opening statement set")
    
    print("\n" + "="*60)
    print(f"✅ App fully configured! App ID: {app_id}")
    print("="*60 + "\n")
    
    return app_id


# ============================================================================
# EXAMPLE 9: Bulk Update Multiple Apps
# ============================================================================
def bulk_update_apps_example(client):
    """Update multiple apps at once"""
    
    print("Fetching all apps...")
    apps_response = client.get_apps()
    apps = apps_response.get('data', [])
    
    print(f"Found {len(apps)} apps. Updating all...")
    
    for app in apps:
        app_id = app['id']
        app_name = app['name']
        
        print(f"\nUpdating: {app_name}")
        
        # Update model settings for all apps
        try:
            client.update_model_settings(
                app_id=app_id,
                model_name="gpt-4",
                temperature=0.7,
                max_tokens=2048
            )
            print(f"  ✓ {app_name} updated")
        except Exception as e:
            print(f"  ✗ {app_name} failed: {e}")
    
    print("\n✅ Bulk update complete!")


# ============================================================================
# EXAMPLE 10: Get Current Configuration
# ============================================================================
def inspect_app_config_example(client, app_id):
    """View current app configuration"""
    
    print(f"\nInspecting app configuration...")
    print("="*60)
    
    # Get app details
    app = client.get_app_detail(app_id)
    print(f"\nApp Name: {app.get('name')}")
    print(f"Mode: {app.get('mode')}")
    print(f"Icon: {app.get('icon')}")
    
    # Get prompt config
    config = client.get_prompt_config(app_id)
    print(f"\nCurrent Prompt:")
    print(config.get('prompt_template', 'N/A'))
    
    # Get parameters
    params = client.get_app_parameters(app_id)
    print(f"\nOpening Statement:")
    print(params.get('opening_statement', 'N/A'))
    
    print(f"\nVariables:")
    for var in params.get('user_input_form', []):
        print(f"  - {var.get('label')} ({var.get('variable')})")
    
    print("="*60)


# ============================================================================
# MAIN - Run Examples
# ============================================================================
if __name__ == "__main__":
    print("Dify App Modification Examples")
    print("="*60)
    
    # Setup
    client = setup_client()
    print("✓ Logged in successfully\n")
    
    # Get first app for examples
    apps = client.get_apps()
    if apps.get('data'):
        app_id = apps['data'][0]['id']
        print(f"Using app ID: {app_id}\n")
        
        # Uncomment the examples you want to run:
        
        # update_app_prompt_example(client, app_id)
        # update_model_settings_example(client, app_id)
        # add_variables_example(client, app_id)
        # update_opening_statement_example(client, app_id)
        # rename_app_example(client, app_id)
        # inspect_app_config_example(client, app_id)
        
        # Or create a complete new app:
        # create_and_configure_app_example(client)
        
        print("\n💡 Uncomment the examples you want to run in the code!")
    else:
        print("No apps found. Create one first!")
        # create_and_configure_app_example(client)
