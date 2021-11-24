FROM python:3.9.5

WORKDIR usr/src/flask_app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python -m unittest tests/test_scores.py
