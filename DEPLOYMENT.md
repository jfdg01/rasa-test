# 🚀 Deployment Guide - Rasa Wizard Game

## Quick Deploy to Railway.app (Recommended)

### Step 1: Prepare Your Repository
1. Push your project to GitHub:
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign up/Login with GitHub
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your repository
6. Railway will automatically:
   - Detect the Dockerfile
   - Build the image
   - Deploy your app

### Step 3: Configure
1. Go to your project settings
2. Under **"Networking"** → **"Public Networking"**
3. Click **"Generate Domain"**
4. You'll get a URL like: `https://your-app.railway.app`

### Step 4: Update Frontend
Update the RASA_SERVER_URL in `game_ui.html`:
```javascript
const RASA_SERVER_URL = 'https://your-app.railway.app:5005/webhooks/rest/webhook';
```

### Step 5: Access Your Game
Open: `https://your-app.railway.app:8080/game_ui.html`

---

## Alternative: Deploy to Render.com

### Step 1: Prepare Repository
Same as Railway (push to GitHub)

### Step 2: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click **"New +"** → **"Web Service"**
4. Connect your GitHub repository
5. Render will detect the `render.yaml` file
6. Click **"Create Web Service"**

### Step 3: Access
Your app will be at: `https://your-app.onrender.com`

---

## Important Notes

### Training the Model
Before deploying, train your Rasa model locally:
```bash
rasa train
```

This creates a model in the `models/` folder that will be included in the deployment.

### Environment Variables (Optional)
You can set these in Railway/Render dashboard:
- `RASA_TELEMETRY_ENABLED=false` - Disable telemetry
- `PORT=8080` - Web server port

### Free Tier Limitations
- **Railway**: $5 credit/month (~500 hours)
- **Render**: 750 hours/month (sleeps after 15 min inactivity)

### Keeping the App Awake (Render)
Render's free tier sleeps after inactivity. Options:
1. Use a service like [UptimeRobot](https://uptimerobot.com) to ping your app
2. Upgrade to paid tier
3. Accept the sleep behavior

---

## Testing Locally with Docker

Before deploying, test the Docker setup:

```bash
# Build the image
docker build -t rasa-game .

# Run the container
docker run -p 8080:8080 -p 5005:5005 -p 5055:5055 rasa-game

# Access at http://localhost:8080/game_ui.html
```

---

## Troubleshooting

### Issue: Rasa server not starting
- Check logs in Railway/Render dashboard
- Ensure model is trained (`rasa train`)
- Verify `requirements.txt` has all dependencies

### Issue: CORS errors
- Rasa is configured with `--cors "*"` in Dockerfile
- If issues persist, check browser console for specific errors

### Issue: Actions server not responding
- Ensure `endpoints.yml` points to correct action server URL
- Check if port 5055 is accessible

---

## Cost Estimate

### Railway.app (Recommended for this project)
- **Free tier**: $5 credit/month
- **Usage**: ~$0.01/hour running
- **Estimate**: Can run ~500 hours/month free
- **Paid**: $5/month for 100+ hours

### Render.com
- **Free tier**: 750 hours/month
- **Limitation**: Sleeps after 15 min inactivity
- **Paid**: $7/month for always-on

---

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Sign up for Railway or Render
3. ✅ Deploy from repository
4. ✅ Get your public URL
5. ✅ Update `game_ui.html` with your URL
6. ✅ Play your game online! 🎮

Need help? Check the platform's documentation:
- [Railway Docs](https://docs.railway.app)
- [Render Docs](https://render.com/docs)

