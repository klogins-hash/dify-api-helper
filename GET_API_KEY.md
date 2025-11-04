# How to Get Your Dify API Key

## Quick Steps

1. **Go to your Dify web interface:**
   - URL: https://web-production-d3c4.up.railway.app

2. **Navigate to your application:**
   - Click on the app you want to get the API key for

3. **Find the API Key in one of these locations:**
   - **Overview page** → Click "API Key" button
   - **API Access page** → Click "API Key" button  
   - **Monitoring page** → Click "API Key" button

4. **Copy the API key:**
   - Click the "API Key" button
   - Copy the generated key (format: `app-xxxxxxxxxxxxx`)

## Using the API Key

Once you have your API key, add it to your `.env` file:

```bash
DIFY_APP_KEY=app-xxxxxxxxxxxxx
```

Or use it directly in API calls:

```bash
curl --location --request POST 'https://api-production-50f6.up.railway.app/v1/chat-messages' \
  --header 'Authorization: Bearer app-xxxxxxxxxxxxx' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "inputs": {},
    "query": "Hello!",
    "response_mode": "blocking",
    "user": "test-user"
  }'
```

## Security Best Practices

⚠️ **Important:**
- Never hardcode API keys in client-side code
- Store API keys in environment variables or secure server-side storage
- Use backend proxy for API calls from frontend applications
- You can disable API access temporarily in: **Monitoring → Backend Service API**

## API Endpoints

### Your Dify Instance URLs:
- **Console API (Backend Management):** https://api-production-50f6.up.railway.app/console/api
- **Public API (App Interactions):** https://api-production-50f6.up.railway.app/v1
- **Web Interface:** https://web-production-d3c4.up.railway.app

## Example with Python Client

```python
from dify_client import DifyClient

# For app interactions (requires app API key)
client = DifyClient("https://api-production-50f6.up.railway.app")

response = client.chat_completion(
    app_key="app-xxxxxxxxxxxxx",  # Your app API key
    query="Hello, how are you?",
    user="user-123"
)

print(response['answer'])
```

## Troubleshooting

### Can't find API Key button?
- Make sure you're logged in
- Ensure you have permission to access the app
- Try refreshing the page

### API Key not working?
- Check that you're using the correct format: `Bearer app-xxxxx`
- Verify the app is published and active
- Check API access isn't disabled in Monitoring settings

### Need Console API access?
- Use the login method in `dify_client.py`
- Login with your email/password to get an access token
- This gives you backend management access
