# Dify API Helper

Python client and REST API for interacting with your Dify backend programmatically.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file:
```bash
cp .env.example .env
```

3. Edit `.env` with your credentials:
```
DIFY_API_URL=https://api-production-50f6.up.railway.app
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
```

## Quick Start

### Run the example:
```bash
python example_usage.py
```

### Use in your own code:
```python
from dify_client import DifyClient

# Initialize
client = DifyClient("https://api-production-50f6.up.railway.app")

# Login
client.login("your-email@example.com", "your-password")

# Get apps
apps = client.get_apps()
print(apps)

# Create a new app
new_app = client.create_app(
    name="My Chat Bot",
    mode="chat",
    icon="🤖",
    description="An AI assistant"
)

# Get datasets
datasets = client.get_datasets()

# Create a dataset
dataset = client.create_dataset(
    name="My Knowledge Base",
    description="Company documentation"
)
```

## API Endpoints

### Console API (Backend Management)
- **Base URL:** `https://api-production-50f6.up.railway.app/console/api`
- **Authentication:** Login with email/password to get access token
- **Use for:** Managing apps, datasets, configurations

### Public API (App Interactions)
- **Base URL:** `https://api-production-50f6.up.railway.app/api`
- **Authentication:** App-specific API keys (get from web UI)
- **Use for:** Chat completions, conversations, app interactions

## Available Methods

### Authentication
- `login(email, password)` - Login and get access token

### Apps
- `get_apps()` - List all apps
- `get_app_detail(app_id)` - Get app details
- `create_app(name, mode, icon, description)` - Create new app
- `update_app_config(app_id, config)` - Update app configuration

### Datasets/Knowledge Bases
- `get_datasets()` - List all datasets
- `create_dataset(name, description)` - Create new dataset
- `upload_document(dataset_id, file_path)` - Upload document to dataset

### Chat (Public API)
- `chat_completion(app_key, query, user, conversation_id)` - Send chat message
- `get_conversations(app_key, user)` - Get conversation history

## Getting App API Keys

1. Go to your Dify web UI: https://web-production-d3c4.up.railway.app
2. Open an app
3. Go to **Settings** > **API Access**
4. Copy the API key
5. Add to `.env` file as `DIFY_APP_KEY`

## Direct Database Access

If you need direct database access:

```python
import psycopg2

conn = psycopg2.connect(
    host="postgres-1e_q.railway.internal",  # Use public URL for external access
    database="railway",
    user="postgres",
    password="jhQTtTxWHUSi3NJBrrqC!_gBKol41w2R",
    port=5432
)
```

**Note:** Direct DB access requires being on Railway's internal network or using a proxy.

## Environment Variables from Railway

Your Dify instance has these key variables:
- `CONSOLE_API_URL`: https://api-production-50f6.up.railway.app
- `CONSOLE_WEB_URL`: https://web-production-d3c4.up.railway.app
- `SECRET_KEY`: M1pi17mfQBZVjMEle260WhaBirMT3nLk

## Troubleshooting

### Authentication Issues
- Make sure you're using the correct email/password
- Check that your account is activated

### API Key Issues
- Verify the app API key is correct
- Make sure the app is published

### Connection Issues
- Verify the API URL is accessible
- Check Railway service status

## Documentation

- [Dify API Documentation](https://docs.dify.ai/guides/application-publishing/developing-with-apis)
- [Railway Dashboard](https://railway.app)
