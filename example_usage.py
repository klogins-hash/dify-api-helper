#!/usr/bin/env python3
"""
Example usage of Dify API Client
"""

import os
from dotenv import load_dotenv
from dify_client import DifyClient

# Load environment variables
load_dotenv()

def main():
    # Initialize client
    api_url = os.getenv('DIFY_API_URL', 'https://api-production-50f6.up.railway.app')
    client = DifyClient(api_url)
    
    # Login
    email = os.getenv('DIFY_EMAIL')
    password = os.getenv('DIFY_PASSWORD')
    
    if not email or not password:
        print("Please set DIFY_EMAIL and DIFY_PASSWORD in .env file")
        return
    
    print("Logging in...")
    try:
        login_response = client.login(email, password)
        print("✓ Login successful!")
        print(f"User: {login_response.get('data', {}).get('email', 'N/A')}")
    except Exception as e:
        print(f"✗ Login failed: {e}")
        return
    
    # Get all apps
    print("\nFetching apps...")
    try:
        apps_response = client.get_apps()
        apps = apps_response.get('data', [])
        print(f"✓ Found {len(apps)} apps:")
        for app in apps:
            print(f"  - {app.get('name')} (ID: {app.get('id')}, Mode: {app.get('mode')})")
    except Exception as e:
        print(f"✗ Failed to fetch apps: {e}")
    
    # Get all datasets
    print("\nFetching datasets...")
    try:
        datasets_response = client.get_datasets()
        datasets = datasets_response.get('data', [])
        print(f"✓ Found {len(datasets)} datasets:")
        for dataset in datasets:
            print(f"  - {dataset.get('name')} (ID: {dataset.get('id')})")
    except Exception as e:
        print(f"✗ Failed to fetch datasets: {e}")
    
    # Example: Create a new app
    print("\nExample: Create a new app")
    print("Uncomment the code below to create a test app:")
    print("""
    # new_app = client.create_app(
    #     name="Test Chat App",
    #     mode="chat",
    #     icon="🤖",
    #     description="A test chat application"
    # )
    # print(f"Created app: {new_app}")
    """)
    
    # Example: Chat with an app (requires app API key)
    app_key = os.getenv('DIFY_APP_KEY')
    if app_key:
        print("\nTesting chat completion...")
        try:
            response = client.chat_completion(
                app_key=app_key,
                query="Hello! How are you?",
                user="test-user"
            )
            print(f"✓ Response: {response.get('answer', 'N/A')}")
        except Exception as e:
            print(f"✗ Chat failed: {e}")
    else:
        print("\nTo test chat completion:")
        print("1. Get an app API key from the web UI (App Settings > API Access)")
        print("2. Add DIFY_APP_KEY to your .env file")
        print("3. Run this script again")

if __name__ == "__main__":
    main()
