# Render Database Setup Guide

## Problem Identified

Your Django app is currently using **SQLite**, which **does NOT persist on Render**. SQLite files are ephemeral and get wiped on each deployment. This is why you're seeing "no data imported".

## Solution: Connect to Render PostgreSQL Database

### Step 1: Create PostgreSQL Database on Render

1. Go to your Render Dashboard: https://dashboard.render.com
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `farmsetu-db` (or any name you prefer)
   - **Database**: `farmsetu_db` (or any name)
   - **User**: `farmsetu_user` (or any name)
   - **Region**: Choose closest to your web service
   - **PostgreSQL Version**: 16 (or latest)
   - **Plan**: Free tier is fine for testing
4. Click **"Create Database"**
5. Wait for the database to be provisioned (takes 1-2 minutes)

### Step 2: Get the Database URL

1. Once created, click on your PostgreSQL database
2. In the **"Connections"** section, you'll see **"Internal Database URL"**
3. Copy the URL (it looks like: `postgresql://user:password@hostname:5432/dbname`)

### Step 3: Set Environment Variable in Your Web Service

1. Go to your **Web Service** (not the database)
2. Click on **"Environment"** tab
3. Click **"Add Environment Variable"**
4. Add:
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the Internal Database URL you copied
5. Click **"Save Changes"**

**Important**: Make sure you're adding this to your **Web Service**, not the database service.

### Step 4: Update Your Web Service Build Settings

Your web service should have these settings:

- **Root Directory**: `jash intern/farmsetu_weather`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn farmsetu_weather.wsgi:application`

### Step 5: Deploy and Run Migrations

After setting `DATABASE_URL`, Render will automatically redeploy. Once deployed:

1. Go to your Web Service dashboard
2. Click on **"Shell"** tab (or use **"Logs"** to see the deployment)
3. Once the service is running, open a **Shell** session
4. Run migrations:
   ```bash
   python manage.py migrate
   ```

### Step 6: Import Data

After migrations are complete, import the MetOffice data:

```bash
python manage.py import_metoffice https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt
```

You can import multiple datasets:
```bash
# Maximum temperature for UK
python manage.py import_metoffice https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt

# Minimum temperature for UK
python manage.py import_metoffice https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmin/date/UK.txt

# Rainfall for UK
python manage.py import_metoffice https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Rainfall/date/UK.txt
```

### Step 7: Verify Data is Loaded

1. Visit your Render app URL
2. You should now see regions and parameters in the dropdowns
3. The chart should display data when you select a parameter and region

## Summary of Changes Made

✅ **Updated `settings.py`**: Now uses PostgreSQL when `DATABASE_URL` is set, falls back to SQLite for local development

✅ **Updated `requirements.txt`**: Added `psycopg2-binary==2.9.10` for PostgreSQL support

## Environment Variables Checklist

Make sure these are set in your Render Web Service:

- ✅ `SECRET_KEY` - Your Django secret key
- ✅ `DEBUG` - Set to `0` for production
- ✅ `ALLOWED_HOSTS` - Your Render domain (e.g., `your-app.onrender.com`)
- ✅ `DATABASE_URL` - **NEW**: PostgreSQL connection string from your database service

## Troubleshooting

### If migrations fail:
- Check that `DATABASE_URL` is set correctly
- Verify the database is running (green status in Render dashboard)
- Check logs for connection errors

### If import fails:
- The MetOffice URLs are public and accessible from Render
- Check that `requests` package is installed (already in requirements.txt)
- Verify network connectivity in Render logs

### If data doesn't appear:
- Make sure you ran `python manage.py migrate` first
- Verify the import command completed successfully
- Check that you're querying the correct parameter/region combination

## Next Steps

After setup, your data will persist across deployments. The PostgreSQL database is separate from your web service, so your data won't be lost when you redeploy.

