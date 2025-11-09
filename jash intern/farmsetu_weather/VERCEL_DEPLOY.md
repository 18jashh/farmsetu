# Deploying to Vercel

This guide will help you deploy your Django project to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed: `npm i -g vercel` (optional, for CLI deployment)
3. Your project pushed to GitHub (already done!)

## Quick Deployment Steps

### Option 1: Deploy via Vercel Dashboard (Recommended)

1. Go to https://vercel.com/new
2. Import your GitHub repository: `18jashh/farmsetu`
3. **IMPORTANT**: Set the **Root Directory** to: `jash intern/farmsetu_weather`
   - Click "Configure Project"
   - Under "Root Directory", enter: `jash intern/farmsetu_weather`
4. Vercel will automatically detect the `vercel.json` configuration
5. Add environment variables in the Vercel dashboard (Settings → Environment Variables):
   - `SECRET_KEY`: Generate a secure secret key:
     ```powershell
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `DEBUG`: Set to `0` for production
   - `ALLOWED_HOSTS`: Set to `*.vercel.app` (or your specific domain)
6. Click **Deploy**

### Option 2: Deploy via Vercel CLI

1. Install Vercel CLI (if not already installed):
   ```powershell
   npm i -g vercel
   ```

2. Navigate to the project directory:
   ```powershell
   cd "C:\Users\admin\Downloads\jash intern final\jash intern\farmsetu_weather"
   ```

3. Login to Vercel:
   ```powershell
   vercel login
   ```

4. Deploy (first time will ask for configuration):
   ```powershell
   vercel
   ```
   - When asked for root directory, enter: `jash intern/farmsetu_weather`
   - When asked to override settings, say yes and use the `vercel.json` file

5. For production deployment:
   ```powershell
   vercel --prod
   ```

## Environment Variables

Make sure to set these in your Vercel project settings:

- `SECRET_KEY`: Django secret key (required)
- `DEBUG`: `0` for production
- `ALLOWED_HOSTS`: Your Vercel domain (comma-separated if multiple)

## Important Notes

1. **Database**: SQLite won't work well on Vercel's serverless functions. Consider using:
   - Vercel Postgres (recommended)
   - Supabase
   - PlanetScale
   - Or any external PostgreSQL database

2. **Static Files**: Static files are served through Vercel's CDN. Make sure to run `python manage.py collectstatic` before deployment or configure it in your build process.

3. **Cold Starts**: Serverless functions may have cold start delays. This is normal for Django on Vercel.

4. **File System**: The file system is read-only except for `/tmp`. Don't rely on local file storage.

## Troubleshooting

- If you get import errors, check that `PYTHONPATH` is set correctly in `vercel.json`
- If static files aren't loading, ensure the static files route is configured in `vercel.json`
- Check Vercel function logs in the dashboard for detailed error messages

## After Deployment

Once deployed, you can:
- Access your app at `https://your-app.vercel.app`
- Import data using Django management commands (you'll need to set up a database first)
- Monitor logs in the Vercel dashboard

