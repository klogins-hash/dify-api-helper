# Programmatic Changes to Dify Apps

Complete guide for making programmatic changes to your Dify applications.

## Quick Start

```python
from dify_client import DifyClient

# Initialize and login
client = DifyClient("https://api-production-50f6.up.railway.app")
client.login("your-email@example.com", "your-password")

# Get your app ID
apps = client.get_apps()
app_id = apps['data'][0]['id']

# Make changes!
client.update_prompt(app_id, "Your new system prompt here")
```

## Available Modifications

### 1. Update System Prompt/Instructions

```python
new_prompt = """You are a helpful assistant.
Follow these guidelines:
- Be concise
- Be accurate
- Be friendly
"""

client.update_prompt(app_id, new_prompt, mode="chat")
```

### 2. Change AI Model & Settings

```python
client.update_model_settings(
    app_id=app_id,
    model_name="gpt-4",        # Model to use
    temperature=0.7,            # 0-2, lower=focused, higher=creative
    max_tokens=2048,           # Max response length
    top_p=0.9                  # Nucleus sampling (0-1)
)
```

**Available Models:**
- `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`
- `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku`
- `gemini-pro`, `gemini-1.5-pro`
- Check your Dify instance for configured models

### 3. Add User Input Variables

```python
# Text input
client.add_variable(
    app_id=app_id,
    variable_name="user_name",
    variable_type="text-input",
    label="Your Name",
    required=True,
    max_length=50
)

# Paragraph input
client.add_variable(
    app_id=app_id,
    variable_name="description",
    variable_type="paragraph",
    label="Detailed Description",
    required=False,
    max_length=500
)

# Number input
client.add_variable(
    app_id=app_id,
    variable_name="age",
    variable_type="number",
    label="Age",
    required=False
)
```

**Variable Types:**
- `text-input` - Single line text
- `paragraph` - Multi-line text
- `number` - Numeric input
- `select` - Dropdown selection

### 4. Update Welcome Message

```python
client.update_opening_statement(
    app_id=app_id,
    opening_statement="👋 Welcome! How can I help you today?",
    suggested_questions=[
        "What can you do?",
        "How do I get started?",
        "Tell me about your features"
    ]
)
```

### 5. Link Knowledge Base (RAG)

```python
# First, get your dataset ID
datasets = client.get_datasets()
dataset_id = datasets['data'][0]['id']

# Link it to your app
client.link_knowledge_base(
    app_id=app_id,
    dataset_id=dataset_id,
    retrieval_model="multiple"  # or "single"
)
```

### 6. Add Tools/Plugins

```python
tool_config = {
    "enabled": True,
    "config": {
        "api_key": "your-api-key",
        "max_results": 5
    }
}

client.add_tool_to_app(
    app_id=app_id,
    tool_name="web_search",
    tool_config=tool_config
)
```

### 7. Rename App & Update Metadata

```python
client.rename_app(
    app_id=app_id,
    new_name="My Awesome Bot",
    icon="🤖",
    description="An AI assistant that helps with..."
)
```

### 8. Workflow Apps (Advanced)

```python
# Get current workflow
workflow = client.get_workflow(app_id)

# Modify workflow data
workflow['nodes'].append({
    "id": "new-node-id",
    "type": "llm",
    "config": {...}
})

# Update workflow
client.update_workflow(app_id, workflow)

# Publish changes
client.publish_workflow(app_id)
```

### 9. Delete App

```python
client.delete_app(app_id)
```

### 10. Inspect Current Configuration

```python
# Get app details
app = client.get_app_detail(app_id)
print(f"Name: {app['name']}")
print(f"Mode: {app['mode']}")

# Get prompt configuration
config = client.get_prompt_config(app_id)
print(f"Prompt: {config['prompt_template']}")

# Get parameters
params = client.get_app_parameters(app_id)
print(f"Opening: {params['opening_statement']}")
print(f"Variables: {params['user_input_form']}")
```

## Complete Example: Create & Configure App

```python
from dify_client import DifyClient

client = DifyClient("https://api-production-50f6.up.railway.app")
client.login("your-email", "your-password")

# 1. Create app
app = client.create_app(
    name="Customer Support Bot",
    mode="chat",
    icon="💬",
    description="AI customer support assistant"
)
app_id = app['id']

# 2. Set system prompt
prompt = """You are a customer support specialist.
- Be helpful and professional
- Solve problems efficiently
- Escalate when needed
"""
client.update_prompt(app_id, prompt)

# 3. Configure model
client.update_model_settings(
    app_id=app_id,
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=1500
)

# 4. Add input variables
client.add_variable(
    app_id=app_id,
    variable_name="customer_name",
    label="Customer Name",
    required=True
)

client.add_variable(
    app_id=app_id,
    variable_name="issue_type",
    label="Issue Type",
    required=True
)

# 5. Set welcome message
client.update_opening_statement(
    app_id=app_id,
    opening_statement="Hi! I'm here to help. What can I assist you with?",
    suggested_questions=[
        "I have a billing question",
        "I need technical support",
        "I want to return a product"
    ]
)

# 6. Link knowledge base (if you have one)
datasets = client.get_datasets()
if datasets['data']:
    client.link_knowledge_base(app_id, datasets['data'][0]['id'])

print(f"✅ App configured! ID: {app_id}")
```

## Bulk Operations

### Update All Apps

```python
apps = client.get_apps()

for app in apps['data']:
    app_id = app['id']
    
    # Update model for all apps
    client.update_model_settings(
        app_id=app_id,
        model_name="gpt-4",
        temperature=0.7
    )
    
    print(f"✓ Updated {app['name']}")
```

### Clone App Configuration

```python
# Get config from source app
source_config = client.get_prompt_config(source_app_id)
source_params = client.get_app_parameters(source_app_id)

# Create new app
new_app = client.create_app("Cloned App", mode="chat")
new_app_id = new_app['id']

# Apply same configuration
client.update_app_config(new_app_id, source_config)
client.update_app_parameters(new_app_id, source_params)
```

## Advanced: Direct API Calls

If you need something not in the client:

```python
# Custom API call
url = f"{client.console_api}/apps/{app_id}/custom-endpoint"
response = client.session.post(url, json={...})
data = response.json()
```

## Common Use Cases

### 1. A/B Testing Different Prompts

```python
# Version A
client.update_prompt(app_id_a, "Prompt version A")

# Version B  
client.update_prompt(app_id_b, "Prompt version B")

# Compare results...
```

### 2. Scheduled Prompt Updates

```python
import schedule

def update_daily_prompt():
    new_prompt = f"Today is {datetime.now().strftime('%A')}. Help users with..."
    client.update_prompt(app_id, new_prompt)

schedule.every().day.at("00:00").do(update_daily_prompt)
```

### 3. Dynamic Model Selection

```python
def use_best_model_for_task(task_complexity):
    if task_complexity == "simple":
        model = "gpt-3.5-turbo"
    elif task_complexity == "complex":
        model = "gpt-4"
    else:
        model = "claude-3-sonnet"
    
    client.update_model_settings(app_id, model_name=model)
```

### 4. Sync Configuration Across Environments

```python
# Export from production
prod_config = prod_client.get_prompt_config(prod_app_id)
prod_params = prod_client.get_app_parameters(prod_app_id)

# Import to staging
staging_client.update_app_config(staging_app_id, prod_config)
staging_client.update_app_parameters(staging_app_id, prod_params)
```

## Troubleshooting

### Authentication Issues
```python
# Make sure you're logged in
client.login(email, password)

# Check if session is valid
try:
    client.get_apps()
except:
    print("Need to re-login")
    client.login(email, password)
```

### Finding App IDs
```python
apps = client.get_apps()
for app in apps['data']:
    print(f"{app['name']}: {app['id']}")
```

### Debugging API Calls
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Now all HTTP requests will be logged
```

## See Also

- `modify_app_examples.py` - Runnable examples
- `dify_client.py` - Full client implementation
- `example_usage.py` - Basic usage examples
- [Dify API Docs](https://docs.dify.ai/api-reference)
