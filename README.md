# Prometheus - RSI Divergence Scanner (Web)

This repository wraps the existing `prometheus_2_1.py` logic in a small Flask web app with a mobile-friendly frontend.

Run locally:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# or cmd.exe:
.venv\Scripts\activate.bat
pip install -r requirements.txt

# IMPORTANT: set credentials before running
You can either edit `config.py` and set `USERNAME` and/or `PASSWORD`, or export environment variables:

```powershell
# Set password-only mode
setx PROMETHEUS_PASSWORD "yourpassword"

# (Optional) set username+password mode
setx PROMETHEUS_USERNAME "yourusername"
setx PROMETHEUS_PASSWORD "yourpassword"

# (Optional) set a Flask secret key
setx FLASK_SECRET_KEY "a-strong-secret"

python app.py
```
```

Open your browser to `http://127.0.0.1:5000` and log in with the password you set.

Notes:
- Scanning large stock groups can take several minutes (yfinance network calls). Consider scanning smaller groups or increasing concurrency.
- For production hosting, run behind a WSGI server (Gunicorn) and set `PROMETHEUS_PASSWORD` and `FLASK_SECRET_KEY` in the environment.
