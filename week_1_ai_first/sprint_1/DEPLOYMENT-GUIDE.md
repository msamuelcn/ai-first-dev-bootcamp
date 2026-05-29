# Deployment Guide — Workout REST API

## Current Public Render Deployment
- URL: https://gauntletai-vslp.onrender.com
- Status: Live and accessible

## Deployment Steps
1. Ensure all code changes are committed to Git.
```bash
git remote add origin https://github.com/msamuelcn/ai-first-dev-bootcamp
git push -u origin main
```
2. Connect to Render.com
 - Go to https://dashboard.render.com/
 - Click +New → Web Service
 - Go to Public GitHub Repo → Paste the repo URL: https://github.com/msamuelcn/ai-first-dev-bootcamp
 - Select the `main` branch
 - Set the Root Directory to `week_1_ai_first/sprint_1`
 - Environment: Python 3

3. Configure build and start commands:
 - Build Command: `pip install -r requirements.txt`
 - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`

4. Deploy
    - Click "Create Web Service"
    - Wait for build and deployment to complete
    - Access the live URL provided by Render

5. Verify deployment
    - Check the health endpoint: `https://gauntletai-vslp.onrender.com/health`
    - Check API docs: `https://gauntletai-vslp.onrender.com/docs`


