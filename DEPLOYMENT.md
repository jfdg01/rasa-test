# Railway Deployment Guide

This guide explains how to deploy the Rasa Wizard Game to Railway.

## Prerequisites

1. A Railway account (sign up at [railway.app](https://railway.app))
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Deployment Steps

### 1. Connect Your Repository

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"** (or your Git provider)
4. Select your repository containing this project
5. Railway will automatically detect the `Dockerfile` and start building

### 2. Configure Ports

Railway will automatically:
- Detect the Dockerfile
- Build the Docker image
- Expose port 8080 (or the PORT environment variable) as the public service

**No additional configuration needed!** The proxy server automatically handles forwarding Rasa API requests, so you only need one public port.

### 3. Environment Variables (Optional)

Railway will automatically set the `PORT` environment variable. The startup script will use it.

No additional environment variables are required for basic deployment.

### 4. Deploy

Railway will automatically:
- Build your Docker image
- Deploy it
- Provide you with a public URL

### 5. Access Your Application

Once deployed, Railway will provide you with a public URL like:
- `https://your-app-name.up.railway.app`

Access your game at:
- `https://your-app-name.up.railway.app/game_ui.html`

## Configuration Details

### Port Configuration

- **Port 8080** (or `$PORT`): Web UI (public)
- **Port 5005**: Rasa API server (internal, can be made public)
- **Port 5055**: Rasa Action Server (internal)

### How It Works

1. The `start.sh` script starts all three services:
   - Rasa Action Server on port 5055 (internal)
   - Rasa Server on port 5005 (internal)
   - Proxy/Web Server on port 8080 (or Railway's PORT) - **public**

2. The proxy server (`proxy_server.py`) serves static files (HTML, CSS, JS) and forwards API requests to the Rasa server on port 5005.

3. The HTML file (`game_ui.html`) automatically detects if it's running on Railway and uses the same origin for all requests (the proxy handles routing).

4. All services run in the same container, so they can communicate via `localhost`.

## Troubleshooting

### Issue: Rasa API not accessible

**Solution**: The proxy server should handle this automatically. Check Railway logs to ensure the proxy server is running. If issues persist, verify that the proxy server is forwarding requests correctly.

### Issue: Build fails

**Solution**: 
- Check Railway build logs
- Ensure all files are committed to Git
- Verify the Dockerfile is correct

### Issue: Services not starting

**Solution**:
- Check Railway logs: `railway logs`
- Verify the model file is in the `models/` directory
- Check that all dependencies are in `requirements.txt`

### Issue: CORS errors

**Solution**: The Rasa server is configured with `--cors "*"` which should allow all origins. If issues persist, check Railway logs.

## Railway CLI (Optional)

You can also deploy using Railway CLI:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

## Cost

Railway offers:
- **Free tier**: $5 credit/month (~500 hours of runtime)
- **Usage**: ~$0.01/hour
- **Estimate**: Can run ~500 hours/month free

## Monitoring

- View logs: Railway Dashboard → Your Service → Logs
- Monitor usage: Railway Dashboard → Usage
- Check health: Railway Dashboard → Metrics

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Get your public URL
3. ✅ Test the game at `https://your-url.up.railway.app/game_ui.html`
4. ✅ Share your game with others!

For more information, see [Railway Documentation](https://docs.railway.app).
