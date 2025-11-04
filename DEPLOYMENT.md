# Railway Deployment Guide

## Quick Deploy

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template)

## Manual Deployment

### 1. Push to GitHub

```bash
cd /Users/franksimpson/CascadeProjects/dify-api-helper
git init
git add .
git commit -m "Initial commit: Dify API Helper"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/dify-api-helper.git
git push -u origin main
```

### 2. Deploy on Railway

1. Go to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `dify-api-helper` repository
5. Railway will auto-detect the Python app and deploy

### 3. Set Environment Variables

In Railway dashboard, add these variables:

```
DIFY_API_URL=https://api-production-50f6.up.railway.app
PORT=5000
```

Optional (for auto-login):
```
DIFY_EMAIL=your-email@example.com
DIFY_PASSWORD=your-password
```

### 4. Get Your API URL

Railway will provide a URL like: `https://dify-api-helper-production.up.railway.app`

## API Endpoints

Once deployed, you can use these endpoints:

### Health Check
```bash
curl https://your-app.railway.app/health
```

### Login
```bash
curl -X POST https://your-app.railway.app/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "your-email@example.com",
    "password": "your-password"
  }'
```

### Get Apps
```bash
curl https://your-app.railway.app/apps \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Create App
```bash
curl -X POST https://your-app.railway.app/apps \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My New App",
    "mode": "chat",
    "icon": "🤖",
    "description": "An AI assistant"
  }'
```

### Update Prompt
```bash
curl -X PUT https://your-app.railway.app/apps/APP_ID/prompt \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "You are a helpful assistant...",
    "mode": "chat"
  }'
```

### Update Model Settings
```bash
curl -X PUT https://your-app.railway.app/apps/APP_ID/model \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "gpt-4",
    "temperature": 0.7,
    "max_tokens": 2048
  }'
```

## Full API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/login` | POST | Authenticate |
| `/apps` | GET | List all apps |
| `/apps` | POST | Create app |
| `/apps/:id` | GET | Get app details |
| `/apps/:id` | PUT | Rename app |
| `/apps/:id` | DELETE | Delete app |
| `/apps/:id/prompt` | PUT | Update prompt |
| `/apps/:id/model` | PUT | Update model settings |
| `/apps/:id/variables` | POST | Add variable |
| `/apps/:id/opening` | PUT | Update opening statement |
| `/apps/:id/knowledge` | POST | Link knowledge base |
| `/datasets` | GET | List datasets |
| `/datasets` | POST | Create dataset |

## Using from Code

### JavaScript/Node.js
```javascript
const API_URL = 'https://your-app.railway.app';

// Login
const loginResponse = await fetch(`${API_URL}/login`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'your-email@example.com',
    password: 'your-password'
  })
});

// Get apps
const appsResponse = await fetch(`${API_URL}/apps`);
const apps = await appsResponse.json();

// Update prompt
await fetch(`${API_URL}/apps/${appId}/prompt`, {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'New system prompt',
    mode: 'chat'
  })
});
```

### Python
```python
import requests

API_URL = 'https://your-app.railway.app'

# Login
session = requests.Session()
session.post(f'{API_URL}/login', json={
    'email': 'your-email@example.com',
    'password': 'your-password'
})

# Get apps
apps = session.get(f'{API_URL}/apps').json()

# Update prompt
session.put(f'{API_URL}/apps/{app_id}/prompt', json={
    'prompt': 'New system prompt',
    'mode': 'chat'
})
```

## Monitoring

View logs in Railway dashboard:
1. Go to your project
2. Click on the service
3. Click "Logs" tab

## Troubleshooting

### Deployment Failed
- Check `railway.json` is present
- Verify `requirements.txt` has all dependencies
- Check Railway logs for errors

### API Not Responding
- Verify service is running in Railway dashboard
- Check environment variables are set
- Test health endpoint: `/health`

### Authentication Issues
- Verify DIFY_API_URL is correct
- Check Dify credentials
- Ensure Dify instance is accessible

## Local Development

Run locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export DIFY_API_URL=https://api-production-50f6.up.railway.app
export PORT=5000

# Run server
python api_server.py
```

Test locally:
```bash
curl http://localhost:5000/health
```

## Security Notes

- Never commit `.env` files
- Use Railway's environment variables for secrets
- The API requires authentication via `/login`
- Consider adding rate limiting for production use
- Add API key authentication for additional security

## Scaling

Railway automatically scales based on usage. For high traffic:
1. Upgrade Railway plan
2. Enable autoscaling
3. Add Redis for session management
4. Implement caching
