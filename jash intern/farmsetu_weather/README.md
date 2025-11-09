# farmsetu_weather

A clean, production-like Django project that ingests summarised UK MetOffice datasets and exposes them via a REST API with a minimal Chart.js frontend for visualization.

## Features

- Management command to import MetOffice datasets
- Normalized data model with indexing for fast queries
- REST API endpoints for browsing, filtering, and statistics
- Root page renders a Chart.js line chart of annual averages
- Dockerfile and docker-compose for containerized development

## Requirements

- Python 3.10+ (tested with 3.12)
- pip
- (Optional) Docker & Docker Compose

## Setup (Local)

1. Create a virtual environment and install dependencies:

```powershell
# From the project root (contains manage.py)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Environment variables (optional for dev):

```powershell
Copy-Item .env.example .env
# Edit .env to set SECRET_KEY, DEBUG, ALLOWED_HOSTS as needed
```

3. Run migrations and start the server:

```powershell
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/ to see the homepage.

## Importing MetOffice Data

Use the management command to import a dataset. Example:

```powershell
python manage.py import_metoffice https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt
```

Notes:
- The command infers `parameter` (e.g., `Tmax`) and `region` (e.g., `UK`) from the URL.
- It parses the header row (Year, months, seasons, ANN) and stores each numeric cell as a `DataRecord`.
- The operation is idempotent thanks to a uniqueness constraint; re-running will skip duplicates.

## API Endpoints

- `GET /api/records/` — Paginated list of all records
- `GET /api/records/filter/?parameter=&region=&year=&column=` — Filtered list; any combination of parameters
- `GET /api/stats/?parameter=&region=` — Aggregated statistics across the selection

Examples:

```powershell
# All annual values for Tmax in UK
Invoke-WebRequest "http://127.0.0.1:8000/api/records/filter/?parameter=Tmax&region=UK&column=ANN" | Select-Object -Expand Content

# Stats for Tmax in UK
Invoke-WebRequest "http://127.0.0.1:8000/api/stats/?parameter=Tmax&region=UK" | Select-Object -Expand Content
```

## Docker

Run with Docker Compose (hot reloading through bind mount):

```powershell
docker compose up --build
```

Then visit http://127.0.0.1:8000/.

To import data inside the container:

```powershell
# Open an interactive shell in the web container
docker exec -it farmsetu_weather_web bash
python manage.py import_metoffice https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt
```

## Project Structure

- `farmsetu_weather/` — Django project settings and root URLs
- `metdata/` — App with models, admin, serializers, views, URLs, and management command
- `templates/index.html` — Simple Chart.js visualization page

## Quality Notes

- Type hints are used where practical
- Logging and idempotent imports ensure safe re-runs
- Indexes and unique constraints support performance and data integrity

## Troubleshooting

- If imports fail to parse, verify the dataset has a header line starting with `Year` and uses whitespace-separated numeric columns.
- If using Docker on Windows, ensure file sharing is enabled for the project drive.
