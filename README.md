# Sinhala Subtitle Finder — Render Ready

A small Flask web app that searches Baiscope's publicly accessible Movies and TV Series catalogue pages for Sinhala-subtitle entries and presents matching source pages in a mobile-friendly interface.

## Deploy on Render

1. Put this project in a GitHub repository.
2. In Render, create **New → Web Service** and connect the repository.
3. Runtime: **Python 3**.
4. Build Command: `pip install -r requirements.txt`.
5. Start Command: `gunicorn app:app`.
6. Choose the Free plan if suitable, then deploy.

Render's Flask deployment docs use Gunicorn as the production server. See:
https://render.com/docs/deploy-flask

## Important limitation

This app uses normal public HTTP requests to read Baiscope catalogue pages. It does not bypass Cloudflare/anti-bot controls and does not retrieve copyrighted media itself. Baiscope may block automated requests, so search results may be empty or fail depending on the site's current access controls. A permitted/official API or integration may be needed for reliable production use.

## Local run

```bash
pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`.
