# 🚀 Quick Deploy to Railway

## Option 1: One-Click Deploy (Easiest)

1. Click this button: [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/klogins-hash/dify-api-helper)

2. Set environment variables in Railway:
   - `DIFY_API_URL` = `https://api-production-50f6.up.railway.app`
   - `PORT` = `5000`

3. Done! Your API will be live at: `https://your-app.up.railway.app`

## Option 2: Deploy from GitHub

1. Go to [Railway](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select `klogins-hash/dify-api-helper`
4. Add environment variables (same as above)
5. Deploy!

## Test Your Deployment

```bash
# Health check
curl https://your-app.up.railway.app/health

# Login
curl -X POST https://your-app.up.railway.app/login \
  -H "Content-Type: application/json" \
  -d '{"email": "your-email", "password": "your-password"}'

# Get apps
curl https://your-app.up.railway.app/apps
```

## What You Get

✅ REST API for managing Dify apps  
✅ Update prompts programmatically  
✅ Change model settings via API  
✅ Add variables and configure apps  
✅ Link knowledge bases  
✅ Full CRUD operations on apps  

## Repository

**GitHub:** https://github.com/klogins-hash/dify-api-helper

## Documentation

- `README.md` - Full setup guide
- `DEPLOYMENT.md` - Detailed deployment instructions
- `PROGRAMMATIC_CHANGES.md` - How to modify apps programmatically
- `GET_API_KEY.md` - How to get Dify API keys
- `modify_app_examples.py` - Code examples

## Support

Issues? Open a ticket on GitHub: https://github.com/klogins-hash/dify-api-helper/issues
